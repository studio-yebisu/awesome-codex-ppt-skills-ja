# Role: Strategist

## Core Mission

Receive source documents, perform content analysis and design planning, and output a **Content Design Specification** (`content_design_spec.md`).

> **Execution discipline**: The Strategist produces ONLY the design spec and confirmations -- no HTML code, no content.html, no template changes. Those are the Executor's job.

## Pipeline Context

| Previous Step | Current Step | Next Step |
|---------------|--------------|-----------|
| Theme files copied to project | **Strategist**: Nine Confirmations + Design Spec | Executor |

> **Technical foundation**: All HTML/CSS rules, viewport units, color systems, and class naming conventions live in `shared-standards.md`. This document does NOT duplicate that content.

---

## 1. Nine Confirmations (BLOCKING)

Complete every confirmation before writing the design spec. Infer from source material when possible; ask only when genuinely ambiguous.

### a. Page Format

- **Default**: 16:9 viewport (`100vw x 100vh` per slide, 1280x720 effective resolution)
- All themes are designed for this format

### b. Page Count

| Duration | General | Academic |
|----------|---------|----------|
| 5 min | 5-7 | 4-6 |
| 10 min | 8-12 | 8-10 |
| 15 min | 12-16 | 12-14 |
| 20 min | 16-20 | 15-18 |
| 30 min | 22-30 | 20-28 |
| 45 min | 30-40 | 30-40 |

**Rule of thumb**: General ~1 slide/min. Academic ~0.8/min (longer dwell).

Always include: cover (1), section dividers (1 per section), content slides, ending (1).

### c. Target Audience

Confirm (or infer):
1. **Who** -- role, expertise level
2. **Context** -- internal/external, formal/informal
3. **Core message** -- single takeaway the audience should remember

### d. Style Objective

| Style | Priority | Best For | Executor |
|-------|----------|----------|----------|
| **General** | Visual Impact | Product launch, training, marketing, proposals | `general.md` |
| **Academic** | Communication Clarity | Conference talks, thesis defense, lectures | `academic.md` |

#### Executor Selection

```
1. Academic/research purpose?
   YES -> academic.md
   NO  -> general.md
```

### e. Color Scheme

**From theme (default)**: Read the chosen template's CSS custom properties. Present existing palette for confirmation.

- **aurora-gradient**: 4 gradient palettes (Aurora, Sunset, Ocean, Forest)
- **cyber-neon**: 4 neon accents (Electric Cyan, Neon Magenta, Neon Blue, Neon Amber)
- **data-dashboard**: 5 status colors (green, amber, red, blue, purple)
- **editorial-magazine**: 5 preset palettes (ink-classic, indigo-porcelain, forest-ink, kraft-paper, dune)
- **ink-landscape**: 4 traditional palettes (Vermillion, Jade, Indigo, Gold)
- **mckinsey-minimal**: 4 corporate accents (Blue, Emerald, Coral, Violet)
- **swiss-international**: 4 accent colors (Klein Blue IKB, Lemon Yellow, Lime Green, Safety Orange)
- **ivory-theorem**: Warm ivory (#FFFEF8) bg, navy (#1B2A4A) headers, crimson (#C62828) accents
- **chalk-classroom**: Chalkboard green (#1B2B1F) bg, chalk white (#F5F0E8) text, yellow (#F4D35E) accents
- **bloomberg-dark**: Near-black (#0F0F12) bg, warm gray (#E8E4DF) text, scarlet (#E63946) accent

**Custom override**: Specify semantic CSS variable overrides that preserve the selected theme's palette roles and contrast contract (see `shared-standards.md` Section 6).

### f. Typography Plan

**From theme (default)**: Each template ships with font selections. Present for confirmation.

- **aurora-gradient**: Outfit (geometric sans) for all text. Bold weight 700 for display.
- **cyber-neon**: Space Grotesk (sans) + JetBrains Mono (mono for metrics). Weight 600-700.
- **data-dashboard**: Inter (sans) + JetBrains Mono (mono for numbers). Compact sizing.
- **editorial-magazine**: Serif headings (Playfair Display) + sans-serif body + monospace metadata.
- **ink-landscape**: Noto Serif SC (headings) + Noto Sans SC (body) + LXGW WenKai (verse). Cormorant Garamond for English headings.
- **mckinsey-minimal**: DM Sans (all text). Clean geometric. Weight 400-700.
- **swiss-international**: All sans-serif (Inter / Helvetica). Weight 200 for large text, 400-600 for small text.
- **ivory-theorem**: Playfair Display (serif headings) + Source Sans 3 (body) + JetBrains Mono (code). Scholarly weight 600-700.
- **chalk-classroom**: Caveat (handwritten headings) + Inter (body) + JetBrains Mono (code). Approachable weight 400-700.
- **bloomberg-dark**: DM Serif Display (headings) + Inter (body) + JetBrains Mono (code/numbers). Weight 400-700.

### g. Image Usage Approach

Determine the image strategy:

| Approach | When |
|----------|------|
| User-provided | Source material includes images |
| AI-generated | Conceptual illustrations needed |
| Web search | Specific real-world images needed |
| None | Data/text-only presentation |

If user-provided images exist, run: `python3 ${SKILL_DIR}/scripts/analyze_images.py <project_path>/assets`

### h. Slide Rhythm Plan

Tag every slide as `anchor` / `dense` / `breathing` and assign `hero dark` / `hero light` / `dark` / `light` mode. See Section 2 below for rhythm rules.

### i. Component Assignment

Map each slide to a specific layout pattern and component set from the theme. Reference `${SKILL_DIR}/references/layouts.md` and `${SKILL_DIR}/references/components.md`.

---

## 2. Content Analysis & Outline

### Analysis Steps

1. **Structure scan** -- identify major sections, logical flow
2. **Density assessment** -- classify each slide as high / medium / low density
3. **Slide type mapping** -- assign: cover, section, content, or ending
4. **Content chunking** -- apply "one idea per slide"
5. **Page rhythm tagging** -- assign `anchor` / `dense` / `breathing`

| Tag | Purpose | Example Slides |
|-----|---------|----------------|
| `anchor` | Key message, structural page | Cover, section dividers, conclusion |
| `dense` | Information-rich, data-heavy | Dashboards, comparison grids, tables |
| `breathing` | Narrative pause, single idea | Hero quote, big number, full-bleed image |

### Narrative Arcs (choose one)

**Arc A -- Hook/Context/Core/Shift/Takeaway**: General, product, storytelling.

```
Hook        -> 1 slide    : What makes them stop and listen?
Context     -> 1-2 slides : Why does this matter?
Core        -> 3-8 slides : The substance -- evidence, data, demonstrations
Shift       -> 1 slide    : The pivot -- challenge, surprise, reframe
Takeaway    -> 1-2 slides : What should they remember? What should they do?
```

**Arc B -- SCQA**: Consulting, executive. Situation -> Complication -> Question -> Answer.

**Arc C -- Funnel**: Academic. Broad context -> specific gap -> approach -> findings -> implications.

### Ghost Deck Test

Read ONLY slide titles in sequence -- they should tell the complete argument. If titles are topic labels ("Overview", "Market", "Technology"), rewrite as conclusions ("Mobile payments grew 3x", "Our SDK cuts integration from 6 weeks to 3 days").

### Rhythm Heuristics

- Review sustained `dense` runs and add breathing room when comprehension needs it
- Change mode when it supports hierarchy, not to satisfy a fixed cadence
- Place section dividers only at real narrative transitions
- Treat the opening and ending as anchors when that fits the narrative

### Mode Planning

- Choose a cover mode that supports the selected theme and opening tone
- Use hero modes for meaningful transitions or emphasis
- Choose content modes for readability and semantic contrast
- Keep a stable mode when continuity is more useful than variation

---

## 3. Per-Theme Layout Recommendations

Each theme has preferred layouts that best express its character.

### aurora-gradient

Prefers: `layout-hero-center`, `layout-two-col`, `layout-three-col`, `layout-center-narrow`

Character: Bold hero moments with gradient backgrounds. Rounded containers, generous whitespace. One hero element per slide. Gradient text for emphasis.

### cyber-neon

Prefers: `layout-title-body`, `layout-two-col`, `layout-three-col`, `layout-full-width`

Character: Terminal-inspired layouts with chrome headers. Sharp rectangles, dark backgrounds. Monospace metrics. Neon glow on focal elements.

### data-dashboard

Prefers: `layout-three-col`, `layout-four-grid`, `layout-full-width`, `layout-title-body`

Character: Dense, compact layouts optimized for data. Metric card grids, full-width data tables, dashboard chrome headers. Status-colored badges.

### editorial-magazine

Prefers: `layout-two-col`, `layout-split-hero`, `layout-mosaic`, `layout-center-narrow`

Character: Magazine-style asymmetry, editorial tension between text blocks and visual elements. Asymmetric column splits (never 50/50, prefer 30/70 or 40/60). Oversized pull-quotes. Mixed media composition.

### ink-landscape

Prefers: `layout-center-narrow`, `layout-two-col`, `layout-hero-center`, `layout-stacked-thirds`

Character: Generous negative space evoking rice paper. Seal stamps as section markers. Verse blocks in kaishu calligraphy. Chinese numerals for section numbering.

### mckinsey-minimal

Prefers: `layout-title-body`, `layout-two-col`, `layout-three-col`, `layout-full-width`

Character: Maximum whitespace, executive summary bars at top. Content flows top-down. Evidence-based structure with insight cards. Action-oriented closing.

### swiss-international

Prefers: `layout-title-body`, `layout-three-col`, `layout-four-grid`, `layout-full-width`

Character: Structured columns, clear hierarchy, grid precision. Use grid-based data layouts and clean card arrangements. Elements snap to 12-column grid. Left-aligned with generous whitespace.

### ivory-theorem

Prefers: `layout-title-body`, `layout-center-narrow`, `layout-two-col`, `layout-full-width`

Character: Scholarly journal layout with generous margins. Theorem and definition blocks as primary content vehicles. Structured arguments flow top-down. Citation callouts for references.

### chalk-classroom

Prefers: `layout-title-body`, `layout-two-col`, `layout-center-narrow`, `layout-stacked-thirds`

Character: Chalkboard lecture flow. Step-by-step progressions, annotation callouts, chalk-bordered cards. Whiteboard mode for contrast. Tutorial-style walkthroughs with numbered steps.

### bloomberg-dark

Prefers: `layout-three-col`, `layout-four-grid`, `layout-full-width`, `layout-title-body`

Character: Dense financial data layouts. KPI card grids, full-width data tables, horizontal bar charts. Dark backgrounds always. Source citation blocks for data provenance.

---

## 4. Design Spec Output

The content design spec MUST follow `${SKILL_DIR}/templates/content_design_spec_reference.md`:

| Section | Contents |
|---------|----------|
| **I. Project Information** | Title, format, page count, style, audience, date |
| **II. Theme Selection** | Theme name, palette/accent, CSS variable overrides |
| **III. Narrative Framework** | Arc choice, structure |
| **IV. Content Outline** | Per-slide table: number, title, type, rhythm, content points, components, slide mode |
| **V. Image Resource List** | Filename, purpose, status |
| **VI. Speaker Notes Plan** | Tone guidelines |

### Content Outline Table Format

```markdown
| Slide # | Type | Title | Rhythm | Mode | Layout | Components | Key Content |
|---------|------|-------|--------|------|--------|------------|-------------|
| 1 | hero | [title] | anchor | hero dark | layout-hero-center | .h-hero, .meta-row | subtitle, author |
| 2 | section | [name] | anchor | hero dark | layout-hero-center | .h-xl | |
| 3-N | content | [action titles] | dense/breathing | light/dark | varies | varies | bullets, data |
| N+1 | ending | Thank You | anchor | hero dark | layout-hero-center | .h-hero | contact info |
```

### Page Rhythm Planning Table

Before filling the slide outline, plan the rhythm pattern:

```
Example (12-slide deck):
| # | Rhythm    | Mode       | Rationale                    |
|---|-----------|------------|------------------------------|
| 1 | anchor    | hero dark  | Cover -- ceremonial opening  |
| 2 | breathing | light      | Context -- single statement  |
| 3 | dense     | light      | Core data -- KPI grid        |
| 4 | breathing | dark       | Insight -- big quote pause   |
| 5 | dense     | light      | Evidence -- bar charts       |
| 6 | dense     | light      | Process -- pipeline          |
| 7 | anchor    | hero dark  | Section divider              |
| 8 | dense     | light      | Comparison table             |
| 9 | breathing | dark       | Key statement -- emphasis    |
|10 | dense     | light      | Timeline -- milestones       |
|11 | breathing | hero light | Shift -- provocative reframe |
|12 | anchor    | hero dark  | Closing -- takeaway + CTA    |
```

---

## 5. Quality Checklist

- [ ] All nine confirmations completed
- [ ] Design spec follows template structure
- [ ] Theme explicitly named with an ID registered in `${SKILL_DIR}/templates/index.json`, not "default"
- [ ] Color scheme specified (palette name or hex values)
- [ ] Content outline has every slide with title + key content
- [ ] Page rhythm tags assigned to every slide
- [ ] Mode assigned to every slide; repeated modes are intentional
- [ ] Ghost Deck Test passes (titles tell the story)
- [ ] Slide count within budget for duration
- [ ] Image needs identified (if any)
- [ ] Component vocabulary supports the content without quota-filling

---

## 6. Handoff

The Executor receives `content_design_spec.md` and implements content.html. No further Strategist input needed unless the Executor flags an ambiguity.
