import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './headline-to-caption.js';
const scenario = {
  beats: [
    { id: 'a', type: 'text', data: {} },
    { id: 'b', type: 'video', data: {} },
  ],
  rects: {
    'a.block': { x: 100, y: 100, w: 500, h: 100 },
    'b.frame': { x: 0, y: 0, w: 1200, h: 700 },
    'b.caption': { x: 760, y: 600, w: 180, h: 40 },
  },
  run: { role: 'link', from: 'a', beat: 'b' },
};
scenario.nodes = (_h, ctx) => [ctx.handoff.from.node, ctx.handoff.to.node];
it('uses uniform scale during the headline carry and meets the link contract', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration * 0.55);
  expect(Number(r.ctx.gsap.getProperty(r.ctx.handoff.from.node, 'scaleX'))).toBeCloseTo(
    Math.min(180 / 500, 40 / 100),
  );
  h.destroy();
});
