import { afterEach, describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './rail-advance.js';
import { checkMove } from '../_shared/contract-check.js';

const events = [
  { date: '2020-01', title: 'Start', weight: 'major' },
  { date: '2020-06', title: 'Middle', note: 'Note', weight: 'minor' },
  { date: '2023-01', title: 'End', weight: 'major' },
];
const params = {
  from: 0,
  to: 2,
  base: 0.6,
  perMonth: 0.05,
  max: 2.6,
  ghostParallax: 0.35,
  blurMax: 4,
  trailOpacity: 0.32,
};
const scenario = {
  beats: [{ id: 'rail', type: 'chronology', data: { events, counter: 'month', parts: {} } }],
  rects: Object.fromEntries(
    ['track', 'ground', 'counter', 'now']
      .map((name, i) => [`rail.${name}`, { x: i * 100, y: 0, w: 80, h: 40 }])
      .concat(
        events.flatMap((_, i) =>
          ['event', 'dot', 'stem', 'title', 'note', 'media'].map((name) => [
            `rail.${name}#${i}`,
            { x: 100 + i * 300, y: 80, w: 40, h: 30 },
          ]),
        ),
      ),
  ),
  run: { role: 'step', beat: 'rail', params },
  prepare(h) {
    const counter = h.beats.get('rail').part('counter')[0];
    for (let i = 0; i < 6; i += 1) {
      const col = document.createElement('span');
      col.dataset.place = String(i);
      col.dataset.digit = '0';
      counter.append(col);
    }
  },
};
const live = [];
afterEach(() => live.splice(0).forEach((h) => h.destroy()));
describe('rail-advance', () => {
  it('passes the move contract and date timing', () => {
    expect(checkMove(move, scenario, createHarness)).toEqual([]);
    expect(move.timing(params, { events }).duration).toBe(2.4);
    expect(move.timing({ ...params, to: 1 }, { events }).duration).toBe(0.85);
  });
  it('rolls only changed reel places and removes blur in reduce mode', () => {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects, reduce: true });
    live.push(h);
    scenario.prepare(h);
    const r = h.runMove(move, scenario.run);
    h.seek(r.timing.duration);
    expect(
      r.ctx.beat.part('counter')[0].querySelectorAll('[data-place]')[0].getAttribute('style') ?? '',
    ).not.toMatch(/yPercent/);
    expect(r.ctx.beat.part('track')[0].getAttribute('style')).not.toMatch(/blur/);
  });
});
