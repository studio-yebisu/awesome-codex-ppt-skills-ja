#!/usr/bin/env node
/**
 * browser_svg_to_png.mjs - Render SVG files to PNG using Chromium.
 *
 * Usage:
 *   node browser_svg_to_png.mjs output/svgs -o output/pngs
 *   node browser_svg_to_png.mjs output/svgs/slide_08.svg -o output/pngs
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 720;

function parseArgs(argv) {
  const args = {
    input: null,
    output: null,
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
    scale: 2,
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

  if (!args.input) throw new Error('Missing SVG input path.');
  if (!args.output) throw new Error('Missing output path. Use -o <path>.');
  if (!Number.isFinite(args.scale) || args.scale <= 0) {
    throw new Error('--scale must be a positive number.');
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node browser_svg_to_png.mjs <svg_file_or_dir> -o <output_file_or_dir>

Options:
  -o, --output <path>  Output PNG path or directory
  --width <px>         Viewport width (default: ${DEFAULT_WIDTH})
  --height <px>        Viewport height (default: ${DEFAULT_HEIGHT})
  --scale <n>          Device scale factor (default: 2)
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
  if (stat.isDirectory()) {
    const entries = await fs.readdir(inputPath);
    return entries
      .filter((entry) => (
        entry.toLowerCase().endsWith('.svg') && !entry.startsWith('.')
      ))
      .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
      .map((entry) => path.join(inputPath, entry));
  }
  return [inputPath];
}

async function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const inputPath = path.resolve(args.input);
    const outputPath = path.resolve(args.output);
    const svgFiles = await listSvgFiles(inputPath);
    if (!svgFiles.length) throw new Error(`No SVG files found: ${inputPath}`);

    const inputStat = await fs.stat(inputPath);
    const outputIsDir = inputStat.isDirectory() || svgFiles.length > 1 || path.extname(outputPath).toLowerCase() !== '.png';
    if (outputIsDir) await fs.mkdir(outputPath, { recursive: true });
    else await fs.mkdir(path.dirname(outputPath), { recursive: true });

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

      let rendered = 0;
      for (const svgFile of svgFiles) {
        const pngPath = outputIsDir
          ? path.join(outputPath, `${path.basename(svgFile, path.extname(svgFile))}.png`)
          : outputPath;
        await page.goto(pathToFileURL(svgFile).href, {
          waitUntil: 'load',
          timeout: args.timeout,
        });
        const svgHandle = await page.$('svg');
        if (svgHandle) {
          await svgHandle.screenshot({ path: pngPath, omitBackground: false });
        } else {
          await page.screenshot({ path: pngPath, omitBackground: false });
        }
        rendered += 1;
        console.log(`-> ${path.relative(process.cwd(), pngPath)}`);
      }
      console.log(`Done! Rendered ${rendered} PNG(s).`);
    } finally {
      await browser.close();
    }
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

await main();
