import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './window-takeover.js';
const scenario = {
  beats: [{ id: 'm', type: 'photo', data: {} }],
  rects: {
    'm.frame': { x: 0, y: 0, w: 400, h: 200 },
    'm.media': { x: 0, y: 0, w: 400, h: 200 },
    'm.caption': { x: 0, y: 0, w: 100, h: 20 },
  },
  run: { role: 'step', beat: 'm', params: { duration: 1.2 } },
};
const layout = (node, box) => {
  for (const [key, value] of Object.entries(box)) Object.defineProperty(node, key, { value, configurable: true });
};
it('meets the move contract', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
});
it('grows the window from its tile slot until it covers the tile, and rewinds', () => {
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  const [frame] = h.beats.get('m').part('frame');
  layout(frame, { offsetLeft: 262, offsetTop: 238, offsetWidth: 1396, offsetHeight: 785 });
  const r = h.runMove(move, scenario.run);
  const get = (prop) => Number(r.ctx.gsap.getProperty(frame, prop));
  h.seek(r.timing.duration);
  expect(get('scale')).toBeGreaterThan(1920 / 1396);
  expect(get('x')).toBeCloseTo(960 - (262 + 698));
  expect(get('y')).toBeCloseTo(540 - (238 + 392.5));
  h.seek(0);
  expect(get('scale')).toBe(1);
  h.destroy();
});
