"""Produce Japanese examples using EACH project's own template or architecture.

This is deliberately separate from make_examples.py, the withdrawn common renderer.
See examples/actual/*/PROVENANCE.md for the exact upstream files and scope.
"""
from pathlib import Path
import base64, hashlib, html, json, re, shutil, subprocess, zipfile
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams'
OUT=ROOT/'examples/actual';OUT.mkdir(parents=True,exist_ok=True)
DOWNLOADS=ROOT/'downloads';DOWNLOADS.mkdir(exist_ok=True)
EMBEDDED_ESCAPE="<script>if(parent!==window)document.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();parent.postMessage({type:'yebisu-close'},location.origin)}},true);</script>"
PINS={p['repository']:p for p in json.loads((ROOT/'data/upstreams.json').read_text(encoding='utf-8'))}
FONT_RECORDS=json.loads((ROOT/'data/preset-fonts.json').read_text(encoding='utf-8'))
ALL_EXAMPLES=[]

def hashfile(file):return hashlib.sha256(file.read_bytes()).hexdigest()
def write(file,value):
    file.parent.mkdir(parents=True,exist_ok=True);file.write_text(value,encoding='utf-8')
def embed_fonts(families):
    rules=[]
    jp={'Noto Sans JP':('assets/fonts/noto-sans-jp.woff2','100 900'),'Noto Serif JP':('assets/fonts/noto-serif-jp.woff2','100 900')}
    for family in families:
        if family in jp:path,weight=jp[family];fmt='woff2'
        else:
            record=next(f for f in FONT_RECORDS if f['family']==family);path=record['file'];fmt='truetype';weight='400' if family in ('IBM Plex Mono','Archivo Black') else '100 900'
        encoded=base64.b64encode((ROOT/path).read_bytes()).decode()
        rules.append(f"@font-face{{font-family:'{family}';src:url(data:font/{fmt};base64,{encoded}) format('{fmt}');font-weight:{weight};font-display:swap}}")
    return '\n'.join(rules)

def provenance(folder,repo,paths,method,changes,commands):
    pin=PINS[repo];source=UP/repo.replace('/','__')
    files=[dict(path=p,sha256=hashfile(source/p)) for p in paths]
    record=dict(repository=repo,commit=pin['commit'],license=pin['github_license'],method=method,used_files=files,changes=changes,commands=commands,qa_status='awaiting_browser_review')
    write(folder/'PROVENANCE.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    listing='\n'.join(f"- [{p}](https://github.com/{repo}/blob/{pin['commit']}/{p})" for p in paths)
    write(folder/'PROVENANCE.md',f"# {repo} の日本語作例\n\n元リポジトリ: https://github.com/{repo}\n\n固定コミット: `{pin['commit']}`\n\n個別ライセンス: **{pin['github_license']}**。原文を同梱しています。\n\n## 制作方法\n\n{method}\n\n{listing}\n\n## 日本語向けの変更\n\n"+'\n'.join('- '+c for c in changes)+"\n\n## 再生成と検証\n\n```text\n"+'\n'.join(commands)+"\n```\n\n未実行の機能まで動作確認済みとは扱いません。ブラウザーの確認記録はサイトのQA記録を参照してください。\n")
    links=''.join(f'<li><a href="https://github.com/{repo}/blob/{pin["commit"]}/{p}">{html.escape(p)} ↗</a></li>' for p in paths)
    proof=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(repo)} の制作記録</title><link rel="stylesheet" href="../../../assets/studio.css"></head><body><main class="shell doc-shell"><a class="text-link" href="../../../#examples">209件の一覧へ戻る ←</a><section class="doc-hero"><p class="eyebrow">ACTUAL SKILL APPLICATION / JAPANESE EXAMPLE</p><h1>{html.escape(repo)}</h1><p>使用した元のスキルと、制作方法。</p></section><section class="doc-section"><p>固定コミット：<a href="https://github.com/{repo}/tree/{pin['commit']}"><code>{pin['commit']}</code></a></p><p>個別ライセンス：{pin['github_license']} / <a href="LICENSE">原文</a></p><h2>どの工程を使ったか</h2><p>{html.escape(method)}</p><ul>{links}</ul><h2>日本語向けの変更</h2><ul>'''+''.join('<li>'+html.escape(c)+'</li>' for c in changes)+'''</ul><h2>再生成と検証</h2><pre>'''+html.escape('\n'.join(commands))+'''</pre><p>全体の確認範囲は <a href="../../../guide.html#verification">検証の記録</a>で確認できます。</p><p><a href="index.html">作例を別画面で開く →</a> · <a href="PROVENANCE.json">取得記録JSON</a></p></section></main></body></html>'''
    write(folder/'PROVENANCE.html',proof)
    shutil.copy2(source/'LICENSE',folder/'LICENSE')
    return record

def register(folder,repo,title,style,method,kind,titles,notes,**extra):
    base=folder.relative_to(ROOT).as_posix()
    ALL_EXAMPLES.append(dict(repository=repo,commit=PINS[repo]['commit'],title=title,style=style,method_label=method,kind=kind,slide_count=len(titles),titles=titles,notes=notes,cover=f'{base}/cover.png',proof=f'{base}/PROVENANCE.html',**extra))

def guizang():
    repo='op7418/guizang-ppt-skill';source=UP/repo.replace('/','__');folder=OUT/'guizang-magazine';folder.mkdir(exist_ok=True)
    # Copy the REAL template's full CSS, WebGL shaders, navigation and presenter.
    template=(source/'assets/template.html').read_text(encoding='utf-8')
    template=template.replace('lang="zh-CN"','lang="ja"').replace('[必填] 替换为 PPT 标题 · Deck Title','つくる前に、見て選ぶ。｜Guizang 日本語作例')
    template=re.sub(r'<link[^>]+(?:fonts.googleapis|fonts.gstatic)[^>]*>','',template)
    template=template.replace('Noto Serif SC','Noto Serif JP').replace('Noto Sans SC','Noto Sans JP')
    template=template.replace('<style>','<style>\n'+embed_fonts(['Noto Sans JP','Noto Serif JP','Playfair Display','Source Serif 4','IBM Plex Mono'])+'\n',1)
    def chrome(left,page):return f'<div class="chrome"><div>{left}</div><div>JAPANESE EDITION · {page:02d} / 04</div></div>'
    def foot(left):return f'<div class="foot"><div>{left}</div><div>八百万図AIツールボックス · 2026</div></div>'
    sections=[]
    sections.append(f'''<section class="slide hero dark" data-slide-id="cover" data-animate="hero">
      {chrome('GUIZANG · MAGAZINE',1)}
      <div class="frame" style="display:grid;gap:3vh;align-content:center;flex:1">
        <div class="kicker" data-anim>AI SLIDE SKILLS / 日本語の作例</div>
        <h1 class="h-hero" style="font-size:7.5vw;line-height:1.22" data-anim>つくる前に、<br>見て選ぶ。</h1>
        <p class="lead" style="max-width:64vw" data-anim>スライドの印象は、選ぶスキルで変わる。<br>元のスタイルを、日本語で確かめる。</p>
        <div class="meta-row" data-anim><span>Guizang の元テンプレート</span><span>·</span><span>Ink Classic</span></div>
      </div>{foot('日本語のスライドを、もっと選びやすく。')}
    </section>''')
    labels=[('GENERAL','20','資料制作総合'),('POWERPOINT','83','PowerPoint'),('IMAGE','7','画像スライド'),('WEB SLIDES','57','ウェブスライド'),('BUSINESS','13','ビジネス資料'),('PRESENTATION','29','発表資料')]
    cards=''.join(f'<div class="stat-card" data-anim><div class="stat-label">{label}</div><div class="stat-nb">{n}<span class="stat-unit"> 件</span></div><div class="stat-note">{jp}</div></div>' for label,n,jp in labels)
    sections.append(f'''<section class="slide light" data-slide-id="catalog" data-animate="stats">
      {chrome('THE CATALOG',2)}<div class="frame" style="padding-top:2vh">
      <div class="kicker" data-anim>THE ORIGINAL 209 PROJECTS</div><h2 class="h-xl" style="font-size:5.3vw" data-anim>209の選択肢。</h2>
      <p class="lead" style="margin-bottom:1vh" data-anim>用途で絞って、それぞれの作例を見比べる。</p>
      <div class="grid-6" style="margin-top:1vh;gap:2vw 5vw">{cards}</div></div>{foot('元カタログの掲載数 · 2026年10月11日の記録')}
    </section>''')
    sections.append(f'''<section class="slide dark" data-slide-id="type" data-animate="quote">
      {chrome('TYPOGRAPHY',3)}<div class="frame" style="display:grid;gap:4vh;align-content:center;flex:1">
      <div class="kicker" data-anim>THE TYPE MAKES THE TONE</div>
      <blockquote style="font-family:var(--serif-zh);font-weight:700;font-size:5.8vw;line-height:1.3;max-width:85vw">
      <span data-anim="line" style="display:block">書体も、</span><span data-anim="line" style="display:block">伝わり方の一部。</span></blockquote>
      <p class="lead" data-anim>明朝体は、余韻を。ゴシック体は、明快さを。<br>日本語の改行と余白まで、一枚のデザインにする。</p>
      <div class="meta-row" data-anim><span>Noto Serif JP</span><span>·</span><span>Noto Sans JP</span></div></div>{foot('この作例は、見出しに日本語の明朝体を使用。')}
    </section>''')
    sections.append(f'''<section class="slide hero light" data-slide-id="closing" data-animate="hero">
      {chrome('YOUR NEXT SLIDE',4)}<div class="frame" style="display:grid;gap:4vh;align-content:center;flex:1">
      <div class="kicker" data-anim>CHOOSE → MAKE → REFINE</div>
      <h1 class="h-hero" style="font-size:6.8vw;line-height:1.25" data-anim>あなたの伝え方に、<br>合うスキルを。</h1>
      <p class="lead" style="max-width:67vw" data-anim>作例を見る。原典を知る。日本語でつくる。<br>その一歩を、このカタログから。</p></div>{foot('awesome-codex-ppt-skills-ja')}
    </section>''')
    template=template.replace('<!-- SLIDES_HERE -->','\n'.join(sections))
    titles=['つくる前に、見て選ぶ。','209の選択肢。','書体も、伝わり方の一部。','あなたの伝え方に、合うスキルを。']
    talks=[['スキルには、それぞれ異なるデザインの考え方があります。','この見本ではGuizangの雑誌風テンプレートをそのまま制作の土台にしています。','見出しの書体、余白、明暗のリズムを比べてみてください。'],['元のカタログには二百九件のプロジェクトが掲載されています。','ここにある六分類は、原版で整理されていた分類です。','この数は実制作済みの件数ではなく、選択肢の数です。'],['このページの見出しは日本語の明朝体、本文はゴシック体です。','英語用の書体だけを指定すると、日本語部分の見た目が変わってしまいます。','書体と改行を日本語の文に合わせて整えることが大切です。'],['用途と作例を手がかりに、自分に合うスキルを選んでください。','元の作者とライセンスを確認し、日本語の内容で制作します。','最後は実際の画面で、読みやすさと動きを確かめます。']]
    talks[2][0]='日本語の明朝体を見出しに使い、データページの注記にはゴシック体を使っています。'
    notes=[dict(id=id,title=title,purpose='該当スキルの日本語での出力を確認する',talk=talk,transition='次のページで具体的な見え方を確かめます。') for id,title,talk in zip(['cover','catalog','type','closing'],titles,talks)]
    template=re.sub(r'const SPEAKER_NOTES = \[.*?\];',lambda _: 'const SPEAKER_NOTES = '+json.dumps(notes,ensure_ascii=False)+';',template,count=1,flags=re.S)
    # Preserve native go(); observe it and bridge the catalog's page controls.
    bridge='''<script>
    const yebisuNativeGo = go;
    go = function(n,opts={}) { yebisuNativeGo(n,opts); if(window.parent!==window)window.parent.postMessage({type:'yebisu-page',index:window.__currentSlideIndex},location.origin); };
    window.addEventListener('message',e=>{if(e.origin===location.origin&&e.source===window.parent&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))go(e.data.index,{force:true});});
    if(window.parent!==window){document.documentElement.classList.add('catalog-embedded');}
    </script><style>.catalog-embedded #hint,.catalog-embedded #nav{display:none}</style>'''
    template=template.replace('</body>',bridge+EMBEDDED_ESCAPE+'\n</body>')
    template=template.replace('总览</button>','一覧</button>').replace('演讲模式</button>','発表者モード</button>').replace('翻页','ページ').replace('静态','静止').replace('动态','動作')
    template=template.replace('https://unpkg.com/lucide@latest/dist/umd/lucide.min.js','./assets/lucide.min.js')
    write(folder/'index.html',template);(folder/'assets').mkdir(exist_ok=True);shutil.copy2(source/'assets/motion.min.js',folder/'assets/motion.min.js')
    for name in ['lucide.min.js','lucide-LICENSE.txt','motion-LICENSE.txt']:shutil.copy2(ROOT/'sources/browser-dependencies'/name,folder/'assets'/name)
    provenance(folder,repo,['SKILL.md','assets/template.html','assets/motion.min.js','references/layouts.md','references/themes.md','references/presenter-mode.md','references/checklist.md'],
      '元の assets/template.html をコピーし、Layout 1・3・8・2 の構造を使って日本語を挿入。元のCSS、WebGL、Motion、go()、発表者モードの実装を保持。独自の共通スライドレンダラーは使用していません。',
      ['中国語用Notoの指定をNoto JPへ変更。英字のPlayfair Display / Source Serif 4 / IBM Plex Monoを維持。','日本語の見出しの改行・字号・フレーム高・データの余白を調整。','スライドIDと日本語講稿を挿入し、親のプレイヤーとのpostMessage接続を追加。','書体をOFL原文とともに同梱。Motionは元のローカルファイルを保持。Lucideを0.468.0のローカル版へ固定し、両ライブラリーの原文を保存。'],
      ['python tools/build_actual_examples.py','node skill-forks/guizang-ppt-skill-ja/scripts/validate-presenter-mode.mjs examples/actual/guizang-magazine/index.html'])
    register(folder,repo,'つくる前に、見て選ぶ。','Magazine / Ink Classic','元のHTMLテンプレートを使用','html',titles,['\n'.join(t) for t in talks],html=f'{folder.relative_to(ROOT).as_posix()}/index.html',download='downloads/guizang-magazine-ja.zip',fork_download='downloads/guizang-ppt-skill-ja.zip')

def frontend():
    repo='zarazhangrui/frontend-slides';source=UP/repo.replace('/','__');folder=OUT/'frontend-bold-signal';folder.mkdir(exist_ok=True)
    base=(source/'viewport-base.css').read_text(encoding='utf-8')
    template=(source/'html-template.md').read_text(encoding='utf-8')
    doc=re.search(r'```html\n(.*?)\n```',template,re.S).group(1)
    doc=doc.replace('lang="en"','lang="ja"').replace('Presentation Title</title>','伝えたいことを、まっすぐに。｜Frontend Slides</title>')
    doc=re.sub(r'<link rel="stylesheet" href="https://api.fontshare.com[^>]*>','',doc)
    styles='''
    :root{--bg-primary:#1a1a1a;--bg-gradient:linear-gradient(135deg,#1a1a1a 0%,#2d2d2d 50%,#1a1a1a 100%);--card-bg:#FF5722;--text-primary:#fff;--text-on-card:#1a1a1a;--stage-bg:#171717;--font-display:'Archivo Black','Noto Sans JP',sans-serif;--font-body:'Space Grotesk','Noto Sans JP',sans-serif;--duration-normal:.6s;--ease-out-expo:cubic-bezier(.16,1,.3,1)}
    .slide{background:var(--bg-gradient);color:var(--text-primary);font-family:var(--font-body);padding:84px}
    .slide-top{display:flex;align-items:center;justify-content:space-between;gap:40px;font-size:22px;letter-spacing:.12em}
    .number{font-family:var(--font-display);font-size:88px;line-height:1}
    .breadcrumbs{display:flex;gap:26px;color:#aaa}.breadcrumbs .selected{color:#fff}
    .signal-card{position:absolute;left:84px;right:84px;top:240px;bottom:120px;background:var(--card-bg);color:var(--text-on-card);padding:64px}
    h1,h2{font-family:var(--font-display);font-weight:900;line-height:1.14;letter-spacing:-.025em;overflow-wrap:normal}
    .signal-card h1{font-size:138px;position:absolute;left:64px;bottom:72px}
    .signal-card .eyebrow{font-size:24px;letter-spacing:.12em;font-weight:500}
    .signal-card .outline{position:absolute;right:70px;top:60px;width:220px;height:220px;border:3px solid #1a1a1a;border-radius:50%}
    .signal-card .outline::after{content:'';position:absolute;inset:30px;border:3px solid #1a1a1a;border-radius:50%}
    .slide-footer{position:absolute;left:84px;right:84px;bottom:44px;display:flex;justify-content:space-between;font-size:20px;color:#aaa}
    .headline{font-size:96px;margin-top:90px}
    .three-up{display:grid;grid-template-columns:repeat(3,1fr);gap:48px;margin-top:68px}
    .principle{border-top:2px solid #fff6;padding-top:35px}.principle .n{font-family:var(--font-display);font-size:72px;color:var(--card-bg)}
    .principle h3{font-size:42px;font-weight:700;margin:35px 0 25px}.principle p{font-size:28px;line-height:1.65;color:#bbb}
    .type-split{display:grid;grid-template-columns:1fr 1fr;gap:70px;margin-top:82px}.type-sample{border-top:2px solid #fff6;padding-top:42px}
    .type-sample strong{display:block;font-size:76px;line-height:1.4}.type-sample p{font-size:30px;line-height:1.6;color:#bbb;margin-top:44px}
    .closing-number{font-family:var(--font-display);font-size:195px;position:absolute;right:60px;top:25px;opacity:.22}
    .deck-controls{display:flex;gap:12px;align-items:center;color:white;font:13px var(--font-body)}
    .deck-controls button,.edit-toggle{font-family:var(--font-body);background:#1a1a1a;color:white;border:1px solid #fff6;padding:8px 14px;cursor:pointer;border-radius:3px}
    .edit-hotzone{position:fixed;top:0;left:0;width:80px;height:80px;z-index:10000}.edit-toggle{position:fixed;top:18px;left:18px;opacity:0;pointer-events:none;transition:opacity .3s;z-index:10001}.edit-toggle.show,.edit-toggle.active{opacity:1;pointer-events:auto}
    [contenteditable=true]{outline:2px dashed white;outline-offset:7px}.catalog-embedded .edit-hotzone,.catalog-embedded .edit-toggle,.catalog-embedded .deck-controls{display:none}
    @media print{.edit-hotzone,.edit-toggle{display:none}}
    '''
    # The entire upstream viewport-base.css is present without modification.
    doc=doc.replace('/* --- PASTE viewport-base.css CONTENTS HERE --- */',base+'\n'+embed_fonts(['Noto Sans JP','Archivo Black','Space Grotesk'])+'\n'+styles)
    def top(n):return f'<div class="slide-top"><span class="number">{n:02d}</span><div class="breadcrumbs"><span>FRONTEND SLIDES</span><span class="selected">BOLD SIGNAL</span></div></div>'
    def footer(n):return f'<div class="slide-footer"><span>JAPANESE EDITION / 八百万図AIツールボックス</span><span>{n:02d} / 04</span></div>'
    sections=[f'''<section class="slide title-slide active"><div>{top(1)}</div><div class="signal-card reveal"><div class="eyebrow" data-edit>日本語で、伝えるためのスライド。</div><div class="outline" aria-hidden="true"></div><h1 data-edit>伝えたいことを、<br>まっすぐに。</h1></div>{footer(1)}</section>''',
      f'''<section class="slide">{top(2)}<h2 class="headline reveal" data-edit>一枚に、ひとつの主張。</h2><div class="three-up"><div class="principle reveal"><span class="n">01</span><h3 data-edit>結論から。</h3><p data-edit>このページで伝えたいことを、<br>最初の一文にする。</p></div><div class="principle reveal"><span class="n">02</span><h3 data-edit>理由を添える。</h3><p data-edit>数字、比較、具体例。<br>主張を支える材料を選ぶ。</p></div><div class="principle reveal"><span class="n">03</span><h3 data-edit>余白を残す。</h3><p data-edit>読ませる場所を絞り、<br>視線の行き先を決める。</p></div></div>{footer(2)}</section>''',
      f'''<section class="slide">{top(3)}<h2 class="headline reveal" data-edit>日本語にも、デザインを。</h2><div class="type-split"><div class="type-sample reveal"><strong style="font-weight:700" data-edit>見出しは、<br>短く力強く。</strong><p data-edit>Noto Sans JP / 700<br>意味のまとまりで、改行する。</p></div><div class="type-sample reveal"><strong style="font-size:60px;font-weight:400" data-edit>本文は、<br>落ち着いて読める。</strong><p data-edit>Noto Sans JP / 400<br>見出しとの大きさに、差をつける。</p></div></div>{footer(3)}</section>''',
      f'''<section class="slide">{top(4)}<div class="signal-card reveal"><div class="eyebrow" data-edit>THE NEXT STEP</div><div class="closing-number" aria-hidden="true">→</div><h1 data-edit>作例を見て、<br>自分の一枚へ。</h1></div>{footer(4)}</section>''']
    doc=re.sub(r'(<main class="deck-stage" id="deckStage">).*?(</main>)',lambda m:m.group(1)+'\n'+ '\n'.join(sections)+'\n'+m.group(2),doc,count=1,flags=re.S)
    doc=doc.replace('// Arrow keys, Space, Page Up/Down',"document.addEventListener('keydown',e=>{if(e.target.isContentEditable)return;if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide+1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide-1)}})")
    doc=doc.replace('// Touch/swipe support for mobile',"let startX=null;document.addEventListener('touchstart',e=>{startX=e.touches[0].clientX},{passive:true});document.addEventListener('touchend',e=>{if(startX===null)return;const dx=e.changedTouches[0].clientX-startX;if(Math.abs(dx)>40)this.showSlide(this.currentSlide+(dx<0?1:-1));startX=null},{passive:true});let last=0;document.addEventListener('wheel',e=>{if(e.target.isContentEditable)return;if(Date.now()-last>700&&Math.abs(e.deltaY)>15){this.showSlide(this.currentSlide+(e.deltaY>0?1:-1));last=Date.now()}},{passive:true})")
    doc=doc.replace('new SlidePresentation();',"const presentation=new SlidePresentation();\nwindow.presentation=presentation;\nwindow.addEventListener('message',e=>{if(e.origin===location.origin&&e.source===window.parent&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))presentation.showSlide(e.data.index)});")
    doc=doc.replace("this.slides.forEach((slide, i) => {", "if(window.parent!==window)window.parent.postMessage({type:'yebisu-page',index:this.currentSlide},location.origin);\n                const count=document.getElementById('page-count');if(count)count.textContent=(this.currentSlide+1)+' / '+this.slides.length;\n                this.slides.forEach((slide, i) => {")
    editor='''<div class="deck-controls"><button id="prev" aria-label="前のスライド">←</button><span id="page-count">1 / 4</span><button id="next" aria-label="次のスライド">→</button></div><div class="edit-hotzone"></div><button class="edit-toggle" id="editToggle" title="編集モード（E）">編集 E</button>
    <script>
    if(window.parent!==window)document.documentElement.classList.add('catalog-embedded');
    document.getElementById('prev').onclick=()=>presentation.showSlide(presentation.currentSlide-1);document.getElementById('next').onclick=()=>presentation.showSlide(presentation.currentSlide+1);
    const editable=[...document.querySelectorAll('[data-edit]')],key='yebisu-frontend-bold-signal-v1';
    try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(Array.isArray(saved)&&saved.length===editable.length)editable.forEach((el,i)=>{el.innerHTML=saved[i]})}catch{}
    const editor={isActive:false,toggleEditMode(){this.isActive=!this.isActive;editable.forEach(el=>el.contentEditable=String(this.isActive));editToggle.classList.toggle('active',this.isActive)}};
    const hotzone=document.querySelector('.edit-hotzone'),editToggle=document.getElementById('editToggle');let hideTimeout=null;
    editToggle.onclick=()=>editor.toggleEditMode();hotzone.onclick=()=>editor.toggleEditMode();
    for(const el of [hotzone,editToggle]){el.addEventListener('mouseenter',()=>{clearTimeout(hideTimeout);editToggle.classList.add('show')});el.addEventListener('mouseleave',()=>{hideTimeout=setTimeout(()=>{if(!editor.isActive)editToggle.classList.remove('show')},400)})}
    editable.forEach(el=>el.addEventListener('input',()=>{try{localStorage.setItem(key,JSON.stringify(editable.map(e=>e.innerHTML)))}catch{}}));
    document.addEventListener('keydown',e=>{if(e.target.isContentEditable)return;if(e.key.toLowerCase()==='e')editor.toggleEditMode();if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();const clone=document.documentElement.cloneNode(true);clone.querySelectorAll('[contenteditable]').forEach(el=>el.removeAttribute('contenteditable'));const url=URL.createObjectURL(new Blob(['<!DOCTYPE html>'+clone.outerHTML],{type:'text/html'}));const a=document.createElement('a');a.href=url;a.download='frontend-bold-signal-ja.html';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}});
    </script>'''
    editor=editor.replace('if(e.target.isContentEditable)return;',"if(e.target.isContentEditable&&!((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'))return;")
    doc=doc.replace('</body>',editor+EMBEDDED_ESCAPE+'\n</body>');write(folder/'index.html',doc)
    titles=['伝えたいことを、まっすぐに。','一枚に、ひとつの主張。','日本語にも、デザインを。','作例を見て、自分の一枚へ。']
    notes=['Frontend SlidesのBold Signalプリセットです。濃いグラデーション、オレンジの大きな面、左下の見出し、左上のページ番号という元の構成を使っています。','結論を最初に示し、理由を添え、余白を残します。一枚のページに主張を絞ると、読む順序がはっきりします。','英字には指定のArchivo BlackとSpace Grotesk、日本語にはNoto Sans JPを使っています。日本語の見出しと本文の字重・大きさを分けています。','元の作例と日本語での見え方を確かめ、自分の内容へ進みます。このHTMLはEキーで編集し、Ctrl+Sで保存できます。']
    provenance(folder,repo,['SKILL.md','STYLE_PRESETS.md','viewport-base.css','html-template.md','animation-patterns.md'],
      '指示型スキルのSKILL.mdを適用。Bold Signalの色・書体・大きな色面・番号・パンくずを使用し、html-template.mdのHTMLとSlidePresentationクラスを土台に制作。viewport-base.cssは全文を挿入。上流に生成CLIはないため「元のCLIを実行した」とは表記しません。',
      ['1920×1080の固定ステージと全体の等比縮小を維持。','元プリセットのArchivo Black / Space Groteskを維持し、日本語用Noto Sans JPを追加。','日本語の内容、改行、キーボード・タッチ・ホイール、E編集・自動保存・Ctrl+S出力を実装。','カタログ用のpostMessage接続を追加。書体を埋め込んで外部CDNを不要にした。'],
      ['python tools/build_actual_examples.py','python tools/verify_actual_examples.py'])
    register(folder,repo,'伝えたいことを、まっすぐに。','Bold Signal','元のSKILL・指定プリセットを適用','html',titles,notes,html=f'{folder.relative_to(ROOT).as_posix()}/index.html',download='downloads/frontend-bold-signal-ja.zip',fork_download='downloads/frontend-slides-ja.zip')

def ppt_master():
    repo='hugohe3/ppt-master';source=UP/repo.replace('/','__');folder=OUT/'ppt-master-native';folder.mkdir(exist_ok=True)
    # Separate native-vector path: no Artifact Tool / image-slides fallback.
    def txt(x,y,s,text,color='#143F47',weight=400):return f'<text x="{x}" y="{y}" font-size="{s}" font-weight="{weight}" fill="{color}">{html.escape(text)}</text>'
    def rect(x,y,w,h,color):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'
    def group(id,bounds,inside):return f'<g id="{id}" data-pptx-bounds="{bounds}">{inside}</g>'
    def svg(page,role,body):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" lang="ja" font-family="Noto Sans JP" data-pptx-page-role="{role}">{rect(0,0,1280,720,"#F3F5EF")}'+body+group('footer','64 655 1150 28',txt(64,677,14,'PPT MASTER / JAPANESE VECTOR EXAMPLE', '#52656A')+txt(1150,677,14,f'{page:02d} / 04','#52656A'))+'</svg>'
    pages=[]
    cover=group('title','64 168 990 220',txt(64,230,58,'スキルの違いを、',weight=700)+txt(64,320,76,'日本語で確かめる。',weight=700))+group('intro','68 397 980 117',txt(68,432,28,'209件のカタログから、あなたの一枚へ。')+txt(68,485,21,'編集可能な文字と図形でつくる、PowerPointの日本語作例。','#52656A'))+group('accent','1120 56 96 542',rect(1120,56,96,542,'#D6E642'))
    pages.append(svg(1,'cover',cover))
    body=group('title','64 72 1140 98',txt(64,135,48,'用途に合わせて、出力を選ぶ。',weight=700))
    for i,(title,line1,line2) in enumerate([('PowerPoint','会議や提案に。','文字と図形を、後から編集。'),('ウェブスライド','動きのある発表に。','ブラウザーで、そのまま再生。'),('画像スライド','見た目を固定したいときに。','出力後の文字編集には制約。')]):
        x=64+i*394
        body+=group(f'output-{i+1}',f'{x} 235 358 320',rect(x,235,358,6,'#143F47')+txt(x,308,27,title,weight=700)+txt(x,398,21,line1)+txt(x,445,19,line2,'#52656A')+txt(x,525,54,f'0{i+1}','#52656A',700))
    pages.append(svg(2,'content',body))
    body=group('title','64 72 1150 98',txt(64,135,48,'日本語の読みやすさを、整える。',weight=700))+group('sample','64 238 572 282',rect(64,238,572,282,'#143F47')+txt(98,332,42,'自然な改行は、','#F3F5EF',700)+txt(98,398,42,'理解の手助け。','#F3F5EF',700))+group('explanation','702 253 512 250',txt(702,296,29,'Noto Sans JP',weight=700)+txt(702,365,22,'見出しと本文の大きさを分ける。')+txt(702,415,22,'意味のまとまりで改行する。')+txt(702,465,22,'文字を詰めすぎず、余白を残す。'))
    pages.append(svg(3,'content',body))
    body=group('title','64 155 1085 195',txt(64,225,60,'作例を見る。原典を知る。',weight=700)+txt(64,319,66,'自分の資料を、つくる。',weight=700))+group('outro','64 397 1080 115',txt(64,432,26,'作者とライセンスを確かめて、合うスキルを選ぶ。')+txt(64,490,23,'最後は、実際の画面で読みやすさを確かめる。','#52656A'))+group('accent','64 580 1148 8',rect(64,580,1148,8,'#D6E642'))
    pages.append(svg(4,'ending',body))
    titles=['スキルの違いを、日本語で確かめる。','用途に合わせて、出力を選ぶ。','日本語の読みやすさを、整える。','自分の資料を、つくる。']
    notes=['この作例はPPT Masterの元の変換処理を使い、SVGから編集可能なPowerPointへ出力しています。元カタログの二百九件には、さまざまな形式のスキルがあります。','会議や提案には、後から編集できるPowerPointが便利です。動きを見せたい発表にはウェブスライド、見た目を固定したい用途には画像スライドを選べます。画像としての出力は、文字編集の自由度が下がります。','日本語では、書体の指定だけでなく、意味のまとまりでの改行が大切です。このページではNoto Sans JPを使い、見出しと本文の大きさを分け、余白を残しています。','作例と原典を確認し、作者と個別のライセンスを尊重して制作します。仕上げは実際の発表画面で、文字と図形の見え方を確かめます。']
    for i,page in enumerate(pages,1):
        write(folder/f'svg_output/{i:02d}_slide.svg',page);write(folder/f'notes/{i:02d}_slide.md',notes[i-1]+'\n')
    # Root metadata must keep the background static for native animation.
    for file in (folder/'svg_output').glob('*.svg'):
        page=file.read_text(encoding='utf-8').replace('<rect x="0" y="0" width="1280" height="720"','<rect id="background" data-pptx-role="background" x="0" y="0" width="1280" height="720"',1)
        write(file,page)
    skill='skills/ppt-master';scripts=source/skill/'scripts';py=ROOT/'.build/ppt-master-venv/Scripts/python.exe'
    fork_scripts=ROOT/'skill-forks/ppt-master-ja/scripts'
    if fork_scripts.exists():scripts=fork_scripts
    r=subprocess.run([str(py),str(scripts/'compact_svg_styles.py'),str(folder/'svg_output'),'--inplace'],capture_output=True,text=True,encoding='utf-8')
    write(folder/'validation/compact-output.txt',r.stdout+'\n'+r.stderr)
    if r.returncode:raise RuntimeError('SVG compacting failed')
    command=[str(py),str(scripts/'svg_quality_checker.py'),str(folder),'--quick-generate','--canonical-authoring','--stage','final','--json']
    r=subprocess.run(command,capture_output=True,text=True,encoding='utf-8');write(folder/'validation/checker-output.json',r.stdout);write(folder/'validation/checker-stderr.txt',r.stderr)
    if r.returncode:raise RuntimeError('PPT Master checker failed; see validation/checker-output.json')
    command=[str(py),str(scripts/'svg_to_pptx.py'),str(folder),'--quick-generate','--primary-language','ja-JP','--with-notes','-t','fade','-o',str(folder/'ppt-master-ja.pptx')]
    r=subprocess.run(command,capture_output=True,text=True,encoding='utf-8');write(folder/'validation/export-output.txt',r.stdout+'\n'+r.stderr)
    if r.returncode:raise RuntimeError('PPT Master exporter failed; see validation/export-output.txt')
    provenance(folder,repo,[f'{skill}/SKILL.md',f'{skill}/references/shared-standards-core.md',f'{skill}/references/executor-base.md',f'{skill}/references/semantic-svg.md',f'{skill}/workflows/profiles/quick-generate.md',f'{skill}/scripts/svg_quality_checker.py',f'{skill}/scripts/svg_to_pptx.py'],
      '日本語版のカタログ作例経路として、上流の閉じたSVG仕様に従ってSVGを制作し、フォークに同梱した元の品質チェッカーとSVG→DrawingML変換器を実行。日本語版の専用経路は --quick-generate を使用します。上流Default GenerateのStrategistや確認UIまで実行したという主張ではありません。文字と図形を持つネイティブPPTXを出力し、画像スライドへ置き換えるフォールバックは使用していません。ブラウザーはPPTXへの入力SVGを表示します。PowerPointアプリ内での視聴検証は未実施。Noto Sans JPを受け手側にも導入する必要があり、上流チェッカーの書体警告を制作記録に保持しています。',
      ['日本語版フォークのカタログ作例用経路を追加。上流の変換器・チェッカー本体は無改変。','日本語内容、Noto Sans JP、1280×720の意味グループ付きSVG、各ページの日本語講稿を制作。','PowerPointの校正言語をja-JPに指定し、元のネイティブfadeトランジションを使用。'],
      ['python tools/build_actual_examples.py','python <PPT_MASTER>/scripts/svg_quality_checker.py <EXAMPLE> --quick-generate --canonical-authoring --stage final --json','python <PPT_MASTER>/scripts/svg_to_pptx.py <EXAMPLE> --quick-generate --primary-language ja-JP --with-notes -t fade -o ppt-master-ja.pptx'])
    paths=[(folder/f'svg_output/{i:02d}_slide.svg').relative_to(ROOT).as_posix() for i in range(1,5)]
    preview='''<!DOCTYPE html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PPT Master 日本語作例</title><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#202b2b}#stage{position:absolute;width:1280px;height:720px;transform-origin:0 0}.slide{position:absolute;inset:0;visibility:hidden}.slide.active{visibility:visible}nav{position:fixed;bottom:8px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:10px;color:white;font:12px sans-serif}button{background:#143F47;color:white;border:1px solid #fff6;padding:6px 12px}.embedded nav{display:none}''' + embed_fonts(['Noto Sans JP']) + '</style><main id="stage">'
    preview+='\n'.join(f'<section class="slide" aria-label="{html.escape(title)}">{file.read_text(encoding="utf-8")}</section>' for title,file in zip(titles,sorted((folder/'svg_output').glob('*.svg'))))
    preview+='''</main><nav><button id="prev" aria-label="前のスライド">←</button><span id="counter"></span><button id="next" aria-label="次のスライド">→</button></nav><script>const slides=[...document.querySelectorAll('.slide')];let page=0;function go(n){page=Math.max(0,Math.min(n,slides.length-1));slides.forEach((s,i)=>s.classList.toggle('active',i===page));document.getElementById('counter').textContent=(page+1)+' / '+slides.length;if(parent!==window)parent.postMessage({type:'yebisu-page',index:page},location.origin)}function fit(){const s=Math.min(innerWidth/1280,innerHeight/720);document.getElementById('stage').style.transform=`translate(${(innerWidth-1280*s)/2}px,${(innerHeight-720*s)/2}px) scale(${s})`}document.getElementById('prev').onclick=()=>go(page-1);document.getElementById('next').onclick=()=>go(page+1);document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();go(page+1)}if(e.key==='ArrowLeft'){e.preventDefault();go(page-1)}});window.addEventListener('message',e=>{if(e.origin===location.origin&&e.source===parent&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))go(e.data.index)});if(parent!==window)document.documentElement.classList.add('embedded');window.addEventListener('resize',fit);fit();go(0);</script></html>'''
    preview=preview.replace('nav{position:fixed','nav{padding:5px;background:#143F47;position:fixed').replace('</html>',EMBEDDED_ESCAPE+'</html>')
    write(folder/'index.html',preview)
    register(folder,repo,'スキルの違いを、日本語で確かめる。','編集可能なネイティブPPTX','元の変換器でPPTX出力 · SVGプレビュー','html',titles,notes,html='examples/actual/ppt-master-native/index.html',pages=paths,download='examples/actual/ppt-master-native/ppt-master-ja.pptx',fork_download='downloads/ppt-master-ja.zip')

if __name__=='__main__':
    guizang();frontend();ppt_master()
    for e in ALL_EXAMPLES:
        folder=(ROOT/e['html']).parent;qa=folder/'QA.json'
        if qa.exists():
            check=json.loads(qa.read_text(encoding='utf-8'))
            if check.get('html_sha256')==hashfile(folder/'index.html'):
                record=json.loads((folder/'PROVENANCE.json').read_text(encoding='utf-8'))
                record['qa_status']='browser_preview_reviewed';record['browser_qa']='QA.json'
                write(folder/'PROVENANCE.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    write(ROOT/'data/actual-examples.json',json.dumps(ALL_EXAMPLES,ensure_ascii=False,indent=2)+'\n')
    print('3 upstream-specific Japanese examples / 12 slides')
