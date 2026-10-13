import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './type-on.js';

// 회귀(kinetic 통합): caret에 무대 좌표를 그대로 translate로 줘서 글 끝 inline 자리에서 오른쪽 멀리 튀었고,
// y를 안 줘서 두 줄 프롬프트의 첫 줄을 칠 때도 마지막 줄에 있었다.
it('moves the caret relative to its own rest place, across lines', () => {
  const h = createHarness({
    beats: [{ id: 'p', type: 'prompt', data: { text: 'ab cd' } }],
    rects: {
      'p.field': { x: 100, y: 100, w: 400, h: 120 },
      'p.caret': { x: 160, y: 160, w: 4, h: 40 }, // rest = 2번째 줄 끝
      'p.char#0': { x: 120, y: 110, w: 20, h: 40 },
      'p.char#1': { x: 140, y: 110, w: 20, h: 40 },
      'p.char#2': { x: 160, y: 110, w: 10, h: 40 },
      'p.char#3': { x: 120, y: 160, w: 20, h: 40 },
      'p.char#4': { x: 140, y: 160, w: 20, h: 40 },
    },
  });
  const r = h.runMove(move, { role: 'enter', beat: 'p', params: { speed: 10, chunk: 'char' } });
  const caret = r.ctx.beat.part('caret')[0];
  const at = () => [Number(r.ctx.gsap.getProperty(caret, 'x')), Number(r.ctx.gsap.getProperty(caret, 'y'))];
  h.seek(0);
  expect(at()).toEqual([-40, -50]); // 첫 글자 왼쪽, 첫 줄
  const d = r.timing.duration;
  h.seek(d * (0.1 + (1 / 5) * 0.82) + 0.001); // 둘째 글자까지
  expect(at()).toEqual([0, -50]); // 160 − 160, 110 − 160
  h.seek(d);
  expect(at()).toEqual([0, 0]); // 마지막 글자 끝 = 제자리
  h.destroy();
});
