import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './point-focus.js';
const scenario = {
  beats: [
    {
      id: 'c',
      type: 'chart',
      data: { highlight: { series: 0, index: 1 }, parts: { plot: true, mark: true, label: true } },
    },
  ],
  rects: { 'c.mark#0': { x: 0, y: 0, w: 1, h: 1 }, 'c.mark#1': { x: 1, y: 0, w: 1, h: 1 } },
  run: { role: 'step', beat: 'c', params: { duration: 1, index: -1 } },
  prepare(h) {
    h.beats
      .get('c')
      .part('mark')
      .forEach((n, i) => {
        n.dataset.index = String(i);
        n.dataset.series = '0';
      });
  },
};
it('passes contract and resolves index -1 from highlight', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(Number(r.ctx.gsap.getProperty(h.beats.get('c').part('mark')[1], 'scaleX'))).toBeCloseTo(1.8);
  h.destroy();
});
it('finds the highlighted point when the series is named and the line path is the first mark', () => {
  const named = {
    ...scenario,
    beats: [
      {
        id: 'c',
        type: 'chart',
        data: {
          series: [{ name: 'boxes', values: [1, 2, 3] }],
          highlight: { series: 'boxes', index: 2 },
          parts: { plot: true, mark: true, label: true },
        },
      },
    ],
    rects: {
      'c.mark#0': { x: 0, y: 0, w: 1, h: 1 },
      'c.mark#1': { x: 0, y: 0, w: 1, h: 1 },
      'c.mark#2': { x: 1, y: 0, w: 1, h: 1 },
      'c.mark#3': { x: 2, y: 0, w: 1, h: 1 },
    },
  };
  const h = createHarness(named);
  const marks = h.beats.get('c').part('mark');
  marks.forEach((n, i) => {
    n.dataset.index = i === 0 ? 'all' : String(i - 1);
    n.dataset.series = '0';
  });
  const r = h.runMove(move, named.run);
  h.seek(r.timing.duration);
  expect(Number(r.ctx.gsap.getProperty(marks[3], 'scaleX'))).toBeCloseTo(1.8);
  expect(Number(r.ctx.gsap.getProperty(marks[2], 'scaleX'))).toBeCloseTo(1);
  h.destroy();
});
