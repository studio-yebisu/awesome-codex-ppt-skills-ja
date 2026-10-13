import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './zoom-dive.js';

const scenario = {
  beats: [
    { id: 'a', type: 'chart', data: { parts: { mark: true, title: true } } },
    { id: 'b', type: 'photo', data: { parts: { frame: true, caption: true } } },
  ],
  rects: {
    'a.mark': { x: 100, y: 200, w: 100, h: 50 },
    'a.title': { x: 80, y: 60, w: 500, h: 60 },
    'a.plot': { x: 40, y: 140, w: 600, h: 500 },
    'b.frame': { x: 320, y: 180, w: 800, h: 500 },
    'b.caption': { x: 320, y: 700, w: 800, h: 30 },
  },
  run: {
    role: 'link',
    from: 'a',
    beat: 'b',
    params: { duration: 2.4, fromPart: 'mark', toPart: 'frame', k: 16 },
  },
  concept: {
    eases: { dive: 'sine.inOut', in: 'power2.in', out: 'power3.out' },
    tokens: { diveFill: 0.86, diveKMax: 40 },
  },
  carry: null,
};

it('meets the link contract and uses exponential midpoint scale', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  h.seek(1.2);
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('a').part('plot')[0], 'scaleX'))).toBeCloseTo(4, 1);
  h.destroy();
});

it('calculates automatic k and the port-fixed transform origin', () => {
  const h = createHarness({
    ...scenario,
    run: { ...scenario.run, params: { ...scenario.run.params, k: 0 } },
  });
  const result = h.runMove(
    move,
    h ? { ...scenario.run, params: { ...scenario.run.params, k: 0 } } : scenario.run,
  );
  const expectedK = Math.min(40, 1 / (0.86 * Math.min(100 / 800, 50 / 500)));
  const P = { x: 150, y: 225 },
    F = { x: 720, y: 430 };
  const fixed = {
    x: (expectedK * P.x - F.x) / (expectedK - 1),
    y: (expectedK * P.y - F.y) / (expectedK - 1),
  };
  h.seek(0.05);
  const [ox, oy] = h.beats.get('a').part('plot')[0].style.transformOrigin.split(' ').map(parseFloat);
  expect(ox).toBeCloseTo(fixed.x - 40, 1);
  expect(oy).toBeCloseTo(fixed.y - 140, 1);
  h.seek(1.2);
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('a').part('plot')[0], 'scaleX'))).toBeCloseTo(
    Math.sqrt(expectedK),
    1,
  );
  h.destroy();
});

it('keeps the zoom speed nonzero at the midpoint and lands B exactly at scale 1', () => {
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  const plotB = h.beats.get('b').part('frame')[0];
  const scale = (t) => {
    h.seek(t);
    return Number(result.ctx.gsap.getProperty(h.beats.get('a').part('plot')[0], 'scaleX'));
  };
  const before = scale(1.1),
    after = scale(1.3);
  expect(Math.log(after / before) / 0.2).toBeGreaterThan(0.5);
  h.seek(2.4);
  expect(Number(result.ctx.gsap.getProperty(plotB, 'scaleX'))).toBe(1);
  h.seek(0);
  h.seek(2.4);
  expect(Number(result.ctx.gsap.getProperty(plotB, 'scaleX'))).toBe(1);
  h.destroy();
});

it('uses only opacity for reduced motion', () => {
  const h = createHarness({ ...scenario, reduce: true }),
    result = h.runMove(move, scenario.run);
  h.seek(1.2);
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('a').part('plot')[0], 'scaleX'))).toBe(1);
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('b').part('frame')[0], 'scaleX'))).toBe(1);
  h.destroy();
});
