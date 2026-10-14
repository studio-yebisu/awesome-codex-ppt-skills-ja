---
name: business-carousel-ja
description: ai-business-skillsの43番を使い、日本語のSNSカルーセルの制作ブリーフと正方形HTMLの構成確認プレビューを作る。SNS公開用の仕上げやPowerPoint出力とは区別する。
license: MIT
---

# 日本語のカルーセルを構成確認する

原典はminhnv0807/ai-business-skillsの43-carousel-brief-global。原作者Over Powers AgencyのMIT表示と固定原文をupstreamに保持した、Studio Yebisuの日本語派生版です。

## 6枚の実例から自分の原稿へ

1. upstream/skills/en/43-carousel-brief-global/SKILL.mdを読む。原典に自動レンダラーやPPTX生成CLIはありません。
2. 題材、読む人、目的、使う場所、原稿、ブランドの色と書体を用意する。足りない事実を作らない。今回の作例は架空ブランドの教育用として明示しています。
3. 5〜7枚を目安に、入口→困りごと→気づき→解決の型→証拠または明示した作例→行動、という流れを決める。実績がなければ証言や改善率を捏造しない。
4. 1枚1論点で、原稿を図案より先に確認する。英語の単語数を日本語へ機械換算せず、短い見出し、意味のある改行、実表示で判断する。
5. 各ページの見出し・本文・図案・背景をMarkdownブリーフへ書く。色と書体を全体で揃え、入口と最後は濃色、本文は淡色にする。
6. 1080×1080のHTMLプレビューを制作する。前後の移動、ページ番号、進捗、スマホ幅を確認。日本語書体の元の条件と収録文字を確認する。
7. 原稿と全ページを実表示で確認し、人による承認と制作エージェントの確認を区別して記録する。

references/WORKFLOW.mdとreferences/recipe.jsonに、今回の日本語6枚、入力、書体、専用の制作ソース、確認範囲と再現方法があります。

## 固有の制作方式

原典43-carousel-brief-globalの指示型工程で、読み手とブランド条件、HookからCTAまでの構成、1枚1論点の原稿、図案と背景をブリーフにし、1080×1080のHTML構成確認プレビューを作る。原典に自動生成CLIやPowerPoint出力はない。SNS公開用の制作データ、人の承認、公開とは区別する。実績の証拠がない箇所は、架空の記入例を明示する。

## 原典の制作段階を保つ

この出力は構成確認用です。SNS公開用の制作ファイル、縦長版、LinkedIn投稿PDFなどは、原典の次の工程としてCanva/Figma/Adobe Express等で仕上げます。人の承認と公開を未実施のまま完了扱いにしません。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 単体の本文から使う

この本文は `skill-forks/business-carousel-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/minhnv0807/ai-business-skills/tree/0360adced422a08f70c3eff8905b81962872105d

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `business-carousel-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: minhnv0807 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/minhnv0807/ai-business-skills/blob/0360adced422a08f70c3eff8905b81962872105d/LICENSE
