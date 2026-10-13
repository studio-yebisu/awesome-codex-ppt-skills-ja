import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './baseline-grow.js';

const make = (orient) => ({
  beats: [
    { id: 'c', type: 'chart', data: { orient, parts: { mark: true, label: true, axis: true, title: true } } },
  ],
  rects: { 'c.mark#0': { x: 0, y: 0, w: 10, h: 10 }, 'c.mark#1': { x: 20, y: 0, w: 10, h: 10 } },
  run: { role: 'enter', beat: 'c', params: { duration: 1.2, stagger: 0.04 } },
});
it('passes contract and grows vertical bars on y', () => {
  const s = make('v');
  expect(checkMove(move, s, createHarness)).toEqual([]);
  const h = createHarness(s);
  const r = h.runMove(move, s.run);
  h.seek(0);
  expect(Number(r.ctx.gsap.getProperty(h.beats.get('c').part('mark')[0], 'scaleY'))).toBe(0);
  h.destroy();
});
it('grows horizontal bars on x', () => {
  const s = make('h');
  const h = createHarness(s);
  const r = h.runMove(move, s.run);
  h.seek(0);
  expect(Number(r.ctx.gsap.getProperty(h.beats.get('c').part('mark')[0], 'scaleX'))).toBe(0);
  h.destroy();
});
