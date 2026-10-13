import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './tracking-close.js';
const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'A B', parts: { word: true } } }],
  run: { role: 'enter', beat: 'b', params: { duration: 1.3, spread: 0.6 } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
