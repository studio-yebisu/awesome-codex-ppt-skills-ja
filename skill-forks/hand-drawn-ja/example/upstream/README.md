# Hand-Drawn Chapter Slides

A [Claude](https://claude.com/claude-code) Skill that generates elegant PowerPoint chapter
divider slides — muted full-bleed backgrounds, minimalist serif typography, and
doodle-style illustrations drawn with thick black ink strokes.

![Preview of five generated chapter slides](examples/preview.png)

## What it does

Ask Claude for "手绘风格的章节页 PPT" (or "hand-drawn chapter slides") and this skill
produces a `.pptx` where every slide follows one consistent design system:

- **Full-bleed muted background** — a unique desaturated color per slide, never bright or saturated
- **Lower-left title block** — `Chapter N` in Calibri 14pt above a Georgia 40pt title
- **Center-right illustration** — flat off-white (`#FAF8F2`) shapes with thick `#141413` outlines
- **Bottom-right page number** — Calibri 14pt, right aligned
- **13.333" × 7.5"** widescreen canvas

The skill ships an illustration library of **40 ready-to-use SVGs** (magnifying glass,
rocket, hourglass, compass, fingerprint, …) with topic mappings, plus the drawing rules
for improvising a new one when no existing illustration fits the chapter.

## Install

**Claude Code** — clone the skill folder into your personal skills directory:

```bash
git clone https://github.com/ABYR1206/claude-skill-hand-drawn-slides.git /tmp/hdcs && \
  cp -r /tmp/hdcs/hand-drawn-chapter-slides ~/.claude/skills/ && rm -rf /tmp/hdcs
```

**Claude Desktop / claude.ai** — package the folder as a `.skill` bundle and upload it in
the Skills panel:

```bash
cd claude-skill-hand-drawn-slides && zip -r hand-drawn-chapter-slides.skill hand-drawn-chapter-slides -x "*.DS_Store"
```

Then start a new session and ask for the slides — the skill triggers on hand-drawn /
doodle / sketch style slide requests in both English and Chinese.

## How it works

Slides are built with [`pptxgenjs`](https://github.com/gitbrent/PptxGenJS). Each
illustration is an SVG string rasterized to a PNG through [`sharp`](https://sharp.pixelplumbing.com/)
and embedded as base64 — so the illustrations stay crisp at any projection size and no
external image files are needed.

```bash
npm install pptxgenjs sharp
```

`SKILL.md` carries the full design system (exact fonts, sizes, positions, palettes) and
the generation workflow; `scripts/illustrations.md` is the copy-paste SVG catalog.

## Repository layout

```
hand-drawn-chapter-slides/
  SKILL.md                    # design system + workflow (the skill itself)
  scripts/illustrations.md    # 40-illustration SVG library
examples/
  demo-chapter-slides.pptx    # 5-slide sample deck
  preview.png                 # the image at the top of this README
  slides/                     # the same 5 slides rendered to PNG
```

---

## 中文说明

这是一个 Claude Skill，用来生成**手绘涂鸦风格的 PPT 章节分隔页**：低饱和度的满版背景色、
左下角衬线大标题、右侧粗黑线条的手绘插画、右下角页码。

触发方式：直接对 Claude 说「做几页手绘风格的章节页 PPT」「涂鸦风格幻灯片」
「hand-drawn chapter slides」，或者「再生成几页那种风格的」都会命中。

设计规范全部写死在 `SKILL.md` 里（画布 13.333"×7.5"、标签 Calibri 14pt、标题 Georgia 40pt
非加粗、文字色 `#141413`、插画填充 `#FAF8F2`），`scripts/illustrations.md` 收录了 40 个
可直接复制的 SVG 插画，并附带「章节主题 → 插画」的对应表；遇到库里没有的主题，文件末尾的
绘制规则会指导现画一个风格一致的新插画。

生成链路：`pptxgenjs` 建 PPT，插画走 SVG → `sharp` 转 PNG → base64 内嵌，不依赖外部图片文件。

安装方式见上方 **Install** 一节。

## License

MIT — see [LICENSE](LICENSE).
