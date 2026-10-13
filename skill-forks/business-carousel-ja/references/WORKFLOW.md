# minhnv0807/ai-business-skillsの日本語制作

原典: https://github.com/minhnv0807/ai-business-skills/tree/0360adced422a08f70c3eff8905b81962872105d

原典43番 / 構成ブリーフ→1080×1080のHTMLプレビュー

原典43-carousel-brief-globalの指示型工程で、読み手とブランド条件、HookからCTAまでの構成、1枚1論点の原稿、図案と背景をブリーフにし、1080×1080のHTML構成確認プレビューを作る。原典に自動生成CLIやPowerPoint出力はない。SNS公開用の制作データ、人の承認、公開とは区別する。実績の証拠がない箇所は、架空の記入例を明示する。

## 作例

- 引き継ぎ、何を書けばいい？ / 6枚 / html
- カタログ内の案内: repository.html?repo=minhnv0807/ai-business-skills
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=minhnv0807/ai-business-skills
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13 / fontTools / Brotli（この作例の再現）
- HTTPで表示できるブラウザー
- 公式BIZ UDPGothicのOFL書体（固定版を取得・サブセット化）

## 元の制作コマンド

    python tools/build_business_carousel_repository_example.py --input examples/repositories/business-carousel/input/data.json

## 確認範囲

- 原典43番のHTMLは構成確認用。Canva/Figma等のSNS公開用仕上げ、縦長版、LinkedIn投稿PDFは未制作。
- 実績の証拠がないため、架空の記入例を明示。SNSの反応や改善効果は測定していない。
- 人による原稿・コンセプトの承認と投稿は未実施。今回の確認は制作エージェントの判断。
- 日本語の短さは字数と実表示で調整。英語の8語・25語を日本語へ機械換算しない。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
