import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move, { morphPoints } from './mark-morph.js';

const data = {
  kind: 'bar',
  categories: ['a', 'b', 'c'],
  series: [{ name: 's', values: [10, 20, 40] }],
  states: [{ name: 'share', kind: 'line', unit: '%', series: [{ name: 'p', values: [1, 2, 4] }], notes: [{ index: 2, text: '4%' }] }],
  parts: { plot: 1, title: 1, unit: 1 },
};
export const scenario = {
  beats: [{ id: 'c', type: 'chart', data }],
  rects: {
    'c.plot': { x: 100, y: 170, w: 1600, h: 900 },
    'c.mark#0': { x: 240, y: 780, w: 40, h: 150 },
    'c.mark#1': { x: 890, y: 630, w: 40, h: 300 },
    'c.mark#2': { x: 1540, y: 330, w: 40, h: 600 },
    'c.note': { x: 1560, y: 310, w: 60, h: 30 },
  },
  prepare(h) {
    const beat = h.beats.get('c');
    beat.part('mark').forEach((m, i) => Object.assign(m.dataset, { index: String(i), series: '0' }));
    Object.assign(beat.part('note')[0].dataset, { index: '2', series: '0', state: 'share' });
  },
  run: { role: 'step', beat: 'c', step: { name: 'share', index: 1 }, params: { duration: 2.4 } },
};
it('passes the contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('lands the line points on the new state scale and folds the bars away', () => {
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  const pts = morphPoints(h.beats.get('c'), data.states[0]);
  expect(pts.map((p) => p.y)).toEqual([780, 630, 330]);
  h.seek(r.timing.duration);
  const dots = [...r.ctx.overlay.querySelectorAll('circle')];
  expect(dots.map((c) => Number(c.getAttribute('cy')))).toEqual([780, 630, 330]);
  expect(h.beats.get('c').part('mark').every((m) => Number(r.ctx.gsap.getProperty(m, 'opacity')) === 0)).toBe(true);
  h.destroy();
});
