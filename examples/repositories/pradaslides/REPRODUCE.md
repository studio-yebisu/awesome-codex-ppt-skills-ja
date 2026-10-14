# 町内会の備品貸出を、迷わない手順にの日本語再現キット

Windows、Microsoft PowerPoint、PowerShell7、Python3、OS游ゴシックが必要。HTTP QAを行う-RenderにはNode.js22以上とChrome/Edgeも必要。

1. ZIPを展開しPowerShellを開く。
2. `.\reproduce\Reproduce.ps1 -Render` を実行。必要なら `-NodePath "node.exeの絶対パス"` を添える。
3. 出力は `reproduce/workspace/examples/repositories/pradaslides/`。新しい出力は確認前の状態で記録する。全6ページを改めて確認してください。
4. 出力フォルダーで `python -m http.server 8000 --bind 127.0.0.1` を起動し、localhostのHTML入口を開く。

原典のbootstrap、brief・出典・設計・レイアウト等の契約validatorとstrict plan lintを使い、native PPTXを作る。原典はauthoring engineを固定しないため、この作例では専用python-pptxソースを使用する。PowerPoint実描画から無改変の原典build_pptx_preview.pyでrender-parity presenterを作り、原典由来HTTP QAを実行する。ブラウザー表示の本文は画像、編集正本はPPTX。OS游ゴシックは配布せず、MITの原文を保持する。

制作原稿と構成はinput/data.json、日本語ノートと制作手順はREADME.mdとPROVENANCE.jsonを参照。構成の変更時は原典の計画・寸法・配置検査と全ページの表示確認を行う。原典MITと素材・依存の各条件を保持し、人の正式採用や公開は別とする。
