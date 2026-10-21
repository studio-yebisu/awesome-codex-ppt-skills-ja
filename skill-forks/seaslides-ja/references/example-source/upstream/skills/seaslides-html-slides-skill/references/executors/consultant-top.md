# Executor Consultant Top -- Top-tier Consulting Style (MBB Level)

## Role Definition
MBB-level (McKinsey/Bain/BCG) top-tier consulting style HTML slide executor, specializing in executive briefings, board presentations, and strategic recommendations.

## References
- `base.md` -- Common execution guidelines, phased generation workflow, slide type mapping
- `shared-standards.md` -- HTML/CSS technical constraints, layout system, browser export rules
- `components.md` -- Component catalog with classes and usage
- `layouts.md` -- Layout patterns with per-theme recommendations
- `template-designer.md` -- Theme design patterns and component architecture

---

## Complexity Level

> See `shared-standards.md` for the full layout and component system.

MBB Consulting **defaults to Rich** -- SCQA framework with takeaway boxes, KPI dashboards, comparison tables, and chart suites.

| Complexity | When to Use |
|------------|-------------|
| **Rich (default)** | Board presentations, strategy reviews, investment decisions with full visual support |
| **Canvas** | Premium executive deliverables with unique per-slide visual composition (e.g., exhibit-style decks) |
| **Plain (override)** | Text-heavy strategy memos, internal discussion papers, quick executive updates |

---

## Template-Content Separation for MBB Slides

> **TCS**: Use CSS classes from `template.css`; allow inline style only for canonical numeric data geometry. See `shared-standards.md`.

### MBB Component Library

> **Component implementations**: See `components.md` for full class definitions of all components.

The template provides these MBB components via CSS classes:

| Component | CSS Classes | Usage in content.html |
|-----------|------------|----------------------|
| Takeaway box | `.highlight-strip` | Key conclusion with emphasis background |
| KPI card | `.kpi-card`, `.kpi-value`, `.kpi-label`, `.kpi-note` | Metric with label/value/change |
| Source footer | `.annotation-box` | Source attribution at slide bottom |
| Insight callout | `.insight-box`, `.insight-title` | Observation callout with accent border |
| Comparison table | `.compare-table`, `.table-header`, `.table-row` | Structured data comparison |
| Pillar card | `.feature-card`, `.feature-icon`, `.feature-title`, `.feature-desc` | Strategic framework element |

### Usage Pattern

Each content slide follows the MBB structure:

```html
<section class="slide light" data-notes="Revenue exceeded target by 18%, the strongest quarterly performance in three years.">
  <div class="layout-title-body">
    <div class="title-area">
      <div class="h-md">Revenue Growth Accelerated to 18% YoY, Exceeding Target</div>
    </div>
    <div class="body-area">
      <p><em>Enterprise segment drove 70% of incremental growth, validating the go-upmarket strategy.</em></p>
      <ul>
        <li>Enterprise revenue grew 32% YoY to $8.2M, adding 14 new logos</li>
        <li>SMB churn stabilized at 12%, down from 18% in Q2</li>
        <li>Gross margin expanded 280 bps through infrastructure optimization</li>
      </ul>
      <div class="highlight-strip">
        Recommendation: Increase enterprise sales headcount by 40% in H2 to capture the expanded pipeline.
      </div>
      <div class="annotation-box">
        <div class="annotation-content">Source: Internal financials, Q3 FY2024 | Confidential</div>
      </div>
    </div>
  </div>
</section>
```

---

## SCQA Framework

**Situation-Complication-Question-Answer** narrative structure for executive presentations:

| Element | Purpose | Timing | Content |
|---------|---------|--------|---------|
| **S - Situation** | Establish common ground | 20% | Current state, background |
| **C - Complication** | Introduce tension | 30% | Problem, challenge |
| **Q - Question** | Frame the issue | 10% | What should we do? |
| **A - Answer** | Provide solution | 40% | Recommendation, next steps |

### SCQA Implementation

Map each element to slides:

- **S** -> 1 slide max (brief context with `.insight-box`)
- **C** -> 1-2 slides (quantified problem with `.kpi-card` grid + `.highlight-strip` takeaway)
- **Q** -> 1 slide (clear actionable question in italic, `hero dark` mode for emphasis)
- **A** -> remaining slides (conclusion-first via `.highlight-strip` + specific recommendations with `.feature-card` pillars)

Keep Situation brief, Complication quantified, Question actionable, Answer decisive with time-bound actions.

---

## Data Contextualization

Never present raw data without context. Five comparison frameworks:

| Type | Description | Example |
|------|-------------|---------|
| **Time** | Compare to previous periods | "+22% YoY, highest growth in 5 years" |
| **Benchmark** | Compare to industry standards | "18.7% margin exceeds industry avg of 14.2%" |
| **Competitive** | Compare to key competitors | "28.5% share, leading by 8.3 pts" |
| **Target Gap** | Compare to goals | "92.3% satisfaction, 2.7 pts short of 95% target" |
| **Ranking** | Show relative position | "Rank #3 of 12, up from #5 last year" |

---

## Pyramid Principle

**Conclusion-first**: Main conclusion -> 3-4 supporting arguments (most important first) -> data/evidence for each -> connect to action. Every slide starts with its takeaway, not its analysis.

---

## MBB-Level Layout Patterns

| Pattern | Structure | Key Elements |
|---------|-----------|-------------|
| **Content Page** | `.layout-title-body` -> `.h-md` action title -> italic takeaway -> 3 bullets -> `.highlight-strip` -> `.annotation-box` | Action-oriented title, time-bound implications |
| **KPI Dashboard** | `.layout-title-body` -> `.layout-three-col` with 3 `.kpi-card` -> `.highlight-strip` | Label + value + change per card |
| **Two-Column Analysis** | `.layout-two-col` -> `.col-left` (current state) + `.col-right` (projected state) -> `.highlight-strip` | Before/after or current/target comparison |
| **Strategic Pillars** | `.layout-three-col` with 3 `.feature-card` -> `.highlight-strip` | Numbered pillars with title + goal + action |
| **Source Footer** | `.annotation-box` at bottom of `.body-area` | Source attribution + confidentiality notice |

---

## Extreme Simplicity

One core message per slide, max 3 supporting points. Every word earns its place. Generous whitespace. If content exceeds 3 bullets, split into multiple slides or move detail to appendix.

---

## Speaker Notes Style

**Executive briefing tone**: Concise, direct, action-oriented, confident but measured. Focus on implications, respect for time. Structure: Opening (purpose) -> 3 key messages -> supporting data -> implications -> specific recommendation -> next action.

---

## Common Use Cases

- **Board**: Executive summary (`.kpi-card` grid) -> KPI dashboard -> SCQA strategic opportunities (`.insight-box` + `.highlight-strip`) -> Risk (`.pros-cons` or `.compare-table`) -> Recommendation (`.feature-card` pillars) -> Next steps (`.pipeline`)
- **Strategy Review**: Situation (1 slide, `.insight-box`) -> Challenges (`.bar-chart`) -> Options (3 `.feature-card` pillars max) -> Recommended approach (`.highlight-strip`) -> Implementation (`.pipeline`) -> Resources (`.kpi-card` grid)
- **Investment Decision**: Opportunity (`.split-stat`) -> Market analysis (`.bar-chart`, `.matrix-2x2`) -> Financial KPIs (`.kpi-card` grid) -> Risk (`.compare-table`) -> Recommendation (`.highlight-strip`) -> Decision needed (action + deadline)

---

### Ghost Deck Test

Read ONLY slide titles in sequence. They should tell the complete argument:

> "Market Opportunity Reached $4.2B -> Competitive Landscape Favors First Movers -> Our Advantage: 2x Faster Execution -> Investment Thesis Yields 3.2x ROI -> Risk Mitigation Plan Covers Three Scenarios -> Recommendation: Proceed with Phase 1 by Q2"
>
> NOT: "Introduction -> Overview -> Details -> More Details -> Summary -> Q&A"

If titles do not convey a clear narrative, revise to be **action-oriented** conclusions.

---

## Quality Checklist

> **Common checks**: See `base.md` for the full shared checklist.

**Consultant-top-specific checks**:
- [ ] Every `<section>` has `data-notes="..."` with executive-appropriate speaker notes
- [ ] Every `<section>` has a mode class (`light`, `dark`, `hero light`, `hero dark`)
- [ ] No `<style>`, `<script>`, or `<link>` tags in content.html
- [ ] Inline styles conform to the canonical data-geometry allowlist
- [ ] All CSS classes verified against `template.css` and `components.md`
- [ ] Bar fills use permitted numeric geometry and match their labels/scales
- [ ] SCQA framework applied to narrative structure
- [ ] All data contextualized (time, benchmark, competitor, target, ranking)
- [ ] Pyramid principle followed (conclusion first on every slide)
- [ ] Each slide has one core message, max 3 supporting points
- [ ] Takeaway boxes (`.highlight-strip`) prominent and clear on key slides
- [ ] Speaker notes executive-appropriate (concise, action-oriented)
- [ ] Recommendations actionable and time-bound
- [ ] All components (`.highlight-strip`, `.kpi-card`, `.annotation-box`) use template CSS classes
- [ ] Browser-exported PNG/SVG output matches the intended composition
- [ ] Repeated modes and layouts are intentional and content-driven
- [ ] Action-oriented slide titles pass the Ghost Deck Test
- [ ] Source attribution (`.annotation-box`) on all data-driven slides

---

## Best Practices

- Start with conclusion, not analysis (Pyramid Principle)
- Contextualize every number (5 comparison types above)
- One message per slide, max 3 points, generous whitespace
- Recommendations must be specific, actionable, and time-bound
- Use template CSS classes; inline style is limited to canonical numeric data geometry (TCS)
- Slide titles are conclusions, not topics: "Revenue Grew 18%" not "Revenue Update"
- Use `.highlight-strip` as the MBB takeaway box on conclusion slides
- Use `.annotation-box` for source attribution and confidentiality notices
- Data slides (`.kpi-card`, `.bar-chart`) should be followed by breathing slides (`.big-quote`, `.split-stat`)
