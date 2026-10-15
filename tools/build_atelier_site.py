"""Build the curated Japanese slide atelier without executing legacy site builders."""
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote
import ast, hashlib, html, json, re

ROOT=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
esc=lambda s:html.escape(str(s),quote=True)
product=load('data/product-collection.json')
cases=load('data/case-studies.json')
by_id={c['id']:c for c in cases}
profiles={p['repository']:p for p in load('data/repository-guides.json')}
font_kit=load('data/oss-font-kit.json')
goal=load('data/project-goal.json')

# Counts come from the canonical JSON. Steps (page_unit 段階) are never added to normal pages.
active=[by_id[i] for i in product['active_case_ids'] if i in by_id]
step_cases=[c for c in active if c.get('page_unit')=='段階']
stats={'skills':len(product['entries']),'decks':len(active),'pages':sum(c['page_count'] for c in active if c.get('page_unit')!='段階'),'steps':sum(c['page_count'] for c in step_cases),'step_decks':len(step_cases),'font_families':len(font_kit['families']),'font_files':sum(len(f.get('files',[])) for f in font_kit['families']),'font_presets':len(font_kit.get('presets',[]))}
formats=Counter(c['format'] for c in active)
format_line=' · '.join(label+' '+str(formats[key]) for key,label in [('pptx','PowerPoint'),('html','Web'),('pdf','PDF')] if formats[key])

# The editorial record is written by the parent after the run. Without a verified record, no Opus usage is claimed.
MODEL_NAMES={'claude-opus-5-5':'Claude Opus 5.5','gpt-6.1-sol':'Sol 6.1'}
model_name=lambda m:MODEL_NAMES.get(str(m),str(m))
editorial_path=ROOT/'data/site-editorial.json'
editorial=load('data/site-editorial.json') if editorial_path.exists() else None
is_opus=lambda m:str(m).strip().lower()=='claude-opus-5-5'
opus_verified=bool(editorial and editorial.get('verification_status')=='verified' and editorial.get('requested_model')=='claude-opus-5-5' and any(is_opus(m) for m in editorial.get('reported_models') or []))
UNSAFE=re.compile(r'[A-Za-z]:[\\/]|\\\\|(^|\s)/(Users|home|root|tmp|var|mnt)/|sk-[A-Za-z0-9]|gh[pousr]_|Bearer\s|api[_-]?key|token\s*[:=]|password',re.I)
public_text=lambda s:not UNSAFE.search(str(s))
built_on=datetime.now(timezone(timedelta(hours=9))).date().isoformat()
existing_model=(editorial or {}).get('existing_examples_model') or goal.get('current_batch',{}).get('production_model','')

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
foot='''<footer class="footer"><div class="shell"><div class="footer-main"><div><p class="footer-brand">Studio Yebisu / AI SLIDE ATELIER</p><p>原典の力を、日本語で使える制作の道具へ。</p></div><div class="footer-links"><a href="guide.html">使い方</a><a href="status.html">制作の状況</a><a href="licenses.html">原典・利用条件</a><a href="archive.html">出発点のカタログ</a></div></div><div class="footer-bottom"><span>原作者とスキル・素材・書体の個別条件を保持しています。</span><span>MADE WITH ORIGINAL SKILLS</span></div></div></footer>'''

def write(path,body,title=None):
    top=head if not title else head.replace('<title>AIスライドアトリエ｜Studio Yebisu</title>','<title>'+esc(title)+'｜Studio Yebisu</title>')
    top=top.replace('href="#examples">スライドを見る</a><header', 'href="#main">本文へ移動</a><header')
    body=body.replace('<main', '<main id="main"', 1)
    (ROOT/path).write_text(top+body+foot+dialog+'</body></html>',encoding='utf-8',newline='\n')

motion=by_id['sol-motion-showcase'];editorial_case=by_id['sol-editorial-showcase']
count_label=lambda c:((str(c['scene_count'])+'場面 / ' if c.get('scene_count') else '')+str(c['page_count'])+'段階') if c.get('page_unit')=='段階' else str(c['page_count'])+'枚'
format_label=lambda c:{'pptx':'PowerPoint','pdf':'PDF'}.get(c['format'],'Web')
entry_by_repo={e['repository']:e for e in product['entries']}
recipe_url=lambda c:'repository.html?repo='+quote(c['repository'],safe='/')+'&case='+quote(c['id'])
step_note='・'.join(c['repository'].split('/')[-1]+' '+str(c['page_count'])+'段階' for c in step_cases)
existing_label=model_name(existing_model) if existing_model else '従来の制作モデル'
scope=(editorial or {}).get('scope') or 'サイト構成・日本語ガイド・使い方の改訂'
if not public_text(scope):scope='サイト構成・日本語ガイド・使い方の改訂'

if opus_verified:
    edition='<aside class="atelier-edition" aria-label="今回の改訂"><div class="shell edition-inner"><p class="edition-model"><span>EDITED WITH</span><b>CLAUDE OPUS 5.5</b></p><p class="edition-copy"><b>'+esc(scope)+'</b>を、Claude Opus 5.5が担当しました。<span>掲載'+str(stats['decks'])+'冊の作例は、'+esc(existing_label)+'中心の並列制作による原典方式の実作例です。</span></p><a class="edition-link" href="status.html">改訂の記録 →</a></div></aside>'
else:
    edition='<aside class="atelier-edition is-pending" aria-label="今回の改訂"><div class="shell edition-inner"><p class="edition-model"><span>EDITION NOTE</span><b>改訂の記録を確認中</b></p><p class="edition-copy">サイト構成・日本語ガイドの改訂は、実行記録の確認を待っています。<span>掲載'+str(stats['decks'])+'冊の作例は、'+esc(existing_label)+'中心の並列制作による原典方式の実作例です。</span></p><a class="edition-link" href="status.html">制作の状況 →</a></div></aside>'

figures=[('厳選スキル',stats['skills'],''),('日本語の作例',stats['decks'],'冊'),('通常ページ',stats['pages'],'枚'),('段階演出',stats['steps'],'段階'),('OSS書体',stats['font_families'],'書体')]
figure_list=''.join('<div><dt>'+label+'</dt><dd>'+str(n)+('<small>'+unit+'</small>' if unit else '')+'</dd></div>' for label,n,unit in figures)
ledger='<section class="atelier-ledger" aria-labelledby="ledger-title"><div class="shell ledger-inner"><h2 id="ledger-title"><span class="eyebrow">THE ATELIER TODAY</span>いま、ここで<br>見られるもの。</h2><dl class="ledger-figures">'+figure_list+'</dl><p class="ledger-note">'+esc(format_line)+'。段階演出は'+str(stats['step_decks'])+'冊の場面送り（'+esc(step_note)+'）で、通常ページとは別に数えています。書体は'+str(stats['font_files'])+'ファイル・'+str(stats['font_presets'])+'つの組み合わせ。<a href="status.html">制作の状況 →</a></p></div></section>'

# Three purpose-led entrances. Each points to a real active case and the existing float / recipe page.
starters=[('動くWebで見せる','beatdeck-showcase','場面が一段ずつ進むWeb資料。再生して、流れの見せ方を確かめる。'),('編集できるPowerPointで渡す','presentation-skill-showcase','文字・図形・表を、受け取った人がPowerPointでそのまま直せる。'),('図解で教える','sci-diagram-showcase','断面図・矢印・注釈まで編集できる、概念図の教材。')]
start_items=''
for n,(purpose,cid,lead) in enumerate([s for s in starters if s[1] in product['active_case_ids'] and s[1] in by_id],1):
    c=by_id[cid];entry=entry_by_repo.get(c['repository'],{})
    start_items+='<li class="start-item"><p class="start-purpose"><b>'+str(n).zfill(2)+'</b>'+esc(purpose)+'</p><button class="start-cover" data-open-case="'+esc(cid)+'" aria-label="'+esc(c['title'])+'のスライドを見る"><img src="'+esc(c['cover'])+'?v='+esc(c['content_revision'])+'" alt="'+esc(c['title'])+'の表紙" loading="lazy"><span class="stage-play">▶ 再生する</span></button><div class="start-copy"><h3>'+esc(c['title'])+'</h3><p>'+esc(lead)+'</p><p class="start-meta">'+format_label(c)+' · '+count_label(c)+' · '+esc(entry.get('title_ja',c['repository']))+'</p><div class="start-actions"><a href="'+esc(recipe_url(c))+'">作り方とスキル →</a>'+('<a href="'+esc(entry['skill_download'])+'" download>スキル本文 ↓</a>' if entry.get('skill_download') else '')+'</div></div></li>'
start='<section class="shell section atelier-start" id="start"><div class="section-heading"><div><p class="eyebrow">00 / CHOOSE YOUR FIRST DECK</p><h2>最初の一冊を、<br>目的で選ぶ。</h2></div><p>迷ったら、ここから。<br>再生して、気に入ったら作り方へ。</p></div><ol class="start-list">'+start_items+'</ol><p class="start-after">ほかの作例は、下の一覧で作風・形式・編集したいものから探せます。<a href="guide.html">はじめての使い方 →</a></p></section>'

def stage(c,extra=''):
    return '<button class="atelier-stage '+extra+'" data-open-case="'+esc(c['id'])+'" aria-label="'+esc(c['title'])+'のスライドを見る"><img src="'+esc(c['cover'])+'?v='+c['content_revision']+'" alt="'+esc(c['title'])+'の完成スライド"><span class="stage-play">▶ 再生する</span></button>'

categories={'pptx':'PowerPoint','html':'Webスライド','general':'制作ツール','business':'業務資料','convert':'発表・変換','image':'画像スライド'}
all_skills=load('data/skills.json')['skills'];selected={e['repository'] for e in product['entries']}
filters='<div class="filters" role="group" aria-label="スキルの形式"><button data-category="all" aria-pressed="true">すべて <span>'+str(len(selected))+'</span></button>'
for key,label in categories.items():
    count=sum(s['repo_full_name'] in selected and s['kind']==key for s in all_skills)
    if count:filters+='<button data-category="'+key+'" aria-pressed="false">'+label+' <span>'+str(count)+'</span></button>'
filters+='</div>'

home='''<main>'''+edition+'''<section class="shell atelier-hero"><div class="atelier-hero-copy"><p class="eyebrow">STUDIO YEBISU / JAPANESE SLIDE SKILLS</p><h1>AIでつくる。<br><span>日本語で、魅せる。</span></h1><p class="hero-description">原典のスキルで、実際に作った。<br>作例を見て、スキルを取って、あなたの内容で。</p><div class="hero-actions"><a class="button primary" href="#start">最初の一冊を選ぶ <span>↓</span></a><a class="text-link" href="#examples">すべての作例を見る ↓</a></div><p class="hero-caption">見る → スキルを取得 → 自分の内容で作る</p></div><div class="atelier-hero-visual"><div class="hero-proof-label"><span>NEW WORKS</span><span>原典から、日本語の新作へ。</span></div>'''+stage(motion,'hero-motion')+stage(editorial_case,'hero-editorial')+'''<span class="hero-sticker">見る。<br>使う。<br>自分のものに。</span></div></section>
'''+ledger+'''
<div class="atelier-ticker"><div class="shell"><span>PLAY THE DECK</span><i>↗</i><span>GET THE SKILL</span><i>↗</i><span>MAKE IT YOURS</span><i>↗</i><span>日本語で、ここから。</span></div></div>
'''+start+'''
<section class="shell section atelier-examples" id="examples"><div class="section-heading"><div><p class="eyebrow">01 / FIND YOUR NEXT LOOK</p><h2>この感じ、<br>つくってみたい。</h2></div><p>どれも元のスキルを使って制作。<br>開くと、実際のスライドを流せます。</p></div><div class="case-filters" role="group" aria-label="スライドの作風"><button data-look="all" aria-pressed="true">すべて</button><button data-look="editorial" aria-pressed="false">誌面・ビジュアル</button><button data-look="motion" aria-pressed="false">動くスライド</button><button data-look="work" aria-pressed="false">仕事の資料</button><button data-look="diagram" aria-pressed="false">図解・教材</button><label class="case-filter-format">形式<select id="case-format"><option value="all">すべて</option><option value="pptx">PowerPoint</option><option value="html">Web</option><option value="pdf">PDF</option></select></label><label class="case-filter-editing">編集したいもの<select id="case-editing"><option value="all">すべて</option><option value="native">文字・図形（PPTX）</option><option value="math">数式（PPTX）</option><option value="image">画像・ノート（PPTX）</option><option value="source">Web・TeX・SVGの原稿</option></select></label></div><p id="case-results" class="results" aria-live="polite"></p><div id="case-grid" class="case-grid"></div></section>
<section class="atelier-how"><div class="shell"><p class="eyebrow">FROM A GOOD EXAMPLE TO YOUR OWN DECK</p><h2>見つけたら、<br>AIに渡そう。</h2><div class="atelier-steps"><article><b>01</b><h3>作風を見る</h3><p>完成スライドを再生して、<br>表紙も本文も見て選ぶ。</p></article><article><b>02</b><h3>スキルを手に入れる</h3><p>短いMarkdownを直接取得。<br>実装が必要なら一式ZIPも。</p></article><article><b>03</b><h3>あなたの内容で作る</h3><p>原稿と書体指示をAIへ渡す。<br>原典の方式で、次の資料へ。</p></article></div><a href="guide.html" class="text-link">もう少し詳しい使い方 ↗</a></div></section>
<section class="shell section repository-catalog atelier-catalog" id="skills"><div class="section-heading"><div><p class="eyebrow">02 / SKILLS YOU CAN ACTUALLY USE</p><h2>いい実例には、<br>使えるスキルがある。</h2></div><p>ここで制作した原典から厳選。<br>日本語の指示本文を、そのまま取得できます。</p></div>'''+filters+'''<div class="catalog-tools"><label class="search"><span>⌕</span><input id="skill-query" type="search" placeholder="作りたい資料・スキル名で探す" aria-label="スキルを検索"></label><label class="catalog-status">作例<select id="skill-status"><option value="local">日本語の実例あり</option></select></label><label>並び順<select id="skill-order"><option value="produced">アトリエのおすすめ順</option><option value="name">名前順</option></select></label></div><p id="skill-results" class="results" aria-live="polite"></p><div id="skill-grid" class="skill-grid"></div><a class="text-link entry-bundle" href="downloads/yebisu-japanese-skill-entries.zip" download>日本語スキル本文をまとめて取得 ↓</a><p class="case-sample-note">本文は制作指示です。テンプレート・実装・原文の利用条件は一式ZIPかGitHub原典から。</p></section>
<section class="shell section atelier-fonts" id="fonts"><div class="section-heading"><div><p class="eyebrow">03 / TYPE MAKES THE DIFFERENCE</p><h2>日本語は、<br>書体でもっと良くなる。</h2></div><p>OSS書体と組み合わせの指示。<br>見た目ごと、AIへ渡せます。</p></div><div id="font-atelier"></div></section></main>'''
home=home.replace('<p id="case-results"', '<div class="case-search"><label for="case-query">題材・作風・スキル名</label><input id="case-query" type="search" placeholder="例：茶、手描き、Marp"></div><p id="case-results"')
write('index.html',home)
write('repository.html','<main class="shell doc-shell"><div id="repository-detail"></div></main>','スキルと作り方')
write('case.html','<main class="shell doc-shell"><div id="case-detail"></div></main>','日本語の制作例')
guide_edition=('<p>このガイドとサイト構成は、Claude Opus 5.5で改訂しました（'+esc(scope)+'）。</p>' if opus_verified else '<p>このガイドとサイト構成の改訂は、実行記録の確認を待っています。</p>')
guide='''<main class="shell doc-shell guide-shell"><section class="doc-hero"><p class="eyebrow">MAKE YOUR NEXT DECK</p><h1>作風を見つけたら、<br>自分の内容で。</h1><p class="guide-lead">見る → スキルを取得 → 自分の内容で作る。<br>はじめてでも、この順番で進められます。</p></section>
<section class="doc-section"><h2>受け取れるものは、四種類。</h2><dl class="guide-kit"><div><dt>完成作例</dt><dd>再生・ダウンロードできる完成資料（PowerPoint・Web・PDF）。作風を選ぶための見本で、あなた用のテンプレートではありません。</dd></div><div><dt>スキル本文</dt><dd>短い日本語のMarkdown。制作の手順と、固定した原典GitHubへの参照をまとめた指示書です。原典のコードやテンプレートは入っていません。</dd></div><div><dt>制作一式（ZIP）</dt><dd>作例の入力・制作スクリプト・必要な原典部分・原文LICENSE。テンプレートや生成器を実際に動かす方式では、これが必要です。</dd></div><div><dt>書体</dt><dd>OSS書体の公式配布ファイルとOFL、AI向けの書体指示。見出し・本文・英数字・コードの役割を分けて渡せます。</dd></div></dl></section>
<section class="doc-section"><h2>六つの手順で、最初の一冊を。</h2><ol class="guide-steps"><li><b>見る。</b>トップの「最初の一冊を選ぶ」か作例一覧で、完成スライドを再生する。</li><li><b>確かめる。</b>「作り方」を開き、原典・制作方式・必要な入力を読む。</li><li><b>取得する。</b>スキル本文をコピーするか、Markdownで保存。テンプレートや生成器を使う方式なら、制作一式ZIPも保存して展開する。</li><li><b>組み立てる。</b>作り方ページで原稿・読み手・希望枚数・書体を入れ、依頼文をコピーする。</li><li><b>渡す。</b>AIへ、スキル本文・制作一式・原稿と必須素材・依頼文をまとめて渡す。</li><li><b>直す。</b>できたPowerPointやWeb資料を開き、文字の欠け・改行・書体を確かめて直す。</li></ol><p class="guide-caution"><b>素材が必須の方式があります。</b>論文・画像・既存のPowerPointやHTMLを元に作る方式では、その素材がないと作れません。メモで代わりにはなりません。作り方ページの「入力」を見て、先に用意してください。</p></section>
<section class="doc-section"><h2>Claude Opus 5.5へ渡す、依頼文の例。</h2><p>作り方ページの依頼文ビルダーでも、選んだスキル向けの文を組み立てられます。下は全体の形の例です。</p><pre>添付した日本語スキル本文と制作一式を読み、原典の方式で日本語の資料を作ってください。
原典：スキル本文にある固定commitのGitHub。そのテンプレート・生成器・controllerを使う
読者：新しい企画を検討する担当者
目的：企画の魅力と、次に決めることを伝える
原稿：添付した原稿（この方式で必須の論文・画像・PPTXなどがあれば、それも添付）
分量：8枚前後（段階表示の方式なら、場面数と段階数で指定）
書体：書体アトリエでコピーした指示に従う
出力：選んだ方式に合う完成資料（PowerPoint・Webスライド・PDF）と制作ソース。編集できる範囲も明記する
完成資料と、作り直しに必要な制作ソースをください。原典から変えた点も短く書いてください。</pre><p>ファイルを読み、コードを実行できる環境かどうかで、AIができる範囲は変わります。原典ごとに必要な環境は作り方ページに記載しています。</p></section>
<section class="doc-section"><h2>書体も一緒に用意する。</h2><p>PowerPointでは、使う書体を作成者と受け手の両方へ導入します。Webでは、必要なフォントと条件を一式に同梱します。</p><p><a href="./#fonts">書体を試す →</a> · <a href="downloads/fonts/AI-FONT-GUIDE.md" download>AI向け書体指示 ↓</a> · <a href="downloads/yebisu-oss-font-kit.zip" download>OSS書体一式 ↓</a></p></section>
<section class="doc-section"><h2>原典の強みを、日本語へ。</h2><p>掲載中の作例は、'''+esc(existing_label)+'''中心の並列制作で、各原典のスキル・テンプレート・生成器を使って作りました。コピー・書体・レイアウト・動きを日本語向けに改良し、必要なビルドと主な出力の初回表示を確認しています。</p>'''+guide_edition+'''<p><a href="status.html">制作の状況</a> · <a href="docs/PROJECT.md">制作方針</a> · <a href="docs/PRODUCT_SPEC.md">製品仕様</a> · <a href="licenses.html">原典・利用条件</a></p></section></main>'''
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

# status.html separates current counts, this edit, the earlier production model, checks and publication.
stamp='このページを生成した'+built_on+'時点の記録です。'
status_figures=figures+[('PowerPoint',formats['pptx'],'冊'),('Web',formats['html'],'冊'),('PDF',formats['pdf'],'冊'),('書体ファイル',stats['font_files'],''),('書体の組み合わせ',stats['font_presets'],'')]
status='<main class="shell doc-shell status-shell"><section class="doc-hero"><p class="eyebrow">STATUS / EDITION RECORD</p><h1>いまのアトリエと、<br>今回の改訂。</h1><p class="status-stamp">'+stamp+'</p></section>'
status+='<section class="doc-section"><h2>現在の掲載</h2><dl class="status-figures">'+''.join('<div><dt>'+label+'</dt><dd>'+str(n)+('<small>'+unit+'</small>' if unit else '')+'</dd></div>' for label,n,unit in status_figures)+'</dl><p>通常ページと段階演出は別に数えています（'+esc(step_note)+'）。数はすべて掲載中の正本データから集計しています。</p></section>'
if opus_verified:
    reported=[m for m in editorial.get('reported_models') or [] if public_text(m)]
    status+='<section class="doc-section status-edition"><h2>今回の改訂</h2><p class="status-model"><span>EDITED WITH</span><b>CLAUDE OPUS 5.5</b></p><dl class="status-list"><dt>担当範囲</dt><dd>'+esc(scope)+'</dd><dt>依頼モデル</dt><dd>Claude Opus 5.5（claude-opus-5-5）</dd><dt>報告されたモデル</dt><dd>'+esc('、'.join(reported))+'</dd>'+('<dt>記録日</dt><dd>'+esc(editorial['updated_on'])+'</dd>' if editorial.get('updated_on') and public_text(editorial['updated_on']) else '')+'</dl><p>作例・スキル本文・制作一式は、この改訂で作り直していません。</p></section>'
else:
    status+='<section class="doc-section status-edition is-pending"><h2>今回の改訂</h2><p class="status-pending"><b>保留</b>サイト構成・日本語ガイドの改訂は、実行記録の確認を待っています。確認できるまで、改訂を担当したモデルは表示しません。</p></section>'
batch=goal.get('current_batch',{})
status+='<section class="doc-section"><h2>従来作例の制作</h2><p>掲載'+str(stats['decks'])+'冊は、'+esc(existing_label)+(('（'+esc(existing_model)+'）') if existing_model and existing_label!=existing_model else '')+'中心の並列制作で、各原典のスキル・テンプレート・生成器を使って作った実作例です。今回の改訂で、制作モデルの表記を書き換えてはいません。</p>'+('<p><a href="'+esc(batch['documentation'])+'">最新の制作バッチの記録</a></p>' if batch.get('documentation') else '')+'</section>'
checks=[c for c in (editorial or {}).get('checks') or [] if public_text(c)]
status+='<section class="doc-section"><h2>確認した範囲</h2><ul><li>各作例：原典に必要なビルドと、主な出力の初回表示（既存の制作記録）。</li><li>全ページ・全端末の詳細な検査は行っていません。</li></ul><h3>今回の改訂後の確認</h3>'+('<ul>'+''.join('<li>'+esc(c)+'</li>' for c in checks)+'</ul>' if checks else '<p>未記録です。</p>')+'</section>'
publication=(editorial or {}).get('publication_status')
if publication=='local_preview':
    pub_text='ローカルプレビュー。この記録の時点で、今回の変更は公開サイトへ反映していません。公開専用のスライドサイトは旧版の内容です。'
elif publication:
    pub_text='記録上の状態：'+esc(publication)+'。公開URLへの到達は、このページでは確認していません。' if public_text(publication) else '記録の形式を確認できません。'
else:
    pub_text='記録がありません。公開への反映状況は未記録です。'
status+='<section class="doc-section"><h2>公開への反映</h2><p>'+pub_text+'</p><p class="status-stamp">'+stamp+'</p></section></main>'
write('status.html',status,'制作の状況')
print(f'Japanese atelier built: {len(product["entries"])} curated skills, {stats["decks"]} decks, {stats["pages"]} pages + {stats["steps"]} steps, opus_verified={opus_verified}')
