import { describe, expect, it } from 'vitest';
import { createRng, hashSeed } from './rng.js';

describe('seeded RNG', () => {
  it('hashes strings deterministically and produces repeatable [0, 1) values', () => {
    expect(hashSeed('deck:beat')).toBe(hashSeed('deck:beat'));
    const a = createRng('deck:beat'),
      b = createRng('deck:beat');
    const av = Array.from({ length: 5 }, a),
      bv = Array.from({ length: 5 }, b);
    expect(av).toEqual(bv);
    expect(av.every((value) => value >= 0 && value < 1)).toBe(true);
  });
});
