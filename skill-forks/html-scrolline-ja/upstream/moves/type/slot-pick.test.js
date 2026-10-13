import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './slot-pick.js';
const scenario = {
  beats: [{ id: 't', type: 'text', data: { text: 'hello world', parts: { word: true } } }],
  rects: { 't.word#0': { x: 40, y: 30, w: 50, h: 20 }, 't.word#1': { x: 95, y: 30, w: 50, h: 20 } },
  run: {
    role: 'enter',
    beat: 't',
    params: {
      word: 0,
      candidates: [
        { word: 'hello', p: 70 },
        { word: 'hi', p: 30 },
      ],
      duration: 2,
      speed: 1,
      candsAt: 0.42,
    },
  },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('places cands at the requested relative time', () =>
  expect(move.timing(scenario.run.params).stops).toEqual([{ name: 'cands', at: 0.84 }]));
