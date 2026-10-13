# Japanese Corporate PPTX Agent Skill

日本企業、業界団体、官公庁、大手メーカーの会議資料でよく見る
「情報量のある一枚図」「ポンチ絵」を、**編集可能なPowerPoint部品**
として作るためのAgent Skillです。

![15種類の編集可能なレイアウト](skills/japanese-corporate-pptx/assets/japanese-corporate-ponchi-layouts.png)

## できること

- JEITA風、経産省風、霞ヶ関ポンチ、JTC風の情報設計
- 技術ロードマップ、レイヤー図、関係者図、事業スキーム、業務フロー
- 現状→変革→目指す姿、判断表、論点管理表、引用グラフへの注釈
- 経歴・会社・事業紹介、法人研修、個別指導などの紹介ページ
- 出所、注記、前提、判断事項まで一枚で閉じる資料
- 参考画像の丸写しを避け、構造を組み替えたオリジナル設計

テンプレートは15レイアウト入りです。タイトル、本文、図形、矢印、
表、グラフ、注釈、出所はPowerPoint上で編集できます。実写写真、
スクリーンショット、ロゴ、原典抜粋だけは必要に応じて画像として
扱います。

## インストール

### GitHub CLI

`gh skill`を利用できる環境では、次のコマンドでユーザー領域へ
インストールできます。

Codex:

```bash
gh skill install gonta223/japanese-corporate-pptx-skill japanese-corporate-pptx \
  --agent codex \
  --scope user
```

Claude Code:

```bash
gh skill install gonta223/japanese-corporate-pptx-skill japanese-corporate-pptx \
  --agent claude-code \
  --scope user
```

`gh skill`が見つからない場合は、GitHub CLIを最新版へ更新するか、
次の手動インストールを使ってください。

### 手動インストール

```bash
git clone https://github.com/gonta223/japanese-corporate-pptx-skill.git
```

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R japanese-corporate-pptx-skill/skills/japanese-corporate-pptx \
  ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R japanese-corporate-pptx-skill/skills/japanese-corporate-pptx \
  ~/.claude/skills/
```

その他のAgent Skills互換クライアントでは、
`skills/japanese-corporate-pptx/`をそのクライアントのSkillディレクトリへ
配置してください。

## 使い方

Skill名を指定し、用途、相手、会議、結論、必要な根拠、納品形式を
伝えます。

```text
$japanese-corporate-pptx を使って、
製造業の経営会議向けに「生成AI導入の全体像」を1枚で作って。
利用部門、データ、モデル、計算資源、セキュリティの関係を示し、
最後に経営が決める事項を置いて。PPTXで、全要素を編集可能にして。
```

```text
$japanese-corporate-pptx を使って、添付画像を参考に
技術ロードマップを作って。参考資料の丸写しはせず、
マクロ構成、読む順番、強調位置を変えてオリジナルにして。
数値は一次情報で確認し、出所と基準日を入れて。
```

```text
$japanese-corporate-pptx を使って、
会社紹介、法人研修、個別指導、AI実装・発信の4要素を
1枚のプロフィールページにまとめて。
写真は提供素材だけを使い、実績を捏造しないで。
```

```text
$japanese-corporate-pptx を使って、
このPDFのグラフを引用した判断資料を作って。
原典グラフは画像のまま保持し、結論帯、転換点マーカー、
解釈、判断事項、加工注記は別々の編集可能な部品にして。
```

### 指示に含めると精度が上がる情報

- 読み手と会議の種類
- 一枚で理解、議論、決定、承認してほしいこと
- 必ず入れる組織、工程、レイヤー、数字、例外
- 参考にするPPTX、PDF、画像、公式資料
- 確定、推計、提案、要確認の区分
- 使用可能な写真、ロゴ、スクリーンショット
- 納品するスライド数と期限

## 編集可能性のルール

このSkillでは「見た目だけ似た一枚画像」は完成扱いにしません。

- 文字はテキストボックス
- 箱、矢印、マーカーは図形またはコネクタ
- 比較表と論点表はネイティブ表
- 検証済みの数値グラフは編集可能なネイティブグラフ
- 追加した結論、翻訳、注釈、出所は独立オブジェクト

写真、実画面、ロゴ、忠実性が必要な原典抜粋は画像で構いません。
ただし、その上に追加する解釈や注釈まで画像へ焼き込まないでください。

## 必要な環境

- Agent Skillsを読み込めるAIエージェント
- PowerPointをネイティブ編集・書き出し・レンダリングできるツール
- 参考資料を調べる場合はWebまたはPDFを閲覧できる環境

利用中のエージェントがスライド画像しか生成できない場合、このSkillは
編集可能なPPTXを保証できません。その場合は画像で代用せず、PPTX対応の
ツールを用意してください。

## 同梱ファイル

```text
skills/japanese-corporate-pptx/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── japanese-corporate-ponchi-template.pptx
│   ├── japanese-corporate-ponchi-layouts.png
│   └── annotated-source-chart-layout.png
└── references/
    ├── jtc-authenticity.md
    ├── layout-catalog.md
    ├── qa-checklist.md
    ├── research-backed-patterns.md
    ├── visual-style.md
    └── writing-and-density.md
```

## 著作権・オリジナリティ

このSkillは、日本の企業・業界団体・官公庁資料に共通する
「情報設計の文法」を研究対象にしています。特定資料の文章、数値、
図版、アイコン、ロゴ、固有の配置を無断で複製するためのものでは
ありません。

- 一つの参考画像を使う場合は、マクロ構成、読む順番、強調位置、
  注釈形状、色の役割などを複数変更します。
- 原典を証拠として使う場合は、引用範囲、出所、ページ、加工内容を
  明記します。
- 同梱テンプレート3枚目の人物写真は架空人物による説明用サンプルです。
  実案件や実績の証拠として使わないでください。
- JEITA、経済産業省、その他の官公庁・業界団体とは無関係であり、
  各組織による公式配布・推奨ではありません。

## ライセンス

MIT Licenseです。詳しくは[LICENSE](LICENSE)を参照してください。
