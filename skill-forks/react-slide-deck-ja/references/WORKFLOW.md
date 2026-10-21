# 問題・問い・概念・例・持ち帰りの順で、図と操作を含む研修用Web資料を組む。

原典の研修の流れとBold Signalを使用。表紙は色付きカードを中心にし、本文は図の段階表示、作例の週別タブで操作して読める。

## 入力と出力

入力：読者の困りごと、学ぶ概念、根拠や事例、持ち帰って行うこと。作例はFAQ整備の架空企画。

出力：固定1280×720で縮尺するReact/Motion資料5頁、週別タブ4状態と段階表示の画像。

## 自分の資料へ使う

1. 読者の困りごとから、問い・概念・具体例・持ち帰りを順に書く。研修の流れをクリック操作だけに置き換えない。
2. presetを一つ選び、表紙にその特徴となる要素を使う。SlideLayout/useSlideScaleで1280×720を縮尺する。
3. 図や文字を原典のMotion variantsで段階表示する。操作が必要な箇所だけ独立stateとdata-interactiveを持たせる。
4. TypeScript/Vite build後に全頁・操作の各状態・通常motion・reduced-motionをブラウザーで確認する。index/assets/fontsを一緒にHTTP配信する。

## 実際に使った機能

- 原典App/SlideLayout/useSlideScale/animation variantsを保持し、TypeScriptとVite buildを実行。
- 問題→問い→概念→例→持ち帰りを5頁へ対応させ、表紙にBold Signalの色付きカードを使う。
- 全5頁とW1〜W4を実操作し、4状態の画像を保存。週別タブは作例固有のReact state拡張で、原典内蔵部品ではない。
- reduced-motionで全頁を確認し、通常Motionでは入場の前・途中・完了を別に保存。

## 未実施と条件

- 原典のInteractive slideを参考にした週別タブは局所拡張。Recharts、他preset、外部API、量的効果測定は未実施。
- 4週間・10問は架空の目標。FAQ改善や問い合わせ削減の実績はない。
- 元Vite8/Tailwind4.2.1のpeer不一致はTailwind4.2.2の固定lockへ局所修正。60fpsの定量計測・全端末の検査は未実施。

現在の再現コマンドはREPRODUCE.md、原典の条件と日本語での一般手順はSKILL.md、現在の実行・画像hashはQA.json。初回PROMPTの限定検査指示は過去の依頼で、後続修復の範囲はこの記録とsourceのRound4ログを使う。
