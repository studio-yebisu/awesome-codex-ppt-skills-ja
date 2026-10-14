# Intent playbooks

Select one primary intent. A secondary intent may alter emphasis, but must not create two competing decks. When the prompt is sparse, infer intent from the requested artifact, sources, audience vocabulary, and desired action; keep the inference explicit in the internal assumptions model and persist it in `brief.json.assumptions` when planning artifacts are enabled.

## Intent selection

| Intent | Audience question | Desired shift | Default delivery | Default density |
|---|---|---|---|---|
| `portfolio` | Can this person/team create the kind of value I need? | Unknown → credible and relevant | Live or async | Hybrid |
| `work-results` | What changed, why, and what should happen next? | Activity awareness → outcome confidence | Live review | Hybrid |
| `business-proposal` | Is this problem worth solving with this offer now? | Interest → decision or next step | Live + leave-behind | Hybrid |
| `sales` | Why change, why this solution, why now? | Status quo → qualified commitment | Live | Speaking/hybrid |
| `investor-pitch` | Is this a large, defensible opportunity this team can win? | Curiosity → diligence/commitment | Live + send-ahead | Hybrid |
| `strategy-decision` | Which option should we choose? | Ambiguity → aligned decision | Decision meeting | Reading/hybrid |
| `research-technical` | What did we learn and how certain are we? | Question → evidence-based understanding | Live conference/briefing | Speaking/hybrid |
| `teaching-workshop` | What can I understand and apply? | Unfamiliar → capable | Facilitated | Speaking |
| `keynote-launch` | What new possibility should I remember and support? | Attention → belief and momentum | Live stage | Speaking |
| `report-async` | What is the answer, evidence, and required action? | Information → independent understanding | Self-read | Reading |
| `template-system` | Can others create consistent decks safely? | Ad hoc slides → reusable system | Reusable asset | Reading |

## Portfolio

**Communication job:** establish a distinctive professional identity and prove relevant capability through selected work.

**Arc:** point of view or promise → compact identity → selected case studies → process and judgment → outcomes and proof → fit for the audience → contact or next step.

**Core slide roles:** cover with positioning, capability map, 2–4 case-study chapters, role/scope, problem, constraints, intervention, craft/process, result, testimonial or metric, lessons, fit, contact.

**Rules:**

- Curate; do not inventory everything.
- Structure each case as context → choice → execution → result → reflection.
- Separate personal contribution from team output.
- Show artifacts at a useful scale; avoid thumbnail walls.
- Use proof appropriate to the work: performance, adoption, quality, reach, time saved, stakeholder feedback, or process maturity.
- Make the final fit explicit for the role, client, or opportunity.

**Failure modes:** biography-first chronology, gallery without argument, fabricated outcomes, tiny mockups, repeated project layouts, or aesthetic polish that hides the actual contribution.

## Work/results review

**Communication job:** explain what changed, connect results to choices, surface learning, and secure next-step alignment.

**Arc:** mandate and baseline → targets → workstreams/decisions → outcome scorecard → causal explanation → lessons → risks → next priorities and asks.

**Core slide roles:** executive answer, before/after, KPI scorecard, trend, contribution tree, workstream proof, obstacle and response, lessons, forward plan, decision/ask.

**Rules:**

- Lead with outcomes, not a task log.
- Compare results with a baseline, target, forecast, or control where valid.
- Distinguish correlation, contribution, and causation.
- Explain shortfalls directly and convert them into a decision or learning.
- Keep detailed activity logs in an appendix.

**Failure modes:** vanity metrics, cherry-picked periods, unsupported causality, or celebration without implications.

## Business proposal and sales

**Communication job:** make a priority problem concrete, show a credible path to value, reduce perceived risk, and earn a defined commitment.

**Arc:** audience situation → costly complication → desired future → solution thesis → mechanism → proof → scope and plan → economics → risk handling → next step.

**Core slide roles:** priority/problem, cost of inaction, insight, solution, workflow/architecture, before/after, proof/case, implementation, responsibilities, timeline, pricing/options, risk/mitigation, decision.

**Rules:**

- Write in the buyer's language and operating reality.
- Sell the change before the product.
- Connect features to mechanisms, outcomes, and evidence.
- State assumptions behind ROI or payback.
- Make the ask specific: approve, pilot, introduce, schedule, or sign.

**Failure modes:** company-history opening, feature dump, generic market pain, logo wall without proof, fake ROI, buried commercials, or vague “thank you” close.

## Investor pitch

**Communication job:** make the opportunity, traction, business logic, right-to-win, and ask legible enough to earn the next diligence step.

**Arc:** vision → problem → solution/product → why now → market → traction → business model → go-to-market → competition/moat → team → financial logic/use of funds → ask.

**Rules:**

- Make market logic auditable; distinguish TAM, SAM, and initial reachable market.
- Use cohort, retention, growth, margin, pipeline, or engagement evidence appropriate to stage.
- State what is real, forecast, target, or scenario.
- Show competitors on decision-relevant dimensions; never claim “no competition.”
- Connect funding to milestones and de-risking.

**Failure modes:** inflated market multiplication, unlabeled forecasts, decorative hockey sticks, product screenshots without value, or an ask disconnected from milestones.

## Strategy and decision deck

**Communication job:** help a defined decision-maker choose among real alternatives using explicit criteria and consequences.

**Arc:** decision and deadline → context → objectives/criteria → diagnosis → options → evidence and trade-offs → recommendation → risks and reversibility → roadmap → decision required.

**Rules:**

- Put the decision question near the beginning.
- Show viable alternatives, including status quo when relevant.
- Separate facts, judgments, and assumptions.
- Apply consistent criteria across options.
- Make risk ownership and decision rights visible.
- Move deep analysis into appendices but keep the recommendation auditable.

**Failure modes:** recommendation disguised as neutral analysis, incomparable options, unexplained weights, or action plan before the decision logic.

## Research and technical presentation

**Communication job:** convey a question, method, evidence, interpretation, uncertainty, and implication at the audience's technical altitude.

**Arc:** why the question matters → prior knowledge/gap → research question → method → main result → interpretation → limitations/alternatives → implication → next inquiry.

**Rules:**

- Tailor de novo to the audience; do not paste a paper into slides.
- Keep the main thread visible and place methodological sidetracks in backup.
- Show actual data when possible; remove surrounding publication clutter.
- Distinguish observed result from interpretation.
- Label axes, units, sample, uncertainty, and comparison basis.
- End by zooming out to the original question.

**Failure modes:** title/bullet summaries of the paper, unreadable figures, unexplained notation, hidden limitations, or conclusions that exceed the evidence.

## Teaching and workshop

**Communication job:** create understanding, practice, feedback, and transfer—not merely exposure.

**Arc:** relevance → objectives → prior-knowledge activation → model → worked example → guided practice → feedback → independent application → recap/transfer.

**Rules:**

- State what learners will be able to do.
- Chunk concepts and progressively disclose complexity.
- Alternate explanation with examples and participation.
- Use advance organizers and retrieval prompts.
- Reserve time for practice; do not use slides as the full lesson script.

**Failure modes:** content dump, decorative activities, no feedback loop, or recap that only repeats headings.

## Keynote and product launch

**Communication job:** create a memorable reframing, demonstrate a new possibility, and channel energy into a specific belief or action.

**Arc:** human tension → antagonist/status quo → new frame → hero/solution → demonstration and proof → broader meaning → memorable close and call.

**Rules:**

- Use few words, strong stage images, concrete demonstrations, and deliberate pauses.
- Introduce only one major idea at a time.
- Contextualize numbers through comparisons without distorting them.
- Rehearse transitions, demos, handoffs, and failure contingencies.
- Design one genuine high point; do not manufacture spectacle on every slide.

**Failure modes:** “inspirational” vagueness, unearned hyperbole, auto-play risk, demo without customer meaning, or dense leave-behind copy on stage.

## Async report

**Communication job:** enable independent, non-linear reading while preserving the argument and required action.

**Arc:** executive answer → key drivers → evidence → implications → action plan → detailed appendix.

**Rules:**

- Make every page self-contained enough to survive forwarding.
- Use descriptive section labels, page numbers, source notes, and compact navigation cues.
- Permit higher density than a live talk, but preserve hierarchy and reading order.
- Include definitions and methodology near the relevant evidence or in linked appendix pages.

**Failure modes:** speaking-style fragments with no narration, hidden assumptions, unexplained charts, or a linear journey that breaks when pages are read out of order.

## Reusable template system

**Communication job:** encode stable identity and layout behavior without hard-coding one future story.

**Arc:** not applicable; design a system of roles.

**Required layout roles:** cover, section divider, title+visual, title+body, comparison, process, timeline, chart, table, quote, case study, summary, closing, and appendix. Add intent-specific roles only when repeated use is likely.

**Rules:**

- Separate brand tokens, structural layout rules, and sample content.
- Use real placeholders and document text/image budgets.
- Test short and long copy, portrait and landscape media, sparse and dense data.
- Do not leave sample text or assets in delivered layouts.
- Preserve native masters/placeholders when the chosen runtime supports them.

## Delivery-mode modifier

| Mode | Copy behavior | Visual behavior | Notes |
|---|---|---|---|
| `speaking` | Fragments and short claims | Large, singular, high contrast | Notes carry detail |
| `hybrid` | Concise but independently legible | Balanced evidence and whitespace | Notes add nuance |
| `reading` | Complete labels and supporting explanation | More structured density | Navigation and citations are prominent |

Do not combine speaking and reading density on the same slide. If both are required, create a live deck plus leave-behind or use notes/appendix deliberately.
