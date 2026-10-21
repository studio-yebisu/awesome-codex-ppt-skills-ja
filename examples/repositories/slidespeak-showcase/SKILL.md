---
name: slidespeak-ja
description: SlideSpeak原典engineでbrief由来の日本語styleを作り、実HTMLを生成する。
---

# ブリーフから独自デザインを作る

1. 同梱upstream/SKILL.md、docs/INTEGRATION.md、docs/SKILL-FORMAT.mdを読む。題材と見た目のbriefを決め、既存preset名で代用しない。
2. tokens、chrome、components、layout grammar、image-style、SKILLの6ファイルを作る。原典templates規約とgateに合わせる。見出し・本文・英数字の書体役割を決め、日本語は意味単位で改行し、過密ならページを分ける。
3. 原典loadSkill→generateDeck→wrapAsStandaloneHtmlを使う。LLMClientに完成slide-treeを渡し、原典検証・brand guard・rendererを通す。無料のコード図形だけでも制作できる。
4. build.mtsと独自style/入力を作品ZIPから利用。Node20+と `npm ci` が必要。原典gateを実行し、全頁の本文・図・改行・ページ移動を確認して直す。確認範囲を記録する。
5. 原典MIT、使用フォントの原TTF/OFLを保持。ホスト専有runtimeやAPI keyをZIPへ含めない。

同梱 `example/` のstyle/入力/build.mtsと原典engineを使う。今回のslide-treeは作者が用意してLLMClientへ渡したもの。ライブLLM呼出しの実行例とは区別する。自分の資料ではbriefとstyleを作り直し、原典gate・全ページ確認を行う。
