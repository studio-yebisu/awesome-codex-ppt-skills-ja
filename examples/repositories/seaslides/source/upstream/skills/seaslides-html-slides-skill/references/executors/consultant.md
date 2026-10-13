# Executor Consultant -- Consulting Style

## Role Definition
Data-driven consulting style HTML slide executor, specializing in business reviews, performance reports, market analysis, and professional presentations.

## References
- `base.md` -- Common execution guidelines, phased generation workflow, slide type mapping
- `shared-standards.md` -- HTML/CSS technical constraints, layout system, browser export rules
- `components.md` -- Component catalog with classes and usage
- `layouts.md` -- Layout patterns with per-theme recommendations
- `template-designer.md` -- Theme design patterns and component architecture

---

## Complexity Level

> See `shared-standards.md` for the full layout and component system.

Consulting style **defaults to Rich** -- KPI dashboards, chart visualizations, data tables with professional formatting.

| Complexity | When to Use |
|------------|-------------|
| **Rich (default)** | Business reviews, performance reports, market analysis with full data visualization |
| **Canvas** | Premium consulting deliverables where every slide has unique visual composition |
| **Plain (override)** | Informal project updates, quick status reports, internal team briefings |

---

## Consultant-Specific Data Visualization Techniques

### 1. KPI Dashboard Design

> **Component reference**: See `components.md` for `.kpi-card` class definition.

**Usage pattern in content.html**:

```html
<section class="slide light" data-notes="Revenue exceeded target by 18%, driven by enterprise segment growth.">
  <div class="layout-title-body">
    <div class="title-area"><div class="h-md">Key Performance Indicators</div></div>
    <div class="body-area">
      <div class="layout-three-col">
        <div class="grid-item">
          <div class="kpi-card">
            <div class="kpi-label">Revenue</div>
            <div class="kpi-value">$12.5M</div>
            <div class="kpi-note">+15% YoY</div>
          </div>
        </div>
        <div class="grid-item">
          <div class="kpi-card">
            <div class="kpi-label">Market Share</div>
            <div class="kpi-value">28.5%</div>
            <div class="kpi-note">+3.2 pts</div>
          </div>
        </div>
        <div class="grid-item">
          <div class="kpi-card">
            <div class="kpi-label">Customer Satisfaction</div>
            <div class="kpi-value">92.3%</div>
            <div class="kpi-note">+5.1 pts</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

**Best Practices**: Use consistent accent color, show both absolute value and change, include comparison context (YoY, QoQ, vs target).

### 2. Chart Color Conventions

Use a **single-color depth gradient**: vary the fill opacity or lightness for different bars/segments. Apply varying lightness for bar charts, consistent stroke for timelines. Professional appearance, prints well in grayscale.

> **Chart implementation**: Use `.bar-chart`, `.vbar-chart`, and `.waterfall-chart` components from `components.md`. Use canonical numeric data geometry and verify a consistent scale.

### 3. Data Annotation Principles

- **Direct labeling** -- labels on data points via `.bar-value`, not in a separate legend
- **Contextual notes** -- brief explanations via `.insight-box` for key data insights
- **Threshold indicators** -- use `.callout-banner` or `.highlight-strip` for targets/benchmarks

### 4. Table Design

Use `.compare-table` with flexbox rows for predictable theme styling:

```html
<div class="compare-table">
  <div class="table-header">
    <span>Metric</span><span>2023</span><span>2024</span><span>Change</span>
  </div>
  <div class="table-row">
    <span>Revenue</span><span>$10.2M</span><span>$12.5M</span><span>+22.5%</span>
  </div>
  <div class="table-row">
    <span>Gross Margin</span><span>42.3%</span><span>45.1%</span><span>+2.8 pts</span>
  </div>
  <div class="table-row">
    <span>Net Income</span><span>$1.5M</span><span>$2.3M</span><span>+53.3%</span>
  </div>
</div>
```

> Use `.compare-table` with `.table-header` + `.table-row` (flexbox-based). Not `<table>` elements. Each cell is a separate `<span>`.

### 5. Callout Components

Use `.insight-box` for key observations and `.callout-banner` for full-width emphasis strips. Both are defined in `template.css` via `components.md`.

```html
<div class="insight-box">
  <div class="insight-title">Key Insight</div>
  <p>Revenue growth is accelerating in enterprise segment, offsetting SMB churn.</p>
</div>
```

---

## Consulting-Specific Layout Patterns

> **Component reference**: See `components.md` for all available component classes. See `layouts.md` for structural layout patterns.

| Pattern | Component | Use Case | Key Principle |
|---------|-----------|----------|---------------|
| **MECE Decomposition** | `.pipeline` or `.numbered-list` | Market segmentation, org breakdown | Mutually exclusive, collectively exhaustive steps |
| **Driver Tree** | `.numbered-list` with nested structure | Revenue/cost cause-and-effect | Root metric -> drivers -> sub-drivers |
| **Matrix / Quadrant** | `.matrix-2x2` | BCG matrix, priority mapping | 2x2 with labeled axes, distinct quadrant backgrounds |
| **Process Flow** | `.pipeline` | Customer journey, pipeline stages | Linear `.step` -> `.step-connector` -> `.step` flow |
| **Comparison** | `.compare-table` or `.compare-grid` | Feature/option evaluation | Structured rows with consistent columns |
| **Financial Analysis** | `.waterfall-chart` | Revenue bridge, cost breakdown | Positive/negative bars from baseline |

---

## Speaker Notes Style

### Analyst Tone

- Objective and factual
- Data-driven explanations
- Professional and measured
- Focus on insights and implications

### Data Presentation Guidelines

When presenting data: (1) State the number clearly, (2) Provide context (vs target/benchmark/prior), (3) Explain drivers, (4) Highlight implications. Use precise language (avoid "about", "around").

### Key Terminology

| Term | Meaning | Usage |
|------|---------|-------|
| **YoY** | Year-over-Year | "Revenue increased 15% YoY" |
| **QoQ** | Quarter-over-Quarter | "Margin improved 2 pts QoQ" |
| **pts** | Percentage points | "Market share grew 3 pts" |
| **CAGR** | Compound Annual Growth Rate | "5-year CAGR of 12%" |

---

## Common Use Cases

- **Business Review**: KPI dashboard (`.kpi-card` grid) -> Financial tables (`.compare-table`) -> Operational drivers (`.bar-chart`) -> Market matrix (`.matrix-2x2`) -> Challenges (`.numbered-list`) -> Action plan (`.pipeline`)
- **Market Analysis**: Overview -> Segmentation (`.pipeline` MECE) -> Competition (`.matrix-2x2`) -> Trends (`.bar-chart`, `.vbar-chart`) -> Opportunity (`.insight-box`) -> Recommendations
- **Performance Report**: KPI cards -> Metrics tables -> Variance (`.waterfall-chart`) -> Root cause (`.numbered-list`) -> Outlook -> Next steps

---

## Quality Checklist

> **Common checks**: See `base.md` for the full shared checklist.

**Consultant-specific checks**:
- [ ] Every `<section>` has `data-notes="..."` with meaningful speaker notes
- [ ] Every `<section>` has a mode class (`light`, `dark`, `hero light`, `hero dark`)
- [ ] No `<style>`, `<script>`, or `<link>` tags in content.html
- [ ] Inline styles conform to the canonical data-geometry allowlist
- [ ] All CSS classes verified against `template.css` and `components.md`
- [ ] Bar fills use permitted numeric geometry and match their labels/scales
- [ ] All images use relative `assets/` paths with meaningful `alt` text
- [ ] Chart colors follow single-color depth gradient (opacity variation)
- [ ] Tables use `.compare-table` with `.table-header` + `.table-row` (flexbox, not `<table>`)
- [ ] KPI cards use `.kpi-card` component class, not inline styling
- [ ] MECE principles applied to frameworks and segmentations
- [ ] Data annotations provide context (YoY, vs target, vs benchmark)
- [ ] Speaker notes use analyst tone with precise language
- [ ] Insights are data-driven, recommendations actionable
- [ ] Browser-exported PNG/SVG output matches the intended composition
- [ ] Repeated modes and layouts are intentional and content-driven
