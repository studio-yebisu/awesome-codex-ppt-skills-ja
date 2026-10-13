#!/usr/bin/env node
/**
 * Browser smoke for one deck: boot errors, then every stop via `__deck.seek(t)`.
 *   node tools/smoke.mjs <deckId> [--port 5190] [--host localhost] [--shots] [--driver aside|chrome] [--out dir]
 * Writes out/smoke/<deck>/report.json (+ stop-XX.png and sheet.png with --shots); --out writes elsewhere.
 * The chrome tab ignores Vite HMR reloads, so other agents' edits during a run do not wipe the probe.
 * Drivers: `aside` = Aside CLI repl (default, current viewport). `chrome` = hyperframes'
 * chrome-headless-shell over raw CDP at 1920×1080; `--shots` uses it because Aside
 * screenshots time out on background tabs.
 */
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ASIDE = '/mnt/c/Users/kim/AppData/Local/Aside/CLI/current/aside.exe';
const DECK_ID = /^_?[a-z0-9][a-z0-9-]*$/;
export const usage =
  'node tools/smoke.mjs <deckId> [--port 5190] [--host localhost] [--shots] [--driver aside|chrome] [--out dir]';
export const SHEET_COLUMNS = 6;
/** How long the probe waits for the page's own boot (vite module loading under load took 20–48 s). */
export const BOOT_WAIT_MS = 60000;
/** Per-stop bound for visible <video>/<img>/frame-sequence canvases to paint before measuring. */
export const MEDIA_WAIT_MS = 20000;

/** @param {string[]} argv */
export function parseArgs(argv) {
  const opts = { deck: null, port: 5190, host: 'localhost', shots: false, driver: null, out: null, help: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') opts.help = true;
    else if (arg === '--shots') opts.shots = true;
    else if (arg === '--port') opts.port = Number(argv[(i += 1)]);
    else if (arg === '--host') opts.host = argv[(i += 1)];
    else if (arg === '--driver') opts.driver = argv[(i += 1)];
    else if (arg === '--out') opts.out = argv[(i += 1)];
    else if (arg.startsWith('--')) throw new Error(`unknown option: ${arg}`);
    else if (!opts.deck) opts.deck = arg;
    else throw new Error(`unexpected argument: ${arg}`);
  }
  if (opts.help) return opts;
  if (!opts.deck) throw new Error(usage);
  if (!DECK_ID.test(opts.deck)) throw new Error(`invalid deck id: ${opts.deck}`);
  if (!Number.isInteger(opts.port) || opts.port <= 0) throw new Error('--port must be a positive integer');
  opts.driver ??= opts.shots ? 'chrome' : 'aside';
  if (!['aside', 'chrome'].includes(opts.driver)) throw new Error(`unknown driver: ${opts.driver}`);
  if (opts.shots && opts.driver !== 'chrome') throw new Error('--shots needs --driver chrome');
  return opts;
}

export const shotName = (index) => `stop-${String(index + 1).padStart(2, '0')}.png`;

/** Summary counts over the per-stop probe results. */
export function summarize(report) {
  const stops = report.stops ?? [];
  return {
    stops: stops.length,
    errors: (report.bootError ? 1 : 0) + stops.reduce((n, s) => n + s.errors.length, 0) + (report.pageErrors?.length ?? 0),
    empty: stops.filter((s) => s.visibleBeats.length === 0).map((s) => s.name),
    overlaps: stops.reduce((n, s) => n + s.overlaps.length, 0),
    clipped: stops.reduce((n, s) => n + s.clipped.length, 0),
    tinyText: stops.filter((s) => s.minFont !== null && s.minFont < 14).map((s) => s.name),
    // 대기 한도 안에 그려지지 않은 media가 있는 정지점: 그 shot의 빈 칸은 덱 문제가 아닐 수 있다
    mediaPending: stops.filter((s) => s.mediaPending?.length).map((s) => s.name),
  };
}

/** One line per stop for the terminal. */
export function formatReport(report) {
  const sum = report.summary ?? summarize(report);
  const lines = [`smoke ${report.deck} · ${report.driver} ${report.viewport?.w}×${report.viewport?.h}`];
  if (report.bootError) lines.push(`BOOT ${report.bootError.split('\n')[0]}`);
  for (const s of report.stops ?? []) {
    const flags = [
      s.errors.length && `err ${s.errors.length}`,
      !s.visibleBeats.length && 'EMPTY',
      s.overlaps.length && `overlap ${s.overlaps.length}`,
      s.clipped.length && `clip ${s.clipped.length}`,
      s.mediaPending?.length && `media wait ${s.mediaPending.join(',')}`,
    ].filter(Boolean);
    lines.push(
      `${String(s.index + 1).padStart(2)} ${s.name.padEnd(26)} t=${s.t.toFixed(2).padStart(6)} beats=${s.visibleBeats.join(',')}${flags.length ? `  ${flags.join(' · ')}` : ''}`,
    );
  }
  lines.push(
    `stops ${sum.stops} · errors ${sum.errors} · empty ${sum.empty.length} · overlaps ${sum.overlaps} · clipped ${sum.clipped} · tiny ${sum.tinyText.length}` +
      (sum.mediaPending?.length ? ` · media-pending ${sum.mediaPending.length}` : ''),
  );
  return lines.join('\n');
}

/**
 * In-page probe, installed as `window.__smoke`. Runs as a string in the page, so it
 * must not close over module scope. The dynamic-import spelling dodges the Aside repl filter.
 */
export function probeSource(deckId) {
  return `(() => {
  if (window.__smoke) return;
  const pageErrors = [];
  addEventListener('error', (e) => pageErrors.push(String(e.error?.stack || e.message)));
  addEventListener('unhandledrejection', (e) => pageErrors.push(String(e.reason?.stack || e.reason)));
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const frame = () => new Promise((r) => { const t = setTimeout(r, 120); requestAnimationFrame(() => { clearTimeout(t); r(); }); });
  const DECK = ${JSON.stringify(deckId)};
  const BOOT_WAIT_MS = ${BOOT_WAIT_MS};
  const MEDIA_WAIT_MS = ${MEDIA_WAIT_MS};
  // The page's own main.js boots the deck (with its sequences and layout CSS). If window.__deck is still missing
  // after the wait, import main.js again: a module that failed rethrows its error here, so the report shows it.
  async function retryMain(waitMs) {
    const load = new Function('u', 'return im' + 'port(u)');
    await load(location.origin + '/decks/' + DECK + '/main.js');
    const until = Date.now() + waitMs;
    while (!window.__deck && Date.now() < until) await sleep(150);
  }
  // Visible media must have painted before a stop is measured or shot; on a loaded box a 60 KB image or a
  // frame sequence takes 10–40 s, and the sheet showed false blanks. Returns what was still pending.
  async function mediaSettled(waitMs) {
    const until = Date.now() + waitMs;
    const pending = () => {
      const out = [];
      const shown = (el) => opacityOf(el) > 0.02 && area(meet(clippedRect(el), { l: 0, t: 0, r: innerWidth, b: innerHeight })) > 0;
      for (const v of document.querySelectorAll('video')) if (shown(v) && v.readyState < 2) out.push('video ' + (v.currentSrc || v.src).split('/').pop());
      for (const i of document.querySelectorAll('img')) if (shown(i) && !(i.complete && i.naturalWidth > 0)) out.push('img ' + i.src.split('/').pop());
      for (const c of document.querySelectorAll('canvas.sl-frame-sequence'))
        if (shown(c) && c.dataset.frame !== undefined && c.dataset.drawn !== c.dataset.frame) out.push('frames ' + c.dataset.drawn + '/' + c.dataset.frame);
      return out;
    };
    let now = pending();
    while (now.length && Date.now() < until) {
      await sleep(250);
      now = pending();
    }
    if (now.length === 0) await frame();
    return now;
  }
  function opacityOf(el) {
    let o = 1;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.display === 'none') return 0;
      o *= Number(cs.opacity);
    }
    const cs = getComputedStyle(el);
    return cs.visibility === 'hidden' ? 0 : o;
  }
  function insetClip(cs, r) {
    const m = /^inset\\(([^)]*)\\)/.exec(cs.clipPath || '');
    if (!m) return null;
    const v = m[1].split(/\\s+/).filter((x) => x && !/round/.test(x)).slice(0, 4);
    const [t, ri = t, b = t, l = ri] = v.map((x, i) => x.endsWith('%') ? parseFloat(x) / 100 * (i % 2 ? r.width : r.height) : parseFloat(x) || 0);
    return { l: r.left + l, t: r.top + t, r: r.right - ri, b: r.bottom - b };
  }
  function clippedRect(el) {
    const r0 = el.getBoundingClientRect();
    let r = { l: r0.left, t: r0.top, r: r0.right, b: r0.bottom };
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      const box = n === el ? r0 : n.getBoundingClientRect();
      const cut = [];
      if (n !== el && cs.overflowX !== 'visible') cut.push({ l: box.left, t: -1e9, r: box.right, b: 1e9 });
      if (n !== el && cs.overflowY !== 'visible') cut.push({ l: -1e9, t: box.top, r: 1e9, b: box.bottom });
      const ins = insetClip(cs, box);
      if (ins) cut.push(ins);
      for (const c of cut) r = { l: Math.max(r.l, c.l), t: Math.max(r.t, c.t), r: Math.min(r.r, c.r), b: Math.min(r.b, c.b) };
    }
    return r;
  }
  const area = (r) => Math.max(0, r.r - r.l) * Math.max(0, r.b - r.t);
  const meet = (a, b) => ({ l: Math.max(a.l, b.l), t: Math.max(a.t, b.t), r: Math.min(a.r, b.r), b: Math.min(a.b, b.b) });
  const round = (r) => ({ x: Math.round(r.l), y: Math.round(r.t), w: Math.round(r.r - r.l), h: Math.round(r.b - r.t) });
  const ownText = (el) => Array.from(el.childNodes).filter((n) => n.nodeType === 3).map((n) => n.textContent).join('').trim();
  function measureNow() {
    const vp = { l: 0, t: 0, r: innerWidth, b: innerHeight };
    const beats = Array.from(document.querySelectorAll('.sl-beat[data-beat]'))
      .filter((b) => opacityOf(b) > 0.02 && area(meet(clippedRect(b), vp)) > 0)
      .filter((b) => Array.from(b.querySelectorAll('*')).concat(b).some((n) => {
        if (opacityOf(n) <= 0.02) return false;
        const vis = area(meet(clippedRect(n), vp));
        return vis > 400 && (ownText(n) || /^(IMG|VIDEO|CANVAS|svg|path|rect|line|circle)$/.test(n.tagName) || getComputedStyle(n).backgroundImage !== 'none' || getComputedStyle(n).backgroundColor !== 'rgba(0, 0, 0, 0)');
      }))
      .map((b) => b.dataset.beat);
    const texts = [];
    for (const el of document.body.querySelectorAll('*')) {
      if (/^(SCRIPT|STYLE|NOSCRIPT)$/.test(el.tagName)) continue;
      const text = ownText(el);
      if (!text) continue;
      const op = opacityOf(el);
      if (op <= 0.05) continue;
      const r = clippedRect(el);
      if (area(r) < 4) continue;
      const scale = el.offsetHeight ? el.getBoundingClientRect().height / el.offsetHeight : 1;
      texts.push({ el, text: text.slice(0, 40), r, inView: area(meet(r, vp)), font: parseFloat(getComputedStyle(el).fontSize) * scale, op });
    }
    const shown = texts.filter((t) => t.inView > 0);
    const overlaps = [];
    for (let i = 0; i < shown.length; i += 1)
      for (let j = i + 1; j < shown.length; j += 1) {
        const a = shown[i], b = shown[j];
        if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
        const both = area(meet(a.r, b.r));
        if (both > 64 && both > 0.15 * Math.min(area(a.r), area(b.r)))
          overlaps.push({ a: a.text, b: b.text, area: Math.round(both), ra: round(a.r), rb: round(b.r) });
      }
    const clipped = shown
      .filter((t) => t.inView < area(t.r) * 0.95)
      .map((t) => ({ text: t.text, rect: round(t.r), visible: Math.round(t.inView / area(t.r) * 100) / 100 }));
    const fonts = shown.map((t) => t.font).filter((f) => f > 0);
    return {
      visibleBeats: beats,
      texts: shown.length,
      overlaps,
      clipped,
      // 1920 기준 px로 환산(Aside 창 폭이 달라도 「너무 작은 글자」 기준이 같게)
      minFont: fonts.length ? Math.round((Math.min(...fonts) * 1920) / innerWidth * 10) / 10 : null,
      textSample: shown.slice().sort((a, b) => b.font - a.font).slice(0, 6).map((t) => ({ text: t.text, font: Math.round(t.font), rect: round(t.r), op: Math.round(t.op * 100) / 100 })),
    };
  }
  window.__smoke = {
    pageErrors,
    async boot(waitMs = BOOT_WAIT_MS) {
      const until = Date.now() + waitMs;
      while (!window.__deck && Date.now() < until) await sleep(150);
      if (!window.__deck) {
        try { await retryMain(waitMs / 2); } catch (e) { return { bootError: String(e?.stack || e) }; }
        if (!window.__deck) {
          const last = pageErrors.at(-1);
          return { bootError: 'window.__deck missing after ' + Math.round((waitMs * 1.5) / 1000) + 's' + (last ? ': ' + last : '') };
        }
      }
      await (document.fonts?.ready ?? Promise.resolve());
      await sleep(600);
      return { bootError: null, viewport: { w: innerWidth, h: innerHeight }, stops: window.__deck.stops().map((s) => ({ name: s.name, beat: s.beat, t: s.t })) };
    },
    async at(index) {
      const errors = [];
      const before = pageErrors.length;
      const stop = window.__deck.stops()[index];
      let mediaPending = [];
      try {
        window.__deck.seek(stop.t);
        const until = Date.now() + 2500;
        let last = -1;
        while (Date.now() < until) {
          await frame();
          const y = scrollY;
          if (y === last && Math.abs(window.__deck.time() - stop.t) < 0.03) break;
          last = y;
        }
        window.__deck.tl.seek(stop.t);
        await (document.fonts?.ready ?? Promise.resolve());
        await frame();
        mediaPending = await mediaSettled(MEDIA_WAIT_MS);
      } catch (e) {
        errors.push(String(e?.stack || e));
      }
      errors.push(...pageErrors.slice(before));
      let probe;
      try { probe = measureNow(); } catch (e) { errors.push('probe ' + String(e?.stack || e)); probe = { visibleBeats: [], texts: 0, overlaps: [], clipped: [], minFont: null, textSample: [] }; }
      return { index, name: stop.name, beat: stop.beat, t: stop.t, time: window.__deck.time(), errors, mediaPending, ...probe };
    },
  };
})();`;
}

/**
 * Injected before the page's own scripts: drops Vite HMR `full-reload`/`update`/`prune` messages so a file
 * saved by another agent mid-run does not reload the tab (which wiped `window.__smoke` and failed the run).
 */
export const HMR_FREEZE = `(() => {
  const Native = window.WebSocket;
  if (!Native || Native.__slFrozen) return;
  const drop = (data) => {
    try { return ['full-reload', 'update', 'prune'].includes(JSON.parse(data).type); } catch { return false; }
  };
  class Frozen extends Native {
    constructor(url, protocols) {
      super(url, protocols);
      this.__slHmr = [].concat(protocols ?? []).includes('vite-hmr');
    }
    addEventListener(type, fn, opts) {
      if (!this.__slHmr || type !== 'message' || typeof fn !== 'function') return super.addEventListener(type, fn, opts);
      return super.addEventListener(type, (event) => { if (!drop(event.data)) fn.call(this, event); }, opts);
    }
  }
  Frozen.__slFrozen = true;
  window.WebSocket = Frozen;
})();`;

function deckUrl(opts) {
  if (process.env.SCROLLINE_URL) {
    if (!/^https?:\/\//.test(process.env.SCROLLINE_URL)) throw new Error("SCROLLINE_URL must use HTTP(S)");
    return process.env.SCROLLINE_URL;
  }
  return `http://${opts.host}:${opts.port}/decks/${opts.deck}/index.html`;
}

/** Aside driver: one repl call opens a tab, runs every stop, closes the tab. */
function runAside(opts) {
  if (!existsSync(ASIDE)) throw new Error(`Aside CLI not found: ${ASIDE}`);
  const code = `{ const smokeTab = await openTab(${JSON.stringify(deckUrl(opts))});
try {
  // openTab can return while the tab is still about:blank (origin "null"); wait for the deck URL.
  for (let i = 0; i < 60 && !String(await smokeTab.evaluate(() => location.href).catch(() => '')).startsWith('http'); i += 1) await sleep(250);
  await smokeTab.evaluate(${JSON.stringify(probeSource(opts.deck))});
  const smokeBoot = await smokeTab.evaluate(() => window.__smoke.boot());
  const smokeOut = { ...smokeBoot, stops: [] };
  if (!smokeBoot.bootError) {
    for (let i = 0; i < smokeBoot.stops.length; i += 1) smokeOut.stops.push(await smokeTab.evaluate((n) => window.__smoke.at(n), i));
    smokeOut.pageErrors = await smokeTab.evaluate(() => window.__smoke.pageErrors.slice());
  }
  console.log('@@SMOKE@@' + JSON.stringify(smokeOut));
} finally { try { await closeTab(smokeTab); } catch (e) { try { await smokeTab.evaluate(() => window.close()); } catch {} } } }`;
  const result = spawnSync('timeout', ['170', ASIDE, 'repl', code], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  const out = `${result.stdout ?? ''}${result.stderr ?? ''}`;
  const line = out.split('\n').find((l) => l.startsWith('@@SMOKE@@'));
  if (!line) throw new Error(`aside repl gave no result:\n${out.slice(-2000)}`);
  return JSON.parse(line.slice('@@SMOKE@@'.length));
}

/** Minimal CDP session over Node's WebSocket. */
export async function cdpConnect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = () => reject(new Error(`CDP connect failed: ${wsUrl}`));
  });
  let id = 0;
  const pending = new Map();
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (!msg.id || !pending.has(msg.id)) return;
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(msg.error.message));
    else resolve(msg.result);
  };
  const send = (method, params = {}) =>
    new Promise((resolve, reject) => {
      id += 1;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  const evaluate = async (expression) => {
    const res = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (res.exceptionDetails) throw new Error(res.exceptionDetails.exception?.description ?? res.exceptionDetails.text);
    return res.result.value;
  };
  return { send, evaluate, close: () => ws.close() };
}

export function chromePath() {
  if (process.env.SCROLLINE_CHROME && existsSync(process.env.SCROLLINE_CHROME)) return process.env.SCROLLINE_CHROME;
  // Cached headless shell first: concurrent `npx hyperframes` calls race on the npx cache and print nothing.
  const cache = path.join(os.homedir(), '.cache', 'hyperframes', 'chrome', 'chrome-headless-shell');
  if (existsSync(cache)) {
    const found = readdirSync(cache)
      .sort()
      .reverse()
      .map((v) => path.join(cache, v, 'chrome-headless-shell-linux64', 'chrome-headless-shell'))
      .find((f) => existsSync(f));
    if (found) return found;
  }
  const result = spawnSync('npx', ['hyperframes', 'browser', 'path'], { cwd: ROOT, encoding: 'utf8' });
  const file = result.stdout.trim().split('\n').at(-1);
  if (!file || !existsSync(file)) throw new Error('chrome not found: run `npx hyperframes browser ensure`');
  return file;
}

/** Chrome driver: headless shell, 1920×1080, optional per-stop PNG. */
async function runChrome(opts, outDir) {
  const profile = mkdtempSync(path.join(os.tmpdir(), 'scrolline-smoke-'));
  const chrome = spawn(
    chromePath(),
    [
      '--headless',
      '--remote-debugging-port=0',
      '--window-size=1920,1080',
      '--hide-scrollbars',
      '--use-angle=swiftshader',
      '--enable-unsafe-swiftshader',
      '--autoplay-policy=no-user-gesture-required',
      `--user-data-dir=${profile}`,
      'about:blank',
    ],
    { stdio: ['ignore', 'ignore', 'pipe'] },
  );
  try {
    const wsBrowser = await new Promise((resolve, reject) => {
      let buf = '';
      const timer = setTimeout(() => reject(new Error('chrome did not start')), 20000);
      chrome.stderr.on('data', (chunk) => {
        buf += chunk;
        const m = /DevTools listening on (ws:\/\/\S+)/.exec(buf);
        if (m) {
          clearTimeout(timer);
          resolve(m[1]);
        }
      });
    });
    const port = new URL(wsBrowser).port;
    const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    const target = targets.find((t) => t.type === 'page');
    const cdp = await cdpConnect(target.webSocketDebuggerUrl);
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
    await cdp.send('Page.enable');
    if (process.env.SCROLLINE_OFFLINE === '1') {
      await cdp.send('Network.enable');
      await cdp.send('Network.setBlockedURLs', { urls: ['http://*', 'https://*'] });
    }
    await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: HMR_FREEZE });
    await cdp.send('Page.navigate', { url: deckUrl(opts) });
    const until = Date.now() + 30000;
    while (Date.now() < until && (await cdp.evaluate('document.readyState').catch(() => '')) !== 'complete')
      await new Promise((r) => setTimeout(r, 200));
    await cdp.evaluate(probeSource(opts.deck));
    const boot = await cdp.evaluate('window.__smoke.boot()');
    const out = { ...boot, stops: [] };
    if (!boot.bootError) {
      for (let i = 0; i < boot.stops.length; i += 1) {
        out.stops.push(await cdp.evaluate(`window.__smoke.at(${i})`));
        if (opts.shots) {
          const shot = await cdp.send('Page.captureScreenshot', { format: 'png' });
          writeFileSync(path.join(outDir, shotName(i)), Buffer.from(shot.data, 'base64'));
        }
      }
      out.pageErrors = await cdp.evaluate('window.__smoke.pageErrors.slice()');
    }
    cdp.close();
    return out;
  } finally {
    const exited = new Promise((r) => chrome.once('exit', r));
    chrome.kill('SIGKILL');
    await exited;
    // Chrome's helper processes can still be flushing the cache after the kill; a leftover temp profile
    // must not fail a finished run.
    try {
      rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
    } catch {}
  }
}

function contactSheet(outDir, count) {
  const files = Array.from({ length: count }, (_, i) => path.join(outDir, shotName(i))).filter(existsSync);
  if (!files.length) return null;
  const w = 480;
  const h = 270;
  const layout = files.map((_, i) => `${(i % SHEET_COLUMNS) * w}_${Math.floor(i / SHEET_COLUMNS) * h}`).join('|');
  const scaled = files
    .map((_, i) => `[${i}:v]scale=${w}:${h}[s${i}]`)
    .join(';');
  const fill = files.length === 1 ? `[s0]copy` : `${files.map((_, i) => `[s${i}]`).join('')}xstack=inputs=${files.length}:layout=${layout}:fill=gray`;
  const sheet = path.join(outDir, 'sheet.png');
  const result = spawnSync(
    'ffmpeg',
    ['-y', '-loglevel', 'error', ...files.flatMap((f) => ['-i', f]), '-filter_complex', `${scaled};${fill}`, '-frames:v', '1', sheet],
    { encoding: 'utf8' },
  );
  if (result.status !== 0) throw new Error(`ffmpeg sheet failed: ${result.stderr}`);
  return sheet;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) return console.log(usage);
  if (!existsSync(path.join(ROOT, 'decks', opts.deck, 'deck.yaml'))) throw new Error(`deck not found: ${opts.deck}`);
  const outDir = opts.out ? path.resolve(opts.out) : path.join(ROOT, 'out', 'smoke', opts.deck);
  mkdirSync(outDir, { recursive: true });
  for (const f of readdirSync(outDir)) if (/^stop-\d+\.png$/.test(f)) rmSync(path.join(outDir, f));
  const raw = opts.driver === 'chrome' ? await runChrome(opts, outDir) : runAside(opts);
  const report = {
    deck: opts.deck,
    url: deckUrl(opts),
    driver: opts.driver,
    at: new Date().toISOString(),
    viewport: raw.viewport ?? null,
    bootError: raw.bootError ?? null,
    pageErrors: raw.pageErrors ?? [],
    stops: raw.stops ?? [],
  };
  report.summary = summarize(report);
  if (opts.shots && report.stops.length) report.sheet = contactSheet(outDir, report.stops.length);
  writeFileSync(path.join(outDir, 'report.json'), `${JSON.stringify(report, null, 2)}\n`);
  console.log(formatReport(report));
  console.log(`report ${path.relative(ROOT, path.join(outDir, 'report.json'))}`);
  process.exitCode = report.summary.errors || report.summary.empty.length ? 1 : 0;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain)
  main().catch((error) => {
    console.error(`smoke: ${error.message}`);
    process.exitCode = 2;
  });
