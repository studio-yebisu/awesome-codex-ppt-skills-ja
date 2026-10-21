# 自分の科学模式図を復元する

判読可能な元画像と、復元したいパネル・保持する文言や関係をAIへ渡す。完成した編集元がなくても、意味を担う文字・図形・線を別々に修正できるPPTXへ復元するための入口。

> 添付した科学模式図の指定パネルを、元の文言・式・包含・矢印の関係を保つ編集可能なPPTX1枚へ復元してください。読めない文字や関係は補作せず知らせてください。原典のReconstructionと使用runtimeの参照を読み、元画像・実際に実行したbuild.mjs・PPTXを渡してください。使ったruntimeと採用pass、検査、近似・raster inset・未確認事項も記してください。

1. [固定原典のSKILL](upstream/SKILL.md) と [Reconstruction](upstream/references/reconstruction.md) を読む。定量グラフや業務図など適用外なら、その図へこの方式を当てはめない。混在図では対象の模式図パネルだけを指定する。
2. 元の画像を保管し、各文字・図・関係の所有をnativeかrasterの一方へ割り当てる。写真・実験画像・複合小図は必要な範囲のreplaceable insetとし、中の文字や矢印を二重に描かない。読めない証拠をOCR推測や描き直しで補わない。
3. 利用できるruntimeを一つ選び、その参照とprobeに従う。PptxGenJSの場合は準備済みホストruntimeの子フォルダーを作業先にし、そこからlocked 4.0.xが解決できることを確かめる。必要依存がない状態で制作中にinstallせず、準備不足を返す。
4. 新しい作業先のpass-01へ元画像の同一バイトコピーを置く。原典の選んだruntime雛形から、その画像専用のNODES・EDGES・INSETSと座標変換を持つbuild.mjsを作る。保存例の4箱・4関係を新しい図の固定ルールにしない。
5. そのbuild.mjsを実行し、原典checkerと選択rendererで1枚のPPTXを確認する。文言・包含・線の意味・方向・欠落・重なりを元画像と比べる。必要なら全blockerを一括してpass-02へ修正し、2回目の結果で納品または残る問題を報告する。

既存PPTXのRepairは [repair.md](upstream/references/repair.md)、変更しないInspectionは [inspection.md](upstream/references/inspection.md) を使う。PptxGenJSで元のPPTXを保ったRepairは行わない。新規復元への変更が必要なら、その変更の判断を受けてから進む。

`example/source/reproduce.py` は、保存した水循環の例を同じ入力から再生成するもの。任意の画像を受け取る自動変換器ではない。依存の配置・CWD・上書きの扱いは [example/REPRODUCE.md](example/REPRODUCE.md) を確認する。

保存例の追加確認: [複合例の入力・出力・再生条件](example/complex-example/README.md)。入れ子と線の意味、nativeとrasterの分担を示す合成概念図で、数式や実験写真の実証ではない。
