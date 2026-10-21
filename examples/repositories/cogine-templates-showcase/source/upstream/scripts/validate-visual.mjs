import { mkdtemp, readFile, readdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { spawn, execFileSync } from 'node:child_process';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

const VIEWPORT = {
  width: 1280,
  height: 720
};
const MIN_BROWSER_MAJOR = 112;
const HEADLESS_MODE_FLAG = '--headless=new';

const CHROME_CANDIDATES = process.platform === 'darwin'
  ? [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
    ]
  : process.platform === 'win32'
    ? [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe'
      ]
    : [
        'google-chrome',
        'google-chrome-stable',
        'chromium',
        'chromium-browser',
        'microsoft-edge',
        'microsoft-edge-stable'
      ];

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function pathExists(filePath) {
  try {
    await readFile(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readJson(filePath) {
  const source = await readFile(filePath, 'utf8');
  try {
    return JSON.parse(source);
  } catch (error) {
    throw new Error(`Invalid JSON in ${filePath}: ${error.message}`, { cause: error });
  }
}

function usage() {
  return `Usage:
  node scripts/validate-visual.mjs
  node scripts/validate-visual.mjs --template airy-modern
  node scripts/validate-visual.mjs --template airy-modern --template b2b-sales-pitch

Options:
  --template <slug>   Validate one template. Can be repeated. Defaults to all templates.
  --root <path>       Repository root. Defaults to the current directory.
  --browser <path>    Chrome/Chromium-compatible executable. Also accepts CHROME_BIN.
  --help              Show this message.`;
}

function parseArgs(argv) {
  const options = {
    rootDir: process.cwd(),
    templates: [],
    browserPath: process.env.CHROME_BIN || process.env.CHROMIUM_BIN || ''
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === '--help' || arg === '-h') {
      options.help = true;
      continue;
    }

    if (arg === '--all') {
      options.templates = [];
      continue;
    }

    if (arg === '--template') {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) {
        throw new Error('--template requires a slug');
      }
      options.templates.push(value);
      index += 1;
      continue;
    }

    if (arg.startsWith('--template=')) {
      options.templates.push(arg.slice('--template='.length));
      continue;
    }

    if (arg === '--root') {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) {
        throw new Error('--root requires a path');
      }
      options.rootDir = path.resolve(value);
      index += 1;
      continue;
    }

    if (arg.startsWith('--root=')) {
      options.rootDir = path.resolve(arg.slice('--root='.length));
      continue;
    }

    if (arg === '--browser') {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) {
        throw new Error('--browser requires a path');
      }
      options.browserPath = value;
      index += 1;
      continue;
    }

    if (arg.startsWith('--browser=')) {
      options.browserPath = arg.slice('--browser='.length);
      continue;
    }

    throw new Error(`Unknown option: ${arg}`);
  }

  return options;
}

function findBrowserExecutable(explicitPath = '') {
  if (explicitPath) {
    if (existsSync(explicitPath)) {
      return explicitPath;
    }
    throw new Error(`Browser executable not found: ${explicitPath}`);
  }

  for (const candidate of CHROME_CANDIDATES) {
    if (path.isAbsolute(candidate) && existsSync(candidate)) {
      return candidate;
    }

    if (!path.isAbsolute(candidate)) {
      try {
        return execFileSync('which', [candidate], {
          encoding: 'utf8',
          stdio: ['ignore', 'pipe', 'ignore']
        }).trim();
      } catch {
        // Try the next candidate.
      }
    }
  }

  throw new Error('No Chrome/Chromium-compatible browser found. Install Chrome/Chromium or set CHROME_BIN.');
}

function assertRuntimeSupport() {
  if (typeof WebSocket !== 'function') {
    throw new Error('Visual validation requires a Node.js runtime with global WebSocket support. Use Node.js 22 or newer.');
  }
}

function browserVersion(browserPath) {
  try {
    return execFileSync(browserPath, ['--version'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
      timeout: 3000
    }).trim();
  } catch {
    return '';
  }
}

function assertBrowserSupportsHeadlessNew(browserPath) {
  const version = browserVersion(browserPath);
  const match = version.match(/\b(\d+)\./);
  if (!match) return;

  const major = Number(match[1]);
  if (major >= MIN_BROWSER_MAJOR) return;

  throw new Error(`Visual validation requires Chrome/Chromium ${MIN_BROWSER_MAJOR}+ for ${HEADLESS_MODE_FLAG}. Found ${version}. Upgrade the browser or pass a newer executable with --browser or CHROME_BIN.`);
}

async function getFreePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.unref();
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      server.close(() => resolve(address.port));
    });
  });
}

async function fetchJson(url, init) {
  const response = await fetch(url, init);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText} from ${url}`);
  }
  try {
    return await response.json();
  } catch (error) {
    throw new Error(`Failed to parse JSON from ${url}: ${response.status} ${response.statusText} - ${error.message}`, { cause: error });
  }
}

async function waitForBrowser(port, timeoutMs = 8000) {
  const start = Date.now();
  let lastError;

  while (Date.now() - start < timeoutMs) {
    try {
      return await fetchJson(`http://127.0.0.1:${port}/json/version`);
    } catch (error) {
      lastError = error;
      await sleep(100);
    }
  }

  throw new Error(`Browser did not start DevTools in time (${lastError?.message || 'timeout'})`);
}

async function createTarget(port) {
  const url = `http://127.0.0.1:${port}/json/new?${encodeURIComponent('about:blank')}`;
  let response = await fetch(url, { method: 'PUT' });

  if (!response.ok && response.status === 405) {
    response = await fetch(url);
  }

  if (!response.ok) {
    throw new Error(`Unable to create browser target: ${response.status} ${response.statusText}`);
  }

  const target = await response.json();
  if (!target.webSocketDebuggerUrl) {
    throw new Error('Browser target did not expose a DevTools websocket URL');
  }
  return target;
}

class CdpPage {
  constructor(wsUrl) {
    this.nextId = 1;
    this.pending = new Map();
    this.handlers = new Map();
    this.ws = new WebSocket(wsUrl);
  }

  async connect() {
    await new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });

    this.ws.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);

      if (message.id) {
        const pending = this.pending.get(message.id);
        if (!pending) return;

        this.pending.delete(message.id);
        if (message.error) {
          pending.reject(new Error(`${message.error.message}${message.error.data ? `: ${message.error.data}` : ''}`));
        } else {
          pending.resolve(message.result || {});
        }
        return;
      }

      const handlers = this.handlers.get(message.method);
      if (!handlers) return;
      for (const handler of handlers) {
        handler(message.params || {});
      }
    });
  }

  on(method, handler) {
    const handlers = this.handlers.get(method) || [];
    handlers.push(handler);
    this.handlers.set(method, handlers);
  }

  once(method, timeoutMs = 5000) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        const handlers = this.handlers.get(method) || [];
        this.handlers.set(method, handlers.filter((handler) => handler !== wrapped));
        reject(new Error(`Timed out waiting for ${method}`));
      }, timeoutMs);

      const wrapped = (params) => {
        clearTimeout(timer);
        const handlers = this.handlers.get(method) || [];
        this.handlers.set(method, handlers.filter((handler) => handler !== wrapped));
        resolve(params);
      };

      this.on(method, wrapped);
    });
  }

  send(method, params = {}) {
    const id = this.nextId;
    this.nextId += 1;

    const payload = JSON.stringify({
      id,
      method,
      params
    });

    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(payload);
    });
  }

  close() {
    this.ws.close();
  }
}

async function evaluate(page, expression) {
  const result = await page.send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
    userGesture: true
  });

  if (result.exceptionDetails) {
    throw new Error(formatException(result.exceptionDetails));
  }

  return result.result.value;
}

function formatRemoteValue(value) {
  if (!value) return '';
  if ('value' in value) return String(value.value);
  if ('description' in value) return value.description;
  return value.type || '';
}

function formatException(details) {
  const text = details.exception?.description || details.text || 'unknown exception';
  const location = details.url ? ` at ${details.url}:${details.lineNumber + 1}:${details.columnNumber + 1}` : '';
  return `${text}${location}`;
}

async function launchBrowser(browserPath) {
  const port = await getFreePort();
  const userDataDir = await mkdtemp(path.join(os.tmpdir(), 'slide-template-visual-'));
  const browser = spawn(browserPath, [
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    HEADLESS_MODE_FLAG,
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-background-networking',
    '--no-first-run',
    '--no-default-browser-check',
    '--allow-file-access-from-files',
    'about:blank'
  ], {
    stdio: ['ignore', 'ignore', 'pipe']
  });

  let stderr = '';
  browser.stderr.on('data', (chunk) => {
    stderr += chunk.toString();
  });
  const exited = new Promise((resolve) => {
    browser.once('exit', resolve);
  });

  async function removeUserDataDir() {
    for (let attempt = 0; attempt < 5; attempt += 1) {
      try {
        await rm(userDataDir, { recursive: true, force: true });
        return;
      } catch (error) {
        if (attempt === 4) throw error;
        await sleep(150);
      }
    }
  }

  try {
    await waitForBrowser(port);
  } catch (error) {
    browser.kill('SIGTERM');
    await Promise.race([exited, sleep(2000)]);
    await removeUserDataDir();
    throw new Error(`${error.message}${stderr ? `\n${stderr.trim()}` : ''}`);
  }

  return {
    port,
    async close() {
      if (browser.exitCode === null && browser.signalCode === null) {
        browser.kill('SIGTERM');
      }
      await Promise.race([exited, sleep(2000)]);
      await removeUserDataDir();
    }
  };
}

async function loadTemplate(page, htmlPath) {
  const loadEvent = page.once('Page.loadEventFired', 10000).catch(() => null);
  await page.send('Page.navigate', {
    url: pathToFileURL(htmlPath).href
  });
  await loadEvent;
  await evaluate(page, `new Promise((resolve) => {
    const ready = () => {
      const fontsReady = document.fonts?.ready?.catch(() => null) || Promise.resolve();
      Promise.race([fontsReady, new Promise((fontResolve) => setTimeout(fontResolve, 2000))])
        .then(() => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    };

    if (document.readyState === 'complete') ready();
    else window.addEventListener('load', ready, { once: true });
  })`);
}

async function preparePage(port) {
  const target = await createTarget(port);
  const page = new CdpPage(target.webSocketDebuggerUrl);
  await page.connect();
  await page.send('Page.enable');
  await page.send('Runtime.enable');
  await page.send('Log.enable');
  await page.send('Emulation.setDeviceMetricsOverride', {
    width: VIEWPORT.width,
    height: VIEWPORT.height,
    screenWidth: VIEWPORT.width,
    screenHeight: VIEWPORT.height,
    deviceScaleFactor: 1,
    mobile: false
  });

  return page;
}

function navigationCheckExpression(features) {
  return `(${async function runNavigationChecks(features) {
    const wait = (ms = 140) => new Promise((resolve) => setTimeout(resolve, ms));
    const slides = [...document.querySelectorAll('.slide')];
    const errors = [];

    function activeIndex() {
      return slides.findIndex((slide) => slide.classList.contains('active'));
    }

    async function resetToFirst() {
      const index = activeIndex();
      if (index > 0 && typeof window.changeSlide === 'function') {
        window.changeSlide(-index);
      } else {
        slides.forEach((slide, slideIndex) => {
          slide.classList.toggle('active', slideIndex === 0);
          slide.classList.remove('prev');
        });
      }
      await wait();
    }

    async function advanceWithClickOrFunction() {
      const button = document.querySelector('#nextBtn') ||
        [...document.querySelectorAll('button')].find((candidate) => /next/i.test(`${candidate.getAttribute('aria-label') || ''} ${candidate.textContent || ''}`)) ||
        document.querySelector('.nav-controls button:last-child');

      if (button) {
        button.click();
      } else if (typeof window.changeSlide === 'function') {
        window.changeSlide(1);
      } else {
        return false;
      }

      await wait();
      return true;
    }

    async function advanceWithKeyboard() {
      document.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'ArrowRight',
        code: 'ArrowRight',
        bubbles: true,
        cancelable: true
      }));
      await wait();
    }

    function progressWidth() {
      const progress = document.querySelector('#progress, .progress-bar');
      return progress ? progress.getBoundingClientRect().width : null;
    }

    function counterText() {
      const counter = document.querySelector('#current, .slide-counter');
      return counter ? counter.textContent.replace(/\s+/g, ' ').trim() : '';
    }

    if (slides.length < 2) {
      return errors;
    }

    if (features.navigation) {
      await resetToFirst();
      const before = activeIndex();
      const attempted = await advanceWithClickOrFunction();
      const after = activeIndex();

      if (!attempted) {
        errors.push('declares navigation but no next button or changeSlide function was found');
      } else if (!(after > before)) {
        errors.push(`declares navigation but next control did not advance the active slide (${before} -> ${after})`);
      }
    }

    if (features.keyboard_navigation) {
      await resetToFirst();
      const before = activeIndex();
      await advanceWithKeyboard();
      const after = activeIndex();

      if (!(after > before)) {
        errors.push(`declares keyboard_navigation but ArrowRight did not advance the active slide (${before} -> ${after})`);
      }
    }

    if (features.progress_bar) {
      await resetToFirst();
      const before = progressWidth();
      await advanceWithClickOrFunction();
      const after = progressWidth();

      if (before === null) {
        errors.push('declares progress_bar but no #progress or .progress-bar element was found');
      } else if (!(after > before)) {
        errors.push(`declares progress_bar but progress width did not increase (${before} -> ${after})`);
      }
    }

    if (features.slide_counter) {
      await resetToFirst();
      await advanceWithClickOrFunction();
      const text = counterText();

      if (!text) {
        errors.push('declares slide_counter but no #current or .slide-counter element was found');
      } else if (!/\b2\b/.test(text)) {
        errors.push(`declares slide_counter but counter did not show slide 2 after navigation ("${text}")`);
      }
    }

    return errors;
  }})(${JSON.stringify(features)})`;
}

function overflowCheckExpression() {
  return `(${function runOverflowCheck() {
    const tolerance = 4;
    const slides = [...document.querySelectorAll('.slide')];
    const errors = [];
    const original = slides.map((slide) => ({
      active: slide.classList.contains('active'),
      prev: slide.classList.contains('prev'),
      transition: slide.style.transition
    }));

    function isVisible(element) {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== 'none' &&
        style.visibility !== 'hidden' &&
        Number(style.opacity) !== 0 &&
        rect.width > 0 &&
        rect.height > 0;
    }

    function labelFor(element) {
      const text = element.textContent.replace(/\s+/g, ' ').trim();
      const readableText = text ? ` "${text.slice(0, 48)}${text.length > 48 ? '...' : ''}"` : '';
      const id = element.id ? `#${element.id}` : '';
      const className = typeof element.className === 'string' && element.className.trim()
        ? `.${element.className.trim().split(/\s+/).join('.')}`
        : '';
      return `${element.tagName.toLowerCase()}${id}${className}${readableText}`;
    }

    function outOfBounds(rect, container) {
      const left = container.left - rect.left;
      const right = rect.right - container.right;
      const top = container.top - rect.top;
      const bottom = rect.bottom - container.bottom;
      const overflow = Math.max(left, right, top, bottom);
      return overflow > tolerance ? Math.round(overflow) : 0;
    }

    for (const [index, slide] of slides.entries()) {
      slides.forEach((candidate, candidateIndex) => {
        candidate.style.transition = 'none';
        candidate.classList.toggle('active', candidateIndex === index);
        candidate.classList.remove('prev');
      });

      const slideRect = slide.getBoundingClientRect();
      const candidates = [...slide.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,blockquote,figcaption,td,th,pre,code,small,strong,b,span')];
      for (const element of candidates) {
        if (!element.textContent.trim() || !isVisible(element)) {
          continue;
        }

        const overflow = outOfBounds(element.getBoundingClientRect(), slideRect);
        if (overflow) {
          errors.push(`slide ${index + 1}: ${labelFor(element)} extends ${overflow}px outside the slide`);
        }
      }
    }

    slides.forEach((slide, index) => {
      slide.style.transition = original[index].transition;
      slide.classList.toggle('active', original[index].active);
      slide.classList.toggle('prev', original[index].prev);
    });

    return errors;
  }})()`;
}

async function validateTemplate(browser, template) {
  const errors = [];
  const consoleErrors = [];
  const page = await preparePage(browser.port);

  page.on('Runtime.consoleAPICalled', (event) => {
    if (event.type !== 'error') return;
    consoleErrors.push(`console.error: ${(event.args || []).map(formatRemoteValue).join(' ')}`);
  });

  page.on('Runtime.exceptionThrown', (event) => {
    consoleErrors.push(`uncaught exception: ${formatException(event.exceptionDetails)}`);
  });

  page.on('Log.entryAdded', (event) => {
    const entry = event.entry;
    if (entry?.level === 'error' && entry.source !== 'network') {
      consoleErrors.push(`${entry.source || 'log'} error: ${entry.text}`);
    }
  });

  try {
    await loadTemplate(page, template.htmlPath);

    const slideCount = await evaluate(page, `document.querySelectorAll('.slide').length`);
    if (slideCount !== template.metadata.slide_count) {
      errors.push(`rendered ${slideCount} .slide element(s), but template.json declares ${template.metadata.slide_count}`);
    }

    const overflowErrors = await evaluate(page, overflowCheckExpression());
    const navigationErrors = await evaluate(page, navigationCheckExpression(template.metadata.features || {}));
    errors.push(...consoleErrors, ...overflowErrors, ...navigationErrors);
  } catch (error) {
    errors.push(`browser validation failed: ${error.message}`);
  } finally {
    page.close();
  }

  return {
    slug: template.slug,
    ok: errors.length === 0,
    errors
  };
}

async function collectTemplates(rootDir, requestedSlugs) {
  const templatesDir = path.join(rootDir, 'templates');
  const entries = await readdir(templatesDir, { withFileTypes: true });
  const dirs = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
  const requested = new Set(requestedSlugs);
  const missing = requestedSlugs.filter((slug) => !dirs.includes(slug));

  if (missing.length > 0) {
    throw new Error(`Unknown template slug(s): ${missing.join(', ')}`);
  }

  const selectedDirs = requested.size > 0 ? dirs.filter((dir) => requested.has(dir)) : dirs;
  const templates = [];

  for (const slug of selectedDirs) {
    const templateDir = path.join(templatesDir, slug);
    const htmlPath = path.join(templateDir, 'template.html');
    const jsonPath = path.join(templateDir, 'template.json');

    if (!(await pathExists(htmlPath))) {
      throw new Error(`${slug}: missing template.html`);
    }

    if (!(await pathExists(jsonPath))) {
      throw new Error(`${slug}: missing template.json`);
    }

    templates.push({
      slug,
      htmlPath,
      metadata: await readJson(jsonPath)
    });
  }

  return templates;
}

export async function validateVisual(options = {}) {
  assertRuntimeSupport();
  const rootDir = path.resolve(options.rootDir || process.cwd());
  const browserPath = findBrowserExecutable(options.browserPath || '');
  assertBrowserSupportsHeadlessNew(browserPath);
  const templates = await collectTemplates(rootDir, options.templates || []);
  const browser = await launchBrowser(browserPath);

  try {
    const results = [];
    for (const template of templates) {
      results.push(await validateTemplate(browser, template));
    }
    return {
      viewport: VIEWPORT,
      browserPath,
      results,
      ok: results.every((result) => result.ok)
    };
  } finally {
    await browser.close();
  }
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    console.error(usage());
    process.exitCode = 1;
    return;
  }

  if (options.help) {
    console.log(usage());
    return;
  }

  try {
    const result = await validateVisual(options);
    const count = result.results.length;

    if (result.ok) {
      console.log(`Visual validation passed for ${count} template(s) at ${result.viewport.width}x${result.viewport.height}.`);
      for (const template of result.results) {
        console.log(`- ${template.slug}`);
      }
      return;
    }

    console.error(`Visual validation failed for ${count} template(s):`);
    for (const template of result.results) {
      if (template.ok) {
        console.error(`- ${template.slug}: ok`);
        continue;
      }

      console.error(`- ${template.slug}:`);
      for (const error of template.errors) {
        console.error(`  - ${error}`);
      }
    }
    process.exitCode = 1;
  } catch (error) {
    console.error(`Visual validation failed: ${error.message}`);
    process.exitCode = 1;
  }
}

const isCli = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isCli) {
  await main();
}
