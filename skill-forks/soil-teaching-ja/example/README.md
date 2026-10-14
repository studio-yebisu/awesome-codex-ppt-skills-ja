# 割合は、全体との比べ方。

原典SOIL Teaching SlidesのMode Cテンプレートを使った、日本語6枚の算数教材です。紙色・深緑・赤橙の大きな図で、部分と全体、割合の計算、値引きの見方を説明します。数値は学習用設定です。

`index.html`を開くと、サーバーやPowerPointなしで使えます。右矢印/Space/「進む」は同じページの図や答えを一段ずつ表示し、すべて表示したら次へ進みます。左矢印は前の段階に戻ります。Home/End、ページhash、全画面、reduce motion、印刷時の全段表示は原典機構です。文字・図・配色はindex.html/styles.cssで編集できます。

原典の`assets/html-deck-template/index.html`からページ構造を作り、元`slides.js`のrender/advance/retreatとfragment状態管理を実使用しました。元styles.cssを保持して日本語用styleを追記。原本はupstream/に保存。共通slide rendererや別frameworkに置き換えていません。再生成はリポジトリの`python tools/build_soil_teaching_showcase.py`、配布物自体にはビルドが不要です。制作計画はinput/PLAN.json、依頼文はPROMPT.mdです。

## 利用条件

原作者: 李俊儀。SOIL Teaching Slides Skill（非公式の日本語改変例）。原典: https://github.com/chunyifish/soil-teaching-slides 。pinはSOURCE.jsonに記録。

HTML template/JavaScript/CSSなどソフトウェアはMIT。SOILの教育方法説明・原典SKILL・referencesおよび日本語派生SKILLはCC BY-NC-SA 4.0です。この部分を商用に再利用する許諾は含まれません。共有・改変時は帰属、変更表示、同じライセンスの継承が必要です。LICENSE/ LICENSE-CONTENT.md / NOTICE.mdを保持してください。原作者の公認・レビュー・推奨を意味しません。

書体はGoogle Fontsの原TTFとOFL原文をfonts/に同梱。Windows fontsからの抽出やremote fontを使いません。教材の日本語本文と数値は本作例で作成しました。

## 確認範囲

生成成功と主要完成画面の初回表示を軽く確認します。6枚のPNGは全段表示の静止プレビューです。全ページ詳細目視、独立レビュー、構造監査、ZIP再実行、授業での理解度、紙印刷は検証していません。技術的な生成成功と授業での採用は別の状態です。
