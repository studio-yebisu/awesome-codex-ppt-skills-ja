# code-on-sunday/slide-deck-generatorの日本語制作

原典: https://github.com/code-on-sunday/slide-deck-generator/tree/a6369f31b0cc4dd5830796455326777a8fe4c7c6

原典React App / SlideLayout / useSlideScale / Framer Motion variants / Vite build

原典en-context-engineeringのReact App、SlideLayout、useSlideScale、Motion variantsで制作する。training-cycleとBold Signalを保持し、CJK字体、reduced-motion、週別タブ、ページ同期を補う。原典依存のVite8/Tailwind4.2.1衝突はTailwind4.2.2への最小補正で解消し、元lockと差分と固定再現lockを保存。HTTPで表示する。

## 作例

- FAQを育てる4週間 / 5枚 / html
- カタログ内の案内: repository.html?repo=code-on-sunday/slide-deck-generator
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=code-on-sunday/slide-deck-generator
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python3.13 / fontTools / Brotli
- Node.js24とnpm
- HTTPの配信環境

## 元の制作コマンド

    python tools/build_reactdeck_repository_example.py --input examples/repositories/react-slide-deck/input/data.json

## 確認範囲

- 架空の計画。改善効果や完成実績ではない。
- PPTXは生成しない。
- HTTP表示が必要。
- 60fpsの定量計測や全端末の確認は未実施。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
