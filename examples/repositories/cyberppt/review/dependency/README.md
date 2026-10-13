# この例の生成用依存の補正

配布ZIPの実行時に、PptxGenJS 4.0.1が間接的に指定するimage-size 1.2.1についてnpm auditがHigh 2件を検出した。検出前後のpackage.json、package-lock.jsonと実監査結果をこのフォルダーに残す。

PptxGenJS 4.0.1は保持し、日本語派生例のpackage.jsonでimage-sizeだけを2.0.3へ固定した。これは上流コードの改変ではなく、この例の依存設定の補正。修正版は[GitHub Advisory DBのJXL/HEIF情報](https://github.com/advisories/GHSA-5p2g-fcmc-qvqq)と[ICNS情報](https://github.com/advisories/GHSA-w3rx-r6r6-pgpr)で確認した。npmの提示したPptxGenJS 4.0.0への退行やaudit fix --forceは使っていない。

補正後のlockに対するnpm auditは検出0件。この結果はその時点・そのlockの検出結果で、将来の脆弱性や他のキットの解消を保証しない。配布ZIPからの5枚再生成の互換性確認はカタログのdata/reproduction-kit-qa.jsonに別途記録する。node_modulesは配布しない。
