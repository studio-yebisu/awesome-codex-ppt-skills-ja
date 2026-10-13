import { expect, it } from 'vitest';
import { frameSeqOf } from './media.js';
it('prefers beat sequence media', () => {
  expect(frameSeqOf({ media: { seq: 1 } })).toBe(1);
  expect(frameSeqOf({ part: () => [{ slSeq: 2 }] })).toBe(2);
  expect(frameSeqOf()).toBeNull();
});
