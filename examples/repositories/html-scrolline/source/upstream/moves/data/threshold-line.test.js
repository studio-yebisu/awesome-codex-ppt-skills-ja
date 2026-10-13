import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './threshold-line.js';

export const scenario = {
  beats: [
    {
      id: 'c',
      type: 'chart',
      data: { orient: 'h', categories: ['a', '세계', '한국', 'b'], unit: '%', series: [{ values: [50, 25, 11, 30] }], parts: { plot: 1, title: 1 } },
    },
  ],
  rects: {
    'c.plot': { x: 100, y: 170, w: 1600, h: 900 },
    'c.mark#0': { x: 260, y: 340, w: 1300, h: 44 },
    'c.mark#1': { x: 260, y: 490, w: 650, h: 44 },
    'c.mark#2': { x: 260, y: 640, w: 286, h: 44 },
    'c.mark#3': { x: 260, y: 790, w: 780, h: 44 },
  },
  prepare: (h) => h.beats.get('c').part('mark').forEach((m, i) => Object.assign(m.dataset, { index: String(i), series: '0' })),
  run: { role: 'step', beat: 'c', step: { name: 'world', index: 0 }, params: { refIndex: 1, focusIndex: 2, duration: 1.8 } },
};
it('passes the contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('draws the rule at the reference value and labels it', () => {
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  const rule = r.ctx.overlay.querySelector('path');
  expect(rule.getAttribute('d')).toMatch(/^M 910 /);
  expect(r.ctx.overlay.textContent).toContain('세계 25%');
  h.destroy();
});
