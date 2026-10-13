import { expect, it } from 'vitest';
import { clamp, lerp, seg, slots } from './timeline.js';
it('calculates segments and compressed slots', () => {
  expect({ ...seg(10, 0.2, 0.7) }).toEqual({ delay: 2, duration: 5 });
  expect(seg(10, 0.2, 0.7).at).toBe(2);
  expect(clamp(3, 0, 2)).toBe(2);
  expect(lerp(2, 6, 0.5)).toBe(4);
  const value = slots(5, { start: 0, span: 4, compress: 0.85 });
  expect(value.at(-1).at).toBeCloseTo(4);
  expect(value[2].at - value[1].at).toBeLessThan(value[1].at - value[0].at);
});
