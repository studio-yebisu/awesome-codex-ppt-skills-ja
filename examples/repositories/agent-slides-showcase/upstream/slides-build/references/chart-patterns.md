# Chart Patterns (slides ops)

Concrete patterns for building data visualization slides. Start from the argument, not the data shape — choose the chart where the visual proves the specific claim.

---

## Chart Color Strategy: Gray-First, Highlight-Green

**Default approach for all charts:** Start in gray monochrome, then highlight only the key data point in green. This focuses attention on the argument.

| Purpose | Color approach |
|---------|---------------|
| Default | All bars/slices in gray (`6E6F73`, `B0B0B0`) |
| Highlight | Key data point in `29BA74`; keep others gray |
| Multiple series | Brand palette in order: `03522D`, `197A56`, `29BA74`, `3EAD92`, `D4DF33`, `295E7E` |

**Rules:**
1. Use full palette only when ALL series are equally important
2. For "our company vs. peers" — our bar in green, peers in gray
3. For "before vs. after" — after in green, before in gray
4. For pie/doughnut — highlight the key segment in green, others in gray shades

---

## Chart Type Selection Guide

| If your argument is... | Chart type | Key element |
|---|---|---|
| "X is growing fast" | `add_line_chart` | Annotate the inflection point |
| "We're bigger than competitors" | `add_bar_chart` orientation=`"bar"` | Highlight our bar in green |
| "Three segments make up 80%" | `add_doughnut_chart` | Group rest into "Other" |
| "Volume up but rate declining" | `add_combo_chart_overlay` | Bars for volume, line for rate |
| "Category X outperforms" | `add_bar_chart` | Sort by value, highlight winner |
| "Investment vs. returns over time" | `add_bar_chart` (grouped) | Two series, gray vs. green |
| "Composition shifts over time" | `add_bar_chart` (stacked, via series) | Stack segments by color |

---

## Chart Formatting Rules

1. Action title states what the data **proves**, not what it shows
2. Start gray, highlight green — only full palette for multiple series
3. Remove chart junk: hide gridlines, minimize axis lines
4. Label directly on bars/lines (`set_chart_data_labels`) rather than requiring legend lookup
5. One chart per slide (unless comparing two closely related views)
6. Include callout box annotating the key insight
7. Round numbers: `~$2.5B` not `$2,487,392,104`
8. Sort bars by value (largest to smallest) unless chronological
9. **ALWAYS set explicit axis font sizes** — PowerPoint defaults are too large for most layouts. After every chart, add:
   ```json
   {"op": "set_chart_axis_options", "slide_index": N, "chart_index": 0, "axis": "category", "font_size": 9}
   {"op": "set_chart_axis_options", "slide_index": N, "chart_index": 0, "axis": "value", "font_size": 9}
   ```
   Use `font_size: 9` for standard charts; `font_size: 8` when the chart shares the slide with a callout or table.
10. **ALWAYS set legend font size and position** — legend must not overlap the chart. First shrink the plot area to make room, then set legend with `include_in_layout: true`:
    ```json
    {"op": "set_chart_plot_style", "slide_index": N, "chart_index": 0, "plot_area_h": 0.78}
    {"op": "set_chart_legend", "slide_index": N, "chart_index": 0, "position": "bottom", "font_size": 9, "include_in_layout": true}
    ```
    `plot_area_h: 0.78` reserves ~22% of chart height for the bottom legend. Adjust lower (e.g., `0.72`) for 3+ series legends.
11. **ALWAYS set explicit table font sizes** — PowerPoint defaults are too large for data tables. Use `font_size` on `add_table`:
    ```json
    {"op": "add_table", "slide_index": N, "rows": [...], "left": 0.7, "top": 2.0, "width": 11.9, "height": 3.0, "font_size": 11}
    ```
    Use `font_size: 11` for standard tables; `font_size: 10` for dense tables (>5 rows). For per-cell overrides, use `update_table_cell` with `font_size`.

---

## Combined Chart + KPI + Callout Slide

The highest-impact data slide pattern. Chart in top half, KPI tiles below, callout at bottom.

**Education:** Use when a single chart needs both summary metrics and a narrative takeaway. The KPIs anchor the headline numbers; the callout states the "so what" for executives who won't study the chart.

```json
[
  {"op": "add_slide", "layout_name": "Title and Text"},
  {"op": "set_semantic_text", "slide_index": 5, "role": "title", "text": "Digital revenue outpaced traditional by 3x, exceeding all targets"},
  {"op": "set_semantic_text", "slide_index": 5, "role": "body", "text": " "},
  {"op": "add_bar_chart", "slide_index": 5, "categories": ["Q1", "Q2", "Q3", "Q4"],
    "series": [["Digital ($M)", [120, 145, 168, 195]], ["Traditional ($M)", [280, 275, 260, 250]]],
    "left": 0.7, "top": 1.5, "width": 11.9, "height": 2.8},
  {"op": "set_chart_series_style", "slide_index": 5, "chart_index": 0, "series_index": 0, "fill_color_hex": "29BA74"},
  {"op": "set_chart_series_style", "slide_index": 5, "chart_index": 0, "series_index": 1, "fill_color_hex": "B0B0B0"},
  {"op": "set_chart_data_labels", "slide_index": 5, "chart_index": 0, "enabled": true, "show_value": true},
  {"op": "set_chart_legend", "slide_index": 5, "chart_index": 0, "visible": true, "position": "bottom"},

  {"op": "add_text", "slide_index": 5, "text": "$195M", "left": 0.7, "top": 4.6, "width": 3.5, "height": 0.5, "font_size": 28, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 5, "text": "Q4 Digital Revenue", "left": 0.7, "top": 5.1, "width": 3.5, "height": 0.3, "font_size": 12, "font_color": "575757"},
  {"op": "add_line_shape", "slide_index": 5, "x1": 4.4, "y1": 4.7, "x2": 4.4, "y2": 5.3, "color": "CCCCCC", "line_width": 0.5},
  {"op": "add_text", "slide_index": 5, "text": "+62%", "left": 4.7, "top": 4.6, "width": 3.5, "height": 0.5, "font_size": 28, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 5, "text": "YoY Growth", "left": 4.7, "top": 5.1, "width": 3.5, "height": 0.3, "font_size": 12, "font_color": "575757"},
  {"op": "add_line_shape", "slide_index": 5, "x1": 8.4, "y1": 4.7, "x2": 8.4, "y2": 5.3, "color": "CCCCCC", "line_width": 0.5},
  {"op": "add_text", "slide_index": 5, "text": "3.1x", "left": 8.7, "top": 4.6, "width": 3.5, "height": 0.5, "font_size": 28, "bold": true, "font_color": "29BA74"},
  {"op": "add_text", "slide_index": 5, "text": "vs Target", "left": 8.7, "top": 5.1, "width": 3.5, "height": 0.3, "font_size": 12, "font_color": "575757"},

  {"op": "add_rounded_rectangle", "slide_index": 5, "left": 0.7, "top": 5.7, "width": 11.9, "height": 0.7, "fill_color": "F0FAF5", "corner_radius": 5000, "border_color": "29BA74", "border_width": 1.5},
  {"op": "add_text", "slide_index": 5, "text": "Key insight: Digital revenue will surpass traditional by Q2 2027 at current trajectory", "left": 0.9, "top": 5.8, "width": 11.5, "height": 0.5, "font_size": 14, "bold": true, "font_color": "03522D"},
  {"op": "add_text", "slide_index": 5, "text": "Source: Company financials, Q4 2026", "left": 0.7, "top": 6.6, "width": 10.0, "height": 0.3, "font_size": 9, "font_color": "999999"}
]
```

---

## Simulated Horizontal Bar Chart (Shape-Based)

Use when a native chart is overkill — e.g., simple ranked comparisons. Shape bars give full visual control.

**Education:** Shape-based bars let you highlight specific bars, add inline labels, and control rounding. Use when the argument is about ranking, not precise values.

```json
[
  {"op": "add_text", "slide_index": 6, "text": "Enterprise", "left": 0.7, "top": 2.1, "width": 2.2, "height": 0.45, "font_size": 13, "font_color": "575757"},
  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 3.0, "top": 2.15, "width": 9.5, "height": 0.35, "fill_color": "E0E0E0", "corner_radius": 8000},
  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 3.0, "top": 2.15, "width": 4.3, "height": 0.35, "fill_color": "29BA74", "corner_radius": 8000},
  {"op": "add_text", "slide_index": 6, "text": "45%", "left": 7.4, "top": 2.1, "width": 0.8, "height": 0.45, "font_size": 13, "bold": true, "font_color": "29BA74"},

  {"op": "add_text", "slide_index": 6, "text": "Mid-Market", "left": 0.7, "top": 2.65, "width": 2.2, "height": 0.45, "font_size": 13, "font_color": "575757"},
  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 3.0, "top": 2.7, "width": 9.5, "height": 0.35, "fill_color": "E0E0E0", "corner_radius": 8000},
  {"op": "add_rounded_rectangle", "slide_index": 6, "left": 3.0, "top": 2.7, "width": 3.6, "height": 0.35, "fill_color": "6E6F73", "corner_radius": 8000},
  {"op": "add_text", "slide_index": 6, "text": "38%", "left": 6.7, "top": 2.65, "width": 0.8, "height": 0.45, "font_size": 13, "bold": true, "font_color": "6E6F73"}
]
```

Repeat for each bar. Use `29BA74` for the highlighted bar, `6E6F73` for others.

---

## Waterfall Bridge (Shape-Based)

Use for showing how a starting value changes through increments/decrements to reach an end value.

**Education:** Use when the argument is about what drove the change between two states. Positive deltas in green, negative in gray/red-toned. The connecting line shows the running total.

```json
[
  {"op": "add_rectangle", "slide_index": 7, "left": 0.7, "top": 2.5, "width": 1.5, "height": 2.5, "fill_color": "6E6F73"},
  {"op": "add_text", "slide_index": 7, "text": "$100M\nStart", "left": 0.7, "top": 2.0, "width": 1.5, "height": 0.45, "font_size": 12, "bold": true, "font_color": "575757"},

  {"op": "add_rectangle", "slide_index": 7, "left": 2.5, "top": 2.0, "width": 1.5, "height": 0.5, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 7, "text": "+$20M\nDigital", "left": 2.5, "top": 1.5, "width": 1.5, "height": 0.45, "font_size": 12, "bold": true, "font_color": "29BA74"},

  {"op": "add_rectangle", "slide_index": 7, "left": 4.3, "top": 2.0, "width": 1.5, "height": 0.3, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 7, "text": "+$15M\nPricing", "left": 4.3, "top": 1.5, "width": 1.5, "height": 0.45, "font_size": 12, "bold": true, "font_color": "29BA74"},

  {"op": "add_rectangle", "slide_index": 7, "left": 6.1, "top": 1.7, "width": 1.5, "height": 0.3, "fill_color": "B0B0B0"},
  {"op": "add_text", "slide_index": 7, "text": "-$10M\nFX", "left": 6.1, "top": 2.05, "width": 1.5, "height": 0.45, "font_size": 12, "bold": true, "font_color": "B0B0B0"},

  {"op": "add_rectangle", "slide_index": 7, "left": 7.9, "top": 2.0, "width": 1.5, "height": 3.0, "fill_color": "03522D"},
  {"op": "add_text", "slide_index": 7, "text": "$125M\nEnd", "left": 7.9, "top": 1.5, "width": 1.5, "height": 0.45, "font_size": 12, "bold": true, "font_color": "03522D"}
]
```

Adjust `top` and `height` of each delta bar so the top aligns with the running total line.

---

## KPI Tile Row (Cards with Accent Bar)

More structured than the basic KPI Row. Each metric gets a card with green left accent and change indicator.

**Education:** Use for executive summary slides or as a header row above detailed content. Each card answers one question: "What is the headline number, and is it good or bad?"

```json
[
  {"op": "add_rounded_rectangle", "slide_index": 8, "left": 0.5, "top": 2.1, "width": 3.0, "height": 1.2, "fill_color": "FFFFFF", "corner_radius": 5000, "border_color": "E0E0E0", "border_width": 0.5},
  {"op": "add_rectangle", "slide_index": 8, "left": 0.5, "top": 2.1, "width": 0.06, "height": 1.2, "fill_color": "29BA74"},
  {"op": "add_text", "slide_index": 8, "text": "Revenue", "left": 0.7, "top": 2.18, "width": 2.6, "height": 0.25, "font_size": 11, "bold": true, "font_color": "575757"},
  {"op": "add_text", "slide_index": 8, "text": "$2.4B", "left": 0.7, "top": 2.45, "width": 2.6, "height": 0.45, "font_size": 28, "bold": true, "font_color": "575757"},
  {"op": "add_text", "slide_index": 8, "text": "+12% YoY", "left": 0.7, "top": 2.95, "width": 2.6, "height": 0.25, "font_size": 11, "bold": true, "font_color": "29BA74"}
]
```

Repeat at `left: 3.7`, `left: 6.9`, `left: 10.1` for 4-across layout.
