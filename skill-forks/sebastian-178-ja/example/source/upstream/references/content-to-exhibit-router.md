# Content To Exhibit Router

Use this router before choosing a component. It turns user-provided or approved external material into an exhibit plan. The agent should infer the exhibit; do not ask the user to choose component names.

## Evidence Inventory

For each possible slide, extract these fields before authoring HTML:

| Field | Meaning |
| --- | --- |
| `claim` | The answer-first message the exhibit must prove or clarify. |
| `evidence_source` | User material, marked assumption, or approved external data. |
| `evidence_shape` | Numeric series, category values, comparison, time, risk, decision, process, architecture, quote, people, or mixed. |
| `records` | Row count, category count, period count, named people count, or option count. |
| `required_fields_present` | Whether the minimum fields for the intended exhibit exist. |
| `selected_component` | The lightest component that preserves the evidence shape. |
| `selected_showcase_pattern` | Optional page combination reference when one component is not enough. |
| `fallback` | Simpler qualitative or tabular expression if fields are missing. |
| `output_role` | Executive answer, evidence page, decision page, risk page, roadmap, appendix, or close. |

## Routing Matrix

| Input pattern | Best component or combination | Use when | Fallback |
| --- | --- | --- | --- |
| One numeric KPI with business meaning | `callout`, centered metric, or `metric-strip` if 3-5 KPIs exist | The number is verified and drives the page message | Statement page with assumption note |
| Ordered time series | `line-chart`, `combo-chart`, or `small-multiples-chart` | Periods are ordered and comparable | `wide-data-table` |
| Multiple comparable segments over time | `small-multiples-chart` | Same measure is repeated across segments | One `line-chart` plus `driver-recap-columns` |
| Cohort or retention by age | `cohort-retention-grid` | Cohorts and period-age columns are available | `matrix-table` |
| Distribution, spread, or outliers | `distribution-plot` | The average hides variance or tails | `range-comparison-plot` |
| Plan versus actual by driver | `variance-bridge-table` | Drivers have plan, actual, variance, and readout | `comparison-table` |
| Ranked numeric drivers | `ranked-bars` or `ranked-evidence-table` | Rank order is the message | `driver-recap-columns` |
| Two opposing quantities | `tornado-bars` | Values should read from a shared center axis | `paired-bars` |
| Current versus desired capability | `competency-gap-range-table` | Gap values and current/target markers exist | `range-competency-chart` |
| Additive value bridge | `waterfall-bridge` or `stacked-waterfall-bridge` | Values sum to a start/end or base/uplift bridge | `driver-recap-columns` |
| Part-to-whole split | `pie-chart`, `donut-chart`, `part-to-whole-comparison`, or `donut-explanation` | Parts sum to a meaningful total | `stacked-bars` or table |
| Option longlist to recommendation | `option-funnel-scorecard` | Screening stages and shortlist scoring both matter | `weighted-scorecard` |
| Option scenarios | `scenario-comparison-table` | Assumptions, impacts, and decision posture are known | `pros-cons-table` |
| Value versus risk tradeoff | `tradeoff-frontier` | Two dimensions explain dominated versus preferred options | `portfolio-prioritization-matrix` |
| Open assumptions or diligence tests | `assumption-register-table` | Each assumption has evidence, test, owner, or status | `decision-log` |
| Risk placement plus mitigation | `risk-matrix-register` | Risk position and register details both matter | `assumption-register-table` or table |
| Architecture context | `system-context-map` | A core system and adjacent actors/systems are known | `input-process-output-layers` |
| Cross-team dependencies | `dependency-map` | Work must move across teams, systems, or controls | `swimlane-process-map` |
| Technical interaction path | `sequence-interaction-flow` | Actor-to-actor sequence matters | `process-flow` |
| Architecture option choice | `architecture-option-comparison` | Options share control, speed, reuse, risk, or cost fields | `weighted-scorecard` |
| Role ownership and cadence | `raci-governance-grid` | Decisions, roles, forums, and cadence are known | `decision-log` |
| Stakeholder influence or commitment | `stakeholder-map` | Stakeholders can be mapped by two dimensions | `contact-network` or `dense-list` |
| Workshop agenda | `agenda-table` or `phase-meeting-plan` | Time blocks or phases and outputs are known | `simple-agenda-grid` |
| Workshop breakout synthesis | `workshop-breakout-synthesis` | Groups produce comparable findings and decisions | `quote-grid` or `dense-list` |
| Workshop decision close | `decision-capture-board` | Decisions, owners, evidence asks, and next actions are known | `decision-log` |
| Named people roster | `contact-roster`, `contact-network`, `team-wall`, or `bio-card-grid` | Names plus grouping/detail fields are supplied | RACI or dense list when names are missing |
| Qualitative root cause | `issue-tree`, `iceberg-model`, `fishbone-cause-effect`, or `cause-effect` | Reasoning structure is stronger than a table | `numbered-list-grid` |

## Showcase Router

Use combination showcases when one primitive cannot express the whole page job:

- Analytics diagnostic or model interpretation: `advanced-analytics-diagnostic-variants.html`.
- Classic consulting data patterns: `data-classic-consulting-variants.html`.
- Option selection or recommendation: `decision-option-comparison-variants.html`.
- Architecture decision or system explanation: `architecture-system-variants.html`.
- Governance, decision rights, or operating cadence: `governance-operating-cadence-variants.html`.
- Workshop planning or synthesis: `workshop-facilitation-variants.html`.
- Data-heavy chart variants: `data-visualization-variants.html`.
- Analysis-heavy tables: `analysis-table-variants.html`.
- Conceptual framework pages: `conceptual-variants.html`.
- Flows, workplans, and handoffs: `flow-workplan-variants.html`.
- People and contact pages: `people-variants.html`.

## Authoring Defaults

- Prefer the simplest component that preserves the evidence shape.
- Use exact labels, groups, legends, axes, owners, and section titles from the user's material.
- If the input is scraped or externally researched, cite the evidence in the internal plan and keep it separate from user-provided material.
- Do not invent missing values, rows, dates, owners, people, or scores to satisfy a component.
- If the slide needs a data exhibit and an implication, use a region layout with a rail rather than adding decorative cards.
