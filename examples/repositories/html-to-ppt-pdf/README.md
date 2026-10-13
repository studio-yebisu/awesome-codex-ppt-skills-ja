# 週末の汐見港町 ― HTMLからPPTX・PDFへ

既存の日本語Guizang作例「週末の汐見港町 回遊企画提案」7ページを、wangzan101/html-to-ppt-pdfの固定原典CLIで変換しました。新しく資料の構成や本文を作った例ではありません。港町・予算・目標は架空の設定です。

- `deck.pptx`：各ページ1枚の画像。本文は個別編集できません。日本語の発表ノートは編集できます。
- `deck.pdf`：原典が生成した7ページのラスタPDF。検索可能な本文・ベクトルPDFではありません。
- `original/frames/slide-01.png`〜`slide-07.png`：原典の5760×3240 PNG。標準scale 3。
- `render/slide-01.png`〜`slide-07.png`：Microsoft PowerPoint 16.0が実際に描画した画像。
- `input/port-town/index.html`：入力原文。元カタログの`examples/cases/port-town/index.html`と同一です。

## 比較する

HTTPサーバーで`input/port-town/index.html`を開くと元の動く資料を見られます。変換後は`index.html`、PPTX、PDFを確認してください。下部のドットやキーヘルプも画像に含まれるため、PPTXではそれらをクリックしても動きません。

`review/compare-01.png`〜`compare-07.png`は、元HTMLの既存参考画像、変換PNG、PowerPoint実描画を並べた比較です。参考画像のビューポートは1280×720、今回の変換は1920×1080なので、レスポンシブな余白や文字サイズには差があります。本文と順序を保持し、変換PNGとPowerPointの全7ページを目視しました。「どの環境でも画素100%一致」という保証ではありません。

## 再生成

```sh
python source/reproduce.py
```

Python 3、Node.js 22+とnpmが必要です。初回に固定lockの依存とPlaywright Chromiumを取得します。Nodeの自動検出が適切でなければ`--node`で実行ファイルを指定し、既存のPlaywrightキャッシュを使うなら`--browser-cache`を指定します。APIキーや有料サービスは使いません。

WindowsでPowerPoint実描画も更新する場合：

```sh
python source/reproduce.py --powerpoint
```

Microsoft PowerPointとPowerShell 7が必要です。`--powerpoint`なしではPPTX/PDFと原典PNGを生成し、PowerPointプレビューは更新しません。再生成時はQAを`generated_awaiting_review`へ戻すので、目視レビュー済みを引き継ぎません。別フォルダのクリーンな依存導入から再生成し、7枚のPNGが一致した記録は`review/portable-proof.json`です。

## 原典との差

`source/upstream/scripts/build.mjs`と実行した`source/runtime/build.mjs`はバイト一致しています。

原文をそのまま変換した初回は7枚成功というログでも2ページ目が表紙の重複になりました。Guizangの`go()`が700ミリ秒の連続操作制限を持ち、変換器の静止モードではそれより早く次のドットを押すためです。`export.html`にだけ、ドットの移動で元の`go(i,{force:true})`を呼ぶ互換処理を加えています。本文・配色・レイアウトは変更しません。初回の誤った出力は`review/initial-unadapted-output/`に証跡として分けています。

原典lockの`image-size 1.2.1`に対して監査でHighが1件報告されたため、`image-size 2.0.3`のoverrideでlockを更新しました。PptxGenJSは3.12.0のままです。更新後の監査は0件。元・更新後のpackageとlock、差分、監査ログを保持しています。

Git Bashの`setup.sh`はWindowsのnpmランチャーで失敗したため、Nodeと同じインストールにある`npm-cli.js`を直接呼んで導入しました。PowerShell 5のレポート取得もこの環境では`Get-FileHash`不在で失敗し、PowerShell 7で完了しています。

`deck.pptx`の日本語発表ノートは変換後の後処理です。無加工のPPTXは`original/deck.pptx`に保持。`review/postprocess-proof.json`で変更がnotesSlide XMLだけであることと、全スライド・画像のバイト一致を確認できます。

## 出典と条件

変換器MIT、入力HTML・対応ソースAGPL-3.0、埋め込み書体OFL-1.1を分けて保持しています。詳しくは`LICENSES.md`。`PROVENANCE.json`にコミット、SHA、実引数・cwd・終了コード・ログのSHAを記録しています。

エージェントによる制作・検証済みです。人による採用、外部公開は未実施です。
