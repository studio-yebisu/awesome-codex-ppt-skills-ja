import { afterEach, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './rail-lift.js';

const live = [];
afterEach(() => live.splice(0).forEach((h) => h.destroy()));

// 회귀: rail-lift가 from 제목에 initial autoAlpha 1을 걸어, 아직 도착 안 한 사건 제목이 b-r5 내내 떠 있었다.
it('keeps a not-yet-focused rail title hidden until its step shows it', () => {
  const run = (withNow) => {
    const rects = {
      'a.title#3': { x: 900, y: 400, w: 300, h: 80 },
      'a.stem#3': { x: 900, y: 500, w: 2, h: 150 },
      'b.label': { x: 480, y: 600, w: 900, h: 40 },
      ...(withNow ? { 'a.now': { x: 719, y: 0, w: 2, h: 1080 } } : {}),
    };
    const h = createHarness({
      beats: [
        { id: 'a', type: 'chronology', data: { events: [{}, {}, {}, { title: 'mini' }] } },
        { id: 'b', type: 'number', data: { value: 1 } },
      ],
      rects,
    });
    live.push(h);
    const calls = [];
    const r = h.runMove(move, {
      role: 'link',
      from: 'a',
      beat: 'b',
      params: { duration: 1.4, fromEvent: 3, fromPart: 'title', toPart: 'label' },
    });
    move.build(r.ctx.gsap.timeline(), { ...r.ctx, initial: (nodes, vars) => calls.push([nodes, vars]) }, {
      ...r.ctx.params,
      duration: 1.4,
      fromEvent: 3,
      fromPart: 'title',
      toPart: 'label',
      toIndex: 0,
      liftRise: 0.12,
    });
    return calls.find(([nodes]) => nodes === r.ctx.handoff.from.node)?.[1].autoAlpha;
  };
  expect(run(true)).toBe(0);
  expect(run(false)).toBe(1);
});
