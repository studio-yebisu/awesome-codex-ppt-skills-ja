# Topology and layout system

## Contents

1. Why topology exists
2. Role, relationship, topology, and layout
3. Selection sequence
4. Topology grammar
5. Layout metadata and safe slots
6. Deck-level rhythm
7. Reference-quality floor
8. Intent-specific topology patterns
9. Cross-runtime fidelity
10. Failure patterns

## 1. Why topology exists

A layout is not a decorative arrangement. It is a spatial explanation of a relationship. Select a topology before placing objects so that hierarchy, direction, comparison, causality, and evidence remain visible even when the copy is blurred.

Use the default registry in `assets/starter/layout-manifest.json`. Extend it only when the content relationship cannot be represented honestly by an existing entry.

## 2. Role, relationship, topology, and layout

Keep these layers distinct:

- **Role** describes what the slide does in the audience journey: cover, evidence, comparison, process, decision, and so on.
- **Relationship** describes what the audience must perceive: one dominant claim, before/after, rank, sequence, hierarchy, network, collection, or exact lookup.
- **Topology** describes the spatial logic: stage, split, spine, axis, matrix, stack, network, mosaic, field, or frame.
- **Layout** is a concrete topology instance with slots, density limits, media capacity, tone support, and fidelity expectations.
- **Style** controls type, color, imagery, surface, and furniture. Style must not change the relationship encoded by the topology.

Do not select a layout from its appearance or name alone. A beautiful pyramid is wrong when the items have no hierarchy. Four equal cards are wrong when one item causes the other three.

## 3. Selection sequence

For every slide:

1. State the slide job and claim.
2. Name the relationship the audience must perceive.
3. Choose the simplest topology that exposes that relationship.
4. Filter layouts by role, density, media count, editability, and target-runtime fidelity.
5. Check slot budgets before writing final copy.
6. Select tone and furniture as deck-rhythm decisions, not page decoration.
7. Record one focal object in `emphasis`.
8. Render and verify the topology at thumbnail and full size.

If no registered layout fits, use a `custom-*` layout ID and record `layout_rationale`. Preserve the same manifest fields so another runtime can understand the custom route.

## 4. Topology grammar

| Topology | Relationship made visible | Typical reading flow | Common error |
|---|---|---|---|
| `stage` | one dominant claim, number, decision, or object | focal entry → compact support | turning a weak point into an oversized slogan |
| `split` | claim/proof, current/target, option A/B | left → right or tension → resolution | presenting incomparable sides as peers |
| `spine` | sequence, timeline, roadmap, gates | along one explicit axis | arbitrary step order or decorative arrows |
| `axis` | rank, trend, variance, distribution | claim → scale → highlighted evidence | chart chosen for novelty instead of question |
| `matrix` | exact comparison or two-dimensional classification | headers → cells → emphasized intersection | excessive card grids with no real matrix |
| `stack` | hierarchy, layers, composition, priority | direction stated by labels | pyramid/stack where position has no meaning |
| `network` | ecosystem, dependency, feedback | anchor → connections → boundary | spaghetti lines and unlabeled edges |
| `mosaic` | curated range with one dominant item | dominant proof → supporting set | equal thumbnails too small to inspect |
| `field` | context, atmosphere, human or product presence | scene → restrained overlay | mood replacing evidence |
| `frame` | one artifact plus explanation | artifact → annotation → implication | full screenshot reduced below readable size |

Use a graph-layout engine for complex network topology. Use native shapes for simple flows. Create connectors before nodes so links remain behind labels.

### HTML topology primitives

The HTML starter ships a portable macro-composition contract:

```html
<div class="prada-composition">
  <div class="prada-region prada-region-copy" data-slot="copy">...</div>
  <div class="prada-region prada-region-visual" data-slot="visual">...</div>
</div>
```

The presenter already places `topology-*` and `layout-*` classes on the slide root. `deck.css` therefore gives stage, field, network, spine, axis, matrix, stack, mosaic, split, and frame different default macro silhouettes. Treat these rules as a spatial starting grammar, not finished art direction. Change proportions, ordering, surface, and focal mass to fit the chosen registered layout, but preserve the relationship encoded by its topology.

Do not claim topology variety by changing metadata alone. The live DOM should show a different macro relationship. Exhaustive reference fixtures are browser-audited for unique topology/layout/tone/density signatures and consecutive repetition.

## 5. Layout metadata and safe slots

Every reusable layout declares:

- compatible roles and relationships;
- required and optional slots;
- maximum media and item counts;
- supported density and tone;
- fidelity expectation: `native`, `native-preferred`, `mixed`, or `vector`;
- guardrails that prevent semantic misuse.

Slots are content budgets, not boxes that must all be filled. Empty optional slots are allowed. Adding an unregistered slot requires a custom layout or a manifest update; do not silently squeeze new content into furniture.

Use these copy budgets as defaults:

| Slot | Speaking | Hybrid | Reading |
|---|---:|---:|---:|
| Headline | 6–14 words | 8–18 words | 8–22 words |
| Support line | 8–20 words | 12–30 words | 20–45 words |
| Body per region | 0–35 words | 20–70 words | 45–110 words |
| Peer items | 2–5 | 3–7 | 4–10 |
| Primary media | 1 dominant | 1 dominant + detail | 1–3 with captions |

Shorten, split, or change topology before shrinking type.

## 6. Deck-level rhythm

Judge a deck as a sequence of silhouettes, not ten independent pages.

- Use at least five distinct topologies in a typical 10-slide deck when the content supports them.
- Do not repeat one topology more than twice consecutively without a deliberate rhetorical reason.
- In an exhaustive stress fixture, target at least 55 percent unique combined topology/layout/tone/density signatures; this is a regression floor, not a target for random variation.
- Use two or more meaningful tone shifts per 10 slides to mark chapters, tension, proof, or decision.
- Repeat anchors such as title logic, page marker, accent behavior, and source position.
- Vary the dominant visual mass: left, right, center, full field, axis, or sequence.
- Alternate compression and release. A dense evidence page should often be followed by synthesis, implication, or decision space.
- Reserve the strongest visual contrast for the opening, decisive proof, or close—not every slide.
- Keep card-grid slides below one quarter of the deck unless the content is truly modular.

Perform a thumbnail test: at roughly 12% scale, the deck should show coherent identity, clear chapter changes, and varied silhouettes. Perform a squint test: each slide should retain one obvious focal region before text is legible.

## 7. Reference-quality floor

Treat supplied visual references as a minimum bar for deliberateness, not as layouts to copy. A final deck must demonstrate:

1. a recognizable visual identity within the first two slides;
2. decisive scale contrast between display message and support copy;
3. one dominant focal object or region per slide;
4. meaningful dark/light/accent or media rhythm;
5. evidence, UI, work samples, or photography shown at inspectable scale;
6. layout variation tied to different relationships;
7. consistent crop, caption, page, and source behavior;
8. full-size legibility that promotional mosaics cannot prove;
9. no unresolved template placeholders or generic stock-business filler;
10. no imitation of a copyrighted marketplace composition or asset.

The visual floor is intent-relative. A scientific talk may be quieter than a creator portfolio, but its figures, hierarchy, and progression must be equally deliberate.

## 8. Intent-specific topology patterns

### Portfolio

Use `stage → mosaic → frame → split → metric/statement → decision-lock`. Give selected work full scale, then explain contribution, process, and outcome. Avoid biography/tool cards displacing the work.

### Work results

Use `stage → axis → split → frame → matrix → decision-lock`. Lead with the result and variance, explain causes and implications, then lock next actions and owners.

### Business proposal or sales

Use `stage → axis/metric → stack/process → split/frame → timeline → risk-control → decision-lock`. Make mechanism and bounded risk as visible as promise.

### Research or technical

Use `stage → advance-organizer/spine → frame/axis → comparison → limitation matrix → synthesis`. Preserve uncertainty and show actual evidence at readable scale.

### Teaching

Use `stage → advance organizer → progressive spine → example frame → comparison → practice/decision`. Reveal complexity progressively instead of displaying the entire model at once.

### Async report

Use more `matrix`, `axis`, `frame`, and appendix layouts, but retain focal hierarchy and section rhythm. Reading density is permission for useful detail, not a license for tiny type.

## 9. Cross-runtime fidelity

Keep topology independent from renderer implementation:

- native PPTX: preserve text, charts, tables, simple flows, and decision structures as editable objects;
- HTML: use a fixed stage and scale the whole canvas; never reflow slide internals responsively;
- HTML-to-PPTX: record which effects rasterize and inspect the PowerPoint round-trip;
- PDF: verify fonts, cropping, links, and page order;
- image-first: use only with explicit acceptance of lost editability and accessibility.

Source preview success is not final-runtime success. Capture exporter warnings and compare final-runtime renders against source renders.

## 10. Failure patterns

Reject or repair:

- topical title plus bullets as the default page;
- every slide built from rounded cards;
- a screenshot occupying less than the space required to read its important labels;
- a different decorative motif on every page;
- topology selected before the claim or evidence relationship;
- repeated dark hero pages with no pacing function;
- complex networks hand-positioned without edge and label checks;
- visual variety achieved by random layout selection;
- source citations, page furniture, or rails overlapping content;
- browser-only polish that breaks in PowerPoint export.
