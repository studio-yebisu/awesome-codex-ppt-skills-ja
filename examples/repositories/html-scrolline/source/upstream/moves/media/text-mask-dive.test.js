import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './text-mask-dive.js';
const scenario = {
  beats: [{ id: 'm', type: 'video', data: { mask: { text: 'GO' } } }],
  rects: { 'm.media': { x: 0, y: 0, w: 400, h: 200 }, 'm.caption': { x: 0, y: 0, w: 100, h: 20 } },
  run: { role: 'step', beat: 'm', params: { duration: 1.4 } },
};
it('meets the move contract and clears its mask', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(r.ctx.beat.part('media')[0].style.maskImage).toBe('none');
  h.destroy();
});
