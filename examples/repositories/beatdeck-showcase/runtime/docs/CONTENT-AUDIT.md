# Content audit — パンが、店先に届くまで。

Source: `reference/SCRIPT.md`（今回の架空企画原稿）。Design reference: `input/BRAND.json`と原典neutral/light。sourceが内容、ブランド指定が見た目を決める。

## Facts（創作しない）

| 項目 | 値 | 出所 |
| --- | --- | --- |
| 題名 | パンが、店先に届くまで。 | 依頼 |
| 状態 | 架空パン店の概念資料 | 依頼 |
| ブランド | 温かい紙・墨・朱 | 依頼 |
| 原料/時間/温度/安全/売上/科学値 | 未提示。数値・仕様を作らない | 依頼 |
| QR target | 未指定。QRなしで閉じる | 依頼 |

## 原稿→段階対応

| 原稿 | 保持する内容 | 段階 | 状態 | 図解 |
| --- | --- | --- | --- | --- |
| 01 | 待機・題名・架空企画 | 1.1–1.2 | kept | 待機とパンの図形 |
| 02 | 素材から始め、次へ | 2.1–2.2 | kept | 共通worldの素材nodeと矢印 |
| 03 | 混ぜる・形づくる・焼く場所へ | 3.1–3.3 | kept | 生地のSVGとNodeBox/Arrow |
| 04 | 焼く・店先へ | 4.1–4.2 | kept | Timelineで図形の色を変える。工程時間ではない |
| 05 | 届く・並べる・選ぶ時間 | 5.1–5.3 | kept | 棚のSVG。図形のパン個数はデータではない |
| 06 | 選ぶ・手渡す・終える | 6.1–6.3 | kept | Typewriterと共通worldの最後のnode |

## 素材と条件

自作説明用SVGのみを使う。公式Dela/BIZ/Manropeの実TTF/OFLをlocalへ収録する。Kernel Panicの第三者素材は私有talkコピーにも配布にも入れない。原典engineは未変更。

## 代理で決めたこと

- 6場面・15段階。原典の待機段階を含む。
- Scene/Revealで内容を切り替え、NodeBox+Arrowの単一worldを残す。焼く場面のTimelineと手渡す場面のTypewriterは説明用motionで、実証値ではない。
- 未提示のQR URLを作らず、最終段階は短い言葉だけ。
- 日本語字体は役割ごとにlocalへ入れ、原典lightのtokensへブランドを重ねる。
原典 `npm run verify -- --source=reference/SCRIPT.md` を実施する。全15段階の前進・後退・URL直接表示を比較し、contact sheetを確認する。実施済みの結果はQA.jsonとrender/verify/report.jsonに記録し、全キーの手動稽古・物理Wi-Fi断・別端末での通し確認は別の未実施項目として残す。
