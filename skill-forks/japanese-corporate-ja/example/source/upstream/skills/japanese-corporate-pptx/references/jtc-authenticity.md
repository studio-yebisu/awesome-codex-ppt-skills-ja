# JTC Authenticity

This reference describes the structural signals of Japanese committee, ministry, industry-association, and large-company working slides.

## Four structural layers

- Document control: material number, meeting, date, version, status, and responsible unit.
- Decision structure: issue, evidence, response, owner, due date, gate, and unresolved point.
- Evidence texture: source excerpts, captions, page references, definitions, units, and processing notes.
- Exception handling: scope, assumptions, exclusions, dependencies, uncertainty, and conditions.

## Industry-association pattern

- Saturated blue rail and compact branded footer.
- Technology timeline, layer model, or imported market chart.
- Named technologies and companies placed directly on the model.
- Several sources, notes, and a specific industry implication.
- Page number and document classification.

## Ministry or public-program pattern

- Document or agenda number in the upper-right.
- Purpose, target, program content, scheme, outcome, responsible division, and fiscal year.
- Red processing note when a source figure has actually been modified.
- Explicit eligibility, exclusions, reporting, and audit conditions.
- Source organization, document title, page, and publication date.

## Large-manufacturer working-paper pattern

- Issue-and-response table, current or future process, or phased roadmap.
- Owners, deadlines, decision gates, and status.
- Factual boxes, diagrams, photos, and chart excerpts mixed on one page.
- `要確認`, `継続審議`, or `本日決定` tied to a real item.
- Operational constraints, interfaces, and dependencies.

## Controls by slide type

| Slide type | Relevant control |
|---|---|
| Timeline | source date, current-point marker, forecast boundary, uncertainty note |
| Layer model | scope boundary, layer definition, dependency, highlighted control point |
| Ecosystem | arrow legend, contract/data/money distinction, governance note |
| Policy scheme | material number, responsible unit, fiscal year, target requirements, exclusions |
| Process | owner lane, decision diamond, system/data foundation, bottleneck, handoff condition |
| Roadmap | owner, evidence required at each gate, dependency, revision condition |
| Data page | unit, period, actual/forecast distinction, source page, processing note |
| Source excerpt | bounded crop, red focus box, caption, source, `一部加工` or `抜粋` note |
| Issue table | fact, response, owner, due date, status, decision, continuing discussion |

## Red markup

Red is reserved for the current point, material risk, exception, source-processing note, decision, verification item, or unresolved issue. Each red box or arrow makes the requested focus explicit.

## Controlled variation

A reusable layout library may include several document families. Within a single delivered deck, chrome stays consistent unless the source deck already varies.

Useful variation includes content-specific figure composition, denser citation zones, working-paper material numbers, status, and accent colors with defined meanings.

Random typeface changes, arbitrary line widths, accidental spacing differences, and unexplained footer changes are not authenticity.

## Scorecard

Score each applicable item from 0 to 2:

- dominant model matches the real reference;
- document control is sufficient;
- actors, flows, and responsibility are explicit;
- evidence is traceable;
- assumptions and exceptions are visible;
- red markup points to a real issue;
- decision or next action is closed;
- compact text has a defined role;
- the page remains editable;
- the page is readable at full-size inspection.

Interpretation:

- `17–20`: convincing working document;
- `13–16`: usable but still template-like;
- `9–12`: generic corporate slide;
- `<9`: redesign before delivery.

Clipping, ambiguous arrows, invented evidence, or unresolved production notes remain hard failures regardless of score.
