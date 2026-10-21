/**
 * chart_renderer.mjs - D3-based chart rendering for presentation slides.
 *
 * Generates clean, professional SVG charts suitable for embedding in slides.
 * Uses D3.js with jsdom to produce SVG output in Node.js (no browser needed).
 *
 * Supported chart types:
 *   - Bar chart (vertical)
 *   - Line chart
 *   - Pie / Donut chart
 *   - Area chart
 *
 * Usage:
 *   import { renderChart } from './chart_renderer.mjs';
 *   const svgString = renderChart({ type: 'bar', labels: [...], values: [...], ... });
 */

import * as d3 from 'd3';
import { JSDOM } from 'jsdom';

// ============================================================
// Default Color Palettes (professional, presentation-ready)
// ============================================================

const PALETTES = {
  blue: ['#1565C0', '#1E88E5', '#42A5F5', '#90CAF9', '#BBDEFB', '#0D47A1'],
  corporate: ['#1565C0', '#2E7D32', '#F57C00', '#7B1FA2', '#C62828', '#00838F'],
  cool: ['#0D47A1', '#1565C0', '#0097A7', '#00838F', '#2E7D32', '#558B2F'],
  warm: ['#E65100', '#F57C00', '#FFA726', '#FFB74D', '#FFCC02', '#FF7043'],
  modern: ['#3F51B5', '#009688', '#FF5722', '#795548', '#607D8B', '#4CAF50'],
};

const DEFAULT_PALETTE = PALETTES.blue;

// ============================================================
// Utility Functions
// ============================================================

/**
 * Create a JSDOM document for D3 to render into.
 */
function createDocument() {
  const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
  return dom.window.document;
}

/**
 * Get colors from options, falling back to default palette.
 */
function getColors(options, count) {
  if (options.colors && options.colors.length >= count) {
    return options.colors;
  }
  const palette = options.palette ? (PALETTES[options.palette] || DEFAULT_PALETTE) : DEFAULT_PALETTE;
  // Cycle through palette if not enough colors
  const colors = [];
  for (let i = 0; i < count; i++) {
    colors.push(palette[i % palette.length]);
  }
  return colors;
}

// ============================================================
// Bar Chart
// ============================================================

/**
 * Render a vertical bar chart.
 *
 * @param {Object} options
 * @param {string[]} options.labels - Category labels
 * @param {number[]} options.values - Data values
 * @param {string[]} [options.colors] - Bar colors
 * @param {string} [options.title] - Chart title
 * @param {number} [options.width=800] - Chart width
 * @param {number} [options.height=450] - Chart height
 * @param {string} [options.yLabel] - Y-axis label
 * @param {string} [options.valueFormat] - Format string for values (e.g., '.0f', '.1%')
 * @returns {string} SVG markup
 */
export function renderBarChart(options) {
  const {
    labels = [],
    values = [],
    title = '',
    width = 800,
    height = 450,
    yLabel = '',
    valueFormat = '',
    showValues = true,
    borderRadius = 4,
  } = options;

  const colors = getColors(options, labels.length);
  const document = createDocument();

  const margin = { top: title ? 50 : 20, right: 30, bottom: 60, left: 60 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const body = d3.select(document.body);
  const svg = body.append('svg')
    .attr('xmlns', 'http://www.w3.org/2000/svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`);

  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  // Scales
  const x = d3.scaleBand()
    .domain(labels)
    .range([0, innerWidth])
    .padding(0.35);

  const y = d3.scaleLinear()
    .domain([0, d3.max(values) * 1.15])
    .nice()
    .range([innerHeight, 0]);

  // Grid lines (subtle)
  const yTicks = y.ticks(5);
  g.selectAll('.grid-line')
    .data(yTicks)
    .enter()
    .append('line')
    .attr('x1', 0)
    .attr('x2', innerWidth)
    .attr('y1', d => y(d))
    .attr('y2', d => y(d))
    .attr('stroke', '#E0E4E8')
    .attr('stroke-width', 1)
    .attr('stroke-dasharray', '4,4');

  // Bars
  g.selectAll('.bar')
    .data(values)
    .enter()
    .append('rect')
    .attr('x', (_, i) => x(labels[i]))
    .attr('y', d => y(d))
    .attr('width', x.bandwidth())
    .attr('height', d => innerHeight - y(d))
    .attr('fill', (_, i) => colors[i % colors.length])
    .attr('rx', borderRadius)
    .attr('ry', borderRadius);

  // Value labels on top of bars
  if (showValues) {
    const formatter = valueFormat ? d3.format(valueFormat) : d => d;
    g.selectAll('.value-label')
      .data(values)
      .enter()
      .append('text')
      .attr('x', (_, i) => x(labels[i]) + x.bandwidth() / 2)
      .attr('y', d => y(d) - 8)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '13px')
      .attr('font-weight', '600')
      .attr('fill', '#333')
      .text(d => formatter(d));
  }

  // X Axis
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x).tickSize(0))
    .call(g => g.select('.domain').remove())
    .selectAll('text')
    .attr('font-family', 'Lato, Inter, sans-serif')
    .attr('font-size', '12px')
    .attr('fill', '#5A6270')
    .attr('dy', '1em');

  // Y Axis
  g.append('g')
    .call(d3.axisLeft(y).ticks(5).tickSize(0))
    .call(g => g.select('.domain').remove())
    .selectAll('text')
    .attr('font-family', 'Lato, Inter, sans-serif')
    .attr('font-size', '11px')
    .attr('fill', '#5A6270');

  // Y-axis label
  if (yLabel) {
    g.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -45)
      .attr('x', -innerHeight / 2)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '12px')
      .attr('fill', '#5A6270')
      .text(yLabel);
  }

  // Title
  if (title) {
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', 28)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '16px')
      .attr('font-weight', '600')
      .attr('fill', '#1A1A2E')
      .text(title);
  }

  return body.html();
}

// ============================================================
// Line Chart
// ============================================================

/**
 * Render a line chart.
 *
 * @param {Object} options
 * @param {string[]} options.labels - X-axis labels
 * @param {number[]} options.values - Data values (single series)
 * @param {number[][]} [options.series] - Multiple series: [[v1, v2,...], [v1, v2,...]]
 * @param {string[]} [options.seriesNames] - Names for each series
 * @param {string[]} [options.colors] - Line colors
 * @param {string} [options.title] - Chart title
 * @param {number} [options.width=800] - Chart width
 * @param {number} [options.height=450] - Chart height
 * @param {boolean} [options.showDots=true] - Show data point dots
 * @param {boolean} [options.smooth=true] - Use curved lines
 * @returns {string} SVG markup
 */
export function renderLineChart(options) {
  const {
    labels = [],
    values = [],
    series = null,
    seriesNames = [],
    title = '',
    width = 800,
    height = 450,
    yLabel = '',
    showDots = true,
    smooth = true,
    showArea = false,
  } = options;

  // Normalize to multi-series format
  const allSeries = series || [values];
  const colors = getColors(options, allSeries.length);
  const document = createDocument();

  const margin = { top: title ? 50 : 20, right: 30, bottom: 60, left: 60 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const body = d3.select(document.body);
  const svg = body.append('svg')
    .attr('xmlns', 'http://www.w3.org/2000/svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`);

  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  // Scales
  const x = d3.scalePoint()
    .domain(labels)
    .range([0, innerWidth])
    .padding(0.1);

  const allValues = allSeries.flat();
  const yMax = d3.max(allValues) * 1.15;
  const y = d3.scaleLinear()
    .domain([0, yMax])
    .nice()
    .range([innerHeight, 0]);

  // Grid lines
  const yTicks = y.ticks(5);
  g.selectAll('.grid-line')
    .data(yTicks)
    .enter()
    .append('line')
    .attr('x1', 0)
    .attr('x2', innerWidth)
    .attr('y1', d => y(d))
    .attr('y2', d => y(d))
    .attr('stroke', '#E0E4E8')
    .attr('stroke-width', 1)
    .attr('stroke-dasharray', '4,4');

  // Line generator
  const lineGen = d3.line()
    .x((_, i) => x(labels[i]))
    .y(d => y(d));

  if (smooth) {
    lineGen.curve(d3.curveMonotoneX);
  }

  // Area generator (for filled area under curve)
  const areaGen = d3.area()
    .x((_, i) => x(labels[i]))
    .y0(innerHeight)
    .y1(d => y(d));

  if (smooth) {
    areaGen.curve(d3.curveMonotoneX);
  }

  // Draw each series
  for (let s = 0; s < allSeries.length; s++) {
    const seriesData = allSeries[s];
    const color = colors[s];

    // Area fill (subtle gradient effect)
    if (showArea) {
      g.append('path')
        .datum(seriesData)
        .attr('d', areaGen)
        .attr('fill', color)
        .attr('fill-opacity', 0.12);
    }

    // Line
    g.append('path')
      .datum(seriesData)
      .attr('d', lineGen)
      .attr('fill', 'none')
      .attr('stroke', color)
      .attr('stroke-width', 2.5)
      .attr('stroke-linecap', 'round')
      .attr('stroke-linejoin', 'round');

    // Dots
    if (showDots) {
      g.selectAll(`.dot-${s}`)
        .data(seriesData)
        .enter()
        .append('circle')
        .attr('cx', (_, i) => x(labels[i]))
        .attr('cy', d => y(d))
        .attr('r', 4)
        .attr('fill', '#fff')
        .attr('stroke', color)
        .attr('stroke-width', 2.5);
    }
  }

  // X Axis
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x).tickSize(0))
    .call(g => g.select('.domain').remove())
    .selectAll('text')
    .attr('font-family', 'Lato, Inter, sans-serif')
    .attr('font-size', '12px')
    .attr('fill', '#5A6270')
    .attr('dy', '1em');

  // Y Axis
  g.append('g')
    .call(d3.axisLeft(y).ticks(5).tickSize(0))
    .call(g => g.select('.domain').remove())
    .selectAll('text')
    .attr('font-family', 'Lato, Inter, sans-serif')
    .attr('font-size', '11px')
    .attr('fill', '#5A6270');

  // Y-axis label
  if (yLabel) {
    g.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -45)
      .attr('x', -innerHeight / 2)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '12px')
      .attr('fill', '#5A6270')
      .text(yLabel);
  }

  // Title
  if (title) {
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', 28)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '16px')
      .attr('font-weight', '600')
      .attr('fill', '#1A1A2E')
      .text(title);
  }

  // Legend (if multiple series)
  if (allSeries.length > 1 && seriesNames.length > 0) {
    const legendG = svg.append('g')
      .attr('transform', `translate(${margin.left}, ${height - 20})`);

    let legendX = 0;
    for (let s = 0; s < seriesNames.length; s++) {
      const itemG = legendG.append('g')
        .attr('transform', `translate(${legendX}, 0)`);

      itemG.append('line')
        .attr('x1', 0).attr('y1', 0)
        .attr('x2', 20).attr('y2', 0)
        .attr('stroke', colors[s])
        .attr('stroke-width', 2.5);

      itemG.append('text')
        .attr('x', 26)
        .attr('y', 4)
        .attr('font-family', 'Lato, Inter, sans-serif')
        .attr('font-size', '11px')
        .attr('fill', '#5A6270')
        .text(seriesNames[s]);

      legendX += 26 + seriesNames[s].length * 7 + 20;
    }
  }

  return body.html();
}

// ============================================================
// Pie / Donut Chart
// ============================================================

/**
 * Render a pie or donut chart.
 *
 * @param {Object} options
 * @param {string[]} options.labels - Slice labels
 * @param {number[]} options.values - Slice values
 * @param {string[]} [options.colors] - Slice colors
 * @param {string} [options.title] - Chart title
 * @param {number} [options.width=500] - Chart width
 * @param {number} [options.height=450] - Chart height
 * @param {boolean} [options.donut=false] - Render as donut chart
 * @param {boolean} [options.showLegend=true] - Show legend
 * @param {boolean} [options.showPercentages=true] - Show percentage labels
 * @returns {string} SVG markup
 */
export function renderPieChart(options) {
  const {
    labels = [],
    values = [],
    title = '',
    width = 500,
    height = 450,
    donut = true,
    showLegend = true,
    showPercentages = true,
  } = options;

  const colors = getColors(options, labels.length);
  const document = createDocument();

  const body = d3.select(document.body);
  const svg = body.append('svg')
    .attr('xmlns', 'http://www.w3.org/2000/svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`);

  const titleOffset = title ? 40 : 0;
  const legendHeight = showLegend ? 60 : 0;
  const availableHeight = height - titleOffset - legendHeight;
  const radius = Math.min(width, availableHeight) / 2 - 20;
  const innerRadius = donut ? radius * 0.55 : 0;

  const centerX = width / 2;
  const centerY = titleOffset + availableHeight / 2;

  const g = svg.append('g')
    .attr('transform', `translate(${centerX},${centerY})`);

  // Pie layout
  const pie = d3.pie()
    .value(d => d)
    .sort(null)
    .padAngle(0.02);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(radius)
    .cornerRadius(3);

  const labelArc = d3.arc()
    .innerRadius(radius * 0.72)
    .outerRadius(radius * 0.72);

  const arcs = pie(values);
  const total = d3.sum(values);

  // Draw slices
  g.selectAll('.slice')
    .data(arcs)
    .enter()
    .append('path')
    .attr('d', arc)
    .attr('fill', (_, i) => colors[i])
    .attr('stroke', '#fff')
    .attr('stroke-width', 2);

  // Percentage labels on slices
  if (showPercentages) {
    g.selectAll('.slice-label')
      .data(arcs)
      .enter()
      .append('text')
      .attr('transform', d => `translate(${labelArc.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'central')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '13px')
      .attr('font-weight', '600')
      .attr('fill', '#fff')
      .text(d => {
        const pct = (d.data / total * 100);
        return pct >= 5 ? `${pct.toFixed(0)}%` : '';
      });
  }

  // Center label for donut
  if (donut) {
    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'central')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '24px')
      .attr('font-weight', '700')
      .attr('fill', '#1A1A2E')
      .text(total.toLocaleString());

    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('y', 22)
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '11px')
      .attr('fill', '#5A6270')
      .text('Total');
  }

  // Title
  if (title) {
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', 28)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'Lato, Inter, sans-serif')
      .attr('font-size', '16px')
      .attr('font-weight', '600')
      .attr('fill', '#1A1A2E')
      .text(title);
  }

  // Legend
  if (showLegend) {
    const legendY = height - legendHeight + 10;
    const legendG = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${legendY})`);

    // Calculate total legend width for centering
    const itemWidths = labels.map(l => 18 + l.length * 7 + 16);
    const totalLegendWidth = itemWidths.reduce((a, b) => a + b, 0);
    let legendX = -totalLegendWidth / 2;

    for (let i = 0; i < labels.length; i++) {
      const itemG = legendG.append('g')
        .attr('transform', `translate(${legendX}, 0)`);

      itemG.append('rect')
        .attr('width', 12)
        .attr('height', 12)
        .attr('rx', 2)
        .attr('fill', colors[i]);

      itemG.append('text')
        .attr('x', 18)
        .attr('y', 10)
        .attr('font-family', 'Lato, Inter, sans-serif')
        .attr('font-size', '11px')
        .attr('fill', '#5A6270')
        .text(labels[i]);

      legendX += itemWidths[i];
    }
  }

  return body.html();
}

// ============================================================
// Area Chart
// ============================================================

/**
 * Render an area chart (filled line chart).
 *
 * @param {Object} options - Same as renderLineChart but with filled area
 * @returns {string} SVG markup
 */
export function renderAreaChart(options) {
  return renderLineChart({ ...options, showArea: true, showDots: options.showDots !== undefined ? options.showDots : false });
}

// ============================================================
// Unified Rendering Entry Point
// ============================================================

/**
 * Render a chart of the specified type.
 *
 * @param {Object} options
 * @param {string} options.type - Chart type: 'bar', 'line', 'pie', 'area'
 * @param {string[]} options.labels - Data labels
 * @param {number[]} options.values - Data values
 * @param {Object} [options...] - Additional options specific to chart type
 * @returns {string} SVG string
 */
export function renderChart(options) {
  const { type } = options;

  switch (type) {
    case 'bar':
      return renderBarChart(options);
    case 'line':
      return renderLineChart(options);
    case 'pie':
    case 'donut':
      return renderPieChart({ ...options, donut: type === 'donut' });
    case 'area':
      return renderAreaChart(options);
    default:
      console.warn(`Unknown chart type: "${type}", falling back to bar chart`);
      return renderBarChart(options);
  }
}

/**
 * Render a chart and return it as a base64 data URI suitable for <img src="...">.
 *
 * @param {Object} options - Same as renderChart
 * @returns {string} data:image/svg+xml;base64,... URI
 */
export function renderChartAsDataURI(options) {
  const svgMarkup = renderChart(options);
  const base64 = Buffer.from(svgMarkup).toString('base64');
  return `data:image/svg+xml;base64,${base64}`;
}
