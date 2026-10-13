import { afterEach, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './rail-split-open.js';

const live = [];
afterEach(() => live.splice(0).forEach((h) => h.destroy()));

// 회귀: from 트랙을 initial로 숨겨 link 전(b-r7 정지점)부터 레일이 빠져 있었다. 숨김은 link 시작에서.
it('hides the outgoing rail only when the link starts', () => {
  const h = createHarness({
    beats: [
      { id: 'a', type: 'chronology', data: { events: [{ date: '2025', title: 'e' }], now: 0.375 } },
      { id: 'b', type: 'video', data: {} },
    ],
    rects: {
      'a.track': { x: 720, y: 713, w: 900, h: 1 },
      'a.now': { x: 719, y: 0, w: 2, h: 1080 },
      'b.frame': { x: 0, y: 0, w: 1920, h: 1080 },
    },
  });
  live.push(h);
  const track = h.beats.get('a').part('track')[0];
  const calls = [];
  const r = h.runMove(move, { role: 'link', from: 'a', beat: 'b', params: { duration: 1.5 } });
  move.build(r.ctx.gsap.timeline(), { ...r.ctx, initial: (nodes, vars) => calls.push([nodes, vars]) }, {
    duration: 1.5,
    lineHold: 0.25,
  });
  expect(calls.some(([nodes, vars]) => [nodes].flat().includes(track) && vars.autoAlpha === 0)).toBe(false);
  h.seek(0.01);
  expect(Number(r.ctx.gsap.getProperty(track, 'opacity'))).toBe(0);
});
