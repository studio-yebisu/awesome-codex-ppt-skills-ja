---
name: hand-drawn-chapter-slides
description: >
  Generate elegant chapter divider / section separator slides in PowerPoint (.pptx)
  featuring hand-drawn doodle-style illustrations with thick black outlines on muted
  colored backgrounds. ALWAYS use this skill when the user mentions any of:
  类手绘风格PPT, 手绘风格ppt, 手绘插画PPT, 涂鸦风格幻灯片, 手绘章节页, 分隔页,
  hand-drawn slides, doodle-style slides, sketch-style chapter pages, illustrated
  dividers, section separators, minimalist illustrated slides, chapter title cards,
  or any request combining "手绘/hand-drawn/doodle/sketch" with "PPT/slides/幻灯片/演示文稿".
  Also trigger when user wants slides with thick black line illustrations on colored
  backgrounds, pen-and-ink style slide art, whimsical chapter pages, or any request
  that references a similar style to what was previously generated. Even if the user
  simply says "再生成几页那种风格的PPT" or "make more slides like those", use this skill.
---

# Hand-Drawn Chapter Slides

Create sophisticated chapter divider slides with minimalist serif typography and
hand-drawn doodle-style illustrations. Each slide features a full-bleed muted color
background, a chapter label + large serif title in the lower-left, a page number in
the bottom-right, and a symbolic hand-drawn illustration in the center-right area.

## Design System

### Canvas Size
Standard widescreen: **13.333" x 7.5"** (12192000 x 6858000 EMU).
When using pptxgenjs, set a custom layout:
```js
pres.defineLayout({ name: "CUSTOM_16x9", width: 13.333, height: 7.5 });
```

### Color Palette
Use sophisticated, muted, desaturated colors. Never use bright or saturated tones.
Each slide gets a unique background color. Generate a cohesive palette before starting.

Example palette (15 colors):
`#D97756` Terracotta, `#788B5D` Sage Green, `#C46685` Mauve Rose,
`#9B8AC6` Lavender, `#6A9BCC` Sky Blue, `#BBD1C9` Mint, `#E2DACC` Warm Beige,
`#D4A0A0` Dusty Rose, `#7B9EB2` Steel Blue, `#C9A96E` Warm Ochre,
`#5D9B8F` Muted Teal, `#A88DB5` Soft Plum, `#8E9EAB` Slate Gray,
`#B8C4A0` Warm Sage, `#DEB89C` Soft Peach

Additional palette:
`#8B7D6B` Warm Brown-Grey, `#7A9E7E` Forest Sage, `#9B8EC4` Soft Purple,
`#C4866E` Clay, `#6B8FA3` Steel Blue, `#7EA388` Forest Green,
`#B07BAC` Muted Purple, `#C4956A` Warm Clay, `#9B9E78` Muted Olive

### Typography — EXACT specifications
| Element | Font | Size | Color | Position (inches) | Size (inches) |
|---------|------|------|-------|--------------------|----------------|
| Chapter label | Calibri | 14pt | #141413 | x=1.0, y=5.0 | w=4.0, h=0.3 |
| Chapter title | Georgia | 40pt | #141413 | x=1.0, y=5.3 | w=9.0, h=1.0 |
| Page number | Calibri | 14pt | #141413 | x=12.3, y=7.0 | w=0.5, h=0.25 |

Important: Chapter label uses **Calibri** (sans-serif), NOT Georgia.
Title uses **Georgia** (serif), regular weight (NOT bold).

### Illustration Style
All illustrations follow this exact aesthetic:
- **Stroke**: Thick black outlines, ~5-7px in SVG (stroke color `#141413`)
- **Fill**: Flat off-white `#FAF8F2` — NO gradients, NO shadows, NO textures
- **Curves**: Slightly irregular, organic (hand-drawn feel)
- **Content**: Symbolic, simplified, iconic — not realistic
- **Aesthetic**: Casual pen-and-ink doodle — like whiteboard sketches
- **Placement**: Center-right area of the slide (x≈5.0", y≈0.4", w≈8.0", h≈5.5")

NEVER use: pure black `#000000`, pure white `#FFFFFF`, shadows, gradients, 3D effects,
realistic illustrations, emoji, or Unicode symbols.

## Workflow

### Step 1: Gather Requirements
Ask the user for:
- Number of slides needed
- Chapter titles/topics for each slide
- Whether cover slides are needed (no chapter number, larger title)
- Starting page/chapter number (default: 1)

### Step 2: Generate Color Palette
Pick N muted colors from the palettes above or generate new ones. Ensure:
- No two adjacent slides have similar colors
- Mix warm and cool tones
- All colors are desaturated/muted

### Step 3: Choose Illustrations
For each chapter topic, pick a symbolic illustration. Read the illustration library
in `scripts/illustrations.md` for a catalog of ready-to-use SVG illustrations.

Common topic → illustration mappings:
- Fundamentals / Basics → Open book
- Planning / Design → Ruler
- Testing / Iteration → Ascending stairs
- Search / Discovery → Magnifying glass
- Communication / Feedback → Speech bubbles
- Cost / Finance → Coin stack
- Launch / Deployment → Rocket
- Collaboration / Team → Two people figures
- Security / Safety → Lock or shield
- Ideas / Creativity → Lightbulb
- Data / Analytics → Bar chart
- Connections / Network → Connected nodes
- Problem-solving → Puzzle piece
- Innovation → Gears
- Time / Context → Hourglass
- Navigation → Compass

### Step 4: Generate Slides with pptxgenjs

Install dependencies:
```bash
npm install pptxgenjs sharp  # in current working directory
```

Use this pattern for each slide:

```javascript
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

async function svgToBase64Png(svgString, width, height) {
  const pngBuffer = await sharp(Buffer.from(svgString))
    .resize(width, height, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

const pres = new pptxgen();
pres.defineLayout({ name: "CUSTOM_16x9", width: 13.333, height: 7.5 });
pres.layout = "CUSTOM_16x9";

// For each slide:
const slide = pres.addSlide();
slide.background = { color: "HEX_WITHOUT_HASH" };

// Illustration (SVG → PNG → base64)
const svgStr = buildSvg(topic); // see illustrations.md
const imgData = await svgToBase64Png(svgStr, 900, 750);
slide.addImage({ data: imgData, x: 5.0, y: 0.4, w: 8.0, h: 5.5 });

// Chapter label
slide.addText("Chapter N", {
  x: 1.0, y: 5.0, w: 4.0, h: 0.3,
  fontSize: 14, fontFace: "Calibri", color: "141413",
  bold: false, margin: 0, valign: "bottom"
});

// Title
slide.addText("Title text", {
  x: 1.0, y: 5.3, w: 9.0, h: 1.0,
  fontSize: 40, fontFace: "Georgia", color: "141413",
  bold: false, margin: 0, valign: "top"
});

// Page number
slide.addText("1", {
  x: 12.3, y: 7.0, w: 0.5, h: 0.25,
  fontSize: 14, fontFace: "Calibri", color: "141413",
  align: "right", margin: 0, valign: "bottom"
});
```

### Step 5: Cover Slide Variation (optional)
The first slide (cover) uses a different layout:
- Larger title (54pt+ Georgia) in the upper-left area
- No "Chapter N" label
- No full illustration — just a small decorative sparkle mark

### Step 6: QA
Convert to images and visually inspect:
```bash
python <pptx-skill-path>/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```
Check: text not cut off, illustration properly positioned, colors match, no overlaps.

## SVG Illustration Template

All illustrations share this structure — a 600x500 viewBox, off-white fill, thick
black strokes, organic curves:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <!-- Main shape with thick outline -->
  <path d="..." fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <!-- Interior detail lines -->
  <path d="..." fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

When creating new illustrations, follow these rules:
1. Use `Q` (quadratic) or `C` (cubic) Bezier curves for organic, hand-drawn feel
2. Avoid perfectly straight lines or geometric perfection
3. Keep it simple: 2-5 main shapes per illustration
4. Fill color is always `#FAF8F2`, stroke is always `#141413`
5. Main outlines: stroke-width 5-7; detail lines: stroke-width 2.5-3.5

See `scripts/illustrations.md` for the full illustration library with copy-paste SVGs.

## Quality Checklist
Before finishing, verify each slide:
- [ ] Background is full-bleed solid muted color
- [ ] Text color is `#141413` (not pure black)
- [ ] Illustration fill is `#FAF8F2` (not pure white)
- [ ] Chapter label is Calibri 14pt (NOT Georgia)
- [ ] Title is Georgia 40pt regular (NOT bold)
- [ ] Page number is Calibri 14pt right-aligned
- [ ] Canvas is 13.333" x 7.5"
- [ ] No overlap between text and illustration
- [ ] Page/chapter numbers are sequential and correct
