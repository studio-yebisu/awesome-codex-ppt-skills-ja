# YEBISU SLIDE STUDIO

**日本語でつくる、伝わるスライド。** Studio Yebisuが企画・編集・制作する、日本語のAIスライド制作プロジェクトです。

**[ウェブサイト](https://studio-yebisu.github.io/awesome-codex-ppt-skills-ja/)** · [使い方](../guide.html) · [出典と利用条件](../licenses.html) · [制作記録](制作記録.md)

カタログの翻訳を出発点に、日本語の作例、実行できる派生スキル、フォントの案内を独立して開発しています。原作者による公式日本語版・推奨ではありません。URLとリポジトリ名は既存のものを維持しています。

- 6つのオリジナルデッキ、計24枚。SVG・再生HTML・講稿・編集可能PPTXを収録。
- 作例を浮かぶプレイヤーで再生。用途で絞り込み、キー操作、講稿、プロンプトのコピー。
- MIT 3種、AGPL 1種の日本語派生スキルと、CC0の共通スキルを配布。
- Noto Sans JP、BIZ UDPGothic、Noto Serif JPの選び方と公式OFLの出典。
- PPT Master、Frontend Slides、Baoyu、Guizang、Slidev、Marp、reveal.js、PptxGenJSなどの固定コミットを確認。
- 従来の209件カタログと個別画像の帰属は継承。

## 作例とスキル

|用途|作例|派生スキル|利用条件|
|---|---|---|---|
|社内提案|[週次レポート](../examples/team-report/index.html)|[yebisu-pptx](../skills/yebisu-pptx/SKILL.md)|MIT|
|企画|[コーヒースタンド](../examples/local-coffee/index.html)|[yebisu-editorial-slides](../skills/yebisu-editorial-slides/SKILL.md)|AGPL-3.0-only|
|教材|[生成AIのしくみ](../examples/ai-classroom/index.html)|[yebisu-story-slides](../skills/yebisu-story-slides/SKILL.md)|MIT|
|技術・登壇|[AIの答えの検証](../examples/evidence-talk/index.html)|[yebisu-web-slides](../skills/yebisu-web-slides/SKILL.md)|MIT|
|製品説明|[プロダクト説明](../examples/product-story/index.html)|[yebisu-pptx](../skills/yebisu-pptx/SKILL.md)|MIT|
|動き|[動くタイポグラフィ](../examples/motion-manifesto/index.html)|[yebisu-web-slides](../skills/yebisu-web-slides/SKILL.md)|MIT|

まずは [yebisu-japanese-slides](../skills/yebisu-japanese-slides/SKILL.md) を使えます。Node.js 22以上を推奨し、SVG / HTML生成に追加ライブラリ・APIキーは不要です。

```text
node skills/yebisu-japanese-slides/scripts/render-deck.mjs skills/yebisu-japanese-slides/assets/example.json new-deck
```

同梱PPTX exporterはPptxGenJSを使います。各スキルフォルダで `npm install --ignore-scripts` してから利用してください。文字・図形・線は編集可能、自由形状pathはSVG画像です。既存PPTXの修復・データchart・tableの制作はこの簡易CLIの対応範囲外です。

## 開発

サイトは静的HTML/CSS/ES modulesで、ビルド不要です。

```text
python -m http.server 8847 --bind 127.0.0.1
node --test tests/content-contracts.test.mjs
python tools/verify_release.py
```

`data/decks.json` が作例の正本。`tools/make_examples.py` はその制作コード、`tools/build_site.mjs` はHTML/SVGの生成、`tools/package_skills.py` と `tools/package_downloads.py` は配布物を生成します。フォント再生成は `tools/build_fonts.py`（fontTools / brotliが必要）。

作例PPTXはOpenAI Artifact Toolで別途制作しています。PowerPointの実アプリでの表示確認は、パッケージ検査・レンダリング確認とは別です。HTMLの出現演出はPPTXに含めず、フォントは埋め込んでいません。上流プログラムの実行結果・品質保証・Opus 5.5による制作とは表示しません。

## ライセンスと出典

独自サイト・文章・作例・制作CLIはCC0-1.0を継続。派生スキルは各MIT / AGPLを継承し、元の著作権表示・原文・改修内容・対応範囲を同梱。Webフォントは各OFL。旧カタログの第三者画像には、各原典の条件が適用されます。ルートのCC0はこれらを再許諾しません。

AnthropicのPPTXスキルは改変・再配布を制限する記述があるためフォーク対象から除外しました。確認結果と原典URLのみ掲載し、スキル実装を収録していません。

原カタログ：[zhuyansen/awesome-codex-ppt-skills](https://github.com/zhuyansen/awesome-codex-ppt-skills)（CC0）。以下の一覧と原版の実測比較は2026年10月11日の取得内容を継承した記録です。現在の派生スキルの検証結果ではありません。

---
