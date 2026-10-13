#!/usr/bin/env node
/** Capture export-path stop centers and optional in-between frames with HyperFrames. */
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseCaptureArgs } from './export-lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const usage = 'node tools/capture.mjs <deckId> [--stops] [--between] [--at s1,s2]';
const run = (command, args, quiet = false) => {
  const result = spawnSync(command, args, { cwd: ROOT, stdio: quiet ? 'pipe' : 'inherit', encoding: 'utf8' });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    if (quiet) process.stderr.write(result.stderr || result.stdout || '');
    throw new Error(`${command} exited ${result.status}`);
  }
};

async function main() {
  const args = process.argv.slice(2);
  const parsed = parseCaptureArgs(args);
  if (parsed.help) return console.log(usage);
  const { deckId } = parsed;
  const deckFile = path.join(ROOT, 'decks', deckId, 'deck.yaml');
  if (!existsSync(deckFile)) throw new Error(`deck not found: ${deckId}`);
  const output = path.join(ROOT, 'out', 'capture', deckId);
  mkdirSync(output, { recursive: true });
  // Keep this wrapper light: export owns the registry/plan imports, then writes
  // the pure plan for snapshots to consume after that child has exited.
  const planFile = path.join(output, '.export-plan.json');
  run(
    process.execPath,
    [
      path.join(ROOT, 'tools', 'export.mjs'),
      deckId,
      '--build-only',
      '--report',
      path.relative(ROOT, planFile),
    ],
    true,
  );
  const report = JSON.parse(readFileSync(planFile, 'utf8'));
  const { map, path: pathInfo } = report;
  const requested = parsed.at;
  const names = parsed.stops || requested.length === 0 ? map.stops.map((stop) => stop.name) : requested;
  const unknown = names.filter((name) => !(name in pathInfo.stopAt));
  if (unknown.length) throw new Error(`unknown stop(s): ${unknown.join(', ')}`);
  const shots = names.map((stop) => ({ stop, t: pathInfo.stopAt[stop], kind: 'stop' }));
  const stopCount = shots.length;
  if (parsed.between)
    for (let index = 1; index < stopCount; index += 1)
      shots.push({
        stop: null,
        t: (shots[index - 1].t + shots[index].t) / 2,
        kind: 'between',
        before: shots[index - 1].stop,
        after: shots[index].stop,
      });
  shots.sort((a, b) => a.t - b.t);
  const project = report.buildDir;
  const manifest = [];
  const before = new Set(readdirSync(output));
  run(
    'npx',
    [
      'hyperframes',
      'snapshot',
      project,
      '--at',
      shots.map((shot) => shot.t).join(','),
      '--no-end',
      '--output',
      output,
    ],
    true,
  );
  const files = readdirSync(output)
    .filter((name) => name.endsWith('.png') && !before.has(name))
    .sort();
  if (files.length !== shots.length)
    throw new Error(`snapshot produced ${files.length} PNGs for ${shots.length} requested frames`);
  for (const [index, shot] of shots.entries()) {
    const file = files[index];
    const safe = (value) =>
      String(value)
        .replace(/[^a-z0-9-]+/gi, '-')
        .replace(/^-+|-+$/g, '');
    const label = shot.kind === 'stop' ? safe(shot.stop) : `${safe(shot.before)}-to-${safe(shot.after)}`;
    const target = `${shot.kind === 'stop' ? 'stop' : 'between'}-${String(index + 1).padStart(2, '0')}-${label}.png`;
    renameSync(path.join(output, file), path.join(output, target));
    manifest.push({ file: target, t: shot.t, stop: shot.stop, kind: shot.kind });
  }
  const pngs = manifest.map((shot) => path.join(output, shot.file));
  if (pngs.length) {
    const columns = Math.ceil(Math.sqrt(pngs.length));
    const layout = pngs
      .map((_, index) => `${(index % columns) * 480}_${Math.floor(index / columns) * 270}`)
      .join('|');
    const filters = pngs.map((_, index) => `[${index}:v]scale=480:270[s${index}]`).join(';');
    run(
      'ffmpeg',
      [
        '-y',
        ...pngs.flatMap((file) => ['-i', file]),
        '-filter_complex',
        `${filters};${pngs.map((_, index) => `[s${index}]`).join('')}xstack=inputs=${pngs.length}:layout=${layout}`,
        '-frames:v',
        '1',
        path.join(output, 'sheet.png'),
      ],
      true,
    );
  }
  writeFileSync(
    path.join(output, 'manifest.json'),
    `${JSON.stringify({ deck: deckId, shots: manifest }, null, 2)}\n`,
  );
}

main().catch((error) => {
  console.error(`capture: ${error.message}`);
  process.exitCode = 2;
});
