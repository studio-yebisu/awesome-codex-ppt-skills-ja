import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './rail-surface.js';
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
      },
    },
  ],
  rects: {
    'rail.event#0': { x: 0, y: 0, w: 10, h: 10 },
    'rail.event#1': { x: 100, y: 0, w: 10, h: 10 },
    'rail.now': { x: 0, y: 0, w: 2, h: 10 },
    'rail.label': { x: 0, y: 0, w: 10, h: 10 },
    'rail.counter': { x: 0, y: 0, w: 10, h: 10 },
  },
  run: { role: 'enter', beat: 'rail', params: { duration: 0.7, stagger: 0.04 } },
};
describe('rail-surface', () => {
  it('passes contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
});
