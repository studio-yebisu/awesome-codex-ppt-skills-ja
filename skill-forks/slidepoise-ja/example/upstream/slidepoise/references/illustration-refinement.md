# Selective illustration edits

Read `raster-composition.md` before selecting sources. A focused edit can give a small illustration more usable detail, repair a visible defect or separate artwork from the slide background for layering. Consider each meaningful illustration at its intended output size. Reuse the original when regeneration offers no material benefit. The host Agent chooses the source and owns its visual review.

## Prepare the source

Record `raster_decision.action` as `refine`, with a reason and `reviewed_by` set to `host_agent_visual_reasoning`. Set `background` to `transparent` when the asset needs a transparent backdrop. Otherwise use `preserve`, the default. Use `geometry_policy: agent_logical` for the registered source canvas. OpenCV still supplies visible bounds as evidence. Keep intrinsic lettering with its raster owner. Resolve occluding native presentation text through the clean-plate route before isolated editing.

Run `scripts/prepare_illustration_refinement.py` with the accepted image, semantic map and resolved config. It writes individual source crops, a manifest, a brief and review contact sheets. Send each selected source crop to the image editor separately. The contact sheets are for inspection, not a canvas the model must reproduce.

Preserve the source subject, intrinsic lettering, aspect ratio, position and margins. Initial slide generation still explores composition freely. These preservation constraints apply to editing artwork from a design already chosen.

## Request and verify transparency

Check the available host tool. Request an isolated PNG asset with actual transparent pixels outside the artwork. When the interface exposes a background parameter, explicitly select transparent output. Preserve depicted paper, photographic backgrounds and shadows that belong to the artwork. Transparent output does not mean every pale region should disappear.

A successful image call does not establish transparency. Inspect the file itself. An RGB image, an opaque RGBA image or a painted checkerboard fails the transparent-background requirement. True alpha is necessary, but it does not establish good edges or faithful artwork.

Register one returned asset with `scripts/extract_refined_illustrations.py`, supplying `--image`, `--manifest`, `--entity-id`, `--output-dir` and `--mapping`. For a manifest containing one item, the entity ID can be omitted. The tool preserves the full canvas and partial alpha. It rejects missing transparency, empty artwork and changed aspect ratios. If the model returned extra canvas, inspect it and explicitly supply `--crop X Y WIDTH HEIGHT`. Never crop automatically to visible alpha bounds, stretch the artwork or remove a painted checkerboard using colour thresholds.

Inspect the generated `.on-light.png` and `.on-dark.png` review images, then the asset on the intended slide background. These previews composite alpha into RGB. Raw transparent-image viewers can exaggerate almost invisible pixels and must not be the sole basis for rejecting edges. Check soft shadows, fringes, isolated speckles, lost pale paper, intrinsic lettering and subject changes. Then compare its placement in the actual PowerPoint render with the approved design. A valid file can still be visually unsuitable.

## Apply or retain

Use `scripts/apply_illustration_sources.py` for inspected, selected items. It binds the file and source canvas to the semantic entity. Measurement retains alpha bounds as evidence while placement uses the full registered canvas. The renderer preserves the PNG and its alpha. Changed files or source coordinates require fresh preparation and inspection.

When the edit fails, set `raster_decision.action` to `reuse_original` and record the reason. Measurement then uses the accepted-slide crop even if an earlier override remains in the authoring record. Make a focused retry when a changed request can address the failure. Repeated retries are not evidence of reliable host support. Keep the existing crop or composite route available so transparent generation never becomes a prerequisite for finishing a deck.

Clean plates retain their panel or full-slide coordinate system and use targeted editing. Do not send them through isolated illustration extraction. A transparent PNG remains a raster image whose position and size can be edited in PowerPoint. It does not make the image's internal strokes or lettering native objects.

## Generation route

The preparation command emits a `.request.json` and `.edit.txt` beside each source crop. Follow `image-generation.md` to route each request through the selected image tool or export it for manual generation. Preserve one source per edit. A provider must support image editing and genuine alpha output for transparent requests. If it cannot, keep a suitable original or agree on a different route with the user.
