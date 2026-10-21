# 帰属と変更

原典: HututuWorks/sci-diagram-pptx
https://github.com/HututuWorks/sci-diagram-pptx/tree/cc8f0030edf80eeab6e52849b8c39fe638466776

固定コミット: cc8f0030edf80eeab6e52849b8c39fe638466776
原典ライセンス: Apache-2.0。原文LICENSEをupstream/LICENSEに保持。取得した原典にNOTICEはない。

Studio Yebisuは原典の再構成用途を日本語で案内し、自作入力PNGを実入力にしたnative PPTX復元例を追加した。原典SKILL本文とportable templateの原本をupstream/に未改変で保持する。日本語SKILLと作例実装は非公式派生。PptxGenJS 4.0.1はMIT。Windowsのフォントファイルは同梱しない。

source/adjust_native_arrows.pyはStudio Yebisuによる局所補助（Python標準ライブラリ、Apache-2.0）。原典checker・renderer・templateとは別の処理で、生成後の3個のtriangle headのw/lenだけをlg/lgへ設定する。

R13の現行pass-04/build.mjsには、Studio YebisuによるSTORE形式限定のCRC/ZIP再構築処理を内包する（Apache-2.0派生）。source/adjust_native_arrows.pyは旧再生の履歴で、現行の引き渡しでは不要。原典checker・renderer・templateは変更していない。
