import { expect, it } from 'vitest';
import { colorOf } from './color.js';
it('prefers explicit colors and has concrete fallbacks', () => {
  expect(colorOf({ colors: { fg: '#123' }, stage: { root: document.body } }, 'fg')).toBe('#123');
  expect(colorOf({ stage: { root: document.body } }, 'accent')).toBe('#ffb000');
});
