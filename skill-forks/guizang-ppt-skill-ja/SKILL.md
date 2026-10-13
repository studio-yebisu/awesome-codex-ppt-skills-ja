---
name: guizang-ppt-skill-ja
description: 雑誌風・Swiss風の日本語HTMLスライドを、Guizangの実際のテンプレートで制作する。Guizangの作例や日本語版を指定されたときに使う。
metadata:
  license: AGPL-3.0
  upstream: https://github.com/op7418/guizang-ppt-skill
  upstream_commit: c91369c449d34755d320a8b81d0734000d99d1ab
---

# Guizang 日本語版

日本語の企画・導入提案は [references/japanese-business-workflow.md](references/japanese-business-workflow.md) を読む。MagazineとSwissの選定、入力、組版、講稿、実テンプレートの検証を扱う。

元の [SKILL.upstream.md](SKILL.upstream.md) を読む。選んだStyle A/Bに必要な参照だけを読み、**assets/template.html または assets/template-swiss.html を実際にコピーして内容を挿入する**。別の共通レンダラーへ置き換えない。Swissは元のS01–S22の登録版式を保持する。

日本語の内容を作り、langをjaにする。中国語用のNoto SC指定はNoto Sans JP / Noto Serif JPへ変更する。英字の指定フォント、テーマ色、レイアウト、WebGL、Motion、ページ制御は保持する。文の意味で改行し、長い日本語の見出しは字号とフレームを調整する。ローカルの日本語フォントはreferences/japanese-fonts.mdを参照する。

上流の「見出しだけ変えた別スタイル」を作らない。元のテンプレートとの差分と出力をSOURCE.jsonに基づいて記録する。スライドIDと講稿を一対一に対応させ、scripts/validate-presenter-mode.mjsを実行する。Swissではscripts/validate-swiss-deck.mjsも実行する。ブラウザーで実表示・翻ページ・字形を確認する。

このフォークとテンプレート派生物のコードはAGPL-3.0。LICENSEを保持し、改変ソースと対応する配布元を用意する。MotionはMIT、LucideはISC、書体はOFLの原文を個別に保持する。カタログのCC0をこのスキルへ適用しない。
