import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './into-word.js';
const scenario = {
  beats: [
    { id: 'a', type: 'video', data: {} },
    { id: 'b', type: 'text', data: { parts: { word: true } } },
  ],
  rects: { 'a.frame': { x: 0, y: 0, w: 400, h: 200 }, 'b.word#0': { x: 200, y: 300, w: 80, h: 30 } },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 1.6, word: 0 } },
  // the frame is clipped in place onto the word (no carried copy), so no carry rect to compare
  carry: null,
};
it('meets the link contract and lands on the target word', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(r.ctx.handoff.to.node.style.visibility).not.toBe('hidden');
  expect(r.ctx.overlay.querySelector('.sl-into-word__fill').style.visibility).toBe('hidden');
  h.destroy();
});
