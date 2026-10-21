"""Execute ai-business-skills 43's brief -> square HTML concept-preview instructions.

The original skill is an instruction workflow, with no renderer or PPTX CLI.
This dedicated preview authoring code is not the catalog's common renderer.
"""
from pathlib import Path
import argparse, hashlib, html, json, shutil, sys, urllib.request
from datetime import datetime, timezone
from fontTools.ttLib import TTFont
from fontTools import subset

ROOT = Path(__file__).resolve().parents[1]
REPO = 'minhnv0807/ai-business-skills'
COMMIT = '0360adced422a08f70c3eff8905b81962872105d'
IDENT = 'business-carousel'
FONT_PIN = '66928797f271fed5ee428544e7229685e2d90127'
SOURCE_REFS = ['LICENSE', 'skills/en/43-carousel-brief-global/SKILL.md']
DATA = {
    'title': '引き継ぎ、何を書けばいい？',
    'brand': 'しおり / 仕事の小さなメモ',
    'purpose': '初めて引き継ぎメモを書く人へ、記入の入口を示す教育用カルーセル',
    'channel': 'SNSカルーセルの構成確認用',
    'funnel': 'TOFU / 初めて知る人への説明',
    'notice': '架空ブランドの構成確認用プレビュー。効果の実績やSNS公開用の完成データではありません。',
    'copy_review': {'status': 'agent_reviewed_for_demo', 'reviewer': 'Codex /root', 'human_approval': 'pending',
                    'scope': '図案作成前に6枚の日本語原稿を確認。1枚1論点、例と実績の区別、最後の具体的な行動を確認。'},
    'slides': [
        {'role': 'HOOK', 'headline': '引き継ぎ、\n何を書けばいい？', 'body': '詳しく書く前に、\n次の人が動ける3点を。', 'visual': '3本の記入線を持つメモのベクトル図',
         'note': 'SNSの教育用コンセプトです。引き継ぎ方法を万能な規則として示さず、書き始めるための3点を提案します。'},
        {'role': 'PROBLEM', 'headline': '「よろしく」だけでは、\n次の一手が見えない。', 'body': '終わったことと、残ること。\n読む人には、どちらも必要。', 'visual': '一言のメモと空欄の次の作業を対比',
         'note': '一言の依頼だけでは、相手が作業の状態を理解しにくい場面を示す架空例です。実際の職場で測定した結果ではありません。'},
        {'role': 'INSIGHT', 'headline': '書くのは、\n目的・次の一手・相談先。', 'body': '全部の経緯より、\n迷ったときの入口を残す。', 'visual': '3点を番号付きの縦カードにする',
         'note': 'このプレビューでは、目的、次の作業、相談する担当という3点を記入型として提案します。詳細な手順書が必要な仕事には追加の情報も必要です。'},
        {'role': 'SOLUTION', 'headline': '今日の作業を、\n3行のメモにする。', 'body': '目的は何か。次に何をするか。\n迷ったら誰に聞くか。', 'visual': '各項目に短い質問を置く記入フォーム',
         'note': '目的、次の一手、相談先という項目を自分の仕事に置き換えます。個人情報や秘密をSNSへ投稿する案内ではありません。'},
        {'role': 'EXAMPLE', 'headline': 'たとえば、\n資料の確認を頼むなら。', 'body': '読む人が、次に動けるか。\n記入例で確かめる。', 'visual': '架空の資料確認メモを3項目で示す',
         'note': '例は、会議前に資料を確認し、単位の表記を揃え、迷ったら作成担当へ聞く、という架空の記入例です。証言や改善実績の代わりに作例で示しています。'},
        {'role': 'CTA', 'headline': 'まず1件、\nメモを書いてみよう。', 'body': '目的・次の一手・相談先。\nこの型から始める。', 'visual': '記入型をコピーする実ボタンとメモのベクトル図',
         'note': 'CTAのボタンは記入型をクリップボードへコピーします。自分の作業に書き換え、必要な相手へ渡す前に内容を確認してください。外部への送信はしません。'}
    ]
}

CSS = '''
@font-face{font-family:ShioriJP;src:url(fonts/carousel-regular.woff2) format("woff2");font-weight:400;font-display:block}
@font-face{font-family:ShioriJP;src:url(fonts/carousel-bold.woff2) format("woff2");font-weight:700;font-display:block}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{font-family:ShioriJP,sans-serif;background:#e3e8e1;color:#142525}
#deck{position:absolute;width:1080px;height:1080px;left:50%;top:50%;transform-origin:center;overflow:hidden;background:#f6f3eb}
.slide{position:absolute;inset:0;display:none;padding:68px 76px 142px;background:#f6f3eb}
.slide.is-active{display:flex;flex-direction:column}.slide.dark{background:#142525;color:#f6f3eb}
.brand{display:flex;align-items:center;gap:16px;font-size:24px;letter-spacing:.04em;line-height:1.4}
.brand svg{width:30px;height:32px}.preview-label{margin-left:auto;font-size:21px;border:1px solid currentColor;padding:7px 13px}
.eyebrow{font-size:24px;letter-spacing:.12em;margin:58px 0 21px;color:#a83b25}.dark .eyebrow{color:#f6f3eb}
h1{font-weight:700;font-size:75px;line-height:1.28;letter-spacing:-.04em;margin:0;white-space:pre-line}
.body-copy{font-size:35px;line-height:1.65;white-space:pre-line;margin:27px 0 0;max-width:920px}
.visual{flex:1;display:flex;flex-direction:column;justify-content:center;gap:17px;min-height:200px;padding-top:24px}
.note-svg{width:450px;height:270px;align-self:flex-end;color:currentColor}.note-svg line{stroke-width:7}
.row{display:flex;align-items:center;gap:24px;border-top:2px solid currentColor;padding:18px 0;font-size:32px;line-height:1.5}
.row strong{color:#a83b25;min-width:138px;font-weight:700}.row span{max-width:675px}.row:last-child{border-bottom:2px solid currentColor}
.question{display:grid;grid-template-columns:1fr 1fr;gap:22px}.question>div{border:2px solid currentColor;border-radius:22px;padding:28px;font-size:35px;line-height:1.5}.question p{margin:10px 0 0;font-size:27px}.missing{border-style:dashed!important}
.example-label{font-size:23px;letter-spacing:.1em;color:#a83b25;margin-bottom:0}
.copy-template{font:inherit;font-size:31px;font-weight:700;align-self:flex-start;color:#142525;background:#f6f3eb;border:2px solid #f6f3eb;padding:20px 27px;cursor:pointer;border-radius:10px}
.copy-template:focus-visible{outline:4px solid #f6f3eb;outline-offset:7px}.copy-state{font-size:26px;min-height:40px;margin:0}
.next-idea{font-size:24px;line-height:1.5;margin-top:17px}
#navigation{position:absolute;bottom:62px;left:76px;right:76px;z-index:8;display:flex;align-items:center;gap:12px;color:#142525}
#deck.dark #navigation{color:#f6f3eb}#navigation button{font:inherit;font-size:27px;color:inherit;background:none;border:1px solid currentColor;padding:8px 15px;cursor:pointer;border-radius:7px}#navigation button:disabled{opacity:.3;cursor:default}
#counter{margin-left:auto;font-size:27px;letter-spacing:.07em}#progress{position:absolute;bottom:29px;left:76px;right:76px;height:5px;background:#a83b2530;z-index:8}#progress>span{height:100%;display:block;background:#a83b25;transition:width .3s ease}
.slide.is-active h1,.slide.is-active .visual{animation:enter .35s ease both}@keyframes enter{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
'''
CSS += "\n/* Codex: reserve a full footer and prevent row overflow into navigation. */\n.slide{padding:54px 76px 168px}.brand{font-size:22px}.eyebrow{margin:36px 0 18px}h1{font-size:68px;line-height:1.25}.body-copy{font-size:32px;line-height:1.5;margin-top:22px}.visual{min-height:0;padding-top:26px;gap:16px}.row{font-size:28px;padding:14px 0}.note-svg{width:380px;height:230px}.next-idea{font-size:22px;margin-top:14px}.brand,.eyebrow,h1,.body-copy{flex-shrink:0}#deck.dark #progress{background:#f6f3eb55}#deck.dark #progress>span{background:#f6f3eb}\n"
JS = '''
let index=0;const slides=[...document.querySelectorAll('.slide')],deck=document.querySelector('#deck'),prev=document.querySelector('#previous'),next=document.querySelector('#next');
function fit(){const scale=Math.min(innerWidth/1080,innerHeight/1080);deck.style.transform=`translate(-50%,-50%) scale(${scale})`}
function goToCard(value){index=Math.max(0,Math.min(slides.length-1,value));slides.forEach((s,i)=>{s.classList.toggle('is-active',i===index);s.setAttribute('aria-hidden',String(i!==index))});deck.classList.toggle('dark',slides[index].classList.contains('dark'));prev.disabled=index===0;next.disabled=index===slides.length-1;document.querySelector('#counter').textContent=String(index+1).padStart(2,'0')+' / '+String(slides.length).padStart(2,'0');document.querySelector('#progress>span').style.width=(index+1)/slides.length*100+'%';if(parent!==window)parent.postMessage({type:'yebisu-page',index},location.origin)}
prev.addEventListener('click',()=>goToCard(index-1));next.addEventListener('click',()=>goToCard(index+1));
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();goToCard(index+(e.key==='ArrowRight'?1:-1))}});
window.addEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;goToCard(e.data.index)});
document.querySelector('#copy-template').addEventListener('click',async()=>{const text='目的：\\n次の一手：\\n相談先：';const status=document.querySelector('#copy-state');try{await navigator.clipboard.writeText(text);status.textContent='記入型をコピーしました'}catch{status.textContent='目的・次の一手・相談先の3行をメモに写してください'}});
window.addEventListener('resize',fit);fit();goToCard(0);
'''

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,s):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def save(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def make_fonts(out,content):
    result=[]
    for weight,file_hash in [('Regular','258d7156c165f2ff774b6efee637c22c3b950de0d8a10e501137061bc8085d01'),('Bold','30eba52fc837e8b62c97d4b82e6706583149fb7294e3712dd71a655eaea80a90')]:
        source=ROOT/'.build/fonts'/f'BIZUDPGothic-{weight}.ttf'
        portable=Path(__file__).resolve().parent/'fonts'/f'BIZUDPGothic-{weight}.ttf'
        if portable.exists():source=portable
        url=f'https://raw.githubusercontent.com/google/fonts/{FONT_PIN}/ofl/bizudpgothic/BIZUDPGothic-{weight}.ttf'
        if not source.exists():
            source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(urllib.request.urlopen(url).read())
        assert sha(source)==file_hash,'Unexpected font source'
        font=TTFont(source,recalcTimestamp=False);options=subset.Options();options.flavor='woff2';options.name_IDs=['*']
        s=subset.Subsetter(options=options);s.populate(text=content+''.join(chr(i) for i in range(32,127)));s.subset(font)
        for record in font['name'].names:
            if record.nameID in (1,16): record.string='Yebisu Carousel JP'.encode(record.getEncoding())
            elif record.nameID in (2,17):record.string=weight.encode(record.getEncoding())
            elif record.nameID==4:record.string=('Yebisu Carousel JP '+weight).encode(record.getEncoding())
            elif record.nameID==6:record.string=('YebisuCarouselJP-'+weight).encode(record.getEncoding())
        font.flavor='woff2';target=out/'fonts'/f'carousel-{weight.lower()}.woff2';target.parent.mkdir(parents=True,exist_ok=True);font.save(target)
        result.append(dict(source_url=url,source_sha256=file_hash,subset_sha256=sha(target),file=target.relative_to(out).as_posix(),font_family='Yebisu Carousel JP',glyphs=len(font.getGlyphOrder())))
    license_path=ROOT/'assets/fonts/bizudpgothic-OFL.txt'
    portable_license=Path(__file__).resolve().parents[1]/'fonts/OFL.txt'
    if portable_license.exists():license_path=portable_license
    if not license_path.exists():
        write(license_path,urllib.request.urlopen(f'https://raw.githubusercontent.com/google/fonts/{FONT_PIN}/ofl/bizudpgothic/OFL.txt').read().decode())
    shutil.copyfile(license_path,out/'fonts/OFL.txt')
    return result

def visual(role):
    if role=='HOOK':return '<svg class="note-svg" viewBox="0 0 480 300" aria-hidden="true"><path d="M55 25H410V255H55Z M350 25V83H410" fill="none" stroke="currentColor" stroke-width="6"/><g stroke="currentColor"><line x1="99" y1="95" x2="298" y2="95"/><line x1="99" y1="145" x2="355" y2="145"/><line x1="99" y1="195" x2="268" y2="195"/></g></svg>'
    if role=='PROBLEM':return '<div class="question"><div>よろしくお願いします<p>いま、どこまで終わった？</p></div><div class="missing">次にすることは？<p>読む人の作業が空欄。</p></div></div><p class="next-idea">次のカードで、メモの入口を揃えます。→</p>'
    values={'INSIGHT':[('01 目的','何のための作業か'),('02 次の一手','次にする作業を一つ'),('03 相談先','迷ったときに聞く担当')],
            'SOLUTION':[('目的','終わったら、何が変わる？'),('次の一手','次に何を確認する？'),('相談先','誰に聞けばよい？')],
            'EXAMPLE':[('目的','会議前に、資料を確認する'),('次の一手','数値の単位を揃える'),('相談先','迷ったら、資料の作成担当へ')]}
    if role in values:
        return ('<p class="example-label">架空の記入例</p>' if role=='EXAMPLE' else '')+''.join('<div class="row"><strong>'+html.escape(k)+'</strong><span>'+html.escape(v)+'</span></div>' for k,v in values[role])
    return '<button type="button" class="copy-template" id="copy-template">記入型をコピー →</button><p id="copy-state" class="copy-state" role="status"></p><p class="next-idea">自分の仕事に置き換えて、内容を確かめる。</p>'

def build(out,up,input_path):
    out.mkdir(parents=True,exist_ok=True)
    data=json.loads(input_path.read_text(encoding='utf-8-sig')) if input_path else DATA
    assert [v['role'] for v in data['slides']]==['HOOK','PROBLEM','INSIGHT','SOLUTION','EXAMPLE','CTA']
    for s in data['slides']:
        assert len(s['headline'].replace('\n',''))<=26 and len(s['body'].replace('\n',''))<=48,'Split long Japanese copy before layout'
    assert json.loads((up/'ACQUISITION.json').read_text(encoding='utf-8'))['commit']==COMMIT
    refs=[]
    for p in SOURCE_REFS:
        dst=out/'source/upstream'/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(up/p,dst)
        refs.append(dict(path=p,sha256=sha(up/p),url=f'https://github.com/{REPO}/blob/{COMMIT}/{p}'))
    shutil.copyfile(up/'LICENSE',out/'LICENSE.upstream')
    save(out/'input/data.json',data)
    write(out/'input/BRIEF.md','# '+data['title']+'\n\n'+data['purpose']+'\n\n'+data['notice']+'\n\n6枚、1080×1080、日本語、親しみのある実務向けの語り。外部への投稿・送信は行わない。\n')
    write(out/'input/product-marketing-context-global.md','# 架空ブランドの制作条件\n\nブランド: '+data['brand']+'\n\n読み手: 初めて引き継ぎメモを書く人。目的: 書き始めるための記入型を示す。教育段階: '+data['funnel']+'。実在企業・商品・効果の実績は扱わない。\n')
    write(out/'input/brand-guideline.md','# しおりの作例用ブランド\n\n架空ブランド。背景と文字は濃緑 #142525、生成り #F6F3EB、銅色 #A83B25。HookとCTAは濃緑、本文は生成り。日本語はBIZ UDPGothicを同じ役割で使い、サブセットをYebisu Carousel JPへ改名。文字色はこの3色以内。しおり形の自作ベクトルマークを各ページへ置く。\n')
    brief='# Carousel Brief — '+data['title']+'\n\n## 概要\n\n| 項目 | 内容 |\n|---|---|\n| 目的 | '+data['purpose']+' |\n| 用途 | SNSカルーセルの構成確認 |\n| 枚数・寸法 | 6枚 / 1080×1080 |\n| 読み手の段階 | '+data['funnel']+' |\n| 語り口 | 短く、親しみのある実務向け |\n| 納期 | 今回のローカル試作 |\n| 修正回数・承認者 | 公開用制作へ進む際に依頼者が決定。現在は人による承認待ち |\n\nブランドはinput/brand-guideline.md、読み手はinput/product-marketing-context-global.mdを参照。\n\n## 流れ\n\nHook → Problem → Insight → Solution → Example → CTA。実績の証拠がないためProofを捏造せず、架空の記入例へ変更。\n'
    brief+='\n## Brand direction\n\n色・字体・自作しおりマークはinput/brand-guideline.mdを参照。CTAボタンは「記入型をコピー」。Logoは各頁のしおり図形、contactは未設定で架空の連絡先は作らない。公開用デザイン・連絡先・人の承認は別工程。\n'
    for i,s in enumerate(data['slides'],1):
        brief+=f'\n## Slide {i} — {s["role"]}\n\n| 要素 | 内容 |\n|---|---|\n| 見出し | {s["headline"].replace(chr(10)," / ")} |\n| 本文 | {s["body"].replace(chr(10)," / ")} |\n| 図案 | {s["visual"]} |\n| 背景 | '+('濃緑 / 白系の文字' if i in (1,6) else '生成り / 濃緑の文字、銅色のアクセント')+' |\n'
    brief+='\n## 引き渡すもの\n\n- このブリーフと編集できるHTML、入力JSON。\n- HTMLとPNG6枚は構成確認用。SNS公開用の制作データではない。\n- コピー確認 → HTML構成確認 → Canva/Figma/Adobe Express等で仕上げ → 人による確認 → 公開、という原典の段階を区別する。今回の例はHTML構成確認まで。\n- LinkedIn用の公開PDF、縦長版、人の承認、投稿は今回の対象外。\n'
    write(out/'carousel-brief-shiori-20261014.md',brief)
    save(out/'input/copy-review.json',data.get('copy_review',{'status':'pending'}))
    save(out/'source/recipe.json',dict(original_skill=SOURCE_REFS[1],method='original instruction workflow: source and brand context -> 6-card narrative arc -> per-card copy/visual/background brief -> square HTML concept preview',production_stage='concept_preview',human_approval='pending',japanese_adaptation='英語の単語数を日本語へ機械換算せず、見出し26字・本文48字以下と実表示で判断。Proofは実績がないため、明示した架空の記入例へ変更。',brief_written_before_html=True))
    sections=[]
    role_labels={'HOOK':'入口','PROBLEM':'困りごと','INSIGHT':'残す3点','SOLUTION':'記入の型','EXAMPLE':'記入例','CTA':'まず1件'}
    for i,s in enumerate(data['slides']):
        brand='<div class="brand"><svg viewBox="0 0 30 32" aria-hidden="true"><path d="M5 2H25V30L15 24L5 30Z" fill="none" stroke="currentColor" stroke-width="2"/></svg><span>'+html.escape(data['brand'])+'</span><span class="preview-label">構成確認用</span></div>'
        sections.append('<section class="slide '+('dark ' if i in (0,5) else '')+'" aria-label="'+str(i+1)+'ページ目 '+html.escape(s['headline'].replace('\n',''))+'">'+brand+'<p class="eyebrow">'+f'{i+1:02d} / '+role_labels[s['role']]+'</p><h1>'+html.escape(s['headline'])+'</h1><p class="body-copy">'+html.escape(s['body'])+'</p><div class="visual">'+visual(s['role'])+'</div></section>')
    doc='<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(data['title'])+'</title><style>'+CSS+'</style></head><body><main id="deck">'+''.join(sections)+'<nav id="navigation" aria-label="カードの移動"><button type="button" id="previous" aria-label="前のカード">←</button><button type="button" id="next" aria-label="次のカード">→</button><span id="counter" aria-live="polite"></span></nav><div id="progress" aria-hidden="true"><span></span></div></main><script>'+JS+'</script></body></html>'
    write(out/'index.html',doc)
    font_records=make_fonts(out,doc+json.dumps(data,ensure_ascii=False)+'記入型をコピーしました')
    shutil.copyfile(Path(__file__),out/'source/build_business_carousel_repository_example.py')
    prompt='minhnv0807/ai-business-skillsの43-carousel-brief-globalを読み、添付の架空ブランドと原稿で「引き継ぎ、何を書けばいい？」を日本語6枚のSNSカルーセルとして構成確認する。原典のHook→Problem→Insight→Solution→Example→CTA、1枚1論点、Hook/CTA濃色・本文淡色、1080×1080のHTML、ページ番号と進捗を守る。Proofの実績は作らず、記入例と明示。BIZ UDPGothicのOFLを保ち、プレビューと公開用の仕上げ・人の承認を区別する。'
    write(out/'PROMPT.txt',prompt+'\n')
    write(out/'README.md','# '+data['title']+'\n\n原典43番の指示を使い、ブリーフと日本語6枚のHTML構成確認プレビューを制作。原典に自動レンダラーやPowerPoint出力CLIはなく、この例のソースはその指示を実行した専用の自作HTMLです。\n\n## 使って試す\n\nHTTPでindex.htmlを開く。←→とキーボードでページを移動。最後のボタンで3行の記入型をコピーできます。入力JSONとブランド条件を変えて再生成し、原稿と全ページを確認してください。\n\n## 原典のどこまでか\n\nこの原典の出力は、デザイナーへ渡すブリーフとHTML構成確認プレビュー。今回も構成確認までで、Canva/Figma等での公開用仕上げ、縦長版、LinkedIn投稿PDF、人の承認、公開は未実施。数値効果・書式の普遍性を保証する例ではありません。\n\n日本語の単語数を英語基準に機械換算せず、短い原稿、明示した記入例、実際の読みやすさで調整しました。字体は公式BIZ UDPGothicを必要文字へサブセット化し、内部名をYebisu Carousel JPへ変更。fonts/OFL.txtに原文条件を保持。原典のMITと原作者をLICENSE.upstreamに保持。\n')
    save(out/'PROVENANCE.json',dict(repository=REPO,upstream_commit=COMMIT,execution_type='instruction_skill_carousel_brief_html_preview',references=refs,input_sha256=sha(out/'input/data.json'),artifact_sha256=sha(out/'index.html'),output='index.html',production_stage='concept_preview',recipe='source/recipe.json',font_records=font_records,commands_executed=[],third_party_ai_api=False,checked_at=datetime.now(timezone.utc).isoformat()))
    save(out/'QA.json',dict(status='generated_awaiting_review',artifact_sha256=sha(out/'index.html'),production_stage='concept_preview',human_approval='pending'))
    print(str(out))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'examples/repositories'/IDENT)
    parser.add_argument('--upstream-dir',type=Path,default=ROOT/'.build/actual-upstreams'/REPO.replace('/','__'))
    parser.add_argument('--input',type=Path)
    args=parser.parse_args();build(args.output_dir,args.upstream_dir,args.input)
if __name__=='__main__':main()
