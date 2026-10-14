# Chart.js Reference

Integration patterns for Chart.js in slide presentations. Read this file when generating slides that contain `### chart` blocks in content.md.

## CDN (add in `<head>`)

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
```

Only include this when at least one slide has a `### chart` block.

## Container CSS

```css
/* === CHART CONTAINERS === */
.chart-card {
    background: var(--chart-card-bg, rgba(255,255,255,0.05));
    border: 1px solid var(--chart-card-border, rgba(255,255,255,0.1));
    border-radius: clamp(6px, 1vw, 12px);
    padding: clamp(12px, 2vw, 24px);
}
.chart-card h3 {
    font-family: var(--font-display);
    font-size: clamp(11px, 1.2vw, 15px);
    color: var(--accent, var(--text-secondary));
    margin-bottom: clamp(4px, 1vh, 12px);
}
.chart-container {
    position: relative;
    width: 100%;
    height: clamp(140px, 28vh, 260px);
}

/* Single chart slide: bigger container */
.chart-container--full {
    height: clamp(180px, 40vh, 360px);
}

/* Side-by-side charts */
.chart-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: clamp(12px, 2vw, 24px);
    width: 100%;
    max-width: 960px;
}
@media (max-width: 600px) {
    .chart-row { grid-template-columns: 1fr; }
}
```

## Parsing content.md `### chart` Blocks

Content.md chart blocks look like this:

```
### chart
type: bar
labels: Q1, Q2, Q3, Q4
Revenue ($M): 12, 18, 25, 31
Cost ($M): 8, 10, 12, 15
```

**Parsing rules:**
1. `type:` → Chart.js chart type (line, bar, doughnut, pie, radar, polarArea)
2. `labels:` → Array of strings for x-axis or segment labels
3. Every other line → A dataset. Name before `:` becomes the legend label, values after `:` are parsed as numbers
4. Number of values in each dataset MUST match number of labels

## Chart Type Templates

### Line Chart

```javascript
new Chart(document.getElementById('chartId'), {
    type: 'line',
    data: {
        labels: [/* from labels: */],
        datasets: [{
            label: 'Dataset Name',
            data: [/* values */],
            borderColor: 'var(--chart-1)',       // use theme color
            backgroundColor: 'var(--chart-1-bg)', // with alpha
            borderWidth: 2.5,
            fill: true,
            tension: 0.4,
            pointBackgroundColor: 'var(--chart-1)',
            pointRadius: 3,
            pointHoverRadius: 6
        }]
    },
    options: { /* see Common Options below */ }
});
```

### Bar Chart

```javascript
new Chart(document.getElementById('chartId'), {
    type: 'bar',
    data: {
        labels: [/* from labels: */],
        datasets: [{
            label: 'Dataset Name',
            data: [/* values */],
            backgroundColor: 'var(--chart-1)',  // solid or with alpha
            borderRadius: 4
        }]
    },
    options: { /* see Common Options below */ }
});
```

### Doughnut Chart

```javascript
new Chart(document.getElementById('chartId'), {
    type: 'doughnut',
    data: {
        labels: [/* from labels: */],
        datasets: [{
            data: [/* values — single dataset, one value per label */],
            backgroundColor: [/* --chart-1 through --chart-6 */],
            borderColor: 'var(--bg-primary)',  // match slide background
            borderWidth: 3
        }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
            legend: { position: 'right', labels: { /* theme font + color */ } }
        }
    }
});
```

### Pie Chart

Same as doughnut, but `type: 'pie'` and remove `cutout`.

### Radar Chart

```javascript
new Chart(document.getElementById('chartId'), {
    type: 'radar',
    data: {
        labels: [/* from labels: */],
        datasets: [{
            label: 'Dataset Name',
            data: [/* values */],
            borderColor: 'var(--chart-1)',
            backgroundColor: 'var(--chart-1-bg)',
            borderWidth: 1.5,
            pointBackgroundColor: 'var(--chart-1)',
            pointRadius: 3
        }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        scales: {
            r: {
                grid: { color: 'var(--chart-grid)' },
                angleLines: { color: 'var(--chart-grid)' },
                pointLabels: { color: 'var(--chart-text)', font: { family: 'var(--font-body)', size: 11 } },
                ticks: { display: false },
                suggestedMin: 0
            }
        }
    }
});
```

### Polar Area Chart

```javascript
new Chart(document.getElementById('chartId'), {
    type: 'polarArea',
    data: {
        labels: [/* from labels: */],
        datasets: [{
            data: [/* values */],
            backgroundColor: [/* --chart-1-bg through --chart-6-bg */],
            borderColor: 'var(--chart-grid)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        scales: { r: { grid: { color: 'var(--chart-grid)' }, ticks: { display: false } } },
        plugins: {
            legend: { position: 'right', labels: { /* theme font + color */ } }
        }
    }
});
```

## Common Options (Cartesian Charts: line, bar)

```javascript
options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true, // false if single dataset
            labels: {
                color: 'var(--chart-text)',
                font: { family: 'var(--font-body)', size: 11 },
                usePointStyle: true,
                pointStyleWidth: 8,
                padding: 16
            }
        }
    },
    scales: {
        x: {
            grid: { color: 'var(--chart-grid)' },
            ticks: { color: 'var(--chart-text)', font: { family: 'var(--font-body)', size: 11 } }
        },
        y: {
            grid: { color: 'var(--chart-grid)' },
            ticks: { color: 'var(--chart-text)', font: { family: 'var(--font-body)', size: 11 } }
        }
    }
}
```

## Theme Adaptation Rules

**IMPORTANT:** CSS variables (`var()`) don't work inside `<script>`. You must resolve theme colors as literal values when generating Chart.js config.

Use the chart color variables from STYLE_PRESETS.md for each theme. When generating:

1. Look up the chosen theme's `--chart-colors` palette
2. Assign colors to datasets in order: first dataset gets color 1, second gets color 2, etc.
3. For `fill` backgrounds, add alpha: use `rgba()` with `0.1` opacity for line fills, `0.7` for bar charts
4. Grid lines: dark themes → `rgba(255,255,255,0.05)`, light themes → `rgba(0,0,0,0.06)`
5. Text (ticks, labels): dark themes → `rgba(255,255,255,0.4)`, light themes → `rgba(0,0,0,0.45)`
6. Font family: use the theme's body font (resolved as string, e.g., `'Space Grotesk'`)
7. Doughnut/pie border color: match the slide background color to create clean gaps

## Slide Layout Rules

| Scenario | Layout |
|----------|--------|
| 1 chart only | `.chart-container--full`, centered below heading |
| 2 charts | `.chart-row` with two `.chart-card` children |
| Chart + text/bullets | Two-column: text left, chart right (or vice versa) |

**Viewport constraint:** Chart containers must never exceed `50vh` height. Use the CSS classes above which enforce `clamp()` limits.

**Animation:** Charts animate natively on render. Wrap the chart container in `.reveal` so it fades in when the slide becomes visible. No extra animation needed.
