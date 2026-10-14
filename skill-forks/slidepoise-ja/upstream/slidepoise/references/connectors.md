# Connector reasoning and rendering

A connector communicates a semantic relationship. The host Agent chooses its meaning and family; deterministic code only binds that intent to exact geometry.

## Certified families
- `direct_flow`: simple directed relation, straight whenever endpoint sides and clearance allow.
- `orthogonal_dependency`: directed relation that needs an orthogonal route for a clear approach.
- `merge_split`: multiple semantic sources and/or targets sharing one semantic routing junction.
- `grouping_bracket`: non-directional grouping expressed with a square bracket.
- `grouping_brace`: non-directional grouping expressed with a curved brace.
- `annotation_leader`: one annotation pointing to one referenced semantic owner.

Do not use a directional arrow when the intent is merely grouping. Do not use a bracket/brace to imply process direction.

## Host-Agent connector contract
For each connector, first compare the generated connection against the intended semantic relationship. Raster topology is not authoritative. If the generated image connects the wrong owners, correct the semantic owners/family here instead of preserving the mistake or moving other objects. Set `semantic_topology_verified: true` in `connector_intent`. Missing confirmation appears in semantic evidence and must be resolved by the reasoning review.

For each connector author:
- source owner(s) and target owner(s);
- directed or non-directed intent;
- explicit `arrowhead_treatment` using `none`, `triangle_at_target`, or `open_arrow_at_target` to preserve the observed endpoint;
- optional `visual_constraints.arrowhead` with `powerpoint_size` or separate `powerpoint_width` and `powerpoint_length`, each `sm`, `med` or `lg`, when the native endpoint needs a page-specific size;
- connector family;
- source/target attachment side for every endpoint;
- attachment fraction (0..1) along every selected side;
- `grouping_side` for bracket/brace families;
- `junction_hint` for every shared merge or split, authored after visual review;
- `junction_style` (`none` or `filled_circle`) and optional `junction_diameter_px` only when the rendered junction itself carries visible meaning;
- `grouping_depth_px` for every brace or bracket, measured and confirmed by the Agent;
- `visual_route_reviewed: true` only after inspecting the route visually;
- `visual_route_decision` stating why the selected path is clear;
- optional `visual_route_review_artifact` pointing to the inspected overlay or comparison;
- `route_mode=minimal_orthogonal` when the Agent delegates least-bend compilation after reviewing the corridor;
- `route_mode=authored_waypoints` with `route_waypoints_px` when an obstacle or semantic corridor needs a deliberate detour;
- `route_mode=authored_geometry` for grouping braces and brackets.

The parent container is an endpoint only when the relationship semantically belongs to the whole parent.

## Deterministic geometry
After semantic binding, the runtime recomputes endpoint ports from the frozen owner geometry, selected side, and fraction. Generated raster endpoints and paths are evidence only. This lets native connectors correct a wrong generated connection or route without moving the connected content.

For ordinary directional routes, the runtime offers a least-bend orthogonal candidate compatible with endpoint axes. The Agent may author waypoints after visual inspection. Arrowhead orientation is determined by the final segment into the target. Two-point paths emit native line connectors with explicit direction. Paths with additional points emit one continuous editable freeform because LibreOffice can reroute custom geometry stored as a connector. The compiled scene records each path in `source_path_representations` and `target_path_representations`. A freeform retains the semantic relationship and authored route through regeneration. It does not automatically attach when an owner is moved in Office. State the actual representation in handoff and review evidence. For grouping braces and brackets, an Agent-authored depth may preserve a visually meaningful target. Otherwise use the configured generic depth.

Native arrowhead dimensions are relative to stroke width. Judge the head together with the visible shaft, especially in short gaps. Per-connector dimensions override the profile default. Pixel length and width measurements remain evidence, not promises of exact native dimensions. Export must preserve the selected native dimensions and must not enlarge every arrow automatically.

## Visual route review
After rendering, the host Agent inspects every connector. Revise the semantic connector intent and rerun if it starts/ends at the wrong owner, points the wrong way, has an unnecessary bend, crosses important content, is occluded, has a confusing merge/split, or uses the wrong family. Do not hand-edit final route coordinates and do not move content merely to accommodate a bad raster connector.

Read paths end to end at the delivered slide size. A visible arrowhead does not establish a readable connection. Labels masking most of a shaft can leave disconnected stubs. Opposite-direction paths need distinguishable routes or another faithful treatment of the two directions. Place labels beside their routes when that makes continuity clearer. Do not cure crowding by adding oversized heads or more line segments.

Inspect `visual_review_facts.connector_text_intersections` in constructor evidence. It reports crossings of allocated text boxes, including intentional line labels. Decide whether each crossing preserves continuity and meaning from the actual render. These facts do not automatically reject a design or authorize rerouting.
