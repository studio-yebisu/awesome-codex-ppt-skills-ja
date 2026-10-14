# 土曜日を、街の作業場に。

架空の一日ワークショップを伝える、独立1ページのnative企画書です。複数ページを1枚扱いにしていません。日時・人数・会場・参加条件は未定。10:00/12:00/15:00は仮のプログラムで、開催予定の確定や実績を示しません。

## 原典方式

mpuig/agent-slidesの元CLIとplan+ops形式を使用。空の16:9コンテナだけをローカルで作り、元extractでtemplate/layout契約を抽出。preflight、dry-run、renderを実行しました。表示要素は全て元のnative add_text/add_rectangle/add_oval/add_line_shape操作です。左の行程は順序、右の人・道具・街は場との関係を表し、循環を捏造しません。

原典のWWWH、結論先行、split-panel、階層、badge/timelineパターンを反映。1枚指定と巨大和文の美術指示を優先して、元skillの自動構造ページ追加・24pt標準サイズ・反復カードを採用しない明示派生です。PPTXを別rendererで偽装していません。

## 再制作

Python3.12+を用意。認証/API/key/専有writer/global skill installは不要です。

```powershell
python -m pip install ./runtime
python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact
python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --dry-run --compact
python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --output deck-rebuilt.pptx --compact
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck-rebuilt.pptx -OutputDirectory render-rebuilt
```

input/slides.jsonが実際の入力、input/project/design-profile.jsonが配色・書体・契約の入口です。抽出から再実行する場合はPROVENANCEのextract commandを使用。source/build_agent_slides_showcase.pyは元カタログ内の制作用記録で、ZIPの利用者は上記の元CLIを直接使用します。

## 書体と条件

fonts/のZen Kaku Gothic New（和文）とManrope（英数字）をTTFから導入し、PowerPointを開き直してください。受け手にも導入します。公式Google Fontsの未改変TTFとOFLを同梱。WindowsFonts抽出なし、PPTX内のフォント埋め込みなし。

原典MITのLICENSE、Python依存の原文条件を保持。原作者の公式日本語版ではありません。node_modules、cache、秘密情報は配布しません。

## 確認範囲

元extract/preflight/dry-run/render、PowerPoint必要な1回書き出し、主出力初回確認のみ。全テスト、全ページ詳細目視、native監査、独立レビュー、全ZIP再実行は未実施。QA.jsonに状態を記録。
