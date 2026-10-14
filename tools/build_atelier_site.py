"""Build the curated Japanese slide atelier without executing legacy site builders."""
from pathlib import Path
from urllib.parse import quote
import ast, hashlib, html, json

ROOT=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
esc=lambda s:html.escape(str(s),quote=True)
product=load('data/product-collection.json')
cases=load('data/case-studies.json')
by_id={c['id']:c for c in cases}
profiles={p['repository']:p for p in load('data/repository-guides.json')}

def version(path):return path+'?v='+hashlib.sha256((ROOT/path).read_bytes()).hexdigest()[:12]

head='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f4f1e9"><title>AIスライドアトリエ｜Studio Yebisu</title><meta name="description" content="原典GitHubスキルで実際に作った日本語スライド。作風を見て、スキル本文・制作一式・OSSフォントを使って自分の資料へ。"><link rel="icon" href="assets/studio-mark.svg">'''
for path in ['assets/studio.css','assets/case-studio.css','assets/repository-studio.css','assets/yebisu-atelier.css','assets/font-atelier.css']:
    if (ROOT/path).exists():head+='<link rel="stylesheet" href="'+version(path)+'">'
for path in ['assets/case-studio.mjs','assets/repository-detail.mjs','assets/font-atelier.mjs']:
    if (ROOT/path).exists():head+='<script type="module" src="'+version(path)+'"></script>'
head+='''</head><body><a class="skip" href="#examples">スライドを見る</a><header class="header"><div class="shell header-inner"><a class="brand atelier-brand" href="./"><span class="brand-symbol">Y.</span><span>AI SLIDE ATELIER<small>日本語で魅せる / Studio Yebisu</small></span></a><nav aria-label="メインメニュー"><a href="./#examples">スライドを見る</a><a href="./#skills">スキルを使う</a><a href="./#fonts">書体を選ぶ</a></nav><a class="header-github" href="https://github.com/studio-yebisu/awesome-codex-ppt-skills-ja">GitHub ↗</a></div></header>'''

tree=ast.parse((ROOT/'tools/build_case_site.py').read_text(encoding='utf-8'))
dialog=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='dialog' for t in n.targets))
dialog=dialog.replace('<a id="case-make"', '<a id="case-skill" class="button outline" download>スキル本文 ↓</a><a id="case-make"')
foot='''<footer class="footer"><div class="shell"><div class="footer-main"><div><p class="footer-brand">Studio Yebisu / AI SLIDE ATELIER</p><p>原典の力を、日本語で使える制作の道具へ。</p></div><div class="footer-links"><a href="guide.html">使い方</a><a href="licenses.html">原典・利用条件</a><a href="archive.html">出発点のカタログ</a></div></div><div class="footer-bottom"><span>原作者とスキル・素材・書体の個別条件を保持しています。</span><span>MADE WITH ORIGINAL SKILLS</span></div></div></footer>'''

def write(path,body,title=None):
    top=head if not title else head.replace('<title>AIスライドアトリエ｜Studio Yebisu</title>','<title>'+esc(title)+'｜Studio Yebisu</title>')
    (ROOT/path).write_text(top+body+foot+dialog+'</body></html>',encoding='utf-8',newline='\n')

motion=by_id['sol-motion-showcase'];editorial=by_id['sol-editorial-showcase']
def stage(c,extra=''):
    return '<button class="atelier-stage '+extra+'" data-open-case="'+esc(c['id'])+'" aria-label="'+esc(c['title'])+'のスライドを見る"><img src="'+esc(c['cover'])+'?v='+c['content_revision']+'" alt="'+esc(c['title'])+'の完成スライド"><span class="stage-play">▶ 再生する</span></button>'

categories={'pptx':'PowerPoint','html':'Webスライド','general':'制作ツール','business':'業務資料','convert':'発表・変換','image':'画像スライド'}
all_skills=load('data/skills.json')['skills'];selected={e['repository'] for e in product['entries']}
filters='<div class="filters" role="group" aria-label="スキルの形式"><button data-category="all" aria-pressed="true">すべて <span>'+str(len(selected))+'</span></button>'
for key,label in categories.items():
    count=sum(s['repo_full_name'] in selected and s['kind']==key for s in all_skills)
    if count:filters+='<button data-category="'+key+'" aria-pressed="false">'+label+' <span>'+str(count)+'</span></button>'
filters+='</div>'

home='''<main><section class="shell atelier-hero"><div class="atelier-hero-copy"><p class="eyebrow">STUDIO YEBISU / JAPANESE SLIDE SKILLS</p><h1>AIでつくる。<br><span>日本語で、魅せる。</span></h1><p class="hero-description">原典のスキルで、実際に作った。<br>気になる作風を見つけて、次はあなたの資料へ。</p><div class="hero-actions"><a class="button primary" href="#examples">スライドを見てみる <span>↗</span></a><a class="text-link" href="#skills">スキルを選ぶ ↓</a></div><p class="hero-caption">日本語の実例 / 短いスキル本文 / OSSフォント</p></div><div class="atelier-hero-visual"><div class="hero-proof-label"><span>NEW WORKS</span><span>原典から、日本語の新作へ。</span></div>'''+stage(motion,'hero-motion')+stage(editorial,'hero-editorial')+'''<span class="hero-sticker">見る。<br>使う。<br>自分のものに。</span></div></section>
<div class="atelier-ticker"><div class="shell"><span>PLAY THE DECK</span><i>↗</i><span>GET THE SKILL</span><i>↗</i><span>MAKE IT YOURS</span><i>↗</i><span>日本語で、ここから。</span></div></div>
<section class="shell section atelier-examples" id="examples"><div class="section-heading"><div><p class="eyebrow">01 / FIND YOUR NEXT LOOK</p><h2>この感じ、<br>つくってみたい。</h2></div><p>どれも元のスキルを使って制作。<br>開くと、実際のスライドを流せます。</p></div><div class="case-filters" role="group" aria-label="スライドの作風"><button data-look="all" aria-pressed="true">すべて</button><button data-look="editorial" aria-pressed="false">誌面・ビジュアル</button><button data-look="motion" aria-pressed="false">動くスライド</button><button data-look="work" aria-pressed="false">仕事の資料</button><button data-look="diagram" aria-pressed="false">図解・教材</button><label class="case-filter-format">形式<select id="case-format"><option value="all">すべて</option><option value="pptx">PowerPoint</option><option value="html">Web</option><option value="pdf">PDF</option></select></label><label class="case-filter-editing">編集したいもの<select id="case-editing"><option value="all">すべて</option><option value="native">文字・図形（PPTX）</option><option value="math">数式（PPTX）</option><option value="image">画像・ノート（PPTX）</option><option value="source">Web・TeX・SVGの原稿</option></select></label></div><p id="case-results" class="results" aria-live="polite"></p><div id="case-grid" class="case-grid"></div></section>
<section class="atelier-how"><div class="shell"><p class="eyebrow">FROM A GOOD EXAMPLE TO YOUR OWN DECK</p><h2>見つけたら、<br>AIに渡そう。</h2><div class="atelier-steps"><article><b>01</b><h3>作風を見る</h3><p>完成スライドを再生して、<br>表紙も本文も見て選ぶ。</p></article><article><b>02</b><h3>スキルを手に入れる</h3><p>短いMarkdownを直接取得。<br>実装が必要なら一式ZIPも。</p></article><article><b>03</b><h3>あなたの内容で作る</h3><p>原稿と書体指示をAIへ渡す。<br>原典の方式で、次の資料へ。</p></article></div><a href="guide.html" class="text-link">もう少し詳しい使い方 ↗</a></div></section>
<section class="shell section repository-catalog atelier-catalog" id="skills"><div class="section-heading"><div><p class="eyebrow">02 / SKILLS YOU CAN ACTUALLY USE</p><h2>いい実例には、<br>使えるスキルがある。</h2></div><p>ここで制作した原典から厳選。<br>日本語の指示本文を、そのまま取得できます。</p></div>'''+filters+'''<div class="catalog-tools"><label class="search"><span>⌕</span><input id="skill-query" type="search" placeholder="作りたい資料・スキル名で探す" aria-label="スキルを検索"></label><label class="catalog-status">作例<select id="skill-status"><option value="local">日本語の実例あり</option></select></label><label>並び順<select id="skill-order"><option value="produced">アトリエのおすすめ順</option><option value="name">名前順</option></select></label></div><p id="skill-results" class="results" aria-live="polite"></p><div id="skill-grid" class="skill-grid"></div><a class="text-link entry-bundle" href="downloads/yebisu-japanese-skill-entries.zip" download>日本語スキル本文をまとめて取得 ↓</a><p class="case-sample-note">本文は制作指示です。テンプレート・実装・原文の利用条件は一式ZIPかGitHub原典から。</p></section>
<section class="shell section atelier-fonts" id="fonts"><div class="section-heading"><div><p class="eyebrow">03 / TYPE MAKES THE DIFFERENCE</p><h2>日本語は、<br>書体でもっと良くなる。</h2></div><p>OSS書体と組み合わせの指示。<br>見た目ごと、AIへ渡せます。</p></div><div id="font-atelier"></div></section></main>'''
home=home.replace('<p id="case-results"', '<div class="case-search"><label for="case-query">題材・作風・スキル名</label><input id="case-query" type="search" placeholder="例：茶、手描き、Marp"></div><p id="case-results"')
write('index.html',home)
write('repository.html','<main class="shell doc-shell"><div id="repository-detail"></div></main>','スキルと作り方')
write('case.html','<main class="shell doc-shell"><div id="case-detail"></div></main>','日本語の制作例')
guide='''<main class="shell doc-shell"><section class="doc-hero"><p class="eyebrow">MAKE YOUR NEXT DECK</p><h1>作風を見つけたら、<br>自分の内容で。</h1></section><section class="doc-section"><h2>まずは短いスキルをAIへ。</h2><ol><li>気になる資料を再生し、「スキル本文」をダウンロード。</li><li>Markdownを使っているAIへ添付。読者、資料の目的、自分の原稿を一緒に渡す。</li><li>本文内の固定原典をAIに読ませ、該当のテンプレート・生成器・controllerで制作する。</li><li>コードやテンプレートが必要なら「一式ZIP」も展開して渡す。</li><li>書体アトリエの指示をコピーして加える。完成PPTXやWeb資料を開き、気になる箇所を直す。</li></ol><p>Markdown本文には制作指示を収録。原典の実装と原文LICENSEは別途ZIPかGitHubから取得します。原典ごとに必要な環境は異なります。</p></section><section class="doc-section"><h2>こんな依頼から始めよう。</h2><pre>このスキルと原典の方式で、日本語の資料を作ってください。
読者：新しい企画を検討する担当者
目的：企画の魅力と、次の一手を伝える
原稿：添付したメモを使う
見た目：書体アトリエでコピーした指示を使う
出力：編集できるPowerPoint、または再生できるWebスライド
元スキルのテンプレート・生成器・controllerを活かしてください。
完成資料と必要な制作ソースをください。</pre></section><section class="doc-section"><h2>書体も一緒に用意する。</h2><p>PowerPointでは使う書体を作成者と受け手の両方へ導入。Webでは必要なフォントと条件を一式に同梱します。</p><p><a href="./#fonts">書体を試す →</a> · <a href="downloads/fonts/AI-FONT-GUIDE.md" download>AI向け書体指示 ↓</a> · <a href="downloads/yebisu-oss-font-kit.zip" download>OSS書体一式 ↓</a></p></section><section class="doc-section"><h2>原典の強みを、日本語へ。</h2><p>元のスキルをこの環境で使い、コピー・書体・レイアウト・動きを改良しています。新作はSol 6.1の並列制作で完成。必要なビルドと初回表示だけを確認し、制作に時間を使う方針です。</p><p><a href="docs/PROJECT.md">制作方針</a> · <a href="docs/PRODUCT_SPEC.md">製品仕様</a> · <a href="licenses.html">原典・利用条件</a></p></section></main>'''
guide=guide.replace('気になる資料を再生し、「スキル本文」をダウンロード。','気になる資料を再生して作り方を開く。スキル本文はその場で読んでコピー、またはMarkdownとして取得。')
guide=guide.replace('Markdownを使っているAIへ添付。読者、資料の目的、自分の原稿を一緒に渡す。','作例の詳細で自分の原稿・読み手・希望枚数・書体を入れ、依頼文を組み立ててコピー。スキル本文と一式ZIPを、使っているAIへ一緒に渡す。')
write('guide.html',guide,'使い方')

terms='''<main class="shell doc-shell"><section class="doc-hero"><p class="eyebrow">CREDITS / LICENSES</p><h1>原典と、書体への敬意。</h1></section><section class="doc-section"><h2>原典を使った、日本語の独自プロジェクト。</h2><p>各スキルの作者と固定原典、原文LICENSE・NOTICEを保持しています。日本語派生・制作コードの変更は各キットに記載。カタログのCC0を原典コード、素材、書体の条件へ広げません。</p><div class="license-table-wrap"><table class="doc-table"><thead><tr><th>原典</th><th>条件</th><th>日本語版</th></tr></thead><tbody>'''
for e in product['entries']:
    p=profiles[e['repository']];official='https://github.com/'+e['repository']+'/tree/'+p['upstream_commit']
    terms+='<tr><td><a href="'+official+'">'+esc(e['repository'])+'</a></td><td>'+esc(p.get('license') or '個別条件')+'</td><td><a href="'+esc(e['skill_download'])+'" download>スキル本文</a> · <a href="repository.html?repo='+quote(e['repository'],safe='/')+'">方式・改変・配布</a></td></tr>'
terms+='''</tbody></table></div><p>Guizang由来のAGPL-3.0は対応する変更後ソースと条件をZIPに提供。MckのApache-2.0は原文LICENSE・NOTICEを保持。Bentoの固定shell・NOTICEも保持しています。SOILはソフトウェアがMIT、設計文・プロンプトなどの内容がCC BY-NC-SA 4.0です。内容を含む日本語派生は非商用・継承条件を保持します。原典に含まれる全素材への一括許諾を表示していません。</p></section><section class="doc-section"><h2>公式配布のOSSフォント</h2><p>新しい書体キットは固定commitの未改変TTFとOFL原文を同梱。OSの標準搭載書体を抽出したものではありません。本文・見出し・英数字の用途を分けて使用します。</p><ul>'''
for f in load('data/oss-font-kit.json')['families']:
    terms+='<li>'+esc(f['family'])+' / <a href="'+esc(f['license_url'])+'">OFL原文</a> / <a href="'+f['download']+'" download>原配布フォント</a></li>'
terms+='''</ul><p><a href="data/oss-font-kit.json">配布元と使用書体の記録</a> · <a href="data/fonts.json">従来の日本語Web書体</a> · <a href="data/preset-fonts.json">英字プリセット書体</a></p></section><section class="doc-section"><h2>出発点のカタログと制作履歴</h2><p><a href="archive.html">原209件の記録</a>と過去の制作物は保存しています。現在は実例と使い方のあるスキルを選んで掲載。原作者の紹介画像と、この環境で作った日本語資料を区別しています。</p></section></main>'''
write('licenses.html',terms,'原典・利用条件')
write('archive.html','''<main class="shell doc-shell"><section class="doc-hero"><p class="eyebrow">WHERE WE STARTED</p><h1>209件から、<br>自分たちのアトリエへ。</h1></section><section class="doc-section"><p>原カタログは資料として保存しています。現在の掲載は、実際に制作した日本語資料と使えるスキルを厳選したものです。209件すべてを作ることは、このプロジェクトの制作条件にしていません。</p><p><a href="data/skills.json" download>原209件の日本語カタログJSON ↓</a> · <a href="https://github.com/zhuyansen/awesome-codex-ppt-skills">出発点のGitHub ↗</a></p><p><a href="./#examples">アトリエの制作例へ戻る →</a></p></section></main>''','出発点のカタログ')
print(f'Japanese atelier built: {len(product["entries"])} curated skills')
