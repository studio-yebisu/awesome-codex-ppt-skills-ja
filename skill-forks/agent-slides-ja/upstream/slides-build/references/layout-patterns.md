# Layout Patterns (slides ops)

Concrete patterns for composing visually rich slides using slides ops. Each pattern shows the exact ops sequence — copy and adapt for your content.

---

## Card Pattern — Parallel Items

Use for 2-4 parallel concepts, capabilities, or categories. Each card gets a background rectangle + accent bar + header + body.

**Education:** Cards signal "these items are peers of equal weight." If one card has 5 bullets and another has 2, the slide looks unbalanced — either equalize depth or split the heavy card into its own slide. The accent bar color can vary per card to encode category (use brand palette in order), or stay uniform to signal equal priority.

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 0.7, "top": 2.1, "width": 3.3, "height": 3.5, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_rectangle", "slide_index": 3, "left": 0.7, "top": 2.1, "width": 3.3, "height": 0.06, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 3, "text": "Card Title", "left": 0.85, "top": 2.3, "width": 3.0, "height": 0.4, "font_size": 16, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 3, "text": "Card body description goes here with specific details.", "left": 0.85, "top": 2.75, "width": 3.0, "height": 2.5, "font_size": 14, "font_color": "333333"}
]
```

Repeat at `left: 4.2`, `left: 7.7` for 3-column layout (each card width ~3.3").

For 2-column: `left: 0.7` (width 5.2) and `left: 6.1` (width 5.2).

---

## Number Badge Pattern — Ordered Steps

Use for 3-5 sequential steps or numbered items. Each step gets a colored circle with number + title + description.

**Education:** Numbers imply sequence and dependency — Step 2 follows Step 1. If items can happen in any order, use cards instead. Keep titles to 3-4 words (verb + noun) for scannability. If you need more than 5 steps, group into phases first.

```json
[
  {"op": "add_oval", "slide_index": 4, "left": 0.7, "top": 2.2, "width": 0.4, "height": 0.4, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 4, "text": "1", "left": 0.7, "top": 2.2, "width": 0.4, "height": 0.4, "font_size": 18, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 4, "text": "Step Title", "left": 1.25, "top": 2.2, "width": 4.5, "height": 0.35, "font_size": 16, "bold": true, "font_color": "333333"},
  {"op": "add_text", "slide_index": 4, "text": "Description of what this step involves.", "left": 1.25, "top": 2.55, "width": 4.5, "height": 0.4, "font_size": 14, "font_color": "575757"}
]
```

Repeat at `top: 3.2`, `top: 4.2`, etc. for subsequent steps (spacing ~1.0" per step).

---

## KPI Row Pattern — Big Numbers

Use for 3-4 key metrics at the top of a slide. Big number + label underneath.

**Education:** KPIs work best as a header row above detailed content (charts, cards, or tables). Each KPI answers one question: "What is the headline number?" Keep to 3-4 max — beyond that, none stand out. Use green for positive metrics, gray for neutral context. Always include a comparison frame (YoY, vs. target, vs. peers) in the label.

```json
[
  {"op": "add_text", "slide_index": 5, "left": 0.7, "top": 2.1, "width": 3.2, "height": 0.7, "text": "$4.2B", "font_size": 36, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 5, "left": 0.7, "top": 2.8, "width": 3.2, "height": 0.4, "text": "Total addressable market", "font_size": 14, "font_color": "575757"},
  {"op": "add_line_shape", "slide_index": 5, "x1": 4.1, "y1": 2.2, "x2": 4.1, "y2": 3.1, "color": "CCCCCC", "line_width": 0.5},
  {"op": "add_text", "slide_index": 5, "left": 4.3, "top": 2.1, "width": 3.2, "height": 0.7, "text": "3.2x", "font_size": 36, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 5, "left": 4.3, "top": 2.8, "width": 3.2, "height": 0.4, "text": "Revenue multiplier", "font_size": 14, "font_color": "575757"},
  {"op": "add_line_shape", "slide_index": 5, "x1": 7.7, "y1": 2.2, "x2": 7.7, "y2": 3.1, "color": "CCCCCC", "line_width": 0.5},
  {"op": "add_text", "slide_index": 5, "left": 7.9, "top": 2.1, "width": 3.2, "height": 0.7, "text": "+87%", "font_size": 36, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 5, "left": 7.9, "top": 2.8, "width": 3.2, "height": 0.4, "text": "YoY growth rate", "font_size": 14, "font_color": "575757"}
]
```

Use vertical `add_line_shape` dividers between KPIs for visual separation.

---

## Key Insight Callout Box

Use at the bottom of a data slide to highlight the main takeaway. Rounded rectangle with brand-color border.

**Education:** The callout box is the "so what" — the one sentence an executive takes away if they read nothing else. Place it at the bottom of data slides, chart slides, and comparison slides. It should state a conclusion, not describe the data. Bad: "Revenue grew 12%." Good: "At current trajectory, digital will surpass traditional by Q2 2027."

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 0.7, "top": 5.8, "width": 11.0, "height": 0.8, "fill_color": "F0FAF5", "corner_radius": 5000, "border_color": "29BA74", "border_width": 1.5},
  {"op": "add_text", "slide_index": 6, "text": "Key insight: Early movers capture 3x the market share of fast followers in regulated fintech", "left": 0.9, "top": 5.9, "width": 10.6, "height": 0.6, "font_size": 14, "bold": true, "font_color": "29BA74"}
]
```

---

## Timeline Pattern — Connected Milestones

Use for 3-5 milestones on a horizontal timeline. Line connector + circles at each point + labels.

**Education:** Timelines show "when" — use when the audience needs to understand sequencing and duration. Keep to 3-5 milestones; more than that and the labels overlap. For detailed project schedules with parallel workstreams, use the Gantt pattern from `process-patterns.md` instead. Alternate label positions (above/below the line) if milestone dates are close together.

```json
[
  {"op": "add_line_shape", "slide_index": 7, "x1": 1.5, "y1": 3.5, "x2": 11.0, "y2": 3.5, "color": "29BA74", "line_width": 2.0},
  {"op": "add_oval", "slide_index": 7, "left": 1.3, "top": 3.3, "width": 0.4, "height": 0.4, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 7, "text": "Q1 2026", "left": 0.8, "top": 3.8, "width": 1.4, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 7, "text": "Launch MVP\nCore banking APIs", "left": 0.8, "top": 4.1, "width": 1.4, "height": 0.6, "font_size": 11, "font_color": "575757"},
  {"op": "add_oval", "slide_index": 7, "left": 4.1, "top": 3.3, "width": 0.4, "height": 0.4, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 7, "text": "Q3 2026", "left": 3.6, "top": 3.8, "width": 1.4, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 7, "text": "Scale partnerships\n100+ agent integrations", "left": 3.6, "top": 4.1, "width": 1.4, "height": 0.6, "font_size": 11, "font_color": "575757"}
]
```

Repeat for each milestone at evenly spaced x positions along the line.

---

## Split-Panel with Callout Numbers

Use for data-heavy split-panel slides. Big numbers in the colored panel, structured content on the right.

**Education:** The colored panel is the "hook" — it should contain 1-2 attention-grabbing numbers that make the audience want to read the right panel for details. Keep left-panel text to big numbers + short labels only. Never put paragraphs in the colored panel. The right panel carries the structured argument (header+body pairs or cards).

```json
[
  {"op": "add_text", "slide_index": 8, "text": "$65B+", "left": 0.5, "top": 2.5, "width": 3.5, "height": 0.8, "font_size": 36, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 8, "text": "global AI spending\nin 2026", "left": 0.5, "top": 3.3, "width": 3.5, "height": 0.5, "font_size": 16, "font_color": "FFFFFF"},
  {"op": "add_line_shape", "slide_index": 8, "x1": 0.8, "y1": 4.2, "x2": 3.5, "y2": 4.2, "color": "FFFFFF", "line_width": 0.5},
  {"op": "add_text", "slide_index": 8, "text": "42%", "left": 0.5, "top": 4.5, "width": 3.5, "height": 0.6, "font_size": 28, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 8, "text": "CAGR through 2030", "left": 0.5, "top": 5.1, "width": 3.5, "height": 0.4, "font_size": 14, "font_color": "FFFFFF"}
]
```

Right panel content uses the standard header+body pattern with `font_color: "333333"`.

---

## SCQA Executive Summary

Structure an exec summary using Situation-Complication-Question-Answer with accent bars separating each section.

**Education:** SCQA is the Pyramid Principle's opening framework. Each section should be 1-2 sentences max. The Answer is your core recommendation — it should be specific and actionable, not vague. If the Answer takes more than 2 lines, it belongs on a separate recommendation slide. The green accent bars create visual rhythm; all four must be present for the framework to work.

```json
[
  {"op": "add_rectangle", "slide_index": 2, "left": 0.7, "top": 2.0, "width": 0.08, "height": 0.9, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "SITUATION", "left": 0.95, "top": 2.0, "width": 2.0, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "AI agents are proliferating but lack financial infrastructure.", "left": 0.95, "top": 2.3, "width": 10.5, "height": 0.5, "font_size": 15, "font_color": "333333"},
  {"op": "add_rectangle", "slide_index": 2, "left": 0.7, "top": 3.1, "width": 0.08, "height": 0.9, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "COMPLICATION", "left": 0.95, "top": 3.1, "width": 2.0, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "Without purpose-built banking, agents cannot transact, hold funds, or build credit.", "left": 0.95, "top": 3.4, "width": 10.5, "height": 0.5, "font_size": 15, "font_color": "333333"},
  {"op": "add_rectangle", "slide_index": 2, "left": 0.7, "top": 4.2, "width": 0.08, "height": 0.9, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "QUESTION", "left": 0.95, "top": 4.2, "width": 2.0, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "How do we build the financial rails that enable autonomous agent commerce?", "left": 0.95, "top": 4.5, "width": 10.5, "height": 0.5, "font_size": 15, "font_color": "333333"},
  {"op": "add_rectangle", "slide_index": 2, "left": 0.7, "top": 5.3, "width": 0.08, "height": 0.9, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "ANSWER", "left": 0.95, "top": 5.3, "width": 2.0, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 2, "text": "AgentBank: purpose-built banking infrastructure for AI agents with KYA, wallets, and credit.", "left": 0.95, "top": 5.6, "width": 10.5, "height": 0.5, "font_size": 15, "font_color": "333333"}
]
```

---

## Comparison Table with Header Bar

Use for side-by-side comparisons. Colored header row via rectangles + table below.

**Education:** Tables work best for structured comparisons with 3-6 rows and 2-3 columns. More than that and the text becomes too small. The colored header bar distinguishes this from a plain table and makes column headers scannable. If comparing just 2 options, consider a split-panel instead. For "us vs. them" comparisons, put "us" in the rightmost column (the eye finishes there).

```json
[
  {"op": "add_rectangle", "slide_index": 9, "left": 0.7, "top": 2.1, "width": 11.0, "height": 0.45, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 9, "text": "Dimension", "left": 0.8, "top": 2.12, "width": 2.5, "height": 0.4, "font_size": 14, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 9, "text": "Traditional Banks", "left": 3.5, "top": 2.12, "width": 3.8, "height": 0.4, "font_size": 14, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 9, "text": "AgentBank", "left": 7.5, "top": 2.12, "width": 4.0, "height": 0.4, "font_size": 14, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_table", "slide_index": 9, "left": 0.7, "top": 2.55, "width": 11.0, "height": 3.0, "rows": [["Identity", "KYC for humans", "KYA for agents + principals"], ["Accounts", "Manual onboarding", "API-first, sub-second"], ["Credit", "Credit scores", "Behavioral scoring"]]}
]
```

---

## 2x3 Grid Pattern — Six Items

Use for 6 parallel items that don't fit in a single row. Two rows of three cards.

**Education:** The 2x3 grid works when all 6 items are true peers (no hierarchy). If some items are more important, use a featured card (larger) + supporting grid instead. Keep card content brief — at this density, each card gets ~3.5" x 2.0", so use 13-14pt body text and limit to 2-3 lines per card.

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 10, "left": 0.7, "top": 2.0, "width": 3.6, "height": 2.0, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_rectangle", "slide_index": 10, "left": 0.7, "top": 2.0, "width": 3.6, "height": 0.06, "fill_color": "29BA74"},
  {"op": "add_icon", "slide_index": 10, "icon_name": "Target", "left": 0.9, "top": 2.2, "size": 0.55, "color": "29BA74"},
  {"op": "add_text", "slide_index": 10, "text": "Item Title", "left": 1.6, "top": 2.2, "width": 2.5, "height": 0.35, "font_size": 14, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 10, "text": "Brief description of this item with key details.", "left": 0.85, "top": 2.7, "width": 3.3, "height": 1.1, "font_size": 13, "font_color": "575757"}
]
```

Row 1 cards at `left: 0.7`, `left: 4.55`, `left: 8.4` (each width ~3.6", gap ~0.25").
Row 2 cards at same x positions, `top: 4.2` (gap ~0.2" between rows).

---

## Shape Ops Reference

| Op | Use case | Key params |
|---|---|---|
| `add_rectangle` | Card backgrounds, accent bars, header strips | `fill_color`, `border_color` |
| `add_rounded_rectangle` | Cards, callout boxes, containers | `fill_color`, `corner_radius`, `border_color` |
| `add_oval` | Number badges, bullet dots, status indicators | `fill_color` (use equal width/height for circle) |
| `add_line_shape` | Dividers, timeline connectors, separators | `x1,y1,x2,y2`, `color`, `line_width` |

All position values are in **inches**. Colors are 6-digit hex without `#`.
