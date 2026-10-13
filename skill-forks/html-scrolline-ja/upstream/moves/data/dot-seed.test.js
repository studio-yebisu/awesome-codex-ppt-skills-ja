import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './dot-seed.js';

const scenario = {
  beats: [{ id: 'c', type: 'chart', data: { parts: { plot: 1, mark: 1, note: 1, title: 1, source: 1 } } }],
  rects: { 'c.mark': { x: 692, y: 576, w: 40, h: 40 }, 'c.note': { x: 176, y: 142, w: 300, h: 40 } },
  run: { role: 'enter', beat: 'c', params: { duration: 1.2, gap: 44 } },
};
it('meets the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('moves the note beside the dot, vertically centred on it', () => {
  const h = createHarness(scenario);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  const note = h.beats.get('c').part('note')[0];
  expect(Number(r.ctx.gsap.getProperty(note, 'x'))).toBeCloseTo(692 + 40 + 44 - 176);
  expect(Number(r.ctx.gsap.getProperty(note, 'y'))).toBeCloseTo(596 - 20 - 142);
  h.destroy();
});
