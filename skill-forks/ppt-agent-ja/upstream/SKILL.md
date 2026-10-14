---
name: ppt-agent
description: 专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流（需求调研 -> 资料搜集 -> 大纲策划 -> 策划稿 -> 设计稿），输出高质量 HTML 格式演示文稿。当用户提到制作 PPT、做演示文稿、做 slides、做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发此技能。即使用户只说"帮我做个关于 X 的介绍"或"我要给老板汇报 Y"，只要暗示需要结构化的多页演示内容，都应该触发。也适用于用户说"帮我把这篇文档做成 PPT"、"把这个主题做成演示"等需要将内容转化为演示格式的场景。
---

# PPT Agent -- 专业演示文稿全流程生成

## 核心理念

模仿专业 PPT 设计公司（报价万元/页级别）的完整工作流，而非"给个大纲套模板"：

1. **先调研后生成** -- 用真实数据填充内容，不凭空杜撰
2. **策划与设计分离** -- 先验证信息结构，再做视觉包装
3. **内容驱动版式** -- Bento Grid 卡片式布局，每页由内容决定版式
4. **全局风格一致** -- 先定风格再逐页生成，保证跨页统一
5. **智能配图** -- 利用图片生成能力为每页配插图（绝大多数环境都有此能力）

---

## 环境感知

开始工作前自省 agent 拥有的工具能力：

| 能力 | 降级策略 |
|------|---------|
| **信息获取**（搜索/URL/文档/知识库） | 全部缺失 -> 依赖用户提供材料 |
| **图片生成**（绝大多数环境都有） | 缺失 -> 纯 CSS 装饰替代 |
| **文件输出** | 必须有 |
| **脚本执行**（Python/Node.js） | 缺失 -> 跳过自动打包和 SVG 转换 |

**原则**：检查实际可调用的工具列表，有什么用什么。

---

## 路径约定

整个流程中反复用到以下路径，在 Step 1 完成后立即确定：

| 变量 | 含义 | 获取方式 |
|------|------|---------|
| `SKILL_DIR` | 本 SKILL.md 所在目录的绝对路径 | 即触发 Skill 时读取 SKILL.md 的目录 |
| `OUTPUT_DIR` | 产物输出根目录 | 用户当前工作目录下的 `ppt-output/`（首次使用时 `mkdir -p` 创建） |

后续所有路径均基于这两个变量，不再重复说明。

---

## 输入模式与复杂度判断

### 入口判断

| 入口 | 示例 | 从哪步开始 |
|------|------|-----------| 
| 纯主题 | "做一个 Dify 企业介绍 PPT" | Step 1 完整流程 |
| 主题 + 需求 | "15 页 AI 安全 PPT，暗黑风" | Step 1（跳部分已知问题）|
| 源材料 | "把这篇报告做成 PPT" | Step 1（材料为主）|
| 已有大纲 | "我有大纲了，生成设计稿" | Step 4 或 5 |

### 跳步规则

跳过前置步骤时，必须补全对应依赖产物：

| 起始步骤 | 缺失依赖 | 补全方式 |
|---------|---------|---------|
| Step 4 | 每页内容文本 | 先用 Prompt #3 为每页生成内容分配 |
| Step 5 | 策划稿 JSON | 用户提供或先执行 Step 4 |

### 复杂度自适应

根据目标页数自动调整流程粒度：

| 规模 | 页数 | 调研 | 搜索 | 策划 | 生成 |
|------|------|------|------|------|------|
| **轻量** | <= 8 页 | 3 题精简版（场景+受众+补充信息） | 3-5 个查询 | Step 3 可与 Step 4 合并一步完成 | 逐页生成 |
| **标准** | 9-18 页 | 完整 7 题 | 8-12 个查询 | 完整流程 | 按 Part 分批，每批 3-5 页 |
| **大型** | > 18 页 | 完整 7 题 | 10-15 个查询 | 完整流程 | 按 Part 分批，每批 3-5 页，批间确认 |

---

## 6 步 Pipeline

### Step 1: 需求调研 [STOP -- 必须等用户回复]

> **禁止跳过。** 无论主题多简单，都必须提问并等用户回复后才能继续。不替用户做决定。

**执行**：使用 `references/prompts.md` Prompt #1
1. 搜索主题背景资料（3-5 条）
2. 根据复杂度选择完整 7 题或精简 3 题，一次性发给用户
3. **等待用户回复**（阻断点）
4. 整理为需求 JSON

**7 题三层递进结构**（轻量模式只问第 1、2、7 题）：

| 层级 | 问题 | 决定什么 |
|------|------|---------|
| 场景层 | 1. 演示场景（现场/自阅/培训） | 信息密度和视觉风格 |
| 场景层 | 2. 核心受众（动态生成画像） | 专业深度和说服策略 |
| 场景层 | 3. 期望行动（决策/理解/执行/改变认知） | 内容编排的最终导向 |
| 内容层 | 4. 叙事结构（问题->方案/科普/对比/时间线） | 大纲骨架逻辑 |
| 内容层 | 5. 内容侧重（搜索结果动态生成，可多选） | 各 Part 主题权重 |
| 内容层 | 6. 说服力要素（数据/案例/权威/方法，可多选） | 卡片内容类型偏好 |
| 执行层 | 7. 补充信息（演讲人/品牌色/必含/必避/页数/配图偏好） | 具体执行细节 |

**产物**：需求 JSON（topic + requirements）

---

### Step 2: 资料搜集

> 盘点所有信息获取能力，全部用上。

**执行**：
1. 根据主题规划查询（数量参考复杂度表）
2. 用所有可用的信息获取工具并行搜索
3. 每组结果摘要总结

**产物**：搜索结果集合 JSON

---

### Step 3: 大纲策划

**执行**：使用 `references/prompts.md` Prompt #2（大纲架构师 v2.0）

**方法论**：金字塔原理 -- 结论先行、以上统下、归类分组、逻辑递进

**自检**：页数符合要求 / 每 part >= 2 页 / 要点有数据支撑

**产物**：`[PPT_OUTLINE]` JSON

---

### Step 4: 内容分配 + 策划稿 [建议等用户确认]

> 将内容分配和策划稿生成合为一步。在思考每页应该放什么内容的同时，决定布局和卡片类型，更自然高效。

**执行**：使用 `references/prompts.md` Prompt #3（内容分配与策划稿）

**要点**：
- 将搜索素材精准映射到每页
- 为每页设计多层次内容结构（主卡片 40-100 字 + 数据亮点 + 辅助要点）
- 同时确定 page_type / layout_hint / cards[] 结构
- **每个内容页至少 3 张卡片 + 2 种 card_type + 1 张 data 卡片**
- 布局选择参考 `references/bento-grid.md` 的决策矩阵

向用户展示策划稿概览，建议等用户确认后再进入 Step 5。

**产物**：每页策划卡 JSON 数组 -> 保存为 `OUTPUT_DIR/planning.json`

---

### Step 5: 风格决策 + 设计稿生成

分三个子步骤，**顺序不可颠倒**：

#### 5a. 风格决策

**执行**：阅读 `references/styles/index.md` 主索引（含决策矩阵），按主题关键词匹配 26 种预置风格之一

**26 风格按 5 板块分组**（详细 JSON 定义在板块文件中）：

| 板块 | 数量 | 风格 ID | 板块文件 |
|------|------|--------|---------|
| 暗色专业 | 7 | dark_tech / xiaomi_orange / luxury_purple / nocturne_violet / cyberpunk_neon / chrome_y2k / noir_film | `references/styles/dark.md` |
| 浅色高级 | 8 | blue_white / fresh_green / minimal_gray / mocha_editorial / medical_pulse / earth_concrete / champagne_gold / liquid_glass | `references/styles/light.md` |
| 活力鲜明 | 4 | vibrant_rainbow / kindergarten_pop / bauhaus_block / candy_pastel | `references/styles/vibrant.md` |
| 东方文化 | 3 | royal_red / sakura_wabi / ink_jade | `references/styles/cultural.md` |
| 自然/复古 | 4 | botanic_forest / safari_savanna / retro_70s / gov_authority | `references/styles/natural.md` |

**风格预览**：执行 `python3 SKILL_DIR/scripts/gallery.py` 生成 `ppt-output/style-gallery/index.html`，浏览器打开可视化对比 26 风格。

**也必读**：`references/typography.md`（排版铁律：字距 / tabular-nums / OpenType / serif italic 混排 / 首字下沉 / 不对称网格 / 字体栈三层降级 / 微妙纹理）

**产物**：风格定义 JSON -> 保存为 `OUTPUT_DIR/style.json`

#### 5b. 智能配图（根据用户偏好）

> 在需求调研（Step 1 第 7 题）中确认用户的配图偏好后执行。如果用户选择"不需要配图"则跳过。

##### 配图时机

在生成每页 HTML **之前**，先为该页生成配图。每页至少 1 张（封面页、章节封面必须有），生成后保存到 `OUTPUT_DIR/images/`。

##### generate_image 提示词构造公式

提示词必须同时满足 **4 个维度**，按以下公式组装：

```
[内容主题] + [视觉风格] + [画面构图] + [技术约束]
```

| 维度 | 说明 | 示例 |
|------|------|------|
| 内容主题 | 从该页策划稿 JSON 的核心概念提炼，具体到场景/对象 | "DMSO molecular purification process, crystallization flask with clear liquid" |
| 视觉风格 | 与 style.json 的配色方案和情感基调对齐 | 暗黑科技 -> "deep blue dark tech background, subtle cyan glow, futuristic" |
| 画面构图 | 根据图片在页面中的放置方式决定 | 右侧半透明 -> "clean composition, main subject on left, fade to transparent on right" |
| 技术约束 | 固定后缀，确保输出质量 | "no text, no watermark, high quality, professional illustration" |

##### 风格与配图关键词对应

| PPT 风格 | 配图风格关键词 |
|---------|--------------|
| 暗黑科技 | dark tech background, neon glow, futuristic, digital, cyber |
| 小米橙 | minimal dark background, warm orange accent, clean product shot, modern |
| 蓝白商务 | clean professional, light blue, corporate, minimal, bright |
| 朱红宫墙 | traditional Chinese, elegant red gold, ink painting, cultural |
| 清新自然 | fresh green, organic, nature, soft light, watercolor |
| 紫金奢华 | luxury, purple gold, premium, elegant, metallic |
| 极简灰白 | minimal, grayscale, clean, geometric, academic |
| 活力彩虹 | colorful, vibrant, energetic, playful, gradient, pop art |

##### 按页面类型调整

| 页面类型 | 图片特征 | Prompt 额外关键词 |
|---------|---------|-----------------|
| 封面页 | 主题概览，视觉冲击 | "hero image, wide composition, dramatic lighting" |
| 章节封面 | 该章主题的象征性视觉 | "symbolic, conceptual, centered composition" |
| 内容页 | 辅助说明，不喧宾夺主 | "supporting illustration, subtle, background-suitable" |
| 数据页 | 抽象数据可视化氛围 | "abstract data visualization, flowing lines, tech" |

##### 禁止事项
- 禁止图片中出现文字（AI 生成的文字质量差）
- 禁止与页面配色冲突的颜色（暗色主题配暗色图，亮色主题配亮色图）
- 禁止与内容无关的装饰图（每张图必须与该页内容有语义关联）
- 禁止重复使用相同 prompt（每页图片必须独特）

**产物**：`OUTPUT_DIR/images/` 下的配图文件

#### 5c. 逐页 HTML 设计稿生成

**执行**：使用 `references/prompts.md` Prompt #4 + `references/bento-grid.md`

> **禁止跳过策划稿直接生成。** 每页必须先有 Step 4 的结构 JSON。

**每页 Prompt 组装公式**：
```
Prompt #4 模板
+ 风格定义 JSON（5a 产物）[必须]
+ 该页策划稿 JSON（Step 4 产物，含 cards[]/card_type/position/layout_hint）[必须]
+ 该页内容文本（Step 4 产物）[必须]
+ 配图路径（5b 产物）[可选 -- 无配图时省略 IMAGE_INFO 块]
```

**核心设计约束**（完整清单见 Prompt #4 内部）：
- 画布 1280x720px，overflow:hidden
- 所有颜色通过 CSS 变量引用，禁止硬编码
- 凡视觉可见元素必须是真实 DOM 节点，图形优先用内联 SVG
- 禁止 `::before`/`::after` 伪元素用于视觉装饰、禁止 `conic-gradient`、禁止 CSS border 三角形
- 配图融入设计：渐隐融合/色调蒙版/氛围底图/裁切视窗/圆形裁切（技法详见 Prompt #4）

**分批策略**：按 Part 为单位分批生成，每批 3-5 页。每批完成后将 HTML 写入 `OUTPUT_DIR/slides/` 目录，再开始下一批。避免上下文爆炸的同时保证同一 Part 内的风格一致性。

**跨页视觉叙事**（让 PPT 有节奏感，不只是独立页面的堆砌）：

| 策略 | 规则 | 原因 |
|------|------|------|
| **密度交替** | 高密度页（混合网格/英雄式）后面跟低密度页（章节封面/单一焦点），形成张弛有度的节奏 | 连续 3+ 页高密度内容会导致观众视觉疲劳 |
| **章节色彩递进** | Part 1 卡片主用 accent-1，Part 2 用 accent-2，Part 3 用 accent-3 ... 每章换一种 accent 主色 | 通过颜色让受众无意识感知章节切换 |
| **封面-结尾呼应** | 结束页的视觉元素与封面页形成呼应（相同装饰图案、对称布局），给出完整闭环感 | 首尾呼应是最基本的叙事美学 |
| **渐进揭示** | 同一概念跨多页展开时，视觉复杂度应递增（第1页简单色块 -> 第2页加数据 -> 第3页完整图表） | 引导观众逐步深入理解 |

**产物**：每页一个 HTML 文件 -> `OUTPUT_DIR/slides/`

---

### Step 6: 后处理 [必做 -- HTML 生成完后立即执行]

> **禁止跳过。** HTML 生成完后必须自动执行以下四步，不要停在 preview.html 就结束。

```
slides/*.html --> preview.html --> svg/*.svg --> presentation.pptx
```

**依赖检查**（首次运行自动执行）：
```bash
pip install python-pptx lxml Pillow 2>/dev/null
```

**依次执行**：

1. **合并预览** -- 运行 `html_packager.py`
   ```bash
   python3 SKILL_DIR/scripts/html_packager.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/preview.html
   ```

2. **SVG 转换** -- 运行 `html2svg.py`（DOM 直接转 SVG，保留 `<text>` 可编辑）
   > **重要**：HTML 设计稿必须遵守 `references/pipeline-compat.md` 中的管线兼容性规则，否则转换后会出现元素丢失、位置错位等问题。
   ```bash
   python3 SKILL_DIR/scripts/html2svg.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/svg/
   ```
   底层用 dom-to-svg（自动安装），首次运行会 esbuild 打包。
   **降级**：如果 Node.js 不可用或 dom-to-svg 安装失败，跳过此步和步骤 3，只输出 preview.html。

3. **PPTX 生成** -- 运行 `svg2pptx.py`（OOXML 原生 SVG 嵌入，PPT 365 可编辑）
   ```bash
   python3 SKILL_DIR/scripts/svg2pptx.py OUTPUT_DIR/svg/ -o OUTPUT_DIR/presentation.pptx --html-dir OUTPUT_DIR/slides/
   ```
   PPT 365 中右键图片 -> "转换为形状" 即可编辑文字和形状。

4. **通知用户** -- 告知产物位置和使用方式：
   - `preview.html` -- 浏览器打开即可翻页预览
   - `presentation.pptx` -- PPTX（右键 -> "转换为形状" 可编辑）
   - `svg/` -- 每个 SVG 也可单独拖入 PPT
   - **如果步骤 2-3 被降级跳过**，说明原因并告知用户手动安装 Node.js 后可重新运行

**产物**：preview.html + svg/*.svg + presentation.pptx

---

## 输出目录结构

```
ppt-output/
  slides/              # 每页 HTML
  svg/                 # 矢量 SVG（可导入 PPT 编辑）
  images/              # AI 配图
  preview.html         # 可翻页预览
  presentation.pptx    # 可编辑 PPTX（右键"转换为形状"）
  outline.json         # 大纲
  planning.json        # 策划稿
  style.json           # 风格定义
```

---

## 质量自检

| 维度 | 检查项 |
|------|-------|
| 内容 | 每页 >= 2 信息卡片 / >= 60% 内容页含数据 / 章节有递进 |
| 视觉 | 全局风格一致 / 配图风格统一 / 卡片不重叠 / 文字不溢出 |
| 技术 | CSS 变量统一 / SVG 友好约束遵守 / HTML 可被 Puppeteer 渲染 / `pipeline-compat.md` 禁止清单检查 |

---

## 资源路由表（字段 → 文件夹）

策划稿 JSON 中各字段决定从哪个目录抽取相应资源：

- 字段路由：`layout_hint→layouts/`、`page_type→page-templates/`、`card_type→blocks/`、`chart_type→charts/`

| 字段 | 取值 | 路由到 | 例 |
|------|------|-------|---|
| `layout_hint` | asymmetric / hero-top / l-shape / mixed-grid / primary-secondary / single-focus / symmetric / t-shape / three-column / waterfall | `references/layouts/<name>.md` | 主次结合 → `references/layouts/primary-secondary.md` |
| `page_type` | cover / toc / section / end | `references/page-templates/<name>.md` | 封面 → `references/page-templates/cover.md` |
| `card_type` | text / data / list / quote / timeline / comparison / diagram / image-hero / matrix-chart / people | `references/blocks/<name>.md` | 数据卡 → `references/blocks/card-styles.md` |
| `chart_type` | progress-bar / ring / sparkline / radar / funnel / kpi / metric-row / waffle / rating / timeline / treemap / comparison-bar / stacked-bar | `references/charts/<name>.md` | 雷达 → `references/charts/radar.md` |

## Step 0/1 采访模板规则

**Step 0 默认强制模板化**：主 agent 必须先生成 `OUTPUT_DIR/runtime/prompt-interview.md`，再依据渲染结果向用户发问；采访运行时模板必须按能力在 `tpl-interview-structured-ui.md` 与 `tpl-interview-text-fallback.md` 之间二选一。

**Step 0 优先结构化采访 UI**：只要当前 CLI 提供任何等价于 `AskUserQuestion` / `request_user_input` 的原生提问能力，主 agent 就必须优先使用结构化采访 UI；不支持时回退到 `tpl-interview-text-fallback.md`。

**Step 0 唯一例外**：仅当 prompt 生成在 Step 0 发生真实脚本接口故障，并已判定 `BLOCKED_SCRIPT_INTERFACE` 时，才允许主 agent 直接发问；但覆盖维度不得低于 `prompt-interview.md` 的最终要求。

详细模板：[`references/prompts/tpl-interview.md`](references/prompts/tpl-interview.md) · [`references/prompts/tpl-interview-structured-ui.md`](references/prompts/tpl-interview-structured-ui.md) · [`references/prompts/tpl-interview-text-fallback.md`](references/prompts/tpl-interview-text-fallback.md)

## Reference 文件索引

| 文件 | 何时阅读 | 关键内容 |
|------|---------|---------|
| `references/prompts.md` | 每步生成前（合并版）| 5 套 Prompt 模板（调研/大纲/策划/设计/备注）|
| `references/prompts/*.md` | 模块化版本（23 文件）| 按 step + module + tpl 拆分的 Prompt 模板 |
| `references/playbooks/*.md` | 每步执行手册（11 文件）| outline / research / source / style / step4 各 phase 的执行 playbook |
| `references/styles/index.md` | **Step 5a** | 26 种预置风格索引 + 决策矩阵 + JSON Schema |
| `references/styles/{dark,light,vibrant,cultural,natural}.md` | Step 5a 选定风格后 | 该板块所有风格的完整 JSON + CSS 变量 + Mock 链接 |
| `references/typography.md` | **Step 5c** | 排版铁律 14 条（字距/tabular-nums/OpenType/serif italic 混排/字体栈降级）|
| `references/charts/index.md` | **Step 5c 涉及数据可视化时** | 18 种图表索引 + 决策矩阵 |
| `references/charts/{basic,advanced,complex}.md` | 选定图表后 | 完整 HTML 模板（基础 8 种 / 进阶 6 种 / ECharts 级 4 种）|
| `references/charts/<chart_type>.md` | 单一图表精细规格 | sunbigfly 风格的单文件图表（13 个）|
| `references/layouts/*.md` | Step 5c layout_hint 路由 | 10 个 layout 各成文件（asymmetric / hero-top / l-shape 等）|
| `references/blocks/*.md` | Step 5c card_type 路由 | 9 个可复用卡片原型（card-styles / comparison / diagram / quote 等）|
| `references/page-templates/*.md` | Step 5c page_type 路由 | 4 个页面模板（cover / end / section / toc）|
| `references/principles/*.md` | **Step 4-5 自检与原则** | 8 设计原则 + failure-modes（cognitive-load / color-psychology / composition / data-visualization / narrative-arc / runtime-failure-modes / visual-hierarchy）|
| `references/design-runtime/*.md` | Step 5c 设计运行时 | css-weapons / data-type-decoration-mapping / data-type-visual-mapping / design-specs / director-command-rules-examples |
| `references/bento-grid.md` | Step 5c | 7 种布局精确坐标 + 5 种卡片类型 + 决策矩阵 |
| `references/method.md` | 初次了解 | 核心理念与方法论 |
| `references/pipeline-compat.md` | **Step 5c 设计稿生成时** | CSS 禁止清单 + 图片路径 + 字号混排 + SVG text + 环形图 + svg2pptx 注意事项 |
| `references/cli-cheatsheet.md` | 脚本调用查阅 | 所有 scripts 的完整调用命令速查 |
| `references/style-system.md` | （兼容引导文件） | 已升级为引导文件，redirect 到 `styles/index.md` |

## 维护与校验

**真源文件**：

| 资源 | 真源位置 | 用途 |
|------|---------|------|
| Step 4 schema | `scripts/planning_validator.py` | P4 planning Gate |
| Workflow 版本 | `scripts/workflow_versions.py` | 跨脚本版本号 |
| Skill 一致性 | `scripts/check_skill.py` | 文档/代码合同漂移检查 |

**自动检查入口**：修改 prompt / playbook / cheatsheet / Step 4 schema 示例后，运行：

```bash
python3 scripts/check_skill.py            # 文档与代码合同漂移检查
python3 scripts/planning_validator.py     # 策划稿 schema 校验
python3 scripts/contract_validator.py     # 各 phase 间 JSON 合同校验
python3 scripts/visual_qa.py              # 视觉 QA 双层断言（planning + html）
python3 scripts/smoke_test.py             # 我们简化版端到端冒烟测试
python3 scripts/smoke_skill.py            # sunbigfly 完整版冒烟测试
```
