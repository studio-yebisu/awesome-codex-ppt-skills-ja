# Framework Patterns (slides ops)

Patterns for strategic frameworks, matrices, hierarchies, and assessment grids. Each pattern uses slides ops directly.

---

## SCQA Executive Summary with Hero Header

High-impact opening slide. Green header band with the recommendation, SCQA cards below with the Answer highlighted.

**Education:** The hero header states the answer immediately (Pyramid Principle). The SCQA cards provide the logical scaffolding. The Answer card is highlighted in green to draw the eye. Use this for the first content slide after the title.

```json
[
  {"op": "add_slide", "layout_name": "Title and Text"},
  {"op": "set_semantic_text", "slide_index": 1, "role": "title", "text": " "},
  {"op": "set_semantic_text", "slide_index": 1, "role": "body", "text": " "},
  {"op": "add_rectangle", "slide_index": 1, "left": 0, "top": 0, "width": 13.33, "height": 1.7, "fill_color": "03522D"},
  {"op": "add_rectangle", "slide_index": 1, "left": 8.5, "top": 0, "width": 4.83, "height": 1.7, "fill_color": "197A56"},
  {"op": "add_text", "slide_index": 1, "text": "Invest $50M in AI-banking to capture $400M+ in annual savings by 2029", "left": 0.7, "top": 0.3, "width": 11.9, "height": 1.1, "font_size": 22, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 1, "left": 0.7, "top": 2.0, "width": 11.9, "height": 1.0, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 1, "text": "SITUATION", "left": 0.9, "top": 2.08, "width": 1.5, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 1, "text": "AI is transforming financial operations across CPG, with $2.4T in supply chain finance now addressable.", "left": 2.5, "top": 2.08, "width": 9.9, "height": 0.8, "font_size": 14, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 1, "left": 0.7, "top": 3.15, "width": 11.9, "height": 1.0, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 1, "text": "COMPLICATION", "left": 0.9, "top": 3.23, "width": 1.5, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 1, "text": "Our manual processes cost $180M annually; peers have invested 3-5x more in AI-banking.", "left": 2.5, "top": 3.23, "width": 9.9, "height": 0.8, "font_size": 14, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 1, "left": 0.7, "top": 4.3, "width": 11.9, "height": 1.0, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 1, "text": "QUESTION", "left": 0.9, "top": 4.38, "width": 1.5, "height": 0.3, "font_size": 12, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 1, "text": "How do we close the gap and transform our financial operations before the window closes?", "left": 2.5, "top": 4.38, "width": 9.9, "height": 0.8, "font_size": 14, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 1, "left": 0.7, "top": 5.45, "width": 11.9, "height": 1.0, "fill_color": "03522D", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 1, "text": "ANSWER", "left": 0.9, "top": 5.53, "width": 1.5, "height": 0.3, "font_size": 12, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 1, "text": "Invest $50M across three pillars — Demand Sensing, Autonomous Logistics, and Intelligent Fulfillment.", "left": 2.5, "top": 5.53, "width": 9.9, "height": 0.8, "font_size": 14, "bold": true, "font_color": "FFFFFF"}
]
```

---

## 2x2 Matrix / SWOT

For strategic positioning, prioritization, effort-impact grids.

**Education:** Each quadrant must be genuinely distinct. The 2x2 works when two independent dimensions create four meaningful categories. If items don't naturally sort into quadrants, use columns instead.

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 0.5, "top": 1.6, "width": 5.9, "height": 2.3, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_rectangle", "slide_index": 4, "left": 0.5, "top": 1.6, "width": 5.9, "height": 0.06, "fill_color": "03522D"},
  {"op": "add_text", "slide_index": 4, "text": "Strengths", "left": 0.7, "top": 1.75, "width": 5.5, "height": 0.35, "font_size": 16, "bold": true, "font_color": "03522D"},
  {"op": "add_text", "slide_index": 4, "text": "Strong brand equity\nEstablished distribution network\nDedicated R&D capability", "left": 0.7, "top": 2.15, "width": 5.5, "height": 1.5, "font_size": 13, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 6.9, "top": 1.6, "width": 5.9, "height": 2.3, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_rectangle", "slide_index": 4, "left": 6.9, "top": 1.6, "width": 5.9, "height": 0.06, "fill_color": "6E6F73"},
  {"op": "add_text", "slide_index": 4, "text": "Weaknesses", "left": 7.1, "top": 1.75, "width": 5.5, "height": 0.35, "font_size": 16, "bold": true, "font_color": "6E6F73"},
  {"op": "add_text", "slide_index": 4, "text": "Legacy IT infrastructure\nFragmented data landscape\nLimited AI talent pipeline", "left": 7.1, "top": 2.15, "width": 5.5, "height": 1.5, "font_size": 13, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 0.5, "top": 4.1, "width": 5.9, "height": 2.3, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_rectangle", "slide_index": 4, "left": 0.5, "top": 4.1, "width": 5.9, "height": 0.06, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 4, "text": "Opportunities", "left": 0.7, "top": 4.25, "width": 5.5, "height": 0.35, "font_size": 16, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 4, "text": "Open banking API adoption\nAI cost curve declining 40% YoY\n$2.4T addressable market", "left": 0.7, "top": 4.65, "width": 5.5, "height": 1.5, "font_size": 13, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 6.9, "top": 4.1, "width": 5.9, "height": 2.3, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_rectangle", "slide_index": 4, "left": 6.9, "top": 4.1, "width": 5.9, "height": 0.06, "fill_color": "295E7E"},
  {"op": "add_text", "slide_index": 4, "text": "Threats", "left": 7.1, "top": 4.25, "width": 5.5, "height": 0.35, "font_size": 16, "bold": true, "font_color": "295E7E"},
  {"op": "add_text", "slide_index": 4, "text": "Peer investment acceleration\nRegulatory uncertainty in APAC\nTalent competition from fintechs", "left": 7.1, "top": 4.65, "width": 5.5, "height": 1.5, "font_size": 13, "font_color": "575757"}
]
```

---

## Harvey Ball Matrix

For capability/maturity assessments. Grid of colored circles indicating readiness levels.

**Education:** Use when evaluating multiple items across multiple criteria with discrete maturity levels. The colored dots give instant visual scanning. Keep to 4-6 rows and 3-5 columns maximum.

Harvey balls use colored ovals at intersections. Map scores to colors:

| Score | Color | Meaning |
|-------|-------|---------|
| 0 | `F2F2F2` | Not started |
| 1 | `D4DF33` | Early |
| 2 | `3EAD92` | In progress |
| 3 | `29BA74` | Advanced |
| 4 | `03522D` | Complete |

```json
[
  {"op": "add_rectangle", "slide_index": 5, "left": 0.7, "top": 1.8, "width": 11.9, "height": 0.4, "fill_color": "03522D"},
  {"op": "add_text", "slide_index": 5, "text": "Capability", "left": 0.8, "top": 1.82, "width": 3.0, "height": 0.35, "font_size": 12, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 5, "text": "Data", "left": 4.0, "top": 1.82, "width": 2.0, "height": 0.35, "font_size": 12, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 5, "text": "AI/ML", "left": 6.0, "top": 1.82, "width": 2.0, "height": 0.35, "font_size": 12, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 5, "text": "Cloud", "left": 8.0, "top": 1.82, "width": 2.0, "height": 0.35, "font_size": 12, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_text", "slide_index": 5, "text": "Security", "left": 10.0, "top": 1.82, "width": 2.0, "height": 0.35, "font_size": 12, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_text", "slide_index": 5, "text": "Demand Sensing", "left": 0.8, "top": 2.4, "width": 3.0, "height": 0.4, "font_size": 13, "font_color": "575757"},
  {"op": "add_oval", "slide_index": 5, "left": 4.75, "top": 2.47, "width": 0.3, "height": 0.3, "fill_color": "D4DF33"},
  {"op": "add_oval", "slide_index": 5, "left": 6.75, "top": 2.47, "width": 0.3, "height": 0.3, "fill_color": "F2F2F2"},
  {"op": "add_oval", "slide_index": 5, "left": 8.75, "top": 2.47, "width": 0.3, "height": 0.3, "fill_color": "29BA74"},
  {"op": "add_oval", "slide_index": 5, "left": 10.75, "top": 2.47, "width": 0.3, "height": 0.3, "fill_color": "03522D"},
  {"op": "add_line_shape", "slide_index": 5, "x1": 0.7, "y1": 2.9, "x2": 12.6, "y2": 2.9, "color": "E0E0E0", "line_width": 0.5}
]
```

Repeat rows at `top: 3.0`, `top: 3.6`, etc. Add a legend at the bottom mapping colors to maturity levels.

---

## Pyramid / Hierarchy Diagram

For strategy cascades (vision → strategy → tactics), value chains, organizational layers.

**Education:** Widening tiers = increasing specificity. The narrowest tier is the most abstract (vision); each tier below adds concrete detail. Use when showing how high-level intent cascades into execution.

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 4.2, "top": 1.8, "width": 5.0, "height": 0.9, "fill_color": "03522D", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 6, "text": "Vision & Mission", "left": 4.2, "top": 1.8, "width": 5.0, "height": 0.9, "font_size": 16, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 2.7, "top": 2.9, "width": 8.0, "height": 0.9, "fill_color": "197A56", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 6, "text": "Strategic Priorities", "left": 2.7, "top": 2.9, "width": 8.0, "height": 0.9, "font_size": 16, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 1.2, "top": 4.0, "width": 11.0, "height": 0.9, "fill_color": "29BA74", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 6, "text": "Operational Objectives", "left": 1.2, "top": 4.0, "width": 11.0, "height": 0.9, "font_size": 16, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 0.5, "top": 5.1, "width": 12.3, "height": 0.9, "fill_color": "3EAD92", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 6, "text": "Tactical Initiatives", "left": 0.5, "top": 5.1, "width": 12.3, "height": 0.9, "font_size": 16, "bold": true, "font_color": "FFFFFF"}
]
```

Add annotation text to the right of narrower tiers to explain what each level contains.

---

## Org Chart Cascade

For organizational hierarchies, team structures, reporting lines.

**Education:** Use when the audience needs to see who reports to whom and how teams are structured. Color tiers by level: darkest at top, lighter as you go down. Keep to 3 levels maximum on one slide.

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 7, "left": 5.2, "top": 1.8, "width": 3.0, "height": 0.6, "fill_color": "03522D", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 7, "text": "CEO", "left": 5.2, "top": 1.8, "width": 3.0, "height": 0.6, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_line_shape", "slide_index": 7, "x1": 6.7, "y1": 2.4, "x2": 6.7, "y2": 2.7, "color": "B0B0B0", "line_width": 1.0},
  {"op": "add_line_shape", "slide_index": 7, "x1": 2.2, "y1": 2.7, "x2": 11.2, "y2": 2.7, "color": "B0B0B0", "line_width": 1.0},

  {"op": "add_line_shape", "slide_index": 7, "x1": 2.2, "y1": 2.7, "x2": 2.2, "y2": 3.0, "color": "B0B0B0", "line_width": 1.0},
  {"op": "add_rounded_rectangle", "slide_index": 7, "left": 0.7, "top": 3.0, "width": 3.0, "height": 0.6, "fill_color": "197A56", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 7, "text": "CFO", "left": 0.7, "top": 3.0, "width": 3.0, "height": 0.6, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_line_shape", "slide_index": 7, "x1": 6.7, "y1": 2.7, "x2": 6.7, "y2": 3.0, "color": "B0B0B0", "line_width": 1.0},
  {"op": "add_rounded_rectangle", "slide_index": 7, "left": 5.2, "top": 3.0, "width": 3.0, "height": 0.6, "fill_color": "197A56", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 7, "text": "CTO", "left": 5.2, "top": 3.0, "width": 3.0, "height": 0.6, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_line_shape", "slide_index": 7, "x1": 11.2, "y1": 2.7, "x2": 11.2, "y2": 3.0, "color": "B0B0B0", "line_width": 1.0},
  {"op": "add_rounded_rectangle", "slide_index": 7, "left": 9.7, "top": 3.0, "width": 3.0, "height": 0.6, "fill_color": "197A56", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 7, "text": "COO", "left": 9.7, "top": 3.0, "width": 3.0, "height": 0.6, "font_size": 14, "bold": true, "font_color": "FFFFFF"}
]
```

Add third-level boxes below each second-level box with lighter fill (`29BA74` or `3EAD92`) and connecting lines.
