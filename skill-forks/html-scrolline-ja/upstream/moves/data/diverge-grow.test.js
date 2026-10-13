import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './diverge-grow.js';

const scenario = {
  beats: [{ id: 'c', type: 'chart', data: { categories: ['w', 'e'], unit: '%', series: [{ values: [-8, 30] }], parts: { plot: 1, title: 1, label: 1 } } }],
  rects: {
    'c.plot': { x: 100, y: 170, w: 1600, h: 900 },
    'c.mark#0': { x: 160, y: 800, w: 200, h: 80 },
    'c.mark#1': { x: 1460, y: 330, w: 200, h: 470 },
  },
  prepare(h) {
    const marks = h.beats.get('c').part('mark');
    Object.assign(marks[0].dataset, { index: '0', series: '0', sign: 'neg' });
    Object.assign(marks[1].dataset, { index: '1', series: '0', sign: 'pos' });
    for (const [k, v] of Object.entries({ x: 160, y: 705, width: 44, height: 55 })) marks[0].setAttribute(k, String(v));
    for (const [k, v] of Object.entries({ x: 1460, y: 160, width: 44, height: 545 })) marks[1].setAttribute(k, String(v));
  },
  run: { role: 'enter', beat: 'c', params: { duration: 2 } },
};
it('passes contract and starts negative bars first', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  h.seek(0.85);
  const marks = h.beats.get('c').part('mark');
  expect(Number(marks[0].getAttribute('height')) / 55).toBeGreaterThan(Number(marks[1].getAttribute('height')) / 545);
  h.seek(r.timing.duration);
  expect(Number(marks[0].getAttribute('y'))).toBe(705);
  expect(Number(marks[1].getAttribute('height'))).toBe(545);
  h.destroy();
});
