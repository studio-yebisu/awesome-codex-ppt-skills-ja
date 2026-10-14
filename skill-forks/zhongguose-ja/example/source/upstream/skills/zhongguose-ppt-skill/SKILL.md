---
name: zhongguose-ppt-skill
description: |-
  以原稿章法为骨架，中国传统色彩为气韵，构建可交互、可迁移的中式汇报体系。
  **制作规范**
  将确认的文稿、大纲或文案梳理为忠于原文的汇报逻辑、章节与页面层级；采用单一中国色、中文主导的中英双语、左上框架导航与章节扉页；HTML 配套交互翻页，PPT 转译为版式规范。
  **触发规则**
  当演示或汇报任务需要梳理叙事逻辑、章节框架、页级结构或版式，并满足至少一项时使用：内容涉及中国文化；希望采用中国色 / 中国风 / 中式（东方）审美。点名本 Skill、模板或框架导航格式时也触发。适用于 HTML 与 PPT/PPTX，PPT 模式无需先接受 HTML 输出。
  **输出产物**
  HTML：`index.html` + `assets/`；PPT：汇报逻辑、章节、导航、页级架构与版式参考。

  Build an interactive Chinese-style system for HTML or PPT guidance.
  **Standards**
  Map confirmed sources into faithful logic and slides; use one Chinese color, Chinese-led bilingual type, top-left navigation, and dividers; add paging for HTML and layout specs for PPT.
  **Trigger**
  Use for presentations needing logic, sections, slide architecture, or layout when content concerns Chinese culture or visuals use Chinese/Eastern style. Also use when this Skill/template or framework navigation is named. Applies to HTML and PPT/PPTX; PPT need not produce HTML.
  **Outputs**
  HTML: `index.html` + `assets/`; PPT: logic, slide architecture, navigation, and layout reference.
---

# Zhongguose Presentation Skill / 中国色汇报演示 Skill

## Credits / 署名

- 本 skill 由【木渡川】制作。/ This skill is created by 木渡川 (Muduchuan).
- 本 skill 的产品思路与交互概念参考了归藏（guizang）的 `guizang-ppt-skill`（<https://github.com/op7418/guizang-ppt-skill>）。
- This skill's product and interaction concepts were inspired by guizang's `guizang-ppt-skill` (<https://github.com/op7418/guizang-ppt-skill>).
- 中国色视觉系统、框架导航、文稿锁定工作流与种子模板内容为【木渡川】制作。/ The zhongguose visual system, framework navigation, manuscript-locking workflow, and seed template content are by 木渡川.
- 封面字体源自令東（Lingdong Huang）的 `qiji-font`（齊伋體，<https://github.com/LingDong-/qiji-font>），以 SIL OFL 1.1 授权；本 skill 生成改名后的 `Zhongguose Cover` WOFF2 子集，并随成稿分发许可证。/ The cover font derives from Lingdong Huang's `qiji-font` (齊伋體, <https://github.com/LingDong-/qiji-font>) under SIL OFL 1.1; this skill generates a renamed `Zhongguose Cover` WOFF2 subset and ships the license with each deck.
- 运行时本 skill 不调用其他 skill；所引用的 `references/` 文档与 `scripts/` 脚本均为本 skill 自带内容。/ At runtime this skill invokes no other skill; all bundled `references/` and `scripts/` belong to this skill.

## Overview / 概览

Build a 中国色 presentation system in two modes: a self-contained interactive HTML deck, or reporting logic, slide architecture, and layout reference for PPT production. Both modes share one Chinese-traditional theme color, Chinese cultural atmosphere, restrained grid discipline, Chinese-led bilingual hierarchy, and a logic-first narrative arc.

构建一套中国色汇报演示体系，支持两种模式：交付自包含的交互式 HTML 演示，或为 PPT 制作提供汇报逻辑、页级架构与版式参考。两种模式都采用单一中国传统色、中式文化气质、克制的网格秩序、中文主导的中英双语层级，以及逻辑优先的叙事结构。

### Routing Boundary / 触发边界

Use this routing formula: presentation or reporting structure work AND (Chinese-cultural content OR Chinese-style visual intent). Naming this Skill, its template, or its framework-navigation format is an explicit override.

使用以下路由公式：演示或汇报结构任务 AND（中华文化内容 OR 中式视觉诉求）。用户点名本 Skill、对应模板或框架导航格式时，视为明确调用。

Chinese-language copy or a China-market topic alone does not satisfy the cultural/style condition. Do not trigger for generic deck conversion with no Chinese-cultural or Chinese-style requirement, or for non-presentation work such as logos and posters.

仅使用中文或仅涉及中国市场，并不等于具备中华文化或中式风格条件。没有相关文化/审美诉求的通用 PPT 转换，以及 logo、海报等非演示类任务，均不触发。

The first responsibility is not visual styling. It is to preserve the user's source logic. When a Markdown script is provided, first confirm whether the manuscript is final and what polishing level is allowed; only then treat the confirmed manuscript as the content contract.

第一责任不是做视觉，而是保留用户文档里的逻辑。只要用户提供了 Markdown 演讲稿或大纲，必须先确认文稿是否定稿、是否需要润色、允许多大幅度润色；确认后再把定稿文稿当成内容契约。

Default to a Chinese-led bilingual deck unless the user explicitly requests a monolingual version. Chinese carries the full message and strongest visual weight; English is a concise semantic translation in a smaller supporting tier, never a same-size competing headline.

除非用户明确要求单语版本，否则默认生成“中文主导的中英双语” deck：中文承载完整信息并占据最强视觉层级；英文只做简洁、准确的语义翻译，以更小字号辅助，不与中文等大并列争夺焦点。

This skill supports two delivery modes. In HTML mode, it outputs `index.html` plus an `assets/` directory. In PPT mode, it provides the reporting logic, section framework, navigation labels, slide architecture, and layout/design reference for the presentation-production workflow. It does not itself create or edit `.pptx` files.

本 skill 支持两种交付模式：HTML 模式输出 `index.html` 和 `assets/` 文件夹；PPT 模式为后续演示文稿制作提供汇报逻辑、章节框架、导航标签、页级架构与版式设计参考。本 skill 本身不直接创建或编辑 `.pptx` 文件。

## HTML-mode Prerequisites / HTML 模式前置条件

The following runtime dependencies apply only to HTML delivery. PPT framework and layout-reference mode has no Node.js, Python, or font-generation prerequisite.

以下运行依赖只适用于 HTML 交付。PPT 框架与版式参考模式不要求 Node.js、Python 或字体生成环境。

- Node.js 16+ is required for the `.mjs` outline and validation scripts.
- 运行 `.mjs` 大纲抽取与校验脚本需要 Node.js 16+。
- Python 3.10+ with FontTools and Brotli is required to rebuild the deck-specific cover font: `python -m pip install "fonttools[woff]"`.
- 逐稿重建封面字体需要 Python 3.10+、FontTools 与 Brotli：`python -m pip install "fonttools[woff]"`。
- If Node.js is unavailable, verify manually against `references/quality-checklist.md`; the Python font step is still required for a final deck whose HTML differs from the seed template.
- 如果环境没有 Node.js，改用 `references/quality-checklist.md` 手动检查；只要正式 deck 的 HTML 与种子模板不同，仍必须执行 Python 字体步骤。

## Workflow / 工作流

Choose the delivery mode before starting:

开始前先确定交付模式：

- HTML delivery / HTML 交付：follow the complete workflow below and deliver a self-contained interactive deck. / 执行下方完整工作流，交付自包含的交互演示。
- PPT framework and layout reference / PPT 框架与版式参考：run steps 0–3 and 6–7, then deliver the source-logic map, section framework, navigation labels, slide architecture, and layout/visual specification. Skip HTML-only steps 4–5 and 8–11 unless an HTML prototype is also requested. If an actual `.pptx` is required, pass this contract to the appropriate presentation-production workflow or tool. / 执行第 0–3、6–7 步，交付源逻辑地图、章节框架、导航标签、页级架构与版式视觉规范；除非同时需要 HTML 原型，否则跳过仅适用于 HTML 的第 4–5、8–11 步。若需要实际 `.pptx` 文件，再将这份结构合同交给相应的 PPT 制作流程或工具落地。

0. Confirm theme color, manuscript status, and polishing scope.
   先确认主题色、文稿状态与润色尺度。
   Before visual-design work begins in either mode, ask which theme color to use, listing the options from the theme-color table in `references/visual-system.md` (name + hex); default to 飞泉绿 if the user has no preference. When asking, open `assets/theme-cover-gallery.html` (under this skill's folder) in the browser so the user can compare cover samples before choosing. Set `--accent` and `--accent-on` as a pair per that table. In a PPT logic-only request, do not block source mapping or slide architecture on theme selection; open the gallery when the user asks to proceed into layout or visual direction.
   两种模式只要进入视觉设计阶段，就要询问用户选哪种主题色，并把 `references/visual-system.md` 主题色表的可选项（名称 + 色值）列出；询问时同时在浏览器打开本 skill 目录下的 `assets/theme-cover-gallery.html`，让用户对照封面示例再选。用户无偏好时默认飞泉绿，并按表成对设置 `--accent` 与 `--accent-on`。若 PPT 任务当前只需逻辑框架，不要让主题色选择阻塞源文档梳理或页级架构；待用户进入版式或视觉方向阶段时再打开色卡。

   If the user provides a Markdown speech script, also ask before any source mapping or layout work: Is this manuscript final? Does it need polishing? If yes, should the polishing be major revision, light polish, or near-verbatim preservation?
   只要用户提供 Markdown 演讲稿，还要在提炼框架或排版之前先问：这份文稿是否已经定稿？是否需要润色？如果需要，润色程度是大调、微调，还是基本保证当前文案内容？

   If the request already says the copy is final or must be preserved, or supplies fixed slide-by-slide content with no polishing request, treat the manuscript as confirmed in near-verbatim mode and do not ask the same question again. If the user explicitly defines the section grouping, use it directly; only a grouping derived by the skill requires user confirmation.
   如果请求已经说明文案定稿、必须原样保留，或直接给出固定的逐页内容且未要求润色，则视为已确认的“基本保证当前文案内容”模式，不要重复追问。用户若已明确版块分组，直接采用；只有 skill 自行提炼的分组才需要用户确认。

   Use these three polishing modes:
   使用以下三种润色模式：

   - Major revision / 大调：may restructure paragraph flow, strengthen transitions, and improve expression, while preserving facts, intent, and user-approved claims.
   - Major revision / 大调：可以重组段落顺序、强化转场、优化表达，但必须保留事实、意图和用户已确认观点。
   - Light polish / 微调：may improve wording, rhythm, emphasis, and redundancy, while preserving the existing structure and argument.
   - Light polish / 微调：可以优化措辞、节奏、重点和重复，但保留现有结构与论述。
   - Near-verbatim / 基本保证当前文案内容：only fix typos, punctuation, obvious grammar, and minimal readability issues; do not change meaning or structure.
   - Near-verbatim / 基本保证当前文案内容：只修正错别字、标点、明显语病和最低限度可读性问题，不改变含义与结构。

   After the user replies, polish and lock the manuscript first. Do not start slide architecture or layout design until the manuscript version is confirmed.
   得到用户回复后，先完成文稿润色并确认定稿版本。文稿未锁定前，不开始页级架构与版式设计。

1. Build the source logic map from the confirmed manuscript.
   先建立源文档逻辑地图。
   Load `references/content-architecture.md` whenever a Markdown script, speech draft, outline, or existing PPT text is provided. Extract top-level sections, subsections, key statements, and copy that must remain verbatim from the locked manuscript.
   当用户提供 Markdown、演讲稿、PPT 大纲或现有文案时，必须读取 `references/content-architecture.md`。基于已确认文稿提取一级版块、子版块、核心观点，以及必须原样保留的文案。

   If the manuscript has no top-level headings (for example a flat list of `###` cards), derive one or two candidate grouping schemes from evidence in the user's actual document: recurring subjects, argument flow, chronology, causal relationships, contrasts, or explicit stages. Do not default to a template taxonomy. For each candidate, show which source items it groups and why, recommend one, confirm it with the user, then treat the confirmed grouping as the top-level sections.
   如果文稿没有一级标题（例如只有平铺的 `###` 卡片），必须从用户实际文档中反复出现的对象、论述推进、时间顺序、因果关系、对照关系或明确阶段提炼一到两个候选分组，不得套用模板化分类。每个候选方案都要说明它归纳了哪些原文条目及分组依据，给出推荐项并与用户确认，再把确认后的分组作为一级版块。

2. Create a slide architecture contract.
   先做页级结构合同。
   For each slide, define: source heading, slide role, top-level section, active framework navigation label, key message, required Chinese copy, concise English support copy, visual hierarchy, and candidate layout.
   每一页都要先定义：对应源文档标题、页面角色、所属一级版块、当前高亮框架标签、核心信息、必须保留的中文文案、简洁英文辅助文案、视觉层级和候选版式。

3. Preserve wording and hierarchy.
   保留文案与层级。
   If copy is too long, split the slide, reduce secondary text, or ask for compression. Do not invent paraphrases just to fit a layout.
   如果文字太长，优先拆页、降低次级文字或请用户压缩，不要为了适配版式擅自改写。

   Preserve the approved Chinese wording as the content contract. Keep the deck bilingual as a whole, but keep Chinese headings, section-divider titles, card titles, and key statements Chinese-only. Place concise English in navigation, metadata, small labels, captions, or supporting body copy instead of adding a second English line beneath a Chinese title. English must preserve meaning, names, numbers, causality, and sequence and must not add a new claim.
   已确认的中文文案仍是内容契约。整份 deck 保持中英双语，但中文主标题、章节扉页标题、卡片标题和核心陈述保持纯中文；英文放在导航、元信息、小标签、图注或辅助正文中，不要在中文标题下另起一行英文。英文必须保留原意、名称、数字、因果与顺序，不得新增观点。

4. Start from `assets/template-zhongguose/`.
   从 `assets/template-zhongguose/` 模板开始。
   Copy the whole folder to the target PPT output directory and edit `index.html`. Keep `assets/motion.min.js`, `assets/lucide.min.js`, `assets/licenses/`, and `assets/fonts/` beside the HTML. The template carries only a small seed WOFF2 subset; the full source archive stays inside this skill and is never copied into a deck.
   将整个模板文件夹复制到目标输出目录并编辑 `index.html`。保留同级 `assets/motion.min.js`、`assets/lucide.min.js`、`assets/licenses/` 与 `assets/fonts/`。模板只携带小型种子 WOFF2 子集；完整源字体归档留在本 skill 内，不复制进成稿。

   The template is seeded with placeholder demo content. For a real deck, always replace:
   模板内置的是占位示例内容。制作正式 deck 时，必须替换：

   - The `<title>` (`中国色 PPT 模板 · 示例`).
   - `<title>`（`中国色 PPT 模板 · 示例`）。
   - Every piece of placeholder copy (all text containing `占位` and the sample framework labels 起/承/转/合).
   - 所有占位文案（含 `占位` 字样的文本，以及示例框架标签 起/承/转/合）。
   - The placeholder deploy link (`replace-with-your-url`) — set the real link or delete the element.
   - 占位部署链接（`replace-with-your-url`）——换成真实链接或删除该元素。
   - All `assets/placeholder-*.svg` images.
   - 所有 `assets/placeholder-*.svg` 占位图。

5. Replace slide content without breaking the shell.
   替换页面内容，但保留演示外壳。
   Preserve global CSS variables, framework navigation, slide scripts, `ascii-bg`, and animation helpers unless the user asks for a new visual system.
   除非用户要求换视觉系统，否则保留全局 CSS 变量、框架导航、翻页脚本、`ascii-bg` 和动效辅助逻辑。

6. Choose layouts after logic is stable.
   逻辑稳定后再选版式。
   Use `references/layout-patterns.md`; reuse the closest existing pattern before inventing a new one.
   参考 `references/layout-patterns.md`，优先复用已有版式模式。

7. Apply the visual system.
   应用视觉系统。
   Use `references/visual-system.md`; keep the chosen theme color (`--accent`, default 飞泉绿 `#497568`), title/body/English font roles, restrained labels, and clear hierarchy.
   参考 `references/visual-system.md`，保持所选主题色（`--accent`，默认飞泉绿 `#497568`）、中英文字体角色、克制标签和清晰层级。

8. Rebuild the deck-specific cover font after the HTML is final.
   HTML 定稿后重建逐稿封面字体。
   Run the bundled script after all slide copy and layout edits (`<skill_dir>` is the folder containing this SKILL.md). It extracts visible characters, generates `assets/fonts/zhongguose-cover.woff2`, copies the OFL license and font notice beside it, and records the HTML/font hashes in `zhongguose-cover.manifest.json`.
   所有页面文案与排版编辑完成后运行内置脚本（`<skill_dir>` 指本 SKILL.md 所在文件夹）。脚本会提取可见字符，生成 `assets/fonts/zhongguose-cover.woff2`，把 OFL 许可证与字体说明复制到同目录，并在 `zhongguose-cover.manifest.json` 中记录 HTML/font 哈希。
   The source font does not contain every Latin or punctuation glyph. Missing Latin and punctuation in `.cover-title` intentionally fall through to the next family in the CSS stack; the script blocks only missing Han characters so common punctuation such as `，` does not interrupt generation.
   源字体并不包含全部拉丁字母或标点；`.cover-title` 中缺失的拉丁字符与标点会按 CSS 字体栈回退到后续字体，脚本只阻断缺失的汉字，因此常用全角逗号 `，` 不会中断生成。

   ```bash
   python <skill_dir>/scripts/subset-cover-font.py path/to/index.html
   ```

   When rebuilding the bundled seed template, include the theme-cover gallery so all six cover names remain in the shared WOFF2 subset:
   重建本 Skill 自带的种子模板时，必须同时纳入主题色封面示例，确保六组封面名称都保留在共用 WOFF2 子集中：

   ```bash
   python <skill_dir>/scripts/subset-cover-font.py \
     <skill_dir>/assets/template-zhongguose/index.html \
     --include-html <skill_dir>/assets/theme-cover-gallery.html
   python <skill_dir>/scripts/check-cover-glyphs.py \
     <skill_dir>/assets/template-zhongguose/assets/fonts/zhongguose-cover.woff2 \
     --text 飞泉绿 --text 藕丝秋 --text 湘蓝 --text 绛缨 --text 鸦黄 --text 山岚
   ```

   Run it again after every subsequent HTML change. Do not copy the archived full source font into the final deck.
   此后只要 HTML 再发生变化，就重新运行。不要把归档的完整源字体复制进最终 deck。

9. Extract and compare the deck outline.
   抽取并对照 HTML 大纲。
   The scripts live in this skill's `scripts/` folder. Your working directory is usually the user's project, not this skill folder, so always call them with the skill directory's absolute path (`<skill_dir>` below is the folder containing this SKILL.md):
   脚本位于本 skill 的 `scripts/` 目录。实际工作目录通常是用户项目而不是 skill 目录，因此必须用 skill 目录的绝对路径调用（下文 `<skill_dir>` 指本 SKILL.md 所在文件夹）：

   ```bash
   node <skill_dir>/scripts/extract-deck-outline.mjs path/to/index.html
   ```

   Compare `activeSection`, page titles, labels, and major modules against the Markdown source map.
   将输出里的 `activeSection`、页标题、标签和模块，与 Markdown 源文档逻辑地图逐项对照。

10. Validate the deck.
   校验演示文稿。

   ```bash
   node <skill_dir>/scripts/validate-deck.mjs path/to/index.html
   ```

11. Do a browser visual pass.
    做浏览器视觉检查。
    Check 16:9 desktop first. Confirm no text overlaps, no unintended placeholders remain, and the active framework label matches the current slide.
    先检查 16:9 桌面视口，确认无文字重叠、无误留占位内容，并且左上角高亮标签与当前页面所属版块一致。
    Wait for `document.fonts.ready`, confirm `document.fonts.check('1em "Zhongguose Cover"')` returns true, and verify there is no local font 404 before judging typography.
    判断字体效果前，等待 `document.fonts.ready`，确认 `document.fonts.check('1em "Zhongguose Cover"')` 返回 true，并确认本地字体没有 404。

## Framework Navigation / 框架导航

Framework navigation is the top-left row of first-level section labels. It is a structural device, not decoration.

框架导航是页面左上角的一组一级版块标签。它是结构工具，不是装饰。

Purpose:

用途：

- Show the whole deck logic at a glance.
- 让观众一眼看到整份 PPT 的逻辑框架。
- Show where the current page sits inside that logic.
- 让当前页和全局结构的关系更直观。
- Keep divider pages and content pages connected by the same narrative spine.
- 让分隔扉页和内容页共享同一条叙事主线。

Rules:

规则：

- Generate labels from the Markdown top-level headings.
- 标签来自 Markdown 一级版块标题。
- If the source has no top-level headings, generate labels from the grouping scheme the user confirmed in the source-map step.
- 源文档没有一级标题时，标签改由源逻辑地图阶段与用户确认的分组方案生成。
- Preserve the heading order and numbering.
- 保留原文档的顺序和编号。
- Show the labels on every non-cover slide.
- 非封面页都要显示这组标签。
- Highlight exactly one current section.
- 每页只能高亮一个当前版块。
- Keep inactive labels visible but muted.
- 其他标签淡显，但必须保持可读。
- Do not use this row for slogans, subtitles, or decorative text.
- 不要把这一区域当作口号、副标题或装饰文字使用。

Example (labels always come from the actual source document):

示例（标签必须来自实际源文档）：

```html
<div class="section-tabs">
  <span class="tab active">01 WHY · 为什么做</span>
  <span class="tab">02 WHAT · 是什么</span>
  <span class="tab">03 HOW · 怎么做</span>
  <span class="tab">04 LESSONS · 经验沉淀</span>
</div>
```

Regenerate the labels for every new Markdown document. Do not reuse labels from a previous deck if the source outline is different.

每份新 Markdown 都要重新生成标签。源文档逻辑不同时，不要沿用旧 deck 的标签。

## Narrative Defaults / 默认叙事结构

Unless the source document implies a different order, a full deck usually follows:

除非源文档另有结构，完整 deck 通常遵循：

1. Cover / 封面：标题与一句话定位。
2. Section dividers / 版块分隔扉页：每个一级版块前一页。
3. Content pages / 内容页：按源文档子版块展开。
4. Roadmap or summary / 路线图或总结页（如源文档包含）。
5. Closing / 收尾页：呼应封面概念。

Narrative arcs such as WHY → WHAT → HOW → LESSONS or 起 → 承 → 转 → 合 are examples, not defaults. Use one only when the document's actual content supports that progression; otherwise name and order sections from the manuscript's recurring concepts and relationships.

WHY → WHAT → HOW → LESSONS、起 → 承 → 转 → 合 等只属于叙事弧示例，不是默认结构。只有用户文档的实际内容支持这种推进时才能采用；否则必须依据文稿中反复出现的概念及其关系命名并排序版块。

## Design Rules / 设计规则

In PPT reference mode, translate CSS-specific variables and classes below into equivalent theme-color tokens, typography hierarchy, and reusable page-component rules; do not require CSS code in the deliverable.

在 PPT 参考模式中，把下列 CSS 变量与 class 规则转换为等价的主题色 token、字体层级和可复用页面组件规范，交付物本身不要求包含 CSS 代码。

- Theme color: exactly one per deck, applied through the `--accent` CSS variable. Default is 飞泉绿 `#497568`; when the user chooses another theme color from `references/visual-system.md`, set `--accent` and its paired `--accent-on` from that table and everything follows. Light theme colors pair with ink `--accent-on` — also convert hardcoded white text on theme-color panels per the visual-system rules.
- 主题色：每份 deck 只用一种，通过 CSS 变量 `--accent` 应用。默认飞泉绿 `#497568`；用户从 `references/visual-system.md` 选择其他主题色时，按该表成对设置 `--accent` 与 `--accent-on`，全局跟随。浅色主题色配墨色 `--accent-on`——主题色面板上硬编码的白字也要按视觉系统规则同步换成墨色。
- Use paper white, theme-color panels, restrained line work, and `ascii-bg` where needed.
- 使用纸白、主题色面板、克制线条，以及必要时的 `ascii-bg` 动效纹理。
- Cover and closing display titles use the `.cover-title` stack (`Zhongguose Cover`, generated as a deck-specific local WOFF2 subset); other large Chinese titles use the `--zh-title` stack; body Chinese uses the Song/Ming-style stack; English and numbers use Orbitron.
- 封面与收尾大字使用 `.cover-title` 栈（逐稿生成的本地 WOFF2 子集 `Zhongguose Cover`）；其余中文大标题使用 `--zh-title` 栈；中文正文使用宋/明体风格字体栈；英文和数字使用 Orbitron。
- Keep bilingual hierarchy asymmetric: Chinese comes first and carries the largest size/weight. Retain only the English tiers supported by the source or the selected template pattern. English display titles are about 18–30% of the Chinese title size and must not exceed the seed template's 34px cap; supporting English is about 50–65% of the Chinese copy and remains visibly secondary.
- 中英层级必须不对称：中文在前并使用最大字号与字重。仅保留源文稿或所选原版模板模式支持的英文层级。英文标题约为中文标题字号的 18–30%，且不得超过种子模板的 34px 上限；辅助英文约为对应中文的 50–65%，始终保持次级。
- Use rectangular labels, hairlines, columns, timelines, and split panels.
- 优先使用矩形标签、细线、分栏、时间线和分割面板。
- Content-page category micro-labels use theme-color background with white text; body-paragraph key phrases get the theme color plus slightly bolder weight (about 1-3 per paragraph).
- 内容页小类目标签使用主题色底白字；正文重点词用主题色稍加粗强调（每段约 1-3 处）。
- Display-title text alignment follows the block's position: centered, left, or right.
- 大标题文字对齐跟随排版位置：居中、靠左或靠右。
- Do not add a lower-right “翻页” hint.
- 不要添加右下角“翻页”提示。
- If content does not fit, change the layout or split the page. Do not flatten the source outline.
- 如果内容放不下，调整版式或拆页，不要压扁源文档结构。
- One slide should have one visual priority.
- 每页只保留一个最明确的视觉重点。

## References / 参考文件

- `references/content-architecture.md`: source-document logic, wording preservation, framework navigation, and hierarchy checks.
- `references/content-architecture.md`：源文档逻辑、文案保真、框架导航和层级检查。
- `references/visual-system.md`: theme colors, typography, texture, motion, and navigation styling.
- `references/visual-system.md`：主题色、字体、纹理、动效和导航样式。
- `references/layout-patterns.md`: reusable page patterns and an example deck blueprint.
- `references/layout-patterns.md`：可复用页面版式和示例页面蓝图。
- `references/quality-checklist.md`: final checks before sharing or reusing the deck.
- `references/quality-checklist.md`：分享或复用前的最终检查清单。

## HTML Template Notes / HTML 模式模板说明

`assets/template-zhongguose/index.html` is a seed deck with placeholder demo content. It keeps one example of each core layout pattern and the full CSS/JS shell. All copy is placeholder text that must be replaced from the locked manuscript.

`assets/template-zhongguose/index.html` 是带占位示例内容的种子模板，保留了每种核心版式的一个示例页和完整的 CSS/JS 外壳。所有文案都是占位文本，必须按锁定文稿替换。

Interaction shell: vertical paging (wheel / arrow keys / Space / click / touch swipe), Esc opens the page-index overlay, B toggles static mode (all motion off). Keep these behaviors when editing slides.

交互外壳：纵向切页（滚轮 / 方向键 / 空格 / 点击 / 触摸滑动），Esc 打开页面索引，B 切换静帧模式（关闭全部动效）。编辑页面时保留这些行为。

Structure contract — the validation scripts parse the HTML with regular expressions and rely on these rules:

结构约定——校验脚本用正则解析 HTML，依赖以下规则：

- Each slide is a top-level `<section class="slide ...">`. Never nest another `<section>` inside a slide.
- 每一页是一个顶层 `<section class="slide ...">`，slide 内不要再嵌套 `<section>`。
- The cover slide carries `data-role="cover"`; framework-navigation checks skip slides with this marker. If no slide has it, the first slide is treated as the cover.
- 封面页带 `data-role="cover"` 标记；框架导航检查会跳过带此标记的页。若整份 deck 都没有该标记，则默认第一页为封面。
- `.section-tabs` contains only flat `<span class="tab">` children — no nested `<div>` inside it.
- `.section-tabs` 内只放并列的 `<span class="tab">`，不要嵌套 `<div>`。

Keep the final shared folder self-contained:

最终分享文件夹应保持自包含：

```text
target-ppt/
├── index.html
└── assets/
    ├── motion.min.js
    ├── lucide.min.js
    ├── licenses/
    │   ├── MOTION-MIT.txt
    │   └── LUCIDE-ISC-AND-FEATHER-MIT.txt
    ├── fonts/
    │   ├── zhongguose-cover.woff2
    │   ├── zhongguose-cover.manifest.json
    │   ├── FONT-NOTICE.txt
    │   └── OFL-1.1.txt
    └── ...
```

Network dependency note: motion and lucide load from local `assets/` first and only fall back to a CDN, so animations and icons work offline. The deck-specific `Zhongguose Cover` WOFF2 subset is local and works offline. Other web fonts (Orbitron, Noto Serif SC, LXGW WenKai, Inter, JetBrains Mono) still load from `fonts.googleapis.com`; without access to it the deck falls back to system fonts and the typography loses most of its character. Tell the user about this limitation if the deck must work fully offline or in a network that blocks Google Fonts.

联网依赖说明：motion 和 lucide 均优先加载本地 `assets/` 文件，仅在缺失时回退 CDN，离线也能保证动效和图标。逐稿生成的 `Zhongguose Cover` WOFF2 子集随 `assets/fonts/` 本地分发，同样离线可用。其余 Web 字体（Orbitron、Noto Serif SC、LXGW WenKai、Inter、JetBrains Mono）仍从 `fonts.googleapis.com` 加载；无法访问时会回退系统字体，版式不变但字体气质会明显打折。如果 deck 需要完全离线或在无法访问 Google Fonts 的网络中放映，需向用户说明这一限制。
