# ConnorRX56/presentation-delivery-skillsの日本語制作

原典: https://github.com/ConnorRX56/presentation-delivery-skills/tree/06ddac077030c62f0118b225860cac46fbf658ea

原典HTML-first Path A → 原典DOM要素変換・寸法検査 → native PPTX / PDF

原典Visual Deck StudioのHTML-first Path A、960×540ptの4条件、無改変の変換・寸法・overflow検査とDOM要素変換を使う。原典deck_index.htmlの概覧・キー操作とPDF結合を保持する。明示HTTP入口、字体待ち、日本語ノート、Windows環境継承だけをadapterで補う。本文文字と図形はnative PPTX。HTML/PPTXの字間・太さ・br行間には差があり、pixel一致・動画・TTS・人の早期承認は主張しない。BIZ UDPGothicのOFL原本を同梱する。

## 作例

- 引き継ぎは、次の一手まで。 / 6枚 / pptx
- カタログ内の案内: repository.html?repo=ConnorRX56/presentation-delivery-skills
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=ConnorRX56/presentation-delivery-skills
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python3（標準ライブラリ）
- Node.js22以上 / npm / 初回公式Chromium取得
- PowerPoint描画: Windows / Microsoft PowerPoint / PowerShell7 / インストール済みBIZ UDPGothic

## 元の制作コマンド

    python source/reproduce.py --powerpoint

    python -m http.server 8000 --bind 127.0.0.1

## 確認範囲

- HTMLとPPTXでは字間・太さ・br行間が違う。pixel一致は主張しない。
- 本文はnative文字・図形。HTMLの概覧motionはPPTXへ移さない。
- この6枚のPath A出力のみ。動画・TTS・3方向Fallback・file URL・人の早期承認は未実施。
- PowerPointの受け取り先にBIZ UDPGothicが必要。OFL原本は同梱。
- 原典コードは保存し、HTTP入口と字体待ち・ノートだけを明示adapterで補う。
- 再生成したQAは確認前になる。人の正式採用と外部公開は未承認。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
