---
name: slidemuse
description: 将书籍、PDF、论文、报告或文字材料制作成视觉优先的图片版 PPT，适用于竞赛、答辩、路演、课程展示和读书分享；在用户明确要求时按 Scene v1 还原可编辑 PPTX。流程包含需求和大纲确认、四套风格选型及逐页生图；不用于直接修改已有可编辑 PPTX。
---

# SlideMuse · 2.17.0

本技能只有一条主流程：**内容提炼 → 图片 PPT 生成 → 可编辑 PPTX 还原**。
用户负责确认内容与风格，Agent 负责按已确认规格执行；不得把流程改写成“先做原生信息层”的编辑优先路线。

## 运行环境

- 常用本地操作优先使用根目录 `slidemuse.py`：[命令指南](docs/cli.md)。入口自动选择当前安装目录的 `.venv`，保留任务路径、原脚本参数和退出码；`doctor --json` 可独立诊断缺失依赖。高级脚本继续按下方方式执行。
- 通过仓库根目录的 `install.py` 安装时，技能目录会创建独立的 `.venv`，并在 `.skill-python` 中记录解释器绝对路径。
- 执行任何 `scripts/*.py` 前，若 `.skill-python` 存在，优先使用其中的解释器；否则使用可用的 Python 3.10+。
- 下文命令中的 `python` 均表示上述技能解释器，不要求用户把依赖安装进全局 Python 环境。
- 任务材料和产物必须放在独立工作目录，不得写入技能安装目录。
- 已确认的 Page Spec 和已准备的 Scene 可使用[可恢复交付流水线](references/pipeline.md)统一编译、逐页渲染、审查和生成待办；待审记录必须实际审阅后填写，不得自动改为通过。
- `init_deck.py` 只生成任务配置，`run_deck.py --check` 只读预检。中文待办定位问题页面及文件；工具不会替代需求确认、图片批准或真实审阅。
- 可编辑编译和审计提供[原生文字溢出预警](references/text-layout.md)，定位文本框和表格单元格。估算无风险不代表放得下；风险项须实际查看渲染，不自动缩字、删内容或填写通过。
- 流水线渲染后生成[本地逐页审阅面板](references/review-panel.md)，可对照画面填写记录、下载并导入；导入后需重新运行评分，不自动通过。

## 平台与生图后端

- **最佳推荐：Codex + GPT Image 2.5。** Codex 暴露模型选择时，风格探索优先使用 GPT Image 2.5 Flare，成品页与精确参考编辑优先使用 GPT Image 2.5 Sunburst。
- Codex 未暴露型号时调用其当前生图能力，不得声称指定了某个 2.5 子型号。
- 其他 Agent 必须调用该 Agent 自身提供或已连接的图像生成/编辑能力，不得假设存在 Codex 专属工具。
- 仓库脚本不负责生图、OCR 或视觉理解，也不自动调用收费 API。

## 强制流程契约

以下是本技能的默认流程；明确的跳过、代定或代选授权只改变对应环节，不扩大其他阶段的授权：

1. 每次行动前判断状态，只执行状态表允许的动作。
2. 五项需求未齐时只确认缺失项；可检查文件存在性和页数等元数据，不得阅读正文、提炼内容或生图。
3. 内容大纲必须展开成可审阅的逐页内容稿，经内容质量自检后单独展示。自检未通过时留在 S1 修正；通过后未获确认或明确代定授权时进入 S2 等待，不得生成风格总览。对应授权已明确时记录后继续，自检仍不可省略。
4. 风格未锁定时默认生成四张独立的幻灯片浏览视图并等待选择；具体豁免只按“风格门禁”执行，不得自行判断跳过。
5. 新材料必须先完成图片版。用户一开始要求可编辑版表示已授权最后阶段，但不能跳过图片版直接创作原生 PPTX。
6. Step 2 开始前必须创建并验证 `page-spec.json`。它保存已确认文字、数据、来源、元素意图和稳定 ID；Step 3 不得重新 OCR 或改写其中的已知内容。
7. “帮我做 PPT”“直接做一份”“按技能制作”不构成跳步授权。只按用户明确说出的跳过、代定或代选范围快进。
8. 用户新指令与旧规格冲突时，按[变更与恢复规则](references/workflow-updates.md)更新已有规格、回退状态并标记受影响产物；尚未创建的 Page Spec 不提前创建。
9. 当前 Agent 没有生图能力时停在对应状态并说明，不能用占位图冒充结果。

## 状态机

| 状态 | 进入条件 | 允许动作 | 阶段出口 |
|---|---|---|---|
| S0 需求未齐 | 五项需求至少一项未明确且无对应代定授权 | 询问缺失项；检查文件元数据 | 用户补充或明确授权 |
| S1 内容提炼 | 五项需求齐全或缺失项已获代定授权 | 阅读材料、创建逐页内容稿、自检、修正并展示 | 自检通过且已展示后：无内容授权进入 S2；已有对应授权进入 S3 |
| S2 等待内容确认 | 逐页内容稿已自检通过并展示 | 接收确认或修改；受影响内容回 S1 修正和自检 | 当前内容版本获确认或明确代定 |
| S3 风格方案 | 当前内容稿自检通过、已展示且获确认或明确代定 | 按风格门禁生成四套总览或记录合法豁免 | 总览已展示或风格已合法锁定 |
| S4 等待风格确认 | 四套总览已展示 | 接收选择/修改；已授权代选时记录选择 | 视觉规范锁定 |
| S5 图片版制作 | 内容和风格均锁定 | 创建 Page Spec、逐页生成、验收并合并图片版 | 图片版交付或进入已授权 S6 |
| S6 可编辑重建 | 用户明确要求可编辑，或要求从已有页面直接还原 | 分层、编写 Scene、编译、审查和渲染核对 | 可编辑交付完成 |
| DONE 已交付 | 已完成用户要求的交付范围 | 记录交付版本；收到修改时按变更表恢复 | 本轮交付结束 |

已有页面图片/扫描 PDF 要求还原时可从 S6 开始；先确认输入范围、原比例和编辑目标，再创建 `page-spec.json` 记录可见内容。
已有可编辑 PPTX 只做普通修改时不走本技能，应保留原生结构；本技能已有 Scene 的后续修改按变更表恢复 S6。

## S0：确认五项需求

一次集中询问尚未明确的项目，已提供的不得重复询问：

1. **源材料**：附件、路径、PDF、书籍或粘贴文字。
2. **参考风格**：模板/图片/文字描述，或明确“没有参考风格”。
3. **使用场景与受众**：课堂、读书分享、组会、周报、项目汇报、路演等。
4. **页数预期**：固定页数、范围，或明确授权根据内容推荐。
5. **交付范围**：图片版，或图片版完成后继续还原可编辑版。

“没有参考风格”“页数由你推荐”“其余由你决定”是有效授权，必须原样记录。

## 制作规格

进入 S1 或 S6 后，把 [规格模板](references/deck-spec-template.md) 复制到任务目录并填写为 `deck-spec.md`。任务目录与技能安装目录分离。

恢复任务、上下文压缩、用户改需求或阶段转换时，先读取并更新规格。用户修改或恢复到不同版本时读取[变更与恢复规则](references/workflow-updates.md)，核对基准图版本和已授权差异。规格记录状态、授权、确认版本、页序、生成状态、质量检查和交付路径。

## Step 1A：内容提炼与确认（S1 → S2）

进入后读取 [Prompt 1A](references/prompts.md) 和[内容深度与自检](references/content-outline.md)。论文和长篇报告/政策按需读取[材料审阅](references/material-reading.md)，核对方法解释、实验口径、来源冲突及目标与观测的区别。

1. 阅读材料，明确受众需要理解或决定的问题、整套回答和页间推进关系；按场景组织，避免只有目录和数据罗列。
2. 把完整页序和逐页内容稿写入 `deck-spec.md`。内容页写出主要结论、支撑要点、可定位的证据、解释及适用边界；区分页面实际展示的文字/图表与可选讲稿。封面、过渡等页面按其作用处理。
3. 按内容深度参考进行语义自检，记录当前版本、各项判断及问题页。论点无支撑、关键问题未回答、口径错误或内容空洞时先修正；材料不足就缩小结论、调整页序或列出必须补充的信息，不靠增加字数或编造因果过关。
4. 自检通过后，单独展示整套叙事、每页结论与实际展示内容、证据/解释及待确认项，不能只展示标题表或文件链接。缺少对应确认或代定授权时进入 S2 并停止；已有授权时记录原文、范围与当前版本后进入 S3。结合上下文判断授权，不要求固定口令，也不把单独的“继续”扩大成全阶段代定。
5. 用户要求修改时只更新受影响页面，重做相关自检并再次展示；明确指定的修改是对该变更的授权，已明确的授权不重复询问。未决定的内容仍按门禁等待。自检通过不代表用户已确认，用户授权也不替代自检。

## Step 1B：风格方案与确认（S3 → S4）

进入后读取 [Prompt 1B](references/prompts.md) 和[缩略图总览验收](references/style-options.md)，按以下确定规则执行：

| 用户指令 | 动作 |
|---|---|
| 无参考或只有宽泛风格方向 | 必须生成四套总览并等待选择 |
| 提供参考但未明确“一比一沿用/严格照此制作” | 基于参考生成四套不越界的演绎并等待选择 |
| 明确要求严格沿用指定模板/母版/页面风格 | 记录 `locked-reference`，不生成四套；把参考转成文字视觉规范 |
| 明确说“跳过四套预览” | 记录 `skipped` 和授权原文；使用已给风格或请求其授权代定 |
| 明确说“你代选” | 仍生成四套，Agent 选择并记录理由与 `delegated` |

四套总览必须使用同一组代表页和相同内容，只改变视觉系统：总页数不超过 8 页时展示全部，超过 8 页时选 6–8 个覆盖主要页面类型的代表页。缩略页沿用任务指定比例，网格按数量适配，不补造页面。分别保存并展示方案 1–4；不得把四套拼成一张四宫格或用纯文字替代。总页数为 1 时，每套自然只有一页。

总览默认采用横向 16:9 画布，缩略页等大、完整、留有间距，页码在缩略页下方；3 页采用 2×2 网格并留空一格，不做纵向整页长图。重试沿用原方案编号并明确说明替换哪一版，交付只列每套最新验收版，历史稿不作为新增方案。

每套直接用一次生图生成含全部代表页的缩略图总览，正常四套共四次调用。风格选定前不逐页生成高清成品，再拼成总览。仅尺寸、排列、边距或外部页码有问题时，使用 `build_style_overview.py` 对已有图片本地缩放排版；需要拆分长图时先视觉确认每页裁切框，不为排版再次调用生图。内容或视觉本身有错才考虑针对性生图修复，并记录额外调用。

实际生成四套时，把当前候选写入 `style-options.json`，逐张核对缩略页网格与内容，并执行以下检查。结构与视觉检查均通过后，才进入 S4 宣布当前四套方案已齐；不将修正中间稿计为新方案。合法豁免四套预览的任务不要求创建此清单。

```sh
python "<skill-dir>/scripts/validate_style_options.py" "<work>/style-options.json"
```

## Step 2：生成图片版 PPT（S5）

进入后读取 [Prompt 2](references/prompts.md)、[Page Spec](references/page-spec.md) 和 [模型说明](references/models.md)。含定量图表时读取[图表可靠性](references/chart-reliability.md)。

1. 把确认后内容稿中所有页面展示内容与锁定视觉规范写入 `page-spec.json`，保留支撑结论的解释和必要边界，不能缩回“标题 + 大数字”；可选讲稿留在 `deck-spec.md`。新任务把配色、字体字号、网格间距和图片处理写入 `style.tokens`，保留可读的 `visual_spec`；若有已选参考图，写入 `reference_images`。每页为所有已知文字、数据、视觉主体和图表分配稳定 ID；位置可先写 `bbox_hint`。
2. 生成第一张图片前必须运行：

```sh
python "<skill-dir>/scripts/validate_page_spec.py" "<work>/page-spec.json" --strict
```

内容稿已有可选讲稿时，按[讲稿保留](references/speaker-notes.md)同步到 `slides[].speaker_notes`，不加入生图可见文案；图片版构建器会保存已声明讲稿。

3. 按 `01-title.png`、`02-title.png` 的零填充序号逐页生成。每次提示包含锁定视觉规范、Page Spec 中的准确内容、页码和总页数。
4. 每页立即检查画幅、文字、数据、裁切、溢出和跨页一致性。含关键数字、日期、专名或必现图表标签的页面，可按 [Page Spec 内容核对](references/page-spec.md)建立绑定当前图片哈希的看图记录，并运行 `audit_page_content.py`；缺失项修复后才能批准该页。脚本只比对观察记录，不负责 OCR；图表数据及未识别的小字仍需视觉核对。通过后更新最终图片路径、状态、提示词和必要的 `bbox_hint`。失败只重做对应页。
5. 同一页文字连续两次不准确时停止重试：按 Prompt 2A 生成保留全部主视觉的无字页面，再用 `scripts/overlay_text.py` 叠加准确文字并栅格化；叠字前后核对主视觉未丢失。Step 2 不提前移除 Step 3 才需拆分的主体。
   图表数字与几何分别检查，并检查未声明的数据视觉。同一几何问题连续两次检查失败时停止生图重试，按图表可靠性参考准备精确区域修复；程序改图须遵守当前宿主工具的授权要求，既有授权覆盖时不重复询问。
6. 全部页面通过后运行交付验证和合并：

```sh
python "<skill-dir>/scripts/validate_page_spec.py" "<work>/page-spec.json" --require-images --strict
python "<skill-dir>/scripts/build_image_ppt.py" "<work>/page-spec.json" "<work>/output/image-deck.pptx"
```

7. 导出按 Page Spec 的批准图片清单、页序和画幅进行；旧稿留在目录中不会加入成品。使用 `render_deck.py` 渲染并查看 `review.png`、`render-report.json`，核对页数、页序、画幅、文字和裁切。无可用渲染器时记录限制，不得声称视觉验收通过。未授权 S6 时记录 DONE 并交付；已授权时更新规格后进入 S6。

```sh
python "<skill-dir>/scripts/render_deck.py" "<work>/output/image-deck.pptx" "<work>/output/image-review" --page-spec "<work>/page-spec.json"
```

## Step 3：还原可编辑 PPTX（S6）

进入后读取 [Prompt 3](references/prompts.md)、[重建与分层](references/reconstruction.md) 和 [Scene 协议](references/scene-format.md)。

1. 以 `page-spec.json` 为语义事实源、验收后的页面图片为视觉事实源。直接还原任务先从可见页面建立 Page Spec；用户要求保留原内容即视为对转录目标的授权，不代表低置信度文字已确认。
2. Page Spec 已记录的文字、数据、来源和 ID 直接复用，不重新 OCR、改写或更换。按变更记录识别重建后的已授权修改；只有未记录或超出授权的图文冲突才请求确认。
3. 每次处理 1–3 页，补齐精确坐标、层级、素材和置信度。文字、简单几何、表格和可靠数据图使用原生对象；复杂视觉拆成独立图片对象。
4. 从背景移除所有原生化文字和已拆主体并补全背景。原始整页图片只作核对证据，不能作为可编辑版底图。
5. 按 [JSON Schema](references/scene.schema.json) 编写 `scene.json`，然后编译和审查：

```sh
python "<skill-dir>/scripts/build_editable_ppt.py" "<work>/scene.json" "<work>/output/editable.pptx" --page-spec "<work>/page-spec.json"
python "<skill-dir>/scripts/audit_editability.py" "<work>/output/editable.pptx" --scene "<work>/scene.json" --output "<work>/output/editability.json"
```

6. 使用 `render_deck.py` 实际渲染并与 Page Spec 中已验收的基准图逐页核对，再抽查移动主体、修改文字和编辑图表数据。`review.png` 的第三列是像素差异，仅供定位，不能单凭差异数值判定合格。问题只修对应 Scene 元素或素材；同一问题连续两次无效时记录限制。

```sh
python "<skill-dir>/scripts/render_deck.py" "<work>/output/editable.pptx" "<work>/output/editable-review" --page-spec "<work>/page-spec.json"
```

质量回归或版本发布时读取[交付评测](references/evaluation.md)，为整套页面建立内容观察和逐页视觉复核记录，再运行 `evaluate_delivery.py` 生成与当前 PPTX、Page Spec、渲染图和记录哈希绑定的评分卡；可编辑版同时传入 Scene。评分卡为 `pass` 才可声称该版本通过完整评测，`incomplete` 不能视为通过。普通交付仍按上述逐页验收，不强制生成评测记录。

## 交付契约

- **图片版**：`image-deck.pptx`、有序页面图片、`page-spec.json`、实际预览/检查说明。
- **可编辑版**：在图片版基础上增加 `editable.pptx`、`scene.json`、引用的 `assets/`、`editability.json` 和渲染预览。
- 说明字体替代、低置信度识别、AI 补全、独立栅格对象和待人工处理项。
- 不能把整页截图加少量文本框、整页 SVG 或未拆分背景称作“每个元素可编辑”。
- 默认不反复展示检查图、初稿和修复稿；工具已显示的图片不再重复嵌入。风格选择只列每套最新验收版，最终只列批准版本及一个清晰预览。用户需要比较或某页需决策时，明确页码/版本后展示相关图；检查与历史证据仍保存到任务目录。
- 无渲染器时写明“仅完成结构验证”，不能声称视觉验收通过。

## 资源路由

- [prompts.md](references/prompts.md)：进入对应 Step 后只读该阶段提示词。
- [content-outline.md](references/content-outline.md)：S1/S2 创建、审阅和修改逐页内容稿时读取；提供深度判断、反例和内容自检，不以字数或字段齐全替代语义审阅。
- [material-reading.md](references/material-reading.md)：S1 阅读论文或长篇报告/政策时按需读取，审阅机制解释、实验口径、实施关系与来源冲突。
- [speaker-notes.md](references/speaker-notes.md)：有可选讲稿的 S5/S6 或仅修改讲稿时读取；保留演讲备注、核对实际 PPTX，按需导出独立讲稿。
- [style-options.md](references/style-options.md)：仅 S3 生成、修正和验收四套缩略图总览时读取。
- [page-spec.md](references/page-spec.md)：仅 S5/S6 创建或更新 Page Spec 时读取。
- [workflow-updates.md](references/workflow-updates.md)：仅用户改需求、交付后修改或跨版本恢复时读取。
- [data-bindings.md](references/data-bindings.md)：修改表格/图表数据及其依赖正文、百分比、差额和讲稿时读取；提供可选契约、差异预览、独立待审草稿与交付检查，不代替来源和语义复核。
- [models.md](references/models.md)：S3/S5 生图，以及 S6 需要背景清理/主体分离时读取。
- [reconstruction.md](references/reconstruction.md) 与 [scene-format.md](references/scene-format.md)：仅 S6 读取。
- [evaluation.md](references/evaluation.md)：仅质量回归、版本发布或需要可复跑评分卡时读取。
- [benchmark.md](references/benchmark.md)：仅跨材料评测时读取；冻结全部案例、保留首次与修复后成绩、验证实际产物证据并按类别/划分汇总。
- [pipeline.md](references/pipeline.md)：已准备好 Page Spec/Scene 后，使用可恢复交付、渲染超时、环境指纹、可选 PowerPoint 实测及逐页待办。
- [production-metrics.md](references/production-metrics.md)：完整制作或质量回归时，推荐从实际开始记录制作事件；保留生图次数、返修页、实测耗时与首次/最终交付结果。缺失部分不能凭估计补零。
- [chart-reliability.md](references/chart-reliability.md)：S5 定量图表检查、有限修复或完整评测时读取；包括几何观察与精确水平条形区域兜底。
- `validate_page_spec.py`：验证内容确认、页序、稳定 ID、画布边界和图片交付状态。
- `overlay_text.py`：仅作为 Step 2 图片页的准确文字兜底。
- `build_image_ppt.py`：仅用于 Step 2 图片版合并。
- `render_deck.py`：渲染 PPTX 全部页面，生成逐页 PNG、总览和可选基准图对照；自动选择可用的 PowerPoint 或 LibreOffice/Poppler 后端。
- `audit_page_content.py`：比对看图或 OCR 的逐页文字观察记录与 Page Spec，并拒绝复用图片哈希已变化的旧记录。
- `plan_deck_update.py`：修改前保存已批准页面和参考图哈希，修改后规划需重做、复查或可复用的页面；不自动更改批准状态。
- `evaluate_delivery.py`：汇总内容、视觉和可编辑性证据，拒绝旧版渲染或复核记录，产出交付评分卡。
