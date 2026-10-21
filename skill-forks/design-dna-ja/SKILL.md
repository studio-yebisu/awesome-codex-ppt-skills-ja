---
name: design-dna-ja
description: 参考画像から色・文字・構図の規則を抜き出し、別の原稿へ展開する。
---
# 参考画像の規則を別の原稿へ使う

固定原典・commit・利用条件は[SOURCE.json](SOURCE.json)と同梱LICENSE。字体等の別条件を保持する。原典の全契約は[未変更SKILL](example/source/upstream/SKILL.md)を読む。以下は日本語の入口で、原典QAを省略する許可ではない。

## 手順

1. 明示された参考画像を読み、使える色・構図と、転用してはいけない被写体を分ける。
2. Mood/Composition/Visual/Content Strategy/Presentationの5層と数値パネルを示し、確認・調整する。
3. 方向の決定後に題材・読者・枚数・画像利用を確認し、Design ContractとBlueprintを作る。
4. 各頁のPage Specsとlayout_box_budgetを数値化してから、固定1920×1080のHTMLを作る。
5. 原典ppt-layout-guard.jsがPASSした成果物を引き渡す。生成後ブラウザーQAは原典の既定工程ではなく、依頼された場合の追加作業。profileは明示的に希望された時だけ保存する。

## 検証と引き渡し

原典guardは6頁27領域PASS。利用者の追加依頼により、修復後の全6頁を1920×1080で実描画・目視。2頁の机の図、3頁の役割説明、4頁の二つの矢印を修復。

上記は同梱作例の確認結果です。新しい題材では原典に指定された検査を実行します。検査失敗を閾値緩和や未実施の成功表記で解消しない。独立評価と実機発表の確認は別に記録する。

## 作例と制約

[再生成・実施範囲](example/README.md)と[QA](example/source/repair-qa.json)。

- 作例は明示画像からのスタイル抽出。画像なし探索、既存資料の修復、保存profileの再利用・差分、Design Adapterは実証していない。
- 原典は完成rendererを配布しておらず、HTML/SVGとページ送りは規則に基づく局所実装。原典の変換CLIとは称さない。
- 元画像を新資料へ埋め込んでいない。PPTXと保存profileは未生成。

元SKILL・LICENSE・NOTICE・実素材と出所を配布に残す。秘密情報・モデル実行履歴・依存キャッシュを追加しない。

原典の段階確認は、Design Source/Preview/Panel→Active DNA→Requirements→Image Assets→Adapter→Generation Handoffの順を守る。生成後もprofileは自動保存せず、保存の希望を確認する。今回の自律制作という例外を一般の依頼へ持ち込まない。
