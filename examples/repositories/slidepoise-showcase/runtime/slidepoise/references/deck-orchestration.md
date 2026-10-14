# Deck orchestration

## One model for every scope

A presentation is an ordered set of one or more slides. The Agent infers the requested scope from conversation. There is no user-facing single-page or multi-page mode switch.

## Deck outline

`work/deck-outline.json` is the live narrative contract. Start from `schemas/deck-outline.example.json`. Its `slides` array is the current order. Each slide has a stable ID that does not depend on its position.

The outline records

- presentation audience, purpose, and central throughline
- shared evidence, brand, style, and asset obligations
- active slide order
- each slide's role, communication job, dominant message, content obligations, evidence and asset obligations
- dependencies on earlier or later slides
- disposition such as active or omitted

Establish whether the deck must stand on its own or accompanies a presenter, and plan explanatory depth accordingly. Across the ordered slides, check what the reader already knows, what each page adds and whether its evidence warrants the next conclusion. Shared evidence must keep the same meaning and qualifications when reused. Repeating an uncertain claim on several pages does not strengthen its support.

Do not store detailed visual coordinates in the outline.

Keep the outline's content categories independent of slide layout. Compare possible visual approaches using `visual-exploration.md` before assigning page workers a composition. Do not turn provisional choices such as equal columns, no logos or a particular table into inherited requirements. Pass their rationale and remaining freedom when a reasoned choice is useful.

## Shared visual decisions

Before independent page production, author `work/deck-design.json` from the user's requirements, Profile, references and communication needs. Use `schemas/deck-design.example.json` as a starting point. This is the Agent's shared design brief, not a template or an automatic consistency score.

Discover recurring visual functions from the planned communication, references and actual page images. Name roles freely from what the deck contains. Repeated words, matching IDs or an existing style token do not by themselves establish peerhood. Different words and page-local object names can serve the same function. A changing series label, caption, source line, section marker or folio can be a peer across pages even when the main compositions differ. No list of familiar roles is complete.

For each discovered role, record its purpose, the observed reason for grouping its members, a concrete `chosen_style`, `page_aliases` that identify its objects on each relevant page, and any explicit `exceptions` in `deck-design.json`. Choose family, native size and units, face or weight, italic treatment, tracking, color and alignment where relevant. Keep placement conventions distinct from type style. Empty generic advice such as "keep labels consistent" leaves the page worker without an applied decision. The example contains illustrative roles and values, not default fonts or an exhaustive inventory.

Revisit this inventory after generated candidates and again after actual PowerPoint renders. Use the contact sheet to notice repeated visual functions, then open the relevant pages at full resolution. Look specifically for recurring elements that nobody declared during planning. A repeated folio may appear under different entity names, and a font substituted during rendering may expose a difference absent from the original brief. Add the newly observed peers to the shared design and trace all affected pages. This is adaptive visual reasoning, with no fixed role classifier or completion state machine.

The resolved configuration owns the shared frame and physical canvas. The generated image owns only the substantive region. Header, footer, page numbers and master-frame rules are excluded from generation even when a style reference shows them. All workers use the same enabled frame heights and content offset. Never turn off the frame merely to make a generated image fit.

Generate a representative content page first when its visual language will guide other pages. Inspect it against the shared brief, refine the brief if necessary, and make its accepted substantive image available as a style reference when the user's source policy permits generated references. Carry its typography, colour and visual finish across pages without copying its layout into unrelated arguments. Rebuild affected generation requests after changing the shared design. A diagram and a financial table can use different layouts while retaining the same title scale, text hierarchy, rules and accent meanings.

Pass the same deck design into each generation request and read it during semantic mapping. Keep its identity and source hash with the page's inputs. This prevents the shared direction from becoming a parent-only note that page workers never consume.

Materialize each decision during semantic mapping. Resolve each page alias to actual entities, then write the chosen font, target size, face, tracking, color and other relevant properties into their `style_hint` values or explicit compatible config tokens. Resolve size units through the source-to-slide transform. Equal source-pixel values on different canvases do not guarantee equal native point sizes. Preserve logical allocations and source-ink windows separately. When content does not fit, the Agent chooses a suitable allocation, reflow, shared-role revision or explicit exception and checks the resulting image.

Record the source deck design and `recurring_role_bindings` in the reconstruction handoff. Bind a role to actual entity IDs, its local fitting group and a named exception when one applies. These are host-authored trace records. The current runtime does not discover roles or automatically apply that mapping. The semantic entity styles and resolved config drive compilation. Verify the compiled/native values and actual appearance after applying them, including any fit reduction or font substitution. A role declaration that never changes its page entities has not implemented the decision.

When a later review changes the shared design, preserve the earlier generation inputs and record the newer host decision as a revision. Do not rewrite historical call evidence to imply the model received that decision. Any further generation call consumes a newly compiled request. When revising retained historical targets, describe their actual canvas and provenance, including an original full-slide reference when applicable. Newly generated targets follow the current substantive-only canvas and inherited-frame policy.

## Page workspaces

Use this structure

```text
work/
  deck-outline.json
  deck-design.json
  resolved-config.json
  deck-resource-selection.json
  deck-scenes.json
  deck-review.json
slides/
  s01-cover/
    work/
    deliverables/
  s02-context/
    work/
    deliverables/
deliverables/
  presentation.pptx
```

Slide folders use stable IDs. Ordering comes only from `deck-outline.json` and `deck-scenes.json`.

## Revision behavior

When the deck changes, reason about dependency scope.

- Copy changes usually invalidate generation and downstream artifacts for that slide.
- Style changes may affect all slides or a named subset.
- Shared asset changes affect only slides that use the asset.
- Reordering usually preserves page-local artifacts, then triggers a sequence review and reassembly.
- Removing a slide preserves its folder and marks it omitted. Do not delete evidence automatically.
- Adding a slide creates a new stable ID and a new page workspace.
- Splitting or merging slides creates new IDs when the communication jobs genuinely change.

Update transitions, repeated content, references such as "as shown earlier", and speaker notes after structural edits.

## Parallel work

Independent slides may be processed concurrently when the host exposes subagents. The parent Agent owns deck structure, shared style, shared resources, ordering, cross-slide consistency, and final assembly. Each page worker owns only one assigned slide directory and returns findings plus artifact paths.

Parallelism is an optimization. If subagents are unavailable, the parent Agent may process pages sequentially. Do not block the deck merely because parallel execution is unavailable.

Give each worker the original task context, relevant source material or source paths, current resolved configuration, deck design, relevant accepted style reference and assigned content obligations. Identify which constraints come from the user and which choices are Agent proposals. Workers can challenge a missing asset or an unsupported exclusion and return a proposed upstream revision. A page assignment does not turn the parent's provisional resource decision into a user requirement. Workers resolve the supplied role aliases to their actual page entities and return those bindings, observed native values, proposed exceptions and newly discovered recurring candidates. The parent compares pages together and decides whether to revise the page, adjust the shared design or retain an intentional exception. Different local typography-group names do not excuse drift within one deck role. Per-page approval and successful local fitting do not establish cross-page consistency.

## Deck scene manifest

Author `work/deck-scenes.json` with a `slides` array in current presentation order. Each active entry contains `slide_id` and `scene`. `scene` may be an absolute path or a path relative to the manifest.

Optional presentation fields include title, company, language, display font, and body font. Every scene must use the same physical slide size. Run

```bash
python scripts/slidepoise_runtime.py render-deck \
  --manifest work/deck-scenes.json \
  --output deliverables/presentation.pptx
```

The runtime verifies structural compatibility and assembles the ordered deck. It does not judge the narrative or visual quality.

`render-deck` accepts only scenes compiled from measured SlidePoise reconstruction inputs. A missing OpenCV version or missing input hashes is an objective lineage failure. A custom direct PptxGenJS deck is outside the SlidePoise reconstruction path and must never be delivered as a SlidePoise result.

## Deck-level review

After assembly, read the original task and relevant source material again before inspecting the deck as a sequence. Check whether planning omitted something material, including subject identity, available evidence or an explanatory visual. Agreement between the plan and output cannot establish that the plan was sufficient. Use the source-first review in `multi-agent-review.md` when an independent reviewer is available. Check

- whether the opening earns attention and frames the question
- whether each slide adds a distinct piece of the argument
- whether evidence appears before the conclusions that depend on it
- whether visual identity stays coherent without repeating one layout
- whether density and pacing vary intentionally
- whether transitions and cross-references still work after edits
- whether the ending resolves the promised communication job

Use a contact sheet for overview and full-resolution renders for detailed inspection. The Agent owns the decision and records concrete observations in `work/deck-review.json`.

Perform a separate visual calibration of recurring roles. First scan all actual pages for visual functions that repeat, including small labels and marks outside the initially declared inventory. Then compare each discovered role through its page aliases. Inspect apparent size, face, weight, tracking, line rhythm, color, alignment and placement. Native object facts can expose the emitted family, point size or character spacing behind a visible difference, and full-resolution images establish how those values look. Check recurring geometric treatments and the inherited frame too. The Agent decides which elements are peers and which differences are intentional.

Record the discovered roles, the actual page/entity members compared, observed and chosen treatments, any drift, the applied correction and each intentional exception with its purpose. Reopen the affected renders and repeat the search for undeclared recurring elements after corrections. Bind the final pages and shared design in the review. A list of file hashes or a sentence saying the deck is coherent does not replace this reasoning. Mechanical summaries of explicit styles can assist inspection, but must never infer peers, choose a design, classify aesthetic similarity or issue a consistency verdict.

Use `slidepoise_runtime.py render-deck-preview` to render every page and an ordered contact sheet with one PDF conversion. Read `references/portable-artifacts.md` when preserving a case, creating a portable bundle, or reproducing a deck outside its authoring directory.
