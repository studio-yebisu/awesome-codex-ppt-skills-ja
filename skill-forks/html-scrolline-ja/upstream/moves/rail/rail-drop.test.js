import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './rail-drop.js';

const scenario = {
  beats: [
    { id: 'a', type: 'photo', data: {} },
    { id: 'b', type: 'chronology', data: { events: [{ date: '2024', title: 'event' }] } },
  ],
  rects: {
    'a.frame': { x: 400, y: 80, w: 500, h: 300 },
    'b.media': { x: 100, y: 500, w: 120, h: 80 },
    'b.stem': { x: 120, y: 400, w: 3, h: 90 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 1.6 } },
  carry: (h, ctx) => ctx.overlay.querySelector('[data-sl-rect]'),
};
describe('rail-drop', () => {
  it('meets the link contract and arcs the carried frame', () => {
    expect(checkMove(move, scenario, createHarness)).toEqual([]);
  });
});
