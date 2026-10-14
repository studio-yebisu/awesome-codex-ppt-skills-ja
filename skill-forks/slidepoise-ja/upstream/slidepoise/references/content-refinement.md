# Optional content refinement

Use this workflow when the user asks for better client-facing content, when a consulting deliverable needs a content review, or when authorised wording must be improved without changing the design. Use the available `consulting-content` skill for its reader and meaning judgement. If unavailable, apply the existing user-language contract and task context. Its absence does not block ordinary slide work.

## Ownership

The companion skill proposes copy and identifies ambiguities. SlidePoise owns the slide composition, resource selection, geometry, text fitting, reconstruction and final render review. Preserve the user's latest designated deck and firm template. Do not restore old generated headers or footers over user-supplied frame elements.

Keep this optional. Exact-copy reproduction and already approved copy do not need compulsory rewriting. Source research remains a separate task when the user has deferred it.

## Before image generation

Put the intended wording into the existing slide intent, with exact strings for approved text. Keep content roles identifiable so later edits can refer to a specific title, explanation or label. Pass the complete intent through `prepare_generation.py`.

The compiled brief already asks the image model to preserve exact wording, facts and qualifications. This instruction does not guarantee the model's output. Do not delegate factual claims or final editorial decisions to the image model merely because it can render text.

## After image generation

Inspect both the visual design and the content. Compare the generated text to the authored strings, then read the actual words from the intended reader's perspective. Attractive layout does not excuse unclear or altered meaning.

For an authorised copy-only correction that fits the existing slots, keep the selected image as the composition reference. Record the affected entity, original text, revised text, reason and preserved meaning in the working handoff or a linked copy-revision record. Preserve the original image and generation request as evidence of what was generated.

Update the intent's wording and the handoff's independent content obligations. Use the semantic entity's `authored_text` for the revised native text and keep its source text accurate to the observed image. Do not invent a new field in a strict schema. Keep geometry, typography groups, font targets, assets and visual relationships stable. Re-run the packaged measurement, reconstruction and rendering stages for the affected slide.

The comparison now checks two explicit things. The accepted image governs the design. The recorded revised copy governs the authorised native wording. Do not treat that recorded text difference as an unexplained reconstruction defect or refresh old hashes to imply the image contained it.

If the correction changes the argument, data, required content, visual relationships or composition, revisit the affected upstream decisions. If text is inseparable from raster artwork, use the normal image-edit or reconstruction workflow. The native-copy exception is not a route around the reconstruction contract.

## Existing editable PowerPoint

When a user supplies a newer native file, it supersedes older constructor scenes for subsequent edits. Inspect the supplied slide, preserve its frame and design, and record its baseline. Apply authorised changes to the identified native text objects through the supported editing path. This does not authorise a custom replacement deck builder or re-creation of the whole slide.

The companion should keep approximately the same wording footprint. If revised copy no longer fits, first rephrase while retaining the meaning. Do not silently reduce font size or move the layout. Surface the specific conflict if a meaningful fit needs a new design choice.

## Verification

Render and inspect the edited slide for comprehension, line wrapping, peer balance, clipping and metric associations. Check that the intended objects alone changed. A fitting report or matching word count is supporting evidence, not proof of layout preservation. When only wording suggestions are requested, return the copy without editing the presentation.
