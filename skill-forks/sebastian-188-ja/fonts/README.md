# Noto Sans CJK JPの取得

字体バイナリはキットに含めない。公式 [notofonts/noto-cjk](https://github.com/notofonts/noto-cjk) の [Sans/OTF/Japanese](https://github.com/notofonts/noto-cjk/tree/main/Sans/OTF/Japanese) から `NotoSansCJKjp-Regular.otf` と `NotoSansCJKjp-Bold.otf` を取得し、使用環境へインストールする。未改変の公式ファイルを使い、OS付属字体を抽出しない。

サイト内では[既存の未改変字体ZIP](../../../downloads/fonts/notosanscjkjp.zip)も取得できる（Regular・BoldとOFL）。このリンクはサイト配置用で、fork ZIPを単独展開した環境では公式取得先を使う。

[SIL Open Font License 1.1原文](OFL.txt)を保持する。原典実装のfont stackはMicrosoft YaHeiを先頭、Noto Sans CJK JPを日本語fallbackとしている。YaHei、SimHei、PingFang SCをこのキットから提供するものではない。選択される字体によってSVG・PDFの組版が変わるため、変更時は使用環境で主要出力を確認する。
