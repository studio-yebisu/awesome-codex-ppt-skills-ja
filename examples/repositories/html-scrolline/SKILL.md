---
name: html-scrolline-ja
description: gongnyang/awesome-html-scrolline-deckの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

# html-scrolline-ja

Studio Yebisuの日本語派生版。原作者の公式翻訳ではありません。

## 原典を読む

- upstream/SKILL.md

同梱README.mdで、実作例・入力・環境・コマンドと確認範囲を読む。

## スキルの選択肢

原典はrail/data/launch/zoom/canvas/kineticの6conceptを持ち、MP4は`npm run export`で出力する。今回の例はrailだけを使い、他conceptとMP4は未実施。

## 固有の制作方式

原典deck.yaml・plan・Vite build・Scrolline engineとrail-advance/era-shiftで6停止点を連続的につなぐ。engine/moves/conceptsは原典と一致。内部localeはen、HTMLの表示は日本語。Windows Chrome探索だけを明示adapterで補正する。原典全体CIのWindowsパス3件不合格を保持し、HTTP上のcore・smoke・操作確認と分ける。GSAP独自条件と各MITの原文通知を分けて保持。

## 連続する日本語の資料を作る

原典CONTRACTSとrailの例を読み、deck.yamlで停止点、時間、項目、handoffを設計する。原典plan、Vite build、smokeを使い、engine・moves・conceptsを改変せず、deck側のCSSと本文で日本語へ合わせる。内部schemaのlocaleはen、HTMLのlangはja。日本語locale機能を実装したとは呼ばない。

原典全体CIのWindowsパス3件不合格は保持する。中核424テスト・HTTP smoke・キー・ホイール・補間の確認と区別し、原典の全ゲート通過を主張しない。捕捉用Chrome探索のadapterは原文と差分を残す。直接file://の禁止を別経路で回避しない。

原典コードのMIT、LenisのMIT、GSAP独自の無償標準ライセンスを分けて読む。Viteが削除する通知は配布bundleと単一HTMLへ復元する。GSAPへMITやカタログのCC0を付け直さない。フォントは端末の日本語書体を使う当作例の条件を記し、新しい字形と全停止点を実際に確認する。

## 日本語で完成させる

- 先に読み手、目的、結論、必要なページ、出力形式を決める。
- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。
- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。
- この作例は端末の游明朝・游ゴシック等を使い、Webフォントを埋め込んでいない。書体を替えたら全停止点を描画し直す。PPTXは対象外。
- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はREADME.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 現在の作例の実施範囲（Round4）

railだけを使い、5月企画→6月会場→7月案内→8月当日を連続して示す。月の間隔を広げて項目名を添え、停止画と自然な移動途中の両方で変化を確かめた。

- 原典はrail/data/launch/zoom/canvas/kineticの6conceptとMP4 exportを持つ。今回制作したのはrailだけで、残り5conceptとMP4は未実施。
- 内部localeはenのまま、日本語本文と端末字体を利用。日本語locale機能を実装した作例ではない。
- 原典全体CIのWindowsパス3件不合格は旧実行記録を保持。今回のbuild/smokeと操作検査を、全CI合格へ読み替えない。印刷・縦長mobile・60fpsの定量確認も未実施。

全6頁の実描画と個別の動作証拠は制作側の確認。独立Kimi K3/Opus5.5の新しい版の評価は別に行う。過去の採点を新しい画像へ引き継がない。
