# Executor General -- Creative Versatile Style

## Role Definition

Creative and versatile HTML slide executor, specializing in product introductions, training materials, proposal presentations, marketing campaigns, and other general-purpose scenarios. Emphasizes visual variety, audience engagement, and dynamic layouts while following TCS architecture.

## References

- `base.md` -- Common execution guidelines, phased generation workflow, slide type mapping
- `shared-standards.md` -- HTML/CSS technical constraints, layout system, browser export rules
- `components.md` -- Component catalog with classes and usage
- `layouts.md` -- Layout patterns with per-theme recommendations
- `design-guide.md` -- Five Laws, theme fidelity, rhythm, anti-patterns

---

## 1. Visual Impact Priority

The general executor prioritizes **visual impact** while maintaining readability:

- **Bold openings** -- Cover slide must make a statement. Use `.h-hero` with strong action title.
- **Visual variety** -- Vary layouts, modes, and component types when the content role changes; retain deliberate repetition for comparison or sequence.
- **Dramatic emphasis** -- Use `hero dark` mode for key numbers, pivotal statements, and turning points.
- **Image integration** -- Use relevant and user-required images prominently when they strengthen the message. `layout-split-hero` supports image+text pairings.
- **Component fitness** -- Use the component vocabulary that best expresses the content; do not add types merely to reach a quota.

---

## 2. Narrative Structure

### Recommended Arc: Hook/Context/Core/Shift/Takeaway

```
Slide 1:     Hook (hero dark)     -- Cover with bold title
Slide 2:     Context (light)      -- Problem statement or scene-setting
Slides 3-5:  Core (mixed)         -- Evidence, data, demonstrations
Slide 6:     Shift (hero dark)    -- Pivot, surprise, reframe
Slides 7-8:  Resolution (mixed)   -- Solution, proposal, recommendation
Slide 9:     Takeaway (light)     -- Key message, next steps
Slide 10:    Close (hero dark)    -- CTA or thank you
```

### Alternative Arcs

| Arc | Structure | Best For |
|-----|-----------|----------|
| **Problem-Solution** | Problem -> Evidence -> Solution -> Proof -> CTA | Product pitches, proposals |
| **Chronological** | Past -> Present -> Future | Progress updates, histories |
| **Compare-Contrast** | Old way -> Problems -> New way -> Benefits | Technology evaluations |
| **Journey** | Start -> Challenge -> Discovery -> Result | Case studies, personal talks |
| **Pyramid** | Conclusion -> Supporting points -> Details | Executive summaries |

---

## 3. Component Selection Guide

### By Content Type

| Content Type | Primary Components | Secondary |
|---|---|---|
| Key metrics | `.kpi-card`, `.stat-card`, `.split-stat` | `.bar-chart`, `.vbar-chart` |
| Process/flow | `.pipeline`, `.roadmap` | `.numbered-list`, `.timeline` |
| Comparison | `.pros-cons`, `.compare-table`, `.compare-grid` | `.matrix-2x2` |
| Story/narrative | `.big-quote`, `.pull-quote`, `.highlight-strip` | `.insight-box`, `.callout-banner` |
| Features/capabilities | `.feature-card`, `.icon-grid` | `.numbered-list`, `.definition-list` |
| Timeline/history | `.timeline`, `.roadmap` | `.numbered-list` |
| Financial/analysis | `.waterfall-chart`, `.funnel`, `.bar-chart` | `.kpi-card`, `.stat-card` |

### Density Matching

| Rhythm Tag | Appropriate Components |
|---|---|
| **anchor** | `.h-hero`, `.h-xl`, `.meta-row` -- minimal elements |
| **dense** | `.kpi-card` grids, `.bar-chart`, `.compare-table`, `.pipeline` |
| **breathing** | `.big-quote`, `.split-stat`, `.highlight-strip` -- single focal element |

---

## 4. editorial-magazine Patterns

When using editorial-magazine theme:

### Cover Slide
```html
<section class="slide hero dark" data-notes="...">
  <div class="layout-hero-center">
    <div class="h-hero">Bold Editorial Title</div>
    <div class="meta-row">Author Name | Date | Organization</div>
  </div>
</section>
```

### Content Slide (Two-Column with Pull Quote)
```html
<section class="slide light" data-notes="...">
  <div class="layout-two-col">
    <div class="col-left">
      <div class="h-md">Action Title States the Conclusion</div>
      <p>Body text with supporting evidence and narrative context.</p>
      <ul><li>Key point one</li><li>Key point two</li></ul>
    </div>
    <div class="col-right">
      <div class="pull-quote">
        <blockquote>"The key insight that changes everything."</blockquote>
      </div>
    </div>
  </div>
</section>
```

### Breathing Slide (Big Quote)
```html
<section class="slide hero dark" data-notes="...">
  <div class="layout-center-narrow">
    <div class="big-quote">
      <blockquote>"A provocative statement that reframes the narrative."</blockquote>
      <div class="cite">-- Attribution, Source</div>
    </div>
  </div>
</section>
```

---

## 5. swiss-international Patterns

When using swiss-international theme:

### Cover Slide
```html
<section class="slide hero dark" data-notes="...">
  <div class="layout-hero-center">
    <div class="h-hero">PRECISE TITLE</div>
    <div class="meta-row">Author | Date | Organization</div>
  </div>
</section>
```

### Data Slide (KPI Grid)
```html
<section class="slide light" data-notes="...">
  <div class="layout-title-body">
    <div class="title-area"><div class="h-md">Revenue exceeded target by 18%</div></div>
    <div class="body-area">
      <div class="layout-three-col">
        <div class="grid-item">
          <div class="kpi-card">
            <div class="kpi-value">$4.2M</div>
            <div class="kpi-label">Q3 Revenue</div>
          </div>
        </div>
        <div class="grid-item">
          <div class="kpi-card">
            <div class="kpi-value">+18%</div>
            <div class="kpi-label">vs Target</div>
          </div>
        </div>
        <div class="grid-item">
          <div class="kpi-card">
            <div class="kpi-value">92%</div>
            <div class="kpi-label">Retention</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## 6. Anti-Patterns for General Style

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| All slides `layout-title-body` | Looks like a Word document | Mix in `layout-two-col`, `layout-full-width`, hero slides |
| Sustained density causes fatigue | Audience fatigue | Add a breathing page at a meaningful narrative pause |
| Generic cover ("Presentation Title") | Weak first impression | Use an action title or provocative statement |
| Mode never changes when hierarchy needs contrast | Weak emphasis | Use dark or hero mode at meaningful transitions or emphasis points |
| Same component type feels accidental | AI-generated feeling | Introduce another form only when it communicates the content better |
| Wall of bullets | Not a presentation, it's a document | Convert to visual components or split slides |
