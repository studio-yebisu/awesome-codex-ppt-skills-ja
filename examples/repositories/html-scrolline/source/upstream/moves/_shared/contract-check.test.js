import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from './contract-check.js';
it('returns a sentence list for invalid timelines', () => {
  const move = {
    id: 'check-test',
    family: 'data',
    role: 'enter',
    accepts: ['*'],
    sources: ['x'],
    reduce: 'self',
    params: {},
    timing: () => ({ duration: 1 }),
    build(t, ctx) {
      t.to(ctx.beat.part('block'), { x: 1, duration: 2 }, 0);
    },
  };
  expect(
    checkMove(
      move,
      { beats: [{ id: 'a', type: 'text', data: {} }], run: { role: 'enter', beat: 'a' } },
      createHarness,
    ),
  ).toContain('timeline exceeds timing duration');
});
