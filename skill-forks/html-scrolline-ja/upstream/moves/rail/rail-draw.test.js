import { afterEach, describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './rail-draw.js';
import { checkMove } from '../_shared/contract-check.js';
const scenario = {
  beats: [
    {
      id: 'rail',
      type: 'chronology',
      data: {
        events: [
          { date: '2020', title: 'A' },
          { date: '2021', title: 'B' },
        ],
        counter: 'year',
      },
    },
  ],
  rects: {
    'rail.track': { x: 0, y: 0, w: 100, h: 10 },
    'rail.now': { x: 100, y: 0, w: 2, h: 20 },
    'rail.tick#0': { x: 80, y: 0, w: 2, h: 2 },
    'rail.tick#1': { x: 300, y: 0, w: 2, h: 2 },
    'rail.dot#0': { x: 90, y: 0, w: 2, h: 2 },
    'rail.dot#1': { x: 310, y: 0, w: 2, h: 2 },
    'rail.stem': { x: 0, y: 0, w: 2, h: 40 },
    'rail.title': { x: 0, y: 0, w: 30, h: 10 },
    'rail.note': { x: 0, y: 0, w: 30, h: 10 },
    'rail.label': { x: 0, y: 0, w: 30, h: 10 },
    'rail.counter': { x: 0, y: 0, w: 30, h: 10 },
  },
  run: { role: 'enter', beat: 'rail', params: { duration: 1.4, stagger: 0.06 } },
};
const hs = [];
afterEach(() => hs.splice(0).forEach((h) => h.destroy()));
describe('rail-draw', () => {
  it('passes contract and starts/ends complete', () =>
    expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('reveals nearer tick first', () => {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
    hs.push(h);
    const r = h.runMove(move, scenario.run);
    h.seek(0.3);
    expect(Number(r.ctx.gsap.getProperty(r.ctx.beat.part('tick')[0], 'opacity'))).toBeGreaterThan(
      Number(r.ctx.gsap.getProperty(r.ctx.beat.part('tick')[1], 'opacity')),
    );
  });
});
