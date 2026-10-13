# PPTAgent：Windowsでの実行試行

**実行試行済み・生成未達です。PPTX、完成HTML、レンダー画像はありません。**

原典の固定依存pptagent==1.1.37がWindowsをassertで明示拒否。READMEもLinux（WSL含む）/macOSを要件とする。libreofficeのWindows shimだけでは、このimport条件を解決できない。

固定commit: `833cda553b343be0e486a93b0b57cac962cdd566`。`ATTEMPT.json`に実行条件、`source/import-preflight.txt`に実際のAssertionErrorを保存しています。Docker Desktopの起動は1回だけ試し、エンジン応答が得られなかったため停止しました。この結果はLinuxでの動作失敗を意味しません。

## 対応環境での再開

Linux（WSL含む）またはmacOS、Python 3.11以降、Node/npm、`libreoffice`コマンドを用意します。原典のrequirements.txtとpackage-lock.jsonを使い、Python/Node両方のPlaywright 1.62.0とChromiumを揃えます。原典`config.example.yaml`のmultimodalモードはホストの実視認を使い、別の画像APIを必要としません。

原典CLIは `doctor → init → scaffold → review-slides → record-slide-review（各頁） → build → review-deck → record-deck-review → finalize` の順です。record-*のpassは画像を実際に確認してから記録します。最終`complete=true`とPowerPointレンダーを得るまでは生成済み作例へ登録しません。

現在の試行のみを再検証するには、カタログrootから`python tools/build_pptagent_repository_example.py`を実行します。この補助スクリプトは環境診断と記録だけを行い、依存installやDocker起動はしません。

原典root/nestedともMIT。再配布時は両LICENSEの著作権・許諾表示を保持します。
