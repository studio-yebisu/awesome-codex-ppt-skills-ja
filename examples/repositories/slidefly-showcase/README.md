# 街を歩く、寄り道を選ぶ。

架空の散歩企画、6枚。道と地点は創作で、実在地点の道案内・営業情報・天気・実績ではありません。暖かな紙・朱橙・深緑、意味単位で改行した和文と道の分岐図で構成。

原典SlideFlyのmorph-engine/nav/frames、free-layoutの指針を実使用。同じ旅人・道・目印actorが6poseで移動・形状変更。カード反復やpreset名の借用ではありません。原典inline-assets.pyで単一HTML化。原典export-pptx.py（標準Pythonのみ）でPPTX生成。

HTMLではnamed actorのMorph状動作。PPTXは文字とactorが編集可能、inline SVGはvector画像。Morph設定は原典exporterで付与しますが、PowerPoint内の実Morph再生確認とは区別します。HTMLの書体はフルTTF内包。PPTXはGoogle importがないので書体未埋込、fonts/の原TTFを手動導入してください（OFL同梱）。

再生成: `python upstream/scripts/inline-assets.py source.html index.html` → `python upstream/scripts/export-pptx.py index.html deck.pptx`。styleはwalk.css、内容はsource.html、原データはinput/data.json。原典runtimeは未変更。原MITはLICENSE、帰属と使用commitはSOURCE/PROVENANCE。

確認は原典deck.auditと主画面・一回の動き。全ページ詳細目視・独立レビュー・native監査・ZIP再実行は行いません。

原典auditは6/6 OK。HTML cover→page2で旅人actorが実移動する一回の動きを確認しました。render/deck.pdfは6poseのPNGから作った静止画PDFで、Motionは含みません。PPTXのMorph実再生は未確認です。
