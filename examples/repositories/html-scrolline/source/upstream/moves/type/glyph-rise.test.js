import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './glyph-rise.js';
const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'ABC', parts: { char: true, caption: true } } }],
  run: { role: 'enter', beat: 'b', params: { duration: 1.2, stagger: 0.08, spread: 0.12 } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
