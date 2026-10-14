---
name: sebastian-207-ja
description: 原典のeditorial-inkとnative PowerPoint生成器で、日本語の編集可能な誌面風資料を作る。
---

# 日本語の編集室スライド

原典固定URL：https://github.com/MURMURE11118586/codex-xkppt-skill/tree/978b46d116fd8fd971f9cd963f745da62f7f1f26

1. 原典SKILLとreferences/native-pptx.mdを読む。native_pptxを選び、原典build_native_pptx.mjsとdesign-system/native/を使う。
2. input/BRIEF.mdを自分の題材へ置き換える。架空の企画・期間・数値は仮定と明示する。
3. spec_lock.jsonで日本語書体・紙色・墨黒・朱色を指定する。見出しは意味で改行し、各頁は一つの役割に絞る。
4. slides_plan.jsonでcover-editorial、statement-hero、quote-editorial、before-after、case-study、process-linear、roadmap、closing-echoの密度を変える。数値用の原典chartを使う場合、固定デモデータを本物と混同しない。
5. 表紙は本と街の関係を示すページ固有のAI画像を用意する。画像へ文字を焼き込まない。タイトル・本文・工程はネイティブ編集可能にする。
6. 一式ZIPのREADMEに従い生成し、完成PPTXを実レンダリングする。画像欠け・日本語改行・表示フォントを確認する。結果と方式を正確に記録する。

原典MIT LICENSEを保持する。この短い本文のみでは生成器と依存は揃わない。必要な一式ZIPまたは固定原典を取得する。

日本語派生では固定中国語ラベルと言語を日本語化し、体験図・工程・文字主体の締めをnative visualとして計画した。原典のAI挿絵最低1点は表紙で満たすが、原典自動QAの合格を保証しない。
