import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './forecast-extend.js';

const scenario = {
  beats: [
    {
      id: 'c',
      type: 'chart',
      data: { categories: ['A', 'B', 'C'], unit: '%', series: [{ name: 'x', values: [10, 20, 30] }], parts: { plot: 1, label: 1, title: 1 } },
    },
  ],
  rects: { 'c.plot': { x: 100, y: 170, w: 1600, h: 900 } },
  run: { role: 'step', beat: 'c', step: { name: 'forecast', index: 0 }, params: { duration: 1.8, fromIndex: 1 } },
};
it('passes the contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('dashes from the last observed point to the forecast and tags it', () => {
  const h = createHarness(scenario);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  const dash = r.ctx.overlay.querySelector('path[mask]');
  expect(dash.getAttribute('d')).toBe('M 910 530 L 1560 330');
  expect(r.ctx.overlay.textContent).toContain('30%');
  h.destroy();
});
