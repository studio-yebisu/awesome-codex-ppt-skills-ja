# QA Checklist

## Reference fidelity

- The user-provided reference or research gallery was inspected visually.
- The output uses the same dominant diagram grammar.
- Density, title hierarchy, line language, photo treatment, and source placement are recognizably aligned.
- The output is not a near-trace: at least three structural choices differ from any single non-owned reference.
- Distinctive wording, data, chart artwork, illustrations, and source-specific placement were not copied without permission.
- An internal derivation note distinguishes reference-derived grammar from original design decisions.
- The output does not fall back to a generic card grid.
- Public references were used for design research unless reuse rights are clear.
- Pages explicitly requested in JTC, JEITA, ministry, or traditional Japanese corporate style score at least 17/20 on [jtc-authenticity.md](jtc-authenticity.md).

## Document control

- Material number, date, version, status, responsible unit, and handling class are shown only when relevant and true.
- `案`, `暫定`, `要確認`, `継続審議`, `抜粋`, and `一部加工` are used accurately.
- The slide distinguishes fact, estimate, proposal, and unresolved issue.
- Owners, due dates, gates, and decision items are named for approval or coordination pages.

## Content closure

- The communication job is explicit.
- Every slide has one primary conclusion.
- The dominant model includes relevant actors, stages, layers, or decisions.
- Important arrows are labelled.
- Evidence, implication, caveat, and next action are present when relevant.
- Facts, dates, units, names, and sources are verified.
- Estimates and illustrative values are labelled.
- No internal production notes appear on audience-facing slides.

## Typography

- Rail and primary titles do not wrap unexpectedly.
- Entity and action labels are readable at normal presentation size.
- Primary body is normally 16pt or larger.
- Compact 11–15pt text is limited to evidence, annotations, definitions, and supporting detail.
- Source and caveat text remains readable at full-size inspection.
- Japanese font substitution is acceptable.

## Layout

- Header, footer, and page numbers are consistent.
- Occupancy is intentionally dense, not accidentally crowded.
- No unintended overlap or clipping exists.
- Connectors sit behind nodes and do not cross labels.
- Arrow direction and meaning are clear.
- Tables have enough cell padding.
- Bottom notes do not cover the main figure.

## Images

- Every image has a defined role.
- Real-world images and logos are authentic and traceable.
- Generated sample or illustrative photography is not presented as client evidence.
- Image crops preserve the relevant subject.
- External source excerpts include organization, document, date, page, or URL as appropriate.
- The same image is not reused without a reason.
- Red boxes and arrows identify a real focus area and do not decorate the page.
- Added chart annotations do not hide essential axes, legends, labels, or data.
- Time and threshold markers align with the actual source date or value.
- Original chart text and presenter-added interpretation are visually distinguishable.
- Cropping, translation, highlighting, and other processing are disclosed accurately.

## Editable integrity

- Text, simple diagrams, tables, and charts remain native and editable.
- No whole slide is flattened.
- A recreated diagram is not a screenshot, background image, or single raster object.
- Every major title, entity, relationship label, marker, annotation, source, and decision statement can be selected and edited independently.
- Native charts expose editable categories, series, and values.
- Every raster image has a justified evidence, photography, logo, screenshot, or attributed-source role.
- Added annotations remain separate components even when the underlying source excerpt is an image.
- No unresolved `{{...}}` placeholder remains in a delivered client deck.
- Sample-photo assets are replaced when authentic project photographs exist.

## Required validation sequence

Use the validation and rendering tools available in the host environment.

1. Test package integrity with `unzip -t "$FINAL_PPTX"`.
2. Run the host's slide-overflow or bounds check when available.
3. Render every slide with an independent compatibility renderer.
4. Create a contact sheet to inspect rhythm and consistency.
5. Inspect every rendered slide individually at full size.
6. Reopen or reimport the exported PPTX and confirm that key text, shapes,
   connectors, tables, charts, and image frames remain independently editable.

In Codex, use the installed Presentations skill and its current validation
commands. In another agent, use that agent's equivalent PPTX inspection and
rendering workflow.

## Package checks

- `unzip -t "$FINAL_PPTX"` passes.
- Slide XML count matches the intended count.
- No non-directory ZIP part is empty.
- No unsupported `.bin` media exists.
- Native shape, table, chart, and image objects appear in inspection.
- The PPTX imports and renders through the host authoring tool and an independent compatibility renderer.

## Delivery

- Preserve source decks unless in-place editing was explicitly requested.
- Keep research downloads, plans, layout JSON, and QA artifacts out of the final output folder.
- Return the editable PPTX, not only screenshots or PDF.
