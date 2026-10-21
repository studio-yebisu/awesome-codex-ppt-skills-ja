# Render, Inspect, Repair, and Present

Visual review is part of slide production, not an optional final polish.

## 1. Compile and Render

- Compile with the engine expected by the deck; use XeLaTeX by default for mixed Latin/CJK Beamer decks.
- Compile twice so references, dimensions, and remembered TikZ positions stabilize.
- Treat LaTeX errors and relevant overfull boxes as failures.
- Render every changed page to PNG at `180–220 dpi`. Render the whole deck when shared theme, macros, page numbering, or common assets changed.
- Inspect the rendered image at original detail. A fit-to-window thumbnail can hide collisions of a few pixels.
- For dense diagrams or visually important objects, render `400–600 dpi` crops around every decision, multi-connector node, route bend cluster, edge label, highlighted overlay, group-boundary entry, and tightly placed outermost child. Inspect those crops at original pixels and record them in the audit receipt.

The helper script performs the mechanical part:

```bash
scripts/render_and_check.sh deck.tex rendered
scripts/render_and_check.sh deck.tex rendered 4 7
scripts/render_pdf_crop.sh deck.pdf 3 /tmp/review/gate 500 900 260 900 620
```

Use [page-audit-checklist.md](page-audit-checklist.md) while inspecting the rendered pages. For a reusable package, preserve a compact audit receipt rather than relying on memory.

## 2. Inspect Each Page

Check the full page first, then zoom into dense regions.

### Page frame

- title, page number, header rule, and footer rule use consistent positions;
- no meaningful element sits outside the safe area;
- the content has a clear visual center and reading order.

### Text and containers

- every text block remains inside its container with visible clearance on all sides;
- multiline text does not touch the bottom edge or end in a clipped line;
- title-to-body, paragraph-to-paragraph, and text-to-separator distances are deliberate and consistent;
- separators do not overlap titles or paragraphs and have whitespace above and below;
- line breaks are natural, especially for long identifiers, mixed-language names, and numbers with units;
- short prose and narrow panels are ragged-right rather than stretched by full justification; headings are not automatically hyphenated;
- peer cards share padding, title baselines, body starts, and row gaps;
- the first and last card in a group have visible group padding and do not sit flush against the group boundary;
- the complete rendered bounds of the leftmost, rightmost, topmost, and bottommost children remain inside the parent group with visible clearance;
- no label relies on manual spaces for alignment.
- body text uses the intended weight and family; title-local `\bfseries`, `\itshape`, color, alignment, and font changes do not leak into later text.
- avoidable one-word final lines, heading hyphenation, split technical terms, and stretched interword spacing have been removed.

### Diagrams and lines

- arrows begin and end at sensible sides of nodes;
- every connector has been traced individually from a visible source anchor to a visible target anchor;
- each arrow uses an explicit side anchor or port, and that connection area is not occupied by a tag, status marker, or other edge;
- a side used by one connector is entered or exited at its visible midpoint; offset ports are reserved for deliberate multi-edge separation;
- the final segment and arrowhead are collinear, centered on the assigned port, and free of one- or two-pixel lateral offsets;
- orthogonal bends lie on deliberate open corridors, with consistent terminal stubs and no arbitrary corrective jogs;
- lines do not pass through text, boxes, headings, labels, or unrelated regions;
- lines that enter a group avoid the group label and its reserved title band;
- arrowheads are neither oversized nor hidden under a node;
- node fills hide ordinary graph edges cleanly; highlighted arrows do not begin inside a node or scrape its outline;
- a highlighted version of an existing graph edge uses the same centerline as the base edge; separate geometry is used only for genuinely parallel edges;
- role tags remain fully inside their cards, have consistent padding, stay visibly distinct from the card fill, and do not compete with the main node title;
- status markers do not sit on node borders or resemble connection ports;
- status labels are aligned closely enough to identify one node without ambiguity;
- inline edge labels create a deliberate break in a straight line, while adjacent labels remain visibly separated from curved or crowded paths;
- loops and optional paths remain distinguishable from the main flow;
- grouped areas have enough internal padding and do not collide with their group labels.

### Images and data graphics

- the image is sharp and not stretched;
- important labels are readable at slide scale;
- multi-series charts use direct labels or a clear legend without label-to-series ambiguity;
- captions and legends do not compete with the graphic;
- cropping removes accidental whitespace without cutting labels or strokes.

### Content consistency

- repeated numbers, units, labels, and category names agree across text, tables, and plots;
- formulas use the intended math font and comparable displays retain consistent color and vertical rhythm;
- a diagram and its formula encode the same structure;
- captions and interpretations do not claim more than the displayed evidence supports;
- illustrative or synthetic data is identified clearly and consistently.

### Language quality

- the title states the slide's question, object, decision, or finding without vague importance claims;
- body text supports the title instead of repeating it or announcing what the slide will show;
- facts, numbers, units, conditions, sources, and uncertainty survive editing;
- headings and cards reflect real distinctions rather than a forced group or mechanically symmetric wording;
- the wording sounds natural when read aloud in the presentation language;
- English, Chinese, and mixed-language text follows [slide-text.md](slide-text.md).

## 3. Repair in the Right Order

For text overflow or crowding:

1. shorten or rewrite the text without changing meaning;
2. remove duplication and move secondary detail to speaker notes or another slide;
3. change the card, column, or row allocation;
4. increase container height or split the page;
5. reduce font size only as a last resort, while respecting the active style package's minimum.

For title/body or separator collisions:

1. set explicit node padding and anchors;
2. separate title and body into distinct vertical positions;
3. define one shared spacing value for peer cards;
4. move or remove the separator if it does not add meaning.

For connector problems:

1. connect from explicit side anchors;
2. reroute through open corridors;
3. move labels to empty edge segments;
4. simplify or split the diagram if clean routing remains impossible.

## 4. Re-render After Every Geometry Change

Do not assume a coordinate edit solved the problem. Recompile and inspect the affected page again. Changes to text, font size, node padding, image dimensions, or line routes all require a new render. Recreate the relevant local crops after a connector, node, or overlay changes; an old crop is not evidence for new geometry.

## 5. Author Review Gate

The author may mark a draft ready only after:

- every changed page has been rendered and inspected;
- all basic overlap, overflow, proximity, alignment, spacing, and connector defects are fixed;
- the PDF page count and changed-page placement are correct;
- editable source, PDF, and page previews are available.

If the user selected `self-review only`, the author may now present the draft. State that the delivery received author self-review only.

If the user selected `self-review + independent reviewer`, meeting this gate starts the reviewer handoff; it does not authorize delivery. Follow [reviewer-workflow.md](reviewer-workflow.md) and present the draft only after the reviewer returns `PASS` or identifies a decision that requires the user.

Human review should focus on message, emphasis, terminology, and preferences—not on defects that visual inspection could have caught first.

When the user requests revisions, translate the feedback into a general cause before editing. For example, “the text touches the box” may require better padding across all peer cards, not a one-off coordinate shift. Reinspect the whole affected group after the fix.

Also inspect every page that shares the changed theme or macro. Update the Skill or style guide when the feedback exposes a reusable decision or missing audit check; do not turn an isolated preference into a universal rule.
