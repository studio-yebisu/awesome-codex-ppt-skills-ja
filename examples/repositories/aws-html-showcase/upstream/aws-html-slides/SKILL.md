---
name: aws-html-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through pre-built visual previews rather than abstract choices.
---

# Frontend Slides

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

## Quick Start — How It Works

**When the user invokes this skill, present this workflow overview first:**

This skill helps you create browser-based HTML presentations with rich animations. There are two paths:

**Rich content blocks** (usable in any slide): images/video, data **charts**, comparison **tables**, and **diagrams** — flowcharts, sequence/UML/ER, network, mind maps, and architecture drawn as **native animated SVG** (zero dependencies, packets flowing along edges, optional isometric 3D); AWS architecture diagrams with official service icons via the drawio skill (needs the draw.io desktop CLI).

### Two Paths

| Path | Flow |
|------|------|
| **New Presentation** | Step 1 -> 2 -> 3 -> 4 -> 5 |
| **PPT Conversion** | Step 1 -> 2 -> 3 (extract + generate in one go) |

```
New Presentation:
  1. Setup (language+mode+editing+pages) -> 2. Topic -> 3. Style -> 4. Fill content.md -> 5. Generate HTML

PPT Conversion:
  1. Setup (language+mode) -> 2. PPT file path -> 3. Style + Extract + Generate (done)
```

### Output structure

```
my-presentation/
├── index.html        # The presentation (all CSS/JS inline, zero dependencies)
└── assets/           # All media files (auto-copied from your references)
    ├── screenshot.png
    └── demo.mp4
```

- Navigate with arrow keys, Space, scroll, or click the nav dots
- Click any image to enlarge, Esc to close
- Share by zipping the folder — recipient unzips and opens index.html

---

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Use pre-built visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character
- **Emoji as icons** — Never use emoji as card/feature icons. Use Lucide icons via CDN instead. See [html-template.md](html-template.md) "Icons: Lucide" section for setup and icon reference

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2) |
| Code slide | 1 heading + 8-10 lines of code |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |
| Chart slide | 1 heading + 1-2 charts (max 50vh) + optional 1-line caption |
| Table slide | 1 heading + 1 table (max 6 rows) |
| Diagram slide | 1 heading + 1 diagram (max 60vh) + optional 1-line caption |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Step 1: Setup

**Single AskUserQuestion — ask all setup questions at once with bilingual labels:**

**Question 1 — Language / 语言** (header: "Language"):
Language / 语言? Options:
- **English**
- **中文**

**Question 2 — Mode / 模式** (header: "Mode"):
What to do / 你想做什么? Options:
- **New Presentation / 新建演示** — Create from scratch / 从零开始创建
- **Convert PPT / 转换 PPT** — Convert .pptx to HTML / 将 .pptx 转为 HTML

**Question 3 — Editing / 编辑** (header: "Editing"):
Inline editing in browser / 浏览器内编辑? Options:
- **Yes / 是 (Recommended)** — Press E to edit, Esc to save / 按 E 编辑，Esc 保存
- **No / 否** — View only, smaller file / 仅展示，文件更小

**Question 4 — Pages / 页数** (header: "Pages"):
How many slides / 多少页? Options:
- **Short / 简短** (5-10)
- **Medium / 中等** (10-20)
- **Long / 详细** (20+)

After the user answers, use the selected language for **ALL** subsequent messages, AskUserQuestion labels, and option descriptions. Technical terms (e.g. PPT, HTML) remain in English.

---

**Disclaimer (always on):** Every presentation includes a fixed AWS disclaimer on every slide: `"© 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved."` — not optional.

**For PPT mode:** Page Count is ignored (determined by the PPT content). Editing choice still applies.

---

## Step 2: Topic / PPT Path

### New Presentation

Ask the user to type a brief topic in chat. This is used for project folder naming (e.g. "bedrock-agents", "s3-security").

### PPT Conversion

Ask the user to provide the .pptx file path.

---

## Step 3: Style Selection + Project Setup

### Style Selection (both paths)

Show the 2 available presets. Available presets are defined in [STYLE_PRESETS.md](STYLE_PRESETS.md).

| # | Preset | Vibe | Theme |
|---|--------|------|-------|
| 1 | Neon Cyber | Futuristic, techy, neon glow, 3D-ready | Specialty |
| 2 | re:Invent Keynote | Futuristic, keynote-stage, high-tech, 3D-ready | Specialty |

**Open the preview directory in Finder** so the user can browse and double-click any style to preview it. The preview files are bundled inside the skill directory at `preview/` (relative to the skill base directory).

```bash
open <skill-base-dir>/preview/
```

User picks a number (1-2) or says "Mix elements".

> **3D & motion effects (optional, experimental):** **Both specialty styles** can be enriched with self-contained, offline 3D/motion effects — CSS 3D heroes, hand-written WebGL shader backgrounds, and GSAP-orchestrated titles. Each technique ships in two palettes: re:Invent purple (`demos/`) and Neon Cyber cyan (`demos/neon/`). These are standalone demos + a reference, not part of the default flow — see [effects-reference.md](effects-reference.md) and the `demos/` directory. The lightweight CSS default (animated-blob cover for #2, particle/grid background for #1) remains the baseline.

### PPT Conversion — Extract + Generate (end of PPT path)

After style is chosen, do everything in one step:

1. **Create the project folder** with `assets/` directory
2. **Extract content** — Run `uv run --with python-pptx python scripts/extract-pptx.py <input.pptx> <output_dir>`
3. **Show the user** a summary of extracted slides (titles, content previews, image counts)
4. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)
5. **Open in browser** — Use `open <folder>/index.html`
6. **Summarize** — Output location, style name, slide count, navigation instructions

**PPT conversion is complete. Steps 4-5 are skipped.**

### New Presentation — Create Project Folder

After style is chosen, create the project folder and generate content.md **using the script** (not AI):

```bash
mkdir -p <topic>/assets
uv run python <skill-base-dir>/scripts/gen-content.py <page_count> <topic>/content.md --lang <language>
touch <topic>/index.html
```

Where `<page_count>` is the middle value of the chosen range (Short=8, Medium=15, Long=25). `<language>` is `en` or `zh` based on the Language choice in Step 1.

**Tell the user:** Fill in `<topic>/content.md` with your content, then come back. I'll review it before generating.

**Also mention the optional rich blocks** so the user knows what's available (the template header in content.md documents each in full):
- `### chart` — data charts (bar, line, pie, etc.)
- `### table` — comparison tables
- `### diagram` — flowcharts, sequence/UML/ER, network topology, mind maps, or architecture, drawn as **native animated SVG** right in the slide (no install needed; supports `animate: flow` request-packet animation and an isometric-3D architecture look). Only `type: aws` (official AWS service icons) uses the drawio skill and requires the draw.io desktop CLI (`brew install --cask drawio`); if it's missing I'll flag it at review and draw natively instead. See [diagram-reference.md](diagram-reference.md).

**IMPORTANT: Do NOT fill in or modify content.md on behalf of the user.** The content must come from the user. If the user asks you to draft content, confirm the topic and outline with them first via AskUserQuestion before writing anything. Never assume or auto-generate slide content without explicit user approval.

---

## Step 4: Content Review (New Presentation only)

Read the completed content.md and perform a review before proceeding:

1. **Parse all slides** — Extract headings, body text, and media references
2. **Validate media files** — Check that every referenced file exists (resolve relative paths from cwd, absolute paths as-is, pasted image paths as-is). Report any missing files.
3. **Check for issues** — Flag:
   - Empty slides (heading but no body or media)
   - Slides that exceed content density limits (too many bullets, etc.)
   - Inconsistent page numbering
   - Media files referenced but not found
   - Chart blocks: validate `type` is one of line/bar/doughnut/pie/radar/polarArea, labels count matches data count
   - Table blocks: validate markdown table syntax is well-formed
   - Diagram blocks: validate `type` (if present) is one of flowchart/sequence/class/er/network/mindmap/arch/aws, and the description is non-empty. Native types need no prerequisites. Only if the deck has a `type: aws` block: note that AWS icon rendering needs the draw.io desktop CLI (`drawio`) — flag once here if it's missing, and mention the fallbacks in [diagram-reference.md](diagram-reference.md)
4. **Present a summary table** to the user showing: slide number, title, content preview, media count, any warnings
5. **Ask for confirmation** via AskUserQuestion (header: "Review"):
   - "Looks good, proceed" — Continue to Step 5
   - "I need to fix some things" — User edits content.md, then re-run review

**Only proceed to generation after user confirms the content review.**

---

## Step 5: Generate HTML (New Presentation only)

Generate the full presentation using content from Step 4 and style from Step 3.

**Before generating, read these supporting files:**
- [html-template.md](html-template.md) — HTML architecture and JS features
- [viewport-base.css](viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference for the chosen feeling
- [chart-reference.md](chart-reference.md) — Chart.js patterns (only if content.md contains `### chart` blocks)
- [diagram-reference.md](diagram-reference.md) — native animated SVG diagram framework + drawio-for-AWS path (only if content.md contains `### diagram` blocks); working demos in `../demos/diagrams/`
- **Layout patterns file for the chosen style** (if available) — CSS classes + HTML templates for rich layouts. These are extracted from preview files and contain the actual implementation details. Read the matching file:
  - Style #1 Neon Cyber → [layout-neon.md](layout-neon.md)
  - Style #2 re:Invent Keynote → [layout-reinvent.md](layout-reinvent.md)
- **[effects-reference.md](effects-reference.md)** (optional, either specialty style) — only when the user wants richer 3D/motion. The catalog is palette-agnostic; use the matching token set and demo dir: style #1 Neon → `demos/neon/`, style #2 re:Invent → `demos/`.

**Layout rule: Never use plain left-aligned bullet lists.** Always use a layout pattern from the layout reference file (pill cards, feature grid, split divider, process flow, etc.). Match content type to the recommended layout in the "Layout Selection Guide" table.

**Key requirements:**
- Single self-contained HTML file, all CSS/JS inline
- Include the FULL contents of viewport-base.css in the `<style>` block
- Use fonts from Fontshare or Google Fonts — never system fonts
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block
- If inline editing was opted in at Step 1: include inline editing code (E to enter edit mode, Esc to save & exit)
- Always include `.slide-footer` with AWS disclaimer on every slide: `"© 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved."`
- Always include `.page-number` element — shows `current / total`, updated by JS. See [html-template.md](html-template.md) "Page Number" section

**Asset bundling (when images or videos are used):**
1. Copy all referenced images/videos into `[presentation-name]/assets/`
2. Place the HTML file at `[presentation-name]/index.html`
3. All `src` paths in HTML must be relative: `assets/image.png`, `assets/video.mp4`
4. The folder is self-contained — zip and share, everything works

If no images or videos are used, a single HTML file is sufficient — no folder needed.

**Lightbox:** When images are included, always include the click-to-enlarge lightbox. See [html-template.md](html-template.md) "Image Lightbox" section for implementation.

### Parallel Generation (8+ slides)

When generating presentations with **8 or more slides**, use parallel sub-agents for faster generation.

| Slides | Strategy |
|--------|----------|
| 1-7 | Single agent generates everything directly |
| 8+ | Framework agent + slide batch agents (1 agent per ~5 slides) in parallel |

**Strategy: split by slide batches, assemble at the end.**

1. **Create a `_parts/` directory** inside the presentation folder
2. **Launch sub-agents in parallel** (all `run_in_background: true`):
   - **Framework agent**: Reads style preset from [STYLE_PRESETS.md](STYLE_PRESETS.md) + `viewport-base.css` + `html-template.md` + `animation-patterns.md`, generates `_parts/00-head.html` (DOCTYPE through `<body>` with all CSS) and `_parts/99-foot.html` (particle canvas + lightbox + all JS + closing tags)
   - **Slide batch agents** (~5 slides each): Each generates a batch of `<section class="slide">` elements to `_parts/10-slides.html`, `_parts/20-slides.html`, etc.
3. **Provide each slide agent with**:
   - A compact CSS class reference (class names + HTML patterns to follow)
   - The exact content for their batch of slides
   - Instruction to write ONLY `<section>` elements — no `<head>`, `<style>`, or `<script>`
4. **After all agents complete**, concatenate: `cat _parts/*.html > index.html`
5. **Clean up**: delete the `_parts/` directory and all its contents — these are build artifacts and must not remain in the final output

**Examples:**
- 8 slides → 1 framework agent + 2 slide agents (slides 1-4, slides 5-8)
- 15 slides → 1 framework agent + 3 slide agents (1-5, 6-10, 11-15)
- 25 slides → 1 framework agent + 5 slide agents (1-5, 6-10, 11-15, 16-20, 21-25)

**Key rules for consistency across agents:**
- All agents must use the **same CSS class names** — define these clearly in each prompt
- Include HTML pattern examples (title slide, divider, grid, image, etc.) in each prompt
- File naming with numeric prefixes (`00-`, `10-`, `20-`...) ensures correct concatenation order
- **Diagram blocks**: prepare every diagram **before** launching slide batch agents. Native types: the lead designs the inline-SVG `<figure>` block (adapting `../demos/diagrams/` patterns) and hands it to the batch agent to inline verbatim — batch agents never invent diagram geometry. `type: aws`: export the PNG to `assets/` via the drawio skill first and hand over only the relative `assets/diagram-N.png` path. See [diagram-reference.md](diagram-reference.md).

### Delivery

After generation:

1. **Open** — Use `open [name]/index.html` (or `[name].html` if no assets) to launch in browser
2. **Summarize** — Tell the user:
   - Output folder location (or file location if no assets), style name, slide count
   - Navigation: Arrow keys, Space, scroll/swipe, click nav dots
   - If images included: Click any image to enlarge, Esc to close
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - If inline editing was enabled: Press E to enter edit mode, click any text to edit, Esc to save & exit
   - AWS disclaimer appears on every slide; edit `.slide-footer` in HTML to update if needed
   - **To share: zip the entire folder, recipient unzips and opens index.html**

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [STYLE_PRESETS.md](STYLE_PRESETS.md) | 2 curated visual presets with colors, fonts, and signature elements | Step 3 (style selection) |
| [viewport-base.css](viewport-base.css) | Mandatory responsive CSS — copy into every presentation | Step 5 (generation) |
| [html-template.md](html-template.md) | HTML structure, JS features, code quality standards | Step 5 (generation) |
| [animation-patterns.md](animation-patterns.md) | CSS/JS animation snippets and effect-to-feeling guide | Step 5 (generation) |
| [chart-reference.md](chart-reference.md) | Chart.js integration patterns, theme color palettes, parsing rules | Step 5 (when charts used) |
| [diagram-reference.md](diagram-reference.md) | Native animated SVG diagram framework (flowchart, sequence, ER, network, mindmap, arch incl. isometric 3D — demos in `../demos/diagrams/`) + drawio path for `type: aws` — parsing, choreography, theme-matching, fallbacks | Step 5 (when `### diagram` blocks used) |
| [layout-neon.md](layout-neon.md) | Neon Cyber layout patterns — HUD chrome, bento/spotlight/gauges/marquee/orbit + FX JS contract | Step 5 (style #1) |
| [layout-reinvent.md](layout-reinvent.md) | re:Invent Keynote layout patterns — CSS + HTML for all slide types incl. bento/spotlight/marquee + motion defaults | Step 5 (style #2) |
| [effects-reference.md](effects-reference.md) | 3D & motion effects catalog (CSS 3D, WebGL shaders, GSAP, View Transitions) — palette-agnostic; license red-lines, offline rules, demos in `../demos/` (purple) and `../demos/neon/` (cyan) | Optional (richer 3D/motion, either specialty style) |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction | Step 3 (PPT conversion) |
| [scripts/gen-content.py](scripts/gen-content.py) | Generate content.md template by page count (no AI needed) | Step 3 (project setup) |
| [preview/](preview/) | 2 pre-built style preview HTML files (bundled with skill) | Step 3 (style selection) |
