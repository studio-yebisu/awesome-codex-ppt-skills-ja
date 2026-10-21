# 依存と条件

原典 requirements.txt: python-pptx (MIT), lxml (BSDとlibxml2/libxsltの条件), fontTools (MIT), Playwright (Apache-2.0), Pillow (HPND)。任意のpdf2image (MIT)、pywin32 (PSF系)。Chromiumには第三者ライセンスが含まれます。実際の条件は各配布物のLICENSE/NOTICEを参照。依存バイナリ・venv・ブラウザcacheはZIPに含めません。使用フォント原TTFとSIL OFLはfonts/へ同梱。Manropeは変換用cacheに静的instanceを作り、PPTX内部のサブセットは原典処理で生成する方式ですが、今回の配布PPTXは原典 --no-embed-fonts を使用。原典の埋込版がPowerPoint COMで開かなかったためです。配布するTTFは未改変原配布物です。
