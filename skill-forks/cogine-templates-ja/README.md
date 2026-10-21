# 原稿に合うテンプレートを選ぶ

用途と原稿量をテンプレートのメタデータと比べ、合う枠へ内容を配置します。選定した理由と、字体・余白の変更箇所も確認できます。

入力: 読み手・用途・本文の量。各テンプレートのscheme/density/avoid_for/content_limits。

出力: 選んだeditorial-luxuryの配色・枠・ページ操作を保った日本語HTML6枚。

## この作例で確かめること

- 実60件のtemplate.jsonを読取・3候補の用途と密度を比較
- 原典editorial-luxuryの全フォルダー複製・見本文字を置換
- 明示した日本語字体・文字寸法・縦余白の派生と原典visual validator

3候補比較の実画面を追加。2頁の手順、3頁の見出し間隔、5頁の三つの選択肢を調整し全6頁を実描画・目視。未変更の原典visual validatorは現HTMLで1280×720 PASS。

## 使い方

1. 原典AGENTSを読み、全templates/*/template.jsonのscheme・density・用途・避ける場面を比較する。
2. content_limitsと必要版式を確認し、合うテンプレートのフォルダー全体を複製する。
3. 実HTMLの埋める場所を対応付ける。今回の原典JSONにはlayout_slotsがないため局所のDOM対応表を使う。
4. 見本の文字・数字・画像をすべて置換し、本文やカードの上限を越える場合は頁を分ける。
5. 全頁をブラウザーで確認し、カウンターと章番号を区別する。利用可能な原典validate-visualも実行する。

## 実施範囲

- 原典は字体・主要レイアウトの保持を求める。今回は日本語化と可読性の保守依頼により、字体・文字寸法・縦余白を意図的に変更した。原典どおりの字体保持は今回の実証範囲に含めない。
- layout_slotsは原典JSONに未定義。局所DOM対応表を原典の機能と称さない。
- 原典validator自体は未変更。今回の日本語資料を検査し、60テンプレート全体の検査や保守はしていない。

今回の修復はCodex。独立再評価は変更後の版に対して別に取得します。[実行・全頁確認](source/repair-qa.json)、[原典検査](source/round4-original-gates.json)に実記録を保存しています。固定原典・利用条件はPROVENANCE.jsonとsource/upstream、元のLICENSE/NOTICE、字体のOFLを保持します。

[展開ZIPからの再生成検査](source/round4-zip-replay.json)も実行済み。既存の互換実行環境を使い、公開HTMLと同一バイトの出力を確認しました。Beatdeckの依存は既存lock済みnode_modulesを再利用し、新規npm ciの実証とはしていません。
