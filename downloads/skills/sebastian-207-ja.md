---
name: codex-ppt-skill-ja
description: 原稿と編集条件を先にそろえ、参照資料で書式を決めて、比較・手順・日程を後から直せる資料へ組む。
---

## このスキルでできること

原稿と編集条件を先にそろえ、参照資料で書式を決めて、比較・手順・日程を後から直せる資料へ組む。

- 困っている状況: 同じ原稿でも、実行方式・図の目的・書式を決めずに作るとページ間で設計がぶれる。
- 必要な入力: 目的・聴衆・元資料・編集性などの制約と、参考にする資料や画像。
- 受け取るもの: 要件に応じた制作方式のスライドと、頁計画・話者ノート・描画・機能と見た目の検査記録。
- 必要環境: 新規制作はCodex built-in imagegenと保存画像のcaptureが必要。原典はpresentations/$slides優先、ローカルfallbackはNode/PptxGenJS。画像生成手段がなければ原典の完成資料合格条件を満たせない。 / 保存済み例の再実行はNode・既存PptxGenJS4.0.1、Python3/Pillow/python-pptx。新規installや画像再生成は今回未実施。 / PowerPoint全頁描画はWindows版PowerPointとPDF描画用pypdfium2。同梱OFL字体を登録。
- 作例で試した範囲: 後編集を優先してnative経路を選び、参照・原稿・画像の役割を固定。表紙の実AI挿絵を残し、4頁では同じ観点の比較、6頁では工程と説明、8頁では未確定条件をnative要素で示す。原典機能QAと美術QAを再実行した。


この日本語スキル内のinput/・source/・qa/・render/は同梱example/内を指します。現在の実行はexample/をCWDにしてください。

# 編集条件に合わせて制作経路を選ぶ

原稿と編集条件を先にそろえ、参照資料で書式を決めて、比較・手順・日程を後から直せる資料へ組む。

原典codex-ppt-skillは、要件からtemplate/native/HTML/image-firstを選び、参照から書式を決め、頁ごとの図・画像とノートを計画して、機能検査と美術検査を通す。作例は後編集のためnativeのローカルfallbackを使う。

## 渡すものと受け取るもの

渡すもの：原稿・元資料、読み手と目的、発表時間、PPTXの後編集やHTML表示の条件、使うテンプレート・配色・書体・参考資料。画像版にする場合は個別編集できないことへの同意。

受け取るもの：選んだ方式の編集可能PPTX、HTML/PDF/PNG、または全面画像PPTX。選択理由・書式指定・頁計画・画像来歴・話者ノート・機能/美術QA・納品目録を添える。画像版の本文は個別編集不可。

## 用意するもの

- 新規制作はCodex built-in imagegenと保存画像のcaptureが必要。原典はpresentations/$slides優先、ローカルfallbackはNode/PptxGenJS。画像生成手段がなければ原典の完成資料合格条件を満たせない。
- 保存済み例の再実行はNode・既存PptxGenJS4.0.1、Python3/Pillow/python-pptx。新規installや画像再生成は今回未実施。
- PowerPoint全頁描画はWindows版PowerPointとPDF描画用pypdfium2。同梱OFL字体を登録。

## 手順

1. 元資料と読み手・目的・発表時間を渡す。既存PPTXの書式維持ならtemplate、テンプレートなしで後編集するならnative、HTML/PDF表示でよければHTML、個別編集を諦める同意がある場合だけimage-firstを選ぶ。
2. 原典build_reference_board.pyで参照を選び、使う書式・書体・配色と引用範囲をdesign_specへ記す。
3. 頁の主張・図・画像計画・ノートを固定。必須画像はbuilt-in imagegenで作り、保存した実画像を原典captureへ渡して頁と結び付ける。
4. 選んだ原典経路で制作し、機能検査・85点以上の原典美術QA・全頁描画を確認して不具合を直す。
5. 原稿・完成物・実描画・QAとdelivery_manifestをそろえて渡す。新しい生成結果へ過去の目視を引き継がない。

## 作例の見る場所

後編集を優先してnative経路を選び、参照・原稿・画像の役割を固定。表紙の実AI挿絵を残し、4頁では同じ観点の比較、6頁では工程と説明、8頁では未確定条件をnative要素で示す。原典機能QAと美術QAを再実行した。

- 1頁・頁に結び付いた挿絵：開いた本から街が立ち上がる実imagegen挿絵が右枠に入り、左の編集可能な見出しと干渉しない。画像はこの頁の本と街の主張に結び付く。
- 4頁・同じ観点の比較：本との関わり・感想と体験・持ち帰るものの3観点が、左右の同じ高さで比べられる。下半分まで内容を置き、空の比較枠を残さない。
- 6頁・工程と説明の対応：選書・街歩き・編集・共有の4本と、その真下の同じ番号の説明を読む。終点の共有と番号4だけが朱色で、番号1との矛盾がない。

2頁の条件は2列で配置、8頁は空の背景パネルを取り除き、未確定の相談事項をnativeで示す。原典QA87.6/PASS、右側未使用0・overfillを含むfailure_modes/issue0。機能QAのpossible-overlap警告は保持し、全8頁を実物で確認した。

## 差分と限界

- 実演はnative経路。原典はpresentations/$slidesを優先し、ここでは原典PptxGenJSのローカルfallbackを使用。他3経路は未実施。
- 新規資料の原典合格条件には、Codex built-in imagegenで生成して保存した、頁の内容に合う画像が最低1枚必要。native図形やプレースホルダーで画像生成済みとはしない。
- 本例は表紙の実AI挿絵を保持。その他の頁はnative文字・図を計画し、画像生成必須=false・省略禁止=falseへ整合。必須画像を生成せず済ませた扱いにしない。
- 原典のnative APIを使い、日本語ラベル、文字箱、2列の項目、比較軸、工程の対応、締めの確認項目を派生差分として保存。原典ファイルとQA/閾値は未変更。
- 原典美術QAは87.6/PASS。右側未使用0件、overfillを含むfailure_modes/issue0件。possible-overlap警告は別の機能QAで保持し、全8頁の実物を確認。
- 書店企画と4週間は架空・実施前。開催実績や効果の測定値を作っていない。機械87.6点は独立採点の100点ではない。

新規画像の生成はCodex built-in imagegenを使い、原典captureで保存した画像の来歴を残す。日本語ユーザーには日本語で説明する（原典の中国語指示は中国語ユーザー向け）。用語だけを列挙せず、参照から何を引き継ぐかと、各画像がどの主張を示すかを記す。

原典MURMURE11118586/codex-xkppt-skill、固定commit978b46d116fd8fd971f9cd963f745da62f7f1f26、MIT保持。raw原典はsource/upstream-original、派生差分はsource/runtime-adapter.diff、実行はsource/reproduce.py。保存済み例の再生成では新しい画像生成を実行しない。現在独立再評価は別。配布再実行はsource/distribution-replay.json。


今回の2・5頁は、既存項目を下半分まで均等に配置し直した。本文の追加・削除や新しい画像の生成はしていない。配置の意図と比較はqa/vertical-density-review.json。原典の図形APIとQA閾値は変更していない。PowerPointの自動処理は開いた資料だけを閉じ、アプリのQuitを呼ばない。

## 単体の本文から使う

この本文は `skill-forks/sebastian-207-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/MURMURE11118586/codex-xkppt-skill/tree/978b46d116fd8fd971f9cd963f745da62f7f1f26

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-207-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: MURMURE11118586 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/MURMURE11118586/codex-xkppt-skill/blob/978b46d116fd8fd971f9cd963f745da62f7f1f26/LICENSE
