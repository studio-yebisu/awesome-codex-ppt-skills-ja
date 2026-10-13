#!/usr/bin/env node
/**
 * browser_svg_to_pdf.mjs - Combine per-slide SVG files into a vector PDF.
 *
 * Usage:
 *   node browser_svg_to_pdf.mjs output/svgs -o output/slides.pdf
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 720;

function parseArgs(argv) {
  const args = {
    input: null,
    output: null,
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
    timeout: 120_000,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '-o' || arg === '--output') {
      args.output = argv[++i];
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

  if (!args.input) throw new Error('Missing SVG input directory.');
  if (!args.output) throw new Error('Missing output path. Use -o <path>.');
  if (!Number.isFinite(args.width) || args.width <= 0) {
    throw new Error('--width must be a positive integer.');
  }
  if (!Number.isFinite(args.height) || args.height <= 0) {
    throw new Error('--height must be a positive integer.');
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node browser_svg_to_pdf.mjs <svg_dir> -o <output.pdf>

Options:
  -o, --output <path>  Output PDF path
  --width <px>         Slide width (default: ${DEFAULT_WIDTH})
  --height <px>        Slide height (default: ${DEFAULT_HEIGHT})
  --timeout <ms>       Browser operation timeout (default: 120000)
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

async function listSvgFiles(inputPath) {
  const stat = await fs.stat(inputPath);
  if (!stat.isDirectory()) {
    throw new Error(`SVG input must be a directory: ${inputPath}`);
  }
  const entries = await fs.readdir(inputPath);
  return entries
    .filter((entry) => (
        entry.toLowerCase().endsWith('.svg') && !entry.startsWith('.')
    ))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
    .map((entry) => path.join(inputPath, entry));
}

async function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const inputPath = path.resolve(args.input);
    const outputPath = path.resolve(args.output);
    const svgFiles = await listSvgFiles(inputPath);
    if (!svgFiles.length) throw new Error(`No SVG files found: ${inputPath}`);

    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    const svgContents = await Promise.all(
      svgFiles.map((svgPath) => fs.readFile(svgPath, 'utf8')),
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
      });
      page.setDefaultTimeout(args.timeout);

      const pages = svgContents
        .map((svg) => `<div class="pdf-page">${svg}</div>`)
        .join('');
      const html = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page { size: ${args.width}px ${args.height}px; margin: 0; }
  html, body { margin: 0; padding: 0; background: white; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .pdf-page {
    width: ${args.width}px;
    height: ${args.height}px;
    overflow: hidden;
  }
  .pdf-page:not(:last-child) { break-after: page; page-break-after: always; }
  .pdf-page > svg {
    display: block;
    width: ${args.width}px;
    height: ${args.height}px;
  }
</style>
</head>
<body>${pages}</body>
</html>`;

      await page.setContent(html, { waitUntil: 'load', timeout: args.timeout });
      await page.evaluate(() => document.fonts.ready);
      await page.pdf({
        path: outputPath,
        printBackground: true,
        preferCSSPageSize: true,
        margin: { top: '0', right: '0', bottom: '0', left: '0' },
        timeout: args.timeout,
      });
      console.log(`-> ${path.relative(process.cwd(), outputPath)}`);
      console.log(`Done! Combined ${svgFiles.length} SVG(s) into one PDF.`);
    } finally {
      await browser.close();
    }
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

await main();
