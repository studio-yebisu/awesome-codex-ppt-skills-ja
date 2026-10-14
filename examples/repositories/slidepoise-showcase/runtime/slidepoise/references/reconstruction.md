# Reconstruction rules

## Native-first routes
Use native PowerPoint text, shapes, tables, charts, and connector graphs when their semantics are known. Restore exact canonical SVG/image assets selected upstream.

Use a fitted freeform only for a meaningful editable irregular shape that cannot be represented by a standard PowerPoint primitive. Use a screenshot crop for a genuine raster/illustrative region when no exact reusable asset exists and editable decomposition would invent unsupported structure. This raster route is also appropriate for a proprietary/profile gradient whose exact editable stops are not specified and no canonical gradient asset is available.

## Profile authority
The resolved profile contributes exact design values and hard rules before reconstruction. The accepted generated image remains the source of truth for composition and non-canonical visual details. Preserve its substantive layout, hierarchy, grouping and meaningful content. Local corrective offsets are permitted when rendered text metrics, asset insets or native geometry disturb the intended optical alignment. The host Agent must inspect the actual render, identify the affected visual relationship and verify that the correction restores it within the accepted composition. This does not authorise unrelated redistribution, simplification or deletion of content. Follow the optical alignment guidance below.

For an authorised wording-only refinement, `content-refinement.md` defines the narrow exception for native text content. The accepted image still governs composition and geometry. Record the original and revised strings, update the intent and obligations, and use `authored_text` for the revised native wording. Keep the packaged reconstruction path and inspect the actual render. This exception does not authorise changing data, meaning or visual relationships.

If a profile rule conflicts with a generated candidate, that conflict should normally have been caught during generation review. Mechanical evidence collection may report explicit violations that can be established without visual judgement. The Agent decides the response.

## Text
First distinguish native presentation text from lettering owned by a raster. Read `raster-composition.md` for intrinsic lettering, expressive handwriting, clean plates, and overlapping foreground text.

The host Agent assigns semantic `role`, visual `text_style_role`, logical textbox region, a non-empty `typography_group`, and `target_font_size_px` for every meaningful text entity. `role` describes meaning. `text_style_role` selects the configured style and readability policy. `typography_group` records the font-size hierarchy and content level. Textboxes at one content level share one group and one target size even when their wording or box dimensions differ. Shared role names alone do not establish visual peerhood. The Agent can assign different groups when local hierarchy calls for it and must explain that choice in its review. A singleton level still has a group. Members of a group must use one `text_style_role`. The fitting runtime may reduce a shared target to prevent overflow. It never increases the Agent's target because a box has spare room.

A typography group is page-local fitting scope. Matching group names on different pages do not enforce a shared size, and different names can still belong to one recurring deck role. Read the deck owner's visual role inventory, resolve its page aliases and materialize each chosen treatment in the actual entity styles or compatible config tokens. Retain those bindings in the handoff. Read the compiled and native style values, then inspect the role across actual renders. Equal emitted numbers alone do not establish equal appearance, and local fit success cannot establish cross-page consistency. See `deck-orchestration.md` for discovering additional recurring roles and recording intentional exceptions.

OpenCV supplies text-ink and foreground/background evidence. The deterministic fitter finds the largest size at or below the Agent-authored target that fits every member of each declared typography group and applies that exact point size to all members. Missing groups are invalid. The runtime never falls back to fitting an ungrouped textbox independently, and it never enforces a visual minimum or maximum font size. The Agent judges whether the resulting size is appropriate for the slide.

The resolved profile may restrict font families, italics, tracking, or text colours. When such restrictions are mechanically checkable, semantic-map evidence should report them early so the Agent can correct the map before reconstruction.

Observed italic and tracking treatments use `style_hint.italic` and `style_hint.char_spacing_px`. Tracking is measured in accepted-image pixels and participates in text fitting. These controls do not identify a font automatically. Compare actual rendered weight, spacing, baseline, and line breaks before accepting a substitution.

An observed paragraph rhythm may set `style_hint.line_spacing` as a multiple of the font size. The same value is consumed by measurement and native emission. Tracking is emitted as signed DrawingML character spacing, including tightly tracked display type. For native charts, explicit `show_category_axis`, `show_value_axis`, `category_order`, `value_axis_minimum`, `value_axis_maximum`, `gap_width_pct`, and relative `plot_layout` describe the observed chart presentation while the authored data remains authoritative.

Use native chart data labels when visible numbers represent its values, so a workbook edit updates both the marks and their labels. Set `show_values`, `data_label_position`, `data_label_format_code`, `data_font_family`, and positive `data_font_size_px` from the target. `data_label_color` sets a shared color. `data_label_colors` can set one six-digit color per category while preserving the native value binding. Set `data_label_wrap` to `false` when each numeric label must stay on one line, or `true` to allow wrapping. Omission preserves the Office reader's default. Inspect the actual render to check label clearance. Keep source numeric regions as chart-owned measurement members to avoid emitting duplicate textboxes. Chart values and numeric options must be finite numbers. Line spacing must be a positive finite number.

Check fonts in the renderer as well as in PowerPoint. A correct font-family string in the PPTX does not establish that the preview renderer found that font. When a host needs a Fontconfig file, keep it in the run or external environment, pass it through `render-preview --font-config`, and retain the font-family choice with the case. Do not put machine-specific font paths or proprietary font binaries in the skill.

On macOS, `render-preview` supplies existing system and user font directories through a temporary Fontconfig file when no explicit font configuration is present. An explicit command option or `FONTCONFIG_FILE` remains authoritative. The render sidecar records the font configuration source. Other operating systems retain the renderer's default font discovery.

`audit-text` checks explicit settings in generated PowerPoint objects. Textboxes require authored body insets, wrapping, anchor, paragraph alignment and line spacing. Native table cells use `a:tcPr` margins and anchor, and may retain legal paragraph defaults. The audit requires explicit cell margins and anchor as the generated-output contract, validates their DrawingML values, and checks both representations for explicit font, size and autofit settings. It does not judge visual fit or replace rendered inspection. Cell centering serializes as `ctr` under the [DrawingML anchor definition](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.textanchoringtypevalues?view=openxml-3.0.1).

Inspect each text group's compiler evidence before accepting the render. `members_not_fitting_target` identifies allocations that force a shared reduction. `font_measurement_sources` records the font files used for measurement, without claiming that every glyph or the preview renderer uses the same font. `profile_adjustments` records requested and resolved values when profile rules replace a font, italic treatment, or colour. Resolve material changes through the semantic map, allocation, or authorised profile settings, then render and compare again. Explicit authored line breaks survive by default. A deliberate reflow may set `preserve_explicit_breaks` to false.

Keep search bounds, visible-pixel evidence, final layout bounds, and source crop bounds distinct. Read the measurement overlay after geometry adjustments. Raw RGB difference images from `make_visual_comparison.py --difference` can locate changed regions, and contain no visual acceptance score. Compare the full page and the affected local region against the same accepted target. Record the discrepancy, changed parameters, and the visual result of the next render. Preserve the previous usable presentation until emission and postprocessing both succeed.

An entity may declare `search_bbox_hint` independently of `bbox_hint`. OpenCV gathers pixel evidence only from the search window. With `geometry_policy: agent_logical`, `bbox_hint` remains the native object allocation. This distinction is useful for large serif text whose Office baseline places visible ink below its textbox top, or for adjacent lines with overlapping logical allocations. The host selects complete source-ink windows and checks that neighboring text has not contaminated the measurements. Raster crops still use the final layout box. Both boxes require finite coordinates, positive dimensions, and an intersection with the accepted-image canvas.

## Novel illustrations
A `kind: image`, `visual_source_class: novel_illustration` entity is a generated raster with no canonical upstream asset. Its geometry comes from the approved slide and OpenCV measurement. Its pixel source may be the original accepted-slide crop or a refined raster selected through Agent review.

For an active `raster_source_override`, preserve the full registered canvas in the original logical box. `raster_source` binds the source file, alpha requirement, canvas and accepted image. Its aspect ratio is validated before placement. Do not crop to alpha bounds or recenter the visible silhouette. Relative source paths resolve from the semantic map. A `reuse_original` decision selects the original crop instead.

Novel illustration refinement does not reopen slide composition. It only upgrades the raster source inside an already approved slot. If a refined source is not good enough, fall back to the original crop unless the user explicitly requests another change.

## Assets and user uploads
The reconstruction handoff retains the exact canonical path/ID chosen by the host Agent. Exact user/current-chat assets are first-class canonical assets. Preserve intrinsic aspect ratio and contain-fit them into their Agent-authored logical slot by default. Do not stretch an asset to mimic a generated placeholder. If the fit leaves a materially wrong composition, revise the slot or upstream design and rerun.

Use optional `handoff.speaker_notes`, an array of strings, for audience-facing presenter notes. The contract and constructor scene preserve these exact strings, and the native renderer writes them before source references in the PowerPoint notes. Internal `handoff.notes` remain outside that channel. The host chooses which assumptions, context or editing limitations belong in the presentation.

## Icons
SlidePoise uses the existing icon pipeline for icons and pictograms alike. Do not introduce a second asset/entity concept just to distinguish those brand terms.

The logical icon slot is separate from the designed surface. Always use the Agent-authored slot for canonical-asset fitting and layout constraints. Every meaningful icon or icon slot also carries an `icon_treatment_group` that represents its local peer-level treatment family. Emit a surface only when `slot_surface.visible` is true because the accepted design intentionally uses a real icon background surface. A faint generation-only localization boundary is scaffolding and must map to `slot_surface.visible=false`. When the icon is meant to sit on a larger colored parent panel or card, omit any white slot box so the icon background remains transparent and the parent colour shows through. Members of one `icon_treatment_group` must reconstruct with one coherent glyph treatment family and one coherent surface treatment. Apply the peer group's explicit profile treatment to every member while preserving canonical glyph geometry.

For a recolourable proxy, use `style_hint.glyph_color` or `style_hint.glyph_gradient`; do not assign both. Exact profile assets should preserve their canonical artwork. A profile may constrain proxy colours/gradients and visible surface fills. Do not add a default badge, holding shape, surface, scaffold border, or white knockout tile that was not part of the accepted design.

## Reusable components
A chart or table may carry an optional `component_id` referencing the selected profile's private component catalog. The host Agent assigns this only when the accepted target actually uses that component grammar.

A component is not copied verbatim. Start from its generic constructor defaults, then override with the entity's real data/content, category/series or row/column count, labels, geometry, and any visual differences visible in the accepted target. The native donor PPTX/slide remains an authoritative editable precedent and provenance source, not sample content to paste. If adaptation would make the precedent misleading or awkward, omit `component_id` and reconstruct normally.

## Data visualisation
When an editable chart has authored data but no explicit series colours, use the resolved profile's chart colour defaults rather than PowerPoint's theme colours. Explicit Agent-authored chart colours remain authoritative only when they are compatible with the selected profile or an intentional profile exception.

Record the chart geometry explicitly. Use `column` for vertical columns and `bar` for horizontal bars. Orientation, category order, axis direction, stacking, labels and scale are part of the chart's semantic structure. Compare each of them with the accepted target in the rendered PowerPoint. Correct data alone does not establish fidelity.

Review the generated design and the actual PowerPoint in one full-slide coordinate system. Confirm the position and relative scale of every major region, then inspect chart orientation, category order, axes, labels and emphasis. Place a body-only generated image at its configured content offset before comparing it with the full slide. Never stretch the body image to fill the complete slide for review.

## Shape geometry
### Authored paths and stacking

For an intentional editable curve, a shape entity may use `shape: authored_path`, `reconstruction_route: fitted_freeform`, and `path_commands_px`. Each command uses absolute accepted-image pixel coordinates. `M` and `L` carry `point`, `C` carries `control1`, `control2`, and `point`, and `Z` closes a path. Omit `Z` for open rules and arrows. The host chooses control points through visual inspection. The runtime only transforms and emits them.

An explicit numeric `z` controls stacking, with lower values behind higher ones. Inspect text, raster repairs, and original crop overlaps in the rendered slide. Do not let kind defaults conceal an intended layer order.

A freeform arrow remains an editable path. It does not automatically attach to moved objects. Use the semantic connector route when owner binding is required and disclose that distinction in examples.

### Rounded geometry

The host Agent visually classifies rounded-rectangle intent and records the observed radius. The runtime translates that radius into an editable PowerPoint roundRect adjustment. It applies only PowerPoint's technical half-short-side limit. Code does not impose an aesthetic rounding cap.

The final visual review must compare silhouettes. An in-range radius is only mechanical evidence and does not establish fidelity.

## Layout integrity and survival
Only the host Agent decides which independent content regions must not overlap. Record those pairs in the semantic map. The runtime enforces the declared pairs after canonical asset placement and text fitting.

The host marks meaningful dividers with `structural_boundary: true`. A textbox allocation crossing a declared boundary is a blocking fact. A thin shape alone does not establish semantic separation, and an allocated textbox is not its visible ink. For an intentional composition such as a label placed across a rule, set `allow_text_crossing: true` on that rule or `allow_boundary_crossing: true` on the text entity and record the reason in the visual review.

Every meaningful visible entity in the accepted target must survive reconstruction. It must either emit its own PowerPoint object or explicitly identify a distinct emitted `render_owner` that replaces/owns it. `measurement_evidence` may be non-emitting only when `meaningful_visible=false`. Never remove an entity merely because a canonical asset is unavailable or because the Agent thinks the slide would be simpler without it; such a candidate should have been rejected upstream.

## Optical alignment

The host Agent must check optical alignment on every reconstructed slide before acceptance. Inspect the measured overlay for geometry evidence, then compare the actual PowerPoint render with the accepted target at the same scale. Judge visible text edges and baselines, apparent centres and visual mass of artwork, and gaps within and between related groups. Equal textbox or container coordinates do not establish equal visible alignment. Preserve intentional asymmetry and distinct hierarchy when deciding which elements should align.

Author necessary local position corrections in `geometry_adjustments`. Inspect font metrics, text insets and asset padding when they explain an apparent offset. Preserve registered raster canvases and their internal placement as required by the raster-source rules. Runtime applies the exact, version-checked decisions. Without a decision it keeps the measured position. It does not infer peers, choose median anchors, snap nearby objects, or decide whether a movement is visually appropriate.

Re-render and inspect the corrected region, its neighbours and the whole slide after every correction batch. Record the affected entities, observed mismatch, correction and visible result in the reconstruction review. Routine offsets that restore intended alignment are part of reconstruction. Discuss material compositional changes with the user when their intent is unclear.

## Master frame
The substantive image excludes enabled header/footer regions. Reconstruction maps that image into the derived generation region, then the renderer creates inherited frame content through the PowerPoint Slide Master/layout hierarchy.

PowerPoint slides do not expose a native slide-header placeholder, so header text/rules are master-layer inherited elements. Footer text/rules are also inherited master/layout elements. Slide number uses PowerPoint's native slide-number field on the master. These frame elements must not be emitted as ordinary slide objects.

## Content obligations and native tables

The handoff's `content_obligations` preserves a host-authored inventory independently of the semantic map. Each entry has a unique `id`, a `description`, and nonempty `entity_ids`. A relationship additionally declares `connection` with `entity_id`, `source_entities`, `target_entities`, and boolean `directed`. The constructor rejects missing required entities and changed relationship ownership or direction. This is an exact contract check. The host still judges whether the inventory covers the plan and image.

Treat a table as a composition of cells. Preserve each cell's alignment, selected-row fill, run-level emphasis and intentional line breaks. Cell `margin_px` accepts four nonnegative pixel values in top, right, bottom, left order. The renderer converts those slide-canvas pixels into Office points. Legacy `options.margin` already uses points. Do not mix both fields or pass measured pixels as Office points. Named fonts, margins and column widths jointly determine wrapping. Inspect the actual native render for broken words and row growth.

Separate spatially distinct formula annotations into individual text entities. Padding a single string with spaces cannot preserve the relationship between factors and captions through font substitution or text fitting.
