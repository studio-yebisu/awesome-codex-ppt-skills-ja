import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import { scrambleAt, scrambleTable } from '../_shared/scramble.js';
import move from './scramble-swap.js';

const scenario = {
  beats: [{ id: 'b', type: 'text', data: { parts: { word: true } } }],
  rects: { 'b.word#0': { x: 200, y: 300, w: 120, h: 42 } },
  run: { role: 'step', beat: 'b', params: { word: 0, from: '이전', duration: 1.6, glyphs: '#%&' } },
};
it('meets the step contract and settles on the authored replacement', () =>
  expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('scrambleAt is deterministic and preserves its endpoints', () => {
  const table = scrambleTable(() => 0.2, 4, 4, '#%');
  expect(scrambleAt('FROM', 'TO!!', 0, table)).toBe('FROM');
  expect(scrambleAt('FROM', 'TO!!', 1, table)).toBe('TO!!');
  expect(scrambleAt('FROM', 'TO!!', 0.5, table)).toBe(scrambleAt('FROM', 'TO!!', 0.5, table));
});
