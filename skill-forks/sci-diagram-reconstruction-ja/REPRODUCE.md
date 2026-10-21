# 保存済み復元の再実行

展開した作例rootをCWDにする。ホストの準備済みruntimeのnode_modulesを祖先から解決できる場所へ置き、作業passへコピー・installしない。現在のaccepted outputを再生成するので--overwriteを明示する。新規の科学図を考案・復元する入口ではない。

```powershell
python source/reproduce.py --overwrite --render --node <Node.js実体> --soffice <既存soffice> --pdftoppm <既存pdftoppm>
python source/check_native_lines.py
pwsh -NoProfile -File source/test_shape_edit.ps1 -PresentationPath pass-01/editable.pptx -OutputDirectory qa/editability
```

本体は原典probe→実際のpass-01/build.mjs→原典checker（--source pass-01/source.png）→XML方向検査→原典isolated LibreOffice renderer→実PowerPoint PDF→pdftoppmの順。PowerPoint全体は終了せず、この処理が開いたプレゼンテーションだけを閉じる。新しい出力へ過去の目視・独立評価を移さない。再表示後は原図と比較する。

原典LibreOfficeのPDF・PNGは、各再生の `qa/original-libreoffice-replay-<UTC時刻>/` に保持する。一時profileと作業領域だけを片付け、描画の証拠は削除しない。自分の別画像で制作する場合は [START-HERE.ja.md](START-HERE.ja.md) を使う。

## 複合例の保存済み追加pass-04

同じ作例rootをCWDにし、採用版とは別の展開コピーで実行する。

```powershell
python source/reproduce_complex.py --overwrite --render --node <Node.js実体> --soffice <既存soffice> --pdftoppm <既存pdftoppm>
```

[複合例README](example/complex-example/README.md)にnative/rasterの所有、原典既定2passと明示された追加pass4、残る警告を記録した。現在のbuild.mjsは矢じりの局所補正まで自己完結し、Python arrow helperを呼ばない。3ファイル（build.mjs、source.png、editable.pptx）が引き渡し単位。原典checkerは--pass-indexを省いて構造を検査するが、それをpass04の承認証明にはしない。同じ保存buildを再生するだけで、新たなauthor passは作らない。再生後は新しいPowerPoint/LibreOffice表示を元画像と照合する。

Windowsでは準備済みruntime直下に近い短い展開先を使う。深い二重フォルダーの再生ではLibreOfficeの一時profileが長パスになりtimeoutした。現在の再生helperは原典LibreOffice rendererをOS所有の一時フォルダーで実行し、完了したPDF/PNGをcaseのqaへコピーして保持する。原典コードと依存は変更しない。複合例の保存先は`qa/c-lo-<UTC時刻>/`と`qa/c-pp-<UTC時刻>/`。
