import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './line-mask-rise.js';
const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'A B', parts: { line: true, word: true, em: true } } }],
  run: {
    role: 'enter',
    beat: 'b',
    params: { rule: true, emStyle: 'underline', stagger: 0.14, tracking: 0, duration: 1 },
  },
};
it('satisfies the move contract and underline preset', () =>
  expect(checkMove(move, scenario, createHarness)).toEqual([]));
