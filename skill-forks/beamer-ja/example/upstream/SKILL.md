---
name: build-beamer-slides
description: Design, implement, render, and visually review polished Beamer slides. Use for a new deck, a single slide, slide-by-slide collaboration, layout repair, or a user-defined visual style; use the bundled restrained light style by default and leave deck-level narrative order to the user unless they ask for help with it.
---

# Build Beamer Slides

Create Beamer slides that are concise, coherent, and ready for human content review only after basic layout defects have been removed.

## Preserve User Control

- Follow the user's requested working mode: build the whole deck, prepare a selected group of slides, or discuss and implement one slide at a time.
- Treat the user's content scope, slide order, and narrative emphasis as authoritative. Suggest alternatives when helpful, but do not silently restructure the deck.
- Keep domain content separate from this skill's design rules. Inspect the user's actual sources before drafting factual slide content.
- Use plain, formal language. Avoid vague business jargon, inflated claims, and unexplained abbreviations unless the audience requires them.

## Choose the Review Mode

- Before substantial slide implementation begins, ask whether the user wants an independent reviewer subagent after the author's self-review. Do not start that implementation until the user answers. Do not ask again when the user has already chosen a mode for the current deck or revision task.
- Explain the tradeoff plainly: an independent reviewer usually provides a stronger visual audit, but uses additional time and tokens. Offer two choices: `self-review only` and `self-review + independent reviewer`.
- The author review is mandatory in both modes. Enabling an independent reviewer strengthens the review; it never replaces compilation, rendering, screenshot inspection, repair, or the draft-ready gate performed by the author.
- If the user selects independent review, read and follow [references/reviewer-workflow.md](references/reviewer-workflow.md). Use a separate read-only subagent when delegation is available. If no independent subagent can be created, disclose that before implementation and ask whether to continue with self-review only or wait.
- If the user selects self-review only, complete the normal render-and-repair loop and deliver directly after the draft-ready gate. State in the delivery that independent review was not requested.

A concise opening question is sufficient:

> Would you like an independent reviewer subagent after my self-review? It can catch additional visual defects, but it uses more time and tokens. Without it, I will deliver after the mandatory self-review.

## Select the Visual Style

- Preserve an existing deck's established style unless the user requests a change.
- When the user supplies a style, reference deck, screenshot, brand guide, palette, typography, or layout preference, read [references/custom-style.md](references/custom-style.md) and derive an explicit style contract before substantial implementation.
- Otherwise use the bundled [restrained light style](styles/light/STYLE.md). When no project template exists, start from [styles/light/template-169.tex](styles/light/template-169.tex).
- Use the optional [Warm Editorial style](styles/warm-editorial/STYLE.md) when the user requests a warmer academic or mathematical visual identity. It is built in but is not the default.
- Use the optional [Slate Violet Light style](styles/slate-violet/STYLE.md) when the user wants a quiet technical light theme with a gray-violet primary color. It preserves the default light hierarchy while giving architecture and planning decks a distinct identity.
- A one-off user preference belongs to the current deck. Create or update a reusable package under `styles/<style-name>/` only when the user explicitly asks to preserve that style for later use.
- A custom style may change palette, typography, page chrome, shapes, density, imagery, and motion conventions. It may not remove the review loop, safe-area discipline, legibility requirements, or draft-ready gate.

## Read the Relevant Guidance

- Read [references/diagram-design.md](references/diagram-design.md) when a slide contains a flowchart, architecture diagram, dependency graph, timeline, or other structured visual.
- Read [references/slide-text.md](references/slide-text.md) before drafting or revising English, Chinese, or mixed-language slide text.
- Read [references/review-loop.md](references/review-loop.md) before presenting any draft to the user. This review is mandatory for every changed page.
- Use [references/page-audit-checklist.md](references/page-audit-checklist.md) during the rendered-page review. Trace every connector and inspect every container edge; do not substitute a general impression for the checklist.
- Read [references/reviewer-workflow.md](references/reviewer-workflow.md) only when the user enables independent review.
- Read [references/example-gallery.md](references/example-gallery.md) when a user asks for examples, when a tested layout pattern would materially reduce rework, or when forward-testing a change to this skill or a style package.
- Read only the active style package; do not load unrelated styles.

## Per-Slide Workflow

1. Define the slide's single main message, the evidence or objects that support it, and the visual form best suited to that relationship.
2. Inspect the existing deck, nearby slides, active style package, reusable assets, fonts, colors, and page geometry. Reuse established patterns rather than rebuilding them inconsistently.
3. Select a layout before writing detailed text. Reserve space for the title, main visual, explanation, legends, and page number; estimate multiline wrapping before placing nodes.
4. Draft concise content using the slide-text guide. Preserve facts and qualifications, give each text region one job, and split a slide when shortening would remove necessary meaning.
5. Implement with stable geometry: explicit widths, consistent inner padding, aligned anchors, and reusable styles or macros.
6. Compile twice, render every changed page at high resolution, and visually inspect it using the mandatory review loop and page-audit checklist. For dense diagrams, also render `400–600 dpi` local crops around decisions, multi-edge nodes, bends, labels, highlighted overlays, group-boundary entries, and tightly placed outermost children.
7. Record which pages were inspected and any repairs made. For reusable packages or multi-page deliveries, keep a compact audit receipt in task notes or `reviews/`.
8. Revise and re-render until the page satisfies the draft-ready gate. The author must complete this step before any reviewer handoff.
9. If independent review is enabled, hand the review-ready artifacts to the reviewer, repair supported findings, re-render, and return the updated artifacts to the same reviewer until it passes or identifies a decision only the user can make. If independent review is disabled, show the draft to the user after step 8.

## Draft-Ready Gate

Do not present a human-review draft while any basic defect remains:

- text exceeds or nearly touches its container, page edge, title band, or footer;
- a peer card is flush with its parent group or lacks visibly balanced group padding, even if it remains technically inside the group;
- an outermost child node's rendered bounding box extends beyond its parent group or lacks visible clearance on the side facing the group boundary;
- multiline text has an implausible line break, clipped final line, or insufficient bottom clearance;
- a heading is hyphenated, a technical term is split, or an avoidable one-word final line remains;
- a title, paragraph, separator, rule, label, or neighboring block overlaps or has visibly inconsistent spacing;
- cards in the same group use inconsistent padding, heights, baselines, column starts, or row gaps without a semantic reason;
- arrows, lines, arrowheads, legends, or graph edges cross text, enter boxes at awkward points, extend beyond their region, or appear disproportionately heavy;
- a connector crosses a group label or its reserved title band when an open boundary entry is available;
- a connector does not visibly meet both intended anchors, approaches the target from the wrong side, or terminates in empty space;
- a single connector misses the geometric midpoint of its assigned side, its arrowhead is not collinear with the final segment, or an offset port lacks a clear multi-edge reason;
- an orthogonal route contains an arbitrary short jog, an uneven terminal stub, or a bend outside a deliberate clear corridor;
- two strokes that represent the same graph edge or route use different geometry instead of a shared centerline;
- a status marker sits on a node border, a role tag disappears into its card fill or competes with the node title, or several connectors share a corner without a deliberate port plan;
- an edge label touches a stroke, bend, arrowhead, or node; an inline label does not create a clean line break; or a curved/crowded path uses an inline label where an adjacent label would be clearer;
- fonts are reduced to compensate for content that should be shortened, reflowed, or split;
- a body paragraph unintentionally inherits bold, italic, color, alignment, or font-family state from a preceding title or formula;
- a status label is not clearly associated with one node, or formulas and body leading change inconsistently across comparable pages;
- a diagram is technically inside the page but too small or dense to communicate its intended relationship;
- a diagram, formula, table, label, or explanatory statement contradicts another representation of the same content;
- slide text relies on vague importance claims, meta narration, repeated title content, forced symmetry, or generic closing language instead of the available evidence;
- compilation reports a relevant error or overfull box.

Automated compilation checks are necessary but never replace screenshot inspection. Whole-page inspection is also insufficient for dense connection geometry: inspect local crops at original pixels before passing the page. When a shared macro or style changes, review every page that uses it, not only the page that exposed the defect.

## Delivery

Provide the editable `.tex` source, compiled PDF, and previews of the changed pages. State which pages were rendered and inspected, which review mode the user selected, and, when enabled, the independent review result. Disclose any remaining limitation that requires the user's content decision.

Use `scripts/render_and_check.sh` for the standard XeLaTeX workflow when its dependencies are available:

```bash
scripts/render_and_check.sh path/to/deck.tex path/to/rendered [first-page] [last-page]
```

Use `scripts/render_pdf_crop.sh` after the full-page render when a dense or important region needs pixel-level review.
