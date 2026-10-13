import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move, { plotBox, pointAt, rangeOf } from './annotation-pin.js';

const data = {
  categories: ['a', 'b', 'c'],
  series: [{ name: 's', values: [10, 20, 30] }],
  highlight: { index: 2 },
  states: [
    {
      name: 'steps',
      notes: [
        { index: 1, text: '+10' },
        { index: 2, text: '+10' },
      ],
    },
  ],
  parts: { plot: 1, title: 1 },
};
const rects = {
  'c.plot': { x: 100, y: 170, w: 1600, h: 900 },
  'c.mark#0': { x: 240, y: 730, w: 40, h: 200 },
  'c.mark#1': { x: 890, y: 530, w: 40, h: 400 },
  'c.mark#2': { x: 1540, y: 330, w: 40, h: 600 },
  'c.note#0': { x: 900, y: 500, w: 80, h: 30 },
  'c.note#1': { x: 1550, y: 300, w: 80, h: 30 },
};
const prepare = (h) => {
  const beat = h.beats.get('c');
  beat.part('mark').forEach((m, i) => Object.assign(m.dataset, { index: String(i), series: '0' }));
  beat.part('note').forEach((n, i) => Object.assign(n.dataset, { index: String(i + 1), series: '0', state: 'steps' }));
};
const scenario = (shape) => ({
  beats: [{ id: 'c', type: 'chart', data }],
  rects,
  prepare,
  run: { role: 'step', beat: 'c', step: { name: 'steps', index: 0 }, params: { shape, duration: 1.8 } },
});
it('passes the contract in every shape', () => {
  for (const shape of ['pin', 'stairs', 'gap']) expect(checkMove(move, scenario(shape), createHarness)).toEqual([]);
});
it('reveals the state notes beside their marks and draws one riser per note', () => {
  const s = scenario('stairs');
  const h = createHarness(s);
  s.prepare(h);
  const r = h.runMove(move, s.run);
  h.seek(r.timing.duration);
  const notes = h.beats.get('c').part('note');
  expect(notes.every((n) => Number(r.ctx.gsap.getProperty(n, 'opacity')) === 1)).toBe(true);
  expect(r.ctx.overlay.querySelectorAll('path')).toHaveLength(2);
  h.destroy();
});
it('maps values onto the renderer box', () => {
  const h = createHarness(scenario('pin'));
  const beat = h.beats.get('c');
  expect(plotBox(beat)).toMatchObject({ x: 260, y: 330, w: 1300, h: 600 });
  expect(rangeOf(data.series)).toEqual({ min: 0, max: 30 });
  expect(pointAt(beat, 2, 30)).toEqual({ x: 1560, y: 330 });
  h.destroy();
});
