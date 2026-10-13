import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { seg } from './timeline.js';

// 회귀(kinetic 보고): `{ ...seg(d, a, b) }`가 GSAP가 모르는 `at`을 펼쳐 모든 구간이 0에서 시작했다.
it('starts a spread segment at d·a inside the move timeline', () => {
  const h = createHarness({ beats: [{ id: 'a', type: 'text', data: {} }] });
  const node = h.beats.get('a').part('block')[0];
  const r = h.runMove(
    {
      id: 'seg-test',
      family: 'type',
      role: 'enter',
      accepts: ['*'],
      sources: ['x'],
      reduce: 'self',
      params: {},
      timing: () => ({ duration: 10 }),
      build: (tl) => tl.fromTo(node, { x: 0 }, { x: 100, ease: 'none', ...seg(10, 0.5, 1) }, 0),
    },
    { role: 'enter', beat: 'a' },
  );
  h.seek(4);
  expect(Number(r.ctx.gsap.getProperty(node, 'x'))).toBe(0);
  h.seek(7.5);
  expect(Number(r.ctx.gsap.getProperty(node, 'x'))).toBe(50);
  h.destroy();
});
