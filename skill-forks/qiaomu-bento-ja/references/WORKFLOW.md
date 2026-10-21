# 原稿やデータを編集できる単体HTMLへまとめ、同じ要素を動かしながら説明できるようにする。

同梱standalone shellを通常の制作経路として使用。3→4頁は同じトークンのmorph、5頁は目標24/30の原典chartとcountUp、表紙と締めには本文に基づく図を配置した。

## 入力と出力

入力：新規作成：brief・ノート・報告・データ・参照URL。更新：原本HTML・文書JSON・安定要素ID。

出力：編集可能/閲覧用の単体Bento HTML6頁。元の文書IDを保つ再生成と各状態の実画像。

## 自分の資料へ使う

1. 新規/更新、読者、比率、オフライン範囲を決め、資料に基づくdeck-planを書く。原典同梱standalone shellと公式formatを読み、locateで確認する。
2. 新規は公式最小JSONから作り --new-document で一度だけIDを発行。更新は原本をextractし、docId・未知フィールド・要素IDを保つ。
3. 数字はchart、比較はtable、連続変化はmorph、重要数値はcountUpへ対応させる。作例で使わない画像・state slide等を実施済みとしない。
4. 元CLIで原本とは別ファイルへbuildし、更新は --identity-source 原本HTML で照合する。schema・shell・identity検査と実ブラウザーの編集/演示/保存/再表示を区別して確認する。

## 実際に使った機能

- 原典CLIがJSON schema、固定shell、原本と同じdocIdを検査し、別出力へ生成。原本を上書きしない。
- 権限確認から回答/出典へ同じIDのトークンと強調位置が移る。自然なmorphの前・途中・後を保存。
- 評価質問30件中24件以上という目標をnative chartとcountUpへ変換。漏えい0件・更新期限と、未達成の計画値である条件を分けて表示。
- 旧版で元UI編集→JSONコピー→元CLI --new-documentの独立コピー→再表示を実確認。直接保存UIの完了は未確認。生の共同編集情報は.privateに隔離。

## 未実施と条件

- 元リポのcheckoutは前提ではなく、同梱standaloneが通常経路。project側の追加validatorはcheckoutが無いため未実行。
- 画像+scrim/ken-burns、state slide、外部媒体、共同編集、実検索と権限制御は未実証。
- ブラウザーの直接「コピー保存」は完了未確認。同docIdコピーは既存状態の影響を受けたため、独立コピーは --new-document を使用した。
- countUpの初期化前に静的値が一瞬描画される原典挙動がある。途中値が増加する区間を撮影し、連続動画全フレームの品質保証とはしない。PPTX/PDF出力は対象外。

現在の再現コマンドはREPRODUCE.md、原典の条件と日本語での一般手順はSKILL.md、現在の実行・画像hashはQA.json。初回PROMPTの限定検査指示は過去の依頼で、後続修復の範囲はこの記録とsourceのRound4ログを使う。
