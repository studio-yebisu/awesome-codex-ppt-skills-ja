# Page Audit Checklist

Use this checklist after compilation and before showing a changed page to the user. It turns visual review into an explicit audit rather than an informal glance.

The author completes this checklist in both review modes. When independent review is enabled, the reviewer repeats the relevant checks against the current rendered artifacts rather than relying on the author's receipt.

## Build Evidence

- [ ] Compile twice with the deck's intended engine.
- [ ] Reject LaTeX errors and relevant overfull boxes.
- [ ] Render every changed page at `180–220 dpi`.
- [ ] Render `400–600 dpi` local crops for dense or important junctions, multi-edge nodes, bends, labels, graph overlays, group-boundary entries, and tightly placed outermost children.
- [ ] Render the whole deck when a shared theme, font, macro, page number, or common asset changed.
- [ ] Confirm the PDF page count and the location of every inserted or removed page.

## Full-Frame Sweep

Inspect the complete page first, then inspect the top, bottom, left, and right edges at original detail.

- [ ] The title, section label, page number, rules, and footer occupy their intended bands.
- [ ] No title is crowded against the top edge or competing with the page number.
- [ ] Meaningful content stays inside the safe area.
- [ ] The page has a clear visual center and reading order.
- [ ] Empty space looks intentional rather than caused by a misplaced or undersized object.

## Containers and Text

Inspect every container individually, including the first and last card in each row.

- [ ] Every card has visible left, right, top, and bottom clearance from its parent group.
- [ ] The full rendered bounding boxes of the outermost children remain inside the parent group; inspect the first and last child rather than inferring containment from node centers or minimum widths.
- [ ] Peer cards use consistent padding, heights, title baselines, body starts, and corner-radius hierarchy.
- [ ] Text does not touch or visually merge with a border, separator, neighboring block, or page edge.
- [ ] No final line contains a single avoidable word, short fragment, or split technical term.
- [ ] Headings and important labels are not automatically hyphenated.
- [ ] Narrow prose is ragged-right; interword spacing is not stretched by justification.
- [ ] Paragraph leading and paragraph gaps are consistent within a slide and across comparable slides.
- [ ] A tag remains inside its card, contrasts with the card fill, and does not displace the title.

## Connector Trace

Trace every connector from source to target. Do not infer that a line is correct because the overall diagram looks plausible.

- [ ] The line visibly touches the intended source and target anchors.
- [ ] A side with one connector uses its visible midpoint; every offset port has a deliberate multi-edge reason.
- [ ] In local crops, the final segment, arrow shaft, and arrowhead are collinear and centered on the assigned port.
- [ ] The final segment approaches the target from a side appropriate to that anchor.
- [ ] No connector terminates in empty space, stops one or two pixels short, or disappears under a border.
- [ ] Lines avoid text, tags, nodes, group titles, and unrelated containers.
- [ ] Every group-boundary entry crosses outside the group label and its reserved title band.
- [ ] Shared junctions are deliberate; ambiguous intersections are rerouted or bridged.
- [ ] Orthogonal bends occupy named open corridors; terminal stubs are consistent and no short corrective jog remains.
- [ ] Primary, return, optional, and exceptional paths use the documented line vocabulary.
- [ ] Inline labels create a clean line break; adjacent labels have visible clearance from the path.
- [ ] Arrowheads are visible, consistently sized, and not crowded against a node or page edge.

## Graphs, Status, Formulas, and Charts

- [ ] A status label is unambiguously associated with its node by alignment, proximity, or a leader; it is not floating between several candidates.
- [ ] Current state is encoded without a dot sitting on the node border.
- [ ] Graph edges are drawn behind nodes and highlighted movement begins and ends at explicit node anchors.
- [ ] A highlight of an existing graph edge uses exactly the base edge's centerline; an offset stroke represents a genuinely different edge.
- [ ] Formula fonts match the active mathematical type system across the deck.
- [ ] Comparable formulas use consistent color, baseline spacing, and display size unless complexity requires a documented exception.
- [ ] Body text resumes with the intended family, weight, color, leading, and alignment after every formula.
- [ ] Axes, ticks, units, thresholds, direct labels, and annotations remain legible at slide scale.
- [ ] Direct labels cannot be mistaken for another line or data series.
- [ ] Diagrams, formulas, plots, captions, and prose encode the same facts and conditions.

## Feedback and Skill Update Loop

When a user identifies a defect:

1. Locate the rendered symptom and its source-level cause.
2. Inspect peer objects and every page that reuses the same macro or layout pattern.
3. Fix the shared cause when it is genuinely general; avoid accumulating one-off offsets.
4. Update the style or Skill guidance only when the failure changes a reusable decision or audit check.
5. Recompile and re-render every affected page; do not rely on source inspection alone.
6. Repeat this checklist and record the new evidence.

## Reusable Example Stress Test

When changing diagram primitives or review rules, test them on at least one realistically dense page. A useful stress page contains several of the following:

- two semantic groups;
- six or more nodes;
- more than one node shape;
- a decision;
- a return loop;
- an optional path;
- an artifact or checkpoint;
- both an inline and an adjacent edge label;
- a legend or short explanatory panel.

The stress page must remain readable. Complexity is evidence of robustness only when hierarchy and routing stay clear.

## Compact Audit Receipt

For a reusable package or multi-page delivery, keep a short receipt in task notes or `reviews/`:

| Pages | Build | Frame/text | Local crops / connectors | Math/data | Result |
| --- | --- | --- | --- | --- | --- |
| `2–4` | twice, 200 dpi | checked | traced | checked | pass / repair |

Record concrete repairs and re-rendered pages. Do not mark a page as passed merely because compilation succeeded.
