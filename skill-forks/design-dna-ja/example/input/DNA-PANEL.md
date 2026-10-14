# 参考画像から抽出したDNAパネル

方向名: **紙と三原色の道具棚**。大きい和文と硬いグリッドを主役に、少ない言葉と意味を持つ幾何で運用の関係を示す。

参考は自作Akxan由来のnative PPTX表紙をPowerPointで描画したPNG。先に実画像を表示し、原本をreference/slide-01.pngへコピーしました。画像はスライド内容へ埋め込みません。

許容する特徴: 紙色・墨色・赤/紺/黄、左揃え、強い見出し階層、硬いエッジ、水平罫線、非対称、広い余白。
引き継がない内容: 元の展示企画の文章、固有の図形配置、元デッキの識別ラベル。人物・製品等の識別できる被写体はありません。道具の図は新しい依頼の台車・机・椅子から自作します。

| 固定パラメータ | 値 |
|---|---:|
| whitespace | 72 |
| information_density | 32 |
| image_weight | 48 |
| title_weight | 92 |
| chart_weight | 42 |
| text_density | 28 |
| formula_friendliness | 5 |
| grid_strictness | 95 |
| hierarchy_strength | 95 |
| motion_intensity | 22 |

数値は見た目の調整用の設計判断です。品質、信頼性、成果を測定したスコアではありません。
semantic tags: minimal85 / editorial91 / playful57 / serious72 / youthful58 / experimental65 / business42 / academic20 / tech12 / premium55 / emotional35 / trustworthy58。

原典の5層を抽出しました。

- Mood: 明快な編集感、紙と硬い幾何の軽い遊び。画面の印象であり、運用の信頼性の実証ではない。
- Composition: 左揃えと非対称。見出しを大きく置き、主図と余白を残す。各頁の役割に合わせて構図を変える。
- Visual: 背景#f4f0e8、墨#1a1a1a、赤#d62828、紺#003049、黄#ffd60a。丸角・影・グラデーションを使わない。Zen Kaku Black、BIZ UDPMincho、Manropeを役割別に。
- Content Strategy: 1頁1つの運用上の問い。道具図、担当の役割、借りる/使う/返す、短い状態表、利用案内を別頁へ。長い規程や実績グラフには向かない。
- Presentation: 話し手の説明に合わせた短い切替え。静止参考から動きは抽出不能なので、関係線・担当・状態の順に出す動きは新作で定義。

実行条件: 1920×1080固定stageを全体で均等縮小。左右120px、24px以上、navigationは940px以降へ予約。CJK見出しは字間0・安全な行高。区画ごとにsurface/ink対を持ち、数値layout_box_budgetで文字高と余白を確保する。元のNode guardがP0を出したら仕様から修正し、隠しoverflowやz-indexで欠けを隠さない。

向く用途: 短い企画説明、使い方、少数の状態を示す表。
リスク: 長い注意文・多数の予約・多数の細かいデータを同じ頁へ載せること。今回は小さい状態表を1頁へ限定する。

現行の自律制作指示により、原典のDNA/要件/画像意図確認ゲートをこの記録へ置換して進めます。原典の未変更SKILLは保持します。確認回答を受けたとは記録せず、canonical design-profilesへの保存も行いません。input/design-dna.jsonは今回の再生成用active candidateです。
