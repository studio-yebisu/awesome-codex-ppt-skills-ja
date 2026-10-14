# PradaSlides 日本語実作例

「町内会の備品貸出を、迷わない手順に」全6ページ。架空の町内会に向けた手順案です。実在の規則・実績を表しません。

編集正本は `output/deck.pptx`。文字・用紙・手順・照合表をnative要素で作成しています。`presenter/index.html` は原典 `build_pptx_preview.py` でPowerPoint実描画を取り込んだrender-parity HTMLです。ブラウザー側のスライドは画像で、編集はPPTXまたはソースで行います。

## 再現

Windows、Microsoft PowerPoint、PowerShell 7 (`pwsh`)、Python 3.10以降、Node.js 22以降、ChromeまたはEdgeが必要です。フォントはOSの游ゴシックを利用し、フォントファイルは配布しません。

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe source/reproduce.py
.venv/Scripts/python.exe source/qa.py
python -m http.server 8765 --bind 127.0.0.1
```

このフォルダーで実行し、`http://127.0.0.1:8765/presenter/index.html` を開きます。Arrow/Home/Endキー、ノート表示、印刷に原典presenterを利用できます。再実行はこの作例の出力とレビュー記録を更新します。

`reproduce.py` は計画生成が失敗した時点で停止します。実行開始時に過去のレビュー状態を無効にし、成功時は `QA.json` を `generated_awaiting_review`、失敗時は `generation_failed` に更新します。前回の目視確認・独立レビュー・採用状態は引き継ぎません。

`qa.py` は既定でPATH上のNode.jsを検索します。別のNode.jsを使う場合は、例えば `.venv/Scripts/python.exe source/qa.py --node "C:/Program Files/nodejs/node.exe"` のように実在する絶対パスを指定してください。検査はローカルHTTPのみで行い、成功しても目視レビュー済みには変更しません。

## 原典を使った範囲

固定commit `b9219b238d812d0dd7b4ed9fb514effbad0d0928` のSKILL、教える資料のplaybook、bootstrap、設計・出典・レイアウト等の契約validator、strict plan lint、PPTX inspection、render-parity previewを実行しています。原典はPPTX作成エンジンを固定していないため、このホストで利用可能なpython-pptxによる作例専用の `source/author.py` を使用しました。原典同梱の完成見本を変更したものではありません。

HTML QAは原典の検査処理を維持し、入口をローカルHTTPへ変更した `source/qa_http.mjs` で実行。変更差分は `source/qa_http.patch`。ブラウザーのfile URLは使いません。モンタージュ経路は無効化しています。

`review/` に実argv・cwd・終了コード・ログSHA、検査JSON、全ページの表示記録を保存。初回design validatorの失敗も残しました。修正後は全errorが解消。briefの日本語を空白単語数で測る短文warningが1件残ります。

6ページを作者エージェントがPowerPoint実描画で確認済み。独立再現・別エージェントレビューはQA.jsonの現在状態を参照してください。人による正式採用を表すものではありません。

## 利用条件

原典コードと参照文書はMIT。`licenses/LICENSE-upstream.txt` に著作権表示と許諾文を保存しています。参照したファイルだけを `source/upstream` に収録。原作者の紹介画像・完成例・フォント・node_modulesは含めていません。
