import { expect, it } from 'vitest';
import { buildReel } from './reel.js';
it('builds digit columns', () => {
  const host = document.createElement('div');
  const reel = buildReel(host, '2016.03');
  expect(reel.cols).toHaveLength(6);
  expect(host.querySelectorAll('.sl-reel__fixed')).toHaveLength(1);
});
