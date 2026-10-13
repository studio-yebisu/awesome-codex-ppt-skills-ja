import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './word-door.js';
const scenario = {
  beats: [{ id: 'm', type: 'video', data: { mask: { text: 'AI' } } }],
  rects: { 'm.media': { x: 0, y: 0, w: 400, h: 200 } },
  run: { role: 'step', beat: 'm', params: { duration: 2.4, split: -1 } },
};
it('meets the move contract and ends unmasked', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(h.beats.get('m').part('media')[0].style.maskImage).toBe('none');
  h.destroy();
});
