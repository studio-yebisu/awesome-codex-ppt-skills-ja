"""Create self-contained Japanese derivatives, keeping each upstream's license and provenance."""
from pathlib import Path
import json, shutil, zipfile
ROOT=Path(__file__).resolve().parents[1]
TYPOGRAPHY='''# 日本語のスライド制作

16:9・1280×720を出発点にする。見出しは48–72px、本文は26–36px程度を目安に、見る距離に合わせる。
文章が多いときは内容を整理し、複数ページへ分ける。1枚1論点を目安に、比較や関係性は図で示す。
句読点・閉じ括弧を行頭に置かず、開き括弧を行末に残さない。数字と単位、固有名詞の途中で改行しない。
英数字だけのフォントを日本語本文へ指定しない。Noto Sans JPは標準、BIZ UDPGothicは教材・業務資料、Noto Serif JPは表紙・企画に向く。
明朝は大きな見出しで活かし、画面上の小さな本文は読みやすさを確認する。正規のフォントをインストールして使用する。

事実・推測・説明用の架空データを分ける。数値に単位、比較に条件を付ける。外部情報は原典と確認日をノートに記録する。
図表、文字、図形を編集可能に保ち、全体を画像1枚にしない。背景イラストが必要な場合だけ、画像を別レイヤーにする。
動きは説明の順番を助ける範囲で使う。短い出現を基本にし、最終フレームを読み取れる時間を残す。
SVG/HTMLとPPTXは別の出力。PPTXの静止版をHTMLアニメーションの再現と呼ばない。
自動チェックは文字範囲とファイル構造の検査であり、内容や見た目の承認ではない。各ページを表示して確認する。
'''
SCHEMA='''# 制作JSON

`assets/example.json` が実行できる入力例。`scripts/render-deck.mjs` のvalidatorも参照する。

デッキには `id`（英小文字・数字・ハイフン）、`title`、`font`、`background`、`ink`、`slides` を指定。
各ページは `title`、`notes`、`duration`（秒）、`nodes` を持つ。キャンバスは1280×720。
ノードは `text` / `rect` / `circle` / `line` / `path`。座標とサイズはpx、色は16進カラー。
`text` は `x,y,text,size,weight` を指定。`y` はベースライン。改行は `\\n`、`leading` は行送り。
`rect` は `x,y,w,h,fill`。`circle` は `x,y,r,fill`。線は `x,y,x2,y2,stroke,strokeWidth`。
`path` はSVG pathの `d`。追加HTMLや外部スクリプトをJSONへ入れない。
`delay` は出現を遅らせるミリ秒。`font` と `anchor`（start / middle / end）はテキスト単位で指定できる。

SVGとHTMLを生成：

```text
node <このスキル>/scripts/render-deck.mjs <入力JSON> <新しい出力フォルダ>
```

Node.js 22以上を推奨。ライブラリやアカウント、APIキーは不要。
HTMLをブラウザで開き、左右キー・自動再生・講稿を確認する。SVGはベクトル編集アプリで開ける。
出力フォルダがすでにある場合、CLIは上書きせず停止する。新しいフォルダを指定する。
Webフォントは別配布。このパッケージではフォント本体を同梱しない。OFL配布元のNoto / BIZ UDを使用する。

編集可能PPTXが必要な場合は `scripts/export-pptx.mjs` を使う。
スキルフォルダで `npm install --ignore-scripts` した後、
`node <このスキル>/scripts/export-pptx.mjs <入力JSON> <新しいファイル.pptx>` を実行する。
PptxGenJSを使用し、文字・図形・線はネイティブオブジェクト、自由形状pathはSVG画像として収録する。
自由形状はPowerPointでポイント編集できる図形ではない。表・chartはこの簡易CLIでは扱わず、必要に応じて別のネイティブ制作系を使う。
フォントは埋め込まず、閲覧先のフォントで表示する。日本語フォントを用意し、PowerPointで最終表示を確認する。
'''
PACKS=[
 dict(id='yebisu-japanese-slides',title='Japanese Slides',symbol='日',license='CC0-1.0',repository=None,
 description='日本語のSVG・HTMLスライドを作成する共通スキル。図解と自然な改行、講稿、編集可能な出力を整えます。',
 route='用途に合わせて見た目を決め、読みやすい日本語のSVG・HTMLを制作する。初めての資料、少数ページの説明、図解に使う。'),
 dict(id='yebisu-pptx',title='編集できる、日本語PPTX',symbol='P',license='MIT',repository='hugohe3/ppt-master',
 description='資料の目的で制作ルートを選ぶ考え方を継承。日本語の提案・報告を、編集できる文字と図形で整えます。',
 route='新規制作と既存PPTXの編集を区別する。既存テンプレートがある場合はマスター、サイズ、フォント、配置を保つ。新規制作は原稿から論点と関係性を抽出し、ネイティブの文字・図形・線へ。簡易出力には同梱PptxGenJS CLIを使える。既存PPTXの編集・ネイティブchart・表は同梱CLIの対応範囲外なので、利用可能なPPTX制作ツールへ引き継ぐ。'),
 dict(id='yebisu-web-slides',title='軽くて動く、Webスライド',symbol='W',license='MIT',repository='zarazhangrui/frontend-slides',
 description='依存の少ないHTMLと固定ステージを継承。日本語の登壇資料に、短い動きとキー操作を添えます。',
 route='16:9のステージを固定し、ページのスクロールを発表操作に使わない。CSSの短い出現、左右キー、停止できる自動再生、講稿を使えるようにする。スマートフォンとprefers-reduced-motionでも確認する。派手な演出を増やすより、話す順番と視線の誘導を揃える。'),
 dict(id='yebisu-story-slides',title='図解で伝える、日本語教材',symbol='図',license='MIT',repository='JimLiu/baoyu-skills',
 description='原稿→構成→スタイル→ページ制作の分離を継承。日本語の教材へ再設計し、図解と文字を編集可能にします。',
 route='原稿の内容と想定読者から構成を作り、見た目のルールを固定してから各ページを制作する。上流の画像スライド方式から意図的に分派し、文字と図解をSVG要素で作る。上流の画像生成プログラムは含まない。教材では例、仕組み、注意点、演習を必要に応じて分ける。用語を最初に説明し、抽象語だけで説明を済ませない。'),
 dict(id='yebisu-editorial-slides',title='余白で見せる、企画スライド',symbol='E',license='AGPL-3.0-only',repository='op7418/guizang-ppt-skill',
 description='雑誌とスイスデザインの構成を日本語向けに改修。Notoの和文書体、余白、講稿を使って企画を伝えます。',
 route='企画・ブランド・発表会の資料に、エディトリアルまたはスイスデザインを選ぶ。エディトリアルはNoto Serif JPの大きな見出し、暖かな背景、広い余白。スイスはNoto Sans JPのサイズ差、グリッド、ひとつの強調色を使う。上流のWebGLテンプレート、スポンサーUI、プレゼンター同期機能は含まない。制作JSONからSVGと単独HTMLを生成し、発表者ノートを付ける。'),
]

def write(path,content):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
if __name__=='__main__':
    sources=json.loads((ROOT/'data/upstreams.json').read_text(encoding='utf-8'))
    data=[]
    for pack in PACKS:
        folder=ROOT/'skills'/pack['id'];folder.mkdir(parents=True,exist_ok=True)
        upstream=next((s for s in sources if s['repository']==pack['repository']),None)
        origin=f"\n派生元：[{upstream['repository']}]({upstream['url']}) / `{upstream['commit']}`。原作者の公式日本語版ではありません。原文・許諾・変更履歴は [CHANGES.md](CHANGES.md) と [LICENSE](LICENSE) を参照。\n" if upstream else '\nStudio Yebisuによる独自制作。CC0-1.0。\n'
        write(folder/'SKILL.md',f'''---
name: {pack['id']}
description: {pack['description']} 単なる既存文章の校正には使わない。
metadata:
  license: {pack['license']}
  author: Studio Yebisu
---

# {pack['title']}
{origin}
## 制作方針

{pack['route']}

日本語の資料を完成させる。出力形式、読者、目的を既存資料と依頼から判断し、未指定の細かなスタイルは選んで進める。
前提を変える情報が不足するときだけ確認する。デモ数値を実績として書かず、上流の公式成果物を名乗らない。
[日本語文字組み](references/japanese.md)を参照し、原稿の意味を保ちながら見出しと本文を整える。
JSON制作と同梱CLIの対応範囲は [入出力](references/schema.md) にある。実行できる入力例は `assets/example.json`。
原稿、制作JSON、SVG、再生HTML、講稿をまとめる。PPTXが必要な場合は同梱CLIの制限を確認して出力する。
出力を表示し、文字のはみ出し、改行、単位、出典、講稿を確認する。ネイティブ図形と画像を区別して報告する。
上流原文は比較・帰属のための保存資料で、この派生版の実行指示ではない。上流のscriptsや別スキルを探して実行しない。
''')
        write(folder/'references/japanese.md',TYPOGRAPHY)
        write(folder/'references/schema.md',SCHEMA)
        renderer=(ROOT/'assets/slide-renderer.mjs').read_text(encoding='utf-8')
        write(folder/'assets/slide-renderer.mjs',renderer)
        write(folder/'scripts/render-deck.mjs',(ROOT/'tools/render-deck.mjs').read_text(encoding='utf-8'))
        if (ROOT/'tools/export-pptx.mjs').exists():write(folder/'scripts/export-pptx.mjs',(ROOT/'tools/export-pptx.mjs').read_text(encoding='utf-8'))
        write(folder/'package.json',json.dumps(dict(name=pack['id'],private=True,type='module',dependencies={'pptxgenjs':'4.0.1'}),indent=2)+'\n')
        decks=json.loads((ROOT/'data/decks.json').read_text(encoding='utf-8'))
        example=next((d for d in decks if d['skill']==pack['id']),decks[2])
        write(folder/'assets/example.json',json.dumps(example,ensure_ascii=False,indent=2)+'\n')
        if upstream:
            for evidence in upstream['license_evidence']:shutil.copy2(ROOT/evidence['path'],folder/Path(evidence['path']).name)
            if not (folder/'LICENSE').exists():shutil.copy2(ROOT/upstream['license_evidence'][0]['path'],folder/'LICENSE')
            shutil.copy2(ROOT/upstream['entrypoint']['path'],folder/'references/SKILL.upstream.md')
            write(folder/'UPSTREAM.json',json.dumps(upstream,ensure_ascii=False,indent=2)+'\n')
            write(folder/'CHANGES.md',f'''# 日本語派生版の変更

派生元：{upstream['url']}\n固定コミット：`{upstream['commit']}`\nライセンス：{pack['license']}\n改修者：Studio Yebisu\n改修日：2026-10-13

上流の入口文書を土台に、実行フローを独立した日本語版へ再設計しました。上流のリポジトリ全体のミラーではありません。

{pack['route']}

日本語の禁則・改行・数字と単位、Noto / BIZ UD、講稿、架空データの表示を追加。
上流の実装を使うCLIを削り、独自のNode.js SVG/HTML rendererとPptxGenJS exporterを同梱。
保存した上流SKILL.mdとLICENSEは原文のまま。原作者の権利表示と出典を保持します。
独自のCLIソースと参照文書を含む、変更済みパッケージの全ソースを配布します。
AGPL由来パッケージはAGPL-3.0-onlyとして配布し、改変して再配布・ネットワーク提供する場合も同ライセンスの条件に従います。
上流特有の画像生成・WebGL・PPTX修復等は、この小さな派生パッケージには収録していません。
''')
            upstream['status']='forked_with_license_and_source'
        else:
            shutil.copy2(ROOT/'LICENSE',folder/'LICENSE')
            write(folder/'CHANGES.md','# 制作記録\n\nStudio Yebisuによる独自の日本語スライド制作スキル。2026-10-13。\n')
        write(folder/'NOTICE.md',f"# 帰属\n\n{origin}\n独自改修・制作CLI：Studio Yebisu。パッケージの利用条件は {pack['license']}。\nPPTX生成に使用するPptxGenJS（Greg Brent）はMIT、Node.jsは各配布元の条件に従います。依存本体はこのZIPに含みません。\n")
        data.append({k:v for k,v in pack.items() if k not in ['route','repository']}|{'upstream': {'repository':upstream['repository'],'url':upstream['url'],'commit':upstream['commit']} if upstream else None})
    for s in sources:
        if not s['derived_skill']:s['status']='excluded_restricted_derivatives' if s['repository']=='anthropics/skills' else 'license_reviewed_reference_only'
    write(ROOT/'data/refined-skills.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    write(ROOT/'data/upstreams.json',json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
    print(f'Created {len(data)} self-contained skills')
