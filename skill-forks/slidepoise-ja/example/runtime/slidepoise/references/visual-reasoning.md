# Visual reasoning authority

A visual question must be answered by looking at the relevant image. Never infer visual acceptance from a score, threshold, object count, file existence, or geometry script.

For collage, intrinsic lettering, texture, and image-text overlaps, read `raster-composition.md`. Inspect both intended output scale and relevant details. Reviews must include actual observations and SHA-256 bindings for every inspected artifact. Measurement review binds the accepted image, active semantic map, measured scene, and overlay. Reconstruction review binds the accepted image, constructor scene, PPTX, and persisted render. A changed file invalidates its old review. These checks establish evidence freshness only.

## Generation review
Start with a reading of the actual slide before rereading its intent or the author's explanation. State briefly what the intended audience could understand from the page alone. For a journey or use case, identify whose situation is being shown, what they need, why another participant acts and what changes for each participant. Record missing context as a finding. Internal stage labels and chronology do not establish that context. If the explanation depends on facts remembered from the brief, revise the page's information structure before judging its polish.

Inspect the candidate image itself. Judge:
- the conclusion a reader would draw from the image and whether the evidence supports it, including uncertainty that could be concealed by a checkmark, arrow, grouping, colour or visual metaphor;
- whether the intended comparison, dependency or other relationship is visible, with values attached unambiguously to the evidence they describe and comparable quantities using a consistent basis;
- whether each text role adds useful information, emphasis follows its importance and repeated conclusions compete for attention;
- whether the page supplies the explanation its reading context needs, preserving material evidence without confusing visual weight with information volume;
- fidelity to the resolved profile hard rules and exact design config;
- typography family/role use, content completeness, and text colour treatment;
- whole-page density and whitespace balance relative to the resolved density profile;
- whether large blank regions are intentional and support hierarchy/pacing/emphasis or instead indicate weak, lopsided space use;
- whether exact/user assets have plausible, aspect-compatible slots;
- whether icons use a coherent profile-approved foreground/background family rather than arbitrary badges or mixed styles;
- whether gradients, charts, tables, and photography follow the selected profile when present;
- factual/asset fidelity and overall professional quality;
- whether any model-created illustrative raster is semantically justified by the active profile/slide role rather than decorative filler. Do not reject a useful novel illustration merely because it is not a packaged asset when the profile permits it; classify it explicitly downstream instead.

Reject material defects before reconstruction. Density does not override profile principles and a profile does not imply one density.

When a page fails these readings, identify whether the source claim, explanatory relationship, text hierarchy or generated treatment caused the problem. Revise the corresponding intent or shared guidance and compile again before another generation call. A palette change cannot repair an unsupported conclusion. Keep this judgement in the existing generation review, with the observed issue and correction. Do not introduce a separate score or aesthetic gate.

## Measurement review
Inspect the accepted image and OpenCV overlay together. Judge whether meaningful objects are mapped once at the right semantic level, logical text regions and parent ownership are correct, and typography groups reflect the actual content hierarchy. Every emitting entity must declare whether its logical Agent-authored box or its OpenCV visible box controls reconstruction through `geometry_policy`. It must also have an explicit `z` layer. Every meaningful textbox must have a `typography_group` and an Agent-authored `target_font_size_px`. Boxes at one content level share the same group and target size. The Agent must justify different groups for similarly named roles in distinct visual hierarchies. Every meaningful icon or icon slot must also have an `icon_treatment_group` and an observed `icon_inset_fraction`. Icons at one visual level share one explicit profile treatment. Also judge whether other peer groups are defensible, canonical asset slots are correct, rounded-container intent and observed radius reflect the visible shape, declared non-overlap pairs match the intended layout, and connector intent matches what the diagram should communicate. For every connector, explicitly verify semantic topology and choose its route mode, arrowhead treatment, and junction style. Correct generated misconnections in the semantic intent instead of copying the raster mistake.

For a user-facing explainability artifact, give entities and groups concise `display_label` values. Give groups a meaningful `semantic_class`, children, and a short reason. Give relationships a readable `display_label`, explicit type, and endpoints. `scripts/make_semantic_explanation_overlay.py` may render these Agent-authored facts as solid entity boxes, dashed semantic groups with labels beneath them, and named relationship arrows. It does not discover groups or relationships. Keep raw IDs and step-debug terminology out of the presentation-facing overlay.

For icons, verify the reserved logical slot separately from the designed background surface. A faint generation-only slot boundary may exist solely for localization. Do not map that scaffold as a real background surface unless the accepted design clearly intends it as visible content. When a real surface exists, record its fill/shape/stroke faithfully and verify that the treatment is profile-compatible. If the icon is visually supposed to sit directly on a larger colored panel/card, prefer a transparent icon background and treat any small white box/border around the glyph as scaffold rather than as a real surface.

OpenCV may reveal pixel evidence. It cannot decide semantic ownership, visual peers, typography groups, icon treatment groups, shape intent, profile fidelity, density quality, or whether a layout looks right.


## Reconstruction review

An optical alignment pass is required for every reconstructed slide before acceptance. Compare the accepted target and actual PowerPoint content crop at the same scale, first as a whole and then by substantive region. Inspect visible text ink, shared baselines, apparent artwork centres, visual mass and surrounding gaps. Judge the intended relationships between peers and preserve deliberate asymmetry. Matching boxes, numerical centring or successful text fitting cannot establish optical alignment. Inspect the full-slide render for alignment with the inherited frame as well.

When a rendered offset disrupts an intended relationship, follow `reconstruction.md` to correct it within the accepted composition. Re-render and inspect the affected region and its neighbours. Record the concrete alignment observations in the existing reconstruction review, including any mismatch, affected entities, correction and observed result. If no correction is needed, describe the visible relationships that support that judgement. The host Agent owns this decision without an automatic alignment score or threshold.

Inspect the accepted target beside the generation-region crop of the reconstructed render, and inspect the full-slide render separately for the master frame. Judge:
- foreground/background colour fidelity and profile compliance;
- typography hierarchy, exact font-size equality within every declared `typography_group`, wrapping, readability, and prohibited treatments such as accidental italics;
- icon/pictogram treatment coherence within every declared `icon_treatment_group`, including black-versus-gradient normalization and slot-surface consistency;
- local/global alignment and spacing;
- icon identity, centering, scale, aspect ratio, glyph colour/gradient, and optional surface treatment;
- whether any generation-only slot scaffold or unintended white knockout tile was accidentally reconstructed;
- whether any independent content elements overlap or crowd each other;
- whether ordinary cards have faithful mild corner rounding rather than exaggerated PowerPoint preset rounding;
- connector meaning, source/target ownership, endpoint placement, direction, bend necessity, junction clarity, occlusion, and family choice;
- chart/table palette and typography when editable data visualisation is present;
- gradient fidelity when a profile gradient is present, including whether a raster/canonical region was used instead of inventing unsupported stops;
- Slide Master header/footer height, content, alignment, and slide number;
- shape geometry, z-order, raster use, whole-page density/whitespace balance, and professional finish;
- for novel illustrations, whether the chosen original/refined raster remains aspect-correct and visually clean within its intended region, preserves its registered canvas and internal placement, and retains the intended optical alignment after any authorised local offset.

If an issue requires visual judgement, record it in the host-Agent review artifact. Deterministic scripts may enforce an explicit resulting constraint but may not create or substitute the judgement.

## Compare the content, then the treatment

Before mapping, read the slide intent beside the generated image. Inventory the claims, evidence, qualifications and relationships that must survive. Carry that inventory independently in `reconstruction-handoff.json` as `content_obligations`. Bind each obligation to its semantic entity IDs. A directed relationship also binds its connector ID, source owners, target owners and direction. A caption alone does not fulfil a relationship. The constructor checks these explicit bindings. It cannot discover an obligation the host omitted.

During reconstruction review, compare every substantive region at the same scale. Record concrete differences in emphasis, alignment, typography, geometry and meaning. Review the actual table cells, chart labels and connector paths, including secondary feedback routes. Separate intentional profile or canonical-asset substitutions from unintended loss. A shared role does not authorize smaller unrelated content or a different local layout. Retain the target's hierarchy and optical footprint when normalizing peers.

If a generated connector is malformed, use the intended owners to correct it and record the exact change. If the intended relationship is unclear, return to the plan. Never discard a path because its generated geometry looks strange.

## Review records are observations

Write a new review only after opening the current persisted images. A change invalidates the affected review. Keep the previous record as history or leave its old hashes intact until inspection. Never refresh hashes under unchanged acceptance prose, run a script that reproduces fixed acceptance statements, or infer review from the successful reproduction of a previous deck. Hash checks establish which files a record describes. They cannot establish whether its observations are true.

Review helpers may produce comparison images, crops, object inventories and blank finding forms. They must not prefill an acceptance decision or favourable observations. Record each material finding, the upstream change that addresses it, and the inspected result. Preserve any remaining limitation accurately.

`render-deck-preview` also writes `rendered-text-evidence.json` when Poppler text extraction is available. It compares each native table cell with the complete words rendered inside that cell's PDF coordinates. Inspect reported discrepancies such as a source word rendered as two fragments. A matching word in a different cell does not conceal the discrepancy. Extraction evidence does not replace visual inspection, and unusual scripts or ligatures may need direct review.
