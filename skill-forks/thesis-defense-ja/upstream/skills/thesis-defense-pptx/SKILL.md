---
name: thesis-defense-pptx
description: Create, polish, and quality-check editable undergraduate or graduate thesis defense PowerPoint decks from a local thesis PDF/LaTeX project and an existing PPTX template. Use when the user asks for a formal defense PPT, thesis presentation, academic答辩PPT, template-matched PPTX, or local PowerPoint deck generation with visual inspection.
---

# Thesis Defense PPTX

Use this skill for local, editable `.pptx` thesis defense decks that must follow a supplied university/lab/company PowerPoint template.

## Operating Principles

- Platform: Windows + Microsoft PowerPoint for COM-driven cloning, export, and overflow inspection. On macOS/Linux, use the python-pptx-only parts and skip COM-based quality gates.
- Treat the visual template as the source of truth. Preserve its cover, colors, fonts, navigation, card styles, logos, and slide proportions unless the user explicitly asks to redesign.
- Read the thesis source first: PDF, LaTeX, figures, old PPT, experiment scripts, tables, and captions. Do not generate from topic/title alone when source files exist.
- Build a source-asset inventory before placing images: extract `\includegraphics` entries and captions from the final TeX/PDF, then use only thesis-cited figures or images the user explicitly approves. Do not carry over pictures from a template, old progress deck, or draft figure folder merely because they look relevant.
- Prefer copying native template slides and replacing content over rebuilding from blank slides.
- Keep slides concise and presentation-oriented. Convert thesis prose into defense talking points.
- Preserve the template's font sizes and hierarchy by default. For projection readability, first shorten text, split dense slides, or use the template's larger existing layouts; only change font sizes locally when the template itself provides no readable fit.
- Always generate an editable `.pptx`, not only an outline, image deck, PDF, or HTML.
- Always run a visual quality gate before final response: export slide images, inspect a contact sheet plus key full-size slide screenshots, check text overflow, check stale template words/images, and verify the PPTX opens.

## Recommended Workflow

1. Identify inputs:
   - thesis project path or full thesis document
   - visual template PPTX
   - optional old defense/report PPTX
   - output directory and desired filename

2. Extract thesis context:
   - Use `scripts/extract_thesis_context.py` to summarize PDF/TeX text and list candidate figures.
   - Read source files directly when details matter: abstract, introduction, method, experiments, results, conclusion.
   - Create an explicit list of final-thesis figures from `\includegraphics` and captions. Treat this as the allow-list for PPT images unless the user requests new visuals.
   - Collect defense-critical facts: problem, motivation, modeling, algorithms, experimental setup, baselines, metrics, key results, limitations, future work.

3. Analyze the template:
   - Export template slides to PNG if PowerPoint is available.
   - Inspect cover, TOC, navigation, section, body/card, chart/image, summary, and closing slide styles.
   - Note fonts, font sizes, red/brand color, card dimensions, line widths, and spacing.

4. Build a native template skeleton:
   - Use PowerPoint COM (`scripts/clone_template_deck.ps1`) when PowerPoint is installed.
   - Copy or duplicate original template slides in the needed order.
   - Use python-pptx only to replace content and add images/shapes after the skeleton is valid.

5. Fill content:
   - Use 12-16 slides for undergraduate defense unless user specifies otherwise.
   - Typical order: cover, TOC, background, problem definition, work summary, system/method, modeling, implementation, experiment setup, training/results, comparison, robustness/multi-seed, innovation/limitations, summary/outlook, thanks.
   - Use final-thesis figures first and verify each inserted picture against the source-asset inventory. If a picture is from a template or old deck and is not thesis-cited, replace it or remove it.
   - Keep dense tables limited to headline metrics; move detailed prose into verbal notes or omit. Prefer one message per slide, large existing template placeholders, metric cards, and short bullets over shrinking text or adding small multi-column tables.
   - Match the template's typography before changing sizes: preserve title/body/table/navigation sizing where possible, and use content reduction or slide splitting before manual font scaling.

6. Quality gate:
   - Export final PPTX to PNG with `scripts/export_pptx_png.ps1`.
   - Create a contact sheet with `scripts/make_contact_sheet.py`.
   - Run `scripts/inspect_pptx_overflow.ps1`.
   - Run `scripts/scan_pptx_text.py` for slide count and stale template terms.
   - Inspect the contact sheet manually, then open any risky slide full-size. COM overflow is not sufficient: also check visible clipping, text crossing card borders, small text caused by overfilling, stale template images, image aspect ratios, and text/card overlap.
   - Check stale template text, placeholders, wrong names/dates, wrong navigation labels, red active-nav white text, and non-thesis images accidentally inherited from the template or old progress deck.
   - Fix and repeat until the exported deck is clean.

7. Final response:
   - Give the full output path, total slide count, main changes, validation performed, and any unresolved manual confirmations.

## Script Usage

Extract thesis context:

```powershell
python scripts/extract_thesis_context.py --input "D:\path\to\thesis" --output "D:\path\to\thesis_context.md"
```

Clone template slides into a native skeleton:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/clone_template_deck.ps1 `
  -Template "D:\path\template.pptx" `
  -Output "D:\path\output.pptx" `
  -SlideSequence "1,2,3,4,4,6,7,8,9,10,11,12,13,14,15"
```

In this example slide 4 is deliberately reused as a sub-section page and slide 5 is skipped.

Export final deck:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/export_pptx_png.ps1 `
  -Pptx "D:\path\output.pptx" `
  -OutDir "D:\path\visual_check" `
  -Width 1600 -Height 900
```

Inspect possible overflow:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/inspect_pptx_overflow.ps1 `
  -Pptx "D:\path\output.pptx" `
  -Tolerance 40 `
  -OutputJson "D:\path\overflow.json"
```

Make a contact sheet:

```powershell
python scripts/make_contact_sheet.py --input "D:\path\visual_check" --output "D:\path\contact_sheet.png"
```

Scan deck text and forbidden terms:

```powershell
python scripts/scan_pptx_text.py `
  --pptx "D:\path\output.pptx" `
  --bad "中期检查,项目简介,系统框图,算法设计,成果展示,总结分析,TODO,占位"
```

For quality criteria, read `references/pptx_quality_gate.md`.

## Iteration Tips

The fastest way to fail a content fill is guessing strings instead of reading them. Use this loop:

1. **Dump first.** Run `scripts/dump_pptx_content.py --pptx <skeleton> --output dump.md` to list every shape's exact text, plus all table cells and picture names. Open `dump.md` and copy the strings you intend to replace.
2. **Prefer partial match for body text.** Use `replace_partial_text(slide, {"keyword": "new full text"})` instead of `replace_exact_text` whenever the body sentence might differ from the template by a stray space, half/full-width quote, or `——` vs `—`. Pass `min_len=20` to avoid short-key collisions with navigation tags.
3. **Keep `replace_exact_text` for short tags.** Navigation labels and section titles ("项目简介", "工作总结") are stable; exact match is safer because it cannot accidentally rewrite a body paragraph that happens to contain the same word.
4. **Use the table/picture helpers.** `write_table(table, rows)` preserves cell font/color/size, and `replace_picture(slide, old_pic, new_path)` swaps an image while keeping position and size — both avoid the boilerplate of removing and re-creating shapes.
5. **Re-run overflow + scan after every fill pass.** Overflow caused by longer content is the single most common bug; fix by shortening copy first, then by manual `\n` line breaks, and only resize the textbox if the template visual really allows it.
6. **Encoding.** All Python scripts shipped here force `stdout` to UTF-8, and the PowerShell scripts force the console output codepage to UTF-8, so cp936/gbk consoles do not corrupt JSON output containing CJK paths or Unicode symbols (`−`, `Δ`, `✓`).

## Script Usage

Dump every slide's shapes/text/tables/pictures (run this BEFORE constructing replacement dicts):

```powershell
python scripts/dump_pptx_content.py --pptx "D:\path\skeleton.pptx" --output "D:\path\dump.md"
```

Add `--slide 4,8,9` to limit to specific slides while iterating.

## Implementation Notes

- Requires Python 3.10+ and the packages in `requirements.txt`.
- On Windows with Microsoft PowerPoint installed, PowerPoint COM is the most reliable way to duplicate template slides and inspect real rendering.
- `python-pptx` is good for editable text, shapes, images, tables, and simple charts, but it does not perfectly model every PowerPoint layout/rendering behavior.
- `scripts/pptx_template_tools.py` uses `THESIS_PPTX_BRAND_RED` when set (`#830604`, `830604`, or `131,6,4`) so new school templates do not require source edits for the primary red.
- When a PowerPoint add-in blocks COM automation, disable only the broken add-in autoload if necessary and report that action.
- Use backups before overwriting a deck.
- Never revert unrelated user files while iterating.
