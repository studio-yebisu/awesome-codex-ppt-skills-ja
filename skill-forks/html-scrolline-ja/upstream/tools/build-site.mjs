#!/usr/bin/env node
/**
 * Gallery site: site/** + decks + previews → out/site (static, relative links, works under a sub-path).
 *   node tools/build-site.mjs [--no-decks] [--decks id,id] [--out out/site]
 * Previews, best first: out/export/<deck>.mp4 → 8 s 720p silent loop (ffmpeg); a loop captured from the built
 * deck (headless chrome seeks the timeline frame by frame between two stops); out/smoke/<deck>/stop-*.png
 * stills that cross-fade; a typeset poster in the concept palette.
 */
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';
import { cdpConnect, chromePath } from './smoke.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const usage =
  'node tools/build-site.mjs [--no-decks] [--decks id,id] [--no-capture] [--recapture] [--out out/site]';
export const CLIP = { seconds: 8, height: 720, maxrate: '1.2M', fps: 24 };
const CAPTURE_LIMIT_MS = 180000;
const STILLS_LIMIT_MS = 90000;
const MIN_STILL_BYTES = 14000; // a 960 px JPEG below this is an empty (black) stop

export function parseArgs(argv) {
  const opts = { decks: true, only: null, capture: true, recapture: false, out: 'out/site', help: false };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--help' || a === '-h') opts.help = true;
    else if (a === '--no-decks') opts.decks = false;
    else if (a === '--no-capture') opts.capture = false;
    else if (a === '--recapture') opts.recapture = true;
    else if (a === '--decks')
      opts.only = String(argv[(i += 1)] ?? '')
        .split(',')
        .filter(Boolean);
    else if (a === '--out') opts.out = argv[(i += 1)];
    else throw new Error(`unknown option: ${a}`);
  }
  return opts;
}

/* ---------- pure helpers (tested) ---------- */

export const esc = (s) =>
  String(s ?? '').replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c],
  );

/** Bilingual pair; a missing side falls back to the other. */
export function t(pair, tag = 'span') {
  const ko = pair?.ko ?? pair?.en ?? '';
  const en = pair?.en ?? pair?.ko ?? '';
  if (ko === en) return esc(ko);
  return `<${tag} class="ko" lang="ko">${esc(ko)}</${tag}><${tag} class="en" lang="en">${esc(en)}</${tag}>`;
}

/** n items spread evenly over the list, first and last included. */
export function pickEvenly(list, n) {
  if (list.length <= n) return list.slice();
  if (n <= 1) return list.slice(0, n);
  return Array.from({ length: n }, (_, i) => list[Math.round((i * (list.length - 1)) / (n - 1))]);
}

/** --sl-bg / --sl-fg / --sl-accent of the first concept rule in tokens.css. */
export function conceptPalette(css) {
  const get = (name) => css.match(new RegExp(`--sl-${name}\\s*:\\s*([^;]+);`))?.[1].trim();
  return { bg: get('bg') ?? '#111113', fg: get('fg') ?? '#f2efe8', accent: get('accent') ?? '#ff5a1f' };
}

/** Distinct non-engine move ids a deck yaml calls. */
export function deckMoves(yamlText) {
  const ids = new Set();
  for (const m of yamlText.matchAll(/\bmove:\s*["']?([a-z0-9][a-z0-9:-]*)/g))
    if (!m[1].startsWith('engine:')) ids.add(m[1]);
  return [...ids];
}

/** Clip window inside a video of `duration` seconds. */
export function clipWindow(duration, at = 0, seconds = CLIP.seconds) {
  const len = Math.min(seconds, duration);
  const start = Math.max(0, Math.min(duration * at, duration - len));
  return { start: Math.round(start * 100) / 100, len: Math.round(len * 100) / 100 };
}

/** Local href/src targets in an html string that do not resolve to a file under outDir. */
export function brokenLinks(html, fileDir, outDir, exists = fs.existsSync) {
  const bad = [];
  for (const m of html.matchAll(/\s(?:href|src|poster|data-src)="([^"]+)"/g)) {
    const raw = m[1];
    if (/^(?:[a-z]+:|#|\/\/)/i.test(raw)) continue;
    if (raw.startsWith('/')) {
      bad.push(`${raw} (absolute path breaks under a sub-path)`);
      continue;
    }
    const clean = decodeURI(raw.split(/[?#]/)[0]);
    let target = path.resolve(fileDir, clean);
    if (!target.startsWith(path.resolve(outDir))) bad.push(`${raw} (outside site)`);
    else if (clean.endsWith('/') || clean === '') target = path.join(target, 'index.html');
    if (!exists(target)) bad.push(raw);
  }
  return bad;
}

/* ---------- media ---------- */

const run = (cmd, args, opts = {}) => {
  const r = spawnSync(cmd, args, { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, ...opts });
  if (r.error) throw r.error;
  return r;
};
const ffmpeg = (args) => {
  const r = run('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args]);
  if (r.status !== 0) throw new Error(`ffmpeg failed: ${r.stderr}`);
};
const newer = (out, src) => fs.existsSync(out) && fs.statSync(out).mtimeMs >= fs.statSync(src).mtimeMs;

function duration(file) {
  const r = run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]);
  return Number(r.stdout.trim()) || 0;
}

/** 8 s silent 720p loop + poster from an exported deck MP4. */
function makeClip(src, outBase, at, seconds) {
  const { start, len } = clipWindow(duration(src), at, seconds);
  const mp4 = `${outBase}.mp4`;
  const jpg = `${outBase}.jpg`;
  if (!newer(mp4, src)) {
    ffmpeg([
      '-ss',
      String(start),
      '-t',
      String(len),
      '-i',
      src,
      '-an',
      '-vf',
      `scale=-2:${CLIP.height}:flags=lanczos,fps=30`,
      '-c:v',
      'libx264',
      '-preset',
      'slow',
      '-crf',
      '27',
      '-maxrate',
      CLIP.maxrate,
      '-bufsize',
      '2.4M',
      '-pix_fmt',
      'yuv420p',
      '-movflags',
      '+faststart',
      mp4,
    ]);
    ffmpeg(['-ss', String(start), '-i', src, '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '4', jpg]);
  }
  return { kind: 'video', src: mp4, poster: jpg };
}

/** Smoke stop PNGs → 960 px JPEGs, empty (near-black) stops dropped. */
function makeStills(deck, stopNumbers, outDir, max = 6) {
  const dir = path.join(ROOT, 'out', 'smoke', deck);
  if (!fs.existsSync(dir)) return null;
  const all = fs
    .readdirSync(dir)
    .filter((f) => /^stop-\d+\.png$/.test(f))
    .sort();
  const wanted = stopNumbers
    ? stopNumbers.map((n) => `stop-${String(n).padStart(2, '0')}.png`).filter((f) => all.includes(f))
    : all;
  fs.mkdirSync(outDir, { recursive: true });
  const usable = [];
  for (const f of wanted) {
    const src = path.join(dir, f);
    const out = path.join(outDir, f.replace('.png', '.jpg'));
    if (!newer(out, src)) ffmpeg(['-i', src, '-vf', 'scale=960:-2:flags=lanczos', '-q:v', '5', out]);
    if (fs.statSync(out).size >= MIN_STILL_BYTES) usable.push(out);
  }
  const picked = stopNumbers ? usable.slice(0, max) : pickEvenly(usable, max);
  return picked.length ? { kind: 'stills', srcs: picked } : null;
}

async function previewFor(spec, mediaDir, ctx) {
  const { deck, at = 0, seconds = CLIP.seconds, stops = null, name, capture } = spec;
  const outBase = path.join(mediaDir, name);
  const mp4 = path.join(ROOT, 'out', 'export', `${deck}.mp4`);
  if (fs.existsSync(mp4)) return makeClip(mp4, outBase, at, seconds);
  const built = path.join(ctx.outDir, 'decks', deck, 'index.html');
  if (ctx.capture && capture && fs.existsSync(built)) {
    const want = {
      deck,
      from: capture.from,
      to: capture.to,
      seconds: capture.seconds ?? seconds,
      posterAt: capture.posterAt ?? 0.5,
    };
    const sidecar = `${outBase}.json`;
    const cached =
      fs.existsSync(sidecar) && newer(sidecar, built) ? JSON.parse(fs.readFileSync(sidecar, 'utf8')) : null;
    const usable = (r) =>
      r && [r.src, r.poster, ...(r.srcs ?? [])].filter(Boolean).every((f) => fs.existsSync(f));
    const same = !ctx.recapture && cached && JSON.stringify(cached.spec) === JSON.stringify(want);
    const remember = (result) => (fs.writeFileSync(sidecar, JSON.stringify({ spec: want, result })), result);
    if (same && usable(cached.result)) return cached.result;
    if (same && cached.result === null) return makeStills(deck, stops, outBase) ?? { kind: 'none' };
    const attempt = async (what, job, limit) => {
      try {
        ctx.browser ??= await openBrowser();
        const started = Date.now();
        const result = await within(job(), limit, `capture ${name}`);
        console.log(
          `capture ${name} (${what}): ${deck} stops ${want.from}→${want.to} · ${((Date.now() - started) / 1000).toFixed(0)} s`,
        );
        return result;
      } catch (e) {
        console.warn(`capture ${name} (${what}) failed: ${e.message}`);
        // a hung page poisons the tab: start the next capture in a fresh browser
        await ctx.browser?.close().catch(() => {});
        ctx.browser = null;
        return null;
      }
    };
    const clip = await attempt(
      'loop',
      () => captureClip(ctx.browser, ctx.base, want, outBase),
      CAPTURE_LIMIT_MS,
    );
    if (clip) return remember(clip);
    const shots = await attempt(
      'stills',
      () => captureStills(ctx.browser, ctx.base, want, outBase),
      STILLS_LIMIT_MS,
    );
    if (shots) return remember(shots);
    remember(null); // deck does not boot: skip it until it is rebuilt
  }
  return makeStills(deck, stops, outBase) ?? { kind: 'none' };
}

/** Times (s) of `frames` evenly spaced samples from stop `from` to stop `to` (1-based, clamped). */
export function captureTimes(stops, from, to, frames) {
  if (!stops.length) return [];
  const at = (n) => stops[Math.max(0, Math.min(stops.length - 1, n - 1))].t;
  const a = at(from);
  const b = at(to);
  return Array.from({ length: frames }, (_, i) => a + ((b - a) * i) / Math.max(1, frames - 1));
}

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.mjs': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.gif': 'image/gif',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.mp3': 'audio/mpeg',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.glb': 'model/gltf-binary',
};

/** Static server over outDir with Range support (video elements seek). */
export function serve(dir) {
  const server = http.createServer((req, res) => {
    let file = path.join(dir, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!file.startsWith(dir)) return res.writeHead(403).end();
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file)) return res.writeHead(404).end();
    const size = fs.statSync(file).size;
    const type = MIME[path.extname(file).toLowerCase()] ?? 'application/octet-stream';
    const range = /bytes=(\d*)-(\d*)/.exec(req.headers.range ?? '');
    if (range) {
      const start = range[1] ? Number(range[1]) : 0;
      const end = range[2] ? Number(range[2]) : size - 1;
      res.writeHead(206, {
        'Content-Type': type,
        'Content-Range': `bytes ${start}-${end}/${size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': end - start + 1,
      });
      return fs.createReadStream(file, { start, end }).pipe(res);
    }
    res.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes' });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server)));
}

/** One headless chrome for every capture of a build. */
export async function openBrowser() {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-site-'));
  const chrome = spawn(
    chromePath(),
    [
      '--headless',
      '--remote-debugging-port=0',
      '--window-size=1920,1080',
      '--hide-scrollbars',
      '--mute-audio',
      '--use-angle=swiftshader',
      '--enable-unsafe-swiftshader',
      '--autoplay-policy=no-user-gesture-required',
      `--user-data-dir=${profile}`,
      'about:blank',
    ],
    { stdio: ['ignore', 'ignore', 'pipe'] },
  );
  const ws = await new Promise((resolve, reject) => {
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
  const port = new URL(ws).port;
  const target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(
    (x) => x.type === 'page',
  );
  const cdp = await cdpConnect(target.webSocketDebuggerUrl);
  // decks lay out at 1920×1080 CSS px; the device scale renders that straight to the clip height
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: 1920,
    height: 1080,
    deviceScaleFactor: CLIP.height / 1080,
    mobile: false,
  });
  await cdp.send('Page.enable');
  return {
    cdp,
    async close() {
      cdp.close();
      const exited = new Promise((r) => chrome.once('exit', r));
      chrome.kill('SIGKILL');
      await exited;
      fs.rmSync(profile, { recursive: true, force: true, maxRetries: 3 });
    },
  };
}

const within = (promise, ms, what) =>
  Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error(`${what} timed out after ${ms / 1000} s`)), ms),
    ),
  ]);

const SEEK = `async (t, y) => {
  const raf = () => new Promise((r) => requestAnimationFrame(() => r()));
  window.scrollTo(0, y);
  window.__deck.tl.seek(t);
  await raf(); await raf();
  window.__deck.tl.seek(t);
  await raf();
}`;

/** Load a built deck and wait for its timeline; returns the stops with scroll y. */
async function openDeck(cdp, base, deck) {
  await cdp.send('Page.navigate', { url: `${base}/decks/${deck}/` });
  const until = Date.now() + 20000;
  while (
    Date.now() < until &&
    !(await cdp.evaluate('Boolean(window.__deck) && document.readyState === "complete"').catch(() => false))
  )
    await new Promise((r) => setTimeout(r, 200));
  if (!(await cdp.evaluate('Boolean(window.__deck)')))
    throw new Error(`${deck}: window.__deck never appeared`);
  await cdp.evaluate('document.fonts.ready.then(() => new Promise((r) => setTimeout(r, 1200)))');
  const stops = await cdp.evaluate('window.__deck.stops().map((s) => ({ t: s.t, y: s.y ?? 0 }))');
  if (stops.length < 2) throw new Error(`${deck}: fewer than two stops`);
  return stops;
}

/** y is linear in t (scroll driver): fit it from the first and last stop. */
function scrollFit(stops) {
  const [s0, s1] = [stops[0], stops.at(-1)];
  const slope = s1.t === s0.t ? 0 : (s1.y - s0.y) / (s1.t - s0.t);
  return (t) => Math.round(s0.y + (t - s0.t) * slope);
}

/** One still per stop between two stops (at most 5) when a loop is too slow to capture. */
async function captureStills(browser, base, spec, outBase) {
  const { cdp } = browser;
  const stops = await openDeck(cdp, base, spec.deck);
  const y = scrollFit(stops);
  const numbers = pickEvenly(
    Array.from({ length: Math.max(1, spec.to - spec.from + 1) }, (_, i) => spec.from + i).filter(
      (n) => n <= stops.length,
    ),
    5,
  );
  const srcs = [];
  for (const n of numbers) {
    const t = stops[n - 1].t;
    await cdp.evaluate(`(${SEEK})(${t}, ${y(t)}).then(() => new Promise((r) => setTimeout(r, 400)))`);
    const shot = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 82 });
    const file = `${outBase}-s${String(n).padStart(2, '0')}.jpg`;
    fs.writeFileSync(file, Buffer.from(shot.data, 'base64'));
    srcs.push(file);
  }
  return { kind: 'stills', srcs };
}

/** Frame-by-frame loop of a built deck between two stops → mp4 + poster. */
async function captureClip(browser, base, spec, outBase) {
  const { cdp } = browser;
  const stops = await openDeck(cdp, base, spec.deck);
  const y = scrollFit(stops);
  const frames = Math.round(spec.seconds * CLIP.fps);
  const times = captureTimes(stops, spec.from, spec.to, frames);
  // visit every stop in range first so lazy images, frame sequences and video posters are loaded
  for (
    let n = Math.min(spec.from, spec.to);
    n <= Math.min(Math.max(spec.from, spec.to), stops.length);
    n += 1
  )
    await cdp.evaluate(
      `(${SEEK})(${stops[n - 1].t}, ${y(stops[n - 1].t)}).then(() => new Promise((r) => setTimeout(r, 700)))`,
    );
  // warm up on the first frame: media and late layout settle before frame 0 is taken
  await cdp.evaluate(
    `(${SEEK})(${times[0]}, ${y(times[0])}).then(() => new Promise((r) => setTimeout(r, 900)))`,
  );
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-frames-'));
  try {
    for (let i = 0; i < times.length; i += 1) {
      const t = times[i];
      await cdp.evaluate(`(${SEEK})(${t}, ${y(t)})`);
      const shot = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 88 });
      fs.writeFileSync(
        path.join(tmp, `f${String(i).padStart(4, '0')}.jpg`),
        Buffer.from(shot.data, 'base64'),
      );
    }
    ffmpeg([
      '-framerate',
      String(CLIP.fps),
      '-i',
      path.join(tmp, 'f%04d.jpg'),
      '-an',
      '-vf',
      `scale=-2:${CLIP.height}:flags=lanczos`,
      '-c:v',
      'libx264',
      '-preset',
      'slow',
      '-crf',
      '26',
      '-maxrate',
      CLIP.maxrate,
      '-bufsize',
      '2.4M',
      '-pix_fmt',
      'yuv420p',
      '-movflags',
      '+faststart',
      `${outBase}.mp4`,
    ]);
    const poster = Math.min(times.length - 1, Math.round(times.length * (spec.posterAt ?? 0.5)));
    fs.copyFileSync(path.join(tmp, `f${String(poster).padStart(4, '0')}.jpg`), `${outBase}.jpg`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  return { kind: 'video', src: `${outBase}.mp4`, poster: `${outBase}.jpg` };
}

/* ---------- html ---------- */

const ARROW =
  '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M2 7h9M7.5 3.5 11 7l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';
const GITHUB =
  '<svg width="18" height="18" viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8a8 8 0 0 0 5.47 7.59c.4.07.55-.17.55-.38v-1.34c-2.23.48-2.7-1.07-2.7-1.07-.36-.92-.89-1.17-.89-1.17-.73-.5.05-.49.05-.49.8.06 1.23.83 1.23.83.72 1.22 1.88.87 2.33.66.07-.52.28-.87.5-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.6 7.6 0 0 1 4 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48v2.2c0 .21.15.46.55.38A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>';
const MARK = `<svg class="brand-mark" viewBox="0 0 18 18" aria-hidden="true"><rect x="1" y="3" width="16" height="2" rx="1" fill="currentColor" opacity=".35"/><rect x="1" y="8" width="16" height="2" rx="1" fill="currentColor"/><rect x="1" y="13" width="16" height="2" rx="1" fill="currentColor" opacity=".35"/><circle cx="7" cy="9" r="3" fill="#ff5a1f"/></svg>`;

function rel(prefix, file, outDir) {
  return prefix + path.relative(outDir, file).split(path.sep).join('/');
}

function mediaHtml(m, prefix, outDir, label, posterText, period) {
  if (m.kind === 'video')
    return `<div class="preview"><video muted loop playsinline preload="metadata" poster="${rel(prefix, m.poster, outDir)}" src="${rel(prefix, m.src, outDir)}" aria-label="${esc(label)}"></video></div>`;
  if (m.kind === 'stills')
    return `<div class="preview stills" data-period="${period}" role="img" aria-label="${esc(label)}">${m.srcs
      .map((s, i) =>
        i === 0
          ? `<img class="on" src="${rel(prefix, s, outDir)}" alt="" decoding="async">`
          : `<img data-src="${rel(prefix, s, outDir)}" alt="" decoding="async">`,
      )
      .join('')}</div>`;
  return `<div class="preview" role="img" aria-label="${esc(label)}"><div class="poster-type">${posterText}</div></div>`;
}

function page({ c, prefix, title, description, body, current }) {
  const nav = [
    ['decks', `${prefix}#decks`],
    ['how', `${prefix}#how`],
    ['start', `${prefix}#start`],
    ['moves', `${prefix}moves/`],
  ];
  return `<!doctype html>
<html lang="ko" data-lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title.ko)}</title>
<meta name="sl-title-ko" content="${esc(title.ko)}">
<meta name="sl-title-en" content="${esc(title.en)}">
<meta name="description" content="${esc(description.en)}">
<meta property="og:title" content="${esc(title.en)}">
<meta property="og:description" content="${esc(description.en)}">
<meta name="theme-color" content="#0a0a0b">
<link rel="icon" href="${prefix}assets/mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="${prefix}assets/style.css">
<script>try{var l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('scrolline-lang')||((navigator.language||'').toLowerCase().indexOf('ko')===0?'ko':'en');document.documentElement.dataset.lang=l;document.documentElement.lang=l}catch(e){}</script>
</head>
<body>
<a class="skip" href="#main">${t({ ko: '본문으로', en: 'Skip to content' })}</a>
<header class="bar"><div class="wrap">
<a class="brand" href="${prefix || './'}">${MARK}Scrolline</a>
<nav aria-label="Site">${nav
    .map(
      ([k, href]) =>
        `<a href="${href}"${k === current ? ' aria-current="page" class="keep"' : k === 'moves' ? ' class="keep"' : ''}>${t(c.nav[k])}</a>`,
    )
    .join('')}</nav>
<div class="lang" role="group" aria-label="Language"><button type="button" data-set="ko">KO</button><button type="button" data-set="en">EN</button></div>
<a class="gh" href="${c.repo}" aria-label="GitHub">${GITHUB}</a>
</div></header>
<main id="main">
${body}
</main>
<footer><div class="wrap"><span>Scrolline v2</span><a href="${c.repo}">${t(c.footer.source)}</a><span>${t(c.footer.license)}</span></div></footer>
<script src="${prefix}assets/app.js" defer></script>
</body>
</html>
`;
}

export function renderIndex(c, decks, how, outDir) {
  const p = '';
  const tiles = decks
    .map((d, i) => {
      const style = `--c-bg:${d.palette.bg};--c-fg:${d.palette.fg};--c-accent:${d.palette.accent}`;
      const label = `${d.name.en}: ${d.title.en}`;
      const media = mediaHtml(d.preview, p, outDir, label, t(d.title), 1800 + i * 170);
      const open = d.built
        ? `<a class="open" href="decks/${d.id}/">${t(c.tile.open)} ${ARROW}</a>`
        : `<span class="open">${t(c.tile.open)}</span>`;
      return `<li class="deck${d.built ? '' : ' disabled'}" style="${style}">
${media}
<div class="meta">
<div class="row"><span class="num mono">${String(i + 1).padStart(2, '0')}</span><h2>${t(d.name)}</h2>${open}</div>
<p class="title">${t(d.title)}</p>
<p class="use">${t(d.use)}<span class="sep" aria-hidden="true"></span>${t(d.sample ? c.tile.sample : c.tile.real)} · ${d.moveCount} ${t(c.tile.moves)}</p>
</div>
</li>`;
    })
    .join('\n');

  const howItems = c.how.items
    .map((h, i) => {
      const media = mediaHtml(how[i], p, outDir, h.title.en, t(h.title), 1100);
      return `<li>${media}<h3>${t(h.title)}</h3><p>${t(h.body)}</p></li>`;
    })
    .join('\n');

  const lines = c.start.lines;
  const families = Object.keys(c.movesPage.families);
  const body = `
<section class="wrap intro" id="decks" aria-labelledby="h-intro">
<h1 id="h-intro">${t(c.hero.lead)} <span class="rest">${t(c.hero.rest)}</span></h1>
</section>
<div class="wrap"><ul class="decks">
${tiles}
</ul></div>

<section class="wrap section" id="how" aria-labelledby="h-how">
<div class="section-head"><h2 id="h-how">${t(c.how.heading)}</h2></div>
<ul class="how">
${howItems}
</ul>
</section>

<section class="wrap section" id="start" aria-labelledby="h-start">
<div class="section-head"><h2 id="h-start">${t(c.start.heading)}</h2></div>
<div class="start">
<p>${t(c.start.body)}</p>
<div>
<div class="code"><pre>${lines.map((l) => `<span class="p">$ </span>${esc(l)}`).join('\n')}</pre><button type="button" class="copy" data-copy="${esc(lines.join('\n'))}"><span class="idle">${t(c.start.copy)}</span><span class="ok">${t(c.start.copied)}</span></button></div>
<p class="after">${t(c.start.after)}</p>
</div>
</div>
</section>

<section class="wrap section" id="moves" aria-labelledby="h-moves">
<div class="section-head"><h2 id="h-moves">${t(c.movesTeaser.heading)}</h2></div>
<div class="teaser"><p class="muted">${t(c.movesTeaser.body)}</p><a class="button" href="moves/">${t(c.movesTeaser.cta)} ${ARROW}</a></div>
<div class="chips">${families
    .map(
      (f) =>
        `<a class="chip" href="moves/#family=${f}"><span>${t(c.movesPage.families[f])}</span><span class="mono">${f}</span></a>`,
    )
    .join('')}</div>
</section>
`;
  return page({ c, prefix: p, title: c.site.title, description: c.site.description, body, current: 'decks' });
}

export function renderMoves(c, moves, lines, decks) {
  const p = '../';
  const byConcept = Object.fromEntries(decks.map((d) => [d.concept, d]));
  const families = Object.keys(c.movesPage.families);
  const counts = Object.fromEntries(families.map((f) => [f, moves.filter((m) => m.family === f).length]));
  const order = (m) => families.indexOf(m.family);
  const rows = moves
    .slice()
    .sort((a, b) => order(a) - order(b) || a.id.localeCompare(b.id))
    .map((m) => {
      const line = lines[m.id] ?? { ko: m.summary, en: m.summary };
      const used = m.concepts
        .map((cid) => byConcept[cid])
        .filter(Boolean)
        .map(
          (d) =>
            `<a href="${d.built ? `${p}decks/${d.id}/` : `${p}#decks`}" style="--c-accent:${d.palette.accent}"><span class="dot" aria-hidden="true"></span>${t(d.name)}</a>`,
        )
        .join('');
      const role = c.movesPage.roles[m.role] ?? { ko: m.role, en: m.role };
      const sig = m.signature_of?.length ? `<span class="sig">${t(c.movesPage.signature)}</span>` : '';
      const search = [m.id, m.family, m.role, line.ko, line.en, ...m.concepts].join(' ').toLowerCase();
      return `<li class="move" data-family="${m.family}" data-search="${esc(search)}">
<div><div class="id">${esc(m.id)}</div><div class="kind mono"><span>${esc(m.family)}</span><span>${t(role)}</span>${sig}</div></div>
<p class="line">${t(line)}</p>
<div class="used" aria-label="${esc(c.movesPage.usedIn.en)}">${used}</div>
</li>`;
    })
    .join('\n');
  const body = `
<section class="wrap page-head" aria-labelledby="h-moves">
<h1 id="h-moves">${t(c.movesPage.title)} <span class="muted mono">${moves.length}</span></h1>
<div class="head-row"><p>${t(c.movesPage.lead)}</p>
<div class="search"><input type="search" placeholder="${esc(c.movesPage.filter.ko)}" data-ph-ko="${esc(c.movesPage.filter.ko)}" data-ph-en="${esc(c.movesPage.filter.en)}" aria-label="${esc(c.movesPage.filter.en)}"><p class="count mono"><span data-n>${moves.length}</span> / ${moves.length}</p></div></div>
</section>
<div class="filters"><div class="wrap">
<div class="chips" role="group" aria-label="Family">
<button type="button" class="chip" data-family="all" aria-pressed="true"><span>${t(c.movesPage.all)}</span><span class="mono">${moves.length}</span></button>
${families
  .map(
    (f) =>
      `<button type="button" class="chip" data-family="${f}" aria-pressed="false"><span>${t(c.movesPage.families[f])}</span><span class="mono">${counts[f]}</span></button>`,
  )
  .join('\n')}
</div>
</div></div>
<div class="wrap">
<ul class="moves">
${rows}
</ul>
<p class="none" hidden>${t(c.movesPage.empty)}</p>
</div>
`;
  return page({
    c,
    prefix: p,
    title: { ko: `${c.movesPage.title.ko} · Scrolline`, en: `${c.movesPage.title.en} · Scrolline` },
    description: c.site.description,
    body,
    current: 'moves',
  });
}

/* ---------- build ---------- */

function buildDeck(id, outDir) {
  const r = run('npx', ['vite', 'build', '--logLevel', 'error'], {
    env: { ...process.env, SCROLLINE_DECK: id, SCROLLINE_OUT: path.join(outDir, 'decks', id) },
  });
  if (r.status !== 0) {
    console.warn(
      `deck ${id}: vite build failed\n${(r.stderr || r.stdout).split('\n').slice(0, 8).join('\n')}`,
    );
    return false;
  }
  // deck.yaml names media by path at runtime, so Vite never sees them: copy the folder like tools/export.mjs
  const assets = path.join(ROOT, 'decks', id, 'assets');
  if (fs.existsSync(assets))
    fs.cpSync(assets, path.join(outDir, 'decks', id, 'assets'), {
      recursive: true,
      filter: (src) => !/\.md$/.test(src) && path.basename(src) !== 'runs',
    });
  return fs.existsSync(path.join(outDir, 'decks', id, 'index.html'));
}

function walkHtml(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory() && e.name !== 'decks') walkHtml(p, out);
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) return console.log(usage);
  const outDir = path.resolve(ROOT, opts.out);
  const mediaDir = path.join(outDir, 'media');
  const c = JSON.parse(fs.readFileSync(path.join(ROOT, 'site', 'content.json'), 'utf8'));

  // Keep built decks (when not rebuilding) and the media cache; regenerate everything else.
  fs.mkdirSync(outDir, { recursive: true });
  for (const e of fs.readdirSync(outDir))
    if (!['decks', 'media'].includes(e)) fs.rmSync(path.join(outDir, e), { recursive: true, force: true });
  fs.mkdirSync(path.join(outDir, 'assets'), { recursive: true });
  for (const f of ['style.css', 'app.js'])
    fs.copyFileSync(path.join(ROOT, 'site', f), path.join(outDir, 'assets', f));
  fs.writeFileSync(
    path.join(outDir, 'assets', 'mark.svg'),
    MARK.replace('class="brand-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replaceAll(
      'currentColor',
      '#f2efe8',
    ),
  );
  fs.writeFileSync(path.join(outDir, '.nojekyll'), '');

  const decks = c.decks.map((d) => {
    const yamlText = fs.readFileSync(path.join(ROOT, 'decks', d.id, 'deck.yaml'), 'utf8');
    const yaml = YAML.parse(yamlText);
    const css = fs.readFileSync(path.join(ROOT, 'concepts', d.concept, 'tokens.css'), 'utf8');
    const wantBuild = opts.decks && (!opts.only || opts.only.includes(d.id));
    const built = wantBuild
      ? buildDeck(d.id, outDir)
      : fs.existsSync(path.join(outDir, 'decks', d.id, 'index.html'));
    console.log(`deck ${d.id}: ${built ? 'ok' : 'missing'}${wantBuild ? ' (built)' : ''}`);
    return {
      ...d,
      title: { ko: yaml.title, en: d.title?.en ?? yaml.title },
      sample: Boolean(yaml.sample),
      palette: conceptPalette(css),
      moveCount: deckMoves(yamlText).length,
      built,
    };
  });

  const server = await serve(outDir);
  const ctx = {
    outDir,
    capture: opts.capture,
    recapture: opts.recapture,
    base: `http://127.0.0.1:${server.address().port}`,
    browser: null,
  };
  const how = [];
  try {
    for (const d of decks)
      d.preview = await previewFor(
        { deck: d.id, at: d.clip?.at ?? 0, stops: d.stills ?? null, capture: d.capture, name: d.id },
        mediaDir,
        ctx,
      );
    for (const h of c.how.items)
      how.push(
        await previewFor(
          {
            deck: h.deck,
            at: h.clip?.at ?? 0,
            seconds: h.clip?.seconds ?? 6,
            stops: h.stills ?? null,
            capture: h.capture,
            name: `how-${h.id}`,
          },
          mediaDir,
          ctx,
        ),
      );
  } finally {
    await ctx.browser?.close();
    server.close();
  }

  const moves = fs
    .readFileSync(path.join(ROOT, 'plan', 'moves.catalog.jsonl'), 'utf8')
    .split('\n')
    .filter(Boolean)
    .map((l) => JSON.parse(l));
  const lines = JSON.parse(fs.readFileSync(path.join(ROOT, 'site', 'data', 'moves.lines.json'), 'utf8'));

  fs.writeFileSync(path.join(outDir, 'index.html'), renderIndex(c, decks, how, outDir));
  fs.mkdirSync(path.join(outDir, 'moves'), { recursive: true });
  fs.writeFileSync(path.join(outDir, 'moves', 'index.html'), renderMoves(c, moves, lines, decks));

  let broken = 0;
  for (const file of walkHtml(outDir)) {
    for (const b of brokenLinks(fs.readFileSync(file, 'utf8'), path.dirname(file), outDir)) {
      console.error(`broken link in ${path.relative(outDir, file)}: ${b}`);
      broken += 1;
    }
  }
  const kinds = decks.map((d) => `${d.id}=${d.preview.kind}`).join(' ');
  console.log(`site → ${path.relative(ROOT, outDir)} · pages 2 · previews ${kinds} · broken links ${broken}`);
  if (broken) process.exitCode = 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((e) => {
    console.error(e.message);
    process.exit(1);
  });
}
