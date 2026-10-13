import { expect, it } from 'vitest';
import { eventDetail, railFocus } from './rail-focus.js';

function fakeBeat(withNow = true) {
  const parts = { event: [], now: withNow ? [document.createElement('div')] : [] };
  for (let i = 0; i < 3; i += 1) {
    const event = document.createElement('article');
    for (const name of ['dot', 'stem', 'date', 'title', 'note']) {
      const node = document.createElement('span');
      node.dataset.part = name;
      event.append(node);
    }
    parts.event.push(event);
  }
  return { part: (name) => parts[name] ?? [] };
}

it('hides the detail of every event but the focused one', () => {
  const beat = fakeBeat();
  const calls = [];
  const hidden = railFocus({ initial: (nodes, vars) => calls.push([nodes, vars]) }, beat, 1);
  expect(hidden).toHaveLength(8);
  expect(hidden.every((node) => ['stem', 'date', 'title', 'note'].includes(node.dataset.part))).toBe(true);
  expect(eventDetail(beat, 1).some((node) => hidden.includes(node))).toBe(false);
  expect(calls[0][1]).toEqual({ autoAlpha: 0 });
});

it('leaves an overview rail without a now line alone', () => {
  const calls = [];
  expect(railFocus({ initial: (n, v) => calls.push(v) }, fakeBeat(false), 0)).toEqual([]);
  expect(calls).toEqual([]);
});
