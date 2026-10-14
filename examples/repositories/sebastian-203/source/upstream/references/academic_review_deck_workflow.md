# Academic Review Deck Workflow

## 1. Build The Source Map

Create a compact table before drafting slides:

| Source type | What to extract | Typical use |
| --- | --- | --- |
| Review draft or outline | Chapter logic, terminology, claim hierarchy | Slide structure and talk flow |
| Core papers | Methods, figures, formulas, experimental evidence | Technical support and citations |
| High-quality review papers | Section organization and academic phrasing | Structural reference, not heavy citation |
| PPT template | logo, margins, title size, page number style, table style | Visual consistency |
| Existing slides | reusable content, visual assets, known user preferences | Continuity |

Never write "based on the user's papers" or "according to the user's request" in a final academic artifact.

## 2. Convert Review Chapters Into A Talk

A strong academic talk usually does not mirror every chapter mechanically. Use a progression that teaches the technical dependency:

1. Context: why the research object matters.
2. Mechanism: what physical, biological, mathematical, or system principle governs it.
3. Structure: what design choices implement the mechanism.
4. Modeling: what variables, assumptions, equations, and approximations describe the system.
5. Control or method: how inputs are computed from states, constraints, and objectives.
6. Applications and outlook: where it works, what metrics matter, and what remains unsolved.

Merge repeated background, related work, and motivation pages. Expand modeling, control, or methods pages when they carry the intellectual weight of the review.

## 3. Slide Content Density

Use this structure for most academic content slides:

- Title: precise object and relation, not a vague theme.
- Core claim: one sentence under the title.
- Evidence: two to four bullets, a table, or annotated figure.
- Visual: one source figure, comparison table, model diagram, or controlled schematic.
- Note: short figure/formula/table explanation when needed.

Avoid slides that only list method names. For each method, specify at least one of:

- input state,
- output variable,
- governing equation,
- constraint,
- experimental scene,
- evaluation metric,
- failure mode.

## 4. Figure Strategy

Use four visual categories:

| Category | Use for | Rule |
| --- | --- | --- |
| Literature figure | real platform, apparatus, experiment, published result | keep source label visible or add caption |
| Redrawn academic figure | workflow, model logic, taxonomy, control architecture | labels must be controlled and readable |
| Editable PPT component | tables, matrices, comparison grids, callout logic | build with native shapes/text |
| Generated text-free schematic | missing structural scene or conceptual object | no embedded text; add labels in PPT |

If a figure is central to the argument, add a "read this figure" note that tells the audience what to look at first.

## 5. Verification Loop

Before final delivery:

1. Export every slide to PNG.
2. Inspect the contact sheet for page-level balance.
3. Inspect key slides at full resolution.
4. Search for process notes and banned phrases.
5. Check every key figure has a source or visual category.
6. Fix and re-export.

Typical high-risk pages:

- formula slides,
- dense comparison tables,
- literature image grids,
- generated schematics with labels,
- title slides with logos,
- application slides with multiple real-world photos.
