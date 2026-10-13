import { afterEach, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './era-shift.js';

const live = [];
afterEach(() => live.splice(0).forEach((h) => h.destroy()));

// 회귀: A·B 트랙 rect가 같아(둘 다 「지금」에서 출발) dx = 0 → A 레일이 처음으로 되감기고 B는 제자리.
// 이제 두 트랙이 개월 차 × monthPx만큼 함께 왼쪽으로 달린다.
it('runs both tracks left by the month gap between eras', () => {
  const h = createHarness({
    beats: [
      { id: 'a', type: 'chronology', data: { events: [{ date: '2023-02-24' }, { date: '2023-12-06' }], now: 0.375 } },
      { id: 'b', type: 'chronology', data: { events: [{ date: '2024-02-15' }], now: 0.375 } },
    ],
    rects: {
      'a.track': { x: 720, y: 713, w: 600, h: 1 },
      'b.track': { x: 720, y: 713, w: 600, h: 1 },
      'a.now': { x: 719, y: 0, w: 2, h: 1080 },
      'b.now': { x: 719, y: 0, w: 2, h: 1080 },
      'a.dot#0': { x: 711, y: 704, w: 18, h: 18 },
      'a.dot#1': { x: 1311, y: 704, w: 18, h: 18 },
      'b.dot': { x: 711, y: 704, w: 18, h: 18 },
      'b.ground': { x: 0, y: 0, w: 1920, h: 1080 },
    },
  });
  live.push(h);
  const r = h.runMove(move, { role: 'link', from: 'a', beat: 'b', params: { duration: 2 } });
  const aTrack = h.beats.get('a').part('track')[0],
    bTrack = h.beats.get('b').part('track')[0];
  h.seek(0.001);
  expect(Math.round(r.ctx.gsap.getProperty(aTrack, 'x'))).toBe(-600);
  expect(Math.round(r.ctx.gsap.getProperty(bTrack, 'x'))).toBe(128);
  h.seek(2);
  expect(Math.round(r.ctx.gsap.getProperty(aTrack, 'x'))).toBe(-728);
  expect(Math.round(r.ctx.gsap.getProperty(bTrack, 'x'))).toBe(0);
  // 회귀: 경계선이 왼쪽 끝 x 0에 남아 B의 모든 정지 화면에 세로선이 보였다.
  const boundary = r.ctx.overlay.lastElementChild;
  expect(Number(r.ctx.gsap.getProperty(boundary, 'opacity'))).toBe(0);
});
