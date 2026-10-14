# 制作依頼

日本語6枚「香りを、贈る。」を制作する。架空の茶の贈りもの企画として、相手の好みを手がかりに茶葉を選ぶ、包みを整える、短い言葉を添える、選ぶ/包む/渡すという体験を提案する。商品仕様や価格、売上実績、効能は発明しない。

原典cogine-ai/ai-slide-templatesの固定commit `8a7a59d39f059a7e58da9c3471014ba7fe3b98eb`、原典AGENTS.md・INPUT_GUIDE.md、全template.jsonと選んだtemplate.htmlを実際に用いる。metadataから一つを選び、folderをclone、content_limitsとlayout_slots（未定義なら実DOM由来であることを明記）へ対応付け、demoを差し替える。汎用rendererへ置換しない。

版式・palette・装飾・navigationを保持し、同じカード列を反復しない。日本語派生への変更と字体変更は承認済み。Shippori Minchoの見出し、Zen Kaku Gothic Newの本文、Manropeの英数字を公式固定TTF/OFLから役割別に組み、単独HTMLへinline化する。自作SVGは茶葉・包み・結びの説明に必要なものだけ。外部写真/商標は不要。

完成HTML、代表PNG、原稿/入力/依頼、選択とslot mapping、再生成コード、未変更原典と局所差分、PROVENANCE、短い日本語SKILLとSOURCE、公式fonts/OFL、制作とスキルの2ZIPを揃える。主要初回表示、原典navigation1→2、必要生成、短いSKILL quick_validateのみ確認。全頁詳細検査・optional validator・採点・全kit再実行なし。
