# SlidePoise page workflow

This page-local workflow is reusable inside a one-slide request or a larger deck. Paths below are relative to `slides/<slide-id>/` for a deck and relative to the run root for legacy one-slide runs.

## 1. Resolve intent

Author `work/slide-intent.json` from the corresponding entry in `work/deck-outline.json`. Capture the audience question, dominant message, exact content, semantic relationships, hierarchy, evidence and source obligations, required assets, exclusions, assumptions, and unresolved questions that affect this page.

Do not force a numbered process unless the information is sequential. Keep `information_structure` semantic. A list of content categories does not mandate columns, cards or table rows. Develop an Agent-proposed layout after resource inspection and visual exploration, then record it in `style_direction` with its reasoning. Preserve a layout the user actually requires.

Establish how the audience will encounter the slide. A page read without a presenter needs enough explanation to interpret its evidence. A spoken presentation may carry that explanation in speaker notes. Record this in the intent's optional `reading_context` when it affects the content. Infer it from the request when clear. Do not add a user-facing mode or a required approval.

For a claim supported by evidence, use the existing `evidence`, `assumptions` and `open_questions` to distinguish observations, estimates, inferences and unresolved conditions. Explain which part of the claim each material observation supports and where its support ends. Numbers need their units, population, period and comparison basis where relevant. If the evidence cannot sustain the proposed conclusion, narrow the conclusion or preserve the uncertainty. Never invent support to make a stronger slide.

Describe in `information_structure` and `semantic_relationships` what the audience should be able to compare, trace or infer. For example, a cost comparison needs comparable cost components and their contribution to the total. This specifies the explanatory work without prescribing a chart type, metaphor, container arrangement or coordinates. When a visual convention could overstate the evidence, capture the prohibited implication in `avoid`. Direction can imply causality, enclosure can imply ownership, and a status mark can imply verification. Each must have support in the intent.

Use `hierarchy` to give each content role a distinct purpose. A conclusion, its explanation, supporting evidence and a qualification should have appropriate emphasis. Remove repeated claims when editing is authorised, while preserving their substantive qualifications. Decide whether a closing implication adds anything to the title. There is no universal requirement for an action title, subtitle, dominant diagram or bottom takeaway. Dense content needs readable relationships and explanation, not an arbitrary word limit. For exact user wording, preserve it and resolve repetition through emphasis or an agreed revision.

When client-facing wording needs refinement, use the optional companion workflow in `content-refinement.md`. It preserves the message, user-selected baseline and layout while improving the copy. Do not infer that a request for a small wording change authorises a new content structure.

## 2. Resolve configuration and resources

Use the deck's resolved configuration and shared visual direction. Automatically retrieve indexed visual-reference candidates for this slide using its communication job, semantic relationships and role. Follow `reference-retrieval.md`, inspect the actual candidate pages, then select references for this page's purpose. Reusing a shared reference still requires a page-specific reason. Add icons, components, images and user assets where they help this slide.

Follow `resource-library.md` to compare concrete source assets and enabled library candidates against this page's purpose. Begin with the original task and source material, then assess the draft intent. The draft may omit a useful identity, example or piece of evidence. Amend it when source inspection reveals that omission. Keep unsupported design assumptions revisable. A library demonstration on one page does not establish that resource choices on other pages are sufficient, and an empty asset list does not require adding decoration.

Apply `visual-exploration.md` before settling the composition. Research useful identity and explanatory assets alongside references. Keep the explored options and selected visual argument in existing `selection_reasoning`. Check that `avoid` and `visual_obligations` have not turned an untested Agent preference into a restriction that closes the search.

For a deck, read the same `work/deck-design.json` used by the other pages. Its recurring visual roles are host-authored decisions. Preserve them during page work and return a proposed change to the deck owner when an exception is needed.

Resolve header and footer settings before preparing the generation context. The substantive canvas has the full slide width and the full height minus enabled header and footer heights. The header and footer are constructed later as inherited frame content. Do not put their wording, page numbers or rules in the page's visual obligations. A footer-like qualification that is essential to this page's argument remains substantive content and must have an explicit content role distinct from the shared frame.

Keep `work/reference-candidates.json` and its inspection sheet separate from the selected inputs. Copy the retrieval policy into `work/resource-selection.draft.json` and author the selected references and their specific lessons. Then run `scripts/prepare_resource_context.py`. The generated context sheet is an input to image generation and an optional review artifact for the user. It is not an approval token.

When a selected visual reference needs readable typography or fine detail, set its `full_resolution_attachment` to `true` to attach its canonical image with a verified hash after the context sheet, in selection order, even under `full_context_sheet`. The default is `false`, and this reference choice is independent of canonical asset attachment policy.

## 3. Prepare and generate the slide image

Run `scripts/prepare_generation.py` to compile the resolved canvas, profile guidance, intent, resources, shared deck design and generation budget into the contract, brief and `work/generation-request.json`.

Follow `image-generation.md` to discover the configured tool or export a manual exchange. Pass the compiled prompt unchanged with its ordered reference images. Save the actual call and returned image reference when the host exposes them. If no suitable tool is available, offer manual generation or help connect one.

Generate a substantive-region candidate from the selected visual approach. Inspect what its spatial relationships, assets and emphasis help the reader understand, as well as its content, frame exclusion and aspect ratio. A complete, tidy page can still be a weak visual explanation. If the structure merely distributes paragraphs or the first idea obscures the message, explore another composition. Use a focused edit for local defects. Compare recurring visual roles with the shared deck direction without forcing identical structures. Update the upstream inputs and recompile when changing generation instructions. Additional candidates should resolve a real design question within the authorised generation budget.

Compare generated wording against the authored content as well as reading it for the intended audience. An authorised native-copy correction that preserves the accepted composition can follow `content-refinement.md` without another image-generation call. Record the difference and carry the revised copy into semantic mapping and native reconstruction.

If feedback rejects a reference source or visual direction, return to resource selection. Preserve the rejected pass, apply the stated exclusions, and revise affected shared guidance and requests before another generation call.

For a focused candidate edit, record the corrections from Agent review or user feedback in `work/image-edit-changes.txt`. Run `python scripts/prepare_image_edit.py --generation-request work/generation-request.json --candidate work/candidate.png --changes work/image-edit-changes.txt --output work/image-edit-request.json`. The request retains the verified substantive canvas, shared design and reference images, binds the candidate pixels and corrections, and applies the generation host's prompt capacity without truncation. Immediately before calling the image capability, run `python scripts/prepare_image_edit.py --verify-request work/image-edit-request.json`, then pass its prompt unchanged with its ordered reference images. The first image is the candidate to edit. Agent review can initiate this correction without a separate user request. A change to source intent or shared design requires recompiling the generation request first. Inspect the returned image before accepting it.

Never repair a wrong aspect ratio by stretching the target. If a model adds removable frame content or returns a different canvas, the Agent may define a crop after inspecting it and use `scripts/normalize_generation_canvas.py` to fit that crop without distortion. Otherwise regenerate. Review the resulting image again before mapping semantics.

Show the image when the user asked to review slides, when their feedback would prevent material rework, or when the result is useful progress to share. A fully automatic request authorizes the Agent to continue after its own review.

Freeze the selected target as `accepted-slide.png`. Here, accepted means selected by the Agent or user for reconstruction. It does not imply a mandatory user gate.

Compare available candidates together and revisit the deck's role inventory. Identify repeated visual functions that emerged in generation, including peripheral labels, captions and series markers that were absent from the initial brief. Give their page-local aliases and chosen treatment to the deck owner before independent reconstruction carries the drift forward.

## 4. Map semantics

Inspect the selected target and author `work/semantic-map.json` plus `work/reconstruction-handoff.json`.

Before populating the map, read the intent and inspect the target to write the handoff's `content_obligations`. Include the claims, data, qualifications and directed relationships the slide must preserve. Then bind each obligation to its emitting entities. Do not derive this inventory from the map itself, since that would preserve its omissions. Check that the generated target satisfies the intent as well. A deficient target needs an upstream correction.

Map meaningful PowerPoint-level entities, logical text regions, text hierarchy, icon slots, canonical assets, connector semantics, and raster-source classes. Every emitting entity has an explicit geometry policy and z layer. Keep semantic role separate from visual style role.

Read the current `deck-design.json` and resolve its recurring roles to the page's actual entities. Apply the chosen styles to `style_hint` or explicit compatible config tokens, and retain `recurring_role_bindings` with the source design in the handoff. Role bindings describe the decision and its recipients. They do not apply styles automatically. A local fitting group describes that page's fitting scope and cannot establish consistency with another page. Report newly discovered peers and any proposed exception to the deck owner.

Run `scripts/collect_semantic_evidence.py` to collect objective structural facts. The Agent consumes the evidence and owns the semantic decision.

## 5. Resolve raster sources

Inspect novel illustrations and textured regions at intended output size. Follow `illustration-refinement.md` to regenerate selected small illustrations at higher resolution or obtain transparent image layers when useful. Review actual alpha-composited previews and retain adequate originals when a new generation adds no benefit. Ask the user only when the extra call, identity change, or visual tradeoff needs their decision.

A refined raster changes its pixel source only. Register the returned canvas against the original logical box, retain transparent margins and preserve the selected substantive-region composition. Native text, charts, connectors and exact user assets retain their reconstruction routes.

## 6. Measure

Run OpenCV measurement with the active semantic map. The Agent inspects the target and overlay, chooses ownership, and authors any geometry corrections. No script discovers visual peers or chooses an aesthetic alignment.

Use the packaged command below for the deterministic reconstruction stages. It always runs OpenCV measurement before it builds the reconstruction contract and constructor scene.

```bash
python scripts/slidepoise_runtime.py reconstruct-slide \
  --image work/accepted-slide.png \
  --semantic-map work/semantic-map.json \
  --upstream-handoff work/reconstruction-handoff.json \
  --config ../../work/resolved-config.json \
  --slide-id <stable-slide-id> \
  --output-dir work/reconstruction
```

Inspect `work/reconstruction/measurement/debug_overlay.png` against the accepted target. If semantic ownership or geometry needs correction, update the semantic map and run the same command again. The authoritative outputs are `measurement/slide_entities.json`, `reconstruction-contract.json`, and `constructor-scene.json`.

## 7. Reconstruct

Build the reconstruction contract from the measured scene and resolved config. Compile one constructor scene for the slide. Restore exact assets, fit declared typography groups, reconstruct native objects, preserve meaningful raster regions, and bind connectors to their semantic owners.

The packaged command above performs these deterministic build steps. Do not replace them with a custom direct PowerPoint construction script.

## 8. Render and review

Render the page or assembled deck and compare the reconstructed slide with its selected target. Inspect fidelity, hierarchy, asset treatment, text fitting, connector routing, collisions, density, whitespace, and editability.

Open the `rendered_text.path` returned by the preview command. It reports native table words from the actual PDF. Inspect each discrepancy in the page image, including whole words split across lines. Check text outside tables visually as well. Zero reported discrepancies covers only the cells the collector examined. When extraction is unavailable, inspect those cells directly and record the limitation.

Use the configured content crop for target comparison and the whole slide for frame review. Header and footer text, rules and page-number fields must come from the shared inherited frame. They must not be duplicated as image content or page-local substitutes.

Keep cross-page typographic peers at the deck's chosen size and treatment. Inspect native style facts and the actual images for every discovered role, including small recurring labels or marks. Revisit the inventory for undeclared peers after rendering. If a member no longer fits, the Agent should reconsider its allocation, wording, line breaks or shared role scale while preserving the message. Do not silently shrink that member and call the role consistent. An exception is possible when the Agent records its actual members, chosen treatment and purpose, then visually reviews it across the deck.

Fix objective runtime defects directly. For a visual issue, decide whether the correction belongs in the semantic map, measurement interpretation, generated target, or deck outline. Do not add arbitrary final coordinates to generic runtime code.

Record concrete findings before editing. After a correction, rerun the affected reconstruction and preview, inspect the cited region at full resolution, and check the whole page for regressions. Recheck its recurring roles across the deck when a shared treatment changes. Carry findings through to their observed resolution. A successful command or an updated file hash does not close a visual finding.

Before delivery, run `scripts/collect_release_evidence.py --help` and collect the page's release facts with the exact inspected PowerPoint and render. Keep the render's `.source.json` sidecar. For a page rendered from the assembled deck, pass its one-based `--slide-number`. Resolve stale or mismatched provenance by rendering the current file again. Do not recreate a sidecar to make an older image appear current.

## 9. Return to deck orchestration

Return the page scene path and current artifact bindings to the deck owner. A page worker writes only its assigned page directory. The parent Agent updates the shared `work/deck-scenes.json`, assembles active slides in outline order and performs the deck-level sequence review described in `deck-orchestration.md`. A sequential host performs both responsibilities itself.
