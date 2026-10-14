# Quality gates

Run three distinct layers: `content QA`, `structural QA`, and `visual QA`. Record evidence for each layer; do not infer one layer from another.

## 1. content QA

- Verify every substantive slide claim against the claim-to-source map.
- Confirm source sufficiency supports the level of interpretation; narrow or remove materially unsupported claims.
- Recheck numbers, units, denominators, cohort sizes, dataset splits, baselines, statistics, confidence intervals, and qualifiers against the source.
- Confirm the correct figure, panel, and crop selection; preserve labels, axes, units, scales, legends, colorbars, and statistical marks.
- Verify figure-to-claim correspondence and ensure cropping makes no misleading exclusion of context, comparisons, controls, or qualifiers.
- Distinguish association from causation and observation from interpretation. Preserve the paper's uncertainty and causal language.
- Label every inference, synthesis, and permitted reconstruction. Confirm every reconstructed component and relationship is source-supported.
- Verify each result slide has a source label and notes explaining the evidence, interpretation, limitations, and transition.
- Include material limitations, failure cases, competing explanations, and boundaries of generalization.

Pass `content QA` only when the evidence chain is supportable and no material contradiction remains.

## 2. structural QA

Run the packaged structural inspector before recording this gate:

```text
python "<SKILL_DIR>/scripts/inspect_pptx.py" deck.pptx [--require-notes] [--json] [--report qa_report.md]
```

Use `<SKILL_DIR>` resolved by the main Skill; do not locate this helper from the current working directory.

`notes_slides` is the package-level count of notesSlide parts. The inspector
separately checks meaningful speaker-note text on each reopened slide. Its result
supports structural QA; it does not replace content QA or rendered visual QA.
It also checks archive limits, CRC integrity, content types, internal relationships,
embedded media, and shape bounds. It rejects each external asset relationship;
ordinary hyperlinks remain allowed. `--report` uses atomic replacement and refuses
any path that aliases the input deck.

- Reopen the generated PPTX as an OOXML package and, when available, with an independent presentation reader.
- Confirm the expected slide dimensions, slide count, order, and output filename.
- Validate media files, content types, slide relationships, image relationships, and notes relationships; report orphaned or missing parts.
- Confirm required speaker notes and source labels are present on every result slide.
- Confirm `presentation_zh.pptx` or the requested language variant and `qa_report.md` exist; require `asset_manifest.md` and `assets/` only when assets were extracted.
- Flag obviously out-of-bounds objects, negative coordinates, zero-size shapes, and objects wholly outside the slide canvas.
- Confirm no external, temporary, or broken asset reference is required to open the deck.

Pass `structural QA` only when the PPTX reopens and its required parts and relationships are intact.

## 3. visual QA

Render every slide when a renderer is available. Inspect both individual pages and a contact sheet for:

- overlap, clipping, text overflow, off-canvas objects, and unintended occlusion;
- missing glyphs, substituted fonts, broken equations, and malformed symbols;
- low contrast, color-only distinctions, and weak visual hierarchy;
- projection readability of titles, body text, legends, axes, captions, and sources;
- excessive figure density, insufficient resolution, compression artifacts, and distortion;
- inconsistent margins, alignment, scale, or caption placement across the deck.

Do not claim `visual QA` passed when no renderer exists. Mark it unavailable, name the missing renderer, and state that visual defects may remain.

## Revise and rerun

1. Record each failure with slide number, gate, symptom, and intended correction.
2. Revise the source deck or generation logic; do not patch only a preview image.
3. Rerun the affected checks until they pass.
4. Rerun all three applicable gates across the full deck before delivery.

## Completion states

- **`pass`:** content QA, structural QA, and visual QA all pass.
- **`structurally-verified-with-disclosure`:** Allow only when content QA and structural QA pass and visual QA is unavailable solely because no renderer exists; disclose that limitation.
- **`blocked`:** editable PPTX authoring or reopening fails, or the requested argument remains materially unsupported by available evidence.
- Set `blocked` for any unresolved content QA failure.
- Set `blocked` for any unresolved structural QA failure.
- When a renderer is available, set `blocked` for any unresolved visual QA failure.

Never label a blocked deck complete. Never downgrade a content failure to a visual limitation.

## Minimal `qa_report.md`

Use this schema and keep evidence concise:

```markdown
# QA report
- Source sufficiency: full-paper | partial-paper | notes-only
- Output: presentation_zh.pptx
- Slide count / dimensions: ...

## content QA
- Status: pass | fail
- Evidence and limitations: ...

## structural QA
- Status: pass | fail
- Reopen, media, notes, sources, bounds: ...

## visual QA
- Status: pass | unavailable | fail
- Renderer and inspected previews: ...

## Unresolved issues
- Slide / gate / impact / next action: ...

## Completion state
- Status: pass | structurally-verified-with-disclosure | blocked
```
