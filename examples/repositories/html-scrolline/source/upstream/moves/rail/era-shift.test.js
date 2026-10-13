import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './era-shift.js';
import { checkMove } from '../_shared/contract-check.js';
const datesA = [
    { date: '2019-01', title: 'A' },
    { date: '2020-01', title: 'B' },
  ],
  datesB = [{ date: '2021-01', title: 'C' }];
const scenario = {
  beats: [
    { id: 'a', type: 'chronology', data: { events: datesA, counter: 'year' } },
    { id: 'b', type: 'chronology', data: { events: datesB, counter: 'year' } },
  ],
  rects: {
    'a.track': { x: 0, y: 0, w: 100, h: 10 },
    'b.track': { x: 300, y: 0, w: 100, h: 10 },
    'a.ground': { x: 0, y: 0, w: 100, h: 100 },
    'b.ground': { x: 0, y: 0, w: 100, h: 100 },
    'a.label': { x: 0, y: 0, w: 10, h: 10 },
    'b.label': { x: 0, y: 0, w: 10, h: 10 },
    'a.counter': { x: 0, y: 0, w: 10, h: 10 },
    'b.counter': { x: 0, y: 0, w: 10, h: 10 },
    'b.stem': { x: 0, y: 0, w: 10, h: 10 },
    'b.title': { x: 0, y: 0, w: 10, h: 10 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 2, boundaryWidth: 2, labelTracking: 0.12 } },
  nodes: () => [],
  prepare(h) {
    for (const id of ['a', 'b']) {
      const counter = h.beats.get(id).part('counter')[0];
      for (let i = 0; i < 4; i += 1) {
        const col = document.createElement('span');
        col.dataset.place = String(i);
        counter.append(col);
      }
    }
  },
};
describe('era-shift', () => {
  it('passes contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('ends with B ground and label visible', () => {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
    scenario.prepare(h);
    const r = h.runMove(move, scenario.run);
    h.seek(r.timing.duration);
    expect(h.beats.get('b').part('ground')[0].style.clipPath).toMatch(/^inset\(0%? 0%? 0%? 0%?\)$/);
    expect(Number(r.ctx.gsap.getProperty(h.beats.get('b').part('label')[0], 'opacity'))).toBe(1);
    h.destroy();
  });
});
