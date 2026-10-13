import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './rank-reorder.js';

const scenario = {
  beats: [
    { id: 'a', type: 'chart', data: { categories: ['중국', '유럽'], highlight: { index: 0 }, series: [{ values: [9, 3] }], parts: { plot: 1, label: 1, title: 1 } } },
    {
      id: 'b',
      type: 'chart',
      data: { orient: 'h', categories: ['노르웨이', '중국', '유럽'], highlight: { index: 1 }, unit: '%', series: [{ values: [97, 53, 28] }], parts: { plot: 1, label: 1, title: 1 } },
    },
  ],
  rects: {
    'a.plot': { x: 100, y: 170, w: 1600, h: 900 },
    'a.mark#0': { x: 300, y: 330, w: 200, h: 600 },
    'a.mark#1': { x: 1200, y: 730, w: 200, h: 200 },
    'b.plot': { x: 100, y: 170, w: 1600, h: 900 },
    'b.mark#0': { x: 260, y: 340, w: 1260, h: 44 },
    'b.mark#1': { x: 260, y: 400, w: 690, h: 44 },
    'b.mark#2': { x: 260, y: 460, w: 360, h: 44 },
  },
  prepare: (h) =>
    ['a', 'b'].forEach((id) =>
      h.beats.get(id).part('mark').forEach((m, i) => {
        Object.assign(m.dataset, { index: String(i), series: '0' });
        for (const [k, v] of Object.entries({ x: 160, y: 180 + 60 * i, width: 1000 - 300 * i, height: 44 })) m.setAttribute(k, String(v));
      }),
    ),
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 2.4 } },
  carry: null,
};
it('meets the link contract and hands China over by name', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  expect(move.handoff({ matchBy: 'label' }, { from: scenario.beats[0].data, to: scenario.beats[1].data })).toEqual({
    from: { part: 'mark', index: 0 },
    to: { part: 'mark', index: 1 },
  });
});
it('walks matched bars as ghosts and grows the unmatched one', () => {
  const h = createHarness(scenario);
  scenario.prepare(h);
  const r = h.runMove(move, scenario.run);
  const norway = h.beats.get('b').part('mark')[0];
  h.seek(0.2);
  expect(Number(norway.getAttribute('width'))).toBe(0);
  h.seek(r.timing.duration * 0.85);
  const ghost = [...r.ctx.overlay.children].find((n) => n.tagName === 'I');
  expect(parseFloat(ghost.style.top)).toBeCloseTo(400);
  h.seek(r.timing.duration);
  expect(Number(norway.getAttribute('width'))).toBe(1000);
  h.destroy();
});
