# zarazhangrui/frontend-slides の日本語作例

元リポジトリ: https://github.com/zarazhangrui/frontend-slides

固定コミット: `9906a34d640d2111f724544cbc50f7f130569ae1`

個別ライセンス: **MIT**。原文を同梱しています。

## 制作方法

指示型スキルのSKILL.mdを適用。Bold Signalの色・書体・大きな色面・番号・パンくずを使用し、html-template.mdのHTMLとSlidePresentationクラスを土台に制作。viewport-base.cssは全文を挿入。上流に生成CLIはないため「元のCLIを実行した」とは表記しません。

- [SKILL.md](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/SKILL.md)
- [STYLE_PRESETS.md](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/STYLE_PRESETS.md)
- [viewport-base.css](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/viewport-base.css)
- [html-template.md](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/html-template.md)
- [animation-patterns.md](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/animation-patterns.md)

## 日本語向けの変更

- 1920×1080の固定ステージと全体の等比縮小を維持。
- 元プリセットのArchivo Black / Space Groteskを維持し、日本語用Noto Sans JPを追加。
- 日本語の内容、改行、キーボード・タッチ・ホイール、E編集・自動保存・Ctrl+S出力を実装。
- カタログ用のpostMessage接続を追加。書体を埋め込んで外部CDNを不要にした。

## 再生成と検証

```text
python tools/build_actual_examples.py
python tools/verify_actual_examples.py
```

未実行の機能まで動作確認済みとは扱いません。ブラウザーの確認記録はサイトのQA記録を参照してください。
