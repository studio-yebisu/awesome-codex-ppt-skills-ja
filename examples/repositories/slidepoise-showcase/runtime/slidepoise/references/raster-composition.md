# Raster ownership and layered reconstruction

Read before mapping a slide with collage, texture, photographed lettering, overlapping text, or a background image. Decide ownership before extraction. A raster crop is an intentional reconstruction unit when native decomposition would lose its meaning or appearance.

## Decide what the words belong to

- Presentation text such as titles, stage labels, and explanatory copy normally becomes native text.
- Lettering depicted inside a photograph, paper fragment, book, interface, or illustration normally belongs to that raster. Preserve it with its owner. A transcript may live in notes or metadata without adding a second visible textbox.
- Expressive lettering and handwriting require a choice. Test a native font when editing matters. Preserve the original mark when its individual strokes carry the design and a substitute is visibly weaker. Disclose that editability limit.

OCR detection does not decide these categories. Do not create a text entity for every detected word. If an intrinsic detail is mapped separately for traceability, give it a raster render owner and no duplicate visible emission.

## Reuse quality is relative to output

Measure the source crop in pixels and its intended display size. For a web export, compare available crop pixels with the pixels it will occupy in that export. For print, calculate effective PPI from pixels and placed inches. These numbers describe resampling demand, not acceptance.

Inspect the crop at intended output scale, then inspect a detail that exposes the relevant edges, grain, or small lettering. A small crop shown small may be adequate. A large crop may still contain blur. Simple resizing increases dimensions without recovering detail. Regenerating a component independently can produce more usable detail than its small region in a full-slide image, but the new detail is generated and needs review. Preserve deliberate grain and soft focus.

Record an entity's `raster_decision` with `action`, `reviewed_by`, and `reason`. Include source dimensions, intended output size, inspected artifact paths, intrinsic text ownership, and any `occluding_native_text_ids` in the decision evidence when relevant.

- `reuse_original` keeps an adequate crop without another image call.
- `refine` selects an isolated crop for more usable detail, a focused repair or background isolation. Only these objects enter illustration preparation.
- `clean_plate` removes foreground content destined for native reconstruction from an underlying image while retaining its coordinate system and background continuity.
- `preserve_composite` keeps an inseparable region together and records which content remains raster.

These are source actions, not size-based classifications. The Agent chooses and explains the action. Scripts neither score sharpness nor infer a winner.

## Text overlapping artwork

A flattened source has lost the pixels hidden by opaque text. Neither cropping nor alpha extraction can recover them exactly. A repair estimates plausible missing content. State this when fidelity matters.

If native text overlaps textured imagery, use an edited clean plate in the same coordinate system. Remove only the external text being rebuilt, preserve intrinsic lettering and artwork, and restore the external text as native foreground. Inspect for residual glyphs, altered artwork, and texture discontinuities before using the plate.

Choose the smallest useful ownership boundary. An isolated panel can have a clean plate. Collage sharing a continuous textured or photographic background may need one full-canvas plate beneath native overlays. This intentionally preserves the background and collage as one raster layer. It does not make each collage fragment separately editable.

Keep the accepted original unchanged. Store the edited plate separately with provenance and the list of removed foreground entities. Place it at the original aspect ratio and coordinates. Use `raster_source_override` on its image owner. Do not stretch a new composition into the old box. Isolated-board refinement cannot clean overlapping presentation text safely.

Never conceal residual text with a sampled flat rectangle unless inspection confirms that region is genuinely uniform. A near-white textured field is not uniform. Background photography is allowed. When a repair is poor, preserve the composite with an explicit editability limitation or ask for a layered source.

## Transparency and segmentation

Treat transparent output as an optional host capability. Use the source preparation, alpha validation and canvas registration in `illustration-refinement.md`. A prompt requesting transparency is not evidence that an alpha channel was produced. Inspect valid transparent assets on contrasting backgrounds and in the rendered slide before adopting them. An opaque same-canvas clean plate does not require transparent generation.

OpenCV can measure a visible boundary. It cannot recover occluded content or decide which lettering belongs to an image. Wispy paper shadows, translucent sheets, and grain often benefit from a shared plate because extracting them separately introduces halos or seams.

## Typography and palette evidence

Read the profile's explicit restrictions. With an open personal profile, take the approved candidate's appearance as evidence, then select available font candidates and compare rendered samples. A raster rarely proves an exact font identity. Record substitutions and inspect weight, tracking, baseline, line breaks, and punctuation.

Sample colors from stable interiors, avoiding antialiasing and texture edges. The Agent decides which peers intentionally share a role and authors their common values. Preserve purposeful photographic, paper, shadow, and transparency variation. Do not flatten the whole image into a palette or force every near-gray into one color.

## Iterative corrections and evidence

Inspect a render, identify affected entities, author exact corrections, then re-render and inspect again. No script discovers alignment peers or chooses target coordinates. Local `geometry_adjustments` contain `entity_id`, `before_bbox_px`, `after_bbox_px`, `reviewed_by`, and `reason`. Stale, nonfinite, resizing, and off-canvas decisions fail. The host Agent decides whether a movement still implements the selected composition. Discuss material compositional changes with the user when their intent is unclear.

Review the whole slide and relevant close-ups of overlaps, lettering, crop edges, and connector junctions. Persist the actual inspected images and hash-bind reviews to those versions. Record concrete observations and remaining limitations. Mechanical evidence can reveal missing records or changed files. It cannot certify that the Agent looked carefully or understood the image.
