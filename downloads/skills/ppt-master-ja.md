---
name: ppt-master-ja
description: PPT Masterの元のチェッカーとネイティブ変換器で、日本語の編集可能なPPTXを作る。PPT Master日本語版やSVGからの日本語PowerPoint制作を指定されたときに使う。
metadata:
  copyright: "Copyright (c) 2025-2026 Hugo He"
  license: "MIT"
  official_repository: "https://github.com/hugohe3/ppt-master"
  sponsors:
    - "SPONSORS.md"
    - "SPONSORS_CN.md"
  upstream: https://github.com/hugohe3/ppt-master
  upstream_commit: ca04346de145ed6462ddf34682848e71df5e20a2
---

# PPT Master 日本語版の制作経路

日本語の提案・報告は [references/japanese-business-workflow.md](references/japanese-business-workflow.md) を読む。入力・単位・前年差・講稿・PPTX実アプリ確認と当地の再現コマンドを収録。書体の変更・配布は [references/japanese-fonts.md](references/japanese-fonts.md) を参照する。

上流の[SKILL.upstream.md](SKILL.upstream.md)を参照し、文字・図形を編集できるPPTXという目的を維持する。上流の通常ルートを使う場合は、そのルーティングと計画契約に従う。

この日本語版には、カタログの作例や文字・図形中心の小規模な資料を制作する専用経路を追加している。これは上流Default Generateの全工程の実行を意味しない。上流のQuick Generate変換契約を内部で使う。外部画像、アイコン、音源を要しない日本語スライド向けであり、素材ライブラリーは同梱していない。

- references/shared-standards-core.md、executor-base.md、semantic-svg.md、preset-shape-vocabulary.mdとworkflows/profiles/quick-generate.mdの技術契約を読む。
- 1280×720のSVGをsvg_outputへ作る。日本語のNoto Sans JP、自然な改行、役割別の字号を指定。意味グループのidとdata-pptx-bounds、rootのdata-pptx-page-roleを付ける。
- scripts/svg_quality_checker.py PROJECT --quick-generate --canonical-authoring --stage final --jsonを実行する。
- 講稿をnotesに保存し、scripts/svg_to_pptx.py PROJECT --quick-generate --primary-language ja-JP --with-notes -t fade -o OUTPUT.pptxで出力する。
- チェッカーと変換器は本体を無改変で使う。画像へ丸ごと変換する代替出力を成功と扱わない。PPTX内に日本語文字、図形、講稿があることを確認する。
- ブラウザーのプレビューは変換入力SVGであり、PowerPointアプリの表示検証と区別する。PPTXの受け手にもNoto Sans JPの導入が必要。警告が残った場合は制作記録に残す。

上流のMIT原文とHugo Heの著作権表示を保持する。素材を追加する場合は、その素材ごとの利用条件も確認する。

元の帰属ガードを保持する。制作前に `python3 "${SKILL_DIR}/scripts/attribution_guard.py"` を実行する。元の著作権・ライセンス・スポンサーの表示は削除しない。

## 単体の本文から使う

この本文は `skill-forks/ppt-master-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/hugohe3/ppt-master/tree/ca04346de145ed6462ddf34682848e71df5e20a2

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `ppt-master-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: hugohe3 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/LICENSE
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/LICENSE
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/scripts/pptx_shapes/data/NOTICE.md
