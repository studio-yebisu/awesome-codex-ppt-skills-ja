# Case Study Postmortem: Industrial Fault Diagnosis Thesis PPT

## Source Project

Workspace: `D:\AI\Codex PPT1_6.3wsg`

Main files:

- `王舒戈-基于深度学习的工业过程故障诊断研究（定稿）.docx`
- `王舒戈-汇报PPT.pptx`
- `王舒戈-汇报PPT讲稿.md`
- `image_pages_v4/slide_01.png` through `slide_21.png`
- `outputs/ppt_correct_contact_sheet.png`
- `基于深度学习的工业过程故障诊断研究_图片版.pptx`

## Real User Intent

The desired output was a full image-based academic defense PPT:

- each slide is a complete generated image;
- the PPTX only wraps those images;
- the visual target is a polished blue academic defense style;
- the deck should follow the thesis content closely and preserve important charts/figures.

This differs from a normal editable PPT request. Editable shapes, native charts, and PowerPoint layout reconstruction are secondary unless explicitly requested.

## Event Chain

1. The paper was extracted into readable Chinese text and source figures/media.
2. Style thumbnails were produced and the blue academic defense style became the preferred direction.
3. A 21-page defense structure emerged: cover, contents, four section dividers, methods, experiments, summary, and thanks.
4. Full-page PNG slides were generated under `image_pages_v4`.
5. Several pages needed correction:
   - citation or footer text fixes on pages 4 and 14;
   - imagegen replacement or source-figure correction on page 6;
   - original confusion-matrix figure replacement on page 16;
   - ROC/source-image correction on page 17.
6. A 20-slide image PPTX was built from `image_pages_v4`, but the final defense structure also included `slide_21.png` for thanks.
7. The later `王舒戈-汇报PPT.pptx` has 21 slides and matches the full defense structure.

## Codex Deviations To Avoid

- Misread "PPT" as editable academic PPT instead of imagegen-created full-page slide images.
- Built a 20-slide package while the case-study final structure needs 21 pages including thanks.
- Wrote a generator with `Expected 20 slide images`, causing slide count drift.
- Treated file existence as success before checking Chinese readability and image-level text quality.
- Chart-like figures need source-faithful handling. Prefer imagegen redraw in the approved slide style, but preserve hard values, trends, axes, labels, legends, AUC/accuracy numbers, and class names exactly; use direct original preservation only when explicitly requested or when exact redraw quality is unsafe.
- Allowed multiple final candidates to diverge without clearly naming which one is canonical.

## Canonical Quality Target

Use `assets/case-study-contact-sheet.png` as the case-study quality target:

- 21 slides;
- deep blue academic palette;
- bilingual headings;
- clean scientific diagrams and chart pages;
- source-faithful metrics;
- final thanks page.

## Mandatory Lessons

- Page count is a first-class requirement, not an implementation detail.
- Chinese OCR/manual inspection is mandatory after imagegen.
- Exact metrics and labels must come from the paper, not inferred decoration.
- A "图片版 PPT" is image-first. The slide image is the source of truth.
