import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { countTo, formatNumber } from './count.js';
it('formats and counts deterministically', () => {
  expect(formatNumber(1234.5, { lang: 'en', decimals: 2, prefix: '$' })).toBe('$1,234.50');
  const h = createHarness({ beats: [{ id: 'a', type: 'text', data: {} }] }),
    node = h.beats.get('a').part('block')[0];
  const m = {
    id: 'count-test',
    family: 'data',
    role: 'enter',
    accepts: ['*'],
    sources: ['x'],
    reduce: 'self',
    params: {},
    timing: () => ({ duration: 1 }),
    build(t) {
      countTo(t, node, { from: 120, to: 105.6, at: 0, duration: 1, decimals: 1 });
    },
  };
  h.runMove(m, { role: 'enter', beat: 'a' });
  h.seek(1);
  expect(node.textContent).toBe('105.6');
  h.destroy();
});
