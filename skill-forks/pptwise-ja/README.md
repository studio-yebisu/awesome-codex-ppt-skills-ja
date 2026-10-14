# ひらく、街の作業場。

架空のものづくり拠点を提案する日本語6ページ。利用者数、収支、面積、実績を作らず、入口・体験・関係・空間の概念構成を語ります。

## 原典方式

liustack/pptwise0.44.0を固定source commitからbuildし、IR v5を原典validate→render CLIへ渡しました。原典Rallyをtheme forkで橙・墨・紙色へ派生。元marquee menuを保ち、日本語OSS書体、角のないruled surfacesを設定しています。元のflowchart/hub_spoke/architectureのtyped componentsとtheme/layout/export engineがnative図形と文字を生成。共通rendererへ名前を貼る方式やPPTX後加工ではありません。

## 再制作

Node22.19+が必要。runtime/は元MITのbuilt CLIと必要source、元package.json/lockです。画像API・認証・有料pack・global skill installは不要です。

```powershell
cd runtime
npm ci --ignore-scripts --no-audit --no-fund
cd ..
node runtime/dist/cli.js validate input/deck.json
node runtime/dist/cli.js render input/deck.json -o deck-rebuilt.pptx --no-git-ignore
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck-rebuilt.pptx -OutputDirectory render-rebuilt
```

原典sourceからbuildし直す場合はruntime/で`npx --no-install tsup`。元tsup.configとsrcを同梱しています。通常の制作ではbuilt CLIをそのまま使います。

input/deck.jsonを編集し、同じフォルダーのtheme.jsonがtheme bindingを解決します。PROMPT.txtはAI依頼文、NOTES.mdは講稿。完成deck.pptxは元CLIが指定パスへ直接書いたものです。

## 書体と条件

fonts/のZen Kaku Gothic NewとSpace GroteskをTTFから導入し、PowerPointを開き直してください。Zenは和文、Space Groteskは英数字。受け手にも導入します。公式Google Fonts未改変TTFとOFLを同梱し、WindowsFontsから抽出していません。書体そのものはPPTXへ埋め込んでいません。

原典MITのLICENSEを保持。runtimeが外部importする依存の原文条件はdependencies/に保持。node_modules、cache、秘密情報は配布しません。原作者の公式日本語版ではありません。

## 確認

元sourceのESM+DTS build、doctorのself-test、元CLI validate/render、PowerPoint必要な1回描画、主出力1枚が開くことのみ。全テスト、全ページ詳細目視、独立レビュー、native監査、ZIP再実行は未実施。QA.jsonに実際の状態を記録。
