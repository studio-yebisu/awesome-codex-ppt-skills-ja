import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './waffle-recount.js';

const scenario = {
  beats: [
    {
      id: 'c',
      type: 'chart',
      data: { categories: ['신차', '도로'], unit: '%', series: [{ values: [25, 5] }], parts: { plot: 1, title: 1 } },
    },
  ],
  rects: { 'c.plot': { x: 100, y: 170, w: 1600, h: 900 } },
  run: { role: 'step', beat: 'c', step: { name: 'stock', index: 0 }, params: { index: 1, duration: 1.8 } },
};
it('meets the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('cools the cells between the two values and counts down to the new value', () => {
  const h = createHarness(scenario);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  const cells = [...r.ctx.overlay.querySelectorAll('.sl-data-cell')];
  expect(cells).toHaveLength(100);
  expect(cells.filter((c) => /inset/.test(c.style.boxShadow) && !/ 0px /.test(c.style.boxShadow))).toHaveLength(20);
  expect(r.ctx.overlay.querySelector('.sl-data-waffle-value').textContent).toBe('5%');
  h.destroy();
});
