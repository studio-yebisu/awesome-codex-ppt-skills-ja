# op7418/guizang-ppt-skill の日本語作例

元リポジトリ: https://github.com/op7418/guizang-ppt-skill

固定コミット: `c91369c449d34755d320a8b81d0734000d99d1ab`

個別ライセンス: **AGPL-3.0**。原文を同梱しています。

## 制作方法

元の assets/template.html をコピーし、Layout 1・3・8・2 の構造を使って日本語を挿入。元のCSS、WebGL、Motion、go()、発表者モードの実装を保持。独自の共通スライドレンダラーは使用していません。

- [SKILL.md](https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/SKILL.md)
- [assets/template.html](https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/assets/template.html)
- [assets/motion.min.js](https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/assets/motion.min.js)
- [references/layouts.md](https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/references/layouts.md)
- [references/themes.md](https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/references/themes.md)
- [references/presenter-mode.md](https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/references/presenter-mode.md)
- [references/checklist.md](https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/references/checklist.md)

## 日本語向けの変更

- 中国語用Notoの指定をNoto JPへ変更。英字のPlayfair Display / Source Serif 4 / IBM Plex Monoを維持。
- 日本語の見出しの改行・字号・フレーム高・データの余白を調整。
- スライドIDと日本語講稿を挿入し、親のプレイヤーとのpostMessage接続を追加。
- 書体をOFL原文とともに同梱。Motionは元のローカルファイルを保持。Lucideを0.468.0のローカル版へ固定し、両ライブラリーの原文を保存。

## 再生成と検証

```text
python tools/build_actual_examples.py
node skill-forks/guizang-ppt-skill-ja/scripts/validate-presenter-mode.mjs examples/actual/guizang-magazine/index.html
```

未実行の機能まで動作確認済みとは扱いません。ブラウザーの確認記録はサイトのQA記録を参照してください。
