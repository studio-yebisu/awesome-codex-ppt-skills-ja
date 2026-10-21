# クリック単位の表示を再現できるか

Beatdeckは発表内容をsceneとbeatへ分け、1クリックで1段階進めるスキルです。各段階は`#3.1`などのURLから直接表示でき、戻ったときにも同じ画面を再現します。

この作例では原典の`npm run verify -- --source=reference/SCRIPT.md`を実行しました。15段階を前進、15段階を後退、15段階をURLから読み直し、原典の既定値0.1%で全フレームが一致しています。文字の範囲外・文字同士の衝突、console warning/error、remote requestは0件です。presenterの接続と操作、overview、reduced motionも原典CLIの範囲で確認しました。

まず[3.1](render/verify/walk-03-01.png)、[3.2](render/verify/walk-03-02.png)、[3.3](render/verify/walk-03-03.png)を比べます。見出しを1段階ずつ変えながら、共通の工程図を同じ場所に保っています。発表では情報をまとめて出さず、話す順番に分けたいときに使います。

- [15段階のcontact sheet](render/verify/contact.png)
- [原典の実測report](render/verify/report.json)
- [実行条件と原典scriptのhash](source/VERIFY.json)
- [再生する](dist/index.html#3.1)

URLが未指定のためQRは作っていません。source照合対象のTerminal/data-exact要素は0個で、原稿全体の内容一致を機械検証した結果ではありません。全キーの手動稽古、実際のWi-Fi切断、別端末での通し確認は未実施です。自動検査とagentの画像確認は、ユーザーの美術的な承認とは区別します。

overviewの暗い背景上で文字が読みにくかったため、deck側の`theme-brand.css`にoverview限定の文字色を指定しました。原典engineとverify script、差分許容値は変更していません。
