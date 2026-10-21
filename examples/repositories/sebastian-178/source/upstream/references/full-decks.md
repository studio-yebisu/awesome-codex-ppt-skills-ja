# Full-Deck Patterns

Full decks should have one coherent storyline. Choose a deck pattern based on the audience's decision and the available evidence, then compose pages from `templates/layouts/` and content blocks from `templates/components/`.

Do not treat these as fixed templates. Add, remove, reorder, or combine pages based on the user's material. The archetypes are there to calibrate storyline pacing, page roles, and component fit, not to constrain agent creativity.

Routing priority:

1. Audience decision: what the reader must approve, fund, stop, choose, understand, or investigate.
2. Evidence shape: numeric, comparison, time, risk, decision, qualitative, quote, contact, or mixed.
3. Storyline role: executive answer, context, proof, tradeoff, risk, roadmap, decision, appendix, or closing.
4. Archetype reference: the closest full-deck pattern for pacing and page-role inspiration.
5. Showcase reference: optional page-level composition help for one exhibit.

The selected archetype is a starting hypothesis, not a page order. If the user's evidence implies a better sequence, use the user's evidence.

## First-Class Archetypes

Use these complete deck skeletons as first-class authoring references before creating a new full deck:

| archetype | best when | inspect for |
| --- | --- | --- |
| `templates/full-decks/ai-application-investment-thesis/index.html` | investment, pitch, thesis, market map, funding, product bet, or diligence-style decks | evidence extraction, thesis flow, market/peer pages, risk framing, pitch-style density |
| `templates/full-decks/enterprise-intelligence-transformation/index.html` | transformation, operating model, AI strategy, capability build, roadmap, governance, or board update decks | executive answer, flywheel/story model, capability heatmap, roadmap, governance, decision pages |
| `templates/full-decks/agent-technology-outlook/index.html` | agent technology outlook, AI platform strategy, agent architecture, technical market scan, interoperability, or governance decks | technical outlook pacing, green strategic style, architecture stack, risk framing, roadmap |
| `templates/full-decks/board-decision-recommendation/index.html` | board approval, executive committee decision, investment committee, funding, go/no-go, or strategic option recommendation decks | board decision pacing, option gates, value proof, risk conditions, explicit approval close |
| `templates/full-decks/technical-architecture-decision/index.html` | architecture option selection, platform path decision, build-vs-extend choice, or technical governance approval decks | architecture tradeoff logic, option matrix, capability coverage, proof path, architecture decision close |
| `templates/full-decks/technical-implementation-plan/index.html` | technical implementation, architecture rollout, platform modernization, integration, or delivery governance decks | target architecture, release gates, dependency/risk framing, implementation roadmap |
| `templates/full-decks/vendor-selection-scorecard/index.html` | vendor selection, platform evaluation, RFP synthesis, solution shortlist, or build/buy recommendation decks | requirements, shortlist comparison, weighted scorecard, TCO/risk, decision close |
| `templates/full-decks/workshop-decision-pack/index.html` | workshop, working session, leadership alignment, decision meeting, or planning pack decks | objectives, agenda, pre-read, option debate, decision capture, next steps |
| `templates/full-decks/cxo-steerco-progress-update/index.html` | CXO update, SteerCo, work progress, PMO, or board-adjacent status decks | KPI status, milestones, risks/blockers, decision asks, forward plan |
| `templates/full-decks/leadership-operating-plan/index.html` | LOP, annual operating plan, quarterly plan, budget cycle, operating rhythm, or initiative portfolio planning decks | KPI ambition, initiative portfolio, capacity tradeoffs, governance cadence, operating decisions |
| `templates/full-decks/investor-pitch-growth-story/index.html` | investor pitch, fundraising, growth story, product/company pitch, or board fundraising update decks | pitch pacing, traction page, market/GTM link, financial path, funding ask |
| `templates/full-decks/initiative-prioritization-recommendation/index.html` | initiative prioritization, strategic initiative recommendation, backlog funding, value-realization planning, or resource allocation decks | portfolio matrix, scorecard, business case, dependencies, roadmap, funding ask |
| `templates/full-decks/market-entry-growth-strategy/index.html` | market entry, growth strategy, regional expansion, segment prioritization, channel strategy, or category expansion decks | attractiveness, segment prioritization, entry options, competitive/channel read, roadmap |
| `templates/full-decks/pricing-commercial-strategy/index.html` | pricing strategy, packaging, discount governance, sales efficiency, revenue uplift, or commercial model redesign decks | pricing architecture, willingness/segment view, sensitivity, commercial governance |
| `templates/full-decks/org-design-operating-model/index.html` | organization design, operating model, role clarity, governance, RACI, or capability build decks | from-to shifts, target operating model, capability gaps, decision rights, migration path |
| `templates/full-decks/due-diligence-findings/index.html` | diligence findings, red-flag review, confirmatory tests, commercial/product/tech/operational diligence decks | findings readout, fact base, red flags, confirmatory tests, sensitivity, implications |
| `templates/full-decks/post-merger-integration/index.html` | PMI, Day 1, 100-day plan, synergy tracking, integration governance, or workstream planning decks | value capture, Day 1 readiness, workstreams, governance, risks, integration decisions |
| `templates/full-decks/turnaround-performance-improvement/index.html` | turnaround, cost reduction, margin improvement, cash improvement, operational reset, or urgent action plan decks | performance gap, root cause, improvement levers, cash/risk controls, recovery roadmap |
| `templates/full-decks/portfolio-review-capital-allocation/index.html` | business portfolio review, capital allocation, product portfolio, resource rebalancing, or build/hold/exit decks | portfolio health, allocation matrix, sensitivity, capital decisions |
| `templates/full-decks/mna-investment-decision/index.html` | acquisition, M&A, investment committee, strategic partnership, or capital allocation decision decks | rationale, value creation, risk, sensitivity, decision conditions |
| `templates/full-decks/advanced-analytics-readout/index.html` | advanced analytics, model result, driver analysis, cohort/segment readout, scenario analysis, or insight-to-action decks | method/data foundation, driver ranking, segment implications, sensitivity, actions |

Read the archetype's `README.md` sidecar before inspecting `index.html`. The sidecar is the fast index for visual traits, when-to-use guidance, storyline pattern, layout + component stack, source inspiration, evidence shape, related showcase patterns, flexible swaps, and when to diverge.

`examples/*` are independent public demo decks. `templates/full-decks/*` are agent-facing archetypes an agent may inspect when deciding how to structure a real deck. Keep archetype content fictional, generic, and reusable; never copy it verbatim into user work. Do not copy archetype footer text, placeholder brand marks, or deck-system labels into user decks.

## Archetype Selection Matrix

| user task | default route |
| --- | --- |
| Investment, thesis, diligence, product bet, pitch | Inspect `ai-application-investment-thesis`, then adapt the Investment Or Diligence Memo sequence. |
| Board approval, executive committee choice, investment committee, or go/no-go recommendation | Inspect `board-decision-recommendation`, then adapt the Board Decision Recommendation sequence. |
| Board or executive update | Inspect `enterprise-intelligence-transformation`, then adapt the Board Or Executive Update sequence. |
| Transformation, operating model, AI strategy, governance | Inspect `enterprise-intelligence-transformation`, then adapt the Operating Model Or Transformation sequence. |
| Market, competitive, customer, or trend scan | Inspect `ai-application-investment-thesis` for market evidence density, then adapt the Market Or Competitive Scan sequence. |
| Agent technology outlook, AI platform strategy, agent architecture, or technical market scan | Inspect `agent-technology-outlook`, then adapt the Technology Outlook Or Agent Architecture sequence. |
| Architecture option selection, platform path decision, or technical governance approval | Inspect `technical-architecture-decision`, then adapt the Technical Architecture Decision sequence. |
| Technical implementation, architecture rollout, or platform modernization | Inspect `technical-implementation-plan`, then adapt the Technical Implementation Plan sequence. |
| Vendor selection, RFP synthesis, solution shortlist, or build/buy decision | Inspect `vendor-selection-scorecard`, then adapt the Vendor Selection sequence. |
| Workshop or working session pack | Inspect `workshop-decision-pack`, then adapt the Workshop Pack sequence. |
| CXO, SteerCo, PMO, progress update, or board-adjacent status | Inspect `cxo-steerco-progress-update`, then adapt the CXO SteerCo Progress Update sequence. |
| LOP, annual operating plan, quarterly planning, budget cycle, operating rhythm, or initiative portfolio planning | Inspect `leadership-operating-plan`, then adapt the Leadership Operating Plan sequence. |
| Investor pitch, fundraising, growth story, product/company pitch, or board fundraising update | Inspect `investor-pitch-growth-story`, then adapt the Investor Pitch Growth Story sequence. |
| Initiative prioritization, initiative recommendation, backlog funding, strategic initiatives, or resource allocation | Inspect `initiative-prioritization-recommendation`, then adapt the Initiative Prioritization Recommendation sequence. |
| Market entry, growth strategy, regional expansion, segment prioritization, or category expansion | Inspect `market-entry-growth-strategy`, then adapt the Market Entry Growth Strategy sequence. |
| Pricing strategy, packaging, discount governance, sales efficiency, revenue uplift, or commercial model redesign | Inspect `pricing-commercial-strategy`, then adapt the Pricing Commercial Strategy sequence. |
| Org design, operating model, role clarity, governance, RACI, or capability build | Inspect `org-design-operating-model`, then adapt the Org Design Operating Model sequence. |
| Diligence findings, red-flag review, confirmatory tests, commercial/product/tech/operational diligence | Inspect `due-diligence-findings`, then adapt the Due Diligence Findings sequence. |
| PMI, Day 1, 100-day plan, synergy tracking, integration governance, or workstream planning | Inspect `post-merger-integration`, then adapt the Post-Merger Integration sequence. |
| Turnaround, cost reduction, margin improvement, cash improvement, operational reset, or urgent action plan | Inspect `turnaround-performance-improvement`, then adapt the Turnaround Performance Improvement sequence. |
| Business portfolio review, capital allocation, product portfolio, resource rebalancing, or build/hold/exit choices | Inspect `portfolio-review-capital-allocation`, then adapt the Portfolio Review Capital Allocation sequence. |
| M&A, acquisition, investment committee, strategic partnership, or capital allocation decision | Inspect `mna-investment-decision`, then adapt the M&A Investment Decision sequence. |
| Advanced analytics, data analysis readout, model result, driver analysis, or cohort/segment analysis | Inspect `advanced-analytics-readout`, then adapt the Advanced Analytics Readout sequence. |
| Strategy recommendation or market entry | Use the Strategy Recommendation sequence and inspect the most relevant archetype based on evidence type. |

## One-Shot Full-Deck Workflow

When the user gives limited context, do not ask them to design the deck page by page. Extract structure from the source material:

1. Identify the audience and likely decision: investor, board, executive, workshop, operating team, or diligence reader.
2. Build an evidence inventory: numeric values, percentages, rankings, comparisons, time periods, risks, customer/market claims, and named uncertainties.
3. Separate user-provided evidence from assumptions and any approved external data.
4. Group the evidence into 2-5 mutually distinct sections.
5. Pick the relevant deck archetype below and inspect the relevant `templates/full-decks/*` skeleton for pacing and page density.
6. Draft an answer-first storyline: answer, why now, proof, implications, risks, and next decisions.
7. Map every body slide to one layout, at least one component, and one fallback if evidence is insufficient. If a slide has data but no component, revise the plan before writing HTML.
8. Build, audit, package, and export.

Evidence-to-page routing:

- Numeric comparisons: table plus ranked bars, column chart, range plot, or metric strip.
- Peer or industry sets: comparison table, ranked bars, heatmap, quadrant, or scatter.
- Segments or business lines: table, stacked bars, donut/pie only when part-to-whole is clean.
- Risks and uncertainty: risk matrix register, pros-cons table, decision log, or callout paired with evidence.
- Timeline or execution: phase roadmap, milestone track, process flow, or stage gate.
- Qualitative thesis: outcome-support, framework-map, cause-effect, or numbered-list-grid.

Short full decks should rarely use pure section dividers. If the source has evidence for a section, open with an evidence-bearing page instead of a blank divider.

No-data fallback:

- If there are no numbers, do not create charts, metrics, rankings, ranges, or heatmaps.
- If there are no comparable records, do not create tables or matrices.
- If there are no dates or ordered phases, do not create timelines or roadmaps.
- Use qualitative layouts for sparse inputs, and label open questions as assumptions, risks, or decisions to validate.
- Do not browse for external data unless the user explicitly requests it or grants permission after being asked.

## Deck-Level Rules

- Start with the audience question and the answer.
- Build a storyline with 2-5 supporting pillars.
- Use content slide titles as answer-first messages.
- Put detailed backup, raw tables, or optional references in appendix pages.
- Avoid filler pages. Every page must either advance the argument, support a decision, or provide necessary reference.
- Apply one theme after the storyline and structure are stable.

## Full-Deck Showcase Validation

Use `templates/showcase/full-deck-operating-case-mono.html` and `templates/showcase/full-deck-operating-case-blue.html` to test whether independent components compose into a coherent 16:9 deck.

- The two showcase files must keep identical content and slide order; only the theme file changes.
- The case content is fictional and exists only to validate fit, visual balance, theme switching, and storyline continuity.
- Visible page headers should use neutral business language such as executive view, evidence, capabilities, target model, working rhythm, roadmap, decisions, team, and next steps.
- Do not expose internal component-family labels as page headers in user-facing full decks.
- Do not copy logos, company names, confidentiality marks, source notes, or footer text from reference materials.

The showcase sequence should cover at least one useful example from each major content job:

- Structure: framework, outcome-support, from-to, or decision model.
- Data: KPI strip, column/bar chart, heatmap, range, or table.
- Process: process flow, stage gate, filter, funnel, loop, or value chain.
- Time: roadmap, timeline, milestone, horizon, or journey.
- Text: quote, dense list, decision log, pros/cons, or numbered grid.
- People: contact/team page only when records are available or the page is explicitly marked showcase-only.

## Strategy Recommendation

Use when the user asks for a recommended direction, growth path, market entry, turnaround, or strategic choice.

Typical sequence:

1. Title page.
2. Executive summary with the answer and 2-4 reasons.
3. Situation/context: why the decision matters now.
4. Opportunity or problem diagnosis.
5. Option comparison or prioritization.
6. Recommendation and rationale.
7. Risks, mitigations, and open questions.
8. Roadmap or next steps.
9. Appendix or supporting analyses.

Useful components: `comparison-table`, `matrix-prioritization`, `metric-strip`, `chart-bars`, `ranked-bars`, `roadmap-swimlane`, `callout`.

## Board Or Executive Update

Use when the audience needs a concise status read and decisions.

Typical sequence:

1. Title page.
2. Executive summary: what changed, what matters, what decisions are needed.
3. KPI snapshot.
4. Progress against priorities.
5. Key risks or blockers.
6. Decision pages.
7. Forward plan.
8. Appendix.

Useful components: `metric-strip`, `data-dashboard`, `table`, `heatmap`, `roadmap-swimlane`, `callout`.

## Board Decision Recommendation

Use when the audience must approve, fund, stop, gate, or choose a strategic option. This is different from a board update: the deck should drive one explicit decision, not merely synchronize status.

Typical sequence:

1. Title page.
2. Recommendation answer and approval ask.
3. Option gate score or weighted evidence.
4. Value bridge, business case, or approval conditions.
5. Risks, mitigations, and board gates.
6. Decision log, owners, and next checkpoint.
7. Appendix or supporting analyses.

Useful components: `outcome-support`, `metric-strip`, `checkmark-bar-table`, `weighted-scorecard`, `waterfall-bridge`, `sensitivity-grid`, `risk-matrix-register`, `decision-log`, `phase-meeting-plan`.

## CXO SteerCo Progress Update

Use when the audience needs a status read, sponsor decisions, blocker resolution, or progress against an operating plan.

Typical sequence:

1. Title page.
2. Executive status: what changed, what is at risk, and what decisions are needed.
3. KPI snapshot.
4. Progress vs plan and milestone status.
5. Risks, blockers, and owner actions.
6. Decision asks.
7. Forward plan and next governance cycle.
8. Appendix or open items.

Useful components: `metric-strip`, `milestone-track`, `risk-matrix-register`, `decision-log`, `phase-roadmap`, `dense-list`.

## Leadership Operating Plan

Use when the audience needs to approve priorities, KPIs, initiative funding, budget/capacity tradeoffs, governance cadence, or the next operating cycle.

Typical sequence:

1. Title page.
2. Operating answer: what leaders should fund, protect, gate, or defer.
3. KPI ambition and performance snapshot.
4. Initiative portfolio and prioritization.
5. Budget, capacity, and resource tradeoffs.
6. Risks, controls, and dependencies.
7. Governance cadence and decision rights.
8. Decisions and next cycle.

Useful components: `metric-strip`, `portfolio-prioritization-matrix`, `comparison-table`, `raci-governance-grid`, `risk-matrix-register`, `decision-log`.

## Investor Pitch Growth Story

Use when the audience is evaluating a fundraising story, growth narrative, product/company pitch, or board fundraising update.

Typical sequence:

1. Title page.
2. Investment answer: why this company can compound now.
3. Problem and customer urgency.
4. Solution and product wedge.
5. Traction and customer proof.
6. Market and go-to-market path.
7. Business model and financial path.
8. Funding ask and next milestones.

Useful components: `metric-strip`, `outcome-support`, `ranked-bars`, `comparison-table`, `phase-roadmap`, `sensitivity-grid`, `decision-log`.

## Initiative Prioritization Recommendation

Use when the audience must choose which initiatives to fund, gate, sequence, defer, or stop.

Typical sequence:

1. Title page.
2. Recommendation answer.
3. Initiative inventory and constraints.
4. Prioritization matrix or weighted scorecard.
5. Business case and sensitivity.
6. Dependencies, risks, and mitigation.
7. Roadmap and resource ask.
8. Decision close.

Useful components: `portfolio-prioritization-matrix`, `weighted-scorecard`, `sensitivity-grid`, `risk-matrix-register`, `phase-roadmap`, `decision-log`.

## Technology Outlook Or Agent Architecture

Use when the user asks for a technology outlook, platform strategy, architecture recommendation, agent roadmap, interoperability view, or technical market scan.

Typical sequence:

1. Title page.
2. Executive answer: what should change and why now.
3. Market or capability signal.
4. Architecture shift or maturity model.
5. Stack or operating model.
6. Interoperability and ecosystem implications.
7. Value pools or priority workflows.
8. Platform choices and build-vs-buy.
9. Risks and governance controls.
10. Roadmap and decisions.
11. Evidence base or appendix.

Useful components: `metric-strip`, `framework-map`, `process-flow`, `comparison-table`, `ranked-bars`, `timeline`, `risk-matrix-register`, `phase-roadmap`, `decision-log`, `outcome-support`.

## Market Entry Growth Strategy

Use when the user asks where to play, which segment or region to prioritize, how to enter, or how to sequence growth.

Typical sequence:

1. Title page.
2. Growth answer and recommended beachhead.
3. Market attractiveness and demand signal.
4. Customer or segment prioritization.
5. Competitive and channel read.
6. Entry option decision.
7. Risks and prerequisites.
8. Entry roadmap and next decisions.

Useful components: `metric-strip`, `ranked-bars`, `comparison-table`, `portfolio-prioritization-matrix`, `risk-matrix-register`, `phase-roadmap`.

## Pricing Commercial Strategy

Use when the user needs to set pricing, packaging, discount governance, sales motion, or commercial model changes.

Typical sequence:

1. Title page.
2. Commercial answer.
3. Revenue leakage or margin opportunity.
4. Customer willingness and segment readout.
5. Pricing architecture and packaging choices.
6. Financial sensitivity.
7. Commercial governance and sales enablement.
8. Roadmap and decisions.

Useful components: `metric-strip`, `comparison-table`, `ranked-bars`, `sensitivity-grid`, `raci-governance-grid`, `phase-roadmap`, `decision-log`.

## Org Design Operating Model

Use when the user needs role clarity, decision rights, governance forums, capabilities, or a target operating model.

Typical sequence:

1. Title page.
2. Operating model answer.
3. Design principles or from-to shifts.
4. Target operating model.
5. Capability gaps.
6. Decision rights and RACI governance.
7. Migration roadmap.
8. Decisions and open design questions.

Useful components: `from-to-multi`, `framework-map`, `heatmap`, `raci-governance-grid`, `process-flow`, `phase-roadmap`, `decision-log`.

## Technical Implementation Plan

Use when the user asks how to implement a target architecture, platform, product capability, integration, or technical operating model.

Typical sequence:

1. Title page.
2. Build answer and implementation principles.
3. Target architecture or implementation spine.
4. Integration and data plan.
5. Release model and gates.
6. Risks, controls, and dependencies.
7. Roadmap.
8. Architecture and delivery decisions.

Useful components: `framework-map`, `comparison-table`, `process-flow`, `risk-matrix-register`, `phase-roadmap`, `decision-log`.

## Technical Architecture Decision

Use when the audience must choose the architecture path, platform pattern, integration model, or technical governance default before implementation planning begins.

Typical sequence:

1. Title page.
2. Architecture recommendation and decision frame.
3. Option comparison by control, reuse, speed, and burden.
4. Capability coverage and unresolved gaps.
5. Proof path across product, platform, risk, and operations.
6. Decisions, proof checkpoints, and scale trigger.
7. Appendix or detailed requirements.

Useful components: `input-process-output-layers`, `matrix-table`, `weighted-scorecard`, `capability-coverage-map`, `heatmap`, `swimlane-process-map`, `phase-roadmap`, `decision-log`, `phase-meeting-plan`.

## Vendor Selection Or Build/Buy Recommendation

Use when the user needs to select, pilot, negotiate with, or reject a vendor, platform, or solution option.

Typical sequence:

1. Title page.
2. Recommendation and decision conditions.
3. Requirements and criteria.
4. Shortlist comparison.
5. Weighted scorecard.
6. Commercial, TCO, and risk readout.
7. Implementation fit and pilot gate.
8. Decision close.

Useful components: `weighted-scorecard`, `comparison-table`, `sensitivity-grid`, `risk-matrix-register`, `decision-log`, `pros-cons-table`.

## Market Or Competitive Scan

Use when the user provides market facts, competitor information, customer segments, or trend evidence.

Typical sequence:

1. Title page.
2. Executive summary.
3. Market size/growth or demand signal.
4. Segment or customer analysis.
5. Competitor or alternative comparison.
6. Implications for strategy.
7. Priority opportunities.
8. Next analyses or decisions.

Useful components: `chart-bars`, `ranked-bars`, `scatter-plot`, `comparison-table`, `matrix-prioritization`, `table`.

## Operating Model Or Transformation

Use when the deck explains organizational changes, processes, capabilities, workstreams, or implementation.

Typical sequence:

1. Title page.
2. Case for change.
3. Current-state diagnosis.
4. Target-state principles or operating model.
5. Capability or maturity assessment.
6. Workstream roadmap.
7. Governance, roles, and decision cadence.
8. Risks and dependencies.
9. Next steps.

Useful components: `heatmap`, `roadmap-swimlane`, `process/flow layouts`, `comparison-table`, `profile`, `table`.

## Workshop Pack

Use when the deck supports a meeting, workshop, or working session.

Typical sequence:

1. Title page.
2. Meeting objectives.
3. Workshop agenda.
4. Pre-read context.
5. Discussion pages or exercises.
6. Decision capture.
7. Next steps and owners.
8. Appendix.

Useful components: `objective-list`, `objective-summary`, `agenda-table`, `simple-agenda-grid`, `table`, `callout`.

## Due Diligence Findings

Use when the audience needs a findings-led evidence readout, red flags, confirmatory tests, and implications for proceed/pause/reprice decisions.

Typical sequence:

1. Title page.
2. Diligence answer.
3. Key findings and fact base.
4. Red flags and risk register.
5. Confirmatory tests.
6. Scenario or sensitivity.
7. Recommendation implications.
8. Next diligence gate.

Useful components: `outcome-support`, `comparison-table`, `risk-matrix-register`, `weighted-scorecard`, `sensitivity-grid`, `decision-log`.

## Post-Merger Integration

Use when the user needs a Day 1, 100-day, synergy tracking, integration governance, or workstream planning deck.

Typical sequence:

1. Title page.
2. Integration answer.
3. Value capture priorities.
4. Day 1 readiness.
5. Workstream plan.
6. Governance and decision rights.
7. Risks and dependencies.
8. 100-day roadmap and decisions.

Useful components: `metric-strip`, `phase-roadmap`, `raci-governance-grid`, `risk-matrix-register`, `comparison-table`, `decision-log`.

## Turnaround Performance Improvement

Use when the user needs urgent performance recovery, cost reduction, margin improvement, cash improvement, or operational reset.

Typical sequence:

1. Title page.
2. Turnaround answer.
3. Performance gap and root causes.
4. Quick wins and structural levers.
5. Cash and risk controls.
6. Recovery roadmap.
7. Governance cadence.
8. Decision ask.

Useful components: `metric-strip`, `cause-effect`, `portfolio-prioritization-matrix`, `sensitivity-grid`, `risk-matrix-register`, `phase-roadmap`, `decision-log`.

## Portfolio Review Capital Allocation

Use when the user needs to allocate capital or management attention across businesses, products, regions, or initiatives.

Typical sequence:

1. Title page.
2. Portfolio answer: build, hold, harvest, or exit.
3. Portfolio health snapshot.
4. Growth/profitability or value/efficiency map.
5. Strategic roles and capital choices.
6. Scenario or sensitivity.
7. Risks and dependencies.
8. Allocation decisions and next review.

Useful components: `metric-strip`, `portfolio-prioritization-matrix`, `comparison-table`, `sensitivity-grid`, `risk-matrix-register`, `decision-log`.

## Advanced Analytics Readout

Use when the user needs to explain analytical results, model output, driver analysis, segment/cohort patterns, or scenario implications.

Typical sequence:

1. Title page.
2. Analytical answer and business implication.
3. Method and data foundation.
4. Headline patterns or KPI results.
5. Driver analysis.
6. Segment or cohort readout.
7. Scenario or sensitivity.
8. Actions, owners, and next tests.

Useful components: `metric-strip`, `comparison-table`, `ranked-bars`, `scatter-plot`, `sensitivity-grid`, `decision-log`, `callout`.

## Investment Or Diligence Memo

Use when the deck evaluates an investment, acquisition, product bet, or major resource allocation.

Typical sequence:

1. Title page.
2. Investment thesis or answer.
3. Market attractiveness.
4. Company/product position.
5. Financial or operating evidence.
6. Key risks.
7. Valuation, scenarios, or sensitivity if provided.
8. Recommendation and next steps.
9. Appendix.

Useful components: `metric-strip`, `chart-bars`, `waterfall-bridge`, `comparison-table`, `table`, `callout`.

## M&A Investment Decision

Use when the deck recommends whether to acquire, invest, partner, continue diligence, or stop.

Typical sequence:

1. Title page.
2. Decision answer.
3. Strategic rationale.
4. Target attractiveness or option scorecard.
5. Value creation thesis or value bridge.
6. Financial and operating evidence.
7. Risks and diligence tests.
8. Sensitivity and downside case.
9. Recommendation and conditions.

Useful components: `weighted-scorecard`, `waterfall-bridge`, `comparison-table`, `risk-matrix-register`, `sensitivity-grid`, `decision-log`.
