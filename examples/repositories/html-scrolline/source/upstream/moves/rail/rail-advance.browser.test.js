import { afterEach, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './rail-advance.js';

// 실제 브라우저에서 드러난 회귀 3건(tools/smoke.mjs rail-ai-decade).
const events = [
  { date: '2017-06-12', title: 'A', media: 'a.jpg' },
  { date: '2018-06-11', title: 'B', note: 'b' },
  { date: '2018-10-11', title: 'C' },
];
const rects = {
  'rail.track': { x: 720, y: 713, w: 1000, h: 1 },
  'rail.now': { x: 719, y: 0, w: 2, h: 1080 },
  'rail.counter': { x: 120, y: 96, w: 120, h: 26 },
  ...Object.fromEntries(
    events.flatMap((_, i) =>
      ['event', 'dot', 'stem', 'title', 'note', 'media', 'date'].map((name) => [
        `rail.${name}#${i}`,
        { x: 711 + i * 500, y: 400, w: 18, h: 18 },
      ]),
    ),
  ),
};
const live = [];
afterEach(() => live.splice(0).forEach((h) => h.destroy()));

function setup() {
  const h = createHarness({ beats: [{ id: 'rail', type: 'chronology', data: { events, counter: 'month', now: 0.375 } }], rects });
  live.push(h);
  const beat = h.beats.get('rail');
  // 렌더러처럼 상세 part를 사건 안에 넣고, 카운터 릴에 정적 inline translateY(%)를 준다.
  beat.part('event').forEach((event, i) =>
    ['dot', 'stem', 'title', 'note', 'media', 'date'].forEach((name) => beat.part(name)[i] && event.append(beat.part(name)[i])),
  );
  const counter = beat.part('counter')[0];
  '201706'.split('').forEach((digit, place) => {
    const col = document.createElement('span');
    col.dataset.place = String(place);
    col.dataset.digit = digit;
    col.style.transform = `translateY(-${Number(digit) * 10}%)`;
    counter.append(col);
  });
  return { h, beat };
}

it('starts each step from its own event, not from the last step written', () => {
  const { h, beat } = setup();
  const r = h.runMove(move, { role: 'step', beat: 'rail', params: { from: 0, to: 1 } });
  h.seek(0.001);
  // now 중심 720 − 점0 중심 720 = 0 (예전: initial x가 마지막 step 값으로 덮임)
  expect(Math.abs(r.ctx.gsap.getProperty(beat.part('track')[0], 'x'))).toBeLessThan(2);
  h.seek(r.timing.duration);
  expect(Math.round(r.ctx.gsap.getProperty(beat.part('track')[0], 'x'))).toBe(-500);
});

it('zeroes the reel y so GSAP does not stack the static translateY(%) onto yPercent', () => {
  const { h, beat } = setup();
  const r = h.runMove(move, { role: 'step', beat: 'rail', params: { from: 0, to: 1 } });
  // happy-dom은 inline transform을 GSAP이 못 읽으므로 initial 호출을 직접 받는다.
  const calls = [];
  move.build(r.ctx.gsap.timeline(), { ...r.ctx, initial: (nodes, vars) => calls.push([nodes, vars]) }, {
    from: 0, to: 1, base: 0.6, perMonth: 0.05, max: 2.6, ghostParallax: 0.35, blurMax: 4, trailOpacity: 0.32,
  });
  const cols = [...beat.part('counter')[0].querySelectorAll('[data-place]')];
  const reelCalls = calls.filter(([nodes]) => cols.includes(nodes));
  expect(reelCalls).toHaveLength(6);
  expect(reelCalls.every(([, vars]) => vars.y === 0)).toBe(true);
});

it('folds a passed thumbnail even when the link put it there (skipNodes)', () => {
  const { h, beat } = setup();
  const media = beat.part('media')[0];
  const r = h.runMove(move, { role: 'step', beat: 'rail', params: { from: 0, to: 1 }, skipNodes: [media] });
  h.seek(r.timing.duration);
  expect(Number(r.ctx.gsap.getProperty(media, 'opacity'))).toBe(0);
  expect(Number(r.ctx.gsap.getProperty(beat.part('title')[1], 'opacity'))).toBe(1);
});

it('keeps rolling the counter that a counter-handoff link placed (skipNodes)', () => {
  const { h, beat } = setup();
  const counter = beat.part('counter')[0];
  const r = h.runMove(move, { role: 'step', beat: 'rail', params: { from: 0, to: 1 }, skipNodes: [counter] });
  const calls = [];
  move.build(r.ctx.gsap.timeline(), { ...r.ctx, initial: (nodes, vars) => calls.push([nodes, vars]) }, {
    from: 0, to: 1, base: 0.6, perMonth: 0.05, max: 2.6, ghostParallax: 0.35, blurMax: 4, trailOpacity: 0.32,
  });
  const cols = [...counter.querySelectorAll('[data-place]')];
  expect(calls.filter(([nodes]) => cols.includes(nodes))).toHaveLength(6);
});
