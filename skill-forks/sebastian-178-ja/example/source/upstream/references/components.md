# Component Catalog

Components are composable blocks used inside layout templates. Pick components after choosing the layout and before choosing the final theme.

Components should be structure-first:

- Do not bake theme-specific colors, image choices, decorative effects, or brand marks into component selection.
- Use semantic classes and theme tokens only. Themes decide color, emphasis, dark/light mode, and visual effects.
- Images belong in user content, `assets/media/`, or showcase/full-deck examples, not generic component rules.
- If a component needs highlighting, use structural states such as `.is-active`, `.is-focus`, or `.highlight`; the theme decides how that state looks.
- Insert components only inside bounded slide slots: `.content`, `.region-body`, `.safe-fill`, or `.safe-stack`.
- If a component does not fit inside its slot at 16:9, reduce rows/labels, use a wider layout, or split the content across slides.

When adding a component, read `references/adding-patterns.md` first. A component is agent-ready only when it has a snippet, semantic CSS, sufficiency rules, data-router guidance when relevant, quality-check coverage when it represents evidence, and a 16:9 fit validation inside a bounded layout.

For complex variants, read `references/content-to-exhibit-router.md` before choosing the exhibit and `references/component-variant-router.md` before choosing snippets. They define when to use each chart, table, conceptual, architecture, workshop, workplan, and people variant, and repeat the rule that titles, legends, axes, and group labels must come from the user's material.

## Selection Rules

Use the component catalog actively. Before authoring HTML, map each planned body slide to at least one component, one evidence shape, one evidence source, and one fallback if the evidence is insufficient. Do not default to prose cards when the source has numeric or tabular evidence.

Components are not decoration. Each component must prove a claim, compare alternatives, show movement over time, expose risk, clarify a decision, or structure qualitative reasoning.

- Numeric section data should become `metric-strip`, `line-chart`, `combo-chart`, `small-multiples-chart`, `column-chart`, `ranked-bars`, `chart-bars`, `stacked-bars`, `paired-bars`, `likert-bars`, `waterfall-bridge`, `stacked-waterfall-bridge`, `tornado-bars`, `distribution-plot`, `cohort-retention-grid`, `variance-bridge-table`, `table`, `comparison-table`, `checkmark-bar-table`, `sensitivity-grid`, `heatmap`, `range-comparison-plot`, `competency-gap-range-table`, or `dot-scale-comparison`.
- Peer/company/industry comparisons should become `comparison-table`, `weighted-scorecard`, `ranked-bars`, `column-chart`, `quadrant-matrix`, `range-comparison-plot`, or `heatmap`.
- Ordered or phased content should become `timeline`, `phase-roadmap`, `milestone-track`, `process-flow`, `stage-gate`, `vertical-process-takeaway`, `process-deep-dive`, `cascading-flow`, `cycle-flow`, `step-explanation-strip`, or `gantt-workplan`.
- Qualification logic should become `funnel-steps`, `filter-cascade`, `screen-filter-grid`, or `decision-flowchart`.
- Root-cause logic should become `fishbone-cause-effect` when several cause categories explain one effect.
- Decisions and recommendations should become `option-funnel-scorecard`, `tradeoff-frontier`, `scenario-comparison-table`, `assumption-register-table`, `weighted-scorecard`, `decision-log`, `pros-cons-table`, `outcome-support`, or `callout` paired with evidence.
- Portfolio, initiative, or market-option choices should become `portfolio-prioritization-matrix`, `weighted-scorecard`, `quadrant-matrix`, or `comparison-table` depending on whether the evidence is directional, scored, or tabular.
- Governance, RACI, or operating cadence records should become `raci-governance-grid`, `decision-log`, `comparison-table`, or `dense-list` depending on whether roles and cadence are explicit.
- Architecture records should become `system-context-map`, `dependency-map`, `sequence-interaction-flow`, `architecture-option-comparison`, `input-process-output-layers`, or `swimlane-process-map` depending on whether the source describes context, dependency, interaction sequence, or option tradeoff.
- Workshop records should become `agenda-table`, `phase-meeting-plan`, `workshop-breakout-synthesis`, `decision-capture-board`, `stakeholder-map`, or `decision-log` depending on whether the source describes agenda, breakout output, decisions, stakeholder alignment, or action tracking.

Evidence shape router:

- Numeric: use metrics, charts, ranked bars, ranges, heatmaps, or tables only when values and labels are present.
- Categorical: use cards, catalog grids, bars, heatmaps, or tables depending on whether categories are prose, scored, or measured.
- Comparison: use comparison tables, weighted scorecards, split-even pages, ranked bars, quadrant matrices, dot-scale comparisons, or range plots.
- Time: use timelines for dated events, phase roadmaps for implementation, milestone tracks for status, horizon bands or horizon curves for uncertainty and ambition, journey maps, journey arcs, or journey waves for stakeholder progression, stair-step timelines for maturity buildup, calendar workplans for short-cycle day/week plans, schedule lists for timed sessions, and Gantt workplans for workstreams over time.
- Risk: use risk matrix register when placement and actions matter; use decision log, pros-cons, callout, or table when only prose risk records exist.
- Decision: use outcome-support, decision-log, comparison-table, compass-choice, pros-cons, or callout paired with evidence.
- Portfolio: use portfolio-prioritization-matrix when options can be mapped by strategic value and feasibility; use weighted-scorecard when criteria are explicit.
- Governance: use raci-governance-grid when decisions, roles, forums, and cadence are known; use decision-log when only asks/status are known.
- Qualitative: use outcome-support, framework-map, `issue-tree`, `iceberg-model`, `capability-coverage-map`, cause-effect, from-to, numbered-list-grid, dense-list, conversion-list, story-block-list, icon-outcome-grid, or callout.

Fallback rule: if the evidence shape lacks required fields, switch to the simpler qualitative component named in the slide plan or omit the page. Do not invent the missing values to keep a specialized component.

## Variant Assembly

Choose the component family first, then assemble the variant from the data shape. Snippets are starting points, not fixed outputs.

- Record count controls density: few records can use compact cards; many records need grids, tables, or split pages.
- Group labels control structure: use the user's labels for section titles, legends, sidebars, and axes instead of keeping demo copy.
- Data roles control emphasis: only use visual emphasis such as `.is-principal`, `.is-active`, or `.is-focus` when the source marks a primary, current, recommended, or otherwise special item.
- Layout controls hierarchy: if one group is supporting context, use a sidebar or rail; if groups are peers, use parallel regions or a grouped grid.

Contact variants:

- `contact-roster`: use for named primary contacts plus secondary contributors, advisors, or support contacts. Replace `.contact-section-title`, `.contact-sidebar h3`, and `.contact-legend` with supplied labels such as Contacts / Contributors, Owners / Support team, or Principal contacts / Advisors.
- `contact-network`: use for expert networks grouped by geography, practice, capability, industry, function, or expertise. Use multiple `.contact-group-title` sections and compact `.contact-mini-card` records. Do not force a sidebar when groups are peers.
- `contact-card` / `profile`: use inside another page when there are only 1-2 people or when people support a larger exhibit.
- Owner maps without named people should usually use `raci-governance-grid`, `decision-log`, or a table instead of fake contact cards.

This same variant logic applies across component families: tables vary by fields and row count; charts vary by data shape and axis needs; process components vary by sequence versus gates versus loops; governance components vary by whether the source has decisions, owners, cadence, or only unresolved asks.

- Use `card` for repeated, comparable ideas.
- Use `callout` for a single implication or decision ask.
- Use `metric-strip` when the page needs 3-5 headline numbers.
- Use `table` when comparison needs row/column precision.
- Use `agenda-list` for narrative structure.
- Use `catalog-grid` for section catalogs or contents pages.
- Use `objective-list` plus `objective-summary` for meeting objectives and decision framing.
- Use `agenda-table` for timed workshops with topics and outcomes.
- Use `simple-agenda-grid` for non-timed agendas with numbered modules.
- Use `illustration-orbit` when the page needs neutral visual support without external assets.
- Use visual primitives only when the page needs supportive imagery and the source does not justify a data/process/time exhibit. Read `references/visual-assets.md` before using them.
- Use `visual-architecture-stack` for platform layers, architecture depth, or integration systems.
- Use `visual-operating-system` for a core operating capability coordinating surrounding routines.
- Use `visual-market-map` for directional opportunity spaces when scored evidence is not available.
- Use `visual-value-bridge` for directional value movement before exact financials are available.
- Use `visual-risk-control` for safeguards and control framing before risks become a register.
- Use `visual-customer-journey` for unlabeled journey support when the page is conceptual.
- Use `visual-team-network` for collaboration shape when real people records are not supplied.
- Use `visual-data-flywheel` for learning loops, telemetry, and compounding reuse.
- Use `profile` for team, expert, or stakeholder pages.
- Use `contact-card` only when the input contains real contact records.
- Contact roster labels are semantic fields, not fixed copy. Set `.contact-section-title`, `.contact-sidebar h3`, and `.contact-legend` from the supplied grouping, such as Contacts / Contributors, Owners / Support team, Executive sponsors / Working team, or Principal contacts / Advisors.
- Use `contact-network` when the input describes a network of experts grouped by region, function, practice, capability, or expertise. Use the group labels as visible section headings.
- Use `team-wall` for compact many-person views when names and roles matter more than hierarchy. Use `bio-card-grid` when each person needs a short credential, responsibility, or biography.
- Use `column-chart` for one categorical series when vertical comparison is appropriate and labels are short.
- Use `line-chart` for ordered trends, `combo-chart` for volume plus rate/index, `paired-bars` for two values per category, `likert-bars` for ordered response distributions, `waterfall-bridge` for additive movement, `stacked-waterfall-bridge` for base-plus-uplift bridges, and `checkmark-bar-table` for pass/fail gates plus a score bar.
- Use `small-multiples-chart` for repeated comparable segment trends, `cohort-retention-grid` for cohort-age retention or conversion, `distribution-plot` for spread and outliers, and `variance-bridge-table` for plan/current/variance by driver.
- Use `option-funnel-scorecard` when screening logic and shortlist scoring must appear together, `tradeoff-frontier` when two dimensions explain dominated choices, `scenario-comparison-table` when assumptions change the decision posture, and `assumption-register-table` when open proof gates should remain visible.
- Use `system-context-map` for a governed core system and adjacent actors, `dependency-map` for cross-team/system dependencies, `sequence-interaction-flow` for actor-to-actor technical interaction order, and `architecture-option-comparison` for architecture path tradeoffs.
- Use `stakeholder-map` for influence/commitment or influence/support mapping, `workshop-breakout-synthesis` for comparable breakout outputs, and `decision-capture-board` for workshop decisions with owners, evidence asks, and next actions.
- Use `quadrant-matrix` for qualitative 2x2 prioritization, segmentation, or portfolio positioning.
- Use `risk-matrix-register` when risk placement must be paired with owners, mitigations, scores, or next actions.
- Components with bottom x-axis labels or bottom captions, including risk/register matrices, portfolio matrices, quadrant/scatter plots, and similar charts, should sit in `section.slide.is-dense` when they run close to the footer. Dense mode provides the axis clearance; do not add arbitrary bottom padding to ordinary heatmaps or tables.
- Use `range-competency-chart` when capabilities have current and target levels on the same numeric scale.
- Use `competency-gap-range-table` when capability rows need group labels, exact gap cells, and current/desired markers in one dense exhibit.
- Use `dot-scale-comparison` for relative positioning on a shared scale when exact axis precision is secondary.
- Use `range-comparison-plot` for benchmark ranges, peer min/max bands, or confidence intervals with a current marker.
- Use `tornado-bars` when two opposing numeric series should read from a shared center axis.
- Use `pie-chart` only for a small number of part-to-whole splits where the total is explicit.
- Use `donut-chart` when the center message matters as much as the part-to-whole split.
- Use `part-to-whole-comparison` for two related pie/donut splits; use `donut-explanation` when one large split needs an explanatory legend/list.
- Use `chart-bars` when the input contains labeled numeric categories.
- Use `ranked-bars` for ordered categorical ranking.
- Use `stacked-bars` for composition across categories.
- Use `heatmap` for capability, maturity, fit, or assessment scores across two categorical dimensions.
- Use `diverging-heatmap` when values can move below and above a neutral midpoint.
- Use `scatter-plot` when the data has two numeric dimensions.
- Use `comparison-table` when options must be compared across consistent criteria.
- Use `weighted-scorecard` when options have weighted criteria, scores, and a recommendation.
- Use `sensitivity-grid` when a decision depends on low/base/high cases or scenario assumptions.
- Use `portfolio-prioritization-matrix` when initiatives, business units, market options, or product bets can be mapped by value and feasibility.
- Use `raci-governance-grid` when governance needs role ownership, decision rights, forums, and cadence in one exhibit.
- Use `contents-card-grid` for module, agenda, or section catalogs with short parallel descriptions.
- Use `six-column-list` for six compact capabilities, principles, or outcome categories.
- Use `wide-data-table` when dense analytical rows need 5-7 comparable fields.
- Use `ranked-evidence-table` when order of importance and proof must stay together, `driver-recap-columns` when a fact base needs concise driver summaries, and `matrix-table` when many options share categorical fields.
- Use `status-table` when workstreams need status, progress, risk/blocker, and next action fields.
- Use `quote-grid` when multiple stakeholder voices need synthesis without one quote owning the page.
- Use `pyramid-stack` when levels build toward a top outcome or narrow from foundation to focus.
- Use `cause-effect` when one root cause, driver, or constraint leads to one primary effect.
- Use `outcome-support` when the conclusion should appear above 2-4 supporting points.
- Use `diverging-textboxes` when two positions, mindsets, models, or options need balanced prose comparison.
- Use `from-to-multi` when several coordinated shifts move from current state to target state.
- Use `compass-choice` when a decision space has up to four mutually distinct strategic directions.
- Use `framework-map` when a core operating concept is surrounded by 3-6 related elements.
- Use `issue-tree` when a question breaks into branches and leaves, `iceberg-model` when symptoms must be separated from underlying drivers, and `capability-coverage-map` when capability coverage or gaps are the message.
- Use `process-flow` when steps are sequential and each step has a distinct role.
- Use `stage-gate` when major work stages are separated by explicit go/no-go decisions.
- Use `funnel-steps` when a broad set is narrowed through qualification stages.
- Use `filter-cascade` when each filter explains why options are removed or advanced.
- Use `loop-cycle` when the work is iterative and learning changes the next cycle.
- Use `cycle-flow` when the operating loop has 3-5 recurring actions around one core rhythm.
- Use `vertical-process-takeaway` when ordered steps each need a takeaway, obstacle, or implication.
- Use `process-deep-dive` when one stage needs detail while the full process remains visible.
- Use `cascading-flow` when work moves through handoffs or dependencies in a stepped sequence.
- Use `decision-flowchart` when pass/fail, yes/no, approval, or triage logic changes the path.
- Use `fishbone-cause-effect` when multiple cause categories explain one performance, risk, or quality effect.
- Use `triangle-steps` when exactly three mutually reinforcing moves support one outcome.
- Use `screen-filter-grid` when multiple inputs pass through 2-4 screens into one outcome.
- Use `value-chain` when activities create, transfer, and improve value across a chain.
- Use `chevron-process-ribbon` for connected linear phases, `swimlane-process-map` for role/system handoffs, `customer-journey-loop` for repeated journey learning, and `input-process-output-layers` for architecture or operating-model transformation from inputs to outputs.
- Use `timeline` for simple chronological events or period markers.
- Use `horizon-bands` for near/mid/long-term opportunity framing.
- Use `horizon-curve` when horizons build toward a larger ambition rather than sitting as equal bands.
- Use `journey-map` when stakeholder experience changes across phases.
- Use `journey-arc` when adoption, maturity, or user progression improves across named stages.
- Use `gantt-workplan` when workstreams are mapped across periods and bars show duration.
- Use `stair-step-timeline` when maturity increases through 4-6 visible steps.
- Use `journey-wave` when the journey has rises and dips, not a simple upward arc.
- Use `calendar-workplan` when short-cycle dates or days own the workplan.
- Use `schedule-list` when a workshop, day plan, or session has time blocks.
- Use `phase-meeting-plan` when a meeting or workshop has phases and outputs but not exact time blocks.
- Use `phase-roadmap` when the implementation path has 3-5 named phases.
- Use `milestone-track` when status across major milestones is the message.
- Use `quote-large` when a sourced voice should own the page.
- Use `quote-small` when a quote supports, but does not replace, the exhibit.
- Use `quote-insight` when the page must translate a quote into an implication.
- Use `numbered-list-grid` for 4-9 short parallel steps or principles.
- Use `dense-list` for compact records that do not need a table's column precision.
- Use `conversion-list` when a sequence converts inputs into signals, actions, and outcomes.
- Use `story-block-list` when one governing statement needs 3-4 compact proof blocks.
- Use `step-explanation-strip` when ordered steps need longer explanation than a simple numbered grid.
- Use `icon-outcome-grid` when 3-6 parallel outcome categories need compact summaries.
- Use `decision-log` when decisions need owner, timing, and status tracking.
- Use `pros-cons-table` when options can be compared across pros, cons, and implication.

## Sufficiency Rules

Do not output components that add no information.

- Contact card: needs a name plus at least one supporting field such as role, location, team, email, or responsibility.
- Contact roster page: needs at least 3 usable contact records. If fewer, use a compact card group inside another page or omit.
- Contact roster headings and legend: use the user's group names when provided; otherwise choose neutral labels from the content. Only use "Principal contacts" and `.is-principal` when the input supplies that grouping or a clear equivalent.
- Team wall: needs at least 5 named people and at least one supporting field such as title, role, region, or team.
- Bio card grid: needs 2-6 named people with at least two supporting fields such as title, responsibility, credential, location, email, or biography.
- Column chart: needs at least 2 labeled numeric values. Use at most one `.is-highlight` item unless the user explicitly asks to compare multiple focus categories.
- Line chart: needs at least 3 ordered periods and one numeric series. Use a table when exact values are the primary need.
- Small multiples chart: needs at least 3 comparable segments, each with the same ordered periods and measure.
- Combo chart: needs one bar series and one line/rate/index series over the same periods. Do not combine unrelated measures.
- Cohort retention grid: needs at least 3 cohort rows, 3 ordered period-age columns, and comparable values.
- Distribution plot: needs histogram buckets or distribution statistics such as min, max, median, and interquartile range.
- Variance bridge table: needs at least 3 drivers with plan, actual, variance, and readout fields.
- Paired bars: needs at least 2 categories with exactly two comparable values per category.
- Likert bars: needs at least 2 rows and 3-5 ordered response buckets that sum to a meaningful total.
- Waterfall bridge: needs a start value, at least two additive/subtractive drivers, and an end value.
- Checkmark bar table: needs 2+ options, 2+ binary criteria, and one score, value, or indexed bar.
- Bar chart: needs at least 2 labeled numeric values. If exact numeric values matter more than visual comparison, use a table.
- Ranked bars: needs sortable numeric values.
- Stacked bars: needs category parts that sum to a meaningful total.
- Heatmap: needs row labels, column labels, and cell ratings or scores.
- Scatter plot: needs x and y values for each point.
- Comparison table: needs options and shared criteria.
- Weighted scorecard: needs at least 3 criteria, 2 options, explicit weights or a clearly stated unweighted scoring rule, and a recommendation readout.
- Option funnel scorecard: needs stage counts or gates plus at least 2 scored shortlist options.
- Tradeoff frontier: needs at least 3 options and two comparable dimensions such as value/risk, control/speed, or cost/impact.
- Scenario comparison table: needs at least 2 scenarios with assumptions, impact, and decision posture.
- Assumption register table: needs at least 2 assumptions with evidence, test, owner, or status.
- Sensitivity grid: needs at least 2 assumptions or scenarios and at least 2 cases such as low/base/high, downside/base/upside, or conservative/target/stretch.
- Portfolio prioritization matrix: needs at least 3 options or initiatives and two meaningful dimensions such as value and feasibility, attractiveness and right-to-win, or impact and readiness.
- RACI governance grid: needs at least 2 decisions or processes and clear role/cadence fields. Do not invent accountable owners if the user has not supplied them.
- System context map: needs one core system or capability and 4-6 adjacent systems, users, data sources, or controls.
- Dependency map: needs at least 2 lanes and multiple dependencies or tasks per lane.
- Sequence interaction flow: needs at least 3 actors and 4 ordered interactions.
- Architecture option comparison: needs at least 2 architecture paths and 3 shared criteria.
- Stakeholder map: needs at least 4 stakeholders or groups and two meaningful dimensions.
- Workshop breakout synthesis: needs 2-4 breakout groups with parallel findings and decisions or actions.
- Decision capture board: needs a decision plus owner, evidence ask, and next action; use `decision-log` for many detailed records.
- Metric strip: needs 3-5 high-signal metrics. If there is only one number, use a statement or callout.
- Table: needs consistent row/column structure. Do not force prose into a table.
- Catalog grid: needs at least 3 sections. If there are more than 9 sections, split the catalog or use a denser list.
- Objective list: needs at least 3 objectives or agenda items. Highlight only one item unless the user asks for multiple focus areas.
- Agenda table: needs time blocks plus topic, outcome, owner, or speaker fields. If times are missing, use `simple-agenda-grid`.
- Simple agenda grid: use for 3-9 items with short parallel labels.
- Quadrant matrix: needs two meaningful dimensions and at least one point, option, segment, or initiative. Do not use a quadrant when only a ranked list is needed.
- Risk matrix with register: needs risk names plus at least one of owner, mitigation, status, score, likelihood, or impact. Use a plain table if the user only provides a risk list.
- Range competency chart: needs a shared numeric or ordinal scale and at least two capabilities. Current and target markers must mean the same thing across rows.
- Dot-scale comparison: needs a common left-to-right interpretation for every row. If rows use different scales, use a table.
- Range comparison plot: needs min/max or low/high values plus a marker or target. Do not invent ranges from single-point data.
- Pie chart: needs parts that sum to a meaningful total, ideally 2-5 slices. Use a table for more slices or small differences.
- Donut chart: needs a center message or total that adds context. Otherwise use `pie-chart` or `stacked-bars`.
- Diverging heatmap: needs a neutral midpoint and categorical rows/columns. Use regular `heatmap` for one-direction scores.
- Pyramid stack: needs 2-4 levels with a clear hierarchy. Do not use it for unordered peer items.
- Cause-effect: needs a specific driver and consequence. If there are many causes, use cards, an issue tree, or a table.
- Outcome-support: needs one answer plus at least two supporting points. If the answer is missing, write the claim first.
- Diverging textboxes: needs two sides that are comparable. If there are more than two options, use cards or a comparison table.
- From-to multi: needs at least two current-to-target pairs. If there is only one shift, use `cause-effect` or a statement page.
- Compass choice: needs 3-4 distinct choices around one decision. Do not use it for sequential steps.
- Framework map: needs one core concept and related elements. If order matters, use a flow or roadmap instead.
- Issue tree: needs one root question, 2-4 branches, and at least two leaves under each branch.
- Iceberg model: needs visible symptoms plus hidden drivers. Do not use it for generic prose lists.
- Capability coverage map: needs 4+ capabilities or domains with explicit coverage states.
- Process flow: needs 3-6 ordered steps with short labels. If order is not meaningful, use cards or a numbered list grid.
- Stage gate: needs at least two stages and at least one decision gate. Do not use it for a simple linear timeline.
- Funnel steps: needs a narrowing set, qualification logic, or count reduction. Do not use a funnel for unrelated categories.
- Filter cascade: needs explicit filter criteria and a resulting set or decision output.
- Loop cycle: needs repeated iteration. If the process ends once, use `process-flow`.
- Vertical process takeaway: needs 3-5 ordered steps plus a takeaway, obstacle, or implication that applies across or beside the steps.
- Process deep dive: needs 3-5 stages and one stage with enough detail to justify the deep-dive panel.
- Triangle steps: needs exactly 3 mutually reinforcing items around one outcome. Use cards when there are more or fewer items.
- Screen filter grid: needs 3+ inputs or option sources, 2-4 filter criteria, and one outcome or shortlist.
- Value chain: needs activities that are linked by value creation or handoff. Avoid it for generic department lists.
- Chevron process ribbon: needs 3-6 ordered phases with short labels.
- Swimlane process map: needs 2+ lanes and 3+ stages, with tasks mapped to lanes.
- Customer journey loop: needs 4+ recurring moments and a learning or feedback implication.
- Input-process-output layers: needs at least one input, one process/control layer, and one output.
- Timeline: needs dated, period-based, or sequential events. Use `phase-roadmap` if work packages matter more than dates.
- Horizon bands: needs distinct time horizons or uncertainty horizons. Do not use it for equal peer options.
- Journey map: needs phases from a user, customer, team, or stakeholder perspective.
- Phase roadmap: needs 3-5 phases plus one or two deliverables per phase. Split dense plans across slides.
- Milestone track: needs milestone names and clear status or sequence.
- Quote large: needs a real quote or user-provided statement. Do not invent attributed quotes.
- Quote small: needs a quote that supports another page element. If no exhibit exists, use `quote-large` or omit.
- Quote insight: needs both a quote and an implication. If the implication is missing, synthesize only when supported by context.
- Quote grid: needs at least 3 real or user-provided quote-like statements. Do not invent quotes; use callouts or dense-list for unsourced themes.
- Numbered list grid: needs short, parallel items. Keep each item to a heading plus one compact support line.
- Dense list: needs repeated records with similar shape. Use a table when exact fields or auditability matter.
- Contents card grid: needs 3-6 modules, agenda sections, or catalog items with short parallel descriptions.
- Six-column list: needs exactly 6 compact parallel categories. Use numbered-list-grid for 4-9 items that need more support text.
- Wide data table: needs 3+ rows and 5-7 consistent fields. Split or simplify if labels are long or cells require paragraphs.
- Ranked evidence table: needs 3+ ranked rows plus evidence and implication fields.
- Driver recap columns: needs 3-5 drivers with parallel short support text. Use a table when fields need auditability.
- Matrix table: needs 3+ rows and 3+ shared categorical columns.
- Status table: needs workstream or item names plus status/progress/risk/action fields. Use decision-log if decisions are the main records.
- Decision log: needs at least two decisions and owner/timing/status fields.
- Pros-cons table: needs options plus pros and cons. Use `comparison-table` when there are more criteria.
- Cycle flow: needs 3-5 repeated loop steps and one core loop label. Use `loop-cycle` for a simpler four-node learning cycle.
- Cascading flow: needs 3-5 ordered handoffs or dependencies. Do not use it for unordered categories.
- Decision flowchart: needs at least one branch condition and two possible paths. Use `filter-cascade` when the path is a linear screening list.
- Fishbone cause-effect: needs one explicit effect plus at least 3 cause categories. Use `cause-effect` for one driver and one consequence.
- Horizon curve: needs 3-4 horizons that build over time or ambition. Use `horizon-bands` when horizons are equal buckets.
- Journey arc: needs 4-5 staged progression steps. Use `journey-map` when the key message is high/mid/low experience by phase.
- Gantt workplan: needs at least 3 workstreams and 3 time periods. Use `phase-roadmap` when exact timing is not known.
- Dense Gantt variant: use `.gantt-workplan.is-dense` inside `.slide.is-dense` when workstreams and period labels need a fixed body band.
- Visual primitives: need a clear answer-first page message and a reason the visual supports comprehension. Do not use them as decoration on sparse pages or as substitutes for charts, tables, matrices, scorecards, timelines, or risk registers when evidence exists.
- Stair-step timeline: needs 4-6 ordered maturity or progression steps. Use `timeline` if the message is chronology rather than increasing maturity.
- Journey wave: needs 4-6 journey stages with explicit rises, dips, friction, or recovery points.
- Calendar workplan: needs named days, dates, or short-cycle periods plus tasks in each period.
- Schedule list: needs time blocks plus activity, owner, outcome, or discussion detail. If times are missing, use `simple-agenda-grid`.
- Phase meeting plan: needs 3-5 phases with actions, decisions, or outputs. Use `agenda-table` or `schedule-list` when exact time blocks are supplied.
- Conversion list: needs 3-6 conversion nodes that turn one input type into a signal, action, or outcome.
- Story block list: needs one governing statement plus 3-4 supporting proof blocks. Do not use it for unrelated points.
- Step explanation strip: needs 4-6 ordered steps with a support sentence for each step.
- Icon outcome grid: needs 3-6 parallel outcomes with short labels and compact support text.

## Data Display Router

- Time series: use `line-chart` for one trend or `combo-chart` when a rate/index must be read with volume over the same periods.
- Categorical comparison: use `column-chart` for a compact single-series vertical comparison with short labels, `ranked-bars` for visual ranking, `paired-bars` for current-vs-target or before-vs-after pairs, `chart-bars` for horizontal category labels, or `table` for exact values and many fields.
- Survey or ordered response distribution: use `likert-bars`.
- Additive movement: use `waterfall-bridge` only when the drivers reconcile from start to end.
- Base plus uplift bridge: use `stacked-waterfall-bridge` when each step has both an existing/base value and an incremental opportunity segment.
- Binary gates plus score: use `checkmark-bar-table`.
- Part-to-whole: use `pie-chart` or `donut-chart` for one or two simple splits, `stacked-bars` for composition across many categories, and `table` when percentages need exact auditability.
- Part-to-whole story pages: use `part-to-whole-comparison` for two related splits and `donut-explanation` for one large split with explanatory labels.
- Opposing series: use `tornado-bars` for left-versus-right quantities on a shared centerline.
- Two-dimensional opportunity: use `scatter-plot` if both axes are numeric, or `quadrant-matrix` if the axes are qualitative.
- Initiative or portfolio prioritization: use `portfolio-prioritization-matrix` for directional value-vs-feasibility choices, `weighted-scorecard` for criteria scoring, or `comparison-table` when exact fields matter.
- Risk view: use `risk-matrix-register` when likelihood/impact placement and action tracking both matter.
- Capability/maturity assessment: use `heatmap` for one-direction scores or `range-competency-chart` when current-vs-target gaps are the message.
- Capability gap diagnostic: use `competency-gap-range-table` when the page must preserve group labels, gap sizing, current level, and desired level together.
- Benchmark spread: use `range-comparison-plot` for min/max, confidence interval, peer range, or low/base/high inputs.
- Relative scorecard: use `dot-scale-comparison` when every row can share the same left-to-right scale.
- Diverging categorical data: use `diverging-heatmap` for negative-to-positive movement or below/above-neutral measures.
- Option evaluation: use `weighted-scorecard` when criteria have weights or scores; use `comparison-table` when exact scoring is not justified.
- Scenario or sensitivity: use `sensitivity-grid` when assumptions change the answer; use a plain table when the cases are only descriptive.
- Few headline KPIs: use `metric-strip`.
- Many records with mixed fields: use `table`.
- Dense analytical records: use `wide-data-table` when fields are comparable and the table must stay on one page, `ranked-evidence-table` when ranking and proof must stay together, and `matrix-table` when option-by-attribute coverage is the main evidence.
- Status records: use `status-table` when the decision job is progress, risk, and next action.
- No numeric data: do not create a chart.

## Text And Structure Router

- Sequential work: use `process-flow` for ordered steps, `chevron-process-ribbon` for connected phases, `vertical-process-takeaway` when steps need implications, `process-deep-dive` when one stage needs detail, `stage-gate` for decision checkpoints, `cascading-flow` or `swimlane-process-map` for handoffs, `cycle-flow`, `loop-cycle`, or `customer-journey-loop` for iteration, `input-process-output-layers` for architecture transformation, and `value-chain` for handoffs across an operating chain.
- Narrowing logic: use `funnel-steps` when the set visibly shrinks, `filter-cascade` when criteria explanation matters, `screen-filter-grid` when multiple inputs pass through screens, and `decision-flowchart` when the path branches.
- Root-cause logic: use `fishbone-cause-effect` when multiple categories lead to one effect, `issue-tree` when a question decomposes into branches, and `iceberg-model` when symptoms should be separated from hidden drivers.
- Time and phases: use `timeline` for chronological events, `phase-roadmap` for implementation phases, `phase-meeting-plan` for meeting phases and outputs, `milestone-track` for progress status, `horizon-bands` or `horizon-curve` for near/mid/long-term framing, `journey-map`, `journey-arc`, or `journey-wave` for stakeholder experience, `stair-step-timeline` for maturity steps, `calendar-workplan` for short-cycle workplans, `schedule-list` for timed sessions, and `gantt-workplan` or `.gantt-workplan.is-dense` for workstreams across periods.
- Lists and decisions: use `numbered-list-grid` for short parallel steps, `step-explanation-strip` for longer step support, `contents-card-grid` for module catalogs, `six-column-list` for exactly six compact categories, `icon-outcome-grid` for parallel outcomes, `conversion-list` for input-to-outcome sequences, `story-block-list` for one message plus proof, `dense-list` for compact repeated records, `status-table` for progress records, `decision-log` for governance tracking, and `pros-cons-table` for option tradeoffs.
- Governance: use `raci-governance-grid` when the page must show accountable/responsible/consulted/informed roles plus forum and cadence.
- Quotes: use `quote-large` only when the quote is the evidence, `quote-small` when the quote supports an exhibit, and `quote-insight` when the implication should be stated beside the quote.
- Visual support: use `visual-architecture-stack`, `visual-operating-system`, `visual-market-map`, `visual-value-bridge`, `visual-risk-control`, `visual-customer-journey`, `visual-team-network`, or `visual-data-flywheel` only after checking `references/visual-assets.md`. Pair them with a claim, implication, or sidebar note.

## Fit Contract

- Components must not rely on resizing or reflowing the slide canvas.
- Browser present mode scales the whole 1600x900 slide. Component internals should keep the same grid, column, and sidebar structure at narrow viewport widths.
- Component wrappers should preserve `min-width: 0`, `min-height: 0`, and bounded overflow behavior.
- Demo data should prove the component shape without using so many rows, columns, or words that the default 16:9 content area overflows.
- Use `safe-stack` only for small components that support one message. Do not stack unrelated exhibits.
- Components should not draw heavy outer boxes by default. Use borders for tables, matrices, heatmaps, true cards, or intentional separators; otherwise rely on spacing, type hierarchy, and theme tokens.

Full-deck showcase files should combine multiple component families in one coherent storyline to validate fit, not to define new generation rules. Keep visible headers neutral and business-oriented rather than exposing internal component taxonomy.

## Next Component Families

Future passes should expand CV/face-page primitives, richer full-deck examples, and any domain-specific components that emerge from real user cases.

## Snippets

| file | purpose |
| --- | --- |
| `templates/components/card.html` | Repeated idea or evidence block. |
| `templates/components/callout.html` | One implication or decision statement. |
| `templates/components/metric-strip.html` | Four headline metrics. |
| `templates/components/agenda-list.html` | Three-item agenda list starter. |
| `templates/components/catalog-grid.html` | Contents or section catalog grid. |
| `templates/components/objective-list.html` | Objective list with optional active marker. |
| `templates/components/objective-summary.html` | Summary/objectives text block. |
| `templates/components/agenda-table.html` | Timed workshop agenda rows. |
| `templates/components/simple-agenda-grid.html` | Numbered agenda grid. |
| `templates/components/table.html` | Compact comparison table. |
| `templates/components/illustration-orbit.html` | Neutral abstract illustration. |
| `templates/components/visual-architecture-stack.html` | Supportive visual for architecture layers and integration depth. |
| `templates/components/visual-operating-system.html` | Supportive visual for a core capability coordinating surrounding routines. |
| `templates/components/visual-market-map.html` | Supportive visual for directional opportunity spaces. |
| `templates/components/visual-value-bridge.html` | Supportive visual for directional value movement. |
| `templates/components/visual-risk-control.html` | Supportive visual for safeguards and control framing. |
| `templates/components/visual-customer-journey.html` | Supportive visual for journey or adoption progression. |
| `templates/components/visual-team-network.html` | Supportive visual for collaboration shape without named people. |
| `templates/components/visual-data-flywheel.html` | Supportive visual for learning loops and compounding reuse. |
| `templates/components/profile.html` | Profile row with generated avatar placeholder. |
| `templates/components/contact-card.html` | Single contact with optional photo. |
| `templates/layouts/contact-roster.html` | Primary contacts plus sidebar contributors or support contacts. |
| `templates/layouts/contact-network.html` | Expert or contact network grouped by geography, practice, capability, or expertise. |
| `templates/components/team-wall.html` | Compact many-person wall for team or expert networks. |
| `templates/components/bio-card-grid.html` | People grid with compact biography, credentials, or responsibility details. |
| `templates/components/line-chart.html` | Ordered trend chart using inline SVG. |
| `templates/components/combo-chart.html` | Volume bars plus line/rate series in one chart. |
| `templates/components/paired-bars.html` | Two-value comparison bars across categories. |
| `templates/components/likert-bars.html` | Ordered response distribution bars. |
| `templates/components/waterfall-bridge.html` | Start-to-end bridge across additive drivers. |
| `templates/components/competency-gap-range-table.html` | Dense capability gap table with group labels, gap cells, and current/desired markers. |
| `templates/components/tornado-bars.html` | Opposing quantitative bars around a shared center axis. |
| `templates/components/stacked-waterfall-bridge.html` | Bridge view with base economics and uplift/saving potential in each step. |
| `templates/components/part-to-whole-comparison.html` | Side-by-side part-to-whole comparison panels. |
| `templates/components/donut-explanation.html` | Large donut split with an explanatory legend/list. |
| `templates/components/checkmark-bar-table.html` | Option gate table with binary checks and score bars. |
| `templates/components/column-chart.html` | Single-series vertical category chart with optional highlighted column. |
| `templates/components/quadrant-matrix.html` | Qualitative 2x2 matrix with points and legend. |
| `templates/components/risk-matrix-register.html` | Impact/likelihood matrix plus action-oriented register. |
| `templates/components/range-competency-chart.html` | Current vs. target capability rows on a shared scale. |
| `templates/components/dot-scale-comparison.html` | Dot-on-line relative comparison rows. |
| `templates/components/range-comparison-plot.html` | Benchmark range bands with current markers and notes. |
| `templates/components/pie-chart.html` | One or two compact part-to-whole pie splits. |
| `templates/components/donut-chart.html` | Donut split with a center message and legend. |
| `templates/components/diverging-heatmap.html` | Negative-neutral-positive heatmap with legend. |
| `templates/components/chart-bars.html` | Static categorical bar chart. |
| `templates/components/ranked-bars.html` | Ordered categorical ranking. |
| `templates/components/stacked-bars.html` | Composition bars. |
| `templates/components/heatmap.html` | Capability or assessment heatmap. |
| `templates/components/scatter-plot.html` | Two-axis opportunity map. |
| `templates/components/comparison-table.html` | Options compared against criteria. |
| `templates/components/weighted-scorecard.html` | Weighted option scoring with recommendation. |
| `templates/components/sensitivity-grid.html` | Low/base/high scenario or assumption sensitivity. |
| `templates/components/ranked-evidence-table.html` | Ranked records with proof and implication fields. |
| `templates/components/driver-recap-columns.html` | Driver recap columns for analysis-heavy summaries. |
| `templates/components/matrix-table.html` | Option-by-attribute matrix for categorical analysis. |
| `templates/components/portfolio-prioritization-matrix.html` | Value-vs-feasibility prioritization for initiatives, markets, or portfolio choices. |
| `templates/components/raci-governance-grid.html` | Role, decision-rights, forum, and cadence mapping. |
| `templates/components/pyramid-stack.html` | Hierarchical levels building toward an outcome. |
| `templates/components/cause-effect.html` | One driver linked to one consequence. |
| `templates/components/outcome-support.html` | Top outcome with supporting proof points. |
| `templates/components/diverging-textboxes.html` | Two balanced prose positions or models. |
| `templates/components/from-to-multi.html` | Multiple current-to-target shifts. |
| `templates/components/compass-choice.html` | Four-direction decision space. |
| `templates/components/framework-map.html` | Core concept with surrounding operating elements. |
| `templates/components/issue-tree.html` | Root question decomposed into branches and leaves. |
| `templates/components/iceberg-model.html` | Visible symptoms separated from hidden drivers. |
| `templates/components/capability-coverage-map.html` | Capability coverage and gap map. |
| `templates/components/process-flow.html` | Sequential process steps. |
| `templates/components/chevron-process-ribbon.html` | Connected chevron phases for linear processes. |
| `templates/components/swimlane-process-map.html` | Role or system lanes across process stages. |
| `templates/components/customer-journey-loop.html` | Recurring journey loop with learning implication. |
| `templates/components/input-process-output-layers.html` | Input-to-control-to-output architecture or operating model. |
| `templates/components/stage-gate.html` | Stages separated by decision gates. |
| `templates/components/funnel-steps.html` | Narrowing opportunity or qualification funnel. |
| `templates/components/filter-cascade.html` | Filter criteria leading to a shortlist or result. |
| `templates/components/loop-cycle.html` | Iterative cycle with four repeated actions. |
| `templates/components/cycle-flow.html` | Recurring operating loop around one core rhythm. |
| `templates/components/vertical-process-takeaway.html` | Ordered steps paired with a takeaway, obstacle, or implication panel. |
| `templates/components/process-deep-dive.html` | Stage strip with one highlighted stage and supporting detail. |
| `templates/components/cascading-flow.html` | Stepped handoff or dependency flow. |
| `templates/components/decision-flowchart.html` | Branching approval, screening, or triage logic. |
| `templates/components/fishbone-cause-effect.html` | Multiple cause categories leading to one effect. |
| `templates/components/triangle-steps.html` | Three mutually reinforcing moves around one outcome. |
| `templates/components/screen-filter-grid.html` | Multiple inputs, screen criteria, and resulting outcome. |
| `templates/components/value-chain.html` | Linked value creation activities. |
| `templates/components/timeline.html` | Chronological events using `.timeline-track`. |
| `templates/components/horizon-bands.html` | Near/mid/long-term horizon framing. |
| `templates/components/horizon-curve.html` | Horizons building toward a larger ambition. |
| `templates/components/journey-map.html` | Stakeholder or customer journey phases. |
| `templates/components/journey-arc.html` | Upward adoption or maturity progression. |
| `templates/components/journey-wave.html` | Journey with rises, dips, friction, and recovery points. |
| `templates/components/phase-roadmap.html` | Four-phase implementation roadmap. |
| `templates/components/gantt-workplan.html` | Workstreams mapped across time periods. |
| `templates/components/phase-meeting-plan.html` | Meeting or workshop phases with actions and outputs. |
| `templates/components/stair-step-timeline.html` | Maturity or progression steps rising over time. |
| `templates/components/calendar-workplan.html` | Short-cycle workplan organized by day or date. |
| `templates/components/schedule-list.html` | Timed agenda or working-session schedule. |
| `templates/components/milestone-track.html` | Milestones with completion/current states. |
| `templates/components/quote-large.html` | Full-page quote evidence. |
| `templates/components/quote-small.html` | Compact supporting quote. |
| `templates/components/quote-insight.html` | Quote plus implication panel. |
| `templates/components/quote-grid.html` | Multiple stakeholder voices in one synthesis page. |
| `templates/components/numbered-list-grid.html` | Numbered parallel steps or principles. |
| `templates/components/contents-card-grid.html` | Module or section catalog cards. |
| `templates/components/six-column-list.html` | Six compact parallel categories. |
| `templates/components/dense-list.html` | Compact repeated text records. |
| `templates/components/conversion-list.html` | Input-to-signal-to-action-to-outcome conversion records. |
| `templates/components/story-block-list.html` | One governing story block plus compact proof blocks. |
| `templates/components/step-explanation-strip.html` | Ordered steps with longer support text. |
| `templates/components/icon-outcome-grid.html` | Parallel outcome categories with compact icon markers. |
| `templates/components/wide-data-table.html` | Dense analytical table with 5-7 fields. |
| `templates/components/status-table.html` | Workstream status, risk, and next-action table. |
| `templates/components/decision-log.html` | Decisions with owner, timing, and status. |
| `templates/components/pros-cons-table.html` | Pros/cons/implication tradeoff table. |

## Showcase-Only Assets

Bundled headshots in `assets/media/headshots/` are for showcase and full-deck demo pages only. Do not use them in generated user decks unless the user explicitly asks for placeholder demo contacts.

## Agenda And Objectives Composition

- A title cover must include a real title. A brand-only or blank visual page is not a default title cover.
- Use `catalog-grid` when the user provides section names or a deck table of contents.
- Use `objective-list` alone for a compact left rail or transition page.
- Combine `objective-list` with `objective-summary` inside a split layout when the page needs both agenda navigation and meeting purpose.
- Use `agenda-table` when the source has time blocks. Do not invent times.
- Use `simple-agenda-grid` when the source has ordered agenda items without time blocks.
- Keep agenda item labels short. Move explanatory text to a summary, notes, or outcome component.

## Structure Patterns Composition

- Use structure components when the source is structured prose, operating logic, or decision framing rather than numeric data.
- Prefer `blank-content` when the structure component owns the whole page.
- Use `blank-split-even` only when the page compares two equal conceptual systems.
- Use `blank-right-sidebar` when the primary concept needs 2-4 implications, caveats, or decision notes.
- Keep structure labels short and parallel. Split the page if boxes require long paragraphs.
- Do not use structure visuals to decorate sparse content; the component must clarify the page message.

## Process Patterns Composition

- Prefer `blank-content` when the flow owns the page.
- Use `blank-right-rail` or `blank-right-sidebar` only when the flow needs a compact implication, result, or caveat beside it.
- Keep step labels parallel and short. Use at most six flow steps, five value-chain links, four funnel bands, five cycle nodes, five cascading steps, five vertical-process steps, and four screen filters unless the page is intentionally dense.
- Use `process-flow` for sequence, `vertical-process-takeaway` for sequence plus implication, `process-deep-dive` for one highlighted stage, `stage-gate` for approval checkpoints, `filter-cascade` or `screen-filter-grid` for criteria, `decision-flowchart` for branching, `triangle-steps` for three mutually reinforcing moves, `cycle-flow` or `loop-cycle` only for repeated iteration, and `fishbone-cause-effect` only for cause categories that lead to one effect.

## Time Patterns Composition

- Prefer `blank-content` for `timeline`, `horizon-bands`, `horizon-curve`, `journey-arc`, `journey-wave`, `phase-roadmap`, `gantt-workplan`, `calendar-workplan`, `schedule-list`, `stair-step-timeline`, and `milestone-track`.
- Use `blank-split-even` only when comparing two timelines or two journey states.
- Keep roadmaps to 3-5 phases, milestone tracks to 4-6 milestones, journey arcs/waves to 4-5 stages, stair-step timelines to 4-6 steps, calendar workplans to 5-7 periods, and Gantt workplans to 3-5 workstreams. Split the page if labels require more than two short lines.
- `templates/components/timeline.html` uses `.timeline-track` to avoid changing legacy `.timeline` examples.

## Text Patterns Composition

- Use `quote-large` on a full blank page when the quote is the main evidence.
- Use `quote-small` inside a sidebar, rail, or small stack when another exhibit owns the page.
- Use `quote-insight` when the quote and implication both need to be visible at once.
- Use `quote-grid` when 3-4 stakeholder voices support a synthesized page message.
- Use `numbered-list-grid` for short parallel items and `dense-list` for compact repeated records.
- Use `contents-card-grid` for section catalogs and `six-column-list` for exactly six short parallel categories.
- Use `conversion-list` when records move from one state to another, `story-block-list` when one message needs proof blocks, `step-explanation-strip` when steps need support text, and `icon-outcome-grid` for compact parallel outcome categories.
- Use `wide-data-table` and `status-table` only when fields are consistent and the table remains readable inside the safe area.
- Use `decision-log` and `pros-cons-table` inside `blank-content` or a wide region. Do not put dense tables into narrow sidebars.

## Minimal Blank-Page Composition

Use `templates/layouts/blank-content.html` when one component owns the whole content area:

```html
<section class="slide" data-title="Agenda">
  <header>
    <h2 class="slide-title">Agenda</h2>
    <div class="slide-rule"></div>
  </header>
  <div class="content is-vertically-centered">
    <!-- paste templates/components/simple-agenda-grid.html here -->
  </div>
  <footer class="footer">
    <span>Source or note</span>
    <span class="page-number"></span>
  </footer>
</section>
```

For a single-series chart page:

```html
<div class="content is-vertically-centered">
  <!-- paste templates/components/column-chart.html here -->
</div>
```

Use `.is-highlight` on one column only when the title or narrative calls attention to that category. The theme controls the highlight color.

Use `.content.is-vertically-centered` for compact single-component pages when the component would otherwise sit near the top with a large empty lower half. Do not use it for dense dashboards or multi-region pages that already fill the safe area.

Use one content area with a small stack when components support the same message:

```html
<div class="content">
  <div class="safe-stack">
    <!-- paste templates/components/objective-list.html here -->
    <!-- paste templates/components/objective-summary.html here -->
  </div>
</div>
```

Use blank region layouts only when the page needs separate zones:

```html
<div class="content no-top">
  <div class="region-layout right-sidebar">
    <main class="region has-frame-lines">
      <div class="region-body">
        <!-- paste primary component here -->
      </div>
    </main>
    <aside class="region is-muted has-frame-lines">
      <div class="region-body">
        <!-- paste supporting component here -->
      </div>
    </aside>
  </div>
</div>
```

## Composition Order

1. Infer the user's communication task.
2. Choose a layout from `references/layouts.md`.
3. Choose components from this file.
4. Choose one theme from `references/themes.md`.
5. Assemble the page in HTML and verify at 16:9.
