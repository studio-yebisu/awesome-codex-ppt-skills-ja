"""Fill FeeiCN's original template; execute its branding, image inliner and smoke test."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
import argparse, base64, hashlib, html, json, os, re, shutil, subprocess, sys
from fontTools import subset
from fontTools.ttLib import TTFont

HERE=Path(__file__).resolve()
DEFAULT=HERE.parents[1]/'examples/repositories/slide-writer/input/data.json'
if not DEFAULT.exists(): DEFAULT=HERE.parents[1]/'input/data.json'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input',type=Path,default=DEFAULT)
args=parser.parse_args()
input_path=args.input.resolve(); case=input_path.parent.parent
data=json.loads(input_path.read_text(encoding='utf-8'))
raw=case/'source/upstream'; work=case/'source/working-upstream'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')

def dump(path,value): write(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')

receipts=[]
def run(argv):
    r=subprocess.run([str(a) for a in argv],cwd=case,capture_output=True,text=True,encoding='utf-8',errors='replace')
    log=case/f'source/logs/{len(receipts)+1:02d}-{Path(str(argv[1])).stem}.log'
    write(log,r.stdout+'\n'+r.stderr)
    receipts.append({'argv':[str(a) for a in argv],'cwd':str(case),'exit_code':r.returncode,'log':log.relative_to(case).as_posix(),'log_sha256':sha(log)})
    dump(case/'source/execution-receipts.json',receipts)
    if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
    print(r.stdout.strip())

for f in raw.rglob('*'):
    if f.is_file():
        target=work/f.relative_to(raw);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
source_template=raw/'template.html'
target=case/'index.html';shutil.copyfile(source_template,target)
theme_css=data['theme_css']
write(work/'themes/shiori.md','# しおり：架空のチーム用の独自テーマ\n\n## CSS\n\n```css\n'+theme_css+'\n```\n')
for variant,color in [('color','#174D44'),('white','#FFFFFF')]:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="160" height="40" viewBox="0 0 160 40"><path d="M6 5h24v30L18 27 6 35z" fill="{color}"/><text x="42" y="28" font-family="sans-serif" font-size="24" font-weight="700" fill="{color}">SHIORI</text></svg>'
    write(work/f'themes/logos/shiori-{variant}.txt','data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode())
run([sys.executable,work/'scripts/apply-template-branding.py',target,'--title',data['title'],'--speaker',data['speaker'],'--theme-id','shiori'])

icons_source=(raw/'icons.md').read_text(encoding='utf-8')
def icon(name):
    match=re.search(r'\*\*'+re.escape(name)+r'\*\*\s*(<svg.*?</svg>)',icons_source)
    if not match:raise ValueError('Original icon missing: '+name)
    return match.group(1).replace('<svg ','<svg aria-hidden="true" ')

content='\n'.join(s['html'] for s in data['slides'])
for name in ['file-text','check-circle','message-circle','edit']:
    content=content.replace('{{icon:'+name+'}}',icon(name))
assert '{{' not in content,'Unresolved content placeholder'
document=target.read_text(encoding='utf-8').replace('<!-- %%SLIDES%% -->',content)
assert document.count('<section class="slide ')==len(data['slides'])
translations={'lang="zh-CN"':'lang="ja"','幻灯片导航':'ページの移動','全屏播放 (F)':'全画面で表示 (F)',
    '* 仅限内部交流使用，如需公开请联系作者。':'架空のチームの提案例。実施効果は未測定。',
    ' 翻页 &nbsp;·&nbsp; ':' ページ移動 &nbsp;·&nbsp; ','</kbd> 全屏':'</kbd> 全画面',
    '`跳到第 ${i + 1} 张`':'`${i + 1}ページ目`'}
for old,new in translations.items():
    assert old in document,old
    document=document.replace(old,new)
document=document.replace('    new MiniSlidePresentation();','    window.slideWriterPresentation = new MiniSlidePresentation();')
document=document.replace("this.slides[index].scrollIntoView({ behavior: 'smooth' });", "this.slides[index].scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });")
assert 'window.slideWriterPresentation' in document
font_css=[];font_reports=[]
font_records=json.loads((case/'source/font-sources.json').read_text(encoding='utf-8'))
font_text=document+data['draft']+''.join(chr(i) for i in range(32,127))
for record in font_records:
    source=case/'source/.cache'/Path(record['source_url']).name
    if not source.exists():
        source.parent.mkdir(parents=True,exist_ok=True)
        with urlopen(Request(record['source_url'],headers={'User-Agent':'Yebisu-slide-writer'}),timeout=45) as r:source.write_bytes(r.read())
    assert sha(source)==record['source_sha256']
    font=TTFont(source,recalcTimestamp=False)
    missing={ord(ch) for ch in font_text if ch.isprintable() and ord(ch) not in font.getBestCmap()}
    # XML/JavaScript comments can contain Chinese glyphs; include every supported glyph and require all Japanese page text.
    visible=re.sub('<[^>]+>','',content)
    assert all(ord(ch) in font.getBestCmap() for ch in html.unescape(visible) if ch.isprintable()),missing
    options=subset.Options();options.name_IDs=['*'];options.name_languages=['*']
    sub=subset.Subsetter(options=options);sub.populate(text=font_text);sub.subset(font)
    weight=700 if 'Bold' in source.name else 400
    for name in font['name'].names:
        if name.nameID in {1,2,3,4,6,16,17}:
            value={2:'Bold' if weight==700 else 'Regular',17:'Bold' if weight==700 else 'Regular',6:'YebisuSlideWriterJP'+str(weight)}.get(name.nameID,'Yebisu Slide Writer JP')
            name.string=value.encode(name.getEncoding(),errors='replace')
    out=case/f'fonts/slide-writer-{weight}.woff2';out.parent.mkdir(parents=True,exist_ok=True)
    font.flavor='woff2';font.save(out)
    encoded=base64.b64encode(out.read_bytes()).decode()
    font_css.append("@font-face{font-family:'SlideWriterJP';src:url(data:font/woff2;base64,"+encoded+") format('woff2');font-weight:"+str(weight)+";font-display:swap}")
    font_reports.append({**record,'subset_sha256':sha(out),'renamed_family':'Yebisu Slide Writer JP','file':out.relative_to(case).as_posix()})
dump(case/'fonts/SOURCE.json',font_reports)
extra_css="\n".join(font_css)+"\n:root{--font:'SlideWriterJP',sans-serif} .slide-header .header-title{font-size:clamp(1.25rem,3vw,2.25rem);line-height:1.4}.cover-title{line-height:1.45}.slide-body{padding-bottom:clamp(3rem,8vh,5rem)} .meeting-example{font-size:var(--body-size);line-height:1.9} .meeting-example p+p{margin-top:1rem} .roadmap-svg{width:100%;height:auto;max-height:45vh}.roadmap-svg text{font-family:var(--font)}"
document=document.replace('</head>','<style>'+extra_css+'</style>\n</head>')
document=document.replace('</head>',"<style>:root{--body-size:clamp(.9rem,1.8vw,1.25rem)}.card-title,.step-title{font-size:clamp(1.1rem,2vw,1.35rem);line-height:1.4}@media(prefers-reduced-motion:reduce){.reveal,.reveal-left{animation:none!important;opacity:1!important;transform:none!important}*{animation-delay:0ms!important;transition-delay:0ms!important}}</style>\n</head>")
# Keep original scroll/observer runtime; bridge it to the catalog without replacing its page engine.
bridge='''<script>
document.addEventListener('DOMContentLoaded',()=>{
 const deck=window.slideWriterPresentation;
 const send=()=>{if(parent!==window)parent.postMessage({type:'yebisu-page',index:deck.currentIndex,total:deck.totalSlides},location.origin)};
 const progress=deck.updateProgress.bind(deck);deck.updateProgress=i=>{progress(i);send()};
 window.addEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;deck.goTo(e.data.index)});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&parent!==window)parent.postMessage({type:'yebisu-close'},location.origin)});
 send();
});
</script>'''
document=document.replace('</body>',bridge+'\n</body>')
licenses={name:(case/path).read_text(encoding='utf-8') for name,path in [('slide-writer MIT','LICENSE.upstream'),('Feather MIT','source/LICENSE.feather'),('BIZ UDPGothic OFL','fonts/OFL.txt')]}
document=document.replace('</head>','<script type="application/json" id="artifact-licenses">'+json.dumps(licenses,ensure_ascii=False).replace('</','<\\/')+'</script>\n</head>')
write(target,document)
run([sys.executable,work/'scripts/inline-images.py',target])
git=shutil.which('git')
bash_candidates=[Path(git).parent.parent/'bin/bash.exe' if git else Path('not-found'),Path('C:/Program Files/Git/bin/bash.exe')]
bash=next((p for p in bash_candidates if p.exists()),None)
if bash is None:raise SystemExit('Git Bash is needed to run the unmodified original smoke-test.sh')
msys=lambda p:'/'+p.drive[0].lower()+'/'+p.as_posix().split(':',1)[1].lstrip('/') if p.drive else p.as_posix()
run([bash,msys(work/'scripts/smoke-test.sh'),msys(target)])
reference_names=json.loads((case/'source/original-source.json').read_text(encoding='utf-8'))['files']
references=[{'path':name,'sha256':sha(raw/name)}for name in reference_names]
pin=json.loads((case/'source/original-source.json').read_text(encoding='utf-8'))
provenance={'repository':'FeeiCN/slide-writer','upstream_commit':pin['commit'],'method':'原典template.htmlを複製し、Mode A1の構成・コンポーネントで日本語原稿を配置。無改変のapply-template-branding.py、inline-images.py、smoke-test.shを実行。固有MiniSlidePresentationで再生。',
 'execution_type':'original_template_branding_inlining_smoke_japanese_fork','references':references,'commands_executed':receipts,'artifact_sha256':sha(target),'input_sha256':sha(input_path),
 'original_refresh_during_production':'source/refresh-receipt.json','changes':['架空ブランドの独自themeと自作logoを原典branding CLIへ渡す。','BIZ UDPGothicのOFLサブセットを別内部名で単一HTMLへ埋め込む。','日本語の操作ラベル、読みやすい改行、原典runtimeと外側カウンターの接続。'],
 'scope':'原典の実装と工程を使った日本語8枚の指示型スキル作例。14企業テーマ全種の動作・効果・人の採用は未確認。再現は固定原典で行い、自動更新しない。ブラウザーの安全ポリシーによりfile://直接起動は未確認、原典の全工程完走とは記録しない。','checked_at':datetime.now(timezone.utc).isoformat()}
dump(case/'PROVENANCE.json',provenance)
dump(case/'QA.json',{'status':'generated_awaiting_review','page_count':len(data['slides']),'artifact_sha256':sha(target),'human_adoption':'pending','production_adoption':False,'publication':False})
write(case/'NOTES.md','\n\n'.join('## '+str(i+1)+'. '+s['title']+'\n\n'+s['notes']for i,s in enumerate(data['slides']))+'\n')
print(f'Original smoke-test: passed ({len(data["slides"])} slides). Rebuilt output needs browser review: {target}')
