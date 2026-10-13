# Chart Verification Workflow

## Trigger

After Step 7 assembly, when the deck contains data visualizations (charts built with CSS component classes).

## Why Verify?

HTML/CSS charts use numeric data geometry and CSS classes, so visual proportions are controlled IF the markup is correct. However, LLMs still introduce:
- Wrong widths/heights (e.g., a bar exceeds its container or contradicts its label)
- Mismatched axis labels vs data
- Incorrect data-to-visual mappings (wrong values assigned to bars/segments)
- Unit errors (e.g., percentages displayed as decimals)
- Missing data points or categories

---

## Process

### Step 1: Identify Charts

Search `content.html` for chart CSS class usage:
- `.bar-chart` -- vertical bar charts
- `.vbar-chart` -- vertical bar chart variant
- `.h-bar-chart` -- horizontal bar charts
- `.pie-chart` / `.donut-chart` -- pie and donut charts
- `.line-chart` -- line charts (using positioned dots/segments)
- `.stacked-bar` -- stacked bar charts
- `.chart-container` -- generic chart wrapper

Build a list of chart slides:
```
Slide 5: bar chart (.bar-chart) -- "Revenue by Quarter"
Slide 8: pie chart (.pie-chart) -- "Market Share"
Slide 12: horizontal bar chart (.h-bar-chart) -- "Growth Trend"
```

If no chart CSS classes are found, output `verify-charts: no data-driven charts detected, nothing to verify` and stop.

### Step 2: Extract Data

For each chart, identify:
- Source data (from `content_design_spec.md` section VI or inline in `content.html`)
- Expected visual output (values, labels, proportions)
- Data format (raw numbers, percentages, currency)

### Step 3: Verify Markup Logic

For each chart, check:
- [ ] All data points present (count of bars/slices/points matches source)
- [ ] Pixel dimensions accommodate all data (no overflow or clipping)
- [ ] Labels match data headers
- [ ] Units are consistent (%, raw numbers, currency)
- [ ] Scale is appropriate (bar heights proportional to values, readable)
- [ ] Colors match theme palette (reference `template.css` CSS custom property definitions)
- [ ] CSS classes are used correctly (correct class names from `components.md`)
- [ ] Chart containers have stable dimensions and charts finish rendering before export

### Step 4: Visual Verification

After a full `html_compiler.py <project_path> --all` build, inspect the chart in `output/browser_pngs/` first. The settled browser layout and `dom-audit.json` are the visual truth. Inspect matching SVG-route PNGs and `render-fidelity.json` only when diagnosing conversion differences:
- [ ] All bars/lines/slices visible
- [ ] Legend matches actual data series
- [ ] No overlapping labels
- [ ] Proportions look reasonable (e.g., 50% value takes ~half the chart area)
- [ ] Text is legible at presentation scale

### Step 5: Fix Protocol

If issues found:
1. Fix the data/markup in `content.html`
2. Run `python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --source-only --profile standard-project`
3. Re-render with `python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all`
4. Re-verify the specific chart in the browser PNG baseline
5. Repeat until all checks pass

---

## Chart Type Checklist

### Bar Charts (.bar-chart, .vbar-chart)
- Container height >= tallest bar + label headroom
- Bar labels readable (not overlapping)
- Correct number of bars = number of categories
- Each bar has explicit `height` in pixels proportional to its value
- Horizontal vs vertical matches the data semantics

### Pie/Donut Charts (.pie-chart, .donut-chart)
- All slices sum to 100% (or total stated value)
- Largest slice matches largest value
- Legend has all categories
- Slice order is consistent (typically descending by value)
- CSS `conic-gradient` or equivalent percentages are accurate

### Horizontal Bar Charts (.h-bar-chart)
- All data points plotted (count bars)
- Bar widths proportional to values
- Labels aligned and readable
- Container width accommodates longest bar + label

### Line Charts (.line-chart)
- All data points plotted (count positioned elements)
- Points don't extend beyond chart container
- Trend direction matches data
- Multiple series are distinguishable (color/style)

### Flowcharts / Diagrams (flexbox layouts)
- All nodes present from the spec
- Connections match the described relationships (using borders/lines)
- Arrow directions are correct (CSS triangles or SVG arrows)
- Labels are readable and correctly placed

---

## Inputs
- `content.html` chart markup sections
- `content_design_spec.md` section VI source data
- Current build artifacts, especially browser PNGs and DOM audit; SVG-route artifacts only for conversion diagnosis

## Outputs
- Verified/fixed chart markup in `content.html`
- Re-assembled and re-rendered output if fixes applied
- Brief verification receipt:

```
verify-charts: slide 5 bar chart | data=correct | scale=correct | labels=fixed (typo)
verify-charts: slide 8 pie chart | data=correct | proportions=correct | no issues
verify-charts: slide 12 h-bar chart | data=fixed (missing Q4 bar) | re-assembled
```
