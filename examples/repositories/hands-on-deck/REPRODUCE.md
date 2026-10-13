# イベント案内の公開前チェックの日本語派生・再現キット

Python3.13。PowerPoint実描画にはWindows、Microsoft PowerPoint、游ゴシック・游明朝等の元書体が必要。Node.js不要。原典の追加renderにはLibreOffice/Popplerが必要ですが、標準再現では使用しません。

1. ZIPを展開してPowerShellを開く。
2. `.\reproduce\Reproduce.ps1` を実行。新しい環境から原典の固有経路で再生成します。
3. 出力は `reproduce/workspace/examples/repositories/hands-on-deck/`。新出力のQAは確認前です。全ページを改めて確認してください。

原典deck.pyのinspect・atomic JSON patch・apply・fix・diffで既存PPTXを編集する。自作日本語ドナーの図形構造を保って本文・文字サイズ・ノートを更新。元shape ID、入力と差分を残し、全ページを独立レビューする。fix advisoryと実際の見切れを区別し、新しい出力へ元QAを移さない。

`-Render`を追加すると実描画も行います。Scrollineの描画はlocalhost HTTPで行い、file://起動は行いません。

自分の内容にはinput/data.jsonと日本語SKILLを使い、本文・配置・停止点を原典方式で調整します。再現の詳細、原典固定commit、個別条件と確認範囲はREADME.md、PROVENANCE.json、QA.jsonを参照してください。
