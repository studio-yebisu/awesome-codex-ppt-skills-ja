# SVGの本文と図を編集可能PPTXへ変換する

原典は編集可能PPTXの生成・画像再構築・Brand/Style/Layout/Deckの再利用・nativeテンプレート編集・既存PPTXの強化を目的別の経路へ振り分ける。今回の作例はQuick Generateの直接SVG制作・検査・native変換を使う。

Quick GenerateのSVG契約へ顧客の関係図と候補地比較を作り、原典の検査・native変換を通す。内容・重み付き計算と編集可能性を確認する。

原典は [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master/tree/ca04346de145ed6462ddf34682848e71df5e20a2)、固定 commit `ca04346de145ed6462ddf34682848e71df5e20a2`。日本語派生であり公式翻訳ではない。

## 用意するもの

- Python / python-pptx / lxml / Pillow、原典PPT Masterのscriptsと契約資料。
- Windows / PowerPoint / PowerShell、公式BIZ UDPGothic。PDF由来RGBプレビューにはpypdfium2。

## 使い方

1. 決裁内容・仮定・数値と単位を固定する。
2. Quick GenerateのSVG・意味ID・境界とノートを作る。
3. 原典guard・checker・native変換器を順に実行する。
4. 全頁の表示と計算を確認し、入力またはSVGへ戻って修正する。

## この作例で確認する箇所

- **2頁・本文から関係図**：上の2顧客像から下の新店へ向く矢印と、さらに下の既存店の役割を読む。 伝える関係をSVGの文字と図形へ分け、native変換後も本文と図を編集可能にする。
- **3頁・同じ列で比較**：比較項目・重み・A/Bの5点評価を同じ行で比べる。帯と太字が各行の優位を示し、下段に81/82点と賃料を併記。 比較条件をそろえて図表化し、同じ意味ID付きSVGからnative文字・線・帯へ変換する。
- **4頁・仮定からの計算**：左の42.4万円と費用、右の計算式・59.2人/日、55人/日の赤字を照合。仮定と注記を読む。 数値と単位を入力に基づき計算し、計画値を実績として表示しない。

## 適用範囲と未実施

- 原典Quick Generate契約を使う日本語専用経路。Default Generate全工程、Brand workspace、手持ちPPTXテンプレート制作は未実施。
- 原典guard・checker・native変換器は無変更。現在のcheckerはerrors0、warnings8で、非PPT-safe字体などの助言を保持。
- SVGの比較表は編集可能な文字と線で、Officeのネイティブ表やデータ連動チャートではない。
- 数値・店名・計画は架空。採算の計算例で、投資や契約の承認、実績を示さない。
- BIZ UDPGothicへ明示変更。PowerPoint全8頁と実PDF字体を確認済み。修復版の独立再評価は未完了。

全頁を制作側が実画像で確認した。修復版の独立再評価・利用者の採用は未完了。検査の内容・現在のPPTX hashは `QA.json`、原典の保持範囲と変更は `PROVENANCE.json` を参照する。

入力と現在の生成器を含む。再実行は [REPRODUCE.md](REPRODUCE.md) を参照する。

## 同梱例の再実行

`example/REPRODUCE.md` に従う。
