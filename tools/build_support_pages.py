from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
examples=json.loads((ROOT/'data/actual-examples.json').read_text(encoding='utf-8'))
pins=json.loads((ROOT/'data/upstreams.json').read_text(encoding='utf-8'))
fonts=json.loads((ROOT/'data/fonts.json').read_text(encoding='utf-8'))
header='<header class="header"><div class="shell header-inner"><a class="brand" href="./"><img width="32" height="32" src="assets/studio-mark.svg" alt=""><span>AIスライドスキル集<span>STUDIO YEBISU / 209の選択肢</span></span></a><nav aria-label="メインメニュー"><a href="./#examples">209件のスキル</a><a href="./#fonts">フォント</a><a href="guide.html">使い方</a><a href="licenses.html">出典・利用条件</a></nav></div></header>'
footer='<footer class="footer"><div class="shell"><p class="footer-brand">AIスライドスキル集 / STUDIO YEBISU</p><a class="text-link" href="./#examples">209件の一覧へ戻る ↑</a></div></footer>'
def page(title,body):return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}｜AIスライドスキル集</title><link rel="icon" href="assets/studio-mark.svg"><link rel="stylesheet" href="assets/studio.css"></head><body><a class="skip" href="#main">本文へ進む</a>{header}<main id="main" class="shell doc-shell">{body}</main>{footer}</body></html>'
rows=''.join(f'<tr><td><a href="https://github.com/{e["repository"]}">{escape(e["repository"])}</a></td><td>{escape(e["style"])}</td><td>{e["slide_count"]}枚</td><td><a href="{e["html"]}">作例を開く</a> · <a href="{e["proof"]}">制作記録</a></td></tr>' for e in examples)
guide='''<section class="doc-hero"><p class="eyebrow">HOW TO CHOOSE / 209 ORIGINAL PROJECTS</p><h1>作例から、スキルを選ぶ。</h1><p>元の209件を、用途と見た目から探せるカタログです。</p></section><section class="doc-section"><h2>気になるカードを開く</h2><p>分類と検索で探し、カードの作例ボタンを押すと浮かぶビューアーが開きます。日本語の作例はページ送り・再生・講稿に対応。矢印キーでもページを送れます。</p><p>「日本語の実制作」は、その掲載スキルのSKILL、テンプレート、実装に従って作ったものです。「公開作例・紹介画像」は原作者の公開素材です。紹介画像からスライドが再生できるとは限りません。</p><h2>元のスキルと日本語版</h2><p>「元のスキルを開く」から作者のREADMEと導入方法へ進めます。日本語対応版がある場合は、原典の実装と個別ライセンスを保持したZIPを取得できます。任意のエージェントのスキルフォルダーに展開して使えます。</p><p>原典ごとに生成経路や必要な環境が異なります。APIや画像生成が必要なものを、別の共通レンダラーで作った作例へ置き換えていません。</p></section><section class="doc-section" id="verification"><h2>今回の日本語作例：3件・12枚</h2><table class="doc-table"><thead><tr><th>該当スキル</th><th>制作方法・スタイル</th><th>枚数</th><th>出力と記録</th></tr></thead><tbody>'''+rows+'''</tbody></table><p>Guizangは元のHTMLテンプレートとCSS・WebGL・Motion・ページ制御を使用。Frontend Slidesは元の固定ステージと指定プリセットを適用。PPT Masterは元の品質チェッカーとSVG→PPTX変換器を実行しました。</p><p>ブラウザーで12ページの表示とカタログの再生を確認。PPT MasterのブラウザープレビューはPPTXへの入力SVGです。PowerPointアプリでの表示、Guizangの発表者モードの全機能、209件すべての生成は今回の確認範囲に含まれていません。</p><p>再生成コード：<a href="tools/build_actual_examples.py">build_actual_examples.py</a> · <a href="data/actual-examples.json">作例と原典の対応JSON</a></p></section><section class="doc-section"><h2>日本語の書体も、仕上がりの一部</h2><p>Noto Sans JP、Noto Serif JP、BIZ UDPGothicを目的に合わせて選べます。元スキルの英字書体を保ち、日本語には日本語を含む書体を指定。意味のまとまりで改行し、長文は文字を小さくする前にページを分けます。</p><p>HTML版は収録文字のWebフォントを使用。新しい文字を増やすときは、公式のフルフォントから作り直してください。PPTXは閲覧するPCにもNoto Sans JPが必要です。</p><a href="licenses.html#fonts">フォントの出典とOFL原文 →</a></section>'''
(ROOT/'guide.html').write_text(page('使い方',guide),encoding='utf-8')
audits=[]
for s in pins:
    if s.get('derived_skill'):
        handling=f'原典実装を同梱した日本語版：<a href="skill-forks/{s["derived_skill"]}/SKILL.md">{s["derived_skill"]}</a> / <a href="downloads/{s["derived_skill"]}.zip">改変ソースZIP</a>'
    elif s['repository']=='anthropics/skills':handling='PPTXスキルに改変・再配布を制限する記述があるため、フォーク対象から除外。実装は同梱していません。'
    else:handling='利用条件の確認・参考情報。今回このツールでの日本語作例は制作していません。'
    terms='<br>'.join(f'<a href="{e["url"]}">{escape(e["upstream_path"])} 原文 ↗</a>' for e in s['license_evidence'])
    audits.append(f'<article class="audit-card"><div class="audit-meta"><span>{escape(s.get("github_license") or "個別条件")}</span></div><h3><a href="{s["url"]}">{escape(s["repository"])} ↗</a></h3><p>{handling}</p><p>固定コミット<br><a href="{s["url"]}/tree/{s["commit"]}"><code>{s["commit"]}</code></a></p><p>{terms}</p></article>')
font_cards=''.join(f'<article class="audit-card"><h3>{escape(f["renamed_family"])}</h3><p>OFL-1.1 / {f["glyphs"]}文字</p><p>{escape(f["modification"])}</p><p><a href="{f["source_url"]}">公式の原本 ↗</a> · <a href="assets/fonts/{f["family"]}-OFL.txt">OFL原文</a></p></article>' for f in fonts)
license_body='''<section class="doc-hero"><p class="eyebrow">SOURCES & LICENSES</p><h1>作者と、個別の利用条件。</h1><p>カタログのライセンスと、掲載スキルのライセンスは別です。</p></section><section class="doc-section"><h2>このカタログの収録範囲</h2><table class="doc-table"><thead><tr><th>対象</th><th>利用条件</th><th>扱い</th></tr></thead><tbody><tr><td>カタログ・独自のサイト部分</td><td>CC0-1.0</td><td>元のCC0カタログを継承、日本語編集：Studio Yebisu</td></tr><tr><td>各掲載スキル</td><td>原典ごと</td><td>209件のカードは原典へリンク。全件の現行ライセンスを再審査したとは扱いません。</td></tr><tr><td>Guizangのフォーク・HTMLテンプレート派生物</td><td>AGPL-3.0</td><td>元LICENSEと改変ソースを提供。CC0へ再許諾しません。</td></tr><tr><td>Frontend Slides / PPT Masterのフォーク</td><td>MIT</td><td>原作者の著作権・LICENSE・元実装を保持</td></tr><tr><td>日本語・プリセットの書体</td><td>OFL-1.1</td><td>公式原本、原文、変更記録を保持</td></tr><tr><td>Motion / Lucide</td><td>MIT / ISC</td><td>Guizangの依存と原文を個別に同梱</td></tr><tr><td>原作者の公開作例・紹介画像</td><td>それぞれの出典条件</td><td>原版で確認した帰属を保持</td></tr></tbody></table><p>日本語版はStudio Yebisuによる分派です。原作者の公式日本語版や推奨ではありません。改変ソースと原文は各ZIPに含まれ、<a href="skill-forks/guizang-ppt-skill-ja/SOURCE.json">Guizangのソース対応記録</a>からファイルを確認できます。</p></section><section class="doc-section"><h2>固定コミットで確認した原典</h2><p>今回の日本語作例と結びつけた原典は3件です。他は利用条件と参考情報の確認記録です。</p><div class="audit-grid">'''+''.join(audits)+'''</div></section><section class="doc-section" id="fonts"><h2>日本語の書体</h2><p>PCにある商用フォントを抜き出して配布していません。公式OFLフォントを収録文字へ絞り、内部名を変更し、著作権と原文を保持しています。</p><div class="audit-grid">'''+font_cards+'''</div><p>元の英字スタイルのArchivo Black、Space Grotesk、Playfair Display、Source Serif 4、IBM Plex Monoも公式OFL原本を使用。<a href="data/preset-fonts.json">固定コミットと取得記録</a> · <a href="data/browser-dependencies.json">Motion / Lucideの取得記録</a></p></section><section class="doc-section"><h2>209件の原版と公開画像</h2><p>原カタログ：<a href="https://github.com/zhuyansen/awesome-codex-ppt-skills">zhuyansen / awesome-codex-ppt-skills</a>。分類・スター数・原版評価は2026年10月11日の取得記録です。</p><p><a href="docs/プロジェクト作例の出典.md">公開画像の出典記録</a> · <a href="docs/出典とライセンス.md">カタログの帰属</a> · <a href="data/project-workflows.json">209件と作例の対応JSON</a></p></section>'''
(ROOT/'licenses.html').write_text(page('出典と利用条件',license_body),encoding='utf-8')
readme=ROOT/'README.md';old=readme.read_text(encoding='utf-8');tail=old[old.index('<a id="choose"></a>'):]
intro='''# AIスライドスキル集 / 209件を日本語で選ぶ

元の209件のスキル・作者・分類を主役にした、日本語の作例カタログ。Studio Yebisuが編集・制作・サイト開発しています。

[ウェブサイト](https://studio-yebisu.github.io/awesome-codex-ppt-skills-ja/) · [使い方](guide.html) · [出典と利用条件](licenses.html)

現在の改修版はローカルでレビュー可能。公開サイトの更新はまだ実施していません。

- 209件の元プロジェクトを検索・6分類・作者・個別ライセンスから選択。
- カードから浮かぶ作例ビューアー。日本語の実制作は再生、ページ送り、講稿に対応。
- 3つの該当スキルで日本語作例を12枚制作。原テンプレートや指定スタイル、上流変換器を実際に使用。
- 原作者の公開画像、GitHub紹介画像、未制作を実制作と区別。
- 日本語版フォークは元実装・著作権・個別のLICENSEを保持。原作者の公式日本語版ではありません。

## 実制作の対応

| 掲載スキル | 適用したもの | 日本語作例 | 日本語版 |
|---|---|---|---|
'''
for e in examples:
    pin=next(s for s in pins if s['repository']==e['repository']);intro+=f'| [{e["repository"]}](https://github.com/{e["repository"]}) | {e["method_label"]} | [{e["slide_count"]}枚]({e["html"]}) / [制作記録]({e["proof"]}) | [{pin["derived_skill"]}](skill-forks/{pin["derived_skill"]}/SKILL.md) |\n'
intro+='''
PPT Masterはフォークに同梱した元のチェッカーと変換器でネイティブPPTXを出力。ブラウザーは入力SVGを表示します。PowerPointアプリ内の表示検証は未実施で、Noto Sans JPの導入が必要です。Guizangの発表者モードの全機能、209件すべての生成は検証済みと扱いません。

## 開発と正本

```text
python -m http.server 8847 --bind 127.0.0.1
node tools/build_site.mjs
python tools/verify_release.py
```

`data/skills.json`が元の209件、`data/actual-examples.json`が実制作、`data/project-workflows.json`がその対応です。サイトは静的HTML/CSS/ES modules。実制作の再生成は`tools/build_actual_examples.py`、日本語版の配布は`tools/package_actual_forks.py`。元ソースの取得は`tools/acquire_real_skill.py`。元コミットの全アーカイブはビルド用キャッシュへ保存し、各作例に使用ファイルのハッシュを記録しています。

サイト・カタログの独自部分はCC0。各フォークはMIT / AGPL、フォントはOFL、公開画像は原典ごとの条件です。CC0を掲載物へ一括適用しません。

前回作った独立5スキル・共通レンダラーの6デッキは、今回の意図に合わない不採用試作として保全。[記録](docs/withdrawn-prototypes.md)。現在の実制作の件数や制作手段に含めません。

以下は元の209件と原版の実測比較の記録であり、今回の制作検証結果とは別です。

---

'''
readme.write_text(intro+tail,encoding='utf-8')
print('Catalog guide, individual licenses and original-209 README updated')
