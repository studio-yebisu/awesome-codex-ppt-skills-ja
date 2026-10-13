import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './line-draw.js';
const scenario = {
  beats: [
    {
      id: 'c',
      type: 'chart',
      data: {
        categories: ['A', 'B'],
        series: [{ name: 'One', values: [1, 2] }],
        parts: { plot: true, axis: true, label: true, mark: true, source: true },
      },
    },
  ],
  rects: { 'c.mark#0': { x: 0, y: 0, w: 10, h: 10 }, 'c.mark#1': { x: 100, y: 50, w: 10, h: 10 } },
  run: { role: 'enter', beat: 'c', params: { duration: 1.8, headLabels: true, markPop: false } },
  prepare(h) {
    const beat = h.beats.get('c'),
      old = beat.part('mark')[0],
      node = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    old.replaceWith(node);
    beat.parts.mark[0] = node;
    node.setAttribute('d', 'M 0 0 L 100 50');
    node.dataset.series = '0';
  },
};
it('passes contract and creates a line-head label without path measurement APIs', () => {
  expect(
    checkMove(
      move,
      { ...scenario, run: { ...scenario.run, params: { ...scenario.run.params, headLabels: false } } },
      createHarness,
    ),
  ).toEqual([]);
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  h.seek(0.5 * r.timing.duration);
  expect(r.ctx.overlay.querySelector('span').textContent).toBe('One');
  expect(move.build.toString()).not.toContain('getPointAtLength');
  h.destroy();
});
