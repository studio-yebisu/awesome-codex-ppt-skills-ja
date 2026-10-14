# 余白を買う

日帰りワークラウンジ「YOHAKU」の架空ブランド提案。6ページ。企画上の体験を示し、売上や利用実績は掲載していません。

## 制作方式

likaku/Mck-ppt-design-skill の固定原典DeckBuilderとMckEngineを使用。type/dataの入力JSONをDeckBuilderへ渡し、6つのlayout methodをEditorialEngineで上書きしています。原典coreのadd_text/add_rect/add_hlineとMckEngineの_ns/save、full_cleanupを直接使用。文字と図形は編集可能なネイティブPowerPointです。コンサルティング標準版式の単なる色替えや翻訳ではなく、明示的なレイアウト派生です。上流本体は改変していません。

## 再制作

配布ZIPはカタログのcacheや`.build`なしで使えます。Pythonに`python-pptx`と`lxml`を導入し、展開先のrootで実行します。原典runtimeは`upstream/`に同梱済みです。

```powershell
python -m pip install python-pptx lxml
python source/rebuild.py --input input/storyline.json --output deck-rebuilt.pptx
# Microsoft PowerPointがあるWindowsでPNG/PDFを描画する場合
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck-rebuilt.pptx -OutputDirectory render-rebuilt
```

原典入力はinput/storyline.json、AI依頼文はPROMPT.txt、生成コードはsource/に保持。描画にはMicrosoft PowerPointが必要です。PPTXに書体自体は埋め込んでいません。

## 書体を用意する

`fonts/`のZen Kaku Gothic New、Shippori Mincho、Space GroteskのTTFを右クリックしてインストールし、PowerPointを開き直してください。Zenは和文見出し・本文、Shipporiは明朝の文章、Space Groteskは英数字に使います。受け手にも3書体を導入します。親が公式Google Fontsから取得した未改変TTFと各OFL原文を同梱し、WindowsのFontsから抽出したものではありません。

## 確認範囲

PowerPointによる初回PNG/PDF描画、ページ数と主スライドが開くことのみを確認。全ページ詳細検査、原典S3/S4 gate、native ZIP監査、独立レビュー、配布ZIPからの再実行は未実施。QA.jsonに実際の状態を記録します。

## 条件

原典 Apache-2.0、Kaku Li (likaku) のLICENSEとNOTICEを保持。この例はStudio Yebisuの派生制作。原作者の公式日本語版でもMcKinseyの公式資料でもありません。書体の条件は各`fonts/<family>/OFL.txt`を参照してください。入力JSONからのZIP再実行は今回未実施です。
