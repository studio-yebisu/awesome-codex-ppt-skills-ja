#!/usr/bin/env node
/**
 * browser_dom_to_svg.mjs - Convert browser-rendered HTML slides to SVG.
 *
 * This renderer uses Chromium for layout and emits native SVG text nodes
 * instead of outlining text as paths. It is intended as a browser-layout
 * primary HTML-to-SVG renderer for the HTML slide pipeline.
 *
 * Usage:
 *   node browser_dom_to_svg.mjs index.html -o output/svgs
 *   node browser_dom_to_svg.mjs index.html -o output/svgs --slide 8
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { chromium } from 'playwright';
import { parse as parseHTML } from 'node-html-parser';
import { renderChart } from './chart_renderer.mjs';

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 720;

function parseArgs(argv) {
  const args = {
    input: null,
    outputDir: null,
    slide: null,
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
    timeout: 120_000,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '-o' || arg === '--output') {
      args.outputDir = argv[++i];
    } else if (arg === '--slide') {
      args.slide = Number.parseInt(argv[++i], 10);
    } else if (arg === '--width') {
      args.width = Number.parseInt(argv[++i], 10);
    } else if (arg === '--height') {
      args.height = Number.parseInt(argv[++i], 10);
    } else if (arg === '--timeout') {
      args.timeout = Number.parseInt(argv[++i], 10);
    } else if (arg === '-h' || arg === '--help') {
      printHelp();
      process.exit(0);
    } else if (!args.input) {
      args.input = arg;
    } else {
      throw new Error(`Unexpected argument: ${arg}`);
    }
  }

  if (!args.input) throw new Error('Missing input HTML file.');
  if (!args.outputDir) throw new Error('Missing output directory. Use -o <dir>.');
  if (args.slide !== null && (!Number.isInteger(args.slide) || args.slide < 1)) {
    throw new Error('--slide must be a 1-based positive integer.');
  }
  if (!Number.isInteger(args.width) || args.width <= 0) {
    throw new Error('--width must be a positive integer.');
  }
  if (!Number.isInteger(args.height) || args.height <= 0) {
    throw new Error('--height must be a positive integer.');
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node browser_dom_to_svg.mjs <input.html> -o <output_dir> [--slide N]

Options:
  -o, --output <dir>  Output directory for slide_XX.svg files
  --slide <N>         Render only one 1-based slide
  --width <px>        Browser viewport width (default: ${DEFAULT_WIDTH})
  --height <px>       Browser viewport height (default: ${DEFAULT_HEIGHT})
  --timeout <ms>      Browser operation timeout (default: 120000)
`);
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function findBrowserExecutable() {
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  ];
  for (const candidate of candidates) {
    if (await fileExists(candidate)) return candidate;
  }
  return null;
}

function mimeFromPath(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
  if (ext === '.png') return 'image/png';
  if (ext === '.gif') return 'image/gif';
  if (ext === '.webp') return 'image/webp';
  if (ext === '.svg') return 'image/svg+xml';
  return 'application/octet-stream';
}

const TRANSPARENT_PNG_DATA_URI =
  'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/l5CU9QAAAABJRU5ErkJggg==';

async function dataUriForHref(href) {
  if (href.startsWith('file://')) {
    let filePath;
    try {
      filePath = fileURLToPath(href);
    } catch {
      return null;
    }
    if (!(await fileExists(filePath))) {
      console.warn(`Warning: missing local image; embedding transparent placeholder: ${href}`);
      return TRANSPARENT_PNG_DATA_URI;
    }

    const bytes = await fs.readFile(filePath);
    return `data:${mimeFromPath(filePath)};base64,${bytes.toString('base64')}`;
  }

  if (href.startsWith('http://') || href.startsWith('https://')) {
    const requestUrl = href.replace(/&amp;/g, '&');
    try {
      const response = await fetch(requestUrl, { signal: AbortSignal.timeout(15_000) });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const contentType = response.headers.get('content-type')?.split(';')[0] || 'application/octet-stream';
      const bytes = Buffer.from(await response.arrayBuffer());
      return `data:${contentType};base64,${bytes.toString('base64')}`;
    } catch (error) {
      console.warn(`Warning: failed to fetch remote image; embedding transparent placeholder: ${href} (${error.message})`);
      return TRANSPARENT_PNG_DATA_URI;
    }
  }

  return null;
}

async function embedLocalImages(svg) {
  const hrefPattern = /\bhref="([^"]+)"/g;
  const replacements = [];

  for (const match of svg.matchAll(hrefPattern)) {
    const href = match[1];
    if (href.startsWith('data:')) continue;
    const dataUri = await dataUriForHref(href);
    if (dataUri) replacements.push([href, dataUri]);
  }

  let result = svg;
  for (const [from, to] of replacements) {
    result = result.split(from).join(to);
  }
  return result;
}

function parseJsonAttribute(node, attrName) {
  const value = node.getAttribute(attrName);
  return value ? JSON.parse(value) : null;
}

async function collectChartSpecs(inputHtml) {
  const html = await fs.readFile(inputHtml, 'utf-8');
  const root = parseHTML(html);
  const chartNodes = root.querySelectorAll('.chart');
  const specs = [];
  let renderableIndex = 0;

  chartNodes.forEach((node) => {
    const type = node.getAttribute('data-type');
    if (!type) return;
    const index = renderableIndex;
    renderableIndex += 1;

    try {
      const labels = parseJsonAttribute(node, 'data-labels') || [];
      const values = parseJsonAttribute(node, 'data-values') || [];
      const colors = parseJsonAttribute(node, 'data-colors');
      const series = parseJsonAttribute(node, 'data-series');
      const seriesNames = parseJsonAttribute(node, 'data-series-names');
      const title = node.getAttribute('data-title') || '';
      const yLabel = node.getAttribute('data-y-label') || '';
      const width = Number.parseInt(node.getAttribute('data-width') || '', 10) || 800;
      const height = Number.parseInt(node.getAttribute('data-height') || '', 10) || 400;
      const palette = node.getAttribute('data-palette') || '';
      const donut = node.getAttribute('data-donut') !== 'false';

      const chartOptions = {
        type,
        labels,
        values,
        title,
        width,
        height,
        yLabel,
      };

      if (colors) chartOptions.colors = colors;
      if (palette) chartOptions.palette = palette;
      if (series) chartOptions.series = series;
      if (seriesNames) chartOptions.seriesNames = seriesNames;
      if (type === 'pie' || type === 'donut') chartOptions.donut = donut;

      specs.push({
        index,
        width,
        height,
        svg: renderChart(chartOptions),
      });
    } catch (error) {
      console.warn(`Warning: failed to render chart #${index + 1}: ${error.message}`);
    }
  });

  return specs;
}

async function renderSlides(inputHtml, options) {
  const chartSpecs = await collectChartSpecs(inputHtml);
  const browserPath = await findBrowserExecutable();
  const launchOptions = {
    headless: true,
    timeout: options.timeout,
    args: ['--allow-file-access-from-files'],
  };
  if (browserPath) launchOptions.executablePath = browserPath;

  const browser = await chromium.launch(launchOptions);
  try {
    const page = await browser.newPage({
      viewport: { width: options.width, height: options.height },
      deviceScaleFactor: 1,
    });
    page.setDefaultTimeout(options.timeout);

    await page.goto(pathToFileURL(inputHtml).href, {
      waitUntil: 'load',
      timeout: options.timeout,
    });

    if (chartSpecs.length > 0) {
      await page.evaluate((specs) => {
        const charts = Array.from(document.querySelectorAll('.chart[data-type]'));
        for (const spec of specs) {
          const el = charts[spec.index];
          if (!el) continue;
          el.innerHTML = spec.svg;
          el.classList.add('chart-rendered');
          if (!el.style.width) el.style.width = `${spec.width}px`;
          if (!el.style.height) el.style.height = `${spec.height}px`;
        }
      }, chartSpecs);
    }

    await page.addStyleTag({
      content: `
        *, *::before, *::after {
          animation: none !important;
          transition: none !important;
        }
        [data-anim] {
          opacity: 1 !important;
          transform: none !important;
        }
      `,
    });

    await page.evaluate(async (settleTimeout) => {
      if (window.SeaSlidesRuntime?.settleForExport) {
        await window.SeaSlidesRuntime.settleForExport({ timeout: settleTimeout });
        return;
      }
      if (window.__dynamicContentReady) {
        await window.__dynamicContentReady;
        return;
      }
      if (window.Prism) {
        window.Prism.highlightAll();
      }
      if (window.pseudocode && window.katex) {
        document.querySelectorAll('pre.pseudocode').forEach((el) => {
          window.pseudocode.renderElement(el);
        });
      }
      if (window.MathJax?.startup?.promise) {
        await window.MathJax.startup.promise;
      }
      if (window.MathJax?.typesetPromise) {
        await window.MathJax.typesetPromise([document.body]);
      }
    }, options.timeout);

    await page.evaluate(async () => {
      if (document.fonts?.ready) await document.fonts.ready;
      await Promise.all(
        Array.from(document.images)
          .filter((img) => !img.complete)
          .map((img) => new Promise((resolve) => {
            img.addEventListener('load', resolve, { once: true });
            img.addEventListener('error', resolve, { once: true });
          })),
      );
    });

    // Rasterize only MathJax output.  The surrounding slide remains native
    // SVG text and geometry, which the PPTX converter maps to editable
    // DrawingML shapes.  MathJax's nested path-heavy SVG is stored on its
    // container as a transparent PNG and emitted as an SVG <image> below.
    await page.evaluate(async () => {
      const SVG_NS = 'http://www.w3.org/2000/svg';
      const SCALE = 3;

      function svgToPngDataUri(svg, color) {
        return new Promise((resolve) => {
          const rect = svg.getBoundingClientRect();
          const width = Math.max(
            1,
            rect.width || svg.width?.baseVal?.value || svg.viewBox?.baseVal?.width || 1,
          );
          const height = Math.max(
            1,
            rect.height || svg.height?.baseVal?.value || svg.viewBox?.baseVal?.height || 1,
          );
          const clone = svg.cloneNode(true);
          clone.setAttribute('xmlns', SVG_NS);
          clone.removeAttribute('x');
          clone.removeAttribute('y');
          clone.setAttribute('width', String(width));
          clone.setAttribute('height', String(height));
          clone.setAttribute('color', color);
          clone.setAttribute('fill', color);

          const source = new XMLSerializer().serializeToString(clone);
          const blob = new Blob([source], { type: 'image/svg+xml;charset=utf-8' });
          const url = URL.createObjectURL(blob);
          const image = new Image();
          image.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = Math.max(1, Math.ceil(width * SCALE));
            canvas.height = Math.max(1, Math.ceil(height * SCALE));
            const context = canvas.getContext('2d');
            context.scale(SCALE, SCALE);
            context.drawImage(image, 0, 0, width, height);
            URL.revokeObjectURL(url);
            resolve(canvas.toDataURL('image/png'));
          };
          image.onerror = () => {
            URL.revokeObjectURL(url);
            resolve('');
          };
          image.src = url;
        });
      }

      const containers = Array.from(document.querySelectorAll('mjx-container, .MathJax'));
      await Promise.all(containers.map(async (container) => {
        const svg = container.querySelector('svg');
        if (!svg) return;
        const color = window.getComputedStyle(container).color || '#000000';
        const png = await svgToPngDataUri(svg, color);
        if (png) container.dataset.seaslidesMathPng = png;
      }));
    });

    return await page.evaluate(({ slideNumber, viewportWidth, viewportHeight }) => {
      const SVG_NS = 'http://www.w3.org/2000/svg';
      const XLINK_NS = 'http://www.w3.org/1999/xlink';
      let uid = 0;

      function nextId(prefix) {
        uid += 1;
        return `${prefix}-${uid}`;
      }

      function escapeText(value) {
        return String(value ?? '')
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;');
      }

      function escapeAttr(value) {
        return escapeText(value).replace(/"/g, '&quot;');
      }

      function isTransparent(value) {
        if (!value || value === 'transparent' || value === 'none') return true;
        return /^rgba?\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*\)$/i.test(value);
      }

      function colorAttrs(name, value) {
        if (isTransparent(value)) return `${name}="none"`;
        const rgba = String(value).match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)$/i);
        if (!rgba) return `${name}="${escapeAttr(value)}"`;
        const hex = [rgba[1], rgba[2], rgba[3]]
          .map((part) => Number.parseInt(part, 10).toString(16).padStart(2, '0'))
          .join('');
        const alpha = rgba[4] === undefined ? 1 : Number.parseFloat(rgba[4]);
        return alpha < 1
          ? `${name}="#${hex}" ${name}-opacity="${alpha.toFixed(3)}"`
          : `${name}="#${hex}"`;
      }

      function num(value, fallback = 0) {
        const parsed = Number.parseFloat(value);
        return Number.isFinite(parsed) ? parsed : fallback;
      }

      function px(value) {
        return Number.parseFloat(value) || 0;
      }

      function fmt(value) {
        return Number.isFinite(value) ? Number(value.toFixed(3)).toString() : '0';
      }

      function splitTopLevel(value, separator = ',') {
        const parts = [];
        let current = '';
        let depth = 0;
        for (const char of String(value || '')) {
          if (char === '(') depth += 1;
          if (char === ')') depth = Math.max(0, depth - 1);
          if (char === separator && depth === 0) {
            parts.push(current.trim());
            current = '';
          } else {
            current += char;
          }
        }
        if (current.trim()) parts.push(current.trim());
        return parts;
      }

      function splitWhitespaceTopLevel(value) {
        const parts = [];
        let current = '';
        let depth = 0;
        for (const char of String(value || '').trim()) {
          if (char === '(') depth += 1;
          if (char === ')') depth = Math.max(0, depth - 1);
          if (/\s/.test(char) && depth === 0) {
            if (current) {
              parts.push(current);
              current = '';
            }
          } else {
            current += char;
          }
        }
        if (current) parts.push(current);
        return parts;
      }

      function relativeRect(rect, slideRect) {
        return {
          x: rect.left - slideRect.left,
          y: rect.top - slideRect.top,
          width: rect.width,
          height: rect.height,
          right: rect.right - slideRect.left,
          bottom: rect.bottom - slideRect.top,
        };
      }

      function visibleElement(el) {
        if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden') return false;
        if (Number.parseFloat(style.opacity || '1') === 0) return false;
        return true;
      }

      function hasVisibleBox(rect) {
        return rect.width > 0.1 && rect.height > 0.1;
      }

      function imageAspect(style) {
        const fit = style.objectFit || 'fill';
        if (fit === 'cover') return 'xMidYMid slice';
        if (fit === 'contain') return 'xMidYMid meet';
        if (fit === 'none') return 'xMinYMin meet';
        return 'none';
      }

      function borderRadius(style) {
        const radius = px(style.borderTopLeftRadius || style.borderRadius);
        return radius > 0 ? radius : 0;
      }

      function clampRectRadius(radius, rect) {
        if (!Number.isFinite(radius) || radius <= 0) return 0;
        return Math.max(0, Math.min(radius, rect.width / 2, rect.height / 2));
      }

      function roundedRectAttrs(rect, radius = 0) {
        const r = clampRectRadius(radius, rect);
        return `x="${fmt(rect.x)}" y="${fmt(rect.y)}" width="${fmt(rect.width)}" height="${fmt(rect.height)}" rx="${fmt(r)}" ry="${fmt(r)}"`;
      }

      function cssProperty(style, name) {
        return style.getPropertyValue ? style.getPropertyValue(name) : '';
      }

      function textFillColor(style) {
        return style.webkitTextFillColor
          || cssProperty(style, '-webkit-text-fill-color')
          || style.color;
      }

      function isBackgroundClippedToText(style) {
        const clip = `${style.backgroundClip || ''} ${style.webkitBackgroundClip || ''} ${cssProperty(style, '-webkit-background-clip')}`;
        return /\btext\b/i.test(clip)
          && !!style.backgroundImage
          && style.backgroundImage !== 'none';
      }

      function backgroundLayers(bgImage) {
        if (!bgImage || bgImage === 'none') return [];
        return splitTopLevel(String(bgImage)).map((layer) => layer.trim()).filter(Boolean);
      }

      function backgroundList(style, cssName, propertyName) {
        const value = cssProperty(style, cssName) || style[propertyName] || '';
        return splitTopLevel(String(value)).map((entry) => entry.trim()).filter(Boolean);
      }

      function layerValue(values, index, fallback) {
        if (!values.length) return fallback;
        return values[Math.min(index, values.length - 1)] || fallback;
      }

      function insetRect(rect, insets) {
        const x = rect.x + insets.left;
        const y = rect.y + insets.top;
        return {
          x,
          y,
          width: Math.max(0, rect.width - insets.left - insets.right),
          height: Math.max(0, rect.height - insets.top - insets.bottom),
        };
      }

      function backgroundClipRect(rect, radius, clip, style, borderWidths) {
        const insets = { top: 0, right: 0, bottom: 0, left: 0 };
        if (/\bpadding-box\b|\bcontent-box\b/i.test(clip)) {
          insets.top += borderWidths.top;
          insets.right += borderWidths.right;
          insets.bottom += borderWidths.bottom;
          insets.left += borderWidths.left;
        }
        if (/\bcontent-box\b/i.test(clip)) {
          insets.top += px(style.paddingTop);
          insets.right += px(style.paddingRight);
          insets.bottom += px(style.paddingBottom);
          insets.left += px(style.paddingLeft);
        }
        return {
          rect: insetRect(rect, insets),
          radius: Math.max(0, radius - Math.max(insets.top, insets.right, insets.bottom, insets.left)),
        };
      }

      function hasBorder(style) {
        for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
          const width = px(style[`border${side}Width`]);
          const borderStyle = style[`border${side}Style`];
          const color = style[`border${side}Color`];
          if (width > 0 && borderStyle !== 'none' && borderStyle !== 'hidden' && !isTransparent(color)) {
            return true;
          }
        }
        return false;
      }

      function hasRenderableBoxStyle(style) {
        const backgroundPaintsBox = !isBackgroundClippedToText(style);
        return (
          (backgroundPaintsBox && !isTransparent(style.backgroundColor))
          || (backgroundPaintsBox && style.backgroundImage && style.backgroundImage !== 'none')
          || (style.boxShadow && style.boxShadow !== 'none')
          || hasBorder(style)
        );
      }

      function colorStopAttrs(value) {
        const rgba = String(value || '').match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)$/i);
        if (!rgba) return `stop-color="${escapeAttr(value)}"`;
        const hex = [rgba[1], rgba[2], rgba[3]]
          .map((part) => Number.parseInt(part, 10).toString(16).padStart(2, '0'))
          .join('');
        const alpha = rgba[4] === undefined ? 1 : Number.parseFloat(rgba[4]);
        return alpha < 1
          ? `stop-color="#${hex}" stop-opacity="${alpha.toFixed(3)}"`
          : `stop-color="#${hex}"`;
      }

      function parseColorStop(raw, index, total) {
        const tokens = splitWhitespaceTopLevel(raw);
        let offset = total <= 1 ? 0 : index / (total - 1);
        let color = raw.trim();
        if (tokens.length > 1) {
          const position = tokens[tokens.length - 1];
          if (/^-?[\d.]+%$/.test(position)) {
            offset = Number.parseFloat(position) / 100;
            color = tokens.slice(0, -1).join(' ');
          } else if (/^-?[\d.]+px$/.test(position)) {
            color = tokens.slice(0, -1).join(' ');
          }
        }
        return { color, offset: Math.max(0, Math.min(1, offset)) };
      }

      function linearGradientVector(direction) {
        if (!direction) return { x1: 0.5, y1: 0, x2: 0.5, y2: 1 };
        const value = direction.trim().toLowerCase();
        if (value.startsWith('to ')) {
          const words = value.slice(3).split(/\s+/);
          const left = words.includes('left');
          const right = words.includes('right');
          const top = words.includes('top');
          const bottom = words.includes('bottom');
          const x1 = left ? 1 : right ? 0 : 0.5;
          const x2 = left ? 0 : right ? 1 : 0.5;
          const y1 = top ? 1 : bottom ? 0 : 0.5;
          const y2 = top ? 0 : bottom ? 1 : 0.5;
          return { x1, y1, x2, y2 };
        }
        const angle = value.endsWith('turn')
          ? Number.parseFloat(value) * 360
          : value.endsWith('rad')
            ? Number.parseFloat(value) * 180 / Math.PI
            : Number.parseFloat(value);
        if (!Number.isFinite(angle)) return { x1: 0.5, y1: 0, x2: 0.5, y2: 1 };
        const rad = angle * Math.PI / 180;
        const dx = Math.sin(rad);
        const dy = -Math.cos(rad);
        return {
          x1: 0.5 - dx / 2,
          y1: 0.5 - dy / 2,
          x2: 0.5 + dx / 2,
          y2: 0.5 + dy / 2,
        };
      }

      function createGradientDef(bgImage, defs, rect = null) {
        if (!bgImage || bgImage === 'none') return '';
        const layers = backgroundLayers(bgImage);
        if (layers.length !== 1) return '';

        const layer = layers[0];
        const linear = layer.match(/^linear-gradient\((.*)\)$/i);
        const radial = layer.match(/^radial-gradient\((.*)\)$/i);
        if (!linear && !radial) return '';

        const args = splitTopLevel(linear ? linear[1] : radial[1]);
        if (!args.length) return '';

        let stops = args;
        if (linear) {
          let direction = '';
          if (/^(to\s+|-?[\d.]+(?:deg|rad|turn)$)/i.test(args[0])) {
            direction = args[0];
            stops = args.slice(1);
          }
          if (!stops.length) return '';
          const id = nextId('grad-linear');
          const vector = linearGradientVector(direction);
          const stopMarkup = stops.map((stop, index) => {
            const parsed = parseColorStop(stop, index, stops.length);
            return `<stop offset="${fmt(parsed.offset)}" ${colorStopAttrs(parsed.color)}/>`;
          }).join('');
          if (rect) {
            defs.push(
              `<linearGradient id="${id}" gradientUnits="userSpaceOnUse" x1="${fmt(rect.x + vector.x1 * rect.width)}" y1="${fmt(rect.y + vector.y1 * rect.height)}" x2="${fmt(rect.x + vector.x2 * rect.width)}" y2="${fmt(rect.y + vector.y2 * rect.height)}">${stopMarkup}</linearGradient>`
            );
          } else {
            defs.push(
              `<linearGradient id="${id}" x1="${fmt(vector.x1)}" y1="${fmt(vector.y1)}" x2="${fmt(vector.x2)}" y2="${fmt(vector.y2)}">${stopMarkup}</linearGradient>`
            );
          }
          return id;
        }

        if (radial) {
          if (/^(circle|ellipse|closest|farthest|at\s+)/i.test(args[0])) {
            stops = args.slice(1);
          }
          if (!stops.length) return '';
          const id = nextId('grad-radial');
          const stopMarkup = stops.map((stop, index) => {
            const parsed = parseColorStop(stop, index, stops.length);
            return `<stop offset="${fmt(parsed.offset)}" ${colorStopAttrs(parsed.color)}/>`;
          }).join('');
          if (rect) {
            defs.push(`<radialGradient id="${id}" gradientUnits="userSpaceOnUse" cx="${fmt(rect.x + rect.width / 2)}" cy="${fmt(rect.y + rect.height / 2)}" r="${fmt(Math.max(rect.width, rect.height) * 0.75)}">${stopMarkup}</radialGradient>`);
          } else {
            defs.push(`<radialGradient id="${id}" cx="0.5" cy="0.5" r="0.75">${stopMarkup}</radialGradient>`);
          }
          return id;
        }
        return '';
      }

      function renderGradientRect(bgImage, rect, radius, defs) {
        const id = createGradientDef(bgImage, defs);
        return id ? `<rect ${roundedRectAttrs(rect, radius)} fill="url(#${id})"/>` : '';
      }

      function renderBackgroundImageLayers(bgImage, rect, radius, style, borderWidths, defs) {
        const layers = backgroundLayers(bgImage);
        if (!layers.length) return '';

        const clips = backgroundList(style, 'background-clip', 'backgroundClip');
        const parts = [];
        for (let index = layers.length - 1; index >= 0; index -= 1) {
          const clip = layerValue(clips, index, 'border-box');
          if (/\btext\b/i.test(clip)) continue;

          const box = backgroundClipRect(rect, radius, clip, style, borderWidths);
          const gradientRect = renderGradientRect(layers[index], box.rect, box.radius, defs);
          if (gradientRect) parts.push(gradientRect);
        }
        return parts.join('');
      }

      function parseShadow(shadow) {
        if (!shadow || shadow === 'none' || /\binset\b/i.test(shadow)) return null;
        const colorMatch = shadow.match(/rgba?\([^)]+\)|#[0-9a-fA-F]{3,8}/);
        const color = colorMatch ? colorMatch[0] : 'rgba(0, 0, 0, 0.25)';
        const lengths = shadow
          .replace(color, '')
          .match(/-?[\d.]+px/g)
          ?.map((part) => Number.parseFloat(part)) || [];
        if (lengths.length < 2) return null;
        return {
          color,
          offsetX: lengths[0] || 0,
          offsetY: lengths[1] || 0,
          blur: lengths[2] || 0,
          spread: lengths[3] || 0,
        };
      }

      function renderBoxShadows(rect, radius, style, defs) {
        if (!style.boxShadow || style.boxShadow === 'none') return '';
        const parts = [];
        for (const rawShadow of splitTopLevel(style.boxShadow)) {
          const shadow = parseShadow(rawShadow);
          if (!shadow) continue;
          const x = rect.x + shadow.offsetX - shadow.spread;
          const y = rect.y + shadow.offsetY - shadow.spread;
          const width = rect.width + shadow.spread * 2;
          const height = rect.height + shadow.spread * 2;
          let filterAttr = '';
          if (shadow.blur > 0) {
            const filterId = nextId('shadow');
            defs.push(`<filter id="${filterId}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="${fmt(shadow.blur / 2)}"/></filter>`);
            filterAttr = ` filter="url(#${filterId})"`;
          }
          parts.push(`<rect ${roundedRectAttrs({ x, y, width, height }, radius)} ${colorAttrs('fill', shadow.color)}${filterAttr}/>`);
        }
        return parts.join('');
      }

      function parseTransformOrigin(origin, rect) {
        const parts = String(origin || '').split(/\s+/);
        const x = Number.parseFloat(parts[0]);
        const y = Number.parseFloat(parts[1]);
        return {
          x: rect.x + (Number.isFinite(x) ? x : rect.width / 2),
          y: rect.y + (Number.isFinite(y) ? y : rect.height / 2),
        };
      }

      function parseCssTransformMatrix(transform) {
        if (!transform || transform === 'none') return '';
        const matrix = transform.match(/^matrix\(([^)]+)\)$/);
        if (matrix) {
          const values = matrix[1].split(',').map((part) => Number.parseFloat(part.trim()));
          if (values.length === 6 && values.every((value) => Number.isFinite(value))) return values;
        }
        const matrix3d = transform.match(/^matrix3d\(([^)]+)\)$/);
        if (matrix3d) {
          const values = matrix3d[1].split(',').map((part) => Number.parseFloat(part.trim()));
          if (values.length === 16 && values.every((value) => Number.isFinite(value))) {
            return [values[0], values[1], values[4], values[5], values[12], values[13]];
          }
        }
        return null;
      }

      function svgTransformFromCss(transform, origin, rect) {
        const values = parseCssTransformMatrix(transform);
        if (!values) return '';
        const point = parseTransformOrigin(origin, rect);
        return `translate(${fmt(point.x)} ${fmt(point.y)}) matrix(${values.map(fmt).join(' ')}) translate(${fmt(-point.x)} ${fmt(-point.y)})`;
      }

      function borderDashAttrs(borderStyle, width) {
        if (borderStyle === 'dotted') {
          return ` stroke-dasharray="0 ${fmt(width * 2)}" stroke-dashoffset="1" stroke-linejoin="round" stroke-linecap="round"`;
        }
        if (borderStyle === 'dashed') {
          return ` stroke-dasharray="${fmt(width * 2)} 4"`;
        }
        return '';
      }

      function renderBackground(el, rect, style, defs) {
        const parts = [];
        const bg = style.backgroundColor;
        const bgImage = style.backgroundImage;
        const radius = borderRadius(style);
        const backgroundPaintsBox = !isBackgroundClippedToText(style);
        const borderWidths = {
          top: px(style.borderTopWidth),
          right: px(style.borderRightWidth),
          bottom: px(style.borderBottomWidth),
          left: px(style.borderLeftWidth),
        };

        parts.push(renderBoxShadows(rect, radius, style, defs));

        if (backgroundPaintsBox && !isTransparent(bg)) {
          parts.push(
            `<rect ${roundedRectAttrs(rect, radius)} ${colorAttrs('fill', bg)}/>`
          );
        }

        const backgroundImageLayers = backgroundPaintsBox
          ? renderBackgroundImageLayers(bgImage, rect, radius, style, borderWidths, defs)
          : '';
        if (backgroundImageLayers) parts.push(backgroundImageLayers);

        const urlMatch = bgImage && bgImage !== 'none'
          ? bgImage.match(/url\(["']?(.+?)["']?\)/)
          : null;
        if (urlMatch) {
          const clipId = nextId('clip-bg');
          defs.push(`<clipPath id="${clipId}"><rect ${roundedRectAttrs(rect, radius)}/></clipPath>`);
          parts.push(`<image x="${fmt(rect.x)}" y="${fmt(rect.y)}" width="${fmt(rect.width)}" height="${fmt(rect.height)}" href="${escapeAttr(urlMatch[1])}" preserveAspectRatio="xMidYMid slice" clip-path="url(#${clipId})"/>`);
        }

        const borderStyles = {
          top: style.borderTopStyle,
          right: style.borderRightStyle,
          bottom: style.borderBottomStyle,
          left: style.borderLeftStyle,
        };
        const borderColors = {
          top: style.borderTopColor,
          right: style.borderRightColor,
          bottom: style.borderBottomColor,
          left: style.borderLeftColor,
        };

        const sameBorder =
          borderWidths.top === borderWidths.right &&
          borderWidths.top === borderWidths.bottom &&
          borderWidths.top === borderWidths.left &&
          borderColors.top === borderColors.right &&
          borderColors.top === borderColors.bottom &&
          borderColors.top === borderColors.left &&
          borderStyles.top === borderStyles.right &&
          borderStyles.top === borderStyles.bottom &&
          borderStyles.top === borderStyles.left;

        if (
          sameBorder &&
          borderWidths.top > 0 &&
          borderStyles.top !== 'none' &&
          borderStyles.top !== 'hidden' &&
          !isTransparent(borderColors.top)
        ) {
          const inset = borderWidths.top / 2;
          const dash = borderDashAttrs(borderStyles.top, borderWidths.top);
          const borderRect = {
            x: rect.x + inset,
            y: rect.y + inset,
            width: Math.max(0, rect.width - borderWidths.top),
            height: Math.max(0, rect.height - borderWidths.top),
          };
          parts.push(
            `<rect ${roundedRectAttrs(borderRect, Math.max(0, radius - inset))} fill="none" ${colorAttrs('stroke', borderColors.top)} stroke-width="${fmt(borderWidths.top)}"${dash}/>`
          );
        } else {
          const lineForSide = (side) => {
            const inset = borderWidths[side] / 2;
            if (side === 'top') return [rect.x, rect.y + inset, rect.right, rect.y + inset];
            if (side === 'right') return [rect.right - inset, rect.y, rect.right - inset, rect.bottom];
            if (side === 'bottom') return [rect.x, rect.bottom - inset, rect.right, rect.bottom - inset];
            return [rect.x + inset, rect.y, rect.x + inset, rect.bottom];
          };
          for (const side of ['top', 'right', 'bottom', 'left']) {
            if (borderWidths[side] <= 0) continue;
            if (borderStyles[side] === 'none' || borderStyles[side] === 'hidden') continue;
            if (isTransparent(borderColors[side])) continue;
            const [x1, y1, x2, y2] = lineForSide(side);
            const dash = borderDashAttrs(borderStyles[side], borderWidths[side]);
            parts.push(`<line x1="${fmt(x1)}" y1="${fmt(y1)}" x2="${fmt(x2)}" y2="${fmt(y2)}" ${colorAttrs('stroke', borderColors[side])} stroke-width="${fmt(borderWidths[side])}"${dash}/>`);
          }
        }

        return parts.join('');
      }

      function renderImage(el, rect, style, defs) {
        const href = el.currentSrc || el.src;
        if (!href) return '';
        const radius = borderRadius(style);
        const clipId = nextId('clip-img');
        defs.push(`<clipPath id="${clipId}"><rect ${roundedRectAttrs(rect, radius)}/></clipPath>`);
        return `<image x="${fmt(rect.x)}" y="${fmt(rect.y)}" width="${fmt(rect.width)}" height="${fmt(rect.height)}" href="${escapeAttr(href)}" preserveAspectRatio="${imageAspect(style)}" clip-path="url(#${clipId})"/>`;
      }

      function renderCanvas(el, rect, style, defs) {
        let href = '';
        try {
          href = el.toDataURL('image/png');
        } catch {
          return '';
        }
        const radius = borderRadius(style);
        const clipId = nextId('clip-canvas');
        defs.push(`<clipPath id="${clipId}"><rect ${roundedRectAttrs(rect, radius)}/></clipPath>`);
        return `<image x="${fmt(rect.x)}" y="${fmt(rect.y)}" width="${fmt(rect.width)}" height="${fmt(rect.height)}" href="${escapeAttr(href)}" preserveAspectRatio="none" clip-path="url(#${clipId})"/>`;
      }

      function isMathJaxContainer(el) {
        const tagName = el.tagName?.toLowerCase();
        return tagName === 'mjx-container' || el.classList?.contains('MathJax');
      }

      function isMathJaxSvg(el) {
        return !!(el.closest?.('mjx-container') || el.querySelector?.('[data-mml-node]'));
      }

      function isAssistiveMathElement(el) {
        if (!el.classList) return false;
        return !!(
          el.classList.contains('katex-mathml')
          || el.closest('.katex-mathml')
          || el.classList.contains('MJX_Assistive_MathML')
          || el.closest('.MJX_Assistive_MathML')
        );
      }

      function hasPreformattedWhitespace(el) {
        if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;
        const style = window.getComputedStyle(el);
        return !!(
          el.closest('pre, code')
          || style.whiteSpace === 'pre'
          || style.whiteSpace === 'pre-wrap'
          || style.whiteSpace === 'break-spaces'
        );
      }

      function clipsOverflow(style) {
        return [style.overflow, style.overflowX, style.overflowY].some((value) => (
          value === 'hidden' || value === 'auto' || value === 'scroll'
        ));
      }

      function directTextNodes(el, preserveWhitespace = false) {
        return Array.from(el.childNodes).filter((node) => {
          if (node.nodeType !== Node.TEXT_NODE || !node.textContent) return false;
          return preserveWhitespace ? node.textContent.length > 0 : node.textContent.trim();
        });
      }

      function textFragments(node, preserveWhitespace = false) {
        const text = node.textContent || '';
        if (preserveWhitespace ? text.length === 0 : !text.trim()) return [];
        const range = document.createRange();
        const fragments = [];
        for (let i = 0; i < text.length; i += 1) {
          range.setStart(node, 0);
          range.setEnd(node, i + 1);
          const rects = Array.from(range.getClientRects()).filter(hasVisibleBox);
          if (!rects.length) continue;
          const index = rects.length - 1;
          if (!fragments[index]) fragments[index] = { text: '', rect: rects[index] };
          fragments[index].text += text.charAt(i);
          fragments[index].rect = rects[index];
        }
        range.detach?.();
        return fragments.filter(Boolean);
      }

      function normalizeFragmentText(text, preserveWhitespace) {
        if (preserveWhitespace) return text.replace(/\r?\n/g, '');
        return text.replace(/\s+/g, ' ');
      }

      function textFillAttrs(style, rect, defs) {
        if (isBackgroundClippedToText(style)) {
          const id = createGradientDef(style.backgroundImage, defs, rect);
          if (id) return `fill="url(#${id})"`;
        }
        const fill = textFillColor(style);
        return colorAttrs('fill', !isTransparent(fill) ? fill : style.color);
      }

      function renderText(el, slideRect, defs, elementRect) {
        const style = window.getComputedStyle(el);
        const preserveWhitespace = hasPreformattedWhitespace(el);
        const fontSize = num(style.fontSize, 16);
        const fontFamily = style.fontFamily || 'sans-serif';
        const fontWeight = style.fontWeight || '400';
        const fontStyle = style.fontStyle || 'normal';
        const letterSpacing = style.letterSpacing && style.letterSpacing !== 'normal'
          ? ` letter-spacing="${fmt(px(style.letterSpacing))}"`
          : '';
        const textAnchor = style.textAlign === 'center'
          ? 'middle'
          : style.textAlign === 'right' || style.textAlign === 'end'
            ? 'end'
            : 'start';
        const writingMode = style.writingMode && style.writingMode !== 'horizontal-tb'
          ? ` writing-mode="${escapeAttr(style.writingMode)}"`
          : '';
        const fillAttrs = textFillAttrs(style, elementRect, defs);

        const chunks = [];
        for (const node of directTextNodes(el, preserveWhitespace)) {
          for (const fragment of textFragments(node, preserveWhitespace)) {
            const text = normalizeFragmentText(fragment.text, preserveWhitespace);
            if (preserveWhitespace ? text.length === 0 : !text.trim()) continue;
            const rect = relativeRect(fragment.rect, slideRect);
            let x = rect.x;
            if (textAnchor === 'middle') x = rect.x + rect.width / 2;
            if (textAnchor === 'end') x = rect.x + rect.width;
            const baseline = rect.y + ((rect.height - fontSize) / 2) + fontSize * 0.86;
            // Preserve Chromium's measured inline-fragment advance.  The
            // standalone SVG does not carry the page's loaded web fonts, so
            // an SVG renderer may fall back to a wider font even though the
            // text starts at the correct browser-laid-out position.  Without
            // this constraint, a line can grow into an adjacent column.
            const textLength = rect.width > 0
              ? ` textLength="${fmt(rect.width)}" lengthAdjust="spacingAndGlyphs"`
              : '';
            chunks.push(
              `<text x="${fmt(x)}" y="${fmt(baseline)}" font-family="${escapeAttr(fontFamily)}" font-size="${fmt(fontSize)}" font-weight="${escapeAttr(fontWeight)}" font-style="${escapeAttr(fontStyle)}" text-anchor="${textAnchor}" xml:space="preserve"${textLength}${letterSpacing}${writingMode} ${fillAttrs}>${escapeText(text)}</text>`
            );
          }
        }
        return chunks.join('');
      }

      function svgStyleAttributes(tagName) {
        if (tagName === 'text' || tagName === 'tspan') {
          return [
            'fill',
            'fill-opacity',
            'opacity',
            'font-family',
            'font-size',
            'font-weight',
            'font-style',
            'text-anchor',
            'letter-spacing',
          ];
        }
        if (tagName === 'line' || tagName === 'polyline') {
          return [
            'stroke',
            'stroke-opacity',
            'stroke-width',
            'stroke-linecap',
            'stroke-linejoin',
            'stroke-dasharray',
            'opacity',
            'fill',
            'fill-opacity',
          ];
        }
        if (['path', 'rect', 'circle', 'ellipse', 'polygon'].includes(tagName)) {
          return [
            'fill',
            'fill-opacity',
            'stroke',
            'stroke-opacity',
            'stroke-width',
            'stroke-linecap',
            'stroke-linejoin',
            'stroke-dasharray',
            'opacity',
          ];
        }
        return ['opacity'];
      }

      function copySvgPresentationStyles(source, target) {
        if (source.nodeType !== Node.ELEMENT_NODE || target.nodeType !== Node.ELEMENT_NODE) return;
        const tagName = source.tagName.toLowerCase();
        if (tagName !== 'svg') {
          const style = window.getComputedStyle(source);
          for (const attr of svgStyleAttributes(tagName)) {
            const value = style.getPropertyValue(attr);
            if (!value || value === 'normal' || value === 'auto') continue;
            if ((attr === 'stroke' || attr === 'fill') && value === 'none') {
              target.setAttribute(attr, 'none');
              continue;
            }
            target.setAttribute(attr, value);
          }
        }
        const sourceChildren = Array.from(source.children);
        const targetChildren = Array.from(target.children);
        for (let i = 0; i < sourceChildren.length; i += 1) {
          if (targetChildren[i]) copySvgPresentationStyles(sourceChildren[i], targetChildren[i]);
        }
      }

      function absoluteUrl(value) {
        if (!value || value.startsWith('data:') || value.startsWith('blob:')) return value;
        try {
          return new URL(value, document.baseURI).href;
        } catch {
          return value;
        }
      }

      function normalizeInlineSvgImageHrefs(source, clone) {
        const sourceImages = Array.from(source.querySelectorAll('image'));
        const cloneImages = Array.from(clone.querySelectorAll('image'));
        for (let i = 0; i < sourceImages.length; i += 1) {
          const sourceImage = sourceImages[i];
          const cloneImage = cloneImages[i];
          if (!cloneImage) continue;
          const href = sourceImage.getAttribute('href') || sourceImage.getAttributeNS(XLINK_NS, 'href');
          if (!href) continue;
          const normalized = absoluteUrl(href);
          cloneImage.setAttribute('href', normalized);
          cloneImage.setAttributeNS(XLINK_NS, 'href', normalized);
        }
      }

      function serializeInlineSvg(el, rect, options = {}) {
        const clone = el.cloneNode(true);
        clone.setAttribute('x', fmt(rect.x));
        clone.setAttribute('y', fmt(rect.y));
        clone.setAttribute('width', fmt(rect.width));
        clone.setAttribute('height', fmt(rect.height));
        normalizeInlineSvgImageHrefs(el, clone);
        if (options.fill) {
          clone.setAttribute('color', options.fill);
          clone.setAttribute('fill', options.fill);
        } else {
          copySvgPresentationStyles(el, clone);
        }
        return new XMLSerializer().serializeToString(clone);
      }

      function renderMathJax(el, slideRect) {
        const svg = el.querySelector('svg');
        if (!svg) return '';
        const rawRect = svg.getBoundingClientRect();
        if (!hasVisibleBox(rawRect)) return '';
        const rect = relativeRect(rawRect, slideRect);
        const png = el.dataset.seaslidesMathPng;
        if (png) {
          return `<image x="${fmt(rect.x)}" y="${fmt(rect.y)}" width="${fmt(rect.width)}" height="${fmt(rect.height)}" href="${escapeAttr(png)}" preserveAspectRatio="none"/>`;
        }
        const style = window.getComputedStyle(el);
        return serializeInlineSvg(svg, rect, { fill: style.color });
      }

      function orderedChildren(el) {
        return Array.from(el.children)
          .map((child, index) => {
            const zIndex = Number.parseInt(window.getComputedStyle(child).zIndex, 10);
            return { child, index, zIndex: Number.isFinite(zIndex) ? zIndex : 0 };
          })
          .sort((a, b) => a.zIndex - b.zIndex || a.index - b.index)
          .map((item) => item.child);
      }

      function shouldRenderInlineFragments(tagName, style) {
        return (
          (tagName === 'span' || tagName === 'mark')
          && style.display.startsWith('inline')
          && hasRenderableBoxStyle(style)
        );
      }

      function renderInlineFragmentBackgrounds(el, slideRect, style, defs) {
        const preserveWhitespace = hasPreformattedWhitespace(el);
        const chunks = [];
        for (const node of directTextNodes(el, preserveWhitespace)) {
          for (const fragment of textFragments(node, preserveWhitespace)) {
            const text = normalizeFragmentText(fragment.text, preserveWhitespace);
            if (preserveWhitespace ? text.length === 0 : !text.trim()) continue;
            chunks.push(renderBackground(el, relativeRect(fragment.rect, slideRect), style, defs));
          }
        }
        return chunks.join('');
      }

      function wrapStyleGroup(output, style) {
        if (!output) return output;
        const attrs = [];
        const styleDecls = [];
        const opacity = Number.parseFloat(style.opacity || '1');
        if (Number.isFinite(opacity) && opacity !== 1) attrs.push(`opacity="${fmt(opacity)}"`);
        if (style.mixBlendMode && style.mixBlendMode !== 'normal') {
          styleDecls.push(`mix-blend-mode:${style.mixBlendMode}`);
        }
        if (style.clipPath && style.clipPath !== 'none') {
          styleDecls.push(`clip-path:${style.clipPath.replace(/"/g, "'")}`);
        }
        if (styleDecls.length) attrs.push(`style="${escapeAttr(styleDecls.join(';'))}"`);
        if (!attrs.length) return output;
        return `<g ${attrs.join(' ')}>${output}</g>`;
      }

      function renderElement(el, slideRect, defs) {
        if (!visibleElement(el)) return '';
        if (isAssistiveMathElement(el)) return '';

        const tagName = el.tagName.toLowerCase();
        const namespace = el.namespaceURI;
        if (namespace === SVG_NS && tagName !== 'svg') return '';
        if (isMathJaxContainer(el)) return renderMathJax(el, slideRect);

        const originalStyle = window.getComputedStyle(el);
        const transformValue = originalStyle.transform;
        const transformOrigin = originalStyle.transformOrigin;
        const hasTransform = transformValue && transformValue !== 'none';
        const previousInlineTransform = el.style.transform;
        if (hasTransform) {
          el.style.transform = 'none';
        }

        let output = '';
        try {
          const style = hasTransform ? window.getComputedStyle(el) : originalStyle;
          const rawRect = el.getBoundingClientRect();
          const rect = relativeRect(rawRect, slideRect);
          let skipChildren = false;
          const fragmentBackground = shouldRenderInlineFragments(tagName, style);

          if (hasVisibleBox(rawRect)) {
            if (tagName === 'img') {
              output += renderImage(el, rect, style, defs);
            } else if (tagName === 'canvas') {
              output += renderBackground(el, rect, style, defs);
              output += renderCanvas(el, rect, style, defs);
              skipChildren = true;
            } else if (namespace === SVG_NS && tagName === 'svg') {
              output += serializeInlineSvg(el, rect, isMathJaxSvg(el) ? { fill: style.color } : {});
              skipChildren = true;
            } else if (fragmentBackground) {
              output += renderInlineFragmentBackgrounds(el, slideRect, style, defs);
            } else {
              output += renderBackground(el, rect, style, defs);
            }
          }

          let content = '';
          if (!skipChildren) {
            content = renderText(el, slideRect, defs, rect);

            for (const child of orderedChildren(el)) {
              content += renderElement(child, slideRect, defs);
            }
          }

          if (content && hasVisibleBox(rawRect) && clipsOverflow(style)) {
            const clipId = nextId('clip-overflow');
            defs.push(`<clipPath id="${clipId}"><rect ${roundedRectAttrs(rect, borderRadius(style))}/></clipPath>`);
            output += `<g clip-path="url(#${clipId})">${content}</g>`;
          } else {
            output += content;
          }

          const transformAttr = hasTransform ? svgTransformFromCss(transformValue, transformOrigin, rect) : '';
          if (transformAttr && output) {
            output = `<g transform="${escapeAttr(transformAttr)}">${output}</g>`;
          }
          output = wrapStyleGroup(output, style);
          return output;
        } finally {
          if (hasTransform) {
            if (previousInlineTransform) {
              el.style.transform = previousInlineTransform;
            } else {
              el.style.removeProperty('transform');
            }
          }
        }
      }

      function shouldUseViewportDeckBox(slide) {
        const deck = document.getElementById('deck');
        if (!deck) return false;
        const deckRect = deck.getBoundingClientRect();
        const slideRect = slide.getBoundingClientRect();
        return (
          deckRect.width > viewportWidth * 1.5 &&
          slideRect.width > viewportWidth * 1.5 &&
          Math.abs(deckRect.width - slideRect.width) <= 2
        );
      }

      function withFixedSlideCanvas(slide, callback) {
        const deck = document.getElementById('deck');
        const shouldFixDeck = shouldUseViewportDeckBox(slide);
        const previous = {
          deckWidth: deck ? deck.style.width : '',
          deckHeight: deck ? deck.style.height : '',
          slideWidth: slide.style.width,
          slideHeight: slide.style.height,
          slideMinWidth: slide.style.minWidth,
          slideMinHeight: slide.style.minHeight,
          slideMaxWidth: slide.style.maxWidth,
          slideMaxHeight: slide.style.maxHeight,
          slideBoxSizing: slide.style.boxSizing,
        };

        if (deck && shouldFixDeck) {
          deck.style.width = `${viewportWidth}px`;
          deck.style.height = `${viewportHeight}px`;
        }
        slide.style.width = `${viewportWidth}px`;
        slide.style.height = `${viewportHeight}px`;
        slide.style.minWidth = `${viewportWidth}px`;
        slide.style.minHeight = `${viewportHeight}px`;
        slide.style.maxWidth = `${viewportWidth}px`;
        slide.style.maxHeight = `${viewportHeight}px`;
        slide.style.boxSizing = 'border-box';

        try {
          return callback();
        } finally {
          if (deck && shouldFixDeck) {
            deck.style.width = previous.deckWidth;
            deck.style.height = previous.deckHeight;
          }
          slide.style.width = previous.slideWidth;
          slide.style.height = previous.slideHeight;
          slide.style.minWidth = previous.slideMinWidth;
          slide.style.minHeight = previous.slideMinHeight;
          slide.style.maxWidth = previous.slideMaxWidth;
          slide.style.maxHeight = previous.slideMaxHeight;
          slide.style.boxSizing = previous.slideBoxSizing;
        }
      }

      function presentationSlides() {
        const sectionSlides = Array.from(document.querySelectorAll('section.slide'));
        if (sectionSlides.length) return sectionSlides;
        return Array.from(document.querySelectorAll('.slide'))
          .filter((candidate) => !candidate.classList.contains('slide-background') && !candidate.closest('.backgrounds'));
      }

      function withActiveSlide(slide, slideIndex, callback) {
        const slides = presentationSlides();
        const needsActiveClass =
          slides.some((candidate) => candidate.classList.contains('active')) ||
          slides.some((candidate) => candidate.classList.contains('present')) ||
          getComputedStyle(slide).display === 'none';

        if (!needsActiveClass) return callback();

        const previous = slides.map((candidate) => ({
          className: candidate.className,
          style: candidate.getAttribute('style'),
        }));
        slides.forEach((candidate, index) => {
          const selected = index === slideIndex;
          candidate.classList.toggle('active', selected);
          candidate.classList.toggle('present', selected);
          if (selected) {
            const computedDisplay = getComputedStyle(candidate).display;
            candidate.classList.remove('past', 'future');
            if (computedDisplay === 'none') candidate.style.display = 'block';
            candidate.style.visibility = 'visible';
            candidate.style.opacity = '1';
            candidate.style.transform = 'none';
            candidate.style.left = '0px';
            candidate.style.top = '0px';
          }
        });

        try {
          return callback();
        } finally {
          slides.forEach((candidate, index) => {
            candidate.className = previous[index].className;
            const previousStyle = previous[index].style;
            if (previousStyle === null) candidate.removeAttribute('style');
            else candidate.setAttribute('style', previousStyle);
          });
        }
      }

      function renderSlide(slide, index) {
        return withActiveSlide(slide, index - 1, () => withFixedSlideCanvas(slide, () => {
          const slideRect = slide.getBoundingClientRect();
          const width = viewportWidth || slideRect.width || 1280;
          const height = viewportHeight || slideRect.height || 720;
          const defs = [];
          const body = renderElement(slide, slideRect, defs);
          const defsBlock = defs.length ? `<defs>${defs.join('')}</defs>` : '';
          const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="${XLINK_NS}" width="${fmt(width)}" height="${fmt(height)}" viewBox="0 0 ${fmt(width)} ${fmt(height)}">${defsBlock}${body}</svg>`;
          return {
            index,
            svg,
            stats: {
              textNodes: (svg.match(/<text\b/g) || []).length,
              images: (svg.match(/<image\b/g) || []).length,
              paths: (svg.match(/<path\b/g) || []).length,
              bytes: svg.length,
            },
          };
        }));
      }

      const deck = document.getElementById('deck');
      if (deck) {
        deck.style.transform = 'none';
        deck.style.transition = 'none';
      }

      const slides = presentationSlides();
      const targets = slides.length ? slides : [document.body];
      const selected = slideNumber
        ? targets.filter((_, index) => index + 1 === slideNumber)
        : targets;

      return selected.map((slide, offset) => {
        const index = slideNumber || offset + 1;
        return renderSlide(slide, index);
      });
    }, {
      slideNumber: options.slide,
      viewportWidth: options.width,
      viewportHeight: options.height,
    });
  } finally {
    await browser.close();
  }
}

async function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const inputHtml = path.resolve(args.input);
    const outputDir = path.resolve(args.outputDir);

    if (!(await fileExists(inputHtml))) {
      throw new Error(`Input HTML not found: ${inputHtml}`);
    }

    await fs.mkdir(outputDir, { recursive: true });
    const slides = await renderSlides(inputHtml, args);
    if (!slides.length) {
      throw new Error(args.slide ? `Slide ${args.slide} not found.` : 'No renderable slides found.');
    }

    for (const slide of slides) {
      const svg = await embedLocalImages(slide.svg);
      const outPath = path.join(outputDir, `slide_${String(slide.index).padStart(2, '0')}.svg`);
      await fs.writeFile(outPath, svg, 'utf8');
      console.log(`-> ${path.relative(process.cwd(), outPath)} text=${slide.stats.textNodes} images=${slide.stats.images} bytes=${svg.length}`);
    }
    console.log(`Done! Rendered ${slides.length} slide(s).`);
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

await main();
