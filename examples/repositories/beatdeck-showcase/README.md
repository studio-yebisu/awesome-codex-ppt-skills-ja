# クリックに合わせて図を進める

クリックごとに話す内容と図を進める資料を作ります。同じ場面でもボウルから生地へ図が変わり、戻った時やURLから直接開いた時も同じ状態になります。

入力: 原稿・話者のメモ・出典と、何を一回のクリックで見せるかの対応表。

出力: 6場面15段階のReact資料。共通の工程図、発表者用のsource/note、自動beatを持つ。

## この作例で確かめること

- 原稿・CONTENT-AUDITと各beatのref/source/note対応
- 同一scene内で混ぜる→形→焼く場所へ図も変化
- 元verifyの全15状態を前進・逆戻り・直接表示で比較

原典buildと未変更verifyを実行。15状態すべての前進・逆戻り・直接表示が既定0.1%で一致、layout/error/remote/warningは0。全15枚を個別に開いて目視。

## 使い方

1. 原稿をreferenceへ保持し、何を舞台に置き何を講稿へ回すかCONTENT-AUDITで照合する。
2. sceneとbeatを定義し、各段階のref/source/noteと自動進行の要否を記録する。
3. 元Scene/Reveal等で段階を組み、戻りや直接URLでも同じ表示になるよう状態から描く。
4. 原典buildで型検査・bundle・外部URL検査を通し、原典verify --sourceで全beatを前進・逆戻り・直接表示で比較する。
5. contact sheetと重要フレームを開いて確認し、RUNBOOKと実施していない実機稽古を引き渡す。

## 実施範囲

- 原典verifyは15段階、既定0.1%の閾値で一致。QR URL未指定でQRなし、Terminal/data-exact照合は0要素。
- 3.1〜3.3は同じ工程内で、ボウル→生地→天板と矢印へ図も変わる。材料量・温度・時間・実際の製パン方法は表現していない。
- 全キーの手動稽古、実機Wi-Fi切断、別端末・プロジェクターでの通し確認は未実施。

今回の修復はCodex。独立再評価は変更後の版に対して別に取得します。[実行・全頁確認](source/repair-qa.json)、[原典検査](source/round4-original-gates.json)に実記録を保存しています。固定原典・利用条件はPROVENANCE.jsonとsource/upstream、元のLICENSE/NOTICE、字体のOFLを保持します。

[展開ZIPからの再生成検査](source/round4-zip-replay.json)も実行済み。既存の互換実行環境を使い、公開HTMLと同一バイトの出力を確認しました。Beatdeckの依存は既存lock済みnode_modulesを再利用し、新規npm ciの実証とはしていません。
