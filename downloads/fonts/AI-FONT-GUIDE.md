# AIへ渡す日本語スライドの書体指示

30ファミリーを用途別の4セットと個別ZIPで配布しています。従来の `yebisu-oss-font-kit.zip` は初期10ファミリーの互換セットです。

見出し・本文・英数字・コードの役割を分けます。日本語は意味の区切りで改行し、装飾書体は短い見出しに使います。Google FontsとNoto CJK公式リポジトリの固定commitから取得した未改変TTF/OTFに、OFL原文を同梱しています。

## 用途別セット

- [日本語ゴシック・丸ゴシック（8ファミリー）](yebisu-japanese-sans.zip)
- [日本語明朝（5ファミリー）](yebisu-japanese-serif.zip)
- [日本語の見出し・手書き調（4ファミリー）](yebisu-japanese-display.zip)
- [欧文・数字・コード（13ファミリー）](yebisu-latin-code.zip)

## 誌面とブランド

見出し: Shippori Mincho / 本文: Zen Kaku Gothic New / 英数字: Manrope

アイボリーと墨黒を基調に、赤橙を一点。明朝の大見出しと短い本文、大きな余白、縦横のグリッドで誌面を作る。

## 夜とモーション

見出し: Zen Kaku Gothic New / 本文: Zen Kaku Gothic New / 英数字: Space Grotesk

墨紺に蛍光ライム。短い見出しを大きく置き、SVG図形と段階表示で視線を導く。動きは220〜450ms、ページごとに一つの主張。

## やさしい教材

見出し: Zen Maru Gothic / 本文: Zen Kaku Gothic New / 英数字: Manrope

丸ゴシックは見出しに、端正なゴシックは本文に。図解と余白を優先し、読み手が次にすることを一つずつ伝える。

## 強い表紙

見出し: Dela Gothic One / 本文: Zen Kaku Gothic New / 英数字: Space Grotesk

Delaは短い見出しのみ。大胆な一色と大きな文字・図形で表紙を作る。本文に太い装飾書体を使わず、ページで構図を変える。

## 業務と数字

見出し: BIZ UDPGothic / 本文: BIZ UDPGothic / 英数字: Manrope

BIZ UDPGothicの太字で結論、標準ウェイトで説明を組む。数字の単位と比較対象を明記し、表は罫線を減らして列を揃える。白地と墨紺に赤橙を一点。見出しを大きく、本文は短い段落にする。

## 説明と教材

見出し: BIZ UDPMincho / 本文: BIZ UDPGothic / 英数字: Manrope

BIZ UDPMinchoの太字で題名、BIZ UDPGothicで説明と図のラベルを組む。紙色と深緑を基調に、赤橙は注目する量だけに使う。式・図・説明を対応させ、学習用の設定と実測値を区別する。

## 研究と図表

見出し: Noto Sans CJK JP / 本文: Noto Sans CJK JP / 英数字: Manrope

Noto Sans CJK JPの太字で主張、標準ウェイトで図のラベルと説明を組む。白地と墨紺を基調に、青は比較する系列だけに使う。図・式・出典を近くに置き、単位と仮定を明記する。Noto Sans JPとNoto Sans CJK JPはフォント名が異なるため、原稿とPPTXに指定した名前を揃える。

## コードと技術発表

見出し: BIZ UDPMincho / 本文: BIZ UDPGothic / 英数字: Manrope / コード: JetBrains Mono

明朝の短い主張、ゴシックの日本語説明、JetBrains Monoのコードと変数を使い分ける。白地と青を基調に、コード・図・実行結果を順に見せる。コードは重要な数行に絞り、字幅を揃える。合字で演算子を省略せず、読み上げる記号を見せる。JetBrains Monoには日本語を任せず、コード内の日本語コメントにはBIZ UDPGothicをフォールバックする。学習用データと実測値を区別し、実行していないコードを結果として扱わない。

## 業務・UI説明

見出し: IBM Plex Sans JP / 本文: IBM Plex Sans JP / 英数字: Inter

太字で結論、標準の太さで説明を組む。UI名・操作・結果を近くに置く。数値の桁と単位を揃える。

## 学術・長い説明

見出し: Noto Serif JP / 本文: Noto Sans JP / 英数字: Source Serif 4

明朝の見出しとゴシックの図ラベルを使い分ける。引用・変数・単位を原典と揃える。欧文書体は日本語へ流用しない。

## 子ども向け教材

見出し: Kiwi Maru / 本文: M PLUS 1 / 英数字: Nunito

丸みのあるKiwi Maruを短い見出しに使い、説明はM PLUS 1にする。問題文・図・答えを分け、同じ文字を同じ役割で使う。

## 手書き調の説明

見出し: Klee One / 本文: BIZ UDPGothic / 英数字: Source Sans 3

手書き調は短い題名と書き込みだけに使う。長い本文や表はBIZ UDPGothicで組む。小さい文字へ装飾書体を使わない。

## 文化・出版

見出し: Zen Old Mincho / 本文: Noto Sans JP / 英数字: Libre Baskerville

和文題名は明朝、本文と図の説明はゴシックで組む。欧文の引用はLibre Baskerville。見出しを改行するときは意味の区切りに合わせる。

## コード・端末出力

見出し: IBM Plex Sans JP / 本文: IBM Plex Sans JP / 英数字: IBM Plex Sans / コード: Fira Code

コードと変数はFira Code、日本語説明はIBM Plex Sans JP。演算子を説明するときはコードの合字を無効にする。日本語コメントに和文フォールバックを指定する。

## 数値・比較表

見出し: Noto Sans JP / 本文: BIZ UDPGothic / 英数字: Barlow Condensed

大きな数値はBarlow Condensed、和文ラベルと表の本文はBIZ UDPGothic。幅の狭い書体を理由に情報を詰め込まない。桁と単位を揃える。

PowerPointでは使う書体を作成者と受け手の両方へ導入。Webでは配布元フォントを同梱し、font-faceで読ませる。未改変TTF/OTFとOFLを同じフォルダーに保持する。Noto Sans CJK JPは研究発表の取り込み3作例にも指定されている書体。環境だけにあった書体をコピーせず、公式配布のRegular/Boldを取得できる。
