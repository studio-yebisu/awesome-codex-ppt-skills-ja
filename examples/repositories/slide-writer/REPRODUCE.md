# 朝会は、判断と相談の入口にの日本語派生・再現キット

Python3.13、fontTools4.66.1、Brotli1.2.0、Git Bash。Node.js不要。初回に公式固定commitのBIZ UDPGothicを取得し、SHAを確認します。

1. ZIPを展開してPowerShellを開く。
2. `.\reproduce\Reproduce.ps1` を実行。新しい環境から原典の固有経路で再生成します。
3. 出力は `reproduce/workspace/examples/repositories/slide-writer/`。新出力のQAは確認前です。全ページを改めて確認してください。

原典template.htmlを複製し、Mode A1の構成・密度・コンポーネントで日本語をまとめ、無改変のbranding・inline-images・smoke-testを実行する。自作しおりテーマとlogo、OFL書体の別名サブセット、意味で区切る改行、原典revealとスクロールを用いる。file://直接起動は安全ポリシーで未確認で、原典の全工程完走とは扱わない。

表示確認は既存localhostで行います。IABではfile://直接起動が安全ポリシーに拒否されるため、その確認や原典の全工程完走は主張しません。

自分の内容にはinput/data.jsonと日本語SKILLを使い、本文・配置・停止点を原典方式で調整します。再現の詳細、原典固定commit、個別条件と確認範囲はREADME.md、PROVENANCE.json、QA.jsonを参照してください。
