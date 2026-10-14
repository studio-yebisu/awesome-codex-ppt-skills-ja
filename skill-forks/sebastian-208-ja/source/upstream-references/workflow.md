# Academic Image PPT Workflow

## 1. Goal Alignment Dialogue

Start with a short, active dialogue. Do not begin extraction, blueprinting, thumbnail design, or image generation until the production direction is clear enough to summarize.

Collect or confirm:

- paper file: `.docx`, `.pdf`, or extracted text;
- use case: thesis defense, seminar, course report, research talk, proposal defense, or other;
- audience: teachers, teachers and classmates, committee, industry audience, or mixed;
- target slide count or defense/report duration; treat target slide count as a planning reference, not a strict limit;
- title, author, school, major, student ID, advisor, date, and required logos;
- paper type, such as empirical, normative/theoretical, policy, design/system, review, or mixed;
- preferred 4-6 part chapter structure, if the user has one;
- style reference thumbnail or permission to use bundled blue academic references;
- source figures, tables, formulas, and metrics that must be preserved;
- required closing-page audience wording;
- output format. Default is imagegen-generated full-page PNGs embedded into an image-only PPTX.

Ask concise follow-up questions for missing high-impact fields. Infer only minor fields from the paper, and record the assumption. Do not infer school identity, logo, target slide count, closing audience, or permission to simplify, omit, or change hard chart values when uncertain.

If the user gives duration but not slide count, propose a page budget and ask whether to adopt it before the `Alignment Summary`: maximum one slide per minute; typical academic budgets are 8-10 content slides for a 10-minute talk, 12-14 content slides for 15 minutes, 15-18 content slides for 20 minutes, and 30-40 content slides for a 45-minute seminar. Treat this suggested budget as a planning reference, not a strict cap. Then translate the approved content-slide budget into the full deck count by adding required structure pages such as cover, contents, section dividers, closing, and any user-requested appendix/reference pages.

## 2. Alignment Summary Gate

Create `qa/alignment-summary.md` and show the user a concise confirmation summary before continuing.

Include:

- confirmed input files and deliverables;
- use case, audience, target slide count/duration as a reference, and final output mode;
- metadata to display or omit;
- paper type and tentative chapter logic;
- style references and visual constraints;
- must-preserve figures, formulas, tables, metrics, and citations;
- standalone closing-page wording;
- assumptions and unresolved risks.

If the user corrects anything material, revise the summary and ask again. Do not proceed to paper extraction and blueprint production until the user confirms the `Alignment Summary`.

## 3. Paper Extraction And Academic Input Pack

Extract text and media from the paper. Confirm the extracted text is readable in Chinese before summarizing. If terminal output appears garbled, reopen with UTF-8 or inspect the file content another way before deciding the extraction failed.

Create an `Academic Input Pack`:

- title and metadata;
- abstract and keywords;
- chapter outline;
- paper type;
- research problem, research gap, research questions, and contributions;
- theories, models, methods, datasets, variables, and experimental setup;
- formulas, tables, figures, metrics, and named methods;
- conclusion, limitations, and outlook;
- figure inventory with redraw/preserve decisions needed; prefer imagegen redraw for charts and analytical figures while preserving source values, trends, axes, labels, legends, and metric numbers exactly;
- source locations for claims, figures, tables, and numbers.

## 4. Academic Narrative Spine

Before listing pages, write a compact narrative spine:

```text
Research context -> research gap -> research question -> method/design -> evidence/results -> contribution -> limitations/outlook -> correction-request closing
```

Most academic decks should be organized into 4-6 parts. Use the paper type and user preference to choose the structure; do not force every paper into the same outline.

By default, the `Deck Blueprint` must include section divider pages for the main academic parts. Omit or compress section dividers only when the user explicitly asks for a compact structure or a no-divider deck. Count section dividers as structure pages when translating a content-slide budget into the final deck count.

For empirical papers, a common 4-part structure is:

```text
01 研究背景与意义
02 研究内容与方法
03 实验设计与结果分析
04 总结与展望
```

For normative, theoretical, or policy-oriented papers, a common 5-part structure is:

```text
01 研究背景与意义
02 理论与文献综述
03 研究过程
04 策略优化
05 结论与展望
```

These are examples, not fixed templates. Adapt section names to the paper and ask the user to confirm when the best structure is ambiguous.

## 5. Deck Blueprint

Create a page-by-page `Deck Blueprint` before any thumbnail design. The blueprint is the production source of truth for style thumbnails, sample pages, final imagegen prompts, QA, and PPTX packaging.

Include section divider pages by default between major parts unless the user explicitly requested otherwise. Do not silently remove section divider pages only to hit a shorter page count; ask whether to prioritize compactness or full academic structure if the count is tight.

Use the target slide count from goal alignment as a reference when shaping the blueprint, but do not treat it as an exact count or hard upper bound. The final slide count should follow the paper's narrative structure, required source figures, section divider pages, and explanation needs, then be confirmed through blueprint approval.

For a thesis defense, use this rhythm unless the user gives a different structure:

1. cover
2. contents
3. section divider: background
4-6. background, research gap, contributions
7. section divider: methods
8-12. preprocessing, architecture, modules, online diagnosis
13. section divider: experiments
14-18. dataset, training, confusion matrix, ROC, model comparison
19. section divider: summary
20. summary and outlook
21. standalone closing / Q&A

Always reserve the final slide as a standalone closing page. Do not combine it with the summary, conclusion, outlook, or any content page. Avoid "感谢聆听". Use one of these defaults unless the user supplies their own:

- `恳请各位老师同学批评指正`
- `恳请各位老师批评指正`

Each blueprint entry must include:

- slide number;
- page type;
- section;
- Chinese title and optional English subtitle;
- governing message: the one claim or communicative purpose this page must deliver;
- evidence role: what evidence or reasoning job this page must perform; this replaces any fixed evidence-shape field;
- visual opportunity: where imagegen may create a more expressive composition instead of a fixed box/table layout;
- candidate visual directions: 2-3 possible visual carriers, not a locked layout shape;
- source evidence from the paper;
- must-preserve evidence: exact facts, names, metrics, captions, formulas, chart labels, source terms, or text to preserve;
- whether imagegen may redraw or must preserve a source figure;
- chart/key-finding annotation plan: callout arrow, highlight, label, shaded region, or focal-color treatment that makes the main finding visible without narration;
- unverified or missing facts: mark as `needs user confirmation`; do not include unsupported numbers, citations, cases, chart values, or claims in image prompts;
- layout intent;
- QA risks.

For a reusable template and examples, read `academic-blueprint-template.md`.

## 6. Blueprint Approval Gate

Show the full `Deck Blueprint` to the user and ask whether it is approved.

If the user is not satisfied, accept page-level revisions such as:

- changing one page's governing message;
- changing section order or section titles;
- changing target slide count;
- adding, deleting, splitting, or merging pages;
- changing the page's evidence role, visual opportunity, candidate visual directions, or which chart/table/source figure appears;
- changing a page from source-figure preservation to approved redraw or vice versa;
- changing final closing wording.

Revise the blueprint, show it again, and wait again. Do not create thumbnail variants until the user explicitly approves the blueprint.

Save the approved version as:

```text
qa/deck-blueprint.md
```

Record final slide count, user approval, and unresolved assumptions or risks.

## 7. Three-Option Thumbnail Gate

Before generating final per-slide images, create exactly three thumbnail variants and stop for user selection.

Use imagegen to create or revise every thumbnail preview board. Do not use Python + PIL, SVG/HTML/canvas, screenshots, local drawing, or other local refinement to create the thumbnail board unless the user explicitly requests that method.

Create:

```text
thumbnails/option_a.png
thumbnails/option_b.png
thumbnails/option_c.png
```

Each option should be a compact preview board, not a complete deck. It should show enough of the intended visual system for the user to choose:

- top introduction band with title, version, overall tone, style keywords, and basic user/project metadata when available;
- body area with exactly 6 miniature slide previews: 1 cover page, 1 contents page, 1 section-divider page, 2 representative content pages, and 1 standalone closing page;
- bottom specification band describing color rules, font rules with key font names, icon style, layout traits, and use scenarios.

The preview-board canvas itself may use any aspect ratio needed by the design. Do not force the whole preview board to 16:9. But the 6 miniature slide previews inside the board are slide mockups, so each one must be a true 16:9 rectangle with consistent proportions. Reject or regenerate boards where any mini slide becomes a vertical card, square card, long strip, cropped panel, rotated panel, or irregular panel.

The thumbnail board must preview a real page system, not a sparse moodboard or a set of cover-like title pages. The 2 representative content miniatures must show realistic evidence carriers guided by the approved blueprint, such as data cards, comparison tables, process arrows, evidence strips, mechanism diagrams, chart strips, framework nodes, and conclusion panels. Reject or regenerate boards that are mostly decorative, overly empty, disconnected from the approved deck structure, or too vague to judge the eventual content-page density.

Use `assets/reference-thumbnails/option-c-preview-board-format.png` as the structural reference for thumbnail and sample-page boards. Match the overall preview-board grammar: wide header, 2-row slide grid, and bottom standards strip. Adapt the visual style, palette, and sample slide content to the current paper and approved blueprint.

Recommended default variants:

- Option A: formal academic blue, closest to the bundled case-study style.
- Option B: cleaner college defense style with lighter ornamentation.
- Option C: more formal technical defense style with stronger diagrams and borders.

Show the three options to the user and ask them to choose one. Do not begin final `image_pages/slide_XX.png` generation until one option is selected.

If the user asks for changes, revise the selected option only unless they explicitly ask for a new three-option round. Save the approved visual contract as:

```text
thumbnails/selected.png
```

Record the selected option and any revision notes in:

```text
qa/thumbnail-selection.md
```

Then create:

```text
qa/thumbnail-style-contract.md
```

The style contract must extract the selected thumbnail's palette, typography, icon style, layout density, title system, header/footer treatment, chart/figure language, content-block rhythm, and decorative motifs. This contract is binding for sample pages and final slide prompts.

## 8. Full-Size Sample Page Gate

After thumbnail selection, generate 1-2 full-size sample pages from the approved blueprint, `thumbnails/selected.png`, and `qa/thumbnail-style-contract.md`. Prefer one cover or section page plus one content-heavy page with an evidence role that tests the visual system.

Use imagegen for sample pages. Do not use local refinement, Python + PIL, SVG/HTML/canvas rendering, screenshots, local drawing, or another local full-slide generation path unless the user explicitly asks for it.

Show the sample pages to the user. If the user requests changes, revise the selected visual direction, thumbnail style contract, or page prompt and regenerate the sample. Do not enter full-slide generation until the user approves the sample quality and the sample visibly inherits the selected thumbnail's style. Samples may add detail and polish, but they must not switch palette, title system, page rhythm, icon language, chart language, or density into another visual system.

If the user points to one sample page as the preferred basis for the final deck, create:

```text
qa/sample-revision-contract.md
```

Record the chosen sample's layout skeleton, information density, header/footer system, recurring evidence carriers, chart/table language, conclusion-panel style, required corrections, and exact high-risk text constraints. Examples of reusable sample-structure fields include: dark title bar, centered subtitle, insight banner, metric cards, evidence strip, bottom trend panels, right-side conclusion panel, and footer page-number system. Final slide prompts must obey this sample contract whenever it exists.

Record the approval in:

```text
qa/sample-approval.md
```

## 9. Full-Slide Image Generation

Use `imagegen` for every full slide. One imagegen call may generate one slide; do not use one prompt to create multiple distinct slides.

Do not use local refinement, Python + PIL, SVG/HTML/canvas rendering, screenshots, local drawing, or another local full-slide generation path unless the user explicitly asks for "本地精修方式生成", "Python + PIL", or equivalent local generation/refinement. The agent may use local tools for packaging, contact sheets, file checks, and QA, but not as a substitute for imagegen visual generation.

For each slide:

- use `qa/deck-blueprint.md` as the content source of truth;
- include exact Chinese text that must appear;
- keep text short enough for reliable image generation;
- include source figures as input references when they must be preserved;
- use `thumbnails/selected.png`, `qa/thumbnail-style-contract.md`, approved sample pages, and `qa/sample-revision-contract.md` when present as style references;
- state that all Chinese, numbers, formulas, and names must be rendered verbatim;
- prohibit hallucinated citations, logos, charts, fake metrics, unsupported cases, and unverified factual claims.

Use anchor-page-first generation when a page defines the final visual standard or carries the user's strongest preference. Typical anchors include the user's preferred sample page, a dense evidence slide, a key result slide, or the most representative content page. Generate and inspect the anchor first; only then expand to other pages. Save a generated image to `image_pages/slide_XX.png` only after it passes the visual contract and high-risk text checks. If one page repeatedly fails imagegen, record the issue, continue with independent pages when safe, then return to regenerate the failed page before contact-sheet QA.

Maintain a high-risk text list while generating. For every relevant page, explicitly check school/institution name, logo use, student/author name, student ID, major/program, advisor display or omission, date, closing wording, section titles, page numbers, metric names, metric values, chart labels, and indicator meanings. A number can be visually correct but still wrong if the indicator label changes; regenerate or correct such pages.

After generation, save the selected slide image under:

```text
image_pages/slide_XX.png
```

Use zero-padded numbering. The final count must match the approved blueprint.

## 10. Contact Sheet QA

Create a contact sheet from all slide PNGs. Inspect it before packaging:

- the section rhythm is clear;
- every expected page is present;
- page numbers are sequential;
- no missing standalone closing page;
- style is coherent;
- all slides follow the selected thumbnail and approved sample direction;
- charts and tables are legible enough at full size;
- no obvious imagegen text corruption.

## 11. PPTX Packaging

Before packaging, create `qa/speaker-notes.md` unless the user explicitly asked to omit speaker notes. Write one note block per approved slide, in slide order.

Speaker notes rules:

- use headings in the exact form `## Slide 01`, `## Slide 02`, and so on;
- base every note on the approved blueprint, slide image content, and source material;
- make notes suitable for defense/report narration, not a verbatim reading of slide text;
- keep each note concise enough for the user's target duration;
- include transition cues where they help the presenter move between sections;
- preserve exact names, metric meanings, chart conclusions, and closing-page wording;
- do not add unsupported claims, citations, numbers, cases, school metadata, or experiment results.

Package by embedding each slide image as one full-bleed image and inserting the matching note block into that slide's speaker notes area.

Rules:

- derive slide count from `image_pages/slide_*.png`;
- never hardcode a count such as 20;
- preserve filename order;
- derive speaker notes count from `qa/speaker-notes.md`;
- match `Slide 01` notes to `image_pages/slide_01.png`, `Slide 02` notes to `image_pages/slide_02.png`, and so on;
- set image position to `x=0`, `y=0`, `w=1280`, `h=720`, `fit=cover`;
- verify that PPTX slide count equals image count and approved blueprint count;
- verify that notes count equals slide count unless the user explicitly chose no notes;
- verify that each PPTX slide's notes area contains the intended note text;
- verify that each slide contains exactly one full-bleed image and no extra editable text/shapes;
- final file name should be `<paper-title>_图片版.pptx`.

Use the bundled script when the environment has Node.js dependencies available:

```bash
npm install
node skills/academic-image-ppt/scripts/package_image_pptx_with_notes.mjs \
  --images <run>/image_pages \
  --notes <run>/qa/speaker-notes.md \
  --out <run>/output/<paper-title>_图片版.pptx \
  --title "<paper title>"
```

## 12. Final Verification

Before delivery, verify:

- `qa/alignment-summary.md` exists and records user confirmation;
- `qa/deck-blueprint.md` exists and records blueprint approval;
- `thumbnails/option_a.png`, `option_b.png`, `option_c.png`, and `selected.png` exist;
- `qa/thumbnail-selection.md` records the user's chosen visual direction;
- `qa/thumbnail-style-contract.md` exists and was used by sample and final prompts;
- `qa/sample-revision-contract.md` exists if the user selected a sample structure as the basis for final pages, and was used by final prompts;
- `qa/sample-approval.md` records full-size sample approval;
- `qa/speaker-notes.md` exists unless notes were explicitly omitted;
- all slide images exist and are exactly `1280x720` unless another size was selected;
- `qa/contact-sheet.png` includes all expected slides;
- PPTX slide count equals image count and approved blueprint count;
- PPTX speaker notes count equals slide count unless notes were explicitly omitted;
- each PPTX slide contains exactly one full-slide image;
- each PPTX slide's notes area contains the matching defense narration from `qa/speaker-notes.md`;
- OCR/manual QA confirms critical Chinese text, formulas, metrics, names, and captions;
- all data, citations, chart values, cases, and factual claims are traceable to source material or explicit user confirmation; unresolved items were omitted or marked `needs user confirmation` before prompting.

Record results in `qa/pptx-package-check.md` or the final response.
