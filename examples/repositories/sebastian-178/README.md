# 動画一本を、教材へ。

日本語7頁の編集可能HTMLデッキ。架空・未実施の教材化企画例。

## 開く
index.htmlはCSS、OSS日本語フォント、最小navigationを内包した単一ファイルです。ネット取得なしで開けます。←/→、PageUp/PageDown、Space、横swipeでページ送り。Oで一覧、Escapeで戻る。ボタンでも操作できます。

source/index.htmlは層別CSSと自作JSを読む編集用です。文言・table・工程をHTMLで編集できます。PPTXはありません。

## 由来
NomiciAI/mbb-page-maker固定commit 36074669b8041783d9637a87dfed2a8733d47357のstarter、CSS5層＋blue theme、工程・比較表・関係構造・変換・decision logを使用。テンプレの名札だけを替えず、教材化の判断に沿ってexhibitを組み直しました。
原典runtime.js・QA/export scriptsは実行していません。自作最小navigationへ差替えた派生版で、原典の全機能・全QAとの同等性を保証しません。

## PC連携
HTTP同一originで親からyebisu-slide/index（0-based整数）を受信し、yebisu-page/indexを返します。送信元parent・origin・範囲を確認します。file://はoriginがnullのため親連携を送信しませんが、内部ナビゲーションは利用できます。外側PC連携の実環境確認はQAをご覧ください。

## ライセンス
root LICENSE Apache-2.0を維持。原典SKILLはMITを記載しており不一致があります。原文はsource/SKILL.mdへ保持。変更点はPROVENANCEに記録。Saitop at NomiciAI <saitop@nomici.ai>への既存帰属を保持。原典webfontは使わず、SIL OFLのNoto Sans CJK JPサブセットを同梱しました。

## 確認の範囲
QA.jsonに実施・未実施を記録。数値成果、公開実績、実ユーザー資料は含みません。

## 実描画
許可済ユーザーPCの既存Google ChromeとPlaywrightで7頁のPNGとPDFを出力。内部arrowとoverviewを確認。初回表示で5頁の日本語ラベル割れを修正し、対象頁を再確認しました。追加インストール・上流runtime/QA/export実行なし。PDFはPNGと同じHTMLから実出力、別個の全頁精査は未実施。


2026-10-14 字体置換: Noto Sans CJK JPは公式 notofonts/noto-cjk固定commit f8d157532fbfaeda587e826d4cd5b21a49186f7c のOTFをsource/fonts/へ未変更保存し、そこからsubset・HTML埋込みを作り直しました。OFLはsource/fonts/OFL.txt、出所はsource/FONT-SOURCE.json。旧クラウド制作記録はPROVENANCE-CLOUD.jsonに保存しています。使用326字のglyph輪郭・横幅・縦メトリクスが一致するため、既存PNG/PDFを保持しています。現在の配布物にOS抽出字体は含みません。
