# Independent Reviewer Workflow

Use this workflow only when the user enables `self-review + independent reviewer`. The reviewer adds a separate visual audit after the author has completed the mandatory self-review.

## Responsibilities

### Author

- designs and implements the slides;
- compiles twice and resolves relevant build diagnostics;
- renders and inspects every changed page;
- creates high-resolution local crops for dense or important geometry;
- repairs all defects found during self-review;
- prepares the exact artifacts and scope for review;
- evaluates reviewer findings, makes supported repairs, and regenerates the evidence.

The author must reach the draft-ready gate before requesting review. Do not use the reviewer as a substitute for unfinished layout work or as the first person to open the rendered pages.

### Reviewer

- works in a separate read-only subagent context when available;
- does not edit the source or redesign the narrative;
- examines the compiled PDF, full-page renders, and required local crops at original detail;
- checks the user request, active style, render-review guide, and page-audit checklist;
- traces every connector on diagram pages and inspects every container boundary;
- reports concrete findings with page, region, severity, visible evidence, and the violated requirement;
- returns `PASS` only when no basic visual defect or unresolved requirement remains.

The reviewer may inspect TeX to identify a likely cause, but source inspection is not visual evidence. It must not approve a page without examining the current render.

## Review Handoff

Give the reviewer only the material needed to perform an independent check:

- the user's current requirements and the chosen style;
- the exact changed-page list and any shared theme or macro affected;
- the current `.tex` source and compiled PDF;
- full-page renders for every page in scope;
- `400–600 dpi` crops for decisions, multi-edge nodes, bends, labels, overlays, group entries, and tightly placed outermost children;
- [review-loop.md](review-loop.md) and [page-audit-checklist.md](page-audit-checklist.md).

Do not tell the reviewer that the result is expected to pass or provide a list limited to the author's suspected weak points. The reviewer should inspect the complete agreed scope.

## Findings and Repair

The reviewer should return findings first, ordered by severity. Each finding should identify:

1. the page and visible region;
2. the defect or inconsistency;
3. the rendered evidence;
4. the relevant checklist or user requirement;
5. whether the finding blocks delivery.

The author then checks each finding against the source and user intent. Repair supported findings without transferring edit ownership to the reviewer. If a suggestion changes the user's content, narrative, or style preference rather than fixing a defect, present that choice to the user instead of applying it silently.

After every repair:

1. compile again twice;
2. render every affected page;
3. recreate affected local crops;
4. inspect the repair and its neighboring elements;
5. inspect every page that shares a changed theme, macro, or component;
6. send the exact updated artifacts to the same reviewer.

Repeat focused repair and re-review until the reviewer returns `PASS` or the remaining issue requires a user decision. After a repair that changes shared geometry or style, require a final pass over the complete affected page set rather than only the original finding.

## Delivery

When the reviewer passes, report the reviewed pages and the final result with the editable source, PDF, and previews. Do not expose internal reviewer conversation as presentation content.

If independent review cannot finish because a required user decision remains, show the decision and its visible consequence to the user. Do not describe the deck as reviewer-approved until the reviewer has checked the resulting artifacts.
