import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './push-build.js';
const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'Push Build', parts: { word: true } } }],
  run: { role: 'enter', beat: 'b', params: { duration: 1.8, accentWords: [0] } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
