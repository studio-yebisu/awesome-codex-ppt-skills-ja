// @vitest-environment node
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { describe, expect, it } from 'vitest';
import { ffmpegAvailable, parseArgs } from './extract-frames.mjs';

describe('extract-frames arguments', () => {
  it('parses documented extraction options', () => {
    expect(
      parseArgs([
        'in.mp4',
        'frames',
        '--fps',
        '12',
        '--tiers',
        '1280,640',
        '--quality',
        '80',
        '--from',
        '1',
        '--to',
        '2',
      ]),
    ).toEqual({
      input: 'in.mp4',
      outDir: 'frames',
      options: { fps: 12, tiers: [1280, 640], quality: 80, from: 1, to: 2 },
    });
  });
  it('rejects invalid and incomplete options', () => {
    expect(() => parseArgs(['in.mp4'])).toThrow(/usage/);
    expect(() => parseArgs(['in.mp4', 'out', '--fps', '0'])).toThrow(/invalid/);
  });
  it('exits 2 when ffmpeg is unavailable', () => {
    const result = spawnSync(process.execPath, ['tools/media/extract-frames.mjs', 'in.mp4', 'out'], {
      cwd: process.cwd(),
      env: { ...process.env, PATH: '/missing-ffmpeg' },
    });
    expect(result.status).toBe(2);
  });
  it.skipIf(!ffmpegAvailable())('extracts a real two-second synthetic video and writes the manifest', () => {
    const root = mkdtempSync(join(tmpdir(), 'scrolline-e6-'));
    try {
      const input = join(root, 'source.mp4');
      const out = join(root, 'frames');
      expect(
        spawnSync('ffmpeg', [
          '-f',
          'lavfi',
          '-i',
          'color=c=black:s=64x36:d=2',
          '-pix_fmt',
          'yuv420p',
          input,
          '-y',
        ]).status,
      ).toBe(0);
      expect(
        spawnSync(process.execPath, [
          'tools/media/extract-frames.mjs',
          input,
          out,
          '--fps',
          '2',
          '--tiers',
          '64,32',
          '--quality',
          '78',
        ]).status,
      ).toBe(0);
      const manifest = JSON.parse(readFileSync(join(out, 'frames.json'), 'utf8'));
      expect(manifest).toMatchObject({ version: 1, fps: 2, pattern: 'f_%04d.webp', poster: 'poster.webp' });
      // 2초 × 2fps = 4장. 1장이면 ffmpeg가 애니메이션 webp 한 파일로 묶은 것.
      expect(manifest.count).toBeGreaterThanOrEqual(4);
      expect(existsSync(join(out, '64', 'f_0004.webp'))).toBe(true);
      expect(existsSync(join(out, '64', 'f_0001.webp'))).toBe(true);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
