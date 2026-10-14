# 待つ時間にも、道しるべを。

原典Presentation Forgeのnew_deck→日本語の1頁1HTML→未変更build.pyで生成した6枚。obsidian/ balanced、1920×1080、ひとつの読込画面の設計提案。

完成index.htmlは実字体、CSS/JS、原文条件を内包しオフラインで開く。矢印/Spaceで進み、原典pは発表者画面、?は操作案内。発表者・編集保存・全画面・印刷は元code保持、別検査はしていない。

## 自分の原稿で

input/MANUSCRIPT.mdとdeck-plan.jsonの主張・読み手を置換し、source/deck/slides/*.htmlを1頁ずつ編集。source/deck/themes/obsidianに書体・配色をまとめる。engineはそのまま。Python3の標準ライブラリだけで `python source/rebuild.py`。元buildはブラウザーで保存した変更を先にpullするため、再制作時に既存index.htmlの編集を消さない。

確認範囲はQA.json。元check_deckの全頁検査はユーザーの最小確認方針で省略。unused原典字体のbinaryは配布せず、rawソースの参照を固定原典へ残す。使用字体は公式未改変TTF/OFLで置換。短い日本語SKILLだけでは必要な実装を含まないため、一式ZIPか固定原典を利用。

## 条件

原典rootとtemplateはMIT ©2026 Thomas Gourmelen。元iconsはLucide ISC・該当Feather MITを同梱。使用字体は個別OFL-1.1。原文条件はsource/upstream、source/deck/engine/icons-LICENSEと各字体folder。PPTX/PDF生成、第三者API、外部写真・ロゴは使用していない。
