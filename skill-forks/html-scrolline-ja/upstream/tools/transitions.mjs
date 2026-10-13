#!/usr/bin/env node
/**
 * 전환 검사: 덱의 모든 link·step 구간을 촘촘히 찍어 시트로 만든다(CONTRACTS C7 v2.3 규칙 4).
 * 정지점만 보는 smoke는 「들어간 뒤 그냥 빠진다」 같은 전환 중 결함을 못 잡는다.
 *   node tools/transitions.mjs <deckId> [--url <덱 URL>] [--samples 6] [--out out/transitions/<deckId>]
 * 기본 URL은 dev 서버(http://localhost:5190/decks/<deckId>/index.html).
 */
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { cdpConnect, chromePath } from './smoke.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
export const usage = 'node tools/transitions.mjs <deckId> [--url <url>] [--samples 6] [--out <dir>]';

export function parseArgs(argv) {
  const opts = { deck: null, url: null, samples: 6, out: null };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--url') opts.url = argv[++i];
    else if (a === '--samples') opts.samples = Math.max(2, Number(argv[++i]) || 6);
    else if (a === '--out') opts.out = argv[++i];
    else if (!a.startsWith('--') && !opts.deck) opts.deck = a;
    else throw new Error(`unknown argument: ${a}`);
  }
  if (!opts.deck || !/^_?[a-z0-9][a-z0-9-]*$/.test(opts.deck)) throw new Error(usage);
  opts.url ??= `http://localhost:5190/decks/${opts.deck}/index.html`;
  opts.out ??= path.join(ROOT, 'out', 'transitions', opts.deck);
  return opts;
}

/** link·step span마다 시작~끝을 samples개로 나눈 시각(양 끝 포함). */
export function sampleTimes(map, samples) {
  const rows = [];
  for (const beat of map.beats)
    for (const span of beat.spans) {
      if (span.role !== 'link' && span.role !== 'step') continue;
      const times = Array.from(
        { length: samples },
        (_, i) => span.start + ((span.end - span.start) * i) / (samples - 1),
      );
      rows.push({
        beat: beat.id,
        role: span.role,
        move: span.move,
        times: times.map((t) => Number(t.toFixed(3))),
      });
    }
  return rows;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  mkdirSync(opts.out, { recursive: true });
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
      'about:blank',
    ],
    { stdio: ['ignore', 'ignore', 'pipe'] },
  );
  try {
    const ws = await new Promise((resolve, reject) => {
      let buf = '';
      const timer = setTimeout(() => reject(new Error('chrome did not start')), 20000);
      chrome.stderr.on('data', (chunk) => {
        const m = /DevTools listening on (ws:\/\/\S+)/.exec((buf += chunk));
        if (m) resolve((clearTimeout(timer), m[1]));
      });
    });
    const port = new URL(ws).port;
    const page = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(
      (t) => t.type === 'page',
    );
    const cdp = await cdpConnect(page.webSocketDebuggerUrl);
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1920,
      height: 1080,
      deviceScaleFactor: 1,
      mobile: false,
    });
    await cdp.send('Page.navigate', { url: opts.url });
    for (let i = 0; i < 120 && !(await cdp.evaluate('!!window.__deck').catch(() => false)); i += 1)
      await new Promise((r) => setTimeout(r, 500));
    const map = await cdp.evaluate('JSON.parse(JSON.stringify(window.__deck.map))');
    const rows = sampleTimes(map, opts.samples);
    const sheets = [];
    for (const [n, row] of rows.entries()) {
      const files = [];
      for (const [k, t] of row.times.entries()) {
        await cdp.evaluate(`window.__deck.tl.seek(${t}); true`);
        await new Promise((r) => setTimeout(r, 900));
        const shot = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 70 });
        const file = path.join(
          opts.out,
          `${String(n + 1).padStart(2, '0')}-${row.beat}-${row.move}-${k}.jpg`,
        );
        writeFileSync(file, Buffer.from(shot.data, 'base64'));
        files.push(file);
      }
      // 한 전환 = 한 줄 시트(ffmpeg tile). 글자 합성 없이 순서만.
      const sheet = path.join(opts.out, `${String(n + 1).padStart(2, '0')}-${row.beat}-${row.move}.jpg`);
      spawnSync('ffmpeg', [
        '-y',
        '-loglevel',
        'error',
        ...files.flatMap((f) => ['-i', f]),
        '-filter_complex',
        `${files.map((_, i) => `[${i}:v]scale=480:-1[v${i}]`).join(';')};${files.map((_, i) => `[v${i}]`).join('')}hstack=inputs=${files.length}`,
        sheet,
      ]);
      sheets.push({ ...row, sheet: path.relative(ROOT, sheet) });
    }
    writeFileSync(
      path.join(opts.out, 'transitions.json'),
      JSON.stringify({ deck: opts.deck, url: opts.url, rows: sheets }, null, 2),
    );
    console.log(`transitions ${opts.deck}: ${sheets.length} spans → ${path.relative(ROOT, opts.out)}`);
    cdp.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url))
  main().catch((err) => {
    console.error(err.message);
    process.exit(2);
  });
