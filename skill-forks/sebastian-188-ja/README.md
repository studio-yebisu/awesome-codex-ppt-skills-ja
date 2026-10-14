# Swiss SVG・日本語制作キット

受領作例「AIに任せる前の設計図」（架空例・7枚）のSVGソースと、日本語で使うための手順を配布する。[SKILL.md](SKILL.md)から始める。

- `input/`：依頼と入力データ。`PROMPT.txt`：制作依頼。
- `.ppt-session/`：構成とSwiss styleの設計情報。
- `svg/`：編集できる7枚のSVG正本。
- `source/build.py`：受領したSVG著述・Inkscape PDF化・PyMuPDF PNG化の補助コード。
- `source/upstream/`：使用した原典SKILL・commands・specs・Swiss styleの未変更原本とMIT LICENSE。
- `source/japanese-original-*`：受領した日本語案内の原本。`source/japanese-fork.diff`：配置整理の差分。
- `SOURCE.json`：固定commit、実装差分、字体と取り込み範囲。

PDFは固定レイアウトで、編集はSVGソースで行う。PPTXのネイティブ図形変換は未確認。完成PDF・PNGはこのソースキットとは別にサイトで配布する。

再生成する場合はPython 3、Inkscape CLI、PyMuPDF、および[外部取得するNoto Sans CJK JP](fonts/README.md)を準備し、キットのルートで `python source/build.py` を実行する。`build.py`は7枚のSVGを書き直す。SVGを手編集した場合はそのファイルをInkscapeで直接PDF出力する。`render/`はPNG出力先として用意してある。

原典の任意Node exporterは受領作例では使っていない。原典の完全一式が必要な場合は[固定commit](https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb)から取得する。

この取り込みでは資料の再生成・追加QAを実施せず、受領した生成方法と確認記録を保存した。原典は[MIT](LICENSE)、字体は[SIL OFL](fonts/OFL.txt)。字体ファイルは含めていない。
