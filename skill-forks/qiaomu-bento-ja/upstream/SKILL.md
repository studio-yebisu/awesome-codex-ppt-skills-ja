---
name: qiaomu-bento-ppt
description: |
  Use the standalone qiaomu-bento-ppt skill to create or edit qiaomu-style bento presentations as self-contained .bento.html files from briefs, notes, reports, URLs, data, or existing bento decks. Use this skill when the user explicitly asks for bento/slides, a .bento.html deck, an offline-editable single-file HTML presentation, or invokes qiaomu-bento-ppt. It applies a proposal-first presentation workflow, ships a pinned official bento shell and authoring references inside the skill, builds through the plaintext #bento-doc contract without requiring the original bento repository, and validates structure, identity, shell integrity, visual heuristics, and rollback boundaries. Do not use for conventional .pptx delivery, generic bento source development, or bento/spaces and bento/dash work.
metadata:
  author: 向阳乔木
  copyright: Copyright (c) 向阳乔木
  upstream: https://github.com/nyblnet/bento
---

# qiaomu bento ppt

把资料转成可编辑、可演示、可离线分发的单文件 bento/slides deck。

## Router Rules

- 触发：用户明确提到 `bento`、`.bento.html`、单文件 HTML 演示文稿、离线可编辑 deck，或点名 `$qiaomu-bento-ppt`。
- 近邻：只说“做 PPT”且未指定格式时，优先使用通用 PPT skill；先确认是否接受 bento 格式。
- 不触发：明确要求 `.pptx`、Keynote、Google Slides；开发 bento 平台源码；制作 bento/spaces、bento/dash 或 bento/vault。
- 编辑已有 deck 时保留 `docId`、未知字段、collab 数据和原始 HTML shell；只改 `#bento-doc`。
- 新建 deck 时只生成一次 `docId`。禁止把既有文档当“新文档”重新生成身份。
- 不发布、不部署、不签名，不读取 `~/.bento/release-key.json`。

## Required Sources

开始制作前读取 [references/workflow.md](references/workflow.md) 和
[references/upstream-contract.md](references/upstream-contract.md)。

本 skill 自带固定版本的官方资料，按顺序读取：

1. `references/upstream/bento-official-skill.md`
2. `references/upstream/bento-agents.md`
3. `references/upstream/bento-format.md`

当前固定 release、commit、文件来源与 SHA-256 记录在
`upstream.lock.json`。普通 deck 任务禁止临时联网换最新版；只有用户明确提出
维护/同步上游时，才运行：

```bash
python3 scripts/sync_upstream.py --report reports/upstream-sync-check.json
```

需要刷新时加 `--update`。脚本只接受同一个官方 GitHub release 的完整快照，
全部暂存并验证后才替换；随后必须重跑 standalone、identity、shell、fixture 和
browser gates。定期 GitHub workflow 只创建 PR，不直接更新 `main`。

用下面的命令检查独立资产：

```bash
python3 scripts/bento_deck.py locate
```

正常结果必须包含 `"standalone": true`。原始 bento checkout 不是前置条件；
只有更新兼容性检查时才可选传入 `--repo`。

## Compact Workflow

1. **判定交付物**：确认新建还是编辑、语言、受众、场景、时长、比例、是否必须完全离线，以及用户是否明确要求跳过方案确认。
2. **先做方案**：广义主题先给 `1a / 2b / 3c` 选择卡和默认建议；形成 source-grounded `deck-plan.md`。用户说“直接生成/跳过确认”时可继续。
3. **读取官方规范**：使用 skill 内置的官方 bento skill/agent/format 快照，禁止凭记忆发明字段。
4. **提取或起草 JSON**：
   - 编辑：`python3 scripts/bento_deck.py extract input.bento.html --output deck.json`
   - 新建：从官方最小文档骨架起草；不带 `collab`、`template`、`readonly`。
5. **内容映射**：数字→chart，规格/对比→table，连续变化→morph，展开细节→state slide，主视觉→image+scrim+ken-burns，流程→path/dash-march，关键数字→countUp。
6. **构建新文件**：默认不覆盖任何输入。

```bash
python3 scripts/bento_deck.py build deck.json \
  --output result.bento.html \
  --new-document \
  --report reports/deck-validation.json
```

编辑已有 deck 时去掉 `--new-document`，用原文件同时锚定身份和 shell：

```bash
python3 scripts/bento_deck.py build deck.json \
  --identity-source input.bento.html \
  --output input.updated.bento.html \
  --report reports/deck-validation.json
```

脚本会拒绝 `deck.json` 与原文件 `docId` 不一致的构建。只有用户明确要求时
才加 `--overwrite`。

7. **验证**：结构校验、bento shell gate、真实浏览器打开、编辑态与演示态检查。视觉任务不能只以脚本通过作为完成证据。
8. **交付**：给出 `.bento.html`、`deck-plan.md`、可选 `deck.json`、验证结果和仍属 `missing evidence` 的项目。

## Authoring Rules

- 默认 1280×720；遵循实际 `doc.size`。常规内容保留约 96px 侧边距。
- 每页一个视觉主语；画面与字幕/正文不要完整复读同一句。
- 一套主色、最多两套字体。不要用左侧彩色竖线、默认网格或施工线制造廉价层级。
- 使用真实图片、图标和数据；外部 URL 媒体会破坏离线承诺，必须明确说明。
- 同一对象跨页变化时使用稳定、确定性的 id；同一页的有效 morph key 不得重复。
- 每页写 speaker notes。控制文字密度，数字能图表化时不要堆文字。
- chart option 必须是纯 JSON；bar/line 数据用纯数字；禁止函数 formatter。
- 写入文档块时所有 `<` 转义为 `\u003c`，文档块中不得出现字面 script 结束标签。

## Gate Ladder

- **Route gate**：触发和近邻边界通过 `evals/trigger_cases.json`。
- **Structure gate**：`scripts/bento_deck.py validate` 无 error。
- **Shell gate**：生成文件必须通过内部 gate；可选 checkout 存在时再跑其 `scripts/shell-gate.mjs` 做兼容性复核。
- **Identity gate**：编辑时 `docId` 与源文件一致；新建时只 mint 一次。
- **Quality gate**：无越界、关键文字过小、空 notes、断链、无动效等未解释 warning。
- **Browser gate**：真实打开后检查封面、至少一页内容页、演示模式、字体/图片/图表和无横向溢出。
- **Rollback boundary**：默认写新文件；源 `.bento.html` 与源资料保持不变。
- **Upstream gate**：`upstream.lock.json` 与四个内置快照的 SHA-256 必须一致；自动同步只能开 PR，合并前仍需浏览器复核。
- 缺少浏览器、人工审阅、外部媒体可用性或发布安装证明时标为 `missing evidence`，不得写成“已验证”。

## Output Contract

1. `deck-plan.md`：受众、目标、叙事弧、逐页结构、素材映射、视觉方向、证据来源。
2. `deck.json`：纯 `bento/slides` 文档数据；编辑场景保留身份和未知字段。
3. `<title>.bento.html`：可独立打开、编辑和演示的单文件交付物。
4. `reports/deck-validation.json`：errors、warnings、shell gate 和身份结果。
5. 简短交付说明：路径、页数、离线边界、已验证项、`missing evidence`。

## Permissions And Exclusions

- 允许：读取用户指定资料和 skill 内置 shell/规范；在任务输出目录写计划、JSON、报告和新 deck；运行 Python 校验与本地浏览器。
- 需用户明确授权：手动联网更新 shell/规范、覆盖既有 deck、把大型媒体改成外链、修改 bento 项目源码。仓库维护者启用的定期同步 workflow 仅限官方 release 元数据和快照，并只创建待审 PR。
- 禁止：发布/部署/release、触碰签名密钥、向 `main` 直接推送、把 token/cookie/账号写入 deck 或报告。

版权与联系：Copyright (c) 向阳乔木 ·
[X](https://x.com/vista8) · [GitHub](https://github.com/joeseesun/)
