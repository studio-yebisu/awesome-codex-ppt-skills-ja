# 引き継ぎは、次の一手まで。の日本語再現キット

Python3、Node.js22以上とnpm、公式Chromium取得の接続が必要。PowerPoint描画を行う-RenderにはWindows、Microsoft PowerPoint、PowerShell7とインストール済みBIZ UDPGothicも必要。

1. ZIPを展開しPowerShellを開く。
2. `.\reproduce\Reproduce.ps1 -Render` を実行。必要なら `-NodePath "node.exeの絶対パス"` を添える。
3. 出力は `reproduce/workspace/examples/repositories/presentation-delivery/`。新しい出力は確認前の状態で記録する。全6ページを改めて確認してください。
4. 出力フォルダーで `python -m http.server 8000 --bind 127.0.0.1` を起動し、localhostのHTML入口を開く。

原典Visual Deck StudioのHTML-first Path A、960×540ptの4条件、無改変の変換・寸法・overflow検査とDOM要素変換を使う。原典deck_index.htmlの概覧・キー操作とPDF結合を保持する。明示HTTP入口、字体待ち、日本語ノート、Windows環境継承だけをadapterで補う。本文文字と図形はnative PPTX。HTML/PPTXの字間・太さ・br行間には差があり、pixel一致・動画・TTS・人の早期承認は主張しない。BIZ UDPGothicのOFL原本を同梱する。

制作原稿と構成はinput/data.json、日本語ノートと制作手順はREADME.mdとPROVENANCE.jsonを参照。構成の変更時は原典の計画・寸法・配置検査と全ページの表示確認を行う。原典MITと素材・依存の各条件を保持し、人の正式採用や公開は別とする。
