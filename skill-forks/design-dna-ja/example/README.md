# 参考画像の規則を別の原稿へ使う

参考画像から配色・書体・構図の規則を抜き出し、別の原稿へ使います。画像をそのまま貼り付けず、新しい図や文へ見た目の規則を展開する作例です。

入力: スタイル参考の画像と、別の内容の原稿。参考画像は完成資料の素材にしない。

出力: 抽出した5層の規則、配色値、頁ごとの配置仕様から作ったHTML6枚。

## この作例で確かめること

- 明示した画像から5層の規則と数値パネルを抽出
- 数値Page Specsから別題材のHTML/SVGを生成
- 未変更の原典layout guardで6頁27領域を検査

原典guardは6頁27領域PASS。利用者の追加依頼により、修復後の全6頁を1920×1080で実描画・目視。2頁の机の図、3頁の役割説明、4頁の二つの矢印を修復。

## 使い方

1. 明示された参考画像を読み、使える色・構図と、転用してはいけない被写体を分ける。
2. Mood/Composition/Visual/Content Strategy/Presentationの5層と数値パネルを示し、確認・調整する。
3. 方向の決定後に題材・読者・枚数・画像利用を確認し、Design ContractとBlueprintを作る。
4. 各頁のPage Specsとlayout_box_budgetを数値化してから、固定1920×1080のHTMLを作る。
5. 原典ppt-layout-guard.jsがPASSした成果物を引き渡す。生成後ブラウザーQAは原典の既定工程ではなく、依頼された場合の追加作業。profileは明示的に希望された時だけ保存する。

## 実施範囲

- 作例は明示画像からのスタイル抽出。画像なし探索、既存資料の修復、保存profileの再利用・差分、Design Adapterは実証していない。
- 原典は完成rendererを配布しておらず、HTML/SVGとページ送りは規則に基づく局所実装。原典の変換CLIとは称さない。
- 元画像を新資料へ埋め込んでいない。PPTXと保存profileは未生成。

今回の修復はCodex。独立再評価は変更後の版に対して別に取得します。[実行・全頁確認](source/repair-qa.json)、[原典検査](source/round4-original-gates.json)に実記録を保存しています。固定原典・利用条件はPROVENANCE.jsonとsource/upstream、元のLICENSE/NOTICE、字体のOFLを保持します。

[展開ZIPからの再生成検査](source/round4-zip-replay.json)も実行済み。既存の互換実行環境を使い、公開HTMLと同一バイトの出力を確認しました。Beatdeckの依存は既存lock済みnode_modulesを再利用し、新規npm ciの実証とはしていません。
