import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './dots-pour.js';

export const scenario = {
  beats: [
    {
      id: 'a',
      type: 'chart',
      data: {
        series: [{ values: [10] }],
        states: [{ name: 'x', series: [{ values: [180] }] }],
        parts: { plot: 1, mark: 1, title: 1 },
      },
    },
    {
      id: 'b',
      type: 'chart',
      data: { categories: ['a', 'b'], unit: '대', series: [{ values: [5, 18] }], parts: { plot: 1, title: 1 } },
    },
  ],
  rects: {
    'a.mark': { x: 700, y: 500, w: 40, h: 40 },
    'b.mark#0': { x: 300, y: 700, w: 80, h: 100 },
    'b.mark#1': { x: 500, y: 400, w: 80, h: 400 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 2.4, toIndex: -1 } },
  carry: null,
  prepare: (h) =>
    h.beats.get('b').part('mark').forEach((m, i) => {
      for (const [k, v] of Object.entries({ x: 300 + 200 * i, y: i ? 400 : 700, width: 80, height: i ? 400 : 100 })) m.setAttribute(k, String(v));
    }),
};
it('meets the link contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('grows the other bars from zero and tags the target value', () => {
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  const other = h.beats.get('b').part('mark')[0];
  h.seek(0.1);
  expect(Number(other.getAttribute('height'))).toBe(0);
  h.seek(r.timing.duration);
  expect(Number(other.getAttribute('height'))).toBe(100);
  expect(Number(other.getAttribute('y'))).toBe(700);
  expect(r.ctx.overlay.textContent).toContain('18대');
  h.destroy();
});
