#!/usr/bin/env node
/** Extract a WebP frame sequence and its C13 frames.json manifest. */
import { existsSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { printMediaNotice } from '../lib/media-notice.mjs';

export function parseArgs(argv) {
  const [input, outDir, ...rest] = argv;
  if (!input || !outDir)
    throw new Error(
      'usage: extract-frames <input.mp4> <outDir> [--fps 24] [--tiers 1920,960] [--quality 78] [--from 0] [--to <sec>]',
    );
  const options = { fps: 24, tiers: [1920, 960], quality: 78, from: 0, to: undefined };
  for (let i = 0; i < rest.length; i += 2) {
    const key = rest[i];
    const value = rest[i + 1];
    if (!key?.startsWith('--') || value === undefined) throw new Error(`invalid argument: ${key ?? ''}`);
    if (key === '--tiers') options.tiers = value.split(',').map(Number);
    else if (key === '--fps' || key === '--quality' || key === '--from' || key === '--to')
      options[key.slice(2)] = Number(value);
    else throw new Error(`unknown option: ${key}`);
  }
  if (
    !Number.isFinite(options.fps) ||
    options.fps <= 0 ||
    !Number.isFinite(options.quality) ||
    options.quality < 0 ||
    options.quality > 100 ||
    !Number.isFinite(options.from) ||
    (options.to !== undefined && (!Number.isFinite(options.to) || options.to <= options.from)) ||
    !options.tiers.length ||
    options.tiers.some((n) => !Number.isInteger(n) || n <= 0)
  )
    throw new Error('invalid frame extraction options');
  return { input, outDir, options };
}
function run(args) {
  return spawnSync('ffmpeg', args, { encoding: 'utf8' });
}
export function ffmpegAvailable() {
  const result = run(['-version']);
  return !result.error && result.status === 0;
}
function dimensions(input) {
  const result = run(['-i', input]);
  const match = `${result.stdout}\n${result.stderr}`.match(/\b(\d{2,5})x(\d{2,5})\b/);
  if (!match) throw new Error('ffmpeg could not determine input dimensions');
  return { width: Number(match[1]), height: Number(match[2]) };
}
export function extract({ input, outDir, options }) {
  if (!ffmpegAvailable()) return 2;
  if (!existsSync(input)) throw new Error(`input does not exist: ${input}`);
  const source = dimensions(input);
  const root = resolve(outDir);
  mkdirSync(root, { recursive: true });
  const timing = options.from > 0 ? ['-ss', String(options.from), '-i', input] : ['-i', input];
  const range = options.to === undefined ? [] : ['-t', String(options.to - options.from)];
  for (const tier of options.tiers) {
    const dir = resolve(root, String(tier));
    mkdirSync(dir, { recursive: true });
    const result = run([
      '-y',
      ...timing,
      ...range,
      '-vf',
      `fps=${options.fps},scale=${tier}:-2`,
      '-q:v',
      String(options.quality),
      '-start_number',
      '1',
      '-f',
      'image2',
      '-c:v',
      'libwebp',
      resolve(dir, 'f_%04d.webp'),
    ]);
    if (result.status !== 0) throw new Error(result.stderr || 'ffmpeg frame extraction failed');
  }
  const largest = Math.max(...options.tiers);
  const poster = run([
    '-y',
    ...timing,
    '-frames:v',
    '1',
    '-vf',
    `scale=${largest}:-2`,
    '-q:v',
    String(options.quality),
    resolve(root, 'poster.webp'),
  ]);
  if (poster.status !== 0) throw new Error(poster.stderr || 'ffmpeg poster extraction failed');
  const count = readdirSync(resolve(root, String(largest))).filter((name) =>
    /^f_\d{4}\.webp$/.test(name),
  ).length;
  const manifest = {
    version: 1,
    fps: options.fps,
    count,
    width: largest,
    height: Math.round((largest * source.height) / source.width / 2) * 2,
    pattern: 'f_%04d.webp',
    tiers: Object.fromEntries(options.tiers.map((tier) => [String(tier), `${tier}/`])),
    poster: 'poster.webp',
  };
  writeFileSync(resolve(root, 'frames.json'), `${JSON.stringify(manifest, null, 2)}\n`);
  return 0;
}
function main() {
  printMediaNotice();
  let parsed;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    return 1;
  }
  try {
    return extract(parsed);
  } catch (error) {
    console.error(error.message);
    return 1;
  }
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) process.exitCode = main();
