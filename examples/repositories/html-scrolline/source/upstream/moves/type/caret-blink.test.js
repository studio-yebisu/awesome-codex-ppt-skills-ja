import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './caret-blink.js';
const scenario = {
  beats: [{ id: 't', type: 'text', data: { text: 'one two', parts: { word: true } } }],
  rects: { 't.word#0': { x: 10, y: 10, w: 30, h: 20 }, 't.word#1': { x: 45, y: 10, w: 30, h: 20 } },
  run: { role: 'ambient', beat: 't', params: { period: 0.4 } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('has fill timing and reduced fixed visibility', () => {
  const h = createHarness({ ...scenario, reduce: true }),
    r = h.runMove(move, scenario.run);
  h.seek(0.8);
  expect(r.timing.duration).toBe(1);
  expect(Number(r.ctx.gsap.getProperty(r.ctx.overlay.firstElementChild, 'opacity'))).toBe(1);
  h.destroy();
});
