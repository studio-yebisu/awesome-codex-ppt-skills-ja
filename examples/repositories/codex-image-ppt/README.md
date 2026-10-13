# Gitの保存・記録・共有 — 画像型PPTX

Codex内蔵の `image_gen.imagegen` で生成した日本語3ページを、ningzimu/codex-ppt-skill の原典 `assemble_ppt.py` でPowerPointにしました。全ページの元画像とPowerPoint 16.0のPNG/PDFを制作担当が確認済みです。

**各ページは1枚の画像です。本文・図・コマンドをPowerPoint上で個別編集できません。** 発表者ノートは日本語で3ページ分入っています。内蔵ツールの実モデル名は公開されないため、GPT Image2使用とは記載しません。

## 再現する

カタログrootからproject-local Python環境を使います。必要な組版依存は `python-pptx`, `Pillow`, `filelock`。共通skill runtimeのbootstrap、APIキー設定、外部API呼び出しは行いません。

1. `source/upstream/` の原典コードとLICENSE、`deck_spec.json`、`outline.md`、`style.json`を確認します。
2. 新しい制作フォルダーで原典 `prepare_slide_prompts.py --spec <deck_spec.json> --out-dir <deck>` を実行します。既存の生成記録を上書きしないでください。
3. `prompts/slide_XX.json` を読み、実際に利用可能なnative画像ツールで1頁ずつ生成します。実際に送った全文と引数は `source/native-imagegen-requests.json` にあります。2・3頁は1頁目を作風だけの参考にしています。
4. 原典 `record_slide_dispatch.py` / `record_slide_result.py` で本当の担当者ID・生成元パス・目視結果を記録します。生成画像を描画コードで置換しません。
5. 全画像を視認し、`speech.md` を用意して原典 `assemble_ppt.py <deckの親> <deck名>.pptx --aspect-ratio 16:9` を実行します。
6. PowerPointで全ページを再描画し、画像とノートを確認します。このカタログでは `pwsh -File tools/render_powerpoint.ps1 -PresentationPath <pptx> -OutputDirectory <render>` を使用しました。

既存画像からの再組版は `python tools/build_codex_image_repository_example.py assemble` で可能です。新規画像の生成はホストツールが必要で、Pythonだけでは実行できません。再組版後はPowerPointレンダーも更新します。

## 原典手順との差分

ユーザーから自律制作を依頼された範囲で、outline・style・sampleを制作担当が判断しました。人が見て承認したという記録ではありません。また、3頁を1人の割り当て済み制作agentが担当し、1頁ごとの追加子agentは作っていません。原典のdispatch/result CLIには実担当者IDを記録しています。`workflow-decisions.json` に差分を明示しました。

原典prompt compilerには言語共通のChinese-text文が残るため、実送信prompt末尾でJapanese指定を明確化しました。原典ソースは無改変です。元画像1672×941を原典packagerが16:9ページへ配置しています。画像の文字を手作業で描き足す処理はしていません。

## 出典と権利

Gitの説明は [Pro Git: Recording Changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository) と [Working with Remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes) を確認した独自の日本語要約です。実際のpushは行っていません。

原典コードはMIT。`LICENSE.upstream` と `source/upstream/LICENSE` の著作権・許諾表示を保持しています。画像は今回の生成物で、原典MITコードと生成画像の扱いを同一視しません。

## 再現キットに含めるファイル

自動の再現スクリプトは**既存3画像の原典組版だけ**を実行します。画像再生成は画像利用枠を消費する別操作です。同梱promptをnative画像ツールへ依頼する手順として案内し、APIキーを探す処理や自動画像生成は入れません。

最小のオフライン組版キットは、次の配置にします。

```text
reproduce/
  source/upstream/LICENSE
  source/upstream/skills/codex-ppt/scripts/assemble_ppt.py
  workspace/codex-image-ppt/origin_image/slide_01.png
  workspace/codex-image-ppt/origin_image/slide_02.png
  workspace/codex-image-ppt/origin_image/slide_03.png
  workspace/codex-image-ppt/speech.md
```

キット内の隔離Pythonへ `python-pptx` と `Pillow` を導入済みなら、キットrootから次を実行できます。原典packagerは画像の原本と3頁のノートを読み、同名フォルダー内にPPTXを出力します。

```powershell
& ./.venv/Scripts/python.exe ./source/upstream/skills/codex-ppt/scripts/assemble_ppt.py ./workspace codex-image-ppt.pptx --aspect-ratio 16:9
```

配布の再現証拠には上記に加え、`LICENSE.upstream`、`PROVENANCE.json`、`QA.json`、`environment.json`、`input/`、`PROMPT.txt`、`outline.md`、`style.json`、`deck_spec.json`、`workflow-decisions.json`、`slide_jobs.json`、`slide_run_state.json`、`prompts/`、`source/native-imagegen-requests.json`、`source/commands.json`、`source/logs/`、`render/powerpoint-render.json` を含めます。原典のjobs/state経路も再現する場合は `source/upstream/skills/codex-ppt/scripts/` の同梱Pythonスクリプト一式と `filelock` が必要です。

`tools/build_codex_image_repository_example.py` はカタログ用の補助で、単体の画像生成器ではありません。カタログroot、`.build/actual-upstreams/ningzimu__codex-ppt-skill`、`.build/ppt-master-venv/Scripts/python.exe`、`examples/repositories/codex-image-ppt` という配置に依存します。持ち運ぶキットでは、このhelperをそのまま動かすより上記の原典packagerを直接呼んでください。PowerPointによる再QAはWindowsとPowerPointを別途要します。
