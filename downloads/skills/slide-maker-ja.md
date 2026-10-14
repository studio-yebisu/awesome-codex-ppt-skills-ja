---
name: slide-maker-ja
description: 原典slides_makerのdeckkit・native chartと独立レビューで、根拠のある日本語PowerPointを制作する。
---

# 根拠を図とグラフへつなぐ日本語PPTX

原典は addsumtech/slides_maker。upstream/skills/slide-maker/SKILL.md と必要なdesign-principles、agentsの担当仕様、references/WORKFLOW.mdを読む。原典deckkit/native_chartと原典検査を使う。

## 入力と日本語化

読み手、目的、話すか手元で読むか、根拠資料・実行結果を用意する。見出しでそのページの結論を述べ、単位・条件・測っていない範囲を図と講稿に残す。作例の検索回数は1〜15の配列で実行した要素照合回数で、秒数のベンチマークではない。

## 制作

1. 入力を読み、構成案とデザイン案を比較し、選ぶ理由を記録する。一般的なユーザー要件の確認はセッションで承認された範囲から判断し、人の採用を捏造しない。
2. 原典sigs.pyで使用するhelperのsignatureをまとめて確認。図はnative shape、数値はnative chartへ結び付け、同じ入力から全冊を生成する。
3. 日本語書体を明示する。作例はWindowsのYu Gothic。搭載フォントをPCから抜き出して再配布しない。
4. 原典lintとgateを実行し、未適用・waiverの理由を具体的に残す。deckkitの画面外semantic titleはアクセシビリティ用で、見た目だけのために削除しない。
5. 実PPTXをPowerPointで全頁描画。独立criticで根拠と図を照合し、別の文脈を渡さないreaderでfirst readを確認する。指摘を修正して候補を確認する。

## 作例と確認範囲

同じ作例を再生成するキットと、別の原稿から作る工程を区別する。再出力に元のQAを移さず確認前として扱う。この5枚はselfread用で、投影可読性は未検証。構成・方向比較を制作後に追加した事実を、最初から全時系列の工程を完走した記録へ変えない。原典MITと個別依存条件を保持し、正式採用・外部公開は別に記録する。

## 単体の本文から使う

この本文は `skill-forks/slide-maker-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/addsumtech/slides_maker/tree/3767cc346d63ef1646082c87f15fbf0be582b152

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `slide-maker-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: addsumtech / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/LICENSE
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/LICENSE
