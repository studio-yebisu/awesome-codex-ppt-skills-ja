import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './counter-handoff.js';

const scenario = (fromType = 'chronology') => ({
  beats:
    fromType === 'chronology'
      ? [
          { id: 'a', type: 'chronology', data: { events: [{ date: '2024-01', title: 'now' }] } },
          { id: 'b', type: 'number', data: { value: 12345 } },
        ]
      : [
          { id: 'a', type: 'number', data: { value: 12345 } },
          { id: 'b', type: 'chronology', data: { events: [{ date: '2024-01', title: 'now' }] } },
        ],
  rects: {
    'a.counter': { x: 20, y: 20, w: 80, h: 20 },
    'a.value': { x: 20, y: 20, w: 80, h: 20 },
    'b.value': { x: 400, y: 300, w: 300, h: 100 },
    'b.counter': { x: 400, y: 300, w: 80, h: 20 },
  },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 1.8 } },
  carry: (h, ctx) => ctx.overlay.querySelector('[data-sl-rect]'),
});
describe('counter-handoff', () => {
  it('meets the link contract in both directions', () => {
    expect(checkMove(move, scenario(), createHarness)).toEqual([]);
    expect(checkMove(move, scenario('number'), createHarness)).toEqual([]);
  });
});
