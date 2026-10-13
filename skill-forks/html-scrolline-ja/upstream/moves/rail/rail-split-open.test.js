import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './rail-split-open.js';

const scenario = {
  beats: [
    { id: 'a', type: 'chronology', data: { events: [{ date: '2024', title: 'event' }], now: 0.5 } },
    { id: 'b', type: 'photo', data: {} },
  ],
  rects: {
    'a.track': { x: 100, y: 500, w: 900, h: 4 },
    'a.now': { x: 550, y: 450, w: 2, h: 80 },
    'b.frame': { x: 0, y: 0, w: 1920, h: 1080 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 1.5 } },
  carry: null,
};
describe('rail-split-open', () => {
  it('meets the opening link contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
});
