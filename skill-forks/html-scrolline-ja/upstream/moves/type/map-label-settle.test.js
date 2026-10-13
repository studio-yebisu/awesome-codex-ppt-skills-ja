import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './map-label-settle.js';
const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'Map Label', parts: { line: true, em: true } } }],
  run: { role: 'enter', beat: 'b', params: { duration: 1.3, spread: 0.45, lineOverlap: 0.5 } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
