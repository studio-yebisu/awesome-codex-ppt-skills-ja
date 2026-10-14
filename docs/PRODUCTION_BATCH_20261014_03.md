# 新作3方式と、本文をそのまま使えるスキル

2026-10-14。Sol 6.1の並列制作で新作16枚を完成し、ローカルサイトへ統合。Astraは使用していない。

| 原典 | 日本語作例 | 実際に使った方式 | 出力 |
| --- | --- | --- | --- |
| SlideSpeak/slide-design-skill | 本の向こうへ。 / 独立書店の仮リブランディング | 独自briefからtokens/chrome/6templatesを設計し、原典loadSkill・generateDeck・validateSlideTree・HTML renderer・wrapAsStandaloneHtmlを使用。Solが完成したslide-treeをLLMClientへ供給。外部API/FAL呼び出しなし | HTML6枚・PDF・代表PNG1枚 |
| liustack/pptwise | ひらく、街の作業場。 / 架空のものづくり拠点 | 原典v5 schema、Rallyテーマの派生、flowchart/hub_spoke/architecture等のcomponentsを使い、元のvalidate/render CLIでnative PPTXを生成。PPTX後加工なし | 編集可能PPTX6枚・PowerPoint PNG6枚・PDF |
| Aham-AIAPP/aham-ppt | 朝の20分を、組み直す。 / 架空ワークショップ | 原典SPC/E-03/E-04/A-90版式の固定座標・コネクタ、svg_to_native_pptxと同梱native DrawingML経路を使用。日本語書体・角丸除去・配色のみ明示変更 | 編集可能PPTX4枚・PowerPoint PNG4枚・PDF |

それぞれ入力、依頼文、固定原典、変更点、原文条件、指定OSS書体、再生成ソース、日本語派生SKILLとZIPを用意。書体は未改変の公式配布物とOFLを保持。PPTXの書体は埋め込まず、受け手への導入を案内する。

## 原典と配布条件

- SlideSpeak: `5e87d8ae71f6306e0c88f4910e6c09114581d91b`、MIT。原典sourceと独自styleを配布し、依存の原文条件も保持。
- pptwise: `65690bc705c1b5db41b5593015675945673da542`、MIT。200MBを超える全archiveの代わりに、同pinの必要sourceをsparse checkoutで取得。原典CLIのdist/src/lockと主要依存条件をキットに保持。
- Aham: `c2b4ece69bbac777557934f981457c1f98c2b73f`、MIT。原LICENSE/NOTICE/ORIGIN/派生LICENSE_NOTEをキットに保持。

最初の編集器候補jinwyp/open-ppt-skillは、root MITと第三者neo-ppt frontend・patched WASM writerを区別した。取得物で後者の再配布条件を確認できず、export・製品作例・fork・ZIPを作っていない。具体的条件は `data/sol-runtime-boundary-repository-guides.json` に記録し、現行推奨から外した。別のrendererを使用して、この原典の制作実績とは呼んでいない。

## 本文と利用導線

- 単体Markdownを共通の紹介文から、各 `skill-forks/<id>/SKILL.md` の固有手順を元にした本文へ変更。参照が一式ZIPに属すること、固定原典と原文条件を短く添える。
- スキルのページで本文を展開して読み、そのままコピーできる。Markdown取得と一式ZIPも維持。
- 初回2作例のスキルは、作例の枚数と利用者が決める枚数を区別。保守済みSKILLを再生成器が上書きせず、作品ソースZIPにも反映。
- 並列制作のfragmentは、主要生成ファイル・包装・確認記録が揃ってからサイトへ取り込む。途中のexportでサイト全体の生成を止めない。

## 確認範囲

原典の必要なbuild・gate・lint、PPTX2冊のPowerPoint初回書き出しと各表紙、HTMLの主画面を確認。親は本文表示とコピー成功、書店HTMLのフロートで1→2ページの移動を確認した。見えた第2ページの「知らない」の分断だけを、入力改行と `white-space: pre-line` で修正し、同じ箇所を確認した。

新しい3スキルのfrontmatterを簡易validatorで確認。全ページ詳細目視、独立採点、native構造監査、完全ZIP再実行は行っていない。過去の大規模QAを今後の条件にしない。

画面: `docs/assets/atelier-book-float.jpg`、`docs/assets/atelier-skill-copy.jpg`。

## 現在の状態

厳選29スキル・29冊161枚。制作履歴39リポ・44冊262枚。これは制作バッチの完了であり、全209件の実制作やプロジェクト全体完了の主張ではない。外部公開・push・merge・deployなし。

作業途中で誤った相対出力先に作った4ファイルは正しいrepo内へ移動済み。`M:/Codex/Projects/examples/repositories/pptwise-showcase/source` は空（親が確認）。空フォルダー削除は担当の自動承認レビューで `blocked by policy` と拒否され、再試行せず残した。制作物・配布キットへの影響はない。
