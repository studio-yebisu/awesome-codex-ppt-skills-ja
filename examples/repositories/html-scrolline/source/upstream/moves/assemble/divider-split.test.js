import { afterEach, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './divider-split.js';

const scenario = {
  beats: [
    {
      id: 'compare',
      type: 'compare',
      data: {
        items: [
          { label: '기존', value: -1234, text: '낮은 비용' },
          { label: '제안', value: 5678, text: '높은 효율' },
        ],
        verdict: '제안이 우세하다',
        parts: { item: true, divider: true, value: true, text: true, verdict: true },
      },
    },
  ],
  rects: {
    'compare.item#0': { x: 180, y: 200, w: 220, h: 140 },
    'compare.item#1': { x: 1520, y: 200, w: 220, h: 140 },
    'compare.divider': { x: 959, y: 160, w: 2, h: 320 },
  },
  run: { role: 'enter', beat: 'compare', params: { duration: 1.4, count: true, spread: 0 } },
};
const harnesses = [];
afterEach(() => harnesses.splice(0).forEach((h) => h.destroy()));

it('passes the contract and finishes every compare part at rest', () =>
  expect(checkMove(move, scenario, createHarness)).toEqual([]));

it('uses the data preset shape and formats an in-flight count', () => {
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  harnesses.push(h);
  const run = h.runMove(move, scenario.run);
  h.seek(0);
  expect(Number(run.ctx.gsap.getProperty(h.beats.get('compare').part('item')[0], 'opacity'))).toBe(0);
  h.seek(0.55 * run.timing.duration);
  expect(h.beats.get('compare').part('value')[0].textContent).toMatch(/^-?\d{1,3}(,\d{3})*$/);
  h.seek(run.timing.duration);
  expect(h.beats.get('compare').part('value')[0].textContent).toBe('-1,234');
  expect(Number(run.ctx.gsap.getProperty(h.beats.get('compare').part('verdict')[0], 'opacity'))).toBe(1);
});
