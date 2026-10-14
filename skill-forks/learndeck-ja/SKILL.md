---
name: learndeck-ja
description: LearnDeck原典のHTML-to-PPT DOM実測converterで、日本語HTMLからnative文字と図形・個別SVG画像を持つPPTXを作る。
---

# LearnDeck 日本語版（非公式）

1. 題材、枚数、確定事項と提供案を短く整理。style指定があれば再質問せず従う。各ページに一つの主張を置き、巨大見出しと役割のある図をHTML .slideで作る。
2. 同梱upstream/SKILL.mdを必要範囲で読む。新規計画は原典generate_ppt.jsも使える。本作例は柔軟な日本語bold構図のためHTML-to-PPT modeを使う。
3. local runtime/scripts/html_to_ppt.jsで変換する。ChromiumのDOM位置が正本。playwright/pptxgenjs/sharp/jszipを用意し、Codexではload_workspace_dependenciesのNode/NODE_PATHを使う。
4. 原典の既定に従い--no-previewで余分な検査を省略。必要な完成物の初回表示だけを実施し、依頼されていない詳細監査を追加しない。
5. Native text/background/rect/ellipseと、SVG由来の個別PNG imageを区別して伝える。SVG元と実TTF/OFL、原MIT、source.htmlを保全。PPTXフォント未埋込時は別端末への導入が必要と説明する。

本forkのruntimeだけ、原典converterの単一font-face固定をcomputed fontFamilyで置換し、roleごとの日本語書体を保存。languageはja-JP。未変更原本はupstream/scripts。その他のDOM/native object/SVG-to-PNG pipelineは原典のまま。

具体例と入力はexample/に同梱。`node runtime/scripts/html_to_ppt.js --input example/source.html --out-dir output --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720`。画像をnative shapeと称さず、提供案を実績と称さない。

原作者LearnAIHubC。https://github.com/LearnAIHubC/LearnDeck 。MIT帰属はLICENSE.txt、使用pinはSOURCE.json。書体は各OFL。公式・原作者の公認ではありません。
