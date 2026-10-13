import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './line-focus.js';
const scenario = {
  beats: [{ id: 't', type: 'text', data: { text: 'a\nb', lines: ['a', 'b'], parts: { line: true } } }],
  rects: { 't.line#0': { x: 10, y: 10, w: 80, h: 20 }, 't.line#1': { x: 10, y: 40, w: 80, h: 20 } },
  run: { role: 'enter', beat: 't', params: { perLine: 1 } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('records one stop per line', () =>
  expect(move.timing({ perLine: 1 }, scenario.beats[0].data)).toEqual({
    duration: 2.1,
    stops: [
      { name: 'l1', at: 1 },
      { name: 'l2', at: 2 },
    ],
  }));
