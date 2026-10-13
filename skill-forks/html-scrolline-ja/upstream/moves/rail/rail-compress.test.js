import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './rail-compress.js';
import { checkMove } from '../_shared/contract-check.js';
const scenario = {
  beats: [
    { id: 'a', type: 'chronology', data: { events: [{ date: '2020', title: 'A' }] } },
    {
      id: 'b',
      type: 'chronology',
      data: {
        events: [
          { date: '2020', title: 'B', weight: 'major' },
          { date: '2021', title: 'C', weight: 'minor' },
        ],
      },
    },
  ],
  rects: {
    'a.track': { x: 0, y: 0, w: 100, h: 10 },
    'b.track': { x: 100, y: 0, w: 100, h: 10 },
    'b.dot#0': { x: 120, y: 0, w: 10, h: 10 },
    'b.dot#1': { x: 200, y: 0, w: 10, h: 10 },
    'b.stem#0': { x: 120, y: 0, w: 10, h: 10 },
    'b.stem#1': { x: 200, y: 0, w: 10, h: 10 },
    'b.title#0': { x: 120, y: 0, w: 10, h: 10 },
    'b.title#1': { x: 200, y: 0, w: 10, h: 10 },
    'b.label': { x: 0, y: 0, w: 10, h: 10 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 2.4, startZoom: 8 } },
  nodes: () => [],
};
describe('rail-compress', () => {
  it('passes contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('settles track scale to one', () => {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
    const r = h.runMove(move, scenario.run);
    h.seek(r.timing.duration);
    expect(Number(r.ctx.gsap.getProperty(h.beats.get('b').part('track')[0], 'scaleX'))).toBe(1);
    h.destroy();
  });
});
