# Formula Rendering Pipeline

## Overview

Two rendering pipelines for LaTeX formulas in PowerPoint:

1. **OMML (default)** — native PowerPoint math via pandoc. Crisp at any zoom, font-consistent with slide text, supports subscripts/fractions/Greek letters. Used for display and inline formulas.
2. **Image (fallback)** — LaTeX → transparent PNG@600DPI or SVG. Used for paragraph-mode formulas (mixed text+math blocks) or when user explicitly requests image rendering.

The `render` field in `formulas.json` controls which pipeline to use (`"omml"`, `"image"`, or `"auto"`). Default is `"auto"` which routes paragraph→image, everything else→omml.

## Usage

### 1. Collect formulas into JSON

```json
[
  {
    "id": "formula-01",
    "latex": "H(X) = -\\sum_{x} p(x) \\log p(x)",
    "mode": "display",
    "fg_color": "1A1A2E",
    "scale": 1.0
  }
]
```

Fields:
- `id`: unique identifier, used as filename stem
- `latex`: raw LaTeX (double-escape backslashes in JSON)
- `mode`: `"display"` (uses `\[...\]`), `"inline"` (uses `$...$`), or `"paragraph"` (raw LaTeX — for mixed text+math blocks using `\begin{minipage}`, `\text{}`, etc.)
- `render`: `"omml"` | `"image"` | `"auto"` (default `"auto"` — paragraph→image, else→omml)
- `fg_color`: 6-char hex foreground color (no #), match to slide background (image pipeline only)
- `scale`: (reserved, not yet implemented)

### 2. Run renderer

```bash
python scripts/render_latex.py formulas.json formulas/              # PNG @ 600 DPI (default)
python scripts/render_latex.py formulas.json formulas/ --dpi 900    # PNG @ custom DPI
python scripts/render_latex.py formulas.json formulas/ --format svg # SVG (requires ghostscript)
```

CLI arguments:
- `formulas` (positional): path to formulas.json
- `outdir` (positional): output directory
- `--dpi N`: PNG resolution, default 600
- `--format png|svg`: output format, default `png`. SVG requires `ghostscript` (`brew install ghostscript`); auto-falls back to PNG if unavailable

### 3. Check manifest

OMML entry (no file generated — inject_omml.py handles conversion at post-processing):
```json
{
  "f01-entropy": { "render": "omml", "latex": "H(X) = -\\sum_{x} p(x) \\log p(x)" }
}
```

PNG output:
```json
{
  "p01-paragraph": {
    "file": "formulas/p01-paragraph.png",
    "format": "png",
    "width_px": 1467,
    "height_px": 109,
    "dpi": 600
  }
}
```

SVG output:
```json
{
  "formula-01": {
    "file": "formulas/formula-01.svg",
    "format": "svg",
    "width_pt": 183.4,
    "height_pt": 13.7
  }
}
```

Entries with `"error"` must be fixed (correct the LaTeX) or replaced with plain text.

### 4. Embed in PptxGenJS script

The `addFormula()` helper in `references/themes.md` script template auto-routes OMML vs image:

- **OMML formulas**: writes `{{MATH:id}}` placeholder text → `inject_omml.py` replaces with native math post-generation
- **Image formulas**: embeds PNG/SVG directly as before

```javascript
// Already defined in script template — auto-routes based on manifest[id].render
addFormula(slide, id, y, targetH);       // centered
addFormulaAt(slide, id, x, y, maxW, h);  // left-aligned
addCardFormula(sl, x, y, w, h, color, title, formulaId, fH);  // card with formula body
```

### 5. OMML post-processing (for OMML formulas)

After `node generate_slides.js`, run:

```bash
python ~/.claude/skills/powerpoint-slides/scripts/inject_omml.py output.pptx formulas.json output.pptx
```

This replaces all `{{MATH:id}}` placeholders with native PowerPoint OMML math. Skip if no OMML entries in manifest.

## SVG Notes

- SVG requires `dvisvgm` (bundled with TeX Live) and `ghostscript` (`dvisvgm --pdf` dependency)
- Install: `brew install ghostscript`
- SVG produces infinitely scalable formulas — no pixelation at any zoom level
- SVG works in modern PowerPoint (Microsoft 365); older versions may not render correctly
- If ghostscript is not available, the renderer automatically falls back to PNG

## Semantic Colors in Formulas

Available in LaTeX: `\textcolor{positive}{...}`, `\textcolor{negative}{...}`,
`\textcolor{emphasis}{...}`, `\textcolor{neutral}{...}`

## Multi-Background Themes (Sandwich)

For themes with both light and dark slide backgrounds, render each formula twice:
- `{"id": "f01-light", "fg_color": "2D3436", ...}` — for light backgrounds
- `{"id": "f01-dark", "fg_color": "FFFFFF", ...}` — for dark backgrounds

## Math-Heavy Paragraphs (Paragraph Mode)

For card bodies that mix text and inline formulas, render the entire paragraph as one LaTeX image using `"mode": "paragraph"`. In paragraph mode, the LaTeX is passed directly to the `standalone` document class without wrapping in `$...$` or `\[...\]` — you control the structure yourself.

**Simple example** (single line with inline math):
```json
{"id": "para-01", "latex": "Let $f(x) = \\sum a_i x^i$ be a polynomial of degree $n$.", "mode": "paragraph", "fg_color": "1A1A2E"}
```

**Multi-line card body** (use `\begin{minipage}` for width control):
```json
{
  "id": "p06-greedy", "mode": "paragraph", "fg_color": "4A4A5A",
  "latex": "\\begin{minipage}{8cm}\\raggedright\\small\\color{fgcolor} $\\Delta_i = l_y - l_i$\\quad\\text{for all }$i \\in [N]$\\\\[8pt] \\text{Constraints:}\\\\[3pt] \\quad$\\Delta_y = 0$\\\\[3pt] \\quad$\\Delta_i \\in [0,\\,2B)\\;\\;\\forall\\,i$\\\\[8pt] \\text{Range checks via Shout lookup.} \\end{minipage}"
}
```

Key points:
- Use `\\color{fgcolor}` to inherit the foreground color defined by `fg_color`
- `\\small` or `\\footnotesize` controls text size within the minipage
- `\\raggedright` prevents ugly justified spacing in narrow columns
- Minipage width should match the card body width (typically 8-9cm)
- Embed in slides via `addCardFormula()` or `addFormulaAt()` instead of `addText()`

## OMML Pipeline Details

### How OMML works

1. `render_latex.py` marks formulas with `render:"omml"` in manifest (no image generated)
2. PptxGenJS script writes `{{MATH:id}}` placeholder text via `addMathText()` helper
3. `inject_omml.py` post-processes the .pptx:
   - Reads `formulas.json`, filters to `render:"omml"` entries
   - Converts LaTeX → OMML via `pandoc` (LaTeX → .docx → extract `m:oMathPara` XML)
   - Finds `{{MATH:id}}` placeholders in slide XML (handles PptxGenJS run-splitting)
   - Replaces with native `<a14:m>` OMML elements
   - Ensures `mc:` and `a14:` namespace declarations

### Limitations

- **Paragraph mode not supported** — OMML cannot render mixed text+math blocks with minipage/raggedright. Use image pipeline (`render:"image"`) for paragraph mode.
- **LibreOffice cannot render OMML** — displays blank. Visual QA via soffice/PDF will show empty math regions. This is expected, not a bug. Use XML validation instead.
- **Requires pandoc** — `brew install pandoc`

### OMML vs Image comparison

| Feature | OMML (default) | Image (fallback) |
|---------|---------------|-----------------|
| Rendering | Native PowerPoint math | PNG@600DPI / SVG |
| Font consistency | Matches slide text | Standalone LaTeX fonts |
| Scaling | Infinite (vector) | DPI-dependent |
| Paragraph mode | Not supported | Supported |
| LibreOffice preview | Blank (known) | Renders correctly |
| Dependencies | pandoc | xelatex, pdfcrop, pdftoppm |
| Post-processing | inject_omml.py required | None |

## Error Recovery

If `render_latex.py` reports errors:
1. Check the LaTeX syntax
2. Fix in `formulas.json`
3. Re-run (only new/changed entries are re-rendered if output already exists)
4. Fallback: render as plain text in PptxGenJS
