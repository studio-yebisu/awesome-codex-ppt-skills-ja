# 画像から編集できるGit入門へ

元画像2枚を原典 `image-to-editable-ppt` のprepare → page worker → build/validate → record → finalizeで再構成した作例です。新しい日本語原稿をゼロから生成する作例ではありません。

`deck.pptx`の文字・カード・単純な矢印はPowerPointのnative要素です。アイコンは内蔵image_genで元画像から分離した画像で、内部の線や色は個別編集できません。元画像はinput、ページmanifest・編集結果・検証はrun/pages、完成PowerPointの描画はrender。画像入力に発表者ノートは含まれません。カタログ制作時に新規作成した日本語案内ノート2件を、原典CLIの出力後にpython-pptxで追加しています。input/data.jsonとカタログの発表メモとPPTXノートは同じ文章です。元画像からの抽出ノートではありません。source/notes-addition.jsonに変更前後のSHAと本文XML・画像の不変を記録し、replayでも同じ処理を実行します。前作の説明ノートはsource/original-NOTES.mdを参考資料として保持しています。

## 再構成と再出力

新しい画像では、同梱source/upstream/skills/image-to-editable-ppt/SKILL.mdを読ませ、PROMPT.txtと入力を渡してください。画像編集を使うAIエージェントとページworkerが必要です。APIキーやOAuthの読取りはこの作例では行っていません。外部OCRは使わず、ローカルtext hintsと画像の視認を使用しました。

保存済みmanifestと分離済み画像からの再出力はPython 3.10+と原典CLI依存の導入後、次で行えます。新しい画像編集やworkerを再実行するコマンドではありません。

```powershell
python -m pip install -e source/upstream/skills/image-to-editable-ppt/cli python-pptx==1.0.2
python source/build_image_editable_repository_example.py --replay --source-dir . --output-dir ../image-editable-replayed --upstream-dir source/upstream
```

既存出力先は拒否します。再出力後は表示レビューが必要です。原典CLIのPyMuPDFなど依存パッケージは別途導入し、そのライセンスに従ってください。原典ソースはMIT、LICENSE.upstreamを保持。第三者の公式作例や、人間による採用済みという意味ではありません。
