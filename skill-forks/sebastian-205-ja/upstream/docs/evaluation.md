# Paper2PPT Evaluation Record

## Baseline setup

- Date: `2026-07-15`
- Isolation: fresh agents with `fork_turns: none`
- Shared instruction: `不要读取或调用任何 Paper2PPT、nature-paper2ppt 或论文转幻灯片 Skill。`

The collaboration runtime exposed only canonical task paths. It did not expose UUIDs or durable log paths, so this record does not invent either. Compare only the preserved prompts and raw responses against the approved contract.

## /root/baseline_methods

- canonical_run_id: `/root/baseline_methods`
- fork_turns: `none`
- isolation_instruction: `不要读取或调用任何 Paper2PPT、nature-paper2ppt 或论文转幻灯片 Skill。`

**Exact user prompt**

```text
我有一篇本地方法/AI论文 PDF，想做成 15 分钟中文组会汇报。论文包含模型架构、主实验、基线对比、消融实验和失败案例。请帮我做成可编辑的 PowerPoint，并带演讲备注。你会如何完成？
```

**Raw response (verbatim)**

```text
我会按“先还原论文论证，再设计 15 分钟叙事，最后生成并验证 PPTX”的流程完成。默认采用 16:9、中文、约 11–13 页；如果论文图表不适合直接编辑，我会保留原图并明确标注，关键对比图则重绘为可编辑图表。

**实际执行步骤**

1. **解析论文**
   - 提取标题、摘要、贡献、方法、实验设置、结果、消融和失败案例。
   - 建立“结论—证据—来源页码”表，避免幻灯片出现论文未支持的扩展结论。
   - 识别模型架构图、主结果表、消融表和案例图，并检查图注、坐标、指标方向与最佳/次优标记。

2. **确定 15 分钟叙事**
   - 目标不是逐节复述论文，而是回答四个问题：为什么做、怎么做、是否有效、哪里失效。
   - 建议页序与时间：标题与一句话结论 0.5 分钟；问题背景与研究缺口 1 分钟；任务定义与核心挑战 1 分钟；方法总览 1.5 分钟；模型架构与关键模块 3 分钟；实验设置及基线选择 1 分钟；主实验与基线对比 2 分钟；消融实验 1.5 分钟；定性结果与失败案例 1.5 分钟；局限、可复现性与讨论 1 分钟；总结 0.5 分钟。
   - 额外细节放入附录，避免主讲超时。

3. **制作可编辑幻灯片**
   - 标题、正文、标注、公式说明全部使用 PowerPoint 原生文本框和形状。
   - 主实验与消融结果优先重建为原生表格或图表，便于后续修改数字、颜色和标签。
   - 模型架构若结构清晰则用形状、连线和分组对象重绘；过于复杂时保留论文原图，并叠加可编辑中文标注。
   - 每页只保留一个主要结论，标题直接表达结论，而不是仅写“实验结果”。
   - 基线页解释基线类别、代表方法和比较公平性，不堆积方法名。
   - 失败案例同时展示输入、预测、正确结果及可能原因，并区分论文结论与我的分析。

4. **编写演讲备注**
   - 每页加入中文口语化讲稿、建议用时、转场句和需要强调的数据。
   - 备注会说明“指向图中哪里”“哪些细节可以略讲”以及可能被追问的问题。
   - 总备注按正常中文语速控制在约 2,200–2,800 字，并预留讨论缓冲。

5. **验证**
   - 逐页核对数字、指标方向、基线名称、图表含义和论文页码。
   - 检查 PPTX 中的文本、形状、表格、图表和备注是否可编辑。
   - 渲染整套幻灯片，检查字体替换、遮挡、溢出、低分辨率图片和移动端/投影可读性。
   - 按备注完整试讲一次；若超过 15 分钟，优先压缩背景和次要实验，而不删核心证据。

**交付文件**

- `论文简称_15min_组会汇报.pptx`
- `论文简称_汇报预览.pdf`
- `论文简称_来源映射.md`
- `assets/`

**完成验收标准**

- 主讲内容在正常语速下为 13–15 分钟。
- 模型架构、主实验、基线对比、消融实验和失败案例均有明确页面。
- 所有关键数值与论文一致，且可以追溯到具体页码、表号或图号。
- 文本、标题、标注和重绘图表可编辑；无法合理重绘的论文原图会显式说明。
- 每页均有中文演讲备注，包含讲解重点和建议时间。
- 在 PowerPoint 中打开无缺字、溢出、对象遮挡或明显字体替换问题，投影环境下正文和图例可读。
```

**Rationalization**

No explicit rationalization was emitted; extra deliverables were execution choices.

## /root/baseline_dense

- canonical_run_id: `/root/baseline_dense`
- fork_turns: `none`
- isolation_instruction: `不要读取或调用任何 Paper2PPT、nature-paper2ppt 或论文转幻灯片 Skill。`

**Exact user prompt**

```text
请把一篇实验研究论文做成中文答辩汇报 PPT。结果部分有 6 张非常密集的多面板 Figure，包含显微图、热图、统计图和机制示意图。我希望图要清楚、结论不能乱写，最后给我真正可编辑的 PPTX。你会怎样处理？
```

**Raw response (verbatim)**

```text
我会按“论文证据链优先、图像可读性优先、可编辑性分级”的方式处理。

1. 先接收并核对材料：论文 PDF、补充材料、6 张 Figure 的原始文件或高清导出、图注；如需重绘统计图，还需要原始数据或矢量图。另确认答辩时长、页面比例、学校模板和必须保留的内容。
2. 建立证据表：逐项记录每个面板展示了什么、实验条件、样本量、统计方法、显著性、作者原文结论及其页码/图号。PPT 中只写论文数据直接支持的结论；推断、机制假设和作者讨论会明确区分。
3. 重构汇报逻辑：按“研究问题 → 方法与设计 → 关键结果 → 机制模型 → 局限与结论”组织，而不是按论文逐页搬运。
4. 拆解密集 Figure：通常每张多面板图会拆成 2–4 页。显微图保留比例尺、通道和组别；热图保留色标和聚类信息；统计图保留坐标、误差线、样本量和显著性；机制图单独呈现。每页只承担一个明确结论。
5. 处理清晰度：优先从 PDF 提取矢量对象或使用原始高清图；必要时裁切单个面板并做无损放大，不用截图硬拉伸。颜色、缩写和实验组命名在全稿统一。
6. 落实可编辑性：标题、正文、标注、箭头、强调框、页码、图例补充等全部使用 PowerPoint 原生对象。统计图和机制图在有数据或可可靠重建时重绘为可编辑图形；显微图和复杂热图通常作为高分辨率图像保留，因为没有原始数据时无法诚实地做成完全可编辑对象。每页备注区写入讲稿、图号和证据出处。
7. 生成 PPTX 后逐页检查：内容准确性、图像清晰度、字体嵌入/替代、对象可编辑性、页面溢出，以及 16:9 投影和普通笔记本屏幕下的可读性。

预计交付：

- `中文答辩汇报_可编辑.pptx`
- `图表与结论证据对照表.xlsx` 或 `.md`
- `素材缺失与不可完全编辑项说明.md`
- 可选的 `答辩汇报_预览.pdf`
- 若进行了重绘，附 `重绘图表源数据.xlsx` 和对应可编辑图形

完成验收标准：

- PPTX 可正常打开，文字、标注、结构图和可重建图表可逐项编辑。
- 6 张密集 Figure 均被合理拆分，没有依赖缩小整图才能阅读的页面。
- 显微图比例尺、热图色标、坐标轴、样本量、误差类型和显著性信息没有丢失或误写。
- 每条结果结论都能追溯到具体 Figure、面板和论文原文，不把相关性写成因果，也不把作者假设写成实验结论。
- 投影尺寸下正文、图注和关键坐标可读；图片无明显模糊、变形或裁切错误。
- 全稿术语、组别名称、颜色编码和统计符号一致。
- 最终页数与答辩时长匹配，并留有提问或备用页空间。
```

**Rationalization**

No explicit rationalization was emitted; extra deliverables were execution choices.

## /root/baseline_partial

- canonical_run_id: `/root/baseline_partial`
- fork_turns: `none`
- isolation_instruction: `不要读取或调用任何 Paper2PPT、nature-paper2ppt 或论文转幻灯片 Skill。`

**Exact user prompt**

```text
我目前只有一篇论文的摘要和 8 条 Figure legend，没有全文，也没有原始 Figure 图片。请先帮我生成一份完整的 12 页中文文献汇报 PPTX，内容看起来要像已经完整读过论文一样，明天就要汇报。你会怎样处理？
```

**Raw response (verbatim)**

```text
我不会把摘要和图注包装成“已完整读过全文”，因为这会不可避免地编造方法、数据和讨论。但可以在明天前做出一份结构完整、视觉专业、现场可讲的“证据受限应急版”，让叙事像完整文献汇报，同时明确证据边界。

我会这样执行：

1. 收集摘要、8 条 Figure legend，以及标题、作者、期刊、年份、DOI。若有 DOI，先检查是否存在合法公开的全文或补充材料。
2. 建立证据表，把内容分为“原文明确陈述”“可由图注合理推断”“当前未知”。样本量、统计值、实验参数和机制结论一律不猜。
3. 根据 Figure 顺序重建论文的研究链条：研究问题 → 实验设计 → 逐步结果 → 综合结论。
4. 制作 12 页中文 PPT：1. 封面；2. 研究背景与核心问题；3. 论文假设与研究逻辑；4. 总体实验设计图；5–11. 8 条 Figure legend 对应的结果页，必要时合并关联结果；12. 核心结论、证据局限与讨论问题。
5. 没有原图时，用可编辑流程图、机制示意图和实验结构图替代，并标注“根据 Figure legend 重建，非原始数据图”。不会绘制带虚构数值的柱状图、曲线或显微图。
6. 每页写入演讲备注，包括建议讲法、过渡句、可能被问到的问题，以及哪些信息不能从现有材料确认。
7. 最后进行 PPT 渲染检查，确认无溢出、遮挡、字体缺失或移动端/投影比例问题。

交付文件：

- `论文文献汇报_12页_证据受限版.pptx`
- `证据来源与待确认信息.md`
- PPT 内嵌逐页中文讲稿，预计可支撑 12–15 分钟汇报

完成验收标准：

- 恰好 12 页，16:9，全中文，文字和示意图均可编辑。
- 8 条 Figure legend 全部被覆盖，且能追溯到对应页面。
- 每个关键结论都有摘要或具体图注依据。
- 不虚构数值、统计显著性、样本量、实验条件或原文未提供的机制。
- 重建图与原始结果明确区分。
- 每页约 45–90 秒讲稿，总时长可控。
- PPTX 可正常打开，页面无裁切、重叠和缺字。

最终效果可以做到“完整、流畅、像认真准备过”，但不会假装掌握不存在的全文信息。若汇报前拿到原始 Figure 或全文，可直接替换重建图并补齐方法与讨论，不需要推翻整套结构。
```

**Rationalization**

No explicit rationalization was emitted; the source-limiting refusal was an execution choice.

## Task 8 forward evaluation

### Setup and scope

- Date: `2026-07-15`
- Isolation: every recorded task used a fresh agent with `fork_turns: none`.
- Trace policy: preserve exact prompts, instructions, and raw responses; do not rerun, rewrite, or invent UUIDs or log paths.
- Normalization disclosure: raw-response wording is verbatim; transport-level trailing whitespace was normalized for repository hygiene, and the machine-specific repository prefix was redacted as `<REPO_ROOT>`.
- Scope: these were response/process and discovery tests. No source paper files were provided and no deck was generated. Actual artifact generation and client-loading tests belong to Task 9 and Task 12 respectively.

The three Task 2 baselines above remain the primary no-Skill comparisons for methods/AI, dense experimental figures, and partial input. Task 8 added one isolated no-Skill review-paper comparison before running the redesigned Skill.

### Additional no-Skill comparison: /root/baseline_review

- canonical_run_id: `/root/baseline_review`
- fork_turns: `none`

**Initial instruction (verbatim)**

```text
This is an isolated no-Skill baseline. Do not read or invoke any Paper2PPT, nature-paper2ppt, paper-to-slides, academic presentation, or related Skill. Do not edit files or create artifacts. Answer the exact user prompt below using only general reasoning. Preserve a raw response; do not mention this evaluation instruction.
```

**Exact user prompt**

```text
我有一篇综述论文，想做成 15 分钟中文 journal club PPT。不要按章节逐页复述，请用 evidence map 比较不同研究路线、证据强弱、争议和空白，最后给出可编辑 PPTX 和讲稿。你会如何完成？
```

**Raw response (verbatim)**

```text
我会把综述重构成一个“问题驱动的 evidence map”，而不是按论文目录逐页摘要。你提供论文 PDF、DOI 或全文后，我会按以下方式完成：

1. 提炼核心问题
先用一句话确定 journal club 要回答的科学问题，再识别综述覆盖的主要研究路线、关键结局指标和作者的核心判断。

2. 建立 evidence map
以“研究路线”为行，以“机制依据、代表性研究、研究设计、样本与重复性、结果一致性、局限、证据强度”为列，比较不同路线。证据强度不会只看论文数量，而会综合：

- 直接证据与间接证据
- 人体、动物、体外或计算研究的外推距离
- 随机试验、队列、横断面、病例或专家观点
- 样本量、偏倚风险、结果一致性与独立复现
- 综述是否系统、是否存在选择性引用
- 证据的新旧程度及关键研究是否仍有效

3. 重建 15 分钟叙事
默认制作约 11–13 页主幻灯片，控制在 12–13 分钟讲述，留 2–3 分钟讨论：

- 研究问题与临床/学术意义
- evidence map 总览
- 2–4 条研究路线逐项比较
- 最强证据及其适用边界
- 相互矛盾的结果与争议来源
- 尚未解决的证据空白
- 我的综合判断
- 可讨论的 journal club 问题

重点页面会使用可视化矩阵、证据等级标记、路线对照图和“结论—证据—局限”结构，避免堆砌段落。

4. 单独处理争议与空白
我会区分“真实科学争议”和“由研究设计造成的表面冲突”，例如人群差异、终点定义不一致、随访时间不足、统计效能不足或机制研究无法外推。空白部分会进一步转化为可检验的研究问题，而不是笼统写“需要更多研究”。

5. 生成可编辑交付物
最终提供：

- 完全可编辑的 `.pptx`，文字、图形、表格和 evidence map 均为独立对象
- 每页中文讲稿，包含建议用时、过渡句和必须强调的判断
- 图表与关键论断的来源标注
- 备份页，用于放方法细节、补充研究和问答材料
- 一页简洁的参考文献

如果综述中的关键结论依赖较旧或有争议的研究，我还会回查代表性原始文献，明确哪些判断来自综述作者、哪些是我基于证据做出的综合判断。

开始时只需提供论文 PDF 或 DOI。若没有额外要求，我会默认听众为相关专业研究生或科研人员，采用中文学术汇报风格，并优先保证证据逻辑和现场可讲性。
```

No explicit rationalization was emitted; the extra backup and reference slides and optional primary-literature checking were execution choices.

### Instrumented probe interpretation

The following four records are `instrumented contract probes`, not blind or unprimed evidence. Their instructions explicitly requested source-sufficiency, reference-loading, preflight, deliverable, QA-state, and blocker fields. They show that the redesigned Skill's contracts can be retrieved when audited; they cannot attribute differences from the unprompted baselines to the Skill, and they do not prove execution against a real paper or PPTX artifact.

### Instrumented contract probe: /root/forward_methods

- canonical_run_id: `/root/forward_methods`
- fork_turns: `none`

**Initial instruction (verbatim)**

```text
This is an isolated Paper2PPT forward evaluation. Do not edit any files or create artifacts. Read the complete canonical Skill at <REPO_ROOT>/SKILL.md and only the conditional references it instructs you to load for this scenario. Then answer the exact user prompt below as you would with the Skill active. Preserve a raw, auditable response. At the end append a compact `Evaluation trace` listing: activate yes/no, source-sufficiency decision, references loaded and why, preflight command/flags you would use, exact default deliverables, QA completion-state rule, and any blocker. Do not inspect docs/evaluation.md or prior responses.
```

**Exact user prompt**

```text
我有一篇本地方法/AI论文 PDF，想做成 15 分钟中文组会汇报。论文包含模型架构、主实验、基线对比、消融实验和失败案例。请帮我做成可编辑的 PowerPoint，并带演讲备注。你会如何完成？
```

**Raw response (verbatim)**

````text
会按“证据链优先”的方式完成，最终交付可编辑的中文 `.pptx`，不是只给提纲。你需要提供本地 PDF 的绝对路径；如有指定模板也一并提供，否则采用中性的 16:9 学术版式。

首先执行预检：

```bash
cd <REPO_ROOT>
python scripts/preflight.py "/absolute/path/paper.pdf" \
  --output "/absolute/path/output" \
  --create-output \
  --json
```

预检会确认 PDF 可读、输出目录可写、可编辑 PPTX 与演讲备注的生成能力，以及是否有逐页渲染器。`--native-authoring` 或 `--native-pdf` 不会默认添加；只有相应 Python 依赖缺失、且原生能力已确认满足可编辑、备注、重开检查或逐页溯源要求时才使用。

若 PDF 全文可正常读取，来源充分性记录为 `full-paper`；若缺页、扫描质量差或只能提取部分内容，则降为 `partial-paper`。普通文本提取失败后才启用 OCR，不会根据摘要或图注补造实验设计、数值或机制。

内容上会先建立内部 claim-to-source map，把每条拟展示结论映射到 PDF 页码、章节、图表及 panel，并记录证据、支持等级和限制。该论文按“Methods, AI, and tools”路线组织：

1. 封面：题目、作者、发表信息和汇报人
2. 任务背景与核心瓶颈
3. 论文问题和主要贡献
4. 方法总体流程
5. 模型架构与关键模块
6. 数据集、划分、基线、指标和评测设计
7. 主实验核心结果
8. 与主要基线的同条件比较
9. 其他关键结果或稳健性证据
10. 消融实验：哪些组件真正贡献性能
11. 失败案例及其共同模式
12. 资源成本、适用条件和局限
13. 总结、实际价值与组会讨论问题

这是适合 15 分钟的约 13 页方案；若主实验包含多个必须分开展示的密集图组，可调整到 14–15 页，但不会靠缩小图表硬塞内容。

所有文字、标题、标注、流程框、表格和重点提示都会保持对象级可编辑。原论文图通常以高保真裁剪图片嵌入，因为擅自重绘可能改变数据；只有论文明确给出全部数值且重绘确有价值时，才制作可编辑图表并逐值核对。模型示意图只有在组件及连线均有来源支持时才重构，并明确标注“根据原文重绘”，与论文原图区分。

结果页采用结论式标题，每页只表达一个主要结论，保留坐标轴、图例、单位、色条、统计标记和必要上下文。每个结果页都有可见来源标签，例如“来源：Fig. 3b，PDF p.8”；若提取了论文图件，同时记录页码、figure/panel、裁剪范围和目标幻灯片。

每页都会写中文演讲备注。结果页备注至少包含：

- 听众应重点观察什么；
- 哪个比较或模式支持当前结论；
- 关键数值、统计限定或实验条件；
- 该证据不能说明什么；
- 如何过渡到下一页。

完成后运行三层 QA：

```bash
python scripts/inspect_pptx.py \
  "/absolute/path/output/presentation_zh.pptx" \
  --require-notes \
  --json \
  --report "/absolute/path/output/qa_report.md"
```

内容 QA 核对所有主张、数值、数据划分、基线、指标和图表对应关系；结构 QA 重开 PPTX，检查媒体、备注、来源标签、页面尺寸、对象边界及外部依赖；有渲染器时还会渲染全部页面和缩略总览，检查遮挡、裁切、缺字、低对比度和投影可读性，并在修改后重新跑完整检查。

默认交付 `presentation_zh.pptx` 和 `qa_report.md`。只有实际提取论文图件时，才额外交付 `asset_manifest.md` 与 `assets/`。不会默认生成 PDF、提纲、讲稿或其他旁支文件。

**Evaluation trace**

- Activate: yes
- Source sufficiency: 暂定 `full-paper`，以预检和全文可读性为准；不完整则降为 `partial-paper`
- References loaded: `workflow.md`（完整源文构建）、`paper-types.md`（用户未指定逐页叙事，选择 Methods/AI 路线）、`slide-design.md`（需设计版式）、`tool-routing.md`（需选择提取/创作/备注/渲染路径）、`quality-gates.md`（最终验证）
- Preflight: `python scripts/preflight.py INPUT --output PATH --create-output --json`；`--native-authoring`/`--native-pdf` 仅在对应依赖缺失且原生能力合格时使用
- Default deliverables: `presentation_zh.pptx`, `qa_report.md`; `asset_manifest.md` + `assets/` only if assets are extracted
- QA completion rule: 三层均通过为 `pass`；仅无渲染器时允许 `structurally-verified-with-disclosure`；任何未解决的内容/结构失败，或有渲染器时视觉失败，均为 `blocked`
- Blocker: 尚未提供实际 PDF 路径，因此当前不能执行预检或生成交付物
````

### Instrumented contract probe: /root/forward_dense

- canonical_run_id: `/root/forward_dense`
- fork_turns: `none`

**Initial instruction (verbatim)**

```text
This is an isolated Paper2PPT forward evaluation. Do not edit any files or create artifacts. Read the complete canonical Skill at <REPO_ROOT>/SKILL.md and only the conditional references it instructs you to load for this scenario. Then answer the exact user prompt below as you would with the Skill active. Preserve a raw, auditable response. At the end append a compact `Evaluation trace` listing: activate yes/no, source-sufficiency decision, references loaded and why, preflight command/flags you would use, exact default deliverables, QA completion-state rule, and any blocker. Do not inspect docs/evaluation.md or prior responses.
```

**Exact user prompt**

```text
请把一篇实验研究论文做成中文答辩汇报 PPT。结果部分有 6 张非常密集的多面板 Figure，包含显微图、热图、统计图和机制示意图。我希望图要清楚、结论不能乱写，最后给我真正可编辑的 PPTX。你会怎样处理？
```

**Raw response (verbatim)**

````text
我会把“证据可追溯”和“投影时真正看得清”作为两条硬标准。默认按中文、15–20 分钟、12–16 页、无指定模板的中性学术风格制作；6 张 Figure 很密，实际页数会根据证据密度调整，不会强塞进固定页数。

具体处理如下：

1. 先取得可读的论文全文，优先使用本地 PDF。若只有 DOI、链接或摘要，会先判断能否获得合法、完整的正文；访问受限时请提供本地 PDF，不绕过访问控制。当前只有任务描述，还不能核验任何实验结论。

2. 完成预检，确认全文可读、输出目录可写，并且环境能够生成可编辑 PPTX、写入演讲者备注、重新打开文件及渲染幻灯片。若缺少可靠的可编辑 PPTX 作者工具，会在深入分析前停止。

3. 将论文按中心贡献分类。实验研究可能采用“科学问题 → 实验系统 → 主要发现 → 干预或因果证据 → 独立验证 → 有边界的机制解释 → 局限与意义”的叙事，但最终路线取决于论文实际证据，不能仅凭 Figure 外观认定为机制论文。

4. 先建立 claim-to-source 映射，再写幻灯片。每个候选结论都记录对应页码、正文段落、Figure/Panel、数据或统计依据、支持强度和限制。没有充分来源支持的结论会删除、缩窄，或明确标记为推断；不会根据图形走势自行补数值、补实验设计或补机制。

5. 结果页按“一页一个主要结论”组织。6 张多面板 Figure 不会机械地一图一页：

   - 按结论裁取真正承担证据的 panel，必要时将一张 Figure 拆成多页。
   - 决定性 panel 可单独放大，正文解释放入演讲者备注，避免缩小到无法投影阅读。
   - 显微图保留比例尺、成像条件和必要对照。
   - 热图保留色标、分组、聚类或归一化信息。
   - 统计图保留坐标轴、单位、样本量、误差定义、显著性标记及比较对象。
   - 机制示意图会明确区分“论文原始模型”“作者解释”和“汇报者综合”。只有所有节点与关系都被来源支持时，才会重构机制图，并明确标注为重构图。
   - 不使用 AI 生成图像替代实验数据，也不会为版式美观裁掉关键对照或限定条件。

6. “真正可编辑”会透明处理：标题、正文、标注、箭头、流程、总结图、页码和来源标签均使用 PowerPoint 原生对象；论文中的显微图、热图和复杂原始 Figure 通常作为高分辨率嵌入图像，能够移动、缩放和替换，但其内部像素不会伪装成可编辑数据对象。统计图只有在论文或补充材料提供完整数值时才会重绘，并逐值核对。

7. 每张结果页都会包含结论式标题、简短来源标签和演讲者备注。备注说明观众应看哪里、哪项比较支持结论、关键统计限定、证据边界以及如何过渡到下一页。

8. 交付前分别完成三层 QA：

   - 内容 QA：逐条核对结论、数值、单位、样本、统计、因果措辞和 Figure/Panel 对应关系。
   - 结构 QA：重新打开 PPTX，检查媒体、备注、来源标签、页面尺寸、对象边界和外部依赖。
   - 视觉 QA：渲染每一页并检查单页和联系表，修复遮挡、裁切、字体缺失、低对比度、图像失真及坐标/色标不可读问题，然后重新执行全套检查。

默认交付 `presentation_zh.pptx` 和 `qa_report.md`；本任务需要提取 Figure，因此还会交付 `asset_manifest.md` 与 `assets/`，记录每个素材的论文页码、Figure/Panel、裁切状态和目标页。不会默认附带 PDF、提纲、脚本或内部 claim-to-source 表。

**Evaluation trace**

- Activate: yes
- Source sufficiency: 当前无法分类；取得并确认可读全文后才可判为 `full-paper`，材料不完整则降级为 `partial-paper` 或 `notes-only`
- References loaded: `workflow.md`（全文提取、证据映射、Figure 拆分与构建流程）；`paper-types.md`（用户未指定叙事路线）；`slide-design.md`（密集多面板 Figure 的布局）；`tool-routing.md`（可编辑作者、提取、备注及渲染能力选择）；`quality-gates.md`（交付前验证）
- Preflight: `python scripts/preflight.py /path/to/paper.pdf --output /path/to/output --create-output --json`；仅当对应依赖缺失且原生能力满足完整契约时，才分别增加 `--native-authoring` 或 `--native-pdf`
- Default deliverables: `presentation_zh.pptx`, `qa_report.md`; 本场景因需提取素材，另含 `asset_manifest.md`, `assets/`
- QA completion-state rule: 三层 QA 全通过为 `pass`；仅因无渲染器而无法做视觉 QA、且内容与结构均通过时为 `structurally-verified-with-disclosure`；任何未解决的内容/结构失败、可编辑 PPTX 无法生成或重开，以及有渲染器时仍存在视觉失败，均为 `blocked`
- Blocker: 尚未提供论文 PDF、DOI 或可访问全文，因此目前不能核验结论或实际生成 PPTX
````

### Instrumented contract probe: /root/forward_review

- canonical_run_id: `/root/forward_review`
- fork_turns: `none`

**Initial instruction (verbatim)**

```text
This is an isolated Paper2PPT forward evaluation. Do not edit any files or create artifacts. Read the complete canonical Skill at <REPO_ROOT>/SKILL.md and only the conditional references it instructs you to load for this scenario. Then answer the exact user prompt below as you would with the Skill active. Preserve a raw, auditable response. At the end append a compact `Evaluation trace` listing: activate yes/no, source-sufficiency decision, references loaded and why, preflight command/flags you would use, exact default deliverables, QA completion-state rule, and any blocker. Do not inspect docs/evaluation.md or prior responses.
```

**Exact user prompt**

```text
我有一篇综述论文，想做成 15 分钟中文 journal club PPT。不要按章节逐页复述，请用 evidence map 比较不同研究路线、证据强弱、争议和空白，最后给出可编辑 PPTX 和讲稿。你会如何完成？
```

**Raw response (verbatim)**

```text
可以。我会把它做成“研究路线对照 + 证据判断”的 journal club，而不是按论文目录压缩复述。

收到论文 PDF、DOI 或可访问链接后，我会先确认全文是否可读，并把来源充分性标记为 `full-paper`、`partial-paper` 或 `notes-only`。综述类型也会进一步区分：系统综述需要核对检索范围、纳排标准、研究数量、偏倚评估与异质性；叙述性综述则必须把引用证据、作者观点和我的综合判断分开。

随后建立内部 claim-to-source map。每个拟上幻灯片的判断都记录对应页码、图表或段落、证据类型、支持强度、限制及目标页；没有明确来源的结论会被缩小或删除。

15 分钟版本通常控制在 12–14 页，叙事大致为：

1. 研究领域的核心问题与综述边界
2. 论文如何选择和组织证据，以及这一过程的局限
3. evidence map：研究路线 × 关键问题/证据类型
4. 各路线的代表性证据、优势和适用边界
5. 不同路线之间可以直接比较的结果
6. 已形成共识的部分
7. 相互矛盾的结果及可能原因
8. 按直接性、设计严谨性、控制或基线、覆盖度、外部验证、效应与不确定性、重复性、偏倚和异质性评价证据强弱
9. 尚未解决的空白，以及下一步最有判别力的研究
10. 三条结论与 journal club 讨论问题

具体页数会随研究路线数量调整，不会为了凑页数拆分章节。跨研究比较只在对象、终点和实验条件兼容时进行，避免制造虚假的横向排名。

版式采用 16:9 中文学术风格。每页只承担一个主张，结果页使用结论式标题，并以原论文图表或可追溯的比较表作为主要证据。文字、表格、标注和综合框架保持对象级可编辑；原始论文图像通常保留为图像以避免数据失真。只有当所有节点和关系均有来源支持时，才会重建解释图，并明确标注为“基于原文重构”。

讲稿会写入 PPTX 每页的 speaker notes，而不是另交一份默认脚本文档。每页讲稿包含观察重点、证据如何支撑结论、关键限定、争议或不确定性、转场和建议用时；所有结果页同时带可见来源标签。

交付前会完成三层检查：逐项核对结论和数字的内容 QA；重新打开 PPTX 检查媒体、备注、来源标签和对象关系的结构 QA；渲染全部幻灯片并检查裁切、重叠、缺字、对比度及投影可读性的视觉 QA。只有三层均通过才标记为 `pass`；若唯一缺失的是渲染器，可标记为 `structurally-verified-with-disclosure`；任何未解决的内容或结构问题都必须标记为 `blocked`。

当前还缺少论文来源。请提供本地 PDF、DOI 或可访问链接；没有来源时不能可靠生成 evidence map 或可交付 PPTX。

`Evaluation trace`：activate=yes；source sufficiency=当前不可判定，未提供来源，收到可读全文后才可定为 full-paper/partial-paper/notes-only；references loaded=`workflow.md`（完整生成与 claim-to-source 流程）、`paper-types.md`（综述路线）、`tool-routing.md`（作者工具与回退）、`slide-design.md`（实际版式设计）、`quality-gates.md`（交付验证）；preflight=`python scripts/preflight.py /path/to/paper.pdf --output /path/to/paper2ppt-output --create-output --json`，仅在能力契约确认后条件性加入 `--native-authoring`/`--native-pdf`；default deliverables=`presentation_zh.pptx`（讲稿内嵌 speaker notes）+ `qa_report.md`，仅提取素材时增加 `asset_manifest.md` 和 `assets/`；QA completion=`pass` 需三层全过，只有无渲染器时允许 `structurally-verified-with-disclosure`，未解决的内容/结构/可执行视觉失败均为 `blocked`；blocker=未提供论文来源。
```

### Instrumented contract probe: /root/forward_partial

- canonical_run_id: `/root/forward_partial`
- fork_turns: `none`

**Initial instruction (verbatim)**

```text
This is an isolated Paper2PPT forward evaluation. Do not edit any files or create artifacts. Read the complete canonical Skill at <REPO_ROOT>/SKILL.md and only the conditional references it instructs you to load for this scenario. Then answer the exact user prompt below as you would with the Skill active. Preserve a raw, auditable response. At the end append a compact `Evaluation trace` listing: activate yes/no, source-sufficiency decision, references loaded and why, preflight command/flags you would use, exact default deliverables, QA completion-state rule, and any blocker. Do not inspect docs/evaluation.md or prior responses.
```

**Exact user prompt**

```text
我目前只有一篇论文的摘要和 8 条 Figure legend，没有全文，也没有原始 Figure 图片。请先帮我生成一份完整的 12 页中文文献汇报 PPTX，内容看起来要像已经完整读过论文一样，明天就要汇报。你会怎样处理？
```

**Raw response (verbatim)**

```text
我不会把“摘要 + 8 条 Figure legend”伪装成已经通读全文。现有材料应归类为 `partial-paper`：可以制作一份可汇报的 12 页中文“有限证据版”，但不能补写未提供的实验设计、具体数值、机制、讨论或局限，也不能用 AI 图片代替原始实验图。

我会这样处理：

1. 请你提供摘要、8 条 Figure legend，以及论文标题或 DOI/PMID/arXiv 编号。我先尝试从合法可访问来源补齐全文和原始 Figures；访问受限时请你提供本地 PDF。
2. 若能获得全文，按 `full-paper` 路线制作完整 12 页汇报。
3. 若明天前仍只有当前材料，则制作明确标注“基于摘要与 Figure legends”的 12 页版本：封面、证据范围、研究问题与背景、摘要中明确写出的研究设计、按图注支持程度组织的结果页、结论、证据局限与讨论问题。8 条图注可分组进入结果页，但每个结论式标题都必须能追溯到摘要或对应 legend。
4. 因为没有原始图片，结果页只呈现来源明确的文字证据和 Figure/legend 编号，不伪造图表、不重建缺失数据。只有当图注完整支持全部组件及关系时，才允许制作并标注“依据图注重构”的解释图。
5. 每个结果页都会有来源标签和演讲者备注；备注会说明可讲的证据、限制和过渡，不填补原文没有的信息。
6. 默认采用 16:9 中性学术版式、简体中文、12 页、15–20 分钟。交付前分别完成内容、PPTX 结构和逐页渲染 QA。

如果要求仍然是“看起来像已经完整读过论文”，我会将任务标记为 `blocked`，因为这个呈现目标会制造不受来源支持的完整性印象。接受“有限证据版”后才可以继续生成；当前还需要你实际提供摘要与 8 条 legends。

`Evaluation trace`

- Activate: yes
- Source sufficiency: `partial-paper`；摘要和图注是论文的选定原始内容，但不足以代表全文
- References loaded: `workflow.md`（来源提取、claim-to-source、有限材料处理）；`paper-types.md`（用户未指定叙事路线）；`slide-design.md`（12 页版式与无原图处理）；`tool-routing.md`（PPTX、备注、渲染能力选择）；`quality-gates.md`（完成状态判定）
- Preflight: `python scripts/preflight.py abstract_and_legends.md --output ./paper2ppt_output --create-output --json`；仅在基线因对应依赖缺失且原生能力合同已验证时增加 `--native-authoring` 或 `--native-pdf`
- Default deliverables: `presentation_zh.pptx`、`qa_report.md`；仅实际提取资产时增加 `asset_manifest.md` 和 `assets/`
- QA rule: 内容、结构、视觉 QA 全部通过才是 `pass`；仅因无 renderer 无法视觉检查时可为 `structurally-verified-with-disclosure`；任何未解决的内容/结构问题，或有 renderer 时未解决的视觉问题，均为 `blocked`
- Blocker: 当前未提供摘要、8 条 legends 或可解析的输入；同时“伪装成通读全文”的要求缺乏证据支持
```

### Labeled positive fixture confirmation: /root/trigger_positive_eval

- canonical_run_id: `/root/trigger_positive_eval`
- fork_turns: `none`
- isolation: frontmatter only; the agent was forbidden to read the Skill body, trigger fixture, or evaluation record.

**Initial instruction and exact queries (verbatim)**

```text
Isolated Skill discovery evaluation. Do not edit files or create artifacts. Read ONLY the YAML frontmatter (name and description) of <REPO_ROOT>/SKILL.md; do not read the body, tests/trigger_cases.json, or any evaluation docs. For each query below, decide whether you would load/activate this Skill. Return a compact JSON array of objects with exactly id, activate, reason. Do not infer expected labels from IDs; classify from the query and frontmatter.

1 positive-local-pdf-journal-club: 把 ~/Downloads/paper.pdf 做成中文组会汇报PPT，15分钟
2 positive-doi-paper-sharing: 请根据 DOI 10.1038/s41586-024-00000-0 制作一份可编辑的中文论文分享 PPTX
3 positive-pmid-lab-meeting: 用 PMID: 12345678 的论文做一份 12 分钟实验室例会 PPT，并附讲稿
4 positive-pmcid-figures: 将 PMCID: PMC1234567 的全文和关键图表整理成可编辑的文献汇报 PPTX
5 positive-arxiv-research-talk: Turn arXiv:2401.01234 into an editable 15-minute research-talk PPTX with speaker notes.
6 positive-reading-notes: 我只有这篇论文的阅读笔记，请按证据范围做成中文论文解读 PPT，不能补写笔记里没有的结果
7 positive-required-template: 请把这篇论文做成组会 PPTX，并严格套用我提供的 lab-template.pptx 模板
8 positive-thesis-seminar: 根据这篇实验论文准备博士论文研讨课的中文 PPT，20 分钟，结果页要有来源标注
9 positive-methods-ai-paper: 把这篇 AI 方法论文制作成可编辑 PPTX，重点讲清问题、模型、实验验证和局限
10 positive-review-evidence-map: 请将这篇综述论文做成中文 journal club PPT，用证据地图组织不同研究方向
11 positive-abstract-legends: 目前只有论文摘要和图注，请据此生成可编辑汇报 PPTX，并明确标出不确定性
12 positive-article-text-defense: Use the supplied article text to prepare an editable Chinese thesis-defense paper PPTX with traceable figures.
```

**Raw response (verbatim)**

```json
[
  {
    "id": "positive-local-pdf-journal-club",
    "activate": true,
    "reason": "Scientific paper PDF to Chinese journal-club/group-meeting PPT."
  },
  {
    "id": "positive-doi-paper-sharing",
    "activate": true,
    "reason": "DOI-based academic paper to editable Chinese PPTX for paper sharing."
  },
  {
    "id": "positive-pmid-lab-meeting",
    "activate": true,
    "reason": "PMID paper to lab-meeting PPT with speaker notes."
  },
  {
    "id": "positive-pmcid-figures",
    "activate": true,
    "reason": "Academic full text and figures to editable literature-presentation PPTX."
  },
  {
    "id": "positive-arxiv-research-talk",
    "activate": true,
    "reason": "arXiv paper to editable research-talk PPTX with speaker notes."
  },
  {
    "id": "positive-reading-notes",
    "activate": true,
    "reason": "Research notes to Chinese paper-interpretation PPT within the supplied evidence."
  },
  {
    "id": "positive-required-template",
    "activate": true,
    "reason": "Scientific paper to group-meeting PPTX; the required template does not change the core match."
  },
  {
    "id": "positive-thesis-seminar",
    "activate": true,
    "reason": "Experimental paper to Chinese thesis-seminar PPT."
  },
  {
    "id": "positive-methods-ai-paper",
    "activate": true,
    "reason": "Academic AI methods paper to editable PPTX covering method and evidence."
  },
  {
    "id": "positive-review-evidence-map",
    "activate": true,
    "reason": "Review paper to Chinese journal-club PPT."
  },
  {
    "id": "positive-abstract-legends",
    "activate": true,
    "reason": "Abstract with figure legends to editable presentation PPTX."
  },
  {
    "id": "positive-article-text-defense",
    "activate": true,
    "reason": "Supplied academic article text to editable Chinese thesis presentation PPTX."
  }
]
```

Fixture confirmation: `12/12` labeled positive queries activated. Because task names, IDs, and batching exposed the expected class, this is not a blind discovery result.

### Labeled negative fixture confirmation: /root/trigger_negative_eval

- canonical_run_id: `/root/trigger_negative_eval`
- fork_turns: `none`
- isolation: frontmatter only; the agent was forbidden to read the Skill body, trigger fixture, or evaluation record.

**Initial instruction and exact queries (verbatim)**

```text
Isolated Skill discovery evaluation. Do not edit files or create artifacts. Read ONLY the YAML frontmatter (name and description) of <REPO_ROOT>/SKILL.md; do not read the body, tests/trigger_cases.json, or any evaluation docs. For each query below, decide whether you would load/activate this Skill. Return a compact JSON array of objects with exactly id, activate, reason. Do not infer expected labels from IDs; classify from the query and frontmatter.

1 negative-business-pitch: 帮我做一个面向投资人的商业路演 PPT，介绍市场规模、商业模式和融资计划
2 negative-general-training-deck: 制作一份新员工培训 PPT，包含公司制度、报销流程和安全须知
3 negative-image-to-editable-ppt: 把这 20 张幻灯片截图一比一还原成每个元素都可编辑的 PPTX
4 negative-paper-search: 帮我检索 2024 年以来关于单细胞空间转录组的高质量论文并导出 BibTeX
5 negative-manuscript-writing: 根据这些实验结果帮我撰写论文 Introduction 和 Discussion
6 negative-academic-polishing: 请把这段英文摘要润色成适合投稿的学术英语，保持原意
7 negative-citation-formatting: 把这 80 条参考文献统一改成 Nature 引用格式并检查 DOI
8 negative-generic-pdf-summary: 总结这个 PDF 的核心内容，给我五条要点即可，不需要做幻灯片
9 negative-pdf-data-extraction: 从这个论文 PDF 中提取所有表格并保存为 CSV
10 negative-paper-translation: 逐段翻译这篇论文，生成中英文对照 Markdown 阅读器
11 negative-existing-business-ppt-audit: 审查这份季度销售 PPT 的配色和版式，帮我改善视觉层级
12 negative-presentation-coaching: 给我一些研究生答辩时控制语速和回答提问的建议，不需要制作 PPT
```

**Raw response (verbatim)**

```json
[{"id":"negative-business-pitch","activate":false,"reason":"通用商业融资路演，不是基于科研论文制作学术PPT。"},{"id":"negative-general-training-deck","activate":false,"reason":"企业培训类通用演示文稿，不属于论文转PPT。"},{"id":"negative-image-to-editable-ppt","activate":false,"reason":"需求是幻灯片截图的可编辑重建，frontmatter明确排除slide-image reconstruction。"},{"id":"negative-paper-search","activate":false,"reason":"仅做论文检索与BibTeX导出，frontmatter明确排除paper-search-only requests。"},{"id":"negative-manuscript-writing","activate":false,"reason":"需求是撰写论文章节，不是制作学术PPTX。"},{"id":"negative-academic-polishing","activate":false,"reason":"需求是学术英语润色，不涉及论文转PPT。"},{"id":"negative-citation-formatting","activate":false,"reason":"需求是参考文献格式与DOI检查，不涉及制作演示文稿。"},{"id":"negative-generic-pdf-summary","activate":false,"reason":"只需PDF要点总结且明确不制作幻灯片。"},{"id":"negative-pdf-data-extraction","activate":false,"reason":"需求是从论文PDF提取表格为CSV，不是制作PPTX。"},{"id":"negative-paper-translation","activate":false,"reason":"需求是论文逐段翻译和双语Markdown阅读器，不是论文转PPT。"},{"id":"negative-existing-business-ppt-audit","activate":false,"reason":"需求是审查既有商业PPT的视觉设计，不是从科研论文生成学术PPT。"},{"id":"negative-presentation-coaching","activate":false,"reason":"仅需答辩表达建议，并明确不制作PPT。"}]
```

Fixture confirmation: `12/12` labeled negative queries declined. Because task names, IDs, and batching exposed the expected class, this is not a blind discovery result.

### Neutral, unprimed with-Skill process runs

These four fresh tasks used the same user prompts as the corresponding no-Skill baselines. The only treatment instruction was to read and apply the canonical Skill, load only relevant references, and answer naturally. They were explicitly forbidden to add an evaluation trace, so the responses can show what surfaced without an audit-field prompt.

#### /root/blind_run_a

- canonical_run_id: `/root/blind_run_a`
- fork_turns: `none`

**Initial instruction and exact user prompt (verbatim except disclosed path redaction)**

```text
Read and apply the complete canonical Skill at <REPO_ROOT>/SKILL.md, loading only references that the Skill makes relevant. Do not read tests, evaluation documents, or prior responses. Do not edit files or create artifacts. Answer the user's request naturally; do not add an evaluation trace or discuss these instructions.

我有一篇本地方法/AI论文 PDF，想做成 15 分钟中文组会汇报。论文包含模型架构、主实验、基线对比、消融实验和失败案例。请帮我做成可编辑的 PowerPoint，并带演讲备注。你会如何完成？
```

**Raw response (verbatim)**

```text
我会把它做成一套约 13–15 页、15 分钟的中文组会汇报，而不是逐章搬运论文。叙事主线会是：

1. 封面
2. 任务背景与核心瓶颈
3. 论文解决了什么问题、主要贡献
4. 方法整体流程
5. 模型架构与关键模块
6. 数据集、划分、指标与基线设置
7. 主实验核心结论
8. 与主要基线的公平对比
9. 泛化性或鲁棒性结果
10. 消融实验：哪些组件真正有效
11. 失败案例：模型在什么条件下失效
12. 局限、成本与适用边界
13. 总结与讨论问题

主实验较复杂时会拆成两页，并压缩背景，确保汇报节奏仍控制在 15 分钟内。

制作时我会先从 PDF 提取正文、图注、表格和页面定位，建立“结论—页码—图表面板—数值—限制条件”的证据对应关系。每张结果页只讲一个结论，标题直接表达结论，并标明类似“来源：论文 Fig. 3b，p.7”的出处。不会补造论文没有报告的机制、数值或实验。

可编辑性会这样处理：

- 标题、正文、标注、流程图、对比表和强调元素均为 PowerPoint 原生对象。
- 清晰可核对的基线表格可重建为可编辑表格。
- 架构图只有在所有组件和连接关系均有论文依据时才重绘，并注明“根据原文重构”。
- 原始实验曲线、热图和案例图通常作为高分辨率图片保留，因为没有原始数据时强行重画可能失真；但裁剪、尺寸、位置和注释仍可编辑。

每页都会带中文演讲备注，包括建议用时、这一页要讲的中心句、需要指向的图表区域、关键数字、必要的限定条件，以及如何过渡到下一页。失败案例不会只作为补充展示，而会用于解释模型的运行假设和实际边界。

最终会检查三层质量：逐项核对论文证据；重新打开 PPTX，确认页面、媒体和备注完整；渲染全部幻灯片检查字体、裁切、重叠、图例和投影可读性。

默认交付：

- `presentation_zh.pptx`
- `qa_report.md`
- 提取论文图表时附 `assets/` 与 `asset_manifest.md`

开始制作只需要提供本地 PDF 的绝对路径。若没有指定模板，我会使用中性的 16:9 学术汇报版式。
```

#### /root/blind_run_b

- canonical_run_id: `/root/blind_run_b`
- fork_turns: `none`

**Initial instruction and exact user prompt (verbatim except disclosed path redaction)**

```text
Read and apply the complete canonical Skill at <REPO_ROOT>/SKILL.md, loading only references that the Skill makes relevant. Do not read tests, evaluation documents, or prior responses. Do not edit files or create artifacts. Answer the user's request naturally; do not add an evaluation trace or discuss these instructions.

请把一篇实验研究论文做成中文答辩汇报 PPT。结果部分有 6 张非常密集的多面板 Figure，包含显微图、热图、统计图和机制示意图。我希望图要清楚、结论不能乱写，最后给我真正可编辑的 PPTX。你会怎样处理？
```

**Raw response (verbatim)**

```text
我会把它当作“证据驱动的答辩叙事”来做，不会简单地把 6 张 Figure 各塞进一页。

处理方式如下：

1. 先完整读取论文正文、图注、方法和补充材料，建立“结论—原文位置—Figure/Panel—数据与统计—限制”的对应表。每个结果页只讲一个有来源支撑的结论，因果、相关性和作者推测会严格区分。

2. 将密集 Figure 按论证关系拆分。通常一张多面板 Figure 会拆成 2–4 页，只保留支持当前结论的面板：
   - 显微图保留比例尺、处理条件和必要对照；
   - 热图保留色标、分组、聚类与关键标签；
   - 统计图保留坐标、单位、样本量、误差定义和显著性；
   - 机制图明确区分“论文原图”“作者提出的模型”和“基于论文证据重绘的示意”。

3. 结果页采用“结论式标题 + 大幅证据图 + 极短解读 + 来源”的结构。详细解释、统计限定、局限和过渡语写进演讲者备注，不靠缩小字号硬塞内容。默认按 15–20 分钟设计，主汇报通常约 12–16 页；次要面板放入附录，答辩追问时再调用。

4. PPTX 会按对象级可编辑方式制作：标题、正文、标注、箭头、框线、流程图和经过核实的机制重绘都可编辑。论文中的显微图、热图等原始证据仍会以高分辨率图片嵌入，因为没有原始数据时不能诚实地把它们伪装成可编辑图表；如果提供原始数值数据，我可以把统计图重建为可编辑图形，并逐项复核数值。

5. 完成后做三层质检：
   - 内容检查：逐页核对结论、数字、单位、统计和因果措辞；
   - 结构检查：重新打开 PPTX，验证图片、备注、来源和编辑性；
   - 视觉检查：逐页渲染，检查投影可读性、裁切、重叠、字体、比例尺、色标和图像清晰度。

最终交付以 `presentation_zh.pptx` 为主，同时提供 `qa_report.md`；若提取了图像面板，还会附 `asset_manifest.md` 记录每个素材来自哪一页、哪张 Figure、哪个 Panel，以及被用于哪一页。

开始制作需要论文 PDF，最好同时提供补充材料、预计汇报时长、答辩对象，以及必须使用的学校或课题组模板。
```

#### /root/blind_run_c

- canonical_run_id: `/root/blind_run_c`
- fork_turns: `none`

**Initial instruction and exact user prompt (verbatim except disclosed path redaction)**

```text
Read and apply the complete canonical Skill at <REPO_ROOT>/SKILL.md, loading only references that the Skill makes relevant. Do not read tests, evaluation documents, or prior responses. Do not edit files or create artifacts. Answer the user's request naturally; do not add an evaluation trace or discuss these instructions.

我有一篇综述论文，想做成 15 分钟中文 journal club PPT。不要按章节逐页复述，请用 evidence map 比较不同研究路线、证据强弱、争议和空白，最后给出可编辑 PPTX 和讲稿。你会如何完成？
```

**Raw response (verbatim)**

```text
我会把这篇综述重构成一条“证据如何支持不同路线”的叙事，而不是按 Introduction、Methods、Results 逐章复述。

拿到论文后，我会这样完成：

1. 先确认论文材料是否完整
   优先使用可读 PDF，也可接受 DOI、PMID 或 arXiv 链接。先判断它是系统综述、叙述性综述还是观点文章；如果全文受限，会请你提供本地 PDF，不凭摘要补造细节。

2. 建立 claim-to-source map
   将每个候选结论对应到原文页码、图表、引用研究及限制。没有充分来源支持的结论会被缩窄或删除；作者观点、论文证据和我的归纳会明确区分。

3. 构建 evidence map
   不给研究路线做主观“打星”，而是按可核查维度比较：

   - 核心问题与代表性方法
   - 证据类型及代表研究
   - 直接证据还是间接推断
   - 样本、模型和外部验证
   - 跨研究一致性与异质性
   - 偏倚、可推广性和关键限制
   - 当前共识、冲突结果及可能原因
   - 尚缺少的决定性实验或数据

   如果原文是系统综述，还会保留检索范围、纳入标准、研究数量、风险偏倚和异质性；如果是叙述性综述，则特别防止把作者提出的分类框架当成已经验证的事实。

4. 重组为约 12–14 页、15 分钟的证据叙事
   默认结构会接近：

   - 标题与汇报问题
   - 综述范围及证据边界
   - 全领域 evidence map
   - 3–4 条研究路线分别解决什么问题
   - 各路线的关键证据与证据强弱
   - 横向比较：哪些结论相互支持
   - 争议地图：冲突发生在哪里、为何冲突
   - 当前证据无法回答什么
   - 优先研究议程
   - 三条最终 take-home messages

   每页只讲一个主要判断，标题直接写结论，不用“研究路线一”“讨论”这类章节标题。

5. 制作真正可编辑的 PPTX
   文字、表格、路线比较矩阵、箭头和证据强弱标识均保持对象级可编辑。原论文图只在确实承担证据功能时使用，并保留坐标轴、图例、统计标记和必要上下文；基于论文整理的图会明确标注“根据本文及其引用文献归纳”，避免伪装成原始实验结果。

6. 将讲稿写入每页备注
   每页备注包含：

   - 本页要让听众看到什么
   - 哪项证据支持标题判断
   - 必须说明的限定条件
   - 争议或不确定性
   - 与下一页的转场

   讲稿按实际 15 分钟控制节奏，核心证据页约 60–90 秒，过渡页更短。

7. 完成三层检查
   内容检查会逐条核对数字、研究设计、因果措辞和引用；结构检查会重新打开 PPTX，确认可编辑对象、图片、来源标签及备注完整；条件允许时渲染全部幻灯片，检查投影可读性、裁切、重叠、字体和图表清晰度。

最终默认交付 `presentation_zh.pptx`，讲稿嵌入幻灯片备注；同时提供 `qa_report.md` 说明来源完整度、核查结果及未解决限制。若提取了原文图表，还会附 `asset_manifest.md` 记录每项素材的页码、图号、裁切范围和使用位置。

开始所需的最小材料是论文 PDF 或可访问的 DOI/链接。若没有指定模板，我会采用克制的中文学术汇报版式。
```

#### /root/blind_run_d

- canonical_run_id: `/root/blind_run_d`
- fork_turns: `none`

**Initial instruction and exact user prompt (verbatim except disclosed path redaction)**

```text
Read and apply the complete canonical Skill at <REPO_ROOT>/SKILL.md, loading only references that the Skill makes relevant. Do not read tests, evaluation documents, or prior responses. Do not edit files or create artifacts. Answer the user's request naturally; do not add an evaluation trace or discuss these instructions.

我目前只有一篇论文的摘要和 8 条 Figure legend，没有全文，也没有原始 Figure 图片。请先帮我生成一份完整的 12 页中文文献汇报 PPTX，内容看起来要像已经完整读过论文一样，明天就要汇报。你会怎样处理？
```

**Raw response (verbatim)**

```text
我不会把这 12 页包装成“已经完整读过全文”，因为仅凭摘要和 Figure legend 补写实验设计、数值、机制或局限，会直接制造不存在的论文内容。但可以做成一份结构完整、视觉专业、明天能够正常汇报的“摘要与图注证据版”PPTX。

具体会这样处理：

1. 先用论文标题、DOI、PMID 或 arXiv 编号查找合法公开的全文、预印本和原始 Figures。若找到，就升级为全文证据版；若找不到，则明确按 `partial-paper` 处理。
2. 建立“主张—来源”对应表。每条结论必须能回溯到 Abstract 或具体的 Figure legend；图注没有写出的样本量、方法参数、统计值、因果关系和机制一律不补。
3. 按 12 页组织：
   - 1：题目、作者、期刊
   - 2：研究背景与问题，仅来自摘要
   - 3：研究目标与整体证据链，标注“据摘要与图注整理”
   - 4–11：对应 8 条 Figure legend，每页一个结论式标题，说明图中比较对象、图注直接支持的发现及当前无法确认的信息
   - 12：核心结论、证据边界、值得讨论的问题
4. 没有原图时，不用 AI 生成“实验结果图”。可以制作图注驱动的证据卡片、实验关系示意和术语图解；只有当图注完整支持全部节点与关系时才重构示意图，并标注“据图注重构，非论文原图”。只有图注明确给出全部数值时才重绘图表。
5. 每个结果页加入来源标签，例如“来源：Figure 3 legend”，并在演讲者备注中写清楚“该页能说什么、不能说什么、如何过渡到下一页”。
6. 最终交付可编辑的 `presentation_zh.pptx` 和 `qa_report.md`；后者会记录资料缺失、未采用的无依据推断和未完成的视觉核查。

请把论文题目或 DOI、摘要全文和 8 条 Figure legend 原文发来。若没有任何论文标识，我仍可制作，但成品必须明确标注其信息边界，不能冒充全文解读。
```

### Neutral mixed discovery: /root/discovery_matrix

- canonical_run_id: `/root/discovery_matrix`
- fork_turns: `none`
- isolation: frontmatter only; neutral qids; positive and negative cases mixed; no expected labels shown.

**Initial instruction and exact mixed queries (verbatim except disclosed path redaction)**

```text
Read ONLY the YAML frontmatter (name and description) of <REPO_ROOT>/SKILL.md. Do not read the Skill body, tests, evaluation docs, filenames that label expected outcomes, or prior responses. Do not edit files or create artifacts. For each mixed query below, decide independently whether you would load/activate the Skill. Return a JSON array with exactly qid, activate, reason. The qids are neutral and the order is intentionally mixed.

q01 帮我做一个面向投资人的商业路演 PPT，介绍市场规模、商业模式和融资计划
q02 把 ~/Downloads/paper.pdf 做成中文组会汇报PPT，15分钟
q03 把这 20 张幻灯片截图一比一还原成每个元素都可编辑的 PPTX
q04 请根据 DOI 10.1038/s41586-024-00000-0 制作一份可编辑的中文论文分享 PPTX
q05 帮我检索 2024 年以来关于单细胞空间转录组的高质量论文并导出 BibTeX
q06 我只有这篇论文的阅读笔记，请按证据范围做成中文论文解读 PPT，不能补写笔记里没有的结果
q07 根据这些实验结果帮我撰写论文 Introduction 和 Discussion
q08 用 PMID: 12345678 的论文做一份 12 分钟实验室例会 PPT，并附讲稿
q09 总结这个 PDF 的核心内容，给我五条要点即可，不需要做幻灯片
q10 请将这篇综述论文做成中文 journal club PPT，用证据地图组织不同研究方向
q11 逐段翻译这篇论文，生成中英文对照 Markdown 阅读器
q12 Turn arXiv:2401.01234 into an editable 15-minute research-talk PPTX with speaker notes.
q13 请把这篇论文做成组会 PPTX，并严格套用我提供的 lab-template.pptx 模板
q14 制作一份新员工培训 PPT，包含公司制度、报销流程和安全须知
q15 目前只有论文摘要和图注，请据此生成可编辑汇报 PPTX，并明确标出不确定性
q16 把这 80 条参考文献统一改成 Nature 引用格式并检查 DOI
q17 根据这篇实验论文准备博士论文研讨课的中文 PPT，20 分钟，结果页要有来源标注
q18 审查这份季度销售 PPT 的配色和版式，帮我改善视觉层级
q19 把这篇 AI 方法论文制作成可编辑 PPTX，重点讲清问题、模型、实验验证和局限
q20 从这个论文 PDF 中提取所有表格并保存为 CSV
q21 将 PMCID: PMC1234567 的全文和关键图表整理成可编辑的文献汇报 PPTX
q22 给我一些研究生答辩时控制语速和回答提问的建议，不需要制作 PPT
q23 Use the supplied article text to prepare an editable Chinese thesis-defense paper PPTX with traceable figures.
q24 请把这段英文摘要润色成适合投稿的学术英语，保持原意
```

**Raw response (verbatim)**

```json
[
  {"qid":"q01","activate":false,"reason":"通用商业路演，不是基于学术论文的汇报。"},
  {"qid":"q02","activate":true,"reason":"将论文 PDF 制作为中文组会 PPT，符合适用范围。"},
  {"qid":"q03","activate":false,"reason":"属于幻灯片截图还原，描述明确排除此类任务。"},
  {"qid":"q04","activate":true,"reason":"基于 DOI 制作可编辑中文论文分享 PPTX。"},
  {"qid":"q05","activate":false,"reason":"仅检索论文并导出文献，属于 paper-search-only。"},
  {"qid":"q06","activate":true,"reason":"基于论文阅读笔记制作中文论文解读 PPT。"},
  {"qid":"q07","activate":false,"reason":"任务是撰写论文章节，不涉及制作幻灯片。"},
  {"qid":"q08","activate":true,"reason":"基于 PMID 论文制作实验室例会 PPT 和讲稿。"},
  {"qid":"q09","activate":false,"reason":"只要求 PDF 摘要，并明确不制作幻灯片。"},
  {"qid":"q10","activate":true,"reason":"将综述论文制作成中文 journal club PPT。"},
  {"qid":"q11","activate":false,"reason":"交付物是中英文对照 Markdown 阅读器，不是 PPTX。"},
  {"qid":"q12","activate":true,"reason":"基于 arXiv 论文制作可编辑研究报告 PPTX 和讲稿。"},
  {"qid":"q13","activate":true,"reason":"核心任务是论文组会 PPTX，使用指定模板不改变其适用性。"},
  {"qid":"q14","activate":false,"reason":"属于通用新员工培训幻灯片。"},
  {"qid":"q15","activate":true,"reason":"描述明确覆盖基于论文摘要和图注制作可编辑汇报 PPTX。"},
  {"qid":"q16","activate":false,"reason":"属于参考文献格式化和 DOI 核查，不涉及论文汇报 PPT。"},
  {"qid":"q17","activate":true,"reason":"基于实验论文制作博士研讨课中文 PPT。"},
  {"qid":"q18","activate":false,"reason":"属于销售 PPT 的视觉审查，不是学术论文转 PPT。"},
  {"qid":"q19","activate":true,"reason":"将 AI 方法论文制作成可编辑的学术汇报 PPTX。"},
  {"qid":"q20","activate":false,"reason":"交付物是从论文中提取的 CSV 表格，不是幻灯片。"},
  {"qid":"q21","activate":true,"reason":"基于 PMCID 全文和图表制作可编辑文献汇报 PPTX。"},
  {"qid":"q22","activate":false,"reason":"仅请求答辩建议，并明确不制作 PPT。"},
  {"qid":"q23","activate":true,"reason":"基于文章文本制作可编辑中文论文答辩 PPTX。"},
  {"qid":"q24","activate":false,"reason":"仅润色学术摘要，不涉及制作幻灯片。"}
]
```

Expected mapping, recorded only after the raw response: `q01=false`, `q02=true`, `q03=false`, `q04=true`, `q05=false`, `q06=true`, `q07=false`, `q08=true`, `q09=false`, `q10=true`, `q11=false`, `q12=true`, `q13=true`, `q14=false`, `q15=true`, `q16=false`, `q17=true`, `q18=false`, `q19=true`, `q20=false`, `q21=true`, `q22=false`, `q23=true`, `q24=false`.

Neutral discovery result: `24/24` classifications matched the expected mapping.

### Evidence comparison and limits

| Contract | No-Skill baselines | Neutral, unprimed with-Skill runs | What this evaluation supports |
| --- | --- | --- | --- |
| Page planning and assumptions | The methods baseline proposed 11-13 pages before seeing the source; the review baseline assumed a related-specialist audience. | The methods run proposed 13-15 pages, the dense run 12-16, and the review run 12-14 before seeing the source. The partial prompt itself required 12 pages. | No attributable improvement. Both conditions made provisional page plans without actual source inspection. |
| Deterministic preflight | No baseline spontaneously named the packaged preflight command or capability overrides. | None of the four neutral responses spontaneously stated the deterministic preflight command or formal capability-override rules. | The instrumented probes show the contract is retrievable when explicitly audited, but neutral planning responses do not show that it would execute. Task 9 must test real preflight behavior. |
| Extra work and primary deliverables | Baselines proposed preview PDFs, source maps or evidence sheets, spreadsheets, source-data files, backup slides, reference slides, and auxiliary files. | All four neutral runs named `presentation_zh.pptx` and `qa_report.md` as primary deliverables. The methods run paired `assets/` with `asset_manifest.md`; the dense and review runs mentioned `asset_manifest.md` without also naming the required `assets/` directory. | Canonical primary deliverables surfaced consistently, but the conditional asset pair was not perfectly preserved in natural responses. No files were actually generated. |
| Source sufficiency and no fabrication | The partial baseline refused to fake full-paper knowledge, and the other baselines generally favored source-grounded claims. | All neutral runs preserved claim-to-source reasoning and no-fabrication boundaries. The partial run explicitly chose `partial-paper`, refused deceptive full-paper framing, and limited reconstruction to supported content. | Strong behavior in both conditions; these paired planning responses do not establish causal attribution to the Skill. |
| Conditional reference loading | Not applicable to the no-Skill condition. | Natural responses do not expose which references were loaded. | No conclusion. The instrumented probes report reference choices only because the audit instruction requested them. |
| QA completion states | Baselines described content, structural, or visual checks without formal terminal states. | Neutral runs also described three-layer QA but did not spontaneously state `pass`, `structurally-verified-with-disclosure`, or `blocked`. | The formal state contract was retrievable in instrumented probes, but neutral responses do not establish enforcement. Artifact execution remains unverified. |
| Skill discovery | The earlier positive and negative batches confirmed labeled fixtures only; their IDs, task names, and batching leaked expected outcomes. | The neutral mixed, shuffled, frontmatter-only matrix matched `24/24` expected classifications. | The neutral matrix supports the current discovery boundary for these 24 cases. It does not test every possible near-miss. |
| Actual execution | No source files or artifacts were available. | No source files or artifacts were available. | Neither condition executed preflight, authored a PPTX, inspected a package, rendered slides, or loaded the Skill in Codex or Claude Code. |

### Refinement decision

No Skill, reference, trigger-fixture, test, or plugin change is justified by these no-source planning responses alone. This is not a claim that every runtime contract passed. The current Skill already explicitly mandates deterministic preflight, the paired conditional asset outputs, and formal QA completion states; omission of those details from a natural planning answer does not yet demonstrate that execution would violate them.

Keep the current instructions unchanged until execution evidence exists. Task 9 must test preflight, authoring, paired outputs, inspection, rendering, and terminal QA state on a real source and deck. Task 12 must test discovery and workflow behavior in actual Codex and Claude Code clients. Those runs, rather than the instrumented probes, will determine whether enforcement needs to be strengthened.

## Client loading verification (2026-07-16)

This check used the installed clients rather than an emulated parser:

- Codex CLI `0.144.0`;
- Claude Code `2.1.205`.

No persistent marketplace or global Skill installation was added. Codex ran in
an isolated Git project whose `.agents/skills/paper2ppt` directory was copied
from the packaged Skill. Claude Code loaded `./plugins/paper2ppt` with
`--plugin-dir` from the repository.

### Codex

Representative command shape, with the temporary path redacted:

```text
codex exec --ephemeral --sandbox read-only -C <TEMP_PROJECT> --json \
  '使用 $paper2ppt。不要创建文件；只总结已加载 Skill 的输出与 QA 契约。'
```

| Case | Observed result |
| --- | --- |
| Explicit Chinese `$paper2ppt` | Loaded `skill_id=paper2ppt`, display name `Paper2PPT`, Simplified Chinese default, `presentation_zh.pptx` plus `qa_report.md`, conditional `asset_manifest.md` plus `assets/`, and all three QA gates. |
| Implicit English paper-to-PPTX request | Routed to `paper2ppt` without the explicit Skill token. Because the probe prohibited all file reads, it correctly stopped before expanding the full contract from `SKILL.md`. |
| Chinese search-only near miss | Routed to literature search/reference management and explicitly said not to use the paper-to-PPT capability. |

The first explicit run exposed a real contract failure: without reading the QA
reference, Codex invented `completed_with_visual_qa_limitation` for the
no-renderer state. The root Skill was therefore changed to carry the exact
terminal states itself. The same probe then returned
`structurally-verified-with-disclosure`, matching the canonical contract.

Codex emitted warnings that its remote featured-plugin catalog required ChatGPT
authentication. Those warnings did not affect project-level Skill discovery or
the completed responses. Persistent Codex marketplace installation remains a
separate distribution check; direct project-level Skill loading passed.

### Claude Code

Interactive development loading used:

```text
claude --plugin-dir ./plugins/paper2ppt --permission-mode plan \
  --debug-file <DEBUG_LOG>
```

The debug trace reported one enabled plugin, zero plugin errors, one Skill from
the default plugin `skills/` directory, and one total plugin Skill. Typing
`/pap` and accepting completion produced the exact invocation
`/paper2ppt:paper2ppt`. `/reload-plugins` preserved the same discoverable
namespaced Skill.

The first trace also showed that the manifest's explicit custom `skills` path
performed a redundant second scan and loaded zero additional Skills, while the
default directory had already loaded the correct Skill. The Claude manifest now
omits that redundant field and relies on documented default `skills/`
discovery. After reload the trace showed zero custom skill paths, one Skill from
the default directory, and one total plugin Skill.

The configured default `claude-fable-5` route returned HTTP 502 twice before a
model turn; excluding user settings reached first-party OAuth but returned HTTP
403. Repeating the same plugin checks with `--model sonnet` succeeded through
the configured gateway (`claude-sonnet-5` in the result metadata):

| Case | Observed result |
| --- | --- |
| Explicit `/paper2ppt:paper2ppt` | Returned `skill_id=paper2ppt`, Simplified Chinese default, the exact primary and conditional outputs, all three QA gates, and `structurally-verified-with-disclosure`. |
| Implicit English paper-to-PPTX request with only the `Skill` tool enabled | Automatically loaded `paper2ppt`, then returned the same output and completion-state contract without creating files or using other tools. |
| Chinese search-only near miss | Said `paper2ppt` was not applicable to literature search or RIS export. |

An earlier implicit probe prohibited every tool, including the `Skill` tool,
and therefore did not load the Skill. It is retained as a constraint check, not
counted as an activation failure. The successful retry enabled only `Skill`,
which isolates automatic routing from extraction, authoring, and file changes.

### Client-verification conclusion

- Codex direct Skill discovery, positive routing, near-miss routing, and exact
  output/QA contract: pass after the terminal-state fix.
- Claude plugin manifest, default Skill discovery, namespaced invocation, and
  reload: pass after removing the redundant manifest path.
- Claude explicit invocation, implicit positive routing, near-miss routing, and
  exact output/QA contract: pass with `sonnet`. The local default Fable gateway
  route remained unavailable, an environment/model-route issue rather than a
  plugin loading failure.

### Installed helper path correction

Final review identified that the first client probes summarized the contract
without executing packaged helpers. The active instructions still used
CWD-relative `python scripts/...` commands, which would fail from an unrelated
user project or could execute a same-named project script. The root Skill now
resolves `<SKILL_DIR>` from `${CLAUDE_SKILL_DIR}` in Claude Code or the absolute
Skill file path in Codex's available-skills entry, and every runtime helper
command uses that directory.

A regression test copies the complete packaged Skill to an installation
directory, changes the process CWD to a separate project, then invokes both
`preflight.py` and `inspect_pptx.py` from the installed Skill path. Both helpers
complete successfully, and active Skill surfaces reject CWD-relative helper
commands.
