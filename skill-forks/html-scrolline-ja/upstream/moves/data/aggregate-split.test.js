import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './aggregate-split.js';

export const scenario = {
  beats: [
    {
      id: 'c',
      type: 'chart',
      data: { categories: ['a', 'b', 'c'], unit: '만', series: [{ values: [60, 30, 10] }], highlight: { index: 0 }, parts: { plot: 1, title: 1, label: 1 } },
    },
  ],
  rects: {
    'c.plot': { x: 100, y: 170, w: 1600, h: 900 },
    'c.mark#0': { x: 160, y: 330, w: 200, h: 600 },
    'c.mark#1': { x: 810, y: 630, w: 200, h: 300 },
    'c.mark#2': { x: 1460, y: 830, w: 200, h: 100 },
  },
  prepare: (h) => h.beats.get('c').part('mark').forEach((m, i) => Object.assign(m.dataset, { index: String(i), series: '0' })),
  run: { role: 'enter', beat: 'c', params: { duration: 2.4 } },
};
it('passes the contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('stacks pieces to the plot height, then lands each on its own bar', () => {
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  const pieces = [...r.ctx.overlay.children].filter((n) => n.tagName === 'I');
  const total = pieces.reduce((s, n) => s + parseFloat(n.style.height), 0);
  expect(total).toBeCloseTo(600);
  h.seek(r.timing.duration * 0.89);
  expect(parseFloat(pieces[0].style.left)).toBeCloseTo(160);
  expect(parseFloat(pieces[0].style.height)).toBeCloseTo(600);
  h.seek(r.timing.duration);
  expect(r.ctx.overlay.textContent).toContain('60만');
  h.destroy();
});
