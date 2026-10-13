# gongnyang/awesome-html-scrolline-deckの日本語制作

原典: https://github.com/gongnyang/awesome-html-scrolline-deck/tree/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc

原典deck CLI・Scrolline engine・rail-advance・era-shift・Vite build・smoke

原典deck.yaml・plan・Vite build・Scrolline engineとrail-advance/era-shiftで6停止点を連続的につなぐ。engine/moves/conceptsは原典と一致。内部localeはen、HTMLの表示は日本語。Windows Chrome探索だけを明示adapterで補正する。原典全体CIのWindowsパス3件不合格を保持し、HTTP上のcore・smoke・操作確認と分ける。GSAP独自条件と各MITの原文通知を分けて保持。

## 作例

- 小さな展示を、ひらくまで / 6枚 / html
- カタログ内の案内: repository.html?repo=gongnyang/awesome-html-scrolline-deck
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=gongnyang/awesome-html-scrolline-deck
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Node.js 22+ / npm
- Python 3（再実行CLI）
- ChromeまたはEdge / ffmpeg（smoke描画）
- 日本語フォント（WindowsではYu Mincho / Yu Gothic）

## 元の制作コマンド

    python source/reproduce.py --input input/data.json --render

## 確認範囲

- 原典全体CIはWindowsのパス検査3件で不合格。原典の全ゲート完了ではない。
- 日本語フォントの見た目は閲覧端末に依存。フォントファイルは同梱しない。
- 現在の確認範囲はlocalhost HTTP表示。IABのfile://表示確認ではない。
- MP4書き出し・印刷・スマートフォン縦画面は未検証。
- 原典内部localeはenのまま。日本語locale機能を追加したものではない。
- エージェント確認済み。人による採用は未承認。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
