import { expect, it } from 'vitest';
import { scrambleAt, scrambleTable } from './scramble.js';
it('precomputes deterministic scramble text', () => {
  const a = scrambleTable(() => 0.1, 4, 3, 'ABC');
  expect(a).toEqual(scrambleTable(() => 0.1, 4, 3, 'ABC'));
  expect(scrambleAt('FROM', 'TO!!', 0, a)).toBe('FROM');
  expect(scrambleAt('FROM', 'TO!!', 1, a)).toBe('TO!!');
});
