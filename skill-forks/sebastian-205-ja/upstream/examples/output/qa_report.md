# QA report

- Source sufficiency: full-paper
- Output: paper2ppt-example-zh.pptx
- Slide count / dimensions: 9 slides; 13.333 x 7.5 in; 16:9
- Source: Nwosu et al. (2022), PLOS ONE, DOI 10.1371/journal.pone.0276250
- Authoring path: python-pptx 1.0.2; PyMuPDF 1.28.0 and publisher JATS XML for page-grounded extraction; Pillow 12.3.0 for showcase images
- Preflight: pass; editable authoring, PDF extraction, Pillow, writable output, and renderer were available

## content QA

- Status: pass
- Source alignment: every substantive statement was checked against the full 14-page PDF and JATS XML.
- Claim-to-source outcome: slide 2 -> Introduction and section 3.3; slide 3 -> sections 3.1-3.3 and Fig 3; slide 4 -> section 2.3 and Fig 1; slide 5 -> Table 2; slide 6 -> Fig 4 and adjacent results text; slide 7 -> Table 3, Fig 5, and adjacent results text; slide 8 -> full study design plus section 5; slide 9 -> Tables 2-3 and section 5.
- Numeric check: slide 5 reproduces F32_R50, EECE, and EMVEM F1/ECE/MCE values from Table 2; slide 7 reproduces the three-model and five-model EMVEM F1/ECE/MCE values from Table 3. All values and standard deviations match the JATS XML and PDF.
- Figure integrity: Figs 1, 3, 4, and 5 retain their complete panels, labels, aspect ratios, and publisher color encoding. No source figure is cropped.
- Attribution: every slide using or reconstructing result evidence has a visible source label; extracted assets are traced in `asset_manifest.md`.
- Evidence boundary: the qualitative examples are identified as examples, the absence of external/clinical validation is labeled as reader synthesis, and lower calibration error is not presented as proof of clinical safety.
- Unsupported candidates removed or narrowed: no significance claim, monotonic model-count claim, clinical-effectiveness claim, or computation-cost claim is made because the paper does not establish them.

## structural QA

- Status: pass
- Inspector: `scripts/inspect_pptx.py --require-notes --json`
- Reopen result: 9 slides, 4 embedded media parts, 9 notes-slide parts.
- Notes: meaningful speaker notes are present on slides 1-9; result-slide notes state the evidence, qualifier, limitation, and transition.
- Package integrity: no missing or orphaned media, broken/internal-invalid relationships, external asset dependency, CRC error, or content-type error.
- Bounds: no negative, zero-area, wholly off-slide, or out-of-bounds object was reported.
- Inspector findings: 0 warnings; 0 errors.

## visual QA

- Status: pass
- Renderer: LibreOffice 26.2.1.2 exported the PPTX to PDF; Poppler `pdftoppm` 26.02.0 rendered every slide at 1920 x 1080.
- Slides inspected individually: 1-9
- Contact sheet inspected: pass
- Showcase inspected: `overview.png`, `slide-04-method.png`, `slide-05-results.png`, and `slide-08-boundaries.png` are readable and nonblank.
- Checks passed: no overlap, clipping, overflow, off-canvas content, missing glyph, broken image, unreadable source label, distorted figure, or inconsistent slide margin.
- Projection readability: slide 4 expresses the method in editable large text so its conclusion does not depend on the fine labels in original Fig 1; slide 7 presents Table 3 values separately so Fig 5 functions only as qualitative evidence.
- Revision record: the first render exposed inconsistent styling after manual line breaks on slides 1, 2, and 9; all text runs were restyled, the deck was rebuilt, and slides 1-9 were rerendered and rechecked.

## Unresolved issues

- None for artifact delivery. Scientific generalization remains bounded by the single-dataset design and the missing external and clinical validation disclosed on slide 8.

## Completion state

- Status: pass
