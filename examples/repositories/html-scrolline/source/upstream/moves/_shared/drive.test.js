import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { driveValue } from './drive.js';
import { scrubTo } from './media.js';

const move = (build) => ({
  id: 'drive-test',
  family: 'media',
  role: 'enter',
  accepts: ['*'],
  sources: ['x'],
  reduce: 'self',
  params: {},
  timing: () => ({ duration: 3 }),
  build,
});

// 회귀(launch 통합): onUpdate는 seek()·pause(t)에서 안 불려 정지점 점프 때 제품 프레임이 0에 머물렀다.
it('applies the tweened value on seek with events suppressed, both directions', () => {
  const h = createHarness({ beats: [{ id: 'a', type: 'text', data: {} }] });
  const seen = [];
  h.runMove(
    move((tl) => {
      tl.to({}, { duration: 3 }, 0);
      driveValue(tl, (v) => seen.push(Math.round(v * 100) / 100), { from: 0.1, to: 0.5, at: 1, duration: 1, ease: 'none' });
    }),
    { role: 'enter', beat: 'a' },
  );
  h.seek(3);
  expect(seen.at(-1)).toBe(0.5);
  h.seek(1.5);
  expect(seen.at(-1)).toBe(0.3);
  h.seek(0);
  expect(seen.at(-1)).toBe(0.1);
  h.destroy();
});

it('scrubTo drives the frame sequence on a jump', () => {
  const h = createHarness({ beats: [{ id: 'a', type: 'text', data: {} }] });
  const calls = [];
  const seq = { setProgress: (p) => calls.push(Math.round(p * 100) / 100) };
  h.runMove(move((tl) => scrubTo(tl, seq, { from: 0, to: 0.8, at: 0, duration: 2 })), { role: 'enter', beat: 'a' });
  h.seek(1);
  expect(calls.at(-1)).toBe(0.4);
  h.seek(2.5);
  expect(calls.at(-1)).toBe(0.8);
  h.destroy();
});
