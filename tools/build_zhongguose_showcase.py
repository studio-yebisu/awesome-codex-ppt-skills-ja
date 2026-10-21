"""Build this Japanese case from the pinned Zhongguose template, not a shared deck generator."""
from pathlib import Path
import json, shutil, hashlib, difflib, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT/'examples/repositories/zhongguose-showcase' if (ROOT/'examples').exists() else ROOT
PIN = 'f4c2af8ff832133822afdce87ed2d6d760631ef4'
REPO = 'tanglele110-hash/zhongguose-ppt-skill'
TITLES = ['町の手仕事を、ひらく。','つくる人に、会いに行く。','一つの町を、三つの道で。','気になる手仕事で、少し止まる。','持ち帰るのは、次のきっかけ。','手仕事の名前を、一つ覚える。']

def write(path, text):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8')
def dump(path, obj): write(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def chrome(n, chapter):
    labels = [('見つける','DISCOVER'),('めぐる','WALK'),('持ち帰る','TAKE HOME')]
    tabs=''.join(f'<span class="tab{" active" if j==chapter else ""}"'+(' aria-current="step"' if j==chapter else '')+f'>{j+1:02} {ja} <small>{en}</small></span>' for j,(ja,en) in enumerate(labels))
    return f'<div class="chrome-min"><div class="l section-tabs">{tabs}</div><div class="r">{n:02} / 06</div></div>'

def build():
    source=CASE/'source'; up=source/'upstream'; skill=up/'skills/zhongguose-ppt-skill'
    template=skill/'assets/template-zhongguose'
    shutil.copytree(template/'assets',CASE/'assets',dirs_exist_ok=True)
    fonts=source/'fonts'
    for family in ['shipporimincho','bizudpgothic','manrope']:
        dest=fonts/family
        if not dest.exists(): shutil.copytree(ROOT/'downloads/fonts'/family,dest)
        shutil.copytree(dest,CASE/'assets/fonts'/family,dirs_exist_ok=True)
    original=(template/'index.html').read_text(encoding='utf-8')
    pages=[]
    pages.append('''<section class="slide accent" data-role="cover" data-animate="hero" data-layout="SWISS-COVER-ASCII">
    <div class="canvas-card"><canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min"><div class="l">手仕事のある町を歩く</div><div class="r">01 / 06</div></div>
    <div class="craft-cover"><div data-anim="kicker" class="t-meta">A WALK THROUGH LOCAL CRAFT</div>
    <div data-anim="title"><h1 class="cover-title">町の手仕事を、<br>ひらく。</h1><p class="hero-subtitle">見つける。めぐる。持ち帰る。</p></div>
    <div data-anim="bottom" class="craft-cover-foot"><span>暮らしのそばにある、つくる仕事へ。</span><span class="t-meta">回遊の体験提案</span></div></div></div></section>''')
    cols=''
    for num,kanji,ja,en,body in [('01','染','色が生まれる','DYE','布に重なる色を、眺める。'),('02','織','糸がつながる','WEAVE','縦と横の糸を、たどる。'),('03','土','かたちが残る','CLAY','手に沿うかたちを、探す。')]:
        cols+=f'<div data-anim="up" class="wn-col"><span class="wn-pill">{num} {en}</span><div class="craft-glyph">{kanji}</div><h3>{ja}</h3><p class="craft-body">{body}</p></div>'
    pages.append(f'<section class="slide light" data-animate="why-now" data-layout="PRINCIPLES"><div class="canvas-card">{chrome(2,0)}<header data-anim="head"><h2 class="craft-heading">{TITLES[1]}</h2><p class="craft-body craft-intro">まずは、気になる手仕事を一つ。</p></header><div class="why-now-grid craft-principles">{cols}</div></div></section>')
    rows=''
    for n,route,en,description,word in [('01','色の道','COLOR','染まる布を入口に、色の違いを見つける。','染'),('02','糸の道','THREAD','織り目を入口に、つながりをたどる。','織'),('03','土の道','FORM','器を入口に、手に沿うかたちを探す。','土')]:
        rows+=f'<div data-anim="row" class="ledger-row craft-route"><span class="ledger-num">{n}</span><div><h3 class="ledger-label">{route} <small>{en}</small></h3><p class="craft-body">{description}</p></div><span class="route-end">{word}</span></div>'
    pages.append(f'<section class="slide light" data-animate="stacked-ledger" data-layout="LEDGER"><div class="canvas-card">{chrome(3,1)}<header data-anim="head"><h2 class="craft-heading">{TITLES[2]}</h2></header><div class="stacked-ledger craft-routes">{rows}</div><p class="craft-note" data-anim="foot">概念ルート。実際の地図や順路を示すものではありません。</p></div></section>')
    pages.append(f'''<section class="slide light" data-animate="duo-mirror" data-layout="DUO"><div class="canvas-card">{chrome(4,1)}<header data-anim="head"><h2 class="craft-heading">気になる手仕事で、<br>少し止まる。</h2></header>
    <div class="duo-compare craft-duo"><div class="col" data-anim="left"><span class="t-meta">LOOK</span><h3 class="col-ttl">見る</h3><p class="craft-body">色、織り目、手触り。<br>気づいた違いを、言葉にしてみる。</p><div class="craft-observation">どこに、目が止まった？</div></div><div class="vrule"></div>
    <div class="col" data-anim="right"><span class="t-meta">TALK</span><h3 class="col-ttl">話す</h3><p class="craft-body">素材や道具、かたちのこと。<br>聞いてみたいことを、一つ。</p><div class="craft-observation">何を、聞いてみたい？</div></div></div></div></section>''')
    things=''
    for n,name,en,desc in [('01','冊子','BOOKLET','見つけた手仕事を、あとで読み返す。'),('02','小片','SMALL PIECE','色や手触りを、暮らしのそばへ。'),('03','メモ','NOTE','気づいたことを、自分の言葉で残す。')]:
        things+=f'<div class="craft-step" data-anim="up"><span class="t-meta">{n} / {en}</span><h3>{name}</h3><p class="craft-body">{desc}</p></div>'
    pages.append(f'<section class="slide light" data-animate="timeline-walk" data-layout="SEQUENCE"><div class="canvas-card">{chrome(5,2)}<header data-anim="head"><h2 class="craft-heading">持ち帰るのは、<br>次のきっかけ。</h2></header><div class="craft-sequence">{things}</div><p class="craft-note" data-anim="foot">冊子・小片・メモは、体験を持ち帰るための提案です。</p></div></section>')
    pages.append('''<section class="slide split" data-role="closing" data-animate="split-statement" data-layout="S10"><div class="canvas-card"><div class="split-half" style="width:100%;height:100%">
    <div class="half b-accent"><canvas class="ascii-bg" aria-hidden="true"></canvas><div class="t-meta">TAKE HOME</div><h2 class="cover-title craft-closing" data-anim="title">手仕事の<br>名前を、<br>一つ覚える。</h2><p class="craft-body">町とのつながりを、暮らしへ。</p></div>
    <div class="half">'''+chrome(6,2)+'''<div class="craft-close-copy" data-anim="right"><div class="t-meta">AFTER THE WALK</div><p>今日、気になった<br>手仕事は？</p><div class="craft-memory-line"></div><span class="craft-body">名前を一つ、書きとめる。</span></div><p class="craft-note">架空の回遊体験案</p></div></div></div></section>''')
    # Round4 chapter-divider: original S09 structure, local Japanese chapter labels.
    pages.insert(1, f"""<section class="slide light" data-animate="field-notes" data-layout="S09"><div class="canvas-card">{chrome(2,0)}<div class="section-divider-body"><span class="dot-mat xl section-divider-dot"></span><span class="ring-mat section-divider-ring"></span><div data-anim="up" class="section-divider-stack"><h1 class="section-divider-title">01 見つける<span class="section-divider-caption">気になる手仕事を一つ選ぶ</span></h1></div></div></div></section>""")
    import re
    pages=[re.sub(r'\d{2} / 06',f'{i+1:02} / 07',page) for i,page in enumerate(pages)]
    joined='\n\n'.join(pages)
    write(source/'slides.html',joined)
    css='''
/* Japanese adaptation: local fonts, paired upstream Chinese color, case-specific pattern tuning. */
@font-face{font-family:"Craft Serif";src:url("./assets/fonts/shipporimincho/ShipporiMincho-Regular.ttf");font-display:block}
@font-face{font-family:"Craft Body";src:url("./assets/fonts/bizudpgothic/BIZUDPGothic-Regular.ttf");font-display:block}
@font-face{font-family:"Craft Latin";src:url("./assets/fonts/manrope/Manrope[wght].ttf");font-weight:200 800;font-display:block}
:root{--accent:#9E3B3B;--accent-rgb:158,59,59;--accent-on:#ffffff;--accent-bright:var(--accent);--zh-title:"Craft Serif",serif;--zh-body:"Craft Body",sans-serif;--zh-cover-title:"Zhongguose Cover","Craft Serif",serif;--latin-display:"Craft Latin","Craft Body",sans-serif;--mono:"Craft Latin","Craft Body",sans-serif;--sans-zh:var(--zh-body)}
.section-tabs{font-family:"Craft Body",sans-serif!important;font-size:clamp(13px,.9vw,19px);gap:1.6vw}.section-tabs small{font:500 .65em "Craft Latin";margin-left:.4em;letter-spacing:.08em}.section-tabs .tab:not(.active){opacity:1;color:#66625a}.half.b-accent > .t-meta{color:var(--accent-on);opacity:1}
.craft-cover{flex:1;display:grid;grid-template-rows:auto 1fr auto;gap:3vh}.craft-cover>div:nth-child(2){align-self:center}.craft-cover .cover-title{font-size:min(9vw,17vh);line-height:1.24;font-weight:400;letter-spacing:.015em}.craft-cover .hero-subtitle{font-size:clamp(21px,1.65vw,34px);margin-top:3vh;opacity:.88}.craft-cover-foot{border-top:1px solid rgba(255,255,255,.4);padding-top:2.5vh;display:flex;justify-content:space-between;font-size:clamp(17px,1.1vw,25px)}
.craft-heading{font-size:clamp(36px,4vw,78px);line-height:1.28;font-weight:400;letter-spacing:.01em}.craft-body{font-family:var(--zh-body)!important;font-size:clamp(21px,1.5vw,31px);line-height:1.65;opacity:.84}.craft-intro{margin-top:2vh}.craft-note{font-family:var(--zh-body);font-size:clamp(15px,.94vw,20px);line-height:1.5;color:var(--text-helper);margin-top:3vh}.craft-principles{margin-top:5vh;gap:4vw}.craft-glyph{font-family:"Craft Serif";font-size:min(9vw,18vh);line-height:1.4;color:var(--accent);margin-top:2vh}.craft-principles h3{font-family:"Craft Serif";font-size:clamp(26px,2.3vw,46px);font-weight:400}.craft-principles .wn-col{border-bottom:1px solid var(--border-subtle);padding-bottom:4vh;gap:2vh}
.craft-routes{margin-top:5vh;gap:1vh}.craft-route{grid-template-columns:1fr 7fr 1fr;gap:3vw;padding:3vh 0}.craft-route .ledger-num{font-size:min(5vw,9vh);color:var(--accent)}.craft-route .ledger-label{font-family:"Craft Serif"!important;font-size:clamp(30px,2.5vw,48px)}.craft-route small{font:500 .38em "Craft Latin";letter-spacing:.12em;vertical-align:middle;margin-left:1em}.craft-route p{margin-top:1vh}.route-end{font-family:"Craft Serif";border:1px solid var(--accent);color:var(--accent);font-size:clamp(27px,2.3vw,45px);display:grid;place-content:center;width:4.7vw;height:4.7vw}
.craft-duo{margin-top:5vh;gap:0 4vw}.craft-duo .col{gap:2vh}.craft-duo .col-ttl{font-size:min(6.4vw,12vh);color:var(--accent);font-weight:400}.craft-observation{margin-top:auto;font-family:"Craft Serif";font-size:clamp(26px,2.4vw,45px);border-top:2px solid var(--accent);padding:3vh 0}.craft-sequence{display:grid;grid-template-columns:repeat(3,1fr);gap:3vw;margin-top:auto}.craft-step{border-top:2px solid var(--accent);padding:3vh 0}.craft-step h3{font-family:"Craft Serif";color:var(--accent);font-weight:400;font-size:min(5.5vw,10vh);margin:3vh 0}.craft-closing{font-size:min(5.8vw,11vh);line-height:1.35;font-weight:400;margin:auto 0;letter-spacing:.01em}.craft-close-copy{margin:auto 0}.craft-close-copy p{font-family:"Craft Serif";font-size:min(4.6vw,8vh);line-height:1.4;margin:4vh 0}.craft-memory-line{height:1px;background:var(--accent);margin:4vh 0;width:100%}.craft-closing+.craft-body{color:var(--accent-on)}
.slide .craft-heading,.craft-duo .col-ttl{font-family:var(--zh-title)!important}.slide h2.cover-title{font-family:var(--zh-cover-title)!important}
/* Protect the cover chapter label from the animated ASCII canvas only beneath its ink. */
.slide[data-role="cover"] .chrome-min{z-index:3}.slide[data-role="cover"] .chrome-min .l{background:var(--accent);padding:7px 12px;margin:-7px -12px}
'''
    css+='\n/* Round4 chapter/reading repairs; original paginator/motion/ASCII remain. */\n.section-divider-title{font-family:var(--zh-title)!important;font-size:min(7vw,13vh);font-weight:400;line-height:1.25}\n.section-divider-caption{font-family:var(--zh-body);font-size:clamp(26px,2.5vw,44px)!important;margin-top:32px!important}\n.craft-cover .hero-subtitle{text-align:left;margin-left:0}\n.craft-sequence{margin-top:6vh}\n.slide[data-role="closing"] .section-tabs{font-size:clamp(18px,1.2vw,24px);gap:22px}\n.slide[data-role="closing"] .section-tabs .tab{display:flex;flex-direction:column;gap:5px;white-space:nowrap}\n.slide[data-role="closing"] .section-tabs small{font-size:16px;margin-left:0;letter-spacing:.03em}\nbody.dark-bg #nav .dot.active{background:#ffffff;outline:1px solid #ffffff}\n'
    write(source/'adaptation.css',css)
    start=original.index('<section class="slide '); end=original.rindex('</section>')+len('</section>')
    html=original[:start]+joined+original[end:]
    import re
    html=re.sub(r'<link[^>]+(?:fonts.googleapis.com|fonts.gstatic.com)[^>]*>\n?', '', html)
    html=html.replace('<html lang="zh-CN">','<html lang="ja">').replace('<title>中国色 PPT 模板 · 示例</title>',f'<title>{TITLES[0]}</title>')
    html=html.replace('</style>',css+'\n</style>',1)
    html=html.replace('/* 图片占位符统一规范：浅绿底、无边框；多图之间固定间距 */','/* Original image-surface tokens: pale green, no border, consistent spacing. */')
    # The complete original paginator is preserved. This adapter calls its public entrypoint.
    bridge='''<script>
// Same-origin 0-based catalog adapter. Native jumpTo/easing/input controller retained.
window.__slideCatalogGo = i => {if(Number.isInteger(i)&&i>=0&&i<document.querySelectorAll('#deck>.slide').length)window.__jumpToPage(i)};
window.__slideCatalogCurrent = () => window.__pageIndex || 0;
function catalogNotify(){if(parent!==window&&location.origin!=='null')parent.postMessage({type:'yebisu-page',index:window.__slideCatalogCurrent()},location.origin)}
addEventListener('message', e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide')window.__slideCatalogGo(e.data.index)});
new MutationObserver(catalogNotify).observe(document.getElementById('nav'),{subtree:true,attributes:true,attributeFilter:['class']});catalogNotify();
</script>'''
    html=html.replace('</body>',bridge+'\n</body>')
    write(CASE/'index.html',html)
    write(source/'template-ja.patch',''.join(difflib.unified_diff(original.splitlines(True),html.splitlines(True),fromfile='upstream/assets/template-zhongguose/index.html',tofile='index.html')))
    # Local font adaptation of the actual upstream subset generator. Preserve original separately.
    old=(skill/'scripts/subset-cover-font.py').read_text(encoding='utf-8')
    changed=old.replace('Copyright (c) 2020, Lingdong Huang. Modified and redistributed under SIL OFL 1.1.','Copyright 2021 The Shippori Mincho Project Authors. Modified and redistributed under SIL OFL 1.1.')
    changed=changed.replace('Reserved Font Name QIJI','Reserved Font Name Shippori Mincho')
    changed=changed.replace('"source_archive_sha256": SOURCE_ARCHIVE_SHA256,','"source_archive_sha256": None,')
    changed=changed.replace('"source_ttf_sha256": ORIGINAL_TTF_SHA256,','"source_ttf_sha256": sha256_bytes((SKILL_DIR / "assets/font-sources/ShipporiMincho-Regular.ttf").read_bytes()),')
    changed=changed.replace('if missing_cover_han:', 'if missing_cover:').replace('sorted(missing_cover_han)[:24]','sorted(missing_cover)[:24]').replace('cover-title Han characters','cover-title characters (including Japanese kana)')
    runtime=source/'japanese-runtime';write(runtime/'scripts/subset-cover-font.py',changed)
    for path in ['ShipporiMincho-Regular.ttf','OFL.txt']:
        dest=runtime/'assets/font-sources'/('OFL-1.1.txt' if path=='OFL.txt' else path);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(fonts/'shipporimincho'/path,dest)
    write(runtime/'assets/font-sources/FONT-NOTICE.txt','Zhongguose Cover: deck-specific modified subset from Shippori Mincho Regular.\nSource: google/fonts @66928797f271fed5ee428544e7229685e2d90127.\nCopyright 2021 The Shippori Mincho Project Authors. SIL OFL 1.1.\nFull unmodified TTF and original OFL accompany source/fonts/shipporimincho/.\nThe pinned qiji seed font and notices are retained only in source/upstream; qiji is not used for Japanese display.\n')
    write(source/'subset-japanese.patch',''.join(difflib.unified_diff(old.splitlines(True),changed.splitlines(True),fromfile='upstream/scripts/subset-cover-font.py',tofile='japanese-runtime/scripts/subset-cover-font.py')))
    subprocess.run([sys.executable,str(runtime/'scripts/subset-cover-font.py'),str(CASE/'index.html'),'--source-font',str(fonts/'shipporimincho/ShipporiMincho-Regular.ttf')],check=True)
    refs=[]
    for p in sorted(up.rglob('*')):
        if p.is_file():
            rel=p.relative_to(up).as_posix();refs.append({'path':rel,'preserved_path':'source/upstream/'+rel,'sha256':digest(p),'url':f'https://github.com/{REPO}/blob/{PIN}/{rel}'})
    fontrefs=[]
    for p in sorted(fonts.rglob('*.ttf')):
        rel=p.relative_to(fonts).as_posix();fontrefs.append({'path':'source/fonts/'+rel,'sha256':digest(p),'modified':False,'license':'OFL-1.1','commit':'66928797f271fed5ee428544e7229685e2d90127','url':'https://raw.githubusercontent.com/google/fonts/66928797f271fed5ee428544e7229685e2d90127/ofl/'+rel})
    dump(source/'FONT-SOURCE.json',fontrefs)
    dump(CASE/'PROVENANCE.json',{'repository':REPO,'commit':PIN,'license':'MIT','copyright':'2026 木渡川','source_refs':refs,'fonts':fontrefs,'method':'source logic → locked manuscript → slide architecture → real upstream template copy → local Japanese typography/color/content patch → original cover subset generator adapted and executed','original_runtime_retained':['vertical paginator','wheel/key/click/touch','Esc overview','B static mode','ASCII canvas','Motion helpers','local lucide'],'output':'index.html + assets/ (multi-file web deck)','confirmation':'Parent/user authorized autonomous topic/theme and six content pages plus an added chapter divider, authorized by the later skill-effect repair; extra original theme/gallery confirmation skipped within that authorization','not_exercised':['PPTX','independent current-version scoring/review','touch','overview','catalog parent integration']})
    if (ROOT/'examples').exists(): shutil.copyfile(Path(__file__),source/'rebuild.py')
    print('Built seven-slide Japanese Zhongguose web deck, original template runtime and executed cover subset.')

def package():
    for name,folder in [('zhongguose-example-ja.zip',CASE),('zhongguose-ja.zip',ROOT/'skill-forks/zhongguose-ja')]:
        with zipfile.ZipFile(ROOT/'downloads'/name,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(folder.rglob('*')):
                if p.is_file() and '__pycache__' not in p.parts:z.write(p,folder.name+'/'+p.relative_to(folder).as_posix())

if __name__=='__main__':
    if '--package' in sys.argv:package()
    else:build()
