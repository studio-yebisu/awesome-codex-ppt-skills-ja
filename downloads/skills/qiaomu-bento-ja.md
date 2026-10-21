---
name: qiaomu-bento-ja
description: 編集できる単体HTMLのBento資料を作る。文書IDと固定shellを保って更新し、同じ要素IDの移動でページ間の関係を示すときに使う。
---

## このスキルでできること

原稿やデータを編集できる単体HTMLへまとめ、同じ要素を動かしながら説明できるようにする。

- 困っている状況: HTMLを修正するためにコード編集が必要だと、利用者が本文や表を直しにくい。
- 必要な入力: 新規作成では依頼内容・ノート・報告・データ・参照URL。更新では原本HTMLと文書データ、更新対象の識別ID。
- 受け取るもの: オフラインで編集するHTMLと閲覧用HTML。文書と要素の識別IDを保ち、更新前後を検査できる。
- 必要環境: Python3、fontTools/Brotliとモダンブラウザー / 同梱standalone shellが標準経路。原始Bento checkoutと追加shell gateは任意
- 作例で試した範囲: 同梱standalone shellを通常の制作経路として使用。3→4頁は同じトークンのmorph、5頁は目標24/30の原典chartとcountUp、表紙と締めには本文に基づく図を配置した。

# Bento資料を日本語で作成・編集する

原典 [SKILL](upstream/SKILL.md) と references/WORKFLOW.md を読む。原典の固定コミット、MITとBento個別条件を保持する。PPTX/PDFの生成は対象外。

1. 原稿・ノート・データ・参照URLから新規作成するか、既存HTMLを更新するかを決め、読者・目的・オフライン範囲をdeck-planへ書く。同梱standalone shellが通常経路で、元リポcheckoutは前提ではない。locateで同梱format/shellを確認し、checkoutがある場合だけ追加のproject検査を使う。
2. 新規作成は文書JSONの必須項目から組み立てる。既存HTMLの更新では原本を保存し、extractで文書JSON全体を取り出す。docId、未知フィールド、要素ID、共同編集情報を勝手に消さない。JSONの更新は --identity-source 原本HTML で同一文書と確認する。
3. 別の出力先へbuildする。原本と出力を同じパスにしない。新しい文書へ明示的に複製するときだけ、継承したdocIdとcollabを外したコピーに --new-document を使い、一度だけIDを発行する。共同編集能力を公開資料へ混ぜない。
4. 数値はchart、仕様や比較はtable、連続変化はmorph、重要数値はcountUpへ割り当てる。同じ概念には同じ要素IDを使う。移動する対象、順序、最後の状態を本文と図の両方で説明し、形と字体の必須項目を満たす。固定shellを作り替えない。
5. validate、schema、shell、文書IDのgate結果を保存する。編集、保存、再表示と通常のmorphをブラウザーで確認する。直接保存、JSON書出し経由、別文書コピーを区別して記録する。

作例は社内検索の架空企画6頁。3役の位置を保ち、3→4頁で文書トークンと強調位置が権限確認から回答と出典へ移る。実際の検索・権限制御・共同編集・検索精度の実績は実装していない。日本語は固定版Noto Sans JPの必要字形を再収録し、OFLを保持する。

制作キットの `source/rebuild_bento.py --output-dir 新しいフォルダー` は元CLIと同じ固定shellで再生成する。元UIのJSON書出し→元CLIの別文書保存→再表示は実確認済み。IABの直接「コピーを保存」の完了は未確認。同じdocIdの再表示ではブラウザー既存状態が優先される場合があった。

## 現在の作例の実施範囲（Round4）

同梱standalone shellを通常の制作経路として使用。3→4頁は同じトークンのmorph、5頁は目標24/30の原典chartとcountUp、表紙と締めには本文に基づく図を配置した。

- 元リポのcheckoutは前提ではなく、同梱standaloneが通常経路。project側の追加validatorはcheckoutが無いため未実行。
- 画像+scrim/ken-burns、state slide、外部媒体、共同編集、実検索と権限制御は未実証。
- ブラウザーの直接「コピー保存」は完了未確認。同docIdコピーは既存状態の影響を受けたため、独立コピーは --new-document を使用した。
- countUpの初期化前に静的値が一瞬描画される原典挙動がある。途中値が増加する区間を撮影し、連続動画全フレームの品質保証とはしない。PPTX/PDF出力は対象外。

全6頁の実描画と個別の動作証拠は制作側の確認。独立Kimi K3/Opus5.5の新しい版の評価は別に行う。過去の採点を新しい画像へ引き継がない。

## 単体の本文から使う

この本文は `skill-forks/qiaomu-bento-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/joeseesun/qiaomu-bento-ppt/tree/55c63c836f42bc9175757d077428c395cd93effe

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `qiaomu-bento-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: joeseesun / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/LICENSE
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/NOTICE.md
