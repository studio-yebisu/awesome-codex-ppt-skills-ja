import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move, { dotCount, unitGrid } from './dot-multiply.js';

const data = {
  categories: ['2012'],
  series: [{ name: 's', values: [119000] }],
  states: [{ name: 'x178', series: [{ name: 's', values: [21200000] }] }],
  parts: { plot: 1, mark: 1, title: 1, note: 1 },
};
const scenario = {
  beats: [{ id: 'c', type: 'chart', data }],
  rects: { 'c.mark': { x: 692, y: 576, w: 40, h: 40 } },
  run: { role: 'step', beat: 'c', step: { name: 'x178', index: 0 }, params: { duration: 2.4, cols: 18 } },
};
it('meets the move contract without a canvas context', () =>
  expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('counts dots as state value over base value', () => {
  expect(dotCount(data, data.states[0])).toBe(178);
});
it('lays the first n cells row-major around the seed cell', () => {
  const cells = unitGrid({ x: 0, y: 0 }, 178, { cols: 18, pitch: 10 });
  expect(cells).toHaveLength(178);
  expect(cells.find((c) => c.d === 0)).toMatchObject({ x: 0, y: 0 });
  expect(cells.at(-1)).toMatchObject({ x: 70, y: 50 });
});
it('ends the counter on n', () => {
  const h = createHarness(scenario);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(r.ctx.overlay.textContent).toContain('178');
  h.destroy();
});
