# Magic Slide：朝の支度を10分短くする企画

原典Magic SlideのHTMLとFLIPを実行した、日本語5枚の架空の実験案です。40分→30分、服4分・鍵3分・バッグ3分は仮定で、実績ではありません。前夜の準備時間も含めて効果を確かめる構成です。

`sources/outline.md` と `brief.md` → 各slide-XX.html/style.css → 原典merge-slides.py → 認証scopeを1行修正した派生inject-runtime.py → 原典と同一のserve.pyで制作。10分、服・鍵・バッグ、30分・5日間を隣接ページに引き継ぎます。講稿はdata-speaker-notesに保持。原典のcursor・stagger・Magic Move・dock・Overview・編集UIを保持しています。

## 表示と編集

静的サイトのiframeはプレゼン用です。矢印、dock、一覧などの表示操作を使います。編集・Save・画像差し替えは原典preview serverが必要です。静的サイトでは保存できません。日本語本文に対し、原典UIのja未登録文字列は原典のEnglish fallbackになります。

このフォルダで `python source/ja-runtime/scripts/serve.py index.html --no-open` を実行し、表示された /deck/ のURLを開いてください。Python標準ライブラリのみ。生成時にはNodeの構文検査を利用しています。画像生成APIや認証情報は不要です。

## 再生成

リポジトリから: `python tools/build_magic_slide_repository_example.py --output-dir morning-regenerated --input examples/repositories/magic-slide/input/data.json`。

このフォルダ単体から: `python source/build_magic_slide_repository_example.py --upstream source/upstream --input input/data.json --font-dir assets/fonts --output-dir ../morning-regenerated`。

既存HTMLを編集した場合は `--source-dir sources` を指定すると、そのモジュールを原典で再merge/injectします。生成先は別フォルダを推奨。再生成は常にawaiting_visual_reviewとなり、今回の合格を引き継ぎません。raw原典はsource/upstreamへ無改変保持。派生runtimeはsource/ja-runtimeへ分離します。

## 原典不具合と局所修正

原典のQAノート読出しが別IIFE内のmsAuthFetchを参照し、ReferenceErrorになりました。source/upstream-failureに実行時の記録を保存。派生injectorは既存の認証付きclosureをwindowへ公開する1行だけを追加します。トークン取得・header付与・server認証・保存パス制限は原典のままです。source/ja-runtime/changes.diffとchanges.jsonが正確な差分です。保存後の再注入にも同じ修正が使われるよう、編集はja-runtime側のserve.pyから起動してください。

## QAと採用状態

原典serve.pyのQA Overview captureを先に視認。その後、依頼されたカタログ実例の検査として全頁とnative motion/navigationを検証しました。記録はQA.jsonとsource/browser-review.json。Agent QAと人によるRevision/正式採用は別です。原典が求める人のレビューはpendingです。

原典MITとNoto Sans JP OFLを同梱。外部写真なし。固定コミット、原典hash、入力/成果物hash、実行ログはPROVENANCE.jsonとsource/に保存しています。
