# Diagram and Flowchart Design

Use diagrams to explain relationships that are harder to understand in prose. Do not turn every list into a flowchart.

## Start with the Semantic Structure

Before drawing, write a compact inventory:

- entry and exit states;
- major stages or layers;
- decisions and their outcomes;
- repeated loops;
- optional paths;
- external actors or agents;
- artifacts passed between stages.

Decide what belongs in the overview and what belongs on detail slides. A useful deck pattern is:

1. one system-level overview with major transitions;
2. one detail slide for each dense subsystem;
3. shared colors and terminology between overview and detail views.

Do not place every internal action on the overview.

## Geometry

- Establish a grid before placing nodes. Use consistent column centers, row baselines, card dimensions, and group padding.
- Group related steps inside pale containers. A group label belongs in a stable title band or above the group with enough clearance.
- Reserve the group-label band as connector-free space. A line entering a group must cross the group boundary outside the rendered label extent, not through or immediately beside the label.
- Check containment using each child's rendered bounding box, not its declared `minimum width`. Long text and node padding can make the actual node wider than expected; the leftmost and rightmost children still need visible parent-group clearance.
- Keep node text short. Put explanatory prose beside or below the diagram, not inside every box.
- Size a node for its rendered multiline text, including top and bottom padding. Check long agent names and mixed English/CJK labels explicitly.
- Use a limited shape vocabulary. Rounded rectangles for actions, diamonds only for genuine branching decisions, low-height capsules for terminal or committed states, and small badges for role or status information are usually enough.

## Shape and Internal Hierarchy

- Use three visual levels rather than treating every rectangle alike:
  1. a pale, large-radius group container for a subsystem or phase;
  2. a white or lightly tinted rounded card for one action, agent, or artifact;
  3. a small capsule tag inside the card for a role such as `Agent`, `Worker`, `Reviewer`, `Input`, or `Optional`.
- Keep role tags near the upper-left of a left-aligned card. Keep the main name or action on the next baseline, followed by at most one short muted description. Centered text is appropriate for compact state nodes; agent cards and prose-bearing actions are usually easier to scan left-aligned.
- Use corner radii consistently by level. A group should have a visibly larger radius than its inner cards; a tag may be fully pill-shaped. Do not mix sharp rectangles, unrelated circle sizes, and several capsule styles without semantic reasons.
- A tag is a secondary identifier, not decoration. Its fill should be paler than the main accent and its text should remain readable without competing with the node title.
- Prefer changing a node's fill, outline, or a separated tag to show the current state. Do not place a status dot directly on the node border: it can be mistaken for a connection port and will collide with edges that meet the same outline.
- When a small external status marker is necessary, keep a visible gap between it and the node outline and do not place it in the angular sector used by incoming or outgoing connectors.

## Ports and Drawing Order

- For a dense diagram, write a small connection inventory before drawing: `source.port -> target.port`, line class, label mode, and routing corridor. This prevents accidental shared ports and makes the rendered connector audit concrete.
- Assign each connection to an explicit side anchor or named port before drawing the path. Main left-to-right flow normally uses `east` to `west`; vertical progress uses `south` to `north`; returns should use a different side or an outer corridor.
- A node with one connector on a side should use that side's geometric midpoint. Offset ports are for multiple connections on the same side; place them symmetrically or define named coordinates and record why the offset is necessary.
- The final segment should meet a rectangular or capsule border approximately perpendicular to that border. The shaft and arrowhead must share one centerline; a visible micro-kink at the endpoint is a failure.
- Reserve a connector-free corner for tags, state markers, or annotations. A card should not have a tag, arrowhead, and status marker clustered at the same corner.
- Draw background groups first, ordinary connectors second, nodes third, and intentional foreground annotations last. This lets card fills hide graph edges cleanly while keeping arrowheads and labels visible.
- For graphs, draw undirected edges before node circles. Start a highlighted movement arrow at an explicit node anchor rather than at an approximate coordinate inside or on top of the circle.
- When a colored stroke highlights an existing graph edge, derive both strokes from the same node-center pair. Draw the base edge behind the nodes, then draw the shortened overlay on the identical centerline. Different anchors imply a different edge and must not be used merely to keep both colors visible.
- Position node-specific tags relative to the named node, not by an unrelated absolute page coordinate. Centered proximity or a short leader should make the association unambiguous.

## Connections

- Route lines from explicit side anchors or ports. Choose the side that follows the reading direction.
- Prefer short orthogonal paths with deliberate bends, or gently curved paths for a single highlighted movement. Avoid diagonal lines through dense areas.
- Put orthogonal bends on a small routing grid or a named open corridor. Keep terminal stubs visibly consistent; remove short corrective jogs and bends that exist only because earlier coordinates were approximate.
- Keep connectors outside text and outside unrelated containers. A line that merely passes behind pale fill still looks like a collision.
- Treat each group-boundary crossing as a routed entry point. Move the child, change the port, or use a deliberate open corridor when a direct segment would cross the group title band.
- Leave clearance between a connector and a box before the arrowhead. Keep arrowheads small relative to text and node size.
- Use approximately `0.6–0.9 pt` for primary connectors and lighter or dashed strokes for optional or planned paths. Give connectors rounded caps and joins; keep arrowheads small and identical within one semantic class.
- Use one line vocabulary consistently: solid dark for the main progression, solid muted accent for callbacks or evidence returns, dashed gray for optional/planned paths, and a restrained dash pattern for maintenance or exceptional operations. Do not use thickness alone to encode an unrelated state.
- Draw feedback loops around the outside of the main flow. Label the loop near an empty segment, never on top of another edge.
- If two lines must cross, reroute first. If crossing is unavoidable, use a visible bridge or a clearly different layer; do not leave an ambiguous intersection.
- Do not use arrow length or thickness as decoration. Every line should have a clear source, target, and meaning.

## Labels and Legends

- Place edge labels only after the route is stable. Never place text at a bend, immediately before an arrowhead, over a node border, or between two closely parallel paths.
- Use an **inline knockout label** when a short branch value or transition name is essential to following one straight, isolated segment. Give the label an opaque background matching the local canvas and enough horizontal padding so the line visibly stops before the text and resumes after it.
- Use an **adjacent label** when the text describes a path rather than names a branch, when the path is curved, when the label is longer than two or three short words, or when several paths run nearby. Offset it consistently above or beside an open segment; do not let it touch the stroke.
- Keep labels horizontal when possible.
- Use the same terms, colors, and line styles across overview and detail slides.
- Explain solid, dashed, status, and node-color semantics once in a compact legend. Remove the legend when the distinctions are already obvious from nearby text.

## External Diagram Assets

- SVG is appropriate for complex reusable diagrams; TikZ is appropriate when geometry is tightly integrated with Beamer.
- Keep the asset's internal page title, page number, and explanatory sidebar out of the diagram file. Let Beamer own slide-level chrome.
- Export SVG to PDF for XeLaTeX when direct SVG support is not configured.
- Inspect the exported PDF or PNG, not only the source SVG. Font substitution, clipping, marker size, and bounding boxes can change during conversion.

## Repair Order for a Crowded Diagram

1. Remove nonessential text and duplicate labels.
2. Separate overview and detail content.
3. Rebalance columns, groups, and node sizes.
4. Reroute edges from explicit side anchors.
5. Increase whitespace and container padding.
6. Reduce font size only after the preceding options are exhausted.

## Diagram Review Questions

- Can every node type be identified from shape and hierarchy without relying on color alone?
- Does every connector meet a deliberate port, and is that port free of tags and status markers?
- For each single-edge side, is the endpoint at the visible midpoint? If not, is the offset intentional, symmetric, and recorded in the connection inventory?
- At every endpoint crop, are the last segment, arrow shaft, and arrowhead collinear and centered on the assigned port?
- Do overlaid base and highlight strokes share exactly the same center-to-center geometry?
- Are callbacks and optional paths visually distinct from the primary flow without becoming heavier?
- Does every inline label create a clean, centered break in its line? Does every adjacent label have visible clearance?
- Would removing a decorative marker, line, or box make the relationship easier to read? If so, remove it.
