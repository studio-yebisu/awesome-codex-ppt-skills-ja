import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './iris-to-dot.js';

const scenario = {
  beats: [
    { id: 'a', type: 'video', data: { parts: { caption: 1 } } },
    { id: 'b', type: 'chart', data: { parts: { plot: 1 } } },
  ],
  rects: { 'a.frame': { x: 0, y: 0, w: 1920, h: 1080 }, 'b.mark#0': { x: 692, y: 576, w: 40, h: 40 } },
  run: { role: 'link', from: 'a', beat: 'b', params: { focusX: 0.5, focusY: 0.5 } },
  carry: null,
};
scenario.nodes = (_h, ctx) => [ctx.handoff.from.node, ctx.handoff.to.node];
it('meets the iris link contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('moves the light, not a scaled frame, onto the mark centre', () => {
  const h = createHarness(scenario);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration * 0.85);
  const frame = r.ctx.handoff.from.node;
  expect(Number(r.ctx.gsap.getProperty(frame, 'x'))).toBeCloseTo(712 - 960);
  expect(Number(r.ctx.gsap.getProperty(frame, 'y'))).toBeCloseTo(596 - 540);
  expect(Number(r.ctx.gsap.getProperty(frame, 'scaleX'))).toBe(1);
  h.destroy();
});
