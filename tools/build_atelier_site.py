"""Build the Japanese slide-skill guide without executing legacy site builders."""
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

SITE_TITLE='AIスライドスキルを効果で選ぶ'
head='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f4f1e9"><title>'''+SITE_TITLE+'''｜八百万図AIツールボックス</title><meta name="description" content="GitHubのAIスライドスキルを、改善できること・必要な入力・作例の該当ページから選べる日本語ガイド。スキル本文と原典一式も取得できます。"><link rel="icon" href="assets/studio-mark.svg">'''
for path in ['assets/studio.css','assets/case-studio.css','assets/repository-studio.css','assets/yebisu-atelier.css','assets/font-atelier.css']:
    if (ROOT/path).exists():head+='<link rel="stylesheet" href="'+version(path)+'">'
# Resolve shared relative imports to the same content-version URLs as entries.
# Versioning only script src would leave cached internal .mjs imports unchanged.
module_imports={
    './'+path.relative_to(ROOT).as_posix():'./'+version(path.relative_to(ROOT).as_posix())
    for path in sorted((ROOT/'assets').rglob('*.mjs')) if path.is_file()
}
head+='<script type="importmap">'+json.dumps({'imports':module_imports},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'
for path in ['assets/case-studio.mjs','assets/repository-detail.mjs','assets/font-atelier.mjs']:
    if (ROOT/path).exists():head+='<script type="module" src="'+version(path)+'"></script>'
head+='''</head><body><a class="skip" href="#main">本文へ移動</a><header class="header"><div class="shell header-inner"><a class="brand atelier-brand" href="./"><span class="brand-symbol">Y.</span><span>AI SLIDE SKILLS<small>スライドスキルの効果と使い方 / 八百万図AIツールボックス</small></span></a><nav aria-label="メインメニュー"><a href="./#skills">スキル一覧</a><a href="guide.html">使い方</a><a href="./#fonts">書体</a></nav><a class="header-github" href="https://github.com/studio-yebisu/yaoyorozu-ai-toolbox-slides">GitHub ↗</a></div></header>'''

tree=ast.parse((ROOT/'tools/build_case_site.py').read_text(encoding='utf-8'))
dialog=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='dialog' for t in n.targets))
dialog=dialog.replace('<a id="case-make"', '<a id="case-skill" class="button outline" download>スキル本文 ↓</a><a id="case-make"')
# The player shows the current skill, its change and what to inspect on this page between the controls and the page strip.
dialog=dialog.replace('<div id="case-pages"', '<section id="case-effect" class="case-effect" aria-label="このスキルの効果"></section><div id="case-pages"',1)
foot='''<footer class="footer"><div class="shell"><div class="footer-main"><div><p class="footer-brand">八百万図AIツールボックス / AI SLIDE SKILLS</p><p>原典スキルの機能・作例・利用条件を日本語で案内しています。</p></div><div class="footer-links"><a href="guide.html">使い方</a><a href="status.html">制作の状況</a><a href="licenses.html">原典・利用条件</a><a href="archive.html">出発点のカタログ</a><a href="https://github.com/studio-yebisu/yaoyorozu-ai-toolbox-slides">GitHub ↗</a></div></div><div class="footer-bottom"><span>原作者とスキル・素材・書体の個別条件を保持しています。</span><span>作例は各原典の方式で制作</span></div></div></footer>'''

def write(path,body,title=None):
    top=head if not title else head.replace('<title>'+SITE_TITLE+'｜八百万図AIツールボックス</title>','<title>'+esc(title)+'｜八百万図AIツールボックス</title>')
    body=body.replace('<main', '<main id="main"', 1)
    (ROOT/path).write_text(top+body+foot+dialog+'</body></html>',encoding='utf-8',newline='\n')

step_note='・'.join(c['repository'].split('/')[-1]+' '+str(c['page_count'])+'段階' for c in step_cases)
existing_label=model_name(existing_model) if existing_model else '従来の制作モデル'
scope=(editorial or {}).get('scope') or 'サイト構成・日本語ガイド・使い方の改訂'
if not public_text(scope):scope='サイト構成・日本語ガイド・使い方の改訂'

# A short record at the end of the page; it does not displace the skill descriptions.
if opus_verified:
    edition='<aside class="atelier-edition" aria-label="改訂の担当"><div class="shell edition-inner"><p class="edition-model"><span>先行改訂</span><b>CLAUDE OPUS 5.5</b></p><p class="edition-copy"><b>'+esc(scope)+'</b>の先行改訂に、Claude Opus 5.5を使用しました。<span>現在の原典照合・個別修復・フォント拡充はCodexが担当。独立評価はKimi K3とOpus 5.5で進行中です。</span></p><a class="edition-link" href="status.html">改訂の記録 →</a></div></aside>'
else:
    edition='<aside class="atelier-edition is-pending" aria-label="今回の改訂"><div class="shell edition-inner"><p class="edition-model"><span>EDITION NOTE</span><b>改訂の記録を確認中</b></p><p class="edition-copy">サイト構成・日本語ガイドの改訂は、実行記録の確認を待っています。<span>掲載中の作例は、'+esc(existing_label)+'中心の並列制作による原典方式の実作例です。</span></p><a class="edition-link" href="status.html">制作の状況 →</a></div></aside>'

figures=[('掲載スキル',stats['skills'],''),('作例',stats['decks'],'冊'),('通常ページ',stats['pages'],'枚'),('段階演出',stats['steps'],'段階'),('OSS書体',stats['font_families'],'書体')]

# Improvement entrances. The ids and labels match NEEDS in assets/skill-effects.mjs; counts are filled from the data at runtime.
needs=[('motion','動きで順に見せる','段階表示・アニメーション'),('edit','受け取った人が編集できる','PowerPoint・ブラウザー編集'),('diagram','図解・概念図にする','矢印・注釈・構造'),('convert','既存の資料を変換する','HTML・画像・PDF・PPTXから'),('layout','レイアウトと書体を整える','版面・余白・デザイン規則'),('academic','数式・論文を発表にする','数式・研究発表')]
need_items=''.join('<li><button type="button" data-need="'+i+'" data-scroll aria-pressed="false"><b>'+label+'</b><span>'+hint+'</span><small data-need-count="'+i+'"></small></button></li>' for i,label,hint in needs)

home='''<main><section class="shell effect-hero" aria-labelledby="hero-title"><p class="eyebrow">八百万図AIツールボックス / 日本語のAIスライドスキル</p><h1 id="hero-title">AIスライドスキルを、効果で選ぶ</h1><p class="hero-description">改善したい点を選び、スキルの機能と作例での使い方を確認できます。</p><div class="need-entrance" role="group" aria-labelledby="need-title"><p id="need-title" class="need-title">改善したいこと</p><ul>'''+need_items+'''</ul></div></section>
<section class="shell section effect-catalog" id="skills" aria-labelledby="skills-title"><div class="section-heading"><div><p class="eyebrow">01 / SKILLS</p><h2 id="skills-title">スキル一覧</h2></div><p>各カードは、スキルの機能・変わること・必要な入力・作例で確かめる箇所の順に並べています。</p></div><p id="skill-results" class="results" aria-live="polite"></p><div class="effect-tools"><label class="effect-search" for="skill-query"><span>検索</span><input id="skill-query" type="search" placeholder="機能・困りごと・用途・リポジトリ名" autocomplete="off"></label><label for="skill-need">改善したいこと<select id="skill-need"><option value="all">すべて</option></select></label><label for="skill-format">形式<select id="skill-format"><option value="all">すべて</option><option value="pptx">PowerPoint</option><option value="html">Web</option><option value="pdf">PDF</option></select></label><label for="skill-tag">方式タグ<select id="skill-tag"><option value="all">すべて</option></select></label></div><div id="skill-active" class="effect-active" aria-label="選択中の条件"></div><p id="skill-data-note" class="effect-data-note" hidden></p><div id="skill-list" class="effect-list"></div><p class="effect-bundle"><a href="downloads/yebisu-japanese-skill-entries.zip" download>日本語スキル本文をまとめて取得 ↓</a><span>本文は制作指示です。テンプレート・実装・原文の利用条件は、各スキルの一式ZIPかGitHub原典にあります。</span></p></section>
<section class="effect-how" aria-labelledby="how-title"><div class="shell"><p class="eyebrow">HOW TO USE</p><h2 id="how-title">使い方</h2><ol class="effect-how-steps"><li><b>1</b><h3>スキルを選ぶ</h3><p>改善したいこと・形式で絞り、機能と「どう変わる」を読む。</p></li><li><b>2</b><h3>効果をページで確認</h3><p>「◯ページ目を確認」で、スキルの指示が表れた箇所を開く。</p></li><li><b>3</b><h3>入力・環境・条件を確認</h3><p>必須の論文・画像・PPTXなど、実行環境、利用条件を確かめる。</p></li><li><b>4</b><h3>本文と一式を取得</h3><p>日本語スキル本文と、必要な原典一式ZIPを保存する。</p></li><li><b>5</b><h3>自分の原稿へ使う</h3><p>依頼文を組み立て、本文・一式・原稿と一緒にAIへ渡す。</p></li></ol><a href="guide.html" class="text-link">詳しい使い方 →</a></div></section>
<section class="shell section atelier-fonts" id="fonts" aria-labelledby="fonts-title"><div class="section-heading"><div><p class="eyebrow">02 / FONTS</p><h2 id="fonts-title">書体を選ぶ</h2></div><p>無料フォントの見本・公式サイト・ダウンロードをまとめました。</p></div><div id="font-atelier"></div></section>'''+edition+'''</main>'''
write('index.html',home)
write('repository.html','<main class="shell doc-shell"><div id="repository-detail"></div></main>','スキルの効果と使い方')
write('case.html','<main class="shell doc-shell"><div id="case-detail"></div></main>','日本語の制作例')
guide_edition=('<p>Claude Opus 5.5が先行改訂を担当しました（'+esc(scope)+'）。現在の原典照合・個別修復・フォント拡充はCodexが担当しています。</p>' if opus_verified else '<p>このガイドとサイト構成の改訂は、実行記録の確認を待っています。</p>')
guide='''<main class="shell doc-shell guide-shell"><section class="doc-hero"><p class="eyebrow">HOW TO USE</p><h1>スキルの選び方と使い方</h1><p class="guide-lead">スキルを選ぶ → 効果を具体ページで確認 → 入力・環境・条件を確認 → 本文と原典一式を取得 → 自分の原稿へ適用。</p></section>
<section class="doc-section"><h2>五つの手順</h2><ol class="guide-steps"><li><b>スキルを選ぶ。</b>トップの「改善したいこと」・形式・検索で絞り、カードの機能名と「どう変わる」「渡すもの」「受け取るもの」を読みます。</li><li><b>効果を具体ページで確認する。</b>「◯ページ目を確認」で作例の該当ページを開き、見る箇所とスキルの指示を照らし合わせます。記載しているのは、この作例で使った機能です。原典の全機能ではありません。</li><li><b>入力・環境・条件を確認する。</b>スキルのページで、必須の入力、実行環境、利用条件（非商用条件など）と、この作例で確認していないことを読みます。</li><li><b>取得する。</b>日本語スキル本文（Markdown）を保存します。テンプレートや生成器を動かす方式では、原典一式ZIPも保存して展開します。</li><li><b>自分の原稿へ適用する。</b>スキルのページで原稿・読み手・枚数・書体を入れて依頼文を組み立て、スキル本文・一式・原稿・必須素材と一緒にAIへ渡します。できた資料の文字欠け・改行・書体を確かめて直します。</li></ol><p class="guide-caution"><b>必須の素材は、メモで代わりになりません。</b>論文・画像・既存のPowerPointやHTMLを元に作る方式では、その素材がないと作れません。スキルのページの「渡すもの」を見て、先に用意してください。</p><p class="guide-caution"><b>原典が対応しない出力は作れません。</b>Webスライドの方式から編集できるPPTXの図形を作る、などの原典にない出力を依頼文だけで求めないでください。出力形式は「受け取るもの」の範囲で選びます。</p></section>
<section class="doc-section"><h2>受け取れるもの</h2><dl class="guide-kit"><div><dt>スキル本文</dt><dd>短い日本語のMarkdown。制作の手順と、固定した原典GitHubへの参照をまとめた指示書です。原典のコードやテンプレートは入っていません。</dd></div><div><dt>原典一式（ZIP）</dt><dd>作例の入力・制作スクリプト・必要な原典部分・原文LICENSE。テンプレートや生成器を実際に動かす方式では、これが必要です。</dd></div><div><dt>完成作例</dt><dd>再生・ダウンロードできる完成資料（PowerPoint・Web・PDF）。スキルの効果を確かめる見本で、あなた用のテンプレートではありません。</dd></div><div><dt>書体</dt><dd>OSS書体の公式配布ファイルとOFL、AI向けの書体指示。見出し・本文・英数字・コードの役割を分けて渡せます。</dd></div></dl></section>
<section class="doc-section"><h2>AIへ渡す依頼文の例</h2><p>スキルのページの依頼文ビルダーで、選んだスキル向けの文を組み立てられます。下は全体の形の例です。</p><pre>添付した日本語スキル本文と原典一式を読み、原典の方式で日本語の資料を作ってください。
使う機能：スキルのページに記載した機能名
原典：スキル本文にある固定commitのGitHub。そのテンプレート・生成器・controllerを使う
読者：新しい企画を検討する担当者
目的：企画の要点と、次に決めることを伝える
原稿：添付した原稿（この方式で必須の論文・画像・PPTXなどがあれば、それも添付）
分量：8枚前後（段階表示の方式なら、場面数と段階数で指定）
書体：書体の欄でコピーした指示に従う
出力：この方式が対応する完成資料（PowerPoint・Webスライド・PDFのいずれか）と制作ソース。編集できる範囲も明記する
完成資料と、作り直しに必要な制作ソースをください。原典から変えた点も短く書いてください。</pre><p>ファイルを読み、コードを実行できる環境かどうかで、AIができる範囲は変わります。原典ごとに必要な環境は、スキルのページの「必要な環境」と「制作方法と実行コマンド」に記載しています。</p></section>
<section class="doc-section"><h2>書体を用意する</h2><p>PowerPointでは、使う書体を作成者と受け手の両方へ導入します。Webでは、必要なフォントと条件を一式に同梱します。</p><p><a href="./#fonts">書体を選ぶ →</a> · <a href="downloads/fonts/AI-FONT-GUIDE.md" download>AI向け書体指示 ↓</a> · <a href="downloads/yebisu-oss-font-kit.zip" download>OSS書体一式 ↓</a></p></section>
<section class="doc-section"><h2>作例の制作について</h2><p>掲載中の作例は、'''+esc(existing_label)+'''中心の並列制作から始め、現在は原典と照合しながら個別に作り直しています。制作時と修復時の担当・実行方法・確認範囲は各作例に記録しています。</p>'''+guide_edition+'''<p><a href="status.html">制作の状況</a> · <a href="docs/PROJECT.md">制作方針</a> · <a href="docs/PRODUCT_SPEC.md">製品仕様</a> · <a href="licenses.html">原典・利用条件</a></p></section></main>'''
write('guide.html',guide,'使い方')

terms='''<main class="shell doc-shell"><section class="doc-hero"><p class="eyebrow">CREDITS / LICENSES</p><h1>原典と利用条件</h1></section><section class="doc-section"><h2>原典と日本語版の条件</h2><p>各スキルの作者と固定原典、原文LICENSE・NOTICEを保持しています。日本語派生・制作コードの変更は各キットに記載。カタログのCC0を原典コード、素材、書体の条件へ広げません。</p><div class="license-table-wrap"><table class="doc-table"><thead><tr><th>原典</th><th>条件</th><th>日本語版</th></tr></thead><tbody>'''
for e in product['entries']:
    p=profiles[e['repository']];official='https://github.com/'+e['repository']+'/tree/'+p['upstream_commit']
    terms+='<tr><td><a href="'+official+'">'+esc(e['repository'])+'</a></td><td>'+esc(p.get('license') or '個別条件')+('<br><small>'+esc(p['license_notice_ja'])+'</small>' if p.get('license_notice_ja') else '')+'</td><td><a href="'+esc(e['skill_download'])+'" download>スキル本文</a> · <a href="repository.html?repo='+quote(e['repository'],safe='/')+'">効果・使い方・配布</a></td></tr>'
terms+='''</tbody></table></div><p>Guizang由来のAGPL-3.0は対応する変更後ソースと条件をZIPに提供。MckのApache-2.0は原文LICENSE・NOTICEを保持。Bentoの固定shell・NOTICEも保持しています。SOILはソフトウェアがMIT、設計文・プロンプトなどの内容がCC BY-NC-SA 4.0です。内容を含む日本語派生は非商用・継承条件を保持します。原典に含まれる全素材への一括許諾を表示していません。</p></section><section class="doc-section"><h2>公式配布のOSSフォント</h2><p>新しい書体キットは固定commitの未改変TTFとOFL原文を同梱。OSの標準搭載書体を抽出したものではありません。本文・見出し・英数字の用途を分けて使用します。</p><ul>'''
for f in load('data/oss-font-kit.json')['families']:
    terms+='<li>'+esc(f['family'])+' / <a href="'+esc(f['license_url'])+'">OFL原文</a> / <a href="'+f['download']+'" download>原配布フォント</a></li>'
terms+='''</ul><p><a href="data/oss-font-kit.json">配布元と使用書体の記録</a> · <a href="data/fonts.json">従来の日本語Web書体</a> · <a href="data/preset-fonts.json">英字プリセット書体</a></p></section><section class="doc-section"><h2>出発点のカタログと制作履歴</h2><p><a href="archive.html">原209件の記録</a>と過去の制作物は保存しています。現在は実例と使い方のあるスキルを選んで掲載。原作者の紹介画像と、この環境で作った日本語資料を区別しています。</p></section></main>'''
write('licenses.html',terms,'原典・利用条件')
write('archive.html','''<main class="shell doc-shell"><section class="doc-hero"><p class="eyebrow">ARCHIVE</p><h1>出発点のカタログ</h1></section><section class="doc-section"><p>原カタログは資料として保存しています。現在の掲載は、実際に制作した日本語資料と使えるスキルを選んだものです。209件すべてを作ることは、このプロジェクトの制作条件にしていません。</p><p><a href="data/skills.json" download>原209件の日本語カタログJSON ↓</a> · <a href="https://github.com/zhuyansen/awesome-codex-ppt-skills">出発点のGitHub ↗</a></p><p><a href="./#skills">スキル一覧へ戻る →</a></p></section></main>''','出発点のカタログ')

# status.html separates current counts, this edit, the earlier production model, checks and publication.
stamp='このページを生成した'+built_on+'時点の記録です。'
status_figures=figures+[('PowerPoint',formats['pptx'],'冊'),('Web',formats['html'],'冊'),('PDF',formats['pdf'],'冊'),('書体ファイル',stats['font_files'],''),('書体の組み合わせ',stats['font_presets'],'')]
status='<main class="shell doc-shell status-shell"><section class="doc-hero"><p class="eyebrow">STATUS / EDITION RECORD</p><h1>制作の状況と今回の改訂</h1><p class="status-stamp">'+stamp+'</p></section>'
status+='<section class="doc-section"><h2>現在の掲載</h2><dl class="status-figures">'+''.join('<div><dt>'+label+'</dt><dd>'+str(n)+('<small>'+unit+'</small>' if unit else '')+'</dd></div>' for label,n,unit in status_figures)+'</dl><p>通常ページと段階演出は別に数えています（'+esc(step_note)+'）。数はすべて掲載中の正本データから集計しています。</p></section>'
if opus_verified:
    reported=[m for m in editorial.get('reported_models') or [] if public_text(m)]
    status+='<section class="doc-section status-edition"><h2>先行改訂と現在の担当</h2><p class="status-model"><span>先行改訂</span><b>CLAUDE OPUS 5.5</b></p><dl class="status-list"><dt>担当範囲</dt><dd>'+esc(scope)+'</dd><dt>依頼モデル</dt><dd>Claude Opus 5.5（claude-opus-5-5）</dd><dt>報告されたモデル</dt><dd>'+esc('、'.join(reported))+'</dd>'+('<dt>記録日</dt><dd>'+esc(editorial['updated_on'])+'</dd>' if editorial.get('updated_on') and public_text(editorial['updated_on']) else '')+'</dl><p>Opus 5.5による先行改訂の実行記録です。現在の原典照合・個別修復・フォント拡充はCodexが担当しています。独立評価の採点と制作担当は分け、各作例に実際の変更範囲を記録しています。</p></section>'
else:
    status+='<section class="doc-section status-edition is-pending"><h2>今回の改訂</h2><p class="status-pending"><b>保留</b>サイト構成・日本語ガイドの改訂は、実行記録の確認を待っています。確認できるまで、改訂を担当したモデルは表示しません。</p></section>'
batch=goal.get('current_batch',{})
status+='<section class="doc-section"><h2>従来作例の制作</h2><p>掲載'+str(stats['decks'])+'冊は、'+esc(existing_label)+(('（'+esc(existing_model)+'）') if existing_model and existing_label!=existing_model else '')+'中心の並列制作から始めた作例です。その後、Opus 5.5が一部を制作・修復し、現在はCodexが原典照合と個別修復を進めています。各作例には、初回制作と修復の担当・実行方法を分けて記録しています。</p>'+('<p><a href="'+esc(batch['documentation'])+'">最新の制作バッチの記録</a></p>' if batch.get('documentation') else '')+'</section>'
review_progress=load('data/review-progress.json') if (ROOT/'data/review-progress.json').exists() else {}
review_rows=review_progress.get('reviews',[])
review_text='全61件の初回評価が完了しました。'+('作例ごとの88点枠の平均は、'+ '、'.join(r['reviewer']+' '+format(r['mean_case_score'],'.2f')+' / 88' for r in review_rows)+'。' if review_rows else '')+'この初回版では、一覧・詳細・PC/スマホ操作の共通12点を採点していません。これらは初回の凍結版への点数です。最新の修正を含む全61件の共通評価は未了で、両者100点にはまだ達していません。'
partial=review_progress.get('partial_recheck',{})
if partial:
    review_text+=' 修正版の途中評価：Kimi K3は'+str(partial['kimi_completed_cases'])+'件、'+str(partial['kimi_score_min'])+'〜'+str(partial['kimi_score_max'])+' / 88。'
    if partial.get('opus_completed_cases'):
        review_text+='Opus 5.5は'+str(partial['opus_completed_cases'])+'件、'+str(partial['opus_score_min'])+'〜'+str(partial['opus_score_max'])+' / 88。'
    review_text+='点数は各固定版への評価です。最新修正を含む全件と共通12点は未了です。'
ui_reviews=review_progress.get('global_UI_rechecks',[])
if ui_reviews:
    review_text+=' 共通UIの別評価：'+'、'.join(r['reviewer']+' '+str(r['score'])+' / 12（'+('UI修復後' if r.get('ui_revision')=='after_ui_repairs' else 'UI修復前')+'の固定版）' for r in ui_reviews)+'。修復後のUIに対するOpus 5.5の評価は未了です。'
status+='<section class="doc-section"><h2>独立評価</h2><p>Kimi K3とClaude Opus 5.5が、原典の効果説明35点・作例での活用35点・視覚品質と操作30点で評価しています。</p><p>'+esc(review_text)+'</p><p><a href="docs/SKILL_EFFECT_REVIEW.md">評価条件と確認範囲</a> · <a href="data/review-progress.json">採点の集計</a></p></section>'
checks=[c for c in (editorial or {}).get('checks') or [] if public_text(c)]
status+='<section class="doc-section"><h2>確認した範囲</h2><ul><li>生成・全ページ表示・操作・配布物の確認範囲は、各作例のQAに記録しています。</li><li>修復版の独立評価と、端末ごとの確認は作業中です。</li></ul><h3>今回の改訂後の確認</h3>'+('<ul>'+''.join('<li>'+esc(c)+'</li>' for c in checks)+'</ul>' if checks else '<p>未記録です。</p>')+'</section>'
publication=(editorial or {}).get('publication_status')
if publication=='local_preview':
    pub_text='ローカルプレビュー。この記録の時点で、今回の変更は公開サイトへ反映していません。公開専用のスライドサイトは旧版の内容です。'
elif publication:
    pub_text='記録上の状態：'+esc(publication)+'。公開URLへの到達は、このページでは確認していません。' if public_text(publication) else '記録の形式を確認できません。'
else:
    pub_text='記録がありません。公開への反映状況は未記録です。'
status+='<section class="doc-section"><h2>公開への反映</h2><p>'+pub_text+'</p><p class="status-stamp">'+stamp+'</p></section></main>'
write('status.html',status,'制作の状況')
print(f'Japanese skill guide built: {len(product["entries"])} skills, {stats["decks"]} decks, {stats["pages"]} pages + {stats["steps"]} steps, opus_verified={opus_verified}')
