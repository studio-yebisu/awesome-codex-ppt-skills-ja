# AIへ渡す日本語スライドの書体指示

見出し・本文・英数字・コードの役割を分け、同じ書体を漫然と並べない。日本語は意味の区切りで改行し、強い表紙と余白を作る。装飾書体は短い見出しに限る。Google FontsとNoto CJK公式リポジトリの固定commitから取得した未改変原配布物に、OFL原文を同梱。フォント単体販売をしない。

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

PowerPointでは使う書体を作成者と受け手の両方へ導入。Webでは配布元フォントを同梱し、font-faceで読ませる。未改変TTF/OTFとOFLを同じフォルダーに保持する。Noto Sans CJK JPは研究発表の取り込み3作例にも指定されている書体。環境だけにあった書体をコピーせず、公式配布のRegular/Boldを取得できる。
