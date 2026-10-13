import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './mask-word-in.js';
const scenario = {
  beats: [{ id: 'm', type: 'video', data: { mask: { text: 'RISE' } } }],
  rects: { 'm.media': { x: 0, y: 0, w: 500, h: 200 }, 'm.caption': { x: 0, y: 0, w: 100, h: 20 } },
  run: {
    role: 'enter',
    beat: 'm',
    params: {
      duration: 1.2,
      riseFrom: 100,
      brightFrom: 0.7,
      brightTo: 1.15,
      scaleFrom: 1,
      trackFrom: 1,
      captionIn: true,
    },
  },
};
it('meets the move contract and masks at the start', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  const r = h.runMove(move, scenario.run);
  h.seek(0);
  expect(r.ctx.beat.part('media')[0].style.maskImage).toContain('data:image/svg+xml');
  h.seek(r.timing.duration);
  expect(r.ctx.gsap.getProperty(r.ctx.beat.part('media')[0], 'filter')).toContain('1.15');
  h.destroy();
});
