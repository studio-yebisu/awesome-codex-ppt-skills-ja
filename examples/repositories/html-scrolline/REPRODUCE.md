# 小さな展示を、ひらくまでの日本語派生・再現キット

Python3.13の標準ライブラリ、Node.js22以上、npm。描画にはインストール済みChrome/Edge。原典npm lockから依存を用意し、GSAP独自条件とMIT表示を保持します。

1. ZIPを展開してPowerShellを開く。
2. `.\reproduce\Reproduce.ps1` を実行。新しい環境から原典の固有経路で再生成します。
3. 出力は `reproduce/workspace/examples/repositories/html-scrolline/`。新出力のQAは確認前です。全ページを改めて確認してください。

原典deck.yaml・plan・Vite build・Scrolline engineとrail-advance/era-shiftで6停止点を連続的につなぐ。engine/moves/conceptsは原典と一致。内部localeはen、HTMLの表示は日本語。Windows Chrome探索だけを明示adapterで補正する。原典全体CIのWindowsパス3件不合格を保持し、HTTP上のcore・smoke・操作確認と分ける。GSAP独自条件と各MITの原文通知を分けて保持。

`-Render`を追加すると実描画も行います。Scrollineの描画はlocalhost HTTPで行い、file://起動は行いません。

自分の内容にはinput/data.jsonと日本語SKILLを使い、本文・配置・停止点を原典方式で調整します。再現の詳細、原典固定commit、個別条件と確認範囲はREADME.md、PROVENANCE.json、QA.jsonを参照してください。
