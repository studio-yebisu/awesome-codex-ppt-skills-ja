---
name: pradaslides-ja
description: PradaSlidesの計画契約・native PPTX・実描画presenterを使って、日本語の説明資料や手順書を制作・更新するときに使う。
---

# PradaSlides 日本語版

Studio Yebisuの独自派生。原作者の公式翻訳ではない。原典は固定commit `b9219b238d812d0dd7b4ed9fb514effbad0d0928`。MITの許諾文と著作権表示を `upstream/LICENSE` に保持する。

## 先に見る実例

「町内会の備品貸出を、迷わない手順に」日本語6枚。申込書の記入例、受取りの三手順、不具合の連絡、返却照合をnative文字・図形で制作した。

完成例ZIPの `input/data.json`、`project/deck-plan.json`、`source/author.py`、`output/deck.pptx` を対応させて読む。実描画の全6枚を作者と別エージェントが確認した。架空の案内で、町内会の正式規則ではない。

## 原典から制作する

1. `upstream/SKILL.md` と、今回の資料に合う `upstream/references/intent-playbooks.md` を読む。機能の列挙でなく、読み手が資料を見た後にすることを決める。
2. 原典bootstrapと計画契約を使う。読み手・目的・出典・主張・レイアウト・必要素材を `brief`、`source-ledger`、`design-system`、`layout-manifest`、`asset-manifest` へ記録する。
3. 原典validatorと `lint_deck_plan.py --strict-visual` を実行し、errorは修正する。日本語を空白単語数で数える短文warningは、内容を実読して判断し、隠さず記録する。
4. 指定されたauthoring engineでPPTXを作る。原典はengineを固定しない。この作例の `author.py` は専用python-pptxソースで、共通rendererや原作者の完成デッキを代用していない。
5. PowerPoint本体で全ページを描画する。本文・表・日時・単位・ノートを入力と照合する。OS字体が置き換わる端末では、同じ字体を用意するか配置を再確認する。
6. 無改変の原典 `build_pptx_preview.py` で、実描画からrender-parity presenterを作る。ここでのHTML本文は画像。編集正本はPPTXである。
7. 原典のHTML QAをHTTP入口の派生で実行し、ブラウザーでページ・ノート・キー操作を確認する。差分を保存し、file URLの実行と混同しない。

## 日本語の実用性

- 「品名・数量」「日時・場所」「担当窓口」など、読み手が確かめる内容を同じ順番で示す。
- 実在ルールがない部分は案・記入例と明示する。利用条件や責任を資料側で勝手に決めない。
- 単位と値、見出しと本文、完了と未確認を分ける。説明をすべて同じ大きさに詰めない。
- 見出しは意味の区切りで改行し、本文はPC閲覧や画面共有でも判読できる量にする。
- 入力を変えたら `plan.py` と専用authoringソースも合わせる。すべての構成変更をJSONだけで自動処理する製品ではない。

## 再現

完成例ZIPで、Windows / Microsoft PowerPoint / PowerShell7 / Python3 / 游ゴシックを使う。

```powershell
python -m pip install -r requirements.txt
python source/reproduce.py
python source/qa.py --node "node.exeの絶対パス"
```

HTML QAにはNode.js22以上とChrome/Edgeが必要。`source/reproduce.py` は計画失敗で止まり、新出力をレビュー待ちにする。前回の全ページ確認や採用を引き継がない。

環境・実行ログ・実際の編集範囲は `references/WORKFLOW.md` と作例の `PROVENANCE.json`、`QA.json` を読む。フォント本体・原作者の広告素材・node_modulesは収録しない。

## 単体の本文から使う

この本文は `skill-forks/pradaslides-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/prodigeproject/pradaslides/tree/b9219b238d812d0dd7b4ed9fb514effbad0d0928

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `pradaslides-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: prodigeproject / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/LICENSE
