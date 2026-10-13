#!/usr/bin/env node
/**
 * browser_html_to_png.mjs - Screenshot assembled HTML slides directly.
 *
 * This is a diagnostic companion to browser_dom_to_svg.mjs. It captures what
 * Chromium actually renders from index.html, before the DOM-to-SVG
 * conversion layer, so output/browser_pngs can be compared with output/pngs.
 *
 * Usage:
 *   node browser_html_to_png.mjs index.html -o output/browser_pngs
 *   node browser_html_to_png.mjs index.html -o output/browser_pngs --slide 8
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
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
    scale: 2,
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
    } else if (arg === '--scale') {
      args.scale = Number.parseFloat(argv[++i]);
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
  if (!Number.isFinite(args.scale) || args.scale <= 0) {
    throw new Error('--scale must be a positive number.');
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node browser_html_to_png.mjs <input.html> -o <output_dir> [--slide N]

Options:
  -o, --output <dir>  Output directory for slide_XX.png files
  --slide <N>         Render only one 1-based slide
  --width <px>        Browser viewport width (default: ${DEFAULT_WIDTH})
  --height <px>       Browser viewport height (default: ${DEFAULT_HEIGHT})
  --scale <n>         Device scale factor (default: 2)
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

async function preparePage(page, inputHtml, chartSpecs, timeout) {
  await page.goto(pathToFileURL(inputHtml).href, {
    waitUntil: 'load',
    timeout,
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
      #hint, #nav {
        display: none !important;
      }
      html, body {
        overflow: hidden !important;
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
      if (document.fonts?.ready) await document.fonts.ready;
      await Promise.all(
        Array.from(document.images)
          .filter((img) => !img.complete)
          .map((img) => new Promise((resolve) => {
            img.addEventListener('load', resolve, { once: true });
            img.addEventListener('error', resolve, { once: true });
          })),
      );
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
    if (document.fonts?.ready) await document.fonts.ready;
    await Promise.all(
      Array.from(document.images)
        .filter((img) => !img.complete)
        .map((img) => new Promise((resolve) => {
          img.addEventListener('load', resolve, { once: true });
          img.addEventListener('error', resolve, { once: true });
        })),
    );
  }, timeout);
}

async function getSlideIndexes(page, selectedSlide) {
  const count = await page.evaluate(() => {
    const sectionSlides = Array.from(document.querySelectorAll('section.slide'));
    const slides = sectionSlides.length
      ? sectionSlides
      : Array.from(document.querySelectorAll('.slide'))
        .filter((slide) => !slide.classList.contains('slide-background') && !slide.closest('.backgrounds'));
    return slides.length || 1;
  });
  if (selectedSlide) {
    if (selectedSlide > count) throw new Error(`Slide ${selectedSlide} not found.`);
    return [selectedSlide - 1];
  }
  return Array.from({ length: count }, (_, index) => index);
}

async function showSlide(page, index) {
  await page.evaluate((slideIndex) => {
    function presentationSlides() {
      const sectionSlides = Array.from(document.querySelectorAll('section.slide'));
      if (sectionSlides.length) return sectionSlides;
      return Array.from(document.querySelectorAll('.slide'))
        .filter((slide) => !slide.classList.contains('slide-background') && !slide.closest('.backgrounds'));
    }

    const deck = document.getElementById('deck');
    const slides = presentationSlides();
    window.scrollTo(0, 0);
    if (deck) {
      deck.style.transition = 'none';
      deck.style.transform = `translateX(${-slideIndex * 100}vw)`;
    }
    const usesActiveClass =
      slides.some((slide) => slide.classList.contains('active')) ||
      slides.some((slide) => slide.classList.contains('present')) ||
      slides.some((slide) => getComputedStyle(slide).display === 'none');
    slides.forEach((slide, index) => {
      slide.style.transition = 'none';
      if (usesActiveClass) {
        const selected = index === slideIndex;
        slide.classList.toggle('active', selected);
        slide.classList.toggle('present', selected);
        if (selected) {
          slide.classList.remove('past', 'future');
        }
      }
      slide.style.opacity = index === slideIndex ? '1' : slide.style.opacity;
    });
  }, index);
  await page.waitForTimeout(100);
}

async function prepareSlideElementScreenshot(page, index, width, height) {
  return await page.evaluate(({ slideIndex, viewportWidth, viewportHeight }) => {
    function presentationSlides() {
      const sectionSlides = Array.from(document.querySelectorAll('section.slide'));
      if (sectionSlides.length) return sectionSlides;
      return Array.from(document.querySelectorAll('.slide'))
        .filter((candidate) => !candidate.classList.contains('slide-background') && !candidate.closest('.backgrounds'));
    }

    if (window.__htmlPngRestoreSlide) {
      window.__htmlPngRestoreSlide();
      window.__htmlPngRestoreSlide = null;
    }

    const slides = presentationSlides();
    const deck = document.getElementById('deck');
    const slide = slides[slideIndex];
    if (!slide) return 'missing';

    const previous = {
      deckStyle: deck ? deck.getAttribute('style') : null,
      slideStates: slides.map((candidate) => ({
        className: candidate.className,
        style: candidate.getAttribute('style'),
      })),
    };

    if (deck) {
      deck.style.transition = 'none';
      deck.style.transform = 'none';
      deck.style.width = `${viewportWidth}px`;
      deck.style.height = `${viewportHeight}px`;
      deck.style.position = 'fixed';
      deck.style.inset = '0';
      deck.style.overflow = 'hidden';
      deck.style.display = 'block';
    }

    slides.forEach((candidate, index) => {
      const selected = index === slideIndex;
      candidate.style.transition = 'none';
      candidate.classList.toggle('active', selected);
      candidate.classList.toggle('present', selected);
      if (selected) {
        const computedDisplay = getComputedStyle(candidate).display;
        candidate.classList.remove('past', 'future');
        if (computedDisplay === 'none') candidate.style.display = 'block';
        candidate.style.position = 'absolute';
        candidate.style.visibility = 'visible';
        candidate.style.opacity = '1';
        candidate.style.transform = 'none';
        candidate.style.left = '0px';
        candidate.style.top = '0px';
        candidate.style.margin = '0';
        candidate.style.flex = '0 0 auto';
        candidate.style.width = `${viewportWidth}px`;
        candidate.style.height = `${viewportHeight}px`;
        candidate.style.minWidth = `${viewportWidth}px`;
        candidate.style.minHeight = `${viewportHeight}px`;
        candidate.style.maxWidth = `${viewportWidth}px`;
        candidate.style.maxHeight = `${viewportHeight}px`;
        candidate.style.boxSizing = 'border-box';
      } else {
        candidate.style.display = 'none';
      }
    });

    window.__htmlPngRestoreSlide = () => {
      if (deck) {
        if (previous.deckStyle === null) deck.removeAttribute('style');
        else deck.setAttribute('style', previous.deckStyle);
      }
      slides.forEach((candidate, index) => {
        candidate.className = previous.slideStates[index].className;
        const previousStyle = previous.slideStates[index].style;
        if (previousStyle === null) candidate.removeAttribute('style');
        else candidate.setAttribute('style', previousStyle);
      });
    };

    return deck ? 'viewport' : 'element';
  }, { slideIndex: index, viewportWidth: width, viewportHeight: height });
}

async function getPresentationSlideHandles(page) {
  const sectionHandles = await page.$$('section.slide');
  if (sectionHandles.length) return sectionHandles;
  return page.$$('.slide:not(.slide-background)');
}

async function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const inputHtml = path.resolve(args.input);
    const outputDir = path.resolve(args.outputDir);
    const chartSpecs = await collectChartSpecs(inputHtml);

    await fs.mkdir(outputDir, { recursive: true });
    const entries = await fs.readdir(outputDir).catch(() => []);
    await Promise.all(
      entries
        .filter((entry) => entry.toLowerCase().endsWith('.png'))
        .map((entry) => fs.unlink(path.join(outputDir, entry))),
    );

    const browserPath = await findBrowserExecutable();
    const launchOptions = {
      headless: true,
      timeout: args.timeout,
      args: ['--allow-file-access-from-files'],
    };
    if (browserPath) launchOptions.executablePath = browserPath;

    const browser = await chromium.launch(launchOptions);
    try {
      const page = await browser.newPage({
        viewport: { width: args.width, height: args.height },
        deviceScaleFactor: args.scale,
      });
      page.setDefaultTimeout(args.timeout);

      await preparePage(page, inputHtml, chartSpecs, args.timeout);
      const slideIndexes = await getSlideIndexes(page, args.slide);

      let rendered = 0;
      for (const index of slideIndexes) {
        await showSlide(page, index);
        const pngPath = path.join(outputDir, `slide_${String(index + 1).padStart(2, '0')}.png`);
        const screenshotMode = await prepareSlideElementScreenshot(page, index, args.width, args.height);
        await page.waitForTimeout(50);
        if (screenshotMode === 'viewport') {
          await page.screenshot({ path: pngPath, fullPage: false, omitBackground: false });
        } else {
          const slideHandles = await getPresentationSlideHandles(page);
          const slideHandle = slideHandles[index] || await page.$('body');
          const box = await slideHandle.boundingBox();
          if (box && box.width > 0 && box.height > 0) {
            try {
              await slideHandle.screenshot({ path: pngPath, omitBackground: false });
            } catch (error) {
              console.warn(`Warning: element screenshot failed on slide ${index + 1}; using page clip fallback (${error.message})`);
              await page.screenshot({
                path: pngPath,
                clip: {
                  x: Math.max(0, box.x),
                  y: Math.max(0, box.y),
                  width: Math.max(1, box.width),
                  height: Math.max(1, box.height),
                },
                omitBackground: false,
              });
            }
          } else {
            await page.screenshot({ path: pngPath, fullPage: false, omitBackground: false });
          }
        }
        await page.evaluate(() => {
          if (window.__htmlPngRestoreSlide) {
            window.__htmlPngRestoreSlide();
            window.__htmlPngRestoreSlide = null;
          }
        });
        rendered += 1;
        console.log(`-> ${path.relative(process.cwd(), pngPath)}`);
      }
      console.log(`Done! Rendered ${rendered} browser PNG(s).`);
    } finally {
      await browser.close();
    }
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

await main();
