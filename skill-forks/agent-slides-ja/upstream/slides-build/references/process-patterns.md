# Process & Timeline Patterns (slides ops)

Patterns for process flows, timelines, roadmaps, stage gates, and Gantt-style visualizations.

---

## Chevron Flow (3-5 Sequential Phases)

Connected chevron shapes showing a sequential process where each phase feeds the next.

**Education:** The chevron shape inherently implies forward motion and dependency. Use when Phase B cannot start until Phase A completes. If phases can run in parallel, use columns instead. Each card below answers: "What happens here, and what does it produce that the next phase needs?"

Build with overlapping rectangles to simulate chevrons, or use detail cards below a connecting line:

```json
[
  {"op": "add_line_shape", "slide_index": 3, "x1": 0.7, "y1": 2.3, "x2": 12.6, "y2": 2.3, "color": "29BA74", "line_width": 3.0},

  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 0.5, "top": 1.6, "width": 2.3, "height": 0.55, "fill_color": "03522D", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 3, "text": "1  Assess", "left": 0.5, "top": 1.6, "width": 2.3, "height": 0.55, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 3.0, "top": 1.6, "width": 2.3, "height": 0.55, "fill_color": "197A56", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 3, "text": "2  Design", "left": 3.0, "top": 1.6, "width": 2.3, "height": 0.55, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 5.5, "top": 1.6, "width": 2.3, "height": 0.55, "fill_color": "29BA74", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 3, "text": "3  Build", "left": 5.5, "top": 1.6, "width": 2.3, "height": 0.55, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 8.0, "top": 1.6, "width": 2.3, "height": 0.55, "fill_color": "3EAD92", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 3, "text": "4  Deploy", "left": 8.0, "top": 1.6, "width": 2.3, "height": 0.55, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 10.5, "top": 1.6, "width": 2.3, "height": 0.55, "fill_color": "295E7E", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 3, "text": "5  Scale", "left": 10.5, "top": 1.6, "width": 2.3, "height": 0.55, "font_size": 14, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 0.5, "top": 2.7, "width": 2.3, "height": 3.5, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 3, "text": "Current state analysis\nPain point mapping\nData audit\nStakeholder interviews", "left": 0.65, "top": 2.85, "width": 2.0, "height": 3.2, "font_size": 12, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 3, "left": 3.0, "top": 2.7, "width": 2.3, "height": 3.5, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 3, "text": "Solution architecture\nVendor selection\nIntegration design\nSecurity review", "left": 3.15, "top": 2.85, "width": 2.0, "height": 3.2, "font_size": 12, "font_color": "575757"}
]
```

Repeat detail cards for remaining phases at `left: 5.5`, `left: 8.0`, `left: 10.5`.

---

## Stage Gate Process

Horizontal flow with colored gate boxes and arrow connectors for intake/approval workflows.

**Education:** Each gate represents a decision point — "go/no-go" before investing in the next phase. Use when the audience needs to see approval checkpoints. The gradient from dark to light implies increasing commitment.

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 0.5, "top": 1.6, "width": 2.8, "height": 1.0, "fill_color": "03522D", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 4, "text": "Gate 1\nConcept Review", "left": 0.5, "top": 1.6, "width": 2.8, "height": 1.0, "font_size": 13, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_text", "slide_index": 4, "text": "→", "left": 3.35, "top": 1.7, "width": 0.4, "height": 0.8, "font_size": 24, "bold": true, "font_color": "29BA74"},

  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 3.8, "top": 1.6, "width": 2.8, "height": 1.0, "fill_color": "197A56", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 4, "text": "Gate 2\nBusiness Case", "left": 3.8, "top": 1.6, "width": 2.8, "height": 1.0, "font_size": 13, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_text", "slide_index": 4, "text": "→", "left": 6.65, "top": 1.7, "width": 0.4, "height": 0.8, "font_size": 24, "bold": true, "font_color": "29BA74"},

  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 7.1, "top": 1.6, "width": 2.8, "height": 1.0, "fill_color": "29BA74", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 4, "text": "Gate 3\nPilot Approval", "left": 7.1, "top": 1.6, "width": 2.8, "height": 1.0, "font_size": 13, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_text", "slide_index": 4, "text": "→", "left": 9.95, "top": 1.7, "width": 0.4, "height": 0.8, "font_size": 24, "bold": true, "font_color": "29BA74"},

  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 10.4, "top": 1.6, "width": 2.8, "height": 1.0, "fill_color": "3EAD92", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 4, "text": "Gate 4\nScale Decision", "left": 10.4, "top": 1.6, "width": 2.8, "height": 1.0, "font_size": 13, "bold": true, "font_color": "FFFFFF"},

  {"op": "add_rounded_rectangle", "slide_index": 4, "left": 0.5, "top": 2.9, "width": 2.8, "height": 3.3, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 4, "text": "Criteria:", "left": 0.65, "top": 3.0, "width": 2.5, "height": 0.3, "font_size": 12, "bold": true, "font_color": "03522D"},
  {"op": "add_text", "slide_index": 4, "text": "Strategic alignment\nMarket validation\nTechnical feasibility\nResource availability", "left": 0.65, "top": 3.35, "width": 2.5, "height": 2.6, "font_size": 12, "font_color": "575757"}
]
```

Repeat detail cards below each gate at matching x positions.

---

## Gantt-Style Horizontal Bars

For project schedules with overlapping timelines and milestones.

**Education:** Use when multiple workstreams run in parallel with different start/end dates. The horizontal layout makes duration and overlap immediately visible. Add diamond milestones for key decision points.

```json
[
  {"op": "add_text", "slide_index": 5, "text": "Q1", "left": 3.5, "top": 1.5, "width": 2.2, "height": 0.3, "font_size": 10, "font_color": "575757"},
  {"op": "add_text", "slide_index": 5, "text": "Q2", "left": 5.7, "top": 1.5, "width": 2.2, "height": 0.3, "font_size": 10, "font_color": "575757"},
  {"op": "add_text", "slide_index": 5, "text": "Q3", "left": 7.9, "top": 1.5, "width": 2.2, "height": 0.3, "font_size": 10, "font_color": "575757"},
  {"op": "add_text", "slide_index": 5, "text": "Q4", "left": 10.1, "top": 1.5, "width": 2.2, "height": 0.3, "font_size": 10, "font_color": "575757"},
  {"op": "add_line_shape", "slide_index": 5, "x1": 3.5, "y1": 1.85, "x2": 12.3, "y2": 1.85, "color": "E0E0E0", "line_width": 0.5},

  {"op": "add_text", "slide_index": 5, "text": "Data Platform", "left": 0.5, "top": 2.0, "width": 2.8, "height": 0.4, "font_size": 12, "font_color": "575757"},
  {"op": "add_rounded_rectangle", "slide_index": 5, "left": 3.5, "top": 2.05, "width": 4.4, "height": 0.3, "fill_color": "03522D", "corner_radius": 8000},

  {"op": "add_text", "slide_index": 5, "text": "AI Models", "left": 0.5, "top": 2.5, "width": 2.8, "height": 0.4, "font_size": 12, "font_color": "575757"},
  {"op": "add_rounded_rectangle", "slide_index": 5, "left": 5.7, "top": 2.55, "width": 6.6, "height": 0.3, "fill_color": "197A56", "corner_radius": 8000},

  {"op": "add_text", "slide_index": 5, "text": "Banking APIs", "left": 0.5, "top": 3.0, "width": 2.8, "height": 0.4, "font_size": 12, "font_color": "575757"},
  {"op": "add_rounded_rectangle", "slide_index": 5, "left": 3.5, "top": 3.05, "width": 8.8, "height": 0.3, "fill_color": "29BA74", "corner_radius": 8000},

  {"op": "add_text", "slide_index": 5, "text": "Change Mgmt", "left": 0.5, "top": 3.5, "width": 2.8, "height": 0.4, "font_size": 12, "font_color": "575757"},
  {"op": "add_rounded_rectangle", "slide_index": 5, "left": 5.7, "top": 3.55, "width": 4.4, "height": 0.3, "fill_color": "3EAD92", "corner_radius": 8000},

  {"op": "add_text", "slide_index": 5, "text": "Pilot Launch", "left": 0.5, "top": 4.0, "width": 2.8, "height": 0.4, "font_size": 12, "font_color": "575757"},
  {"op": "add_rounded_rectangle", "slide_index": 5, "left": 7.9, "top": 4.05, "width": 2.2, "height": 0.3, "fill_color": "295E7E", "corner_radius": 8000}
]
```

For milestones, add small diamond-shaped indicators using `add_oval` (small circle) or `add_text` with "◆" at the milestone x-position.

---

## Multi-Track Workstream Overview

For 4-5 parallel workstreams shown as columns, each with numbered badges and detail cards.

**Education:** Use when workstreams run concurrently (not sequentially). Equal-width columns imply equal priority. If some workstreams are more critical, make them wider. The connecting line at the bottom shows they converge to a common outcome.

```json
[
  {"op": "add_oval", "slide_index": 6, "left": 1.3, "top": 1.6, "width": 0.5, "height": 0.5, "fill_color": "03522D"},
  {"op": "add_text", "slide_index": 6, "text": "1", "left": 1.3, "top": 1.6, "width": 0.5, "height": 0.5, "font_size": 16, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_rectangle", "slide_index": 6, "left": 0.5, "top": 2.25, "width": 2.3, "height": 0.35, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 6, "text": "Data Platform", "left": 0.65, "top": 2.25, "width": 2.0, "height": 0.35, "font_size": 12, "bold": true, "font_color": "FFFFFF"},
  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 0.5, "top": 2.7, "width": 2.3, "height": 3.3, "fill_color": "F2F2F2", "corner_radius": 5000},
  {"op": "add_text", "slide_index": 6, "text": "Unified data lake\nReal-time ingestion\nAPI gateway\nData governance", "left": 0.65, "top": 2.85, "width": 2.0, "height": 3.0, "font_size": 11, "font_color": "575757"}
]
```

Repeat for each workstream at `left: 3.0`, `left: 5.5`, `left: 8.0`, `left: 10.5` (5 columns, width 2.3" each). Add a connecting line at y=6.2 with dots under each column.
