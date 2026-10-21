"""Source-linked Japanese descriptions of what each showcased skill changes.

This is editorial data, not an automatic visual score or a claim that every
upstream capability has been exercised. Page indices are zero based.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROWS = []
REMOTE_HASH_CHECKS = {}
SOURCE_LOCKS = {}


def add(case_id, name, problem, change, input_, output, when, principle,
        summary, index, inspect, features, limits, edit):
    ROWS.append(dict(case_id=case_id, name=name, problem=problem, change=change,
                     input=input_, output=output, when_to_use=when,
                     principle=principle, summary=summary, index=index,
                     inspect=inspect, features=features.split(" / "),
                     limits=limits.split(" / "), edit=edit))


add("sol-motion-showcase", "原稿を動き付きの単一HTMLへ",
    "原稿だけでは、発表の見せる順番や画面構成を確かめにくい。",
    "話題と原稿を、16:9を保つWebスライドと段階表示に変える。",
    "発表の題材・読者・原稿・参考スタイル", "単一HTMLの発表資料",
    "アプリのインストールなしで、動きのある発表をブラウザーで見せたいとき。",
    "固定16:9ステージ、単一HTML、視覚プレビューによる方向決定、段階表示。",
    "図書館企画に原典の固定ステージ・ページ制御・段階表示を適用。選書タブは作例の追加実装。",
    3, "選書タブを切り替え、説明と表示の対応を見る。前後の移動では文字が順に出る。",
    "固定ステージ / 段階表示 / 単一HTML",
    "PPTXからの変換はこの作例では未実施。 / 選書タブ自体は原典の標準機能ではない。",
    "input/BRIEF.mdを自分の原稿へ替え、見せたい順番とスタイルを指定する。")
add("mck-native-showcase", "図・表・工程を部品で作る",
    "一枚ずつ図形を配置すると、書式や間隔をそろえる作業が繰り返しになる。",
    "原稿をMckEngineの部品で構成し、文字と図形を編集できるPPTXにする。",
    "資料の目的・原稿・ページ構成", "文字と図形を編集できるPPTX",
    "PowerPointで後から文言や図形を直す、書式のそろった資料を作りたいとき。",
    "MckEngineの高水準部品APIと共通の文字・間隔ルールでPowerPointを生成する。",
    "原典のcover・donut・data_table・timelineへ30ファミリーの実集計と工程を渡し、4ページを生成。原典S3/S4検査を実行した。",
    1, "分類別の実数12・8・4・3・3と、図形・凡例の色の対応を見る。PPTXでは文字と弧を個別に編集できる。",
    "MckEngine高水準API / 図形によるドーナツ / 文字と罫線の表 / 時系列図",
    "原典67メソッド中4つを使用。 / 表とドーナツは編集可能な文字・図形。Officeのデータ連動表・チャートではない。",
    "inputの原稿と色・書体設定を替え、必要な部品APIでページを構成する。")
add("sci-diagram-reconstruction", "科学図の画像を編集可能なPPTXへ",
    "科学図を画像で貼ると、ラベル・領域・矢印を個別に直せない。",
    "提供された科学図の意味と接続関係を保ち、編集できるPowerPointの図へ再構築する。",
    "復元したい科学模式図PNGと読めるラベル", "図形・ラベル・矢印を編集できるPPTXと制作ソース",
    "研究の概念図や機構図を、意味を変えず編集可能にしたいとき。",
    "意味、領域の入れ子、接続関係、編集性を優先し、見た目の微差を追い過ぎない。",
    "先に作成した科学模式図PNGを実入力にし、同じ日本語・4箱・4本の矢印を編集可能な文字・図形・線に復元。元画像と出力を並べて確認できる。",
    0, "元画像と復元結果で、4個の箱・日本語ラベル・矢印の向きが一致するか見る。配布PPTXではラベルを個別に変更できる。",
    "画像からの再構築 / ラベルと矢印 / native図形 / 公式PptxGenJS雛形",
    "科学図の新規考案やデザイン改善を示した例ではない。 / 複雑な顕微鏡写真や統計グラフの復元は未実施。 / このPptxGenJS経路はReconstruction専用。既存PPTXのRepairはartifact runtimeが必要で、この作例では未実施。",
    "元の科学図と正確なラベルを渡し、変更してよい範囲を指定する。")
add("html-editable-showcase", "HTMLを編集可能なPPTXへ変換",
    "HTML資料しかないと、PowerPointで提出・修正できない。",
    "HTMLの文字と単純な図形を測り、編集可能なPPTXに変換する。",
    "既存のHTMLスライド", "編集可能なPPTX。複雑な装飾は画像になる場合がある",
    "ブラウザー用に作った資料を、PowerPointで配布・修正したいとき。",
    "ブラウザーで位置を測定し、文字はベクター優先、表現できない装飾は画像で保つ。",
    "焙煎所のHTMLを原典convert.pyでPPTX化。日本語フォントを局所登録し、--no-embed-fontsを使用した。",
    2, "大きな文字と配色見本の位置を元HTMLと比べる。文字の編集性はPPTXで確認する。",
    "DOM実測 / 文字の再構築 / 日本語フォント対応",
    "全CSSがPowerPointの図形へ変換されるわけではない。 / この作例はフォントをPPTXに埋め込んでいない。",
    "変換元HTMLと使用フォントを用意し、原典convert.pyへ渡す。")
add("hand-drawn-showcase", "章扉に手描き図版を付ける",
    "章の切り替わりが本文ページと同じ見た目で、話題の区切りを伝えにくい。",
    "章名を、大きな見出し・淡い背景・手描き図版の区切りページにする。",
    "章名・章の意味・使う色", "章扉中心のPPTX",
    "研修や発表の章の区切りを、短い見出しとイラストで示したいとき。",
    "太い黒線の手描き図版、左下の章名、淡い全面背景という章扉の組み方。",
    "表紙と4章の区切りに、原典SVGライブラリーとPptxGenJS雛形を使用。本文資料の制作例ではない。",
    2, "短い章名と手描き図版の組合せを見る。文章を読むページと章の区切りを分けられる。",
    "章扉 / 原典SVG / PptxGenJS雛形",
    "表・グラフ・長い本文を含む業務資料全体は未実施。 / イラストはSVG画像として配置している。",
    "章の数・章名・章ごとの意味を書き、対応する原典図版を選ぶ。")
add("slidespeak-showcase", "ブリーフから専用のWeb資料を作る",
    "既成テーマを選ぶだけでは、ブランドの色・書体・ページ構成が合わない。",
    "資料の内容とブランドの指定から、専用トークンと版式を持つHTML資料を生成する。",
    "内容のブリーフ・ブランドや見た目の指定", "1920×1080のHTMLスライド",
    "自社や店舗の色・書体を持つ資料を、Webで見せたいとき。",
    "テーマ一覧から選ぶ方式ではなく、ブリーフから見た目を設計して原典エンジンへ渡す。",
    "書店企画の緑・明朝見出し・版式を個別設計し、原典エンジンで6ページをHTML化した。",
    3, "緑を使う役割と、見出し・本文の書体の使い分けを見る。ページを移動して同じ規則が続くか確認する。",
    "専用スタイル定義 / 版式への内容配置 / 原典HTMLエンジン",
    "外部画像APIは使っていない。 / 原典の全チャート・表機能はこの作例では未使用。",
    "自分のブリーフとブランド指定を用意し、色・書体・版式を先に決める。")
add("pptwise-showcase", "意味付きJSONからPPTXを作る",
    "原稿と図形の配置を同時に決めると、内容を変えるたびに配置を直す必要がある。",
    "ページの役割と部品をJSONで記述し、テーマに沿う編集可能PPTXへ変換する。",
    "原稿・ページの役割・型付き部品を記したJSON", "編集可能なPPTX",
    "内容データと見た目を分け、同じテーマで資料を更新したいとき。",
    "意図→話の構成→テーマ→kind付きspec→内容→renderの順に分離する。",
    "作業拠点の提案をv5スキーマで記述し、派生テーマと原典部品でPPTX化した。",
    3, "人の関係を表す図と短い説明の対応を見る。部品の内容はinput/deck.jsonから変更できる。",
    "型付き部品 / JSON検証 / テーマによる共通書式",
    "JSONとCLIの環境が必要。 / この作例は原典テーマそのままではなく派生テーマを使用。",
    "input/deck.jsonのページ役割と内容を替え、検証してから原典renderを実行する。")
add("aham-showcase", "資料を論点と版式に分けて組む",
    "短い依頼をすぐにスライド化すると、論点やページごとの役割が決まらない。",
    "材料を論点・話の順序・版式へ分け、編集可能なPPTXにまとめる。",
    "依頼・説明材料・読者・視覚テーマ", "編集可能なPPTX",
    "説明材料から、図解・工程・実施案を持つ業務資料を作りたいとき。",
    "材料解析から論点、構成、版式、ページ制作へ進む。固定layoutIDの座標を使用する。",
    "朝のワークショップ案4ページでSPC/E-03/E-04/A-90の原典SVG関数と変換器を使用。",
    2, "作業を始めるまでの手順と、各段階の短い説明の関係を見る。",
    "原典layoutID / SVG図解 / 原典native変換器",
    "全8段階のユーザー確認を完走した実証ではない。 / 原典の全チャート部品は未使用。",
    "説明材料から論点を決め、関係に合うlayoutIDへ内容を入れる。")
add("agent-slides-showcase", "既存テンプレートの規則でPPTXを組む",
    "会社のテンプレートを渡しても、既存の配置・書式ルールが制作に引き継がれない。",
    "テンプレートから規則を抽出し、意図と編集操作の計画からPPTXを生成する。",
    "既存PPTXテンプレート・説明の目的・内容", "テンプレート規則に沿う編集可能PPTX",
    "手持ちの会社用テンプレートを使って資料を増やしたいとき。",
    "slides-extractのテンプレート契約を前提に、計画とnative編集操作を検証して描画する。",
    "規則抽出→事前確認→操作計画→描画を通し、土曜日の作業場企画を1ページで制作。",
    0, "この作例は1ページ。企画の目的・内容・参加方法がどう配置されているかを見る。",
    "テンプレート規則の抽出 / 編集操作の事前確認 / native生成",
    "複数ページを通じた構成は未実証。 / この作例に内部ページはなく、1ページ目を証拠にする。",
    "テンプレートを抽出し、input/slides.jsonへ目的とページ内容を記す。")
add("slidefly-showcase", "同じ図形をページ間で動かす",
    "ページが切り替わるたびに図形が消えると、同じ対象がどう変わったか追いにくい。",
    "同じ名前の図形を保持し、位置・大きさ・色を変えながらページをつなぐ。",
    "原稿・ページごとの図形と位置・スタイル", "単一HTMLと原典exporterによるPPTX",
    "同じ対象の移動や変化を、ページの切り替えで説明したいとき。",
    "共通ステージ上のactorを消さず、次ページのposeへ移動させる。",
    "散歩企画で原典morph engineとactor/poseを使用し、HTMLとPPTXを保存した。",
    2, "前後へ移動して、同じ図形が次の位置へ移ることを見る。静止画だけでは動きは確認できない。",
    "persistent actor / pose間の移動 / 単一HTML",
    "HTMLとPPTXの動きの完全な同等性はこの説明では保証しない。 / 85スタイル全ての比較は未実施。",
    "隣接ページで同じ対象を何として残すか決め、名前と位置を指定する。")
add("soil-teaching-showcase", "教材を理解の順番で段階表示する",
    "定義・例・練習を一度に見せると、学習者が何から考えるか分かりにくい。",
    "教材をページごとの学習上の役割へ分け、問い・図・答えを順に見せる。",
    "授業内容・学習目標・ページ計画", "オフラインHTML教材。この作例はMode C",
    "割合などの考え方を、問いと図を使って説明したいとき。",
    "先に文章だけのページ計画を作り、SOILの学習上の役割に沿って表示を組む。",
    "割合の6ページ教材をMode Cで制作。同じ6個でも全体が違えば割合が変わる比較と、計算・練習を使用。",
    1, "同じ6個を異なる全体と比べる図を見る。進む操作で説明が段階的に出る。",
    "学習上のページ役割 / 比較図 / 段階表示",
    "学習効果を測定した実験ではない。 / 編集可能PPTXのMode Bや画像版Mode Aは未実施。",
    "学習目標と例題を書き、問い・説明・練習のページ計画を作る。")
add("beamer-showcase", "数式と図をTeXで組版する",
    "数式と図を別々に作ると、本文との書式や修正方法がそろわない。",
    "原稿・数式・TikZ図をTeXにまとめ、再コンパイルできるPDF発表資料にする。",
    "発表原稿・数式・図の内容", "TeXソースとPDF",
    "数式や機構図を含む発表を、TeXで保守したいとき。",
    "原稿の順序を尊重し、Beamerテーマ内で数式と図を組版して実表示を確認する。",
    "待ち行列の説明5ページをWarm Editorialで制作。日本語書体を追加し、TikZ図と数式をPDF化した。",
    2, "待ち時間の式と変数の説明が同じページにまとまることを見る。",
    "Beamer / TeX数式 / TikZ図",
    "PowerPoint用の編集可能PPTXではない。 / 日本語書体を加えた派生設定を使用。",
    "TeXの原稿・数式・TikZ図を自分の内容へ替え、PDFを再コンパイルする。")
add("native-math-showcase", "PowerPoint内で直せる数式を作る",
    "数式を画像で貼ると、変数や分母をPowerPointで変更できない。",
    "数式をOMML形式でPPTXへ入れ、本文・図と一緒に編集できる教材にする。",
    "学術原稿・数式・説明図", "数式を含む編集可能PPTX",
    "PowerPointを使って数式のある講義や研究資料を後から修正したいとき。",
    "PptxGenJSで本文を組み、原則OMMLでnative数式を入れる。必要時のみ画像へ切り替える。",
    "平均・分散・標準偏差を5ページで説明。原典render_latexとinject_ommlで数式を注入した。",
    2, "偏差の二乗と分散の式を図と対応させて見る。OMML編集は配布PPTXで確認する。",
    "OMML数式 / 原典Sandwichテーマ / PowerPoint実描画",
    "プレビュー画像だけでは数式の編集性は分からない。 / 論文からの図抽出はこの作例では未実施。",
    "原稿とformulas.jsonを替え、OMML注入まで実行してPowerPointで式を開く。")
add("thesis-defense-showcase", "論文と既存テンプレートから発表を組む",
    "論文を要約するだけでは、指定テンプレートの書式や研究の根拠が保たれない。",
    "論文の図・本文を読み、手持ちのPPTXを複製して研究発表へ組み替える。",
    "論文PDF/TeX・図表・既存PPTXテンプレート", "指定書式に沿う編集可能PPTX",
    "大学・研究室のテンプレートを使って卒論・修論発表を作りたいとき。",
    "論文の実ソースとテンプレートを正本にし、既存スライドのnative要素を複製・置換する。",
    "仮想の通学経路計画6ページを原典の無地テンプレートとCOM複製helperで制作。既存論文の要約例ではない。",
    3, "経路候補を表で比べ、前ページのモデルと次ページの仮想試算へつなぐ構成を見る。",
    "テンプレート複製 / 書式を保持した置換 / native表",
    "提供論文からの図表抽出や大学テンプレートの忠実な再利用は未実証。 / COMの全機能にはWindows版PowerPointが必要。",
    "論文・使用可能な図表・指定テンプレートをそろえ、原典helperで複製して内容を置換する。")
add("sebastian-207", "原稿を選んだデザイン規則でPPTX化",
    "同じ原稿でも、実行方式・図の目的・書式を決めずに作るとページ間で設計がぶれる。",
    "原稿に合う制作方式とデザイン規則を選び、編集可能なPPTXへまとめる。",
    "原稿・参考スタイル・図版の計画", "編集可能なPPTX。この作例はnative_pptx方式",
    "文字・図形を直せる資料を、選んだデザイン規則で統一したいとき。",
    "template/native/HTML/image-firstの方式を先に選び、実行可能なdesign-systemで組む。",
    "書店文化企画8ページを原典native生成器とeditorial-inkで制作。表紙にAI画像、本文・工程にnative要素を使用。",
    4, "街の記録が一冊になる工程を、短いラベルと順序で示した部分を見る。",
    "原典native生成器 / editorial-ink / 図版と文字の分離",
    "原典の全4方式を比較した作例ではない。 / 固定中国語ラベルや言語設定を日本語へ変更している。",
    "原稿と図版の目的を整理し、spec_lock.jsonとslides_plan.jsonを自分の内容へ替える。")
add("sebastian-208", "論文をノート付きの画像PPTXへ",
    "研究内容を全ページ画像で見せても、根拠と話者ノートが切れると発表に使いにくい。",
    "論文の内容をページ別に整理し、全ページを画像生成して話者ノート付きPPTXへ包装する。",
    "論文・報告書・原稿・各ページの根拠とノート", "各ページが一枚の画像になったPPTXと話者ノート",
    "図版を含む一貫した画像主体の研究発表を作り、ノートと一緒に配布したいとき。",
    "画像を各ページの正本とし、原典包装スクリプトで一ページ一画像と対応ノートを保持する。",
    "架空の空間研究提案11ページを実画像生成し、原典スクリプトでノートを付けた。論文の根拠を抽出する機能は実証していない。",
    5, "観察・聞き取り・記録の三つを、同じ視覚規則で整理したページを見る。",
    "全ページ画像生成 / スタイル契約 / 話者ノート付き包装",
    "原論文の要約・根拠対応は未実施。 / 本文や図形は画像内で、個別には編集できない。",
    "論文と図表の利用条件をそろえ、ページ別の主張・根拠・正確なコピー・ノートを書く。")
add("sebastian-192", "複数スタイルを比べて画像資料を作る",
    "完成後に見た目を決め直すと、全ページの画像を作り直すことになる。",
    "同じ内容を四つのスタイルで試し、決めた方向で各ページを画像生成する。",
    "書籍・PDF・原稿・発表条件", "画像主体のPPTX。編集可能への再構築は別工程",
    "空間や構造を画像で説明する資料で、制作前に作風を比べたいとき。",
    "内容を先に整理し、四つの独立した作風候補から方向を決めて逐頁生成する。",
    "日陰の空間計画を4スタイルで比較し、白い模型案を選んで8ページを画像生成した。",
    4, "座る高さからの空間表現を見る。同じ模型表現が他ページの断面や計画図にも続く。",
    "4スタイル比較 / ページ別画像生成 / 模型・断面表現",
    "編集可能PPTXへの再構築は未実施。 / 最終包装と検査には独立した最小実装を使用した。",
    "同じ内容の4スタイル案を比較し、選んだ案の規則を全ページの画像指示へ渡す。")
add("ppt-agent-showcase", "内容に合う版式でHTMLからPPTXへ",
    "同じカード型を全ページに使うと、関係・順序・工程の違いが伝わらない。",
    "内容の関係に合わせたHTML版式を作り、文字・図形を持つPPTXへ変換する。",
    "説明材料・読者・ページ構成・選んだスタイル", "HTMLと編集可能PPTX",
    "内容を整理してからデザインし、Web版とPowerPoint版を作りたいとき。",
    "内容の計画と設計を分け、各ページの情報に合わせて版式を選ぶ。",
    "展示企画5ページを原典Bauhaus Blockの実mockで組み、原典DOM→SVG→PPTX変換を使用。",
    2, "入口から見終わるまでの順序を、三原色の幾何図形と短い説明で示した部分を見る。",
    "Bauhaus Block / 内容別版式 / 原典DOM・SVG変換",
    "外部調査を実施した企画ではない。 / 原典の全スタイルや画像生成方式は未実施。",
    "各ページの目的と内容を決め、関係図・工程など内容に合うmockへ入れる。")
add("presentation-skill-showcase", "説明の役割に合わせて図表を選ぶ",
    "情報をすべて箇条書きにすると、順序・比較・担当・期限の関係が読み取れない。",
    "原稿をページの役割へ分け、フロー・時系列・表・比較で構成する。",
    "原稿・数値・図の元データ・発表の目的", "再生成できる編集可能PPTX",
    "業務・研究・提案などの内容を、必要な関係が分かる図表にしたいとき。",
    "内容からページ構造を選び、outlineと原典ビルダーを正本にして描画・修正する。",
    "仕事の引き継ぎ6ページにOperating Gridの規則を適用し、フロー・期限表・判断条件を原典部品で制作。",
    3, "期限と状態を同じ表に並べ、次に確認するものを探せることを見る。",
    "outline駆動 / 役割別版式 / native表と図解",
    "すべての分野別スタイルを実証したものではない。 / 実在の業務成果を測定した資料ではない。",
    "原稿をoutlineへ分け、順序・比較・期限など説明したい関係に合う版式を選ぶ。")
add("aws-html-showcase", "既存PPTXを動き付きHTMLへ",
    "既存PPTXをWebで見せたいが、文字・ノート・図の関係を手で写し直したくない。",
    "PPTXから文字・画像・ノートを抽出し、Webの図形や段階表示へ組み替える。",
    "既存PPTXまたは新規の発表原稿", "ブラウザーで再生するHTML",
    "既存PowerPointを、ブラウザーで配布・再生する発表へ移したいとき。",
    "PPT変換では原典extract-pptx.pyで内容を抽出し、選んだHTMLスタイルに再構成する。",
    "既存の展示企画PPTX5ページから抽出し、図形座標の補助変換と原典Neon制御・SVG演出でHTML化。",
    2, "元PPTXと同じ展示の順序図を、HTML側で文字・線の動きとともに見る。",
    "原典PPTX抽出 / SVG再構成 / 段階表示",
    "座標の再現には作例専用のOOXML補助変換を使用。 / AWS構成図やdraw.io連携はこの作例では未実施。",
    "変換元PPTXを指定し、原典抽出結果と元ページを照らしてHTMLへ配置する。")
add("marp-mcp-showcase", "MCPの操作でMarp資料を更新する",
    "Markdownを直接編集するだけでは、ページ追加や書式変更の操作をエージェントに任せにくい。",
    "MCPの構造化操作でMarp原稿を作成・変更し、HTMLやPDFへ書き出す。",
    "原稿・ページ構成・テーマ・MCP/CLIへの操作", "Marp原稿・HTML・PDF・画像主体PPTX",
    "エージェントへ資料の追加・修正・出力を操作として依頼したいとき。",
    "MarpのファイルをCLI/MCPで管理し、原典export操作で書き出す。",
    "服の補修企画6ページを実MCP stdio呼び出しと原典minimal構造で作り、Marp CLIで出力。",
    2, "見つける・試す・記録する手順を、Marpの共通書式で並べたページを見る。",
    "実MCP呼び出し / Marp原稿 / 複数形式への出力",
    "PPTXは画像主体で、文字や図を個別編集する例ではない。 / MCPを使わない普通のHTML制作とは方式が異なる。",
    "原稿を用意し、MCPのcreate/manage操作でページを作ってexportする。")
add("sketch-note-showcase", "説明を手描きノート風HTMLへ",
    "文字だけの説明では、比較・補足・判断の分かれ道が同じ重さに見える。",
    "原稿を吹き出し・手描き下線・比較・判断図へ分け、単一HTMLへまとめる。",
    "話題・説明文・読者・選んだスタイル", "自己完結するHTMLスライド",
    "短い解説や教材を、手描きノートの図と注釈で見せたいとき。",
    "フレームワークなしの単一HTMLで、原典CSS・吹き出し・判断図・段階表示を使用する。",
    "文字の丸さ・太さ・行間・改行を6ページで観察。原典sketch-notes CSSとgo()制御を使用。",
    2, "文字の太さと内側の空白を比較するページを見る。注釈と比較対象を結び付ける。",
    "手描きノートCSS / 吹き出しと下線 / 単一HTML",
    "図版は自作SVGを含む。 / 原典の他スタイル全てを使った作例ではない。",
    "原稿を比較・補足・判断に分け、原典の対応する図解部品へ配置する。")
add("slide-wright-showcase", "実物2ページで方向を決めて増やす",
    "全ページ完成後にスタイルを変えると、修正範囲が大きくなる。",
    "専用テーマの実物2ページを先に作り、方向を確認して同じHTMLへ追加する。",
    "話題・メモ・原稿・見た目の方向", "専用テーマの単一HTML資料",
    "完成前に実物を見て、発表資料の方向を決めたいとき。",
    "最初は一方向のテーマと2ページを作る。既存資料の編集はそのファイルで行う。",
    "天文台企画で同じHTMLの最初の2ページを作成・実表示し、それを残して4ページ追加した。",
    1, "最初の2ページの見出し・配色・図形を見て、後続ページでも同じテーマが続くことを確認する。",
    "2ページ試作 / 専用テーマ / 同じファイルへの追加",
    "作例の方向は制作担当が判断した。ユーザーの個別承認取得とは記録しない。 / PPTXは出力していない。",
    "自分の原稿で2ページだけ試作し、確認した方向を保って残りを追加する。")
add("design-dna-showcase", "参考画像の規則を新しい資料へ移す",
    "参考画像を渡すだけでは、何を引き継いだか説明できず、ページごとに作風がぶれる。",
    "参考画像を色・文字・配置などの再利用できる規則に分け、新しい資料へ適用する。",
    "参考画像または見た目の条件・原稿・読者", "Design DNA・ページ仕様・HTML資料",
    "手持ちの参考デザインに合わせた新しい資料を作りたいとき。",
    "参考→5層のDNA→tokens→Design Contract→Blueprint→数値Page Specsの順に設計する。",
    "自作参考PNGからDNAを抽出し、道具の貸借企画6ページへ適用。原典レイアウト検査を実行した。",
    4, "道具の予定と状態を同じ表に配置したページを見る。書体・罫線・色を参考規則と比べる。",
    "参考画像の分析 / 再利用トークン / 数値ページ仕様",
    "画面が同一になることを保証する機能ではない。 / PPTX出力はこの作例では未実施。",
    "参考画像と引き継ぎたい点を指定し、DNAとページ仕様を作ってから本文を組む。")
add("cogine-templates-showcase", "内容に合うHTMLテンプレートを選ぶ",
    "見た目だけでテンプレートを選ぶと、必要な文章量や図版を収められない。",
    "テンプレートのメタデータと内容量を照合し、実DOMの枠へ原稿を配置する。",
    "原稿・読者・図版・テンプレート条件", "テンプレート方式のHTML資料",
    "既存テンプレートを使いながら、内容量とページの役割を合わせたいとき。",
    "template.jsonを読んで内容に合うものを選び、フォルダーを複製して内容制限と実DOMを守る。",
    "Editorial Luxuryを複製し、香りの贈り物企画6ページの原稿へ差し替えた。",
    4, "選ぶ・包む・渡すの順序が、テンプレートの構成に沿って並ぶことを見る。",
    "メタデータによる選択 / 内容量制限 / 実DOMへの差し替え",
    "白紙から専用の描画エンジンを設計する方式ではない。 / 他テンプレートとの比較作例はない。",
    "原稿量と必要なページ役割を確認し、合うtemplate.jsonのフォルダーを複製する。")
add("keynot-showcase", "ブランド指定をWeb発表に反映する",
    "ブランドガイドがあっても、色・書体・配置が資料へ一貫して反映されない。",
    "ブランドの色・書体・形の規則を抽出し、単一HTMLの発表へ適用する。",
    "ブランドガイドと発表原稿", "ブランドに合わせた単一HTML資料",
    "ブランド指定付きの発表を、ブラウザーで再生・共有したいとき。",
    "ブランド抽出を先に行い、ページ構成・文字・配色へ反映する。既存の操作制御を保持する。",
    "独立したBRAND.mdから活版イベントの規則を抽出。原典CSSと完全なページ制御を使い6ページ制作。",
    4, "紙とインクを並べる比較ページの色と書体を、表紙や工程ページと比べる。",
    "ブランド抽出 / 単一HTML / キーボード・スワイプ操作",
    "実在企業のブランドガイド検証ではなく自作BRAND.mdを使用。 / PPTXは出力していない。",
    "ブランドガイドと原稿を渡し、抽出した色・書体・形の規則を先に確認する。")
add("beatdeck-showcase", "一クリック一段階で工程を見せる",
    "工程を一枚に詰めると、話している箇所を聞き手が追いにくい。",
    "原稿をsceneとbeatに分け、一クリックごとに説明対象を追加・移動する。",
    "原稿・工程・見せる順番・図版", "固定ステージのReact資料とオフラインHTML",
    "工程や仕組みを、発表者のクリックに合わせて少しずつ説明したいとき。",
    "一クリックを一beatとして、原稿監査→scene/beat map→SceneDef→描画の順に組む。",
    "パン店の工程を6場面・15段階へ分解し、原典React stageとScene/Reveal/Arrowで制作。",
    5, "前後の段階へ進み、混ぜる→形づくる→焼くで対象が順に変わることを見る。",
    "scene/beat map / 一クリック一段階 / 原典React stage",
    "15は静的ページ数ではなく表示段階数。 / 動きは静止プレビューだけでは確認できない。",
    "原稿を場面と一クリック分の説明へ分け、SceneDefへ順番と動きを記す。")
add("scene-graph-showcase", "構造を保ってPPTXのテーマを変える",
    "完成PPTXの色や書体を変えると、ページごとの修正が必要になる。",
    "大綱から要素構造を持つPPTXを作り、共通テーマで文字・色・間隔を調整する。",
    "大綱YAML/JSONまたは既存PPTX", "構造化データと編集可能PPTX",
    "PPTXの構造を扱いながら、テーマを統一・変更したいとき。",
    "要素木と関係を扱うscene graphを使い、OutlineSpec/SlideSpecから作成・美化する。",
    "資料の読みやすさを説明する6ページをcreate_from_outlineで生成後、原典beautifyでprojectionテーマへ変更。",
    3, "文字を強調する数を絞ったページを見る。元draftと完成PPTXのテーマ設定の違いは制作ソースで確認する。",
    "OutlineSpec / テーマ変更 / 編集可能な文字と枠",
    "任意の既存PPTXを解析する品質の網羅試験ではない。 / 欠けていた同版vendor部品を補完した環境を使用。",
    "大綱のページ内容を替え、createで初稿を作ってから適用テーマを指定する。")
add("quarto-talks-showcase", "原稿・コード・数式を同じ発表へ",
    "計算結果を別アプリから貼ると、原稿・コード・出力の関係が追いにくい。",
    "Quarto原稿に説明・式・コード・図をまとめ、RevealJS資料へrenderする。",
    "原稿・コード・図・数式・出典", "QMDソースと自己完結HTML",
    "計算や根拠を含む技術発表を、Markdown系の原稿で管理したいとき。",
    "先に論点を選び、主張・問い・図・式・コードを目的別のページへ分ける。",
    "合成CSVの最小二乗計算をNumPyで実行し、図・式・コードを原典QMDと拡張で6ページにした。",
    3, "最小二乗のコードと出力を読む。前ページの式、次ページの限界説明との対応を見る。",
    "QMD / 実計算の出力 / 原典RevealJS拡張",
    "入力は合成データで、現実の観測結果ではない。 / 外部データの実証研究を紹介したものではない。",
    "QMDの論点・コード・元データを替え、計算出力を確かめてQuartoでrenderする。")
add("zhongguose-showcase", "原稿の章立てをナビ付きHTMLへ",
    "長い原稿をページに分けるだけでは、章の位置や話のつながりが分からない。",
    "原稿から章とページの階層を作り、中国伝統色と章ナビゲーションで示す。",
    "確定原稿・章の構造・中国色の指定", "章ナビゲーション付きHTML、またはPPT向け版式仕様",
    "東洋的な色や章の構造を持つ発表を作りたいとき。",
    "原稿の論理を先に固定し、一つの中国色・左上の枠組みナビ・章扉へ展開する。",
    "町の手仕事企画を3章・6ページへ整理し、原典テンプレートとページ制御を保持。日本語本文へ変更した。",
    2, "章ナビゲーションと三つの道の説明を見る。ページを移動して現在章の表示を確認する。",
    "原稿から章立て / 章ナビ / 原典フォントsubset生成",
    "中国語主導の既定表現は日本語に変更。 / 原典のPPT出力は版式参考で、native PPTX生成例ではない。",
    "確定原稿を章とページへ分け、使用する中国色とナビゲーションを指定する。")
add("presentation-forge-showcase", "一ページずつ編集して単一HTMLへ",
    "長い単一HTMLを直接編集すると、ページの原稿と発表用機能が混ざる。",
    "各ページを別HTMLで書き、原典ビルドでノート・テーマと一緒に単一HTMLへまとめる。",
    "ページ別HTML・ノート・テーマ・画像", "オフライン再生できる単一HTML",
    "ページを分けて保守し、最後は一つのファイルで渡したいとき。",
    "一スライド一HTML、Python標準ライブラリーのbuild.pyで原典エンジンと資材を束ねる。",
    "待機画面の設計案6ページを個別HTMLで書き、原典Obsidian部品とビルドで単一ファイル化。",
    3, "進捗が不明な場合の状態表示を、前後のページと同じ書式で説明する部分を見る。",
    "一ページ一HTML / 原典Pythonビルド / 発表ノート",
    "native PowerPointは生成しない。 / PPTXや画像からブランドテーマを抽出する機能は未実施。",
    "ページ別のHTMLとnotesを自分の原稿へ替え、原典build.pyでまとめる。")
add("and-scene-showcase", "同じ対象を保って説明を進める",
    "ページごとに図を描き直すと、同じ対象の移動なのか別の対象なのか分からなくなる。",
    "同じlayoutIdの対象を保持し、連続する説明段階の間で位置や大きさを変える。",
    "説明の段階・各対象の同一性・原稿", "React/Viteの動くWeb資料",
    "本・部品・データなど一つの対象が移る流れを説明したいとき。",
    "共通canvasとtyped Step契約を使い、groupKey/layoutIdで対象の連続性を保持する。",
    "一冊の本が次の人へ渡り、本棚へ戻る8段階を原典scene kitで制作。",
    3, "前後へ進め、同じ一冊が本棚から次の読み手へ動くことを見る。",
    "typed Step / 同じlayoutId / 原典scene kit",
    "8は表示段階数。 / 静止画だけでは対象の連続した動きは確認できない。",
    "説明する対象を固定し、各段階で同じlayoutIdと次の位置を指定する。")
add("sebastian-188", "Markdown原稿をSVGページへ",
    "原稿を図版にしても、画像に焼き込むと文字や配置を直しにくい。",
    "Markdownをページ構造へ分け、PowerPointへ取り込めるSVGとして組む。",
    "Markdown原稿・ページ構成・選んだスタイル", "ページ別SVGとPDF",
    "ベクター形式で原稿を保管し、必要に応じPowerPointへ取り込みたいとき。",
    "原稿分析→スタイル設計→PPT互換のSVG生成という手順を使う。",
    "AIへの制作依頼を整理する7ページを原典SVG方式とSwiss presetで制作し、InkscapeでPDF化。",
    4, "曖昧な依頼を具体的な仕様へ変える比較を、大きな文字と対比で示した部分を見る。",
    "Markdown原稿 / Swiss preset / SVG出力",
    "この作例の最終配布はPDFとSVG。 / PowerPointで図形変換した完成PPTXの実証ではない。",
    "Markdownを自分の内容へ替え、ページ構造とスタイルを決めてSVGを生成する。")
add("sebastian-178", "主張と根拠に合う図解を選ぶ",
    "関係の違う情報を同じカードへ入れると、結論の根拠や判断順序が分からない。",
    "答え・根拠・次の行動を整理し、比較・工程・関係に合う図解でHTML化する。",
    "意思決定の目的・原稿・根拠・仮定", "オフラインで開くHTML資料とPNG/PDF",
    "提案や教材の論点を、説明する関係に合う図で示したいとき。",
    "意思決定から逆算し、evidenceの形に合うexhibitを選ぶ。原典starterとCSS6層を保持する。",
    "動画教材化の7ページで原典starter・CSS・図解routerを使用。ページ制御だけ自作へ置換した。",
    3, "各工程の出力を次の工程の入力へ渡す関係を見る。工程を飾りのカード列にしていない。",
    "answer-first構成 / 関係別exhibit / 原典CSS6層",
    "原典runtimeを使用した実証ではない。 / 原文SKILLとroot LICENSEの表記不一致が残るため両方を保持。",
    "読者の判断と根拠を入力へ書き、図解routerで適切なexhibitを選ぶ。")
add("sebastian-173", "文字の階層と版式でHTML資料を組む",
    "色や装飾を足しても、主役の情報と補足の区別がつかない。",
    "一つの主張と中心図版を決め、文字の大きさ・細線・暗明の切り替えで情報を整理する。",
    "ブリーフ・原稿・ページの役割", "HTML/CSS資料とPNG/PDF",
    "大きな文字や図を中心に、投影向けのWeb資料を作りたいとき。",
    "固定1920×1080、主張見出し、中心対象一つ、文字の階層、13の版式語彙を使用する。",
    "音の観察イベントを7ページで制作。原典CSSと版式を使い、暗色と紙色のページを切り替えた。",
    3, "音の種類と印象を並べたページで、主見出し・項目名・説明の文字階層を見る。",
    "原典CSS / 13-slot版式 / 暗色と紙色の切り替え",
    "PPTX生成器ではない。 / 作例のイベントや効果は架空で未実施。",
    "一ページの主張と中心対象を一つずつ決め、原典CSSの版式へ配置する。")
add("slidepoise-showcase", "画像案を編集可能なPPTXへ再構築",
    "AIで作ったスライド画像は、文字や接続線を個別に修正できない。",
    "画像で作った見た目を測定し、意味を持つ文字・図形・接続線へ再構築する。",
    "原稿・生成画像案・各要素の意味と再構築指示", "native要素を持つ編集可能PPTX",
    "画像のデザイン案を、後から直せるPowerPointへ移したいとき。",
    "画像生成→意味対応→OpenCV測定→reconstruction contract→constructor→原典rendererを通す。",
    "予約サイト改善の仮想案3ページで原典パイプラインを使用し、文字・分岐・接続線をnative要素へ変換。",
    1, "空席の有無で分かれる図のラベルと接続を確認する。元画像との比較と個別編集は配布ソース/PPTXで見る。",
    "画像案の生成 / 実測と意味対応 / native再構築",
    "『操作を半分』は目標であり実測成果ではない。 / 自動測定だけで見た目の合格を判定する方式ではない。",
    "原稿から画像案を作り、文字・図形・線の意味を指定して原典再構築器へ渡す。")
add("sebastian-205", "研究ノートを根拠付きPPTXへ",
    "研究メモの仮説と実測結果を混ぜると、何が根拠か分からなくなる。",
    "論文や研究ノートの主張を出典へ対応させ、ノート付き編集可能PPTXへ整理する。",
    "論文・部分資料または研究ノート", "出典と話者ノートを持つ編集可能PPTX",
    "研究メモを、仮説・評価計画・限界が区別できる発表にしたいとき。",
    "full-paper/partial-paper/notes-onlyを区別し、作成前にclaim-to-source mapを持つ。",
    "食品在庫UIの研究ノートをnotes-onlyと記録し、8ページを入力節へ対応させた。架空・未実施を明示。",
    5, "見つけやすさと更新しやすさを別の評価項目として扱うページを見る。出典注記と未実施表示も確認する。",
    "notes-only判定 / claim-to-source map / 出典と話者ノート",
    "論文全文の読解・実験図の抽出は未実施。 / 原典preflight/inspectを省いた最小確認で、全QA合格とは扱わない。",
    "研究ノートの各主張を入力節へ対応させ、仮説・計画・結果を区別してページ化する。")
add("sebastian-203", "研究の大綱を学術テンプレートへ",
    "研究の章名を並べただけでは、問い・仮説・比較・評価の関係が伝わらない。",
    "研究の大綱やレビューを論点の流れに組み替え、既存学術テンプレートに配置する。",
    "研究大綱・レビュー原稿・論文・学術PPTXテンプレート", "学術的な関係図・表を持つ編集可能PPTX",
    "研究提案のモデル・比較条件・評価方法を、指定の学術書式で説明したいとき。",
    "技術的な対象と関係を主役にし、主張の出典・推論・テンプレートの書式を保持する。",
    "図書館の研究大綱を8ページへ整理。原典学術テンプレートを再利用し、仮説関係・比較表・評価手順をnative化した。",
    3, "仮説と検証する関係の図を見る。仮説を既知の結果として表示していないか確認できる。",
    "研究大綱の再構成 / 原典学術テンプレート / native関係図と表",
    "架空・未実施研究で、文献レビューや実験結果の抽出例ではない。 / Microsoft PowerPoint実機での確認は未実施。",
    "研究大綱の問い・仮説・比較条件・評価方法を整理し、使用するテンプレートへ配置する。")
add("sebastian-193", "学術テンプレートを保って図表を作る",
    "学術資料を作り直すと、指定テンプレートのmasterや書式が失われやすい。",
    "テンプレートの規則を保ち、原稿を編集可能な文字・図形・表へ組み直す。",
    "論文・研究計画・原稿・テンプレート", "テンプレート方式の編集可能PPTX",
    "学術書式を保ったまま、研究の関係や手順を図で説明したいとき。",
    "入力とテンプレートを優先し、画像案・直接native制作・画像再構築の経路を選ぶ。",
    "公共空間サインの研究計画8ページをRoute BのPptxGenJS方式で制作。defaultのmaster/themeを保全。",
    3, "サインを点ではなく連続として扱う関係図を見る。図中の文字と接続はPPTXで個別編集できる。",
    "Route B / テンプレートmaster保持 / native関係図",
    "画像生成を使うRoute A/Cは未実施。 / 実験結果ではなく研究計画を示す。",
    "原稿とテンプレートを渡し、native直接制作のRoute Bで図表を組む。")
add("learndeck-showcase", "HTMLの位置を測ってPPTX化",
    "HTMLを全面スクリーンショットにすると、文字と基本図形を別々に直せない。",
    "HTMLのDOM位置をブラウザーで測り、文字・基本図形・個別SVGを分けてPPTXへ変換する。",
    "学習原稿または既存のHTML資料", "要素別に編集できるPPTX",
    "HTMLで作った教材や説明資料を、PowerPointへ移したいとき。",
    "DOM測定から文字・図形・SVGを分離して再構築し、全面画像への置換を避ける。",
    "花の提供企画5ページを原典HTML-to-PPT converterで変換。文字・基本図形と個別の花画像を分離。",
    2, "選ぶ→届く→飾るの順序と各ラベルを見る。個別編集の範囲はPPTXで確かめる。",
    "ブラウザー実測 / 文字と図形の分離 / 個別SVG抽出",
    "花の図版は互換性用の個別画像で、すべてがnative図形ではない。 / 任意HTMLの完全互換は保証しない。",
    "変換するHTMLを用意し、原典converterでDOMを測ってPPTXへ書き出す。")
add("port-town", "雑誌風のWeb発表とノートを作る",
    "Web資料に発表用の操作やノートを後から付けると、表示と話す内容が分かれやすい。",
    "原稿を雑誌風またはSwissの版式へ配置し、ページ操作・話者ノートと一緒に単一HTMLへまとめる。",
    "発表原稿・読者・選んだスタイル・話者ノート", "単一HTMLの横移動型発表資料",
    "人文・企画の発表を、ノート付きのWeb資料として見せたいとき。",
    "原典テンプレート、規定テーマ、章扉・図表などの版式と発表者機能を使用する。",
    "港町の回遊企画7ページを元HTMLテンプレートへ配置。ページ制御と演出を保持し日本語を調整。",
    2, "徒歩行程の時間と順序を見る。短い行程情報を発表向けにまとめた部分を確認する。",
    "原典HTMLテンプレート / ページ制御 / 講稿",
    "PPTXを生成する方式ではない。 / WebGL演出の有無や負荷は再生環境によって変わる。",
    "発表内容とノートを用意し、原典の雑誌風かSwissのテンプレートへ配置する。")
add("cyberppt", "根拠と画像案からPPTXを組み直す",
    "資料を先に飾ると、結論を支える根拠や必要な情報が抜けやすい。",
    "根拠と論点を整理し、画像blueprintを基準に主要文字を編集できるPPTXへ再構築する。",
    "文書・報告・元データ・ページ別blueprint", "主要文字が編集できるPPTXと画像案の比較",
    "情報量のある業務提案で、論点・画像案・編集版を対応させたいとき。",
    "根拠分析とSCR→視覚案→全ページblueprint→見た目と編集性を両立する再構築。",
    "商店街の案内企画5ページで内容lock・画像blueprint・測定比較を実施し、日本語native版を制作。",
    2, "比較に必要な日時・場所・費用・雨天時を同じ表に整理したページを見る。元blueprintとの対応は比較資料で確認する。",
    "内容lock / 全ページ画像blueprint / 日本語native再構築",
    "原典strict一致の検査は未達と記録されている。 / 原典の全工程合格例としては扱わない。",
    "元資料の根拠と結論を整理し、画像blueprintと編集版を同じ内容で対応させる。")
add("html-scrolline", "工程を連続スクロールでつなぐ",
    "離れたページへ切り替えると、準備の流れや現在の位置を見失いやすい。",
    "内容をbeatとmoveへ分け、一つのステージ上を連続して移動する発表へ変える。",
    "ブリーフ・deck.yamlの内容と動き指定", "スクロールで進むWeb資料",
    "工程や時系列を、連続した移動で追って見せたいとき。",
    "内容はbeat、動きはmoveに分離し、deck.yamlで指定する。原典engineを資料ごとに書き換えない。",
    "小さな展示の準備を6停止点へ分け、原典Scrolline engine・rail-advance・era-shift・handoffを使用。",
    3, "前後へ進め、準備の連続線上で案内から当日の準備へ移る動きを見る。",
    "連続timeline / rail移動 / handoff",
    "MP4出力はこの作例では未実施。 / 原典全体CIはWindowsパス3件が未通過。",
    "deck.yamlへ停止点と各点の内容を記し、既存moveを選んでブラウザーで再生する。")
add("react-slide-deck", "Reactで操作付きの発表を作る",
    "クリックで内容を切り替える説明は、静的なスライドだけでは試せない。",
    "Reactの状態とコンポーネントでページや内容を切り替え、Motionで動きを付ける。",
    "ユーザーの原稿・ページ構成・操作要件", "React/ViteのWeb資料とbuild済みHTML",
    "ページ内のタブなど、説明に必要な操作を持つ資料を作りたいとき。",
    "React/TypeScript、固定比率のSlideLayout、状態管理、Framer Motionで構成する。",
    "問い合わせをFAQへ整理する5ページで原典App・SlideLayout・useSlideScaleを使用。週別タブは作例の追加。",
    3, "週別タブを切り替え、4週間の作業内容が変わることを見る。",
    "React状態 / 固定比率レイアウト / Motion",
    "週別タブは原典の標準部品ではなく追加実装。 / ソースからの再buildにはNode環境が必要。",
    "原稿と必要な操作を決め、Reactページと状態を編集してViteでbuildする。")
add("cafe-pptx", "図と数値の提案を編集可能PPTXへ",
    "提案の図や計算を画像へまとめると、審議中に文言や数値を修正しにくい。",
    "文書・計数・図解を、文字と図形を編集できるPPTXへ組み立てる。",
    "原稿・元データ・図解・使用テンプレート", "編集可能PPTX・PDF・ページ別講稿",
    "数値の仮定や判断条件を示し、会議後にPowerPointで修正したいとき。",
    "編集可能PPTXを目的に制作方式を選び、ブランド・スタイル・版式と内容を分離する。",
    "喫茶店の出店提案8ページを、日本語文字・図形profileと原典native SVG→PPTX変換器で制作。",
    3, "損益分岐の客数60人と計算の仮定を見る。候補比較・リスク・次の判断へつながる構成も確認する。",
    "native SVG変換 / 入力計数の計算 / PowerPoint実描画",
    "架空の店舗・計数で、実績や見積ではない。 / 原典Default全工程・音声・自動動画は未実施。",
    "input/data.jsonの計数と原稿を替え、図解をnative形式で生成してPPTXへ変換する。")
add("japanese-corporate", "情報量のある業務図を部品で組む",
    "情報を削り過ぎると、関係者・根拠・例外・次の担当を一枚で確認できない。",
    "業務全体・担当・関係・数値・注記を、編集できる図表部品で一枚へまとめる。",
    "業務資料・計数・関係者・前提・出典", "情報密度のある日本語の編集可能PPTX",
    "社内報告、稟議、事業スキームや担当の関係をまとめたいとき。",
    "参照資料から適切なポンチ絵の型を選び、装飾より関係を先に描く。native部品を使用する。",
    "公式15型PPTXから6型を選び、月次報告のチャート・表・担当関係を編集した。",
    4, "販売・商品・顧客対応で確認結果を渡す関係を見る。担当と次の作業を同じ図に記している。",
    "公式15型の再利用 / native表・チャート / 担当関係図",
    "専用生成APIは同梱されていない。 / 月次計数は共通の架空データ。",
    "報告内容・担当・根拠・前提を整理し、公式15型から関係に合う型を選んで編集する。")
add("presentation-delivery", "HTML案を編集可能PPTXで渡す",
    "HTMLの見た目だけを確認しても、相手が編集するPPTXの仕上がりは分からない。",
    "HTMLで構成を作り、DOM変換と寸法確認を通して編集可能なPPTXへ渡す。",
    "依頼の意図・原稿・HTML案・受け渡し条件", "HTML・編集可能PPTX・PDF",
    "ブラウザーの試作を、相手がPowerPointで直せる提出物にしたいとき。",
    "原典visual-deck-studioのHTML-firstと、最終的に相手が見える結果へつなぐ受け渡しを使う。",
    "引き継ぎ案内6ページをHTML-first Path Aと原典DOM変換で制作。本文・図形・ノートをPPTXへ保存。",
    3, "完了と保留を書き分ける例を見る。HTMLとPPTXの両方で同じ区別が残ることを確認する。",
    "HTML-first / 原典DOM変換 / native文字とノート",
    "画像や動画への全出力機能は未実施。 / プレビューだけでPPTXの編集性を判定しない。",
    "原稿と受け渡し条件を整理し、HTML案を原典のPPTX変換経路へ渡す。")
add("pradaslides", "読者の次の行動から資料を設計する",
    "資料の枚数や見た目だけを先に決めると、読んだ人に何をしてほしいか抜ける。",
    "読者・期待する変化・根拠を定め、構成から完成ファイルまで対応させる。",
    "短い依頼・原稿・読者・期待する行動", "PPTXと実描画を使うHTML presenter。この作例の経路",
    "手順や提案を、読者が次に行動できる資料にしたいとき。",
    "communication contract→根拠→audience journey→deck plan→制作→実描画の対応を保持する。",
    "町内会の備品貸出6ページを原典計画契約とlintで制作し、PowerPoint描画をHTML presenterへ使用。",
    4, "返却時に何を確認して誰へ渡すかを見る。最後の依頼行動に必要な情報が具体的にある。",
    "伝達目的の契約 / 読者の行動に沿う構成 / 実描画presenter",
    "原典が対応する全出力経路を実証したものではない。 / 架空の備品貸出手順。",
    "読者と読後の行動を一文で決め、根拠と必要な手順をdeck planへ記す。")
add("office-powerpoint-mcp", "MCPのツール操作でPPTXを作る",
    "エージェントに図表の追加を頼んでも、直接編集する共通操作がない。",
    "MCPの作成・文字・表・チャート操作で、PowerPointをプログラムから組み立てる。",
    "テンプレート・原稿・表データ・チャートデータ", "native表・チャートを含むPPTX",
    "エージェントから表やチャートの追加・更新をツール操作として行いたいとき。",
    "python-pptxを使うMCPサーバーのツールを通して、作成・管理・デザインを行う。",
    "公式MCP stdioでcreate_presentation_from_template/add_slide/manage_text/add_table/add_chart/saveを実行し、月次報告6ページを作成。",
    2, "売上増分をチャートで表示したページを見る。チャートの元データの編集はPPTXで確認する。",
    "実MCP stdio / native表 / nativeチャート",
    "原典はSKILLではなくMCPサーバー。 / サーバーはアーカイブ済みと現行案内に記録されている。",
    "MCPサーバーを接続し、原稿と表・チャートのデータを構造化ツール操作へ渡す。")
add("qiaomu-bento", "オフライン編集できるBento資料へ",
    "HTMLを修正するためにコード編集が必要だと、利用者が本文や表を直しにくい。",
    "JSON文書を固定Bento shellへ組み、ブラウザーで編集・再生できる一ファイルにする。",
    "ブリーフ・原稿・データ・bento文書JSON", "編集版と再生版の.bento.html",
    "オフライン配布した後も、ブラウザーで本文や表を直したいとき。",
    "固定shellを保持し、#bento-doc文書契約から構築して構造・同一性・shell整合を検証する。",
    "社内検索の試行6ページを原典bento_deck.pyで制作。権限確認から回答へ同じ検索要素を移動させた。",
    2, "前後へ進め、検索要素が権限確認から出典付き回答へ移ることを見る。編集版では本文・表を変更できる。",
    "文書JSON / 固定shell / ブラウザー編集とmorph",
    "通常の.pptx納品を行うスキルではない。 / 元のBento製品全体を構築する例ではない。",
    "文書JSONへ原稿と表を入れ、原典builderで編集版と再生版を生成する。")
add("seaslides", "同じ原稿からWeb資料と書き出しを作る",
    "HTML・PDF・画像を別々に作ると、内容やページ構成がずれる。",
    "内容仕様とHTMLを正本にし、同じコンパイル経路から表示と書き出しを作る。",
    "原稿・内容仕様・テーマ・content.html", "HTML・SVG・PNG・PDF。この作例で生成した形式",
    "Web表示と配布用出力を、同じ内容でそろえたいとき。",
    "Source→Project→Theme→Strategist→Executor→Assemble→Review→Exportの原典経路を使う。",
    "読書会5ページをeditorial-magazineと原典html_compiler --allで生成し、source/visual gateを実行。",
    2, "60分の進行を同じ時間軸にまとめたページを見る。出力形式が変わっても内容の順序を保つ。",
    "内容仕様 / 原典HTML compiler / 同経路の複数出力",
    "この作例の配布にnative PPTXは含まない。 / Windowsのreceipt pathを派生修正した。",
    "内容仕様とcontent.htmlを自分の原稿へ替え、原典compilerとsource/visual gateを実行する。")
add("minorun-marp", "同じ図を少しずつ足す登壇資料",
    "仕組み全体を一枚で見せると、話し手の説明と聞き手の読む順番がずれる。",
    "問いから始め、同じ図を3〜5ページに分けて要素を一つずつ追加する。",
    "登壇・講義の原稿・聴衆・持ち時間", "Marp Markdownと黒地テーマのHTML",
    "Gitなどの仕組みを、口頭説明に合わせて段階的に教えたいとき。",
    "先に話の骨子と各ページ固有の内容を決め、図を段階開示する。黒地の文字・配色・余白は実表示で確認する。",
    "Gitの作業フォルダー→ステージ→履歴→共有を9ページで段階表示。原典3スキルとminorun-darkを使用。",
    4, "前後のページと比べてステージが追加されることを見る。追加された場所とコマンドを対応させる。",
    "問いから始める構成 / 同じ図の段階開示 / 原典minorun-dark",
    "配布用の網羅的マニュアルではなく登壇・講義を想定。 / 原稿はMarp Markdownとして編集する。",
    "聴衆と話の骨子を決め、一つの図へ3〜5ページかけて要素を足す。")
add("ppt-design-skill", "ブリーフとテーマからnative PPTXを作る",
    "原稿をそのまま配置すると、資料の目的に合う密度や比較方法が決まらない。",
    "目的・構成・テーマを先に定め、公開Pythonライブラリーで編集可能PPTXを生成する。",
    "ブリーフ・原稿・元データ・テーマ条件", "編集可能PPTXと描画プレビュー",
    "説明の目的に合わせて、図表と見た目を調整しながらPPTXを作りたいとき。",
    "設計判断を先に行い、Build/FreeStyle/VIの経路から選ぶ。公開APIのみで生成しPNGで確認する。",
    "朝営業の仮想企画5ページをBuild Mode・ThemeComposer・strict Presentationと公開helperで制作。",
    2, "客数などの仮定を変えた売上比較を見る。実績ではなく入力条件別の試算として示す。",
    "Build Mode / ThemeComposer / 公開Python API",
    "朝営業の売上は仮定による試算。 / FreeStyle/VI Buildはこの作例では未実施。",
    "目的と入力計数を整理し、テーマを設定して公開APIの部品でページを構成する。")
add("ppt-design-system", "文字と配色の規則を資料全体へ",
    "ページごとに色や文字を選ぶと、見出し・説明・補足の役割がぶれる。",
    "テーマと10種の版式を使い、見出し・本文・補足の文字階層を資料全体でそろえる。",
    "原稿・出力形式・選ぶテーマと版式", "HTML資料。この作例はForest Ink",
    "決められたテーマで、案内や説明資料のページ間の書式をそろえたいとき。",
    "5スタイル・10版式、見出し/本文/メタデータの三層と暗明の切り替えを使う。",
    "雨の日の図書館案内6ページを原典HTMLテンプレート・Forest Ink・ページ制御で制作。",
    4, "開催・変更・中止など、お知らせごとの次の行動が同じ書式で示される部分を見る。",
    "Forest Ink / 文字の三層 / 原典HTMLテンプレート",
    "PPTX形式はこの作例では出力していない。 / 5テーマ全ての比較ではない。",
    "出力形式とテーマを決め、内容に合う版式へ原稿を配置する。")
add("hands-on-deck", "既存PPTXをJSON差分で編集する",
    "既存PPTXの一部を直したいのに、全面生成し直すと元の書式や内容を失いやすい。",
    "対象要素を検査してJSON patchで変更し、変更差分と実描画で結果を確認する。",
    "既存PPTXと変更内容を記したJSON patch", "変更済みPPTXと編集差分",
    "手持ち資料の文言・図形・配置を、対象を限定して修正したいとき。",
    "inspect→atomic JSON patch→apply/fix→diff→実描画の編集ループを使う。",
    "既存の日本語PPTXを原典deck.pyで79箇所変更し、全5ページをPowerPointで描画した。",
    2, "問題を次の対応へつなぐページを、元PPTXと変更差分で比べる。最終画面だけでなくinput/patch.jsonを確認できる。",
    "既存PPTX検査 / atomic patch / diff",
    "この作例は既存資料の編集で、白紙からの制作ではない。 / 操作のページ番号は0始まり。",
    "元PPTXをinspectし、変更対象と内容だけをJSON patchへ記してapplyする。")
add("image-to-editable", "スライド画像を要素別PPTXへ",
    "画像になったスライドでは、本文を直すにも画像全体の再生成が必要になる。",
    "画像の文字・基本図形・アイコンを分離し、要素別に編集できるPPTXへ再構築する。",
    "スライド画像・画像主体PPTX・PDFと任意の話者ノート", "要素別に編集できるPPTX",
    "手元に画像しかない資料を、PowerPointで更新したいとき。",
    "editpptでページを分解・再構築・記録・結合する。新規資料制作とは分ける。",
    "Git入門画像2枚を、編集可能な文字・カードと画像アイコンへ分離した。",
    1, "作業・ステージ・履歴の各ラベルと枠を見る。元画像との比較で位置を確認し、PPTXでラベルを変更できる。",
    "原典editppt / 文字と枠の分離 / 元画像との比較",
    "アイコンは画像のままの部分がある。 / 白紙から内容やデザインを作るスキルではない。",
    "編集したい元画像とノートを用意し、editpptのprepare→rebuild→finalizeへ渡す。")
add("codex-image-ppt", "原稿から一貫した画像PPTXを作る",
    "各ページを別々に画像生成すると、書式や説明の粒度がそろわない。",
    "原稿を共通のスタイル指示とページ別指示へ分け、画像と講稿をPPTXへまとめる。",
    "記事・報告・原稿・共通スタイル・講稿", "一ページ一画像のPPTXと講稿",
    "図と文字を一体にした画像主体の資料を、同じ見た目でそろえたいとき。",
    "共通仕様と逐頁promptを作り、画像生成の結果と状態を記録して原典assembleでPPTX化する。",
    "Gitの保存・記録・共有を3ページの画像として生成。原典prepare/dispatch/result/stateとassemble_ppt.pyを使用。",
    1, "作業フォルダー・ステージ・履歴の流れを見る。他ページと同じ視覚規則で説明を続ける。",
    "共通スタイル指示 / ページ別画像生成 / 原典包装CLI",
    "本文と図は画像内にあり個別編集できない。 / native図形へ再構築するスキルではない。",
    "原稿と講稿を用意し、共通スタイルとページ別promptを作って画像生成・包装する。")
add("slide-maker", "実行したコードを根拠に図表を作る",
    "計算例を手で書くと、図や数値が実行結果と食い違いやすい。",
    "原稿と実行結果を根拠に、主張・図・チャートを持つ編集可能PPTXへ組む。",
    "原稿・コード・図・データ・読者", "編集可能PPTXと描画プレビュー",
    "技術やアルゴリズムを、実行結果と図を対応させて説明したいとき。",
    "内容計画→設計→deckkit制作→独立criticの検証と修正を行う。根拠は実行・出典で確かめる。",
    "1〜15の探索をPythonで実行し、原典deckkit/native_chartで5ページ教材へした。全制作ゲートの完走とは区別。",
    2, "二分探索の訪問先を順に追い、目的値13へ4回で届くことを見る。次ページでは全15通りの最大比較回数を示す。",
    "実行トレース / 原典deckkit / native chart",
    "比較回数は訪問要素数。実行時間や整列コストの測定ではない。 / 原典全工程の完走を示す作例ではない。",
    "元コードとデータを実行して結果を保存し、その根拠と主張をdeckkitの図表へ渡す。")
add("business-carousel", "投稿の流れを先にカルーセルで確認する",
    "スライド画像を作り始める前に、最初の引き込みから最後の行動までを確認できない。",
    "原稿をhook→問題→価値→行動の流れへ分け、ページ別ブリーフとHTML確認版にする。",
    "投稿の目的・読者・ブランド・伝えたい内容", "ページ別Markdownブリーフと正方形HTMLプレビュー",
    "SNSの複数枚投稿を、画像制作前に内容と順序から確かめたいとき。",
    "各ページにheadline/body/visual direction/backgroundを持ち、最後は具体的なCTAで終える。",
    "引き継ぎメモの6枚カルーセルを原典43番で構成し、1080×1080のHTMLプレビューを作成。",
    4, "三行メモの具体例を見る。前の説明を、読者が書ける例へ落とし込んでいる。",
    "ページ別ブリーフ / hookからCTAの構成 / 正方形HTML確認版",
    "完成SNS画像の量産や投稿は未実施。 / Canva/Figmaの制作作業を行うスキルではない。",
    "投稿目的と読者を定め、各ページの見出し・本文・視覚指示・背景をブリーフへ書く。")
add("magic-slide", "同じ要素の変化でページをつなぐ",
    "毎ページで要素を消して出すと、時間や準備品の変化を追いにくい。",
    "隣接ページに同じ要素を残し、位置や大きさの変化で話をつなぐ。",
    "話題・原稿・ページ間で引き継ぐ対象", "Magic Move付き単一HTML資料",
    "数字・見出し・図の対象を保ったまま、変化を説明したいとき。",
    "Magic Moveを最後の飾りにせず、同じ見出し・数値・図形が残るよう構成段階で計画する。",
    "朝の準備を5ページで説明。原典Magic Moveで10分という時間と準備品を隣接ページへ引き継いだ。",
    2, "前後へ進め、前夜に移す10分と三つの準備品がどう引き継がれるか見る。",
    "構成から動きを計画 / 同じ要素の継続 / 原典mergeとserve",
    "時間短縮の効果を測定した資料ではない。 / 動きは静止プレビューだけでは分からない。",
    "隣接ページへ残す数字や対象を決め、同じ識別子を持つ要素として原稿を組む。")
add("revealjs-skill", "原稿を発表操作付きHTMLへ",
    "HTMLを並べるだけでは、発表のページ操作・ノート・段階表示を個別に作る必要がある。",
    "公式スキャフォールドに原稿を入れ、Reveal.jsの移動・ノート・レイアウトを使う。",
    "原稿・ページ構成・ノート・スタイル", "HTMLとCSSのブラウザー発表資料",
    "コード・表・説明文を含む発表を、Reveal.jsで再生したいとき。",
    "原典create-presentation.jsとbase-styles.cssを基に、適切なsection構造と版式を選ぶ。",
    "社内検索の試行6ページを公式スクリプトで生成した骨格に配置し、2カラム・表・ノートと原典単位を使用。",
    3, "4週間の作業と判断材料を表で見る。ページ操作と発表ノートは実HTMLで確認できる。",
    "公式scaffold / 2カラムと表 / Reveal.jsナビゲーション",
    "縦方向スタックやコード強調など全機能の作例ではない。 / PowerPointファイルは出力していない。",
    "原稿とページ数を決め、原典scaffoldへsection・表・発表ノートを入れる。")


SOURCE_OVERRIDES = {
    "sebastian-207": "skill-forks/sebastian-207-ja/source/upstream-adapted/codex-ppt-skill/SKILL.md",
    "sebastian-208": "skill-forks/sebastian-208-ja/source/UPSTREAM-SKILL.md",
    "sebastian-178": "skill-forks/sebastian-178-ja/example/source/SKILL.md",
    "office-powerpoint-mcp": "skill-forks/office-powerpoint-mcp-ja/upstream/README.md",
    "presentation-delivery": "skill-forks/presentation-delivery-ja/upstream/skills/visual-deck-studio/SKILL.md",
    "minorun-marp": "skill-forks/minorun-marp-ja/upstream/skills/slide-story/SKILL.md",
}
ORIGINAL_PATH_OVERRIDES = {
    "agent-slides-showcase": "skills/slides-build/SKILL.md",
    "sebastian-207": "codex-ppt-skill/SKILL.md",
    "sebastian-208": "skills/academic-image-ppt/SKILL.md",
    "sebastian-178": "SKILL.md",
    "office-powerpoint-mcp": "README.md",
    "presentation-delivery": "skills/visual-deck-studio/SKILL.md",
    "minorun-marp": "skills/slide-story/SKILL.md",
}
MOTION_IDS = {"sol-motion-showcase", "slidefly-showcase", "beatdeck-showcase",
              "and-scene-showcase", "html-scrolline", "magic-slide", "qiaomu-bento"}
CORE_STATUS = {
    "sci-diagram-showcase": "core_input_reconstruction_not_demonstrated",
    "thesis-defense-showcase": "sample_template_and_research_notes",
    "sebastian-205": "research_notes_mode",
    "sebastian-203": "research_outline_mode",
    "sebastian-208": "manuscript_adaptation",
    "cyberppt": "original_strict_gate_not_passed",
    "agent-slides-showcase": "single_page_scope",
}


def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def posix(path):
    return path.relative_to(ROOT).as_posix()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def case_base(case):
    path = (ROOT / case["preview"]).parent
    if path.name in ("dist", "pages", "presenter"):
        path = path.parent
    return path


def source_candidates(case):
    found = []
    bases = [ROOT / "skill-forks" / case["fork_id"], case_base(case)]
    for base in bases:
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "dist", "render")]
            for filename in files:
                path = Path(root) / filename
                if filename in ("SKILL.md", "SKILL.upstream.md", "UPSTREAM-SKILL.md") and path != base / "SKILL.md":
                    found.append(path)
    found += list((ROOT / "sources" / case["repository"].replace("/", "__")).glob("*SKILL*"))
    return found


def resolve_source(case, guide):
    base = case_base(case)
    provenance = read_json(base / "PROVENANCE.json")
    commit = case.get("upstream_commit") or provenance.get("upstream_commit") or provenance.get("commit") or guide["upstream_commit"]
    all_refs = provenance.get("source_refs", []) + guide.get("source_refs", [])
    refs = [ref for ref in all_refs if isinstance(ref, dict) and f"/{commit}/" in ref.get("url", "")]
    candidates = source_candidates(case)
    override = SOURCE_OVERRIDES.get(case["id"])
    if override:
        selected = ROOT / override
    else:
        exact = [(p, ref) for p in candidates for ref in refs
                 if ref.get("sha256") == sha(p) and ref.get("path", "").endswith("SKILL.md")]
        if exact:
            selected = min(exact, key=lambda pair: len(str(pair[0])))[0]
        else:
            upstream = [p for p in candidates if "upstream" in p.parts or p.name == "SKILL.upstream.md"]
            selected = min(upstream or candidates, key=lambda p: len(str(p)))
    text = selected.read_text(encoding="utf-8-sig", errors="strict")
    digest = sha(selected)
    matched = next((ref for ref in refs if ref.get("sha256") == digest), None)
    original_path = ORIGINAL_PATH_OVERRIDES.get(case["id"])
    if not original_path:
        original_path = matched["path"] if matched else next((s for s in guide.get("skill_paths", []) if s.endswith("SKILL.md")), "SKILL.md")
    url = f"https://github.com/{case['repository']}/blob/{commit}/{original_path}"
    raw_url = url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")
    remote = REMOTE_HASH_CHECKS.get(case["id"], {})
    if not remote:
        remote = next((check for check in REMOTE_HASH_CHECKS.values() if check.get("url") == raw_url and check.get("remote_sha256") == digest), {})
    remote_verified = (remote.get("status") == "verified"
                       and remote.get("remote_sha256") == digest
                       and remote.get("url") == raw_url)
    lock = SOURCE_LOCKS.get((case['repository'], commit, original_path), {})
    locked = lock.get('verified') is True and lock.get('sha256') == digest and lock.get('url') == url
    verified = bool(matched) or remote_verified or locked
    # A local adapter is not mislabeled as an exact original snapshot.
    return dict(commit=commit, skill_path=original_path, url=url, local_path=posix(selected),
                source_sha256=digest, pinned_source_hash_verified=verified), {
                    "path": posix(selected), "sha256": digest,
                    "pinned_source_hash_verified": verified,
                    "verification_method": "pinned-source-ref-sha256" if matched else "github-pinned-raw-sha256" if remote_verified else "audited-pinned-source-lock" if locked else "unverified",
                    "source_ref": matched or remote or lock, "lines": len(text.splitlines()),
                    "headings": [line for line in text.splitlines() if line.startswith("#")][:25],
                }


def evidence(case, row):
    index = row["index"]
    base = case_base(case)
    pages = case.get("pages") or []
    candidates = []
    if index < len(pages):
        candidates.append(ROOT / pages[index])
    candidates.append(base / "render" / f"effect-page-{index+1:02d}-after.png")
    candidates.append(base / "render" / f"effect-page-{index+1:02d}-after.jpg")
    candidates.append(base / "render" / f"effect-page-{index+1:02d}.jpg")
    candidates.append(base / "render" / f"slide-{index+1:02d}.png")
    if case["id"] == "sebastian-192":
        candidates.append(base / "pages" / f"{index+1:02d}-slide.png")
    image = next((path for path in candidates if path.is_file()), None)
    proof = image or ROOT / case["preview"]
    assert proof.is_file(), proof
    title = (case.get("titles") or [])[index]
    return dict(index=index, label=f"{index+1}段階目" if case["id"] in ("beatdeck-showcase", "and-scene-showcase") else f"{index+1}ページ目",
                title=title, what_to_inspect=row["inspect"], skill_rule=row["principle"],
                proof_path=posix(proof), proof_kind="render-image" if image else "live-html",
                preview_path=case["preview"])


def source_proofs(case):
    base = case_base(case)
    candidates = [ROOT / case.get("input", "missing"), ROOT / case.get("input_data", "missing"), base / "input/BRIEF.md",
                  base / "input/deck.json", base / "input/slides.json", base / "input/patch.json",
                  base / "source/build.py", base / "source/build.mjs", base / "source/build_deck.py", base / 'build.mts',
                  base / "work/deck-scenes.json", base / "notes/claim-to-source.json",
                  base / "PROVENANCE.json", ROOT / case.get("artifact_download", "missing"),
                  base / 'verification.html', base / 'source/verification-index.json',
                  base / 'source/VERIFY.json', base / 'render/verify/report.json']
    return list(dict.fromkeys(posix(path) for path in candidates if path.is_file()))


def cautions(case):
    qa = read_json(ROOT / case['qa'])
    result = []
    aesthetic = qa.get('upstream_aesthetic', {})
    if aesthetic.get('status') == 'FAIL':
        result.append('原典の美術QAは未合格です（' + str(aesthetic.get('score')) + '点）。表示と制作方法を試せる作例として掲載しています。')
    if qa.get('original_gate_not_passed'):
        result.append('原典の画像との厳密一致ゲートは未合格です。日本語派生版として内容と編集性を確認した作例です。')
    if qa.get('full_verify_executed') is False:
        result.append('原典の全段階往復・直接移動のverifyは未実施です。初回表示と生成を確認した段階です。')
    return result


def main():
    global REMOTE_HASH_CHECKS, SOURCE_LOCKS
    SOURCE_LOCKS = {(s['repository'], s['commit'], s['skill_path']):s for s in read_json(ROOT / 'data/skill-source-lock.json').get('sources', [])}
    audit_path = ROOT.parents[1] / ".local/reviews/slides-skill-effect/source-audit.json"
    previous_audit = read_json(audit_path)
    remote_checks = previous_audit.get("remote_source_hash_checks", [])
    REMOTE_HASH_CHECKS = {row["case_id"]: row for row in remote_checks}
    product = read_json(ROOT / "data/product-collection.json")
    cases = {case["id"]: case for case in read_json(ROOT / "data/case-studies.json")}
    guides = {guide["repository"]: guide for guide in read_json(ROOT / "data/repository-guides.json")}
    need_data = read_json(ROOT / 'data/skill-needs.json').get('needs_by_repository', {})
    rows = {row["case_id"]: row for row in ROWS}
    editorial_patches = {}
    for patch_file in sorted((ROOT / 'data/skill-effect-patches').glob('*.json')):
        for patch in read_json(patch_file):
            previous = editorial_patches.get(patch['case_id'], {})
            editorial_patches[patch['case_id']] = {**previous, **patch,
                'demonstration': {**previous.get('demonstration', {}), **patch.get('demonstration', {})},
                'guide_patch': {**previous.get('guide_patch', {}), **patch.get('guide_patch', {})}}
    assert len(rows) == len(ROWS) == 61
    assert set(rows) == set(product["active_case_ids"])
    skills, audits = [], []
    for entry in product["entries"]:
        case = cases[entry["featured_case_id"]]
        row = rows[case["id"]]
        source, audit = resolve_source(case, guides[entry["repository"]])
        source["principle"] = row["principle"]
        page = evidence(case, row)
        pages = [page]
        if case['id'] == 'mck-native-showcase':
            patch = read_json(ROOT / 'data/mck-native-fragment.json')['effect_patch']['demonstration']
            pages = [{**p, 'title':case['titles'][p['index']], 'preview_path':case['preview']} for p in patch['pages']]
        if case['id'] == 'beatdeck-showcase' and case.get('pages'):
            pages = [evidence(case, {**row, 'index':n, 'inspect':note}) for n,note in [
                (4,'混ぜる段階。工程全体を残し、いま説明する箇所を強調する。次へ一度進める。'),
                (5,'形づくる段階。同じ工程図上の強調が移る。前後へ一度ずつ動かし、対象の継続を見る。'),
                (6,'焼く段階。さらに一度進めると次の工程へ移る。15段階の往復・直接移動は原典verifyで比較済み。')]]
        proofs = source_proofs(case)
        if case['id'] == 'mck-native-showcase':
            proofs = list(dict.fromkeys([*proofs, *patch['source_proof_paths']]))
        if case["id"] in MOTION_IDS:
            verify = "生成後にHTMLを開き、前後の移動で同じ対象と説明順序を確認する。"
        elif case["format"] == "pptx":
            verify = "完成PPTXを開き、文字・図表の表示と編集できる範囲を確認する。"
        elif case["format"] == "pdf":
            verify = "完成PDFを開き、日本語・数式・図が欠けていないか確認する。"
        else:
            verify = "完成HTMLを開き、ページ移動・日本語表示・図の対応を確認する。"
        skills.append(dict(
            repository=entry["repository"], case_id=case["id"], name=row["name"],
            job="", problem=row["problem"], change=row["change"],
            when_to_use=row["when_to_use"], input=row["input"], output=row["output"], upstream=source,
            demonstration=dict(summary=row["summary"], pages=pages,
                               applied_features=row["features"], not_demonstrated=row["limits"],
                               cautions=cautions(case),
                               scope_status=CORE_STATUS.get(case["id"], "demonstrated_scope"),
                               source_proof_paths=proofs),
            how_to_use=["日本語スキルと一式ZIPを取得し、原典の実行条件を確認する。", row["edit"], verify],
            constraints=row["limits"], tags=[case["format"], *row["features"]],
            needs=need_data.get(entry['repository'], []),
        ))
        if case['id'] == 'mck-native-showcase':
            effect_patch = read_json(ROOT / 'data/mck-native-fragment.json')['effect_patch']
            skills[-1]['name'] = effect_patch['name']
            skills[-1]['change'] = effect_patch['change']
            skills[-1]['demonstration'].update(effect_patch['demonstration'])
            skills[-1]['demonstration']['pages'] = pages
        if case.get('editability_proof'):
            skills[-1]['demonstration']['editability'] = case['editability_proof']
        patch = editorial_patches.get(case['id'])
        if patch:
            if patch.get('upstream_principle'):
                skills[-1]['upstream']['principle'] = patch['upstream_principle']
            for key in ['name', 'job', 'problem', 'change', 'input', 'output', 'when_to_use', 'how_to_use', 'constraints']:
                if key in patch:
                    skills[-1][key] = patch[key]
            demo = patch.get('demonstration', {})
            for key in ['summary', 'applied_features', 'not_demonstrated', 'scope_notes', 'editability']:
                if key in demo:
                    skills[-1]['demonstration'][key] = demo[key]
            if demo.get('source_proof_paths'):
                skills[-1]['demonstration']['source_proof_paths'] = list(dict.fromkeys([*proofs, *demo['source_proof_paths']]))
            if demo.get('pages'):
                for pg in demo['pages']:
                    assert 0 <= pg['index'] < case['page_count'], (case['id'], pg)
                    assert (ROOT / pg['proof_path']).is_file(), (case['id'], pg['proof_path'])
                    pg['preview_path'] = case['preview']
                skills[-1]['demonstration']['pages'] = demo['pages']
        for key in ('constraints','how_to_use'):
            if isinstance(skills[-1].get(key), str):
                skills[-1][key] = [skills[-1][key]] if skills[-1][key].strip() else []
        if not str(skills[-1].get('job') or '').strip():
            skills[-1].pop('job', None)
        audits.append(dict(case_id=case["id"], repository=entry["repository"],
                           upstream=source, source_audit=audit,
                           evidence=page, source_proof_paths=proofs,
                           scope_status=CORE_STATUS.get(case["id"], "demonstrated_scope")))
    result = dict(version=1, updated_on="2026-10-15", index_base=0,
                  policy="原典の機能と作例で実施した範囲を分け、具体的なページと制作ソースへ接続する。",
                  skills=skills)
    (ROOT / "data/skill-effects.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(json.dumps(dict(updated_on="2026-10-15", count=len(audits),
                                         assessment="Source/metadata/path audit, not an automatic beauty score.",
                                         visually_inspected_in_this_authoring=[
                                             "sci-diagram-showcase/render/slide-02.png",
                                             "cyberppt/render/slide-03.png",
                                             "sol-editorial-showcase/render/slide-03.png",
                                             "sebastian-205/render/slide-04.png",
                                             "beatdeck-showcase/render/major-02.png",
                                             "and-scene-showcase/render/major-02.png",
                                             "quarto-talks-showcase/render/major-02.png",
                                             "presentation-forge-showcase/render/slide-02.png"],
                                         remote_source_hash_checks=remote_checks,
                                         remote_source_hash_checked_on=previous_audit.get("remote_source_hash_checked_on"),
                                         cases=audits), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(count=len(skills), exact_pinned_sources=sum(s["upstream"]["pinned_source_hash_verified"] for s in skills),
                          live_html_proofs=[s["case_id"] for s in skills if s["demonstration"]["pages"][0]["proof_kind"] == "live-html"],
                          audit_path=str(audit_path)), ensure_ascii=False))


if __name__ == "__main__":
    main()
