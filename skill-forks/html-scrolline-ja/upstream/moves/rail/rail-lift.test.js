import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './rail-lift.js';

const scenario = (fromPart = 'media') => ({
  beats: [
    { id: 'a', type: 'chronology', data: { events: [{ date: '2024', title: 'event' }] } },
    { id: 'b', type: 'quote', data: { text: 'hello', by: 'me' } },
  ],
  rects: {
    [`a.${fromPart}`]: { x: 20, y: 100, w: 100, h: 60 },
    'a.stem': { x: 50, y: 140, w: 4, h: 80 },
    'b.block': { x: 500, y: 200, w: 300, h: 180 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 1.6, fromPart } },
  carry: (h, ctx) => ctx.overlay.querySelector('[data-sl-rect]'),
});
describe('rail-lift', () => {
  it('carries media, dot, and title to the target', () => {
    for (const part of ['media', 'dot', 'title'])
      expect(checkMove(move, scenario(part), createHarness)).toEqual([]);
  });
});
