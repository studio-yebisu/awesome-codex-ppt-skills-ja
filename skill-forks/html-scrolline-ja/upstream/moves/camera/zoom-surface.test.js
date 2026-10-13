import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './zoom-surface.js';

const scenario = {
  beats: [
    { id: 'a', type: 'number', data: { parts: { label: true, source: true } } },
    { id: 'b', type: 'chart', data: { parts: { mark: true, title: true } } },
  ],
  rects: {
    'a.value': { x: 300, y: 200, w: 800, h: 500 },
    'a.label': { x: 300, y: 750, w: 600, h: 40 },
    'b.mark': { x: 120, y: 270, w: 100, h: 50 },
    'b.plot': { x: 40, y: 140, w: 900, h: 600 },
    'b.title': { x: 80, y: 60, w: 600, h: 60 },
  },
  run: {
    role: 'link',
    from: 'a',
    beat: 'b',
    params: { duration: 2.2, fromPart: 'value', toPart: 'mark', k: 16, keepRing: true },
  },
  concept: {
    eases: { dive: 'sine.inOut', in: 'power2.in', out: 'power3.out' },
    tokens: { diveFill: 0.86, diveKMax: 40 },
  },
  carry: null,
};

it('meets the link contract and reverses the exponential scales', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  h.seek(1.1);
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('a').part('value')[0], 'scaleX'))).toBeCloseTo(
    0.25,
    1,
  );
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('b').part('plot')[0], 'scaleX'))).toBeCloseTo(4, 1);
  h.seek(2.2);
  expect(
    Number(result.ctx.gsap.getProperty(h.stage.overlay.querySelector('.sl-zoom-ring'), 'opacity')),
  ).toBeCloseTo(0.9, 2);
  h.destroy();
});

it('uses only opacity for reduced motion', () => {
  const h = createHarness({ ...scenario, reduce: true }),
    result = h.runMove(move, scenario.run);
  h.seek(1.1);
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('a').part('value')[0], 'scaleX'))).toBe(1);
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('b').part('plot')[0], 'scaleX'))).toBe(1);
  h.destroy();
});
