---
name: learn-deck
description: Generate editable learning PPTX decks by first creating HTML slides, or convert local HTML slide decks and single-page HTML presentations into editable PPTX files by rendering in a browser, reading DOM element positions, extracting inline SVG assets, and rebuilding text, shapes, gradients, bullets, and icons as separated PowerPoint objects. Use when a user asks to generate PPT/PPTX from a topic, outline, course material, study notes, or structured content, or asks for pixel-level/browser-positioned HTML-to-PPT/PPTX conversion with editable/separate elements instead of one full-slide screenshot.
---

# LearnDeck

## Quick Start

This skill has two main commands.

### 1. Generate PPT

Use this when the user asks to create a new PPT/PPTX from a topic, outline, notes, or source material.

1. Create a slide plan JSON using the shape in `examples/slides.example.json`.
2. Run:

```bash
node /path/to/learn-deck/scripts/generate_ppt.js \
  --slides /path/to/slides.json \
  --out-dir /path/to/output \
  --name deck-name \
  --style clean \
  --no-preview
```

This command first writes `<out-dir>/<name>.html`, then calls the HTML-to-PPT converter.

### 2. HTML to PPT

Use this when the user already has a local HTML file or URL:

```bash
node /path/to/learn-deck/scripts/html_to_ppt.js \
  --input /path/to/source.html \
  --out-dir /path/to/output \
  --name deck-name
```

If Codex workspace dependencies are available, prefer the bundled runtime:

```bash
NODE_PATH="$NODE_MODULES:/Users/$USER/node_modules" "$NODE_BIN" \
  /path/to/learn-deck/scripts/generate_ppt.js \
  --slides /path/to/slides.json \
  --out-dir /path/to/output \
  --name deck-name \
  --style clean \
  --no-preview
```

or:

```bash
NODE_PATH="$NODE_MODULES:/Users/$USER/node_modules" "$NODE_BIN" \
  /path/to/learn-deck/scripts/html_to_ppt.js \
  --input /path/to/source.html \
  --out-dir /path/to/output \
  --name deck-name
```

When running in Codex Desktop, call `load_workspace_dependencies` first and set:

- `NODE_BIN` to the returned Node.js executable.
- `NODE_MODULES` to the returned Node.js packages directory.

## Workflow

### Generate PPT

1. Ask one short style question when the user has not specified a style and the request is not urgent. Offer choices such as `clean`, `academic`, `warm`, `bold`, or `dark`; if the user says they do not care, choose based on audience and topic.
2. Turn the user's topic/content into a concise `slides.json` plan. Include `"style": "<chosen-style>"` in the plan or pass `--style`.
3. Keep each slide focused; split long content into more slides rather than crowding one slide.
4. Use `layout` values `cover`, `content`, `steps`, `compare`, or `summary` when useful.
5. Run `scripts/generate_ppt.js`; it writes HTML and then runs the converter. Use `--no-preview` by default for direct delivery.
6. Do not run extra validation by default. Directly report the generated `.html` and `.pptx` paths to the user/customer.

### Revision Loop

When the user/customer asks for adjustments after delivery:

1. Edit the original generated HTML file rather than starting over.
2. Run `scripts/html_to_ppt.js` on that same HTML file with the same `--name`/output directory.
3. Return the regenerated PPTX path. Only validate or preview when the user explicitly asks or a conversion error occurs.

### HTML to PPT

1. Load the HTML in Chromium/Chrome through Playwright.
2. Wait for network idle and `document.fonts.ready`.
3. Detect slides with `.slide` by default; pass `--slide-selector` for another selector.
4. Read every visible DOM element's bounding box, computed styles, text runs, pseudo bullets, and SVG children relative to its slide.
5. Save each inline SVG to `<output>/<base>-assets/svg/` and a PNG preview to `<output>/<base>-assets/png/`.
6. Create a PPTX with:
   - Editable text boxes for headings, paragraphs, spans, list items, and labels.
   - Editable rectangle/rounded-rectangle/ellipse shapes for backgrounds, pills, cards, borders, and bullets.
   - Separate image objects for extracted SVG icons, using PNG in the PPTX for compatibility while preserving source SVGs on disk.
   - Native OOXML linear gradients where possible.
7. Deliver the generated PPTX path directly. Do not run extra validation by default; validate only when explicitly requested or when troubleshooting a failed conversion.

## Script Options

```bash
node scripts/generate_ppt.js --help
node scripts/html_to_ppt.js --help-converter
```

Important HTML-to-PPT options:

- `--input <file-or-url>`: Required. Local HTML file or HTTP(S) URL.
- `--out-dir <dir>`: Required. Output directory.
- `--name <base>`: Output basename. Defaults to input filename.
- `--style <name>`: For `generate_ppt.js`, choose `clean`, `academic`, `warm`, `bold`, or `dark`.
- `--slide-selector <css>`: Defaults to `.slide`.
- `--chrome <path>`: Use a specific Chrome/Edge/Chromium executable.
- `--ppt-width <inches>` and `--ppt-height <inches>`: Defaults to 13.333 x 7.5.
- `--keep-raw`: Keep the intermediate unpatched PPTX.
- `--no-preview`: Skip LibreOffice PDF/PNG preview generation.

## Bundled Showcase Templates

LearnDeck includes two editable four-slide showcase templates:

- `templates/learn-deck-showcase-zh.pptx`
- `templates/learn-deck-showcase-en.pptx`

Use them as visual references when the user asks for the LearnDeck showcase style, or clone and revise them when a four-slide knowledge-to-PPT overview matches the request.

## Notes

- `generate_ppt.js` expects an agent-authored slide plan JSON; it is intentionally deterministic and does not call an LLM by itself.
- This skill prioritizes editable separated elements over screenshot-perfect fidelity.
- Browser coordinates are authoritative. Avoid hand-calculating flex/grid positions when the script can read them.
- PowerPoint and LibreOffice may lay out CJK fonts slightly differently from Chrome. Use installed system fonts such as `PingFang SC` or pass `--font-face`.
- Complex CSS effects are approximated: radial backgrounds become translucent ellipses, box shadows become approximate PowerPoint shadows, and CSS filters are ignored.
- If SVG support in PowerPoint is important, keep the saved SVG assets and replace the generated PNG icon objects manually or adapt the script. PptxGenJS needs PNG previews for SVG in Node, so PNG is the compatibility default.
