# touying-typ/seaslidesの日本語制作

原典: https://github.com/touying-typ/seaslides/tree/dcde5bf6c6875b300e2999fc7766f369a13a67ac

原典TCS→source gate→html_compiler --all→visual gate。Windows receipt pathのみ派生修正。

原典のHTML lane、TCS、editorial-magazineテーマを使い、source gate→固有compiler --all→visual gateで生成する。Windowsのreceipt相対パスをPOSIX表記へ直す2ファイルの派生差分を保持し、validatorは変更しない。原典Motion・WebGL・ナビゲーションを保持し、日本語OFL書体と講稿を収録する。HTML表示はローカルHTTP経由。PPTXは今回の出力に含めない。

## 作例

- 読書会を月1回続けるには / 5枚 / html
- カタログ内の案内: repository.html?repo=touying-typ/seaslides
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=touying-typ/seaslides
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13 / Pillow / pypdf / python-pptx
- Node24 / 原典package-lockのnpm依存 / Chromium1223
- ローカルHTTPで表示

## 元の制作コマンド

    python tools/build_seaslides_repository_example.py

## 確認範囲

- AI画像生成/APIなし。手入力原稿を原典固有テーマとcompilerで生成。
- PPTXは生成していない。
- 汎用フォント依存を除くためNoto JPのOFLフォントを同梱。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
