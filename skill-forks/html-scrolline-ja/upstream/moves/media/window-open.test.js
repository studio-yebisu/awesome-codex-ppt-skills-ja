import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './window-open.js';
const scenario = {
  beats: [{ id: 'm', type: 'photo', data: {} }],
  rects: {
    'm.frame': { x: 0, y: 0, w: 400, h: 200 },
    'm.media': { x: 0, y: 0, w: 400, h: 200 },
    'm.caption': { x: 0, y: 0, w: 100, h: 20 },
  },
  run: { role: 'enter', beat: 'm', params: { duration: 1.4, shape: 'box', scrim: true } },
};
it('meets the move contract and opens both shapes', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  for (const shape of ['line', 'box']) {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
    const r = h.runMove(move, { ...scenario.run, params: { duration: 1.4, shape } });
    h.seek(r.timing.duration);
    expect(r.ctx.beat.part('frame')[0].style.clipPath).toContain('inset(0%');
    h.destroy();
  }
});
