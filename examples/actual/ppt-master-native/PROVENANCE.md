# hugohe3/ppt-master の日本語作例

元リポジトリ: https://github.com/hugohe3/ppt-master

固定コミット: `ca04346de145ed6462ddf34682848e71df5e20a2`

個別ライセンス: **MIT**。原文を同梱しています。

## 制作方法

日本語版のカタログ作例経路として、上流の閉じたSVG仕様に従ってSVGを制作し、フォークに同梱した元の品質チェッカーとSVG→DrawingML変換器を実行。日本語版の専用経路は --quick-generate を使用します。上流Default GenerateのStrategistや確認UIまで実行したという主張ではありません。文字と図形を持つネイティブPPTXを出力し、画像スライドへ置き換えるフォールバックは使用していません。ブラウザーはPPTXへの入力SVGを表示します。PowerPointアプリ内での視聴検証は未実施。Noto Sans JPを受け手側にも導入する必要があり、上流チェッカーの書体警告を制作記録に保持しています。

- [skills/ppt-master/SKILL.md](https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/SKILL.md)
- [skills/ppt-master/references/shared-standards-core.md](https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/references/shared-standards-core.md)
- [skills/ppt-master/references/executor-base.md](https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/references/executor-base.md)
- [skills/ppt-master/references/semantic-svg.md](https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/references/semantic-svg.md)
- [skills/ppt-master/workflows/profiles/quick-generate.md](https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/workflows/profiles/quick-generate.md)
- [skills/ppt-master/scripts/svg_quality_checker.py](https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/scripts/svg_quality_checker.py)
- [skills/ppt-master/scripts/svg_to_pptx.py](https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/scripts/svg_to_pptx.py)

## 日本語向けの変更

- 日本語版フォークのカタログ作例用経路を追加。上流の変換器・チェッカー本体は無改変。
- 日本語内容、Noto Sans JP、1280×720の意味グループ付きSVG、各ページの日本語講稿を制作。
- PowerPointの校正言語をja-JPに指定し、元のネイティブfadeトランジションを使用。

## 再生成と検証

```text
python tools/build_actual_examples.py
python <PPT_MASTER>/scripts/svg_quality_checker.py <EXAMPLE> --quick-generate --canonical-authoring --stage final --json
python <PPT_MASTER>/scripts/svg_to_pptx.py <EXAMPLE> --quick-generate --primary-language ja-JP --with-notes -t fade -o ppt-master-ja.pptx
```

未実行の機能まで動作確認済みとは扱いません。ブラウザーの確認記録はサイトのQA記録を参照してください。
