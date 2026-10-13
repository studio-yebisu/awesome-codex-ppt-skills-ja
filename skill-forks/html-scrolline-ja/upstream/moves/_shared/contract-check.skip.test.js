import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from './contract-check.js';
import { partFree } from './skip.js';

const base = {
  id: 'skip-test',
  family: 'type',
  role: 'enter',
  accepts: ['*'],
  sources: ['x'],
  reduce: 'self',
  params: { duration: { type: 'number', default: 1.2, doc: 'd' } },
  timing: (p) => ({ duration: p.duration, stops: [] }),
};
const scenario = { beats: [{ id: 'a', type: 'text', data: {} }], run: { role: 'enter', beat: 'a' } };

// 문서 대조로 찾은 결함: timing에 기본값이 안 채워진 params가 갔고(duration NaN도 통과 못 하던 move),
// C17 8번(skipNodes 불변·handoff 순수)을 검사하지 않았다.
it('passes schema defaults to timing', () => {
  expect(checkMove({ ...base, build() {} }, scenario, createHarness)).toEqual([]);
});

it('flags an enter move that sets or tweens the handed node, and passes one that skips it', () => {
  const careless = {
    ...base,
    build(tl, ctx) {
      const block = ctx.beat.part('block');
      ctx.initial(block, { autoAlpha: 0, y: 20 });
      tl.to(block, { autoAlpha: 1, y: 0, duration: 1 }, 0);
    },
  };
  const careful = {
    ...base,
    build(tl, ctx) {
      const block = partFree(ctx, 'block');
      ctx.initial(block, { autoAlpha: 0, y: 20 });
      tl.to(block, { autoAlpha: 1, y: 0, duration: 1 }, 0);
    },
  };
  expect(checkMove(careless, scenario, createHarness)).toContain('skipNodes changed by build');
  expect(checkMove(careful, scenario, createHarness)).toEqual([]);
});
