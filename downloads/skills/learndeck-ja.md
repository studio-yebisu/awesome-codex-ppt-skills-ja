---
name: learndeck-ja
description: LearnDeck原典のHTML-to-PPT DOM実測converterで、日本語HTMLからnative文字と図形・個別SVG画像を持つPPTXを作る。
---

## このスキルでできること

HTMLの文字と単純図形をPowerPointで直せる部品へ変え、SVGは個別画像として残す。

- 困っている状況: HTMLを全面スクリーンショットにすると、文字と基本図形を別々に直せない。
- 必要な入力: 変換するHTML、使用するSVG・画像と実際のフォントファイル。
- 受け取るもの: 文字・背景・基本図形を個別に編集できるPPTXと、元HTMLとの比較。複雑な図は個別の画像として残る場合がある。
- 必要環境: Node18+・playwright/pptxgenjs/sharp/jszip / Chromium/Chrome/Edgeと同梱の実TTF/OFL / PPTXの実描画用PowerPoint等
- 作例で試した範囲: 花の提供案5頁を同じHTMLから元DOM変換で再生成。HTML5頁とPowerPoint5頁を目視し、全DOM文字を照合。字間、見出し下余白、SVGの縦伸びを修正した。
- 制約: 本例はHTML-to-PPT経路。学習原稿から5styleで生成する別経路は未実施。 / 局所変更は字体役割・日本語metadataと、SVGの実表示幅高さの保存。元との差分を同梱。 / 花はSVG由来の個別PNG。花びらや茎がnative図形になったとは称さない。 / 元SKILLに専用の必須QA CLIはない。今回の明示修正依頼で全頁の実描画確認を行った。


# LearnDeck 日本語版（非公式）

1. 題材、枚数、確定事項と提供案を短く整理。style指定があれば再質問せず従う。各ページに一つの主張を置き、巨大見出しと役割のある図をHTML .slideで作る。
2. 同梱upstream/SKILL.mdを必要範囲で読む。新規計画は原典generate_ppt.jsも使える。本作例は柔軟な日本語bold構図のためHTML-to-PPT modeを使う。
3. local runtime/scripts/html_to_ppt.jsで変換する。ChromiumのDOM位置が正本。playwright/pptxgenjs/sharp/jszipを用意し、Codexではload_workspace_dependenciesのNode/NODE_PATHを使う。
4. 原典は既定で追加検査を省略するが、明示された修正・検証依頼では元HTMLを直して同じconverterを再実行する。HTMLとPowerPointを全頁描画して字間・改行・余白を目視し、native要素とSVG由来PNGの分離を記録する。
5. Native text/background/rect/ellipseと、SVG由来の個別PNG imageを区別して伝える。SVG元と実TTF/OFL、原MIT、source.htmlを保全。PPTXフォント未埋込時は別端末への導入が必要と説明する。

本forkのruntimeだけ、原典converterの単一font-face固定をcomputed fontFamilyで置換し、roleごとの日本語書体を保存。languageはja-JP。未変更原本はupstream/scripts。SVG書き出し時は実DOMのviewport幅・高さを保存し、SVGのpreserveAspectRatioをPNGへ反映する局所補正も適用。その他のDOM/native object/gradient pipelineは原典のまま。

具体例と入力はexample/に同梱。`node runtime/scripts/html_to_ppt.js --input example/source.html --out-dir output --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720`。画像をnative shapeと称さず、提供案を実績と称さない。

原作者LearnAIHubC。https://github.com/LearnAIHubC/LearnDeck 。MIT帰属はLICENSE.txt、使用pinはSOURCE.json。書体は各OFL。公式・原作者の公認ではありません。

元Generate PPT（slides.jsonから5styleへ生成）はこの作例では未実施。radial背景・影は近似、CSS filterは無視されます。元HTMLとPPTXの完全一致は保証せず、花の内部はnative図形ではありません。修正時はsource.htmlが正本で、元DOM変換→全頁の実描画→要素照合の順で確認し、source/*.diffとQAへ結果を残します。

小さいラベル・脚注・頁番号は背景と4.5:1以上のコントラストを確保する。今回の3頁はクリーム色の文字と少し暗くした朱赤で4.561:1。原典DOM変換後のHTMLとPowerPointの両方を実描画して確認する。

## 単体の本文から使う

この本文は `skill-forks/learndeck-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/LearnAIHubC/LearnDeck/tree/d5ea12ca88f9a87edaf20b6bb48847790baed698

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `learndeck-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: LearnAIHubC / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/LearnAIHubC/LearnDeck/blob/d5ea12ca88f9a87edaf20b6bb48847790baed698/LICENSE.txt
