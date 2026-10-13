import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move, { waffleGeom } from './line-to-waffle.js';

export const scenario = {
  beats: [
    {
      id: 'a',
      type: 'chart',
      data: {
        categories: ['x', 'y'],
        series: [{ values: [10, 20] }],
        states: [{ name: 's', series: [{ values: [5, 25] }] }],
        parts: { plot: 1, mark: 1, title: 1 },
      },
    },
    { id: 'b', type: 'chart', data: { categories: ['p', 'q'], unit: '%', series: [{ values: [25, 5] }], parts: { plot: 1, title: 1, dek: 1 } } },
  ],
  rects: { 'a.plot': { x: 100, y: 170, w: 1600, h: 900 }, 'b.plot': { x: 100, y: 170, w: 1600, h: 900 } },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 2 } },
  carry: null,
};
it('meets the link contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('lights as many cells as the end value', () => {
  const h = createHarness(scenario);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(r.ctx.overlay.querySelectorAll('.sl-data-cell')).toHaveLength(100);
  expect(r.ctx.overlay.dataset.litCells).toBe('25');
  const g = waffleGeom(h.beats.get('b'));
  expect(g.list[0]).toMatchObject({ x: 260, y: 330 });
  expect(g.pitch).toBe(60);
  h.destroy();
});
