# 小さな展示を、ひとつの体験に。 動く展示案内

既存の自作PPTX5枚を動くHTMLへ変換。元資料はAkxan/ppt-agent-skillのHTML→native PPTXで作った、MITの仮想展示企画です。新しいPPTXを生成した作例ではありません。日時・会場・参加条件は未定、準備日程は相対的な仮案です。

原典aws-html-slidesのPPT conversion経路で、extract-pptx.pyを実行して全テキスト・画像・speaker notesを抽出。原典extractorはnative円/四角/三角を含めないので補助native-shapes.jsonで実OOXMLの位置・色・path/fontを保全し、同じ構成をSVG text/ellipse/rect/path/lineへ変換しました。抽出済み文字とnotesから原稿/HTML commentsを作り、元の形にbreath/slide/path drawを加えています。同じ文章を別の画面へ貼り直しただけではありません。

原典Neon previewの実controller（IntersectionObserver、keyboard、wheel、touch、nav dots、progress）とFXコード、viewport-base.css全文、reveal stagger、native SVG diagramのedge choreographyを使用。各ページは100vh/100dvh、SVGのfixed viewBoxを画面へ縮尺。元三原色のBauhaus図を暗いNeon frameへ入れた派生です。AWSのlogo/公式性/提携を主張しないStudio Yebisu表示へfooterを置換しています。未変更原本とMITを保持。

index.htmlはfontを含めた単一HTMLで、ネット接続なしに開けます。矢印/Space/PageUp/PageDown、wheel、swipe、nav dotsでページ送り、Escで一覧。Reduce motionにも対応。文字・vector geometry・motionをsource/のSVG/CSSとindex.htmlで編集できます。PPTX編集の例ではなく、入力PPTXはinput/deck.pptxに原本保全。

再変換: Python3.10+とpython-pptxを用意し `python rebuild.py`。原典extract→実OOXML補助抽出→元controller/templateでindex.htmlを再生成。別のPPTXへはinput/deck.pptxを入れ、題名/枚数情報もrebuild.pyと依頼文へ合わせてください。原典gen-content.pyは新規制作のみなので、本変換でStep4/5は実行しません。入力出所とhashはSOURCE/PROVENANCE、原稿はMANUSCRIPT.md、依頼文はPROMPT.md、controller局所差分はsource/controller.diff。

元MIT著作権©2025 Zara Zhang（lanceli93/aws-html-slides固定版）をLICENSEへ保持。Akxan原典のMIT/commit/provenanceもinput/に添付。書体はGoogle Fonts固定pinの未改変TTFと各OFLをfonts/へ添付、Windows fontsから抽出していません。原典のCDNはこの派生の再生に不要です。

確認は原典extractの成功、主要完成物とページ送りの初回表示まで。全ページ目視・構造監査・独立review・ZIP再実行は行いません。変換でSVG textのbaseline/line metricsはPowerPointと完全一致を保証しません。
