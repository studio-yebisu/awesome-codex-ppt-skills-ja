import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './fold-to-rail.js';

const scenario = {
  beats: [
    { id: 'a', type: 'quote', data: { text: 'hello', by: 'me' } },
    { id: 'b', type: 'chronology', data: { events: [{ date: '2024', title: 'event' }] } },
  ],
  rects: {
    'a.block': { x: 300, y: 180, w: 400, h: 200 },
    'b.track': { x: 100, y: 500, w: 900, h: 4 },
    'b.stem': { x: 200, y: 400, w: 3, h: 100 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 1.4 } },
  carry: (h, ctx) => ctx.overlay.querySelector('[data-sl-rect]'),
};
describe('fold-to-rail', () => {
  it('meets the link contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
});
