import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './glyph-to-bar.js';

export const scenario = {
  beats: [
    { id: 'a', type: 'video', data: { parts: { caption: 1, media: 1 } } },
    { id: 'b', type: 'chart', data: { orient: 'h', unit: '%', categories: ['v', 'k'], highlight: { index: 0 }, series: [{ values: [160, 70] }], parts: { plot: 1, title: 1 } } },
  ],
  rects: {
    'a.frame': { x: 0, y: 0, w: 1920, h: 1080 },
    'b.mark#0': { x: 260, y: 340, w: 1300, h: 44 },
    'b.mark#1': { x: 260, y: 400, w: 560, h: 44 },
  },
  prepare: (h) => h.beats.get('b').part('mark').forEach((m, i) => Object.assign(m.dataset, { index: String(i), series: '0' })),
  run: { role: 'link', from: 'a', beat: 'b', params: { toIndex: 0 } },
  carry: null,
};
scenario.nodes = (_h, ctx) => [ctx.handoff.from.node, ctx.handoff.to.node];
it('meets the chart handoff contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('clips the media down to the target bar before it cools into the bar', () => {
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration * 0.62);
  expect(r.ctx.handoff.from.node.style.clipPath).toBe('inset(340px 360px 696px 260px)');
  h.destroy();
});
