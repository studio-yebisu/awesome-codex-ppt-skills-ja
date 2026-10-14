# deck-factory 日本語適応版

HTML/CSSで1920×1080のスライド誌面を手で構成する方法論。PPTX生成器ではありません。

1. input/BRIEF.mdとdata.jsonを読み、頁ごとの主題を決める。
2. assets/styles.cssの原典トークン・クラスを実際に使う。変更はadaptation.cssへ分離する。
3. cover / chapter / statement / bullets / two-col / cards-3 / data-split / image-full / image-split / flow / chart-bar / kpi-3 / closing の13スロットから選ぶ。
4. 近黒#08090Aまたは紙#F7F4EC。左右140px、上下96pxを基準に安全余白を確保する。四隅のブランド・メタ・著者・頁を全頁に置く。
5. eyebrow、句点で終わるアクションタイトル、主オブジェクトひとつ、hairlineとtailを組む。塗りつぶしカードを避け、accentはeyebrowだけにまとめる。
6. 大きな数字はラベル、172pxの値、文脈で構成。日本語はkeep-all / strict。本文を増やすより短くする。
7. 完成HTMLをChromiumで開き、初回表示と頁送りを確認。source/render.pyでPNG・原本PDFを作り、既存Ghostscriptの直接コマンドでlite PDFを作る。未知のcompact-pdf.shは実行しない。
8. PNG全頁とPDFを目視し、明らかな欠けを直す。未実施の確認を合格扱いにしない。

この作例は7頁の架空文化イベント企画。音源・実測波形・個人の位置情報なし。地図は編集可能な説明SVG、波形的図形は抽象記号。音の再生機能はありません。

原典: https://github.com/kimsh-1/deck-factory/tree/11d456351763b0efbc2a4989da688334f709dd9b/skills/deck-factory
原典ライセンス: MIT / Copyright (c) 2026 kimsh-1
