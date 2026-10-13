import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move, { seriesTone } from './ink-in.js';

const data = {
  categories: ['A', 'B', 'C'],
  unit: '%',
  highlight: { series: 'kr' },
  series: [
    { name: 'kr', values: [1, 2, 3] },
    { name: 'w', values: [2, 3, 4] },
  ],
  parts: { plot: 1, axis: 1, mark: 1, label: 1, title: 1 },
};
const scenario = {
  beats: [{ id: 'c', type: 'chart', data }],
  rects: { 'c.plot': { x: 100, y: 170, w: 1600, h: 900 } },
  run: { role: 'enter', beat: 'c', params: { duration: 2, upto: 1 } },
};
it('passes the contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('inks only up to upto and tags each series end', () => {
  const h = createHarness(scenario);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(r.ctx.overlay.querySelectorAll('circle')).toHaveLength(4);
  expect(r.ctx.overlay.textContent).toContain('kr 2%');
  expect(seriesTone(data, 0)).toBe('accent');
  expect(seriesTone(data, 1)).toBe('accent-2');
  h.destroy();
});
