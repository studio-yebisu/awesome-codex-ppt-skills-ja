---
name: slidepoise-ja
description: SlidePoiseの生成画像→OpenCV→contract→constructor→固有rendererを保ち、日本語のnative編集可能PPTXを作る。
---

# SlidePoise 日本語版（非公式）

1. 題材・主張・関係・出所・仮定をintentへ書く。数字が目標なら目標と明記。Native diagramが説明する関係を決め、反復card gridへ押し込まない。
2. 同梱upstream/slidepoise/SKILL.mdと必要referencesを読む。画像工程を省かない。元prepare_generation.pyでconfig/intent/resourcesからrequestをcompileし、exact promptとreferenceをbuiltin画像toolへ渡す。能力がなければ依存工程だけ止めて具体条件を知らせる。
3. 得た画像を見て採用し、元normalizerでcanvasを整える。Agentがsemantic-mapに文字・論理的allocation・図形・connector owner・target字体を記す。座標を汎用builderへ写す代替は禁止。
4. 元reconstruct-slideでOpenCV計測→contract→constructorをcompile。overlayでownershipを読む。元render-deckで順序通りnative PPTX化し、画像を全頁背景へ貼って編集可能と称さない。
5. 必要な原典buildと代表完成物の初回表示を確認。本作例はユーザーの軽い確認指定で全詳細目視/独立review/構造監査/ZIP再実行を省略。明白な句点欠けをsemantic targetへ戻して修正した。

日本語の見出し/本文/英数字を別familyへ。実TTF/OFLだけ添付する。local Windows fitterは同梱OSS familyを明示解決する差分のみ。PowerPoint COMはApplication.Quitを使わず自分のdeckをClose。

example/rebuild.pyが保全画像からの原典再構成入口、example/PROMPT.mdは別題材への依頼文。例では3枚の生成画像・semantic map・OpenCV計測・contract・constructor・PPTXが揃う。Original global Console/profile install、外部library retrieval、SAMは未実行。

原典 https://github.com/henryhyw/slidepoise 、MIT原文とpinはLICENSE/SOURCE.json。非公式改変。Fontは各OFL、PPTXフォント未埋込時は他端末へ導入する。任意reviewを省いたことと原典build成功を区別する。
