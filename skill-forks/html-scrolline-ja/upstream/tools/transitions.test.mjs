// @vitest-environment node
import { describe, expect, it } from 'vitest';
import { parseArgs, sampleTimes } from './transitions.mjs';

describe('transitions', () => {
  it('parses deck, url, samples and out', () => {
    const o = parseArgs(['rail-ai-decade', '--samples', '4']);
    expect(o.deck).toBe('rail-ai-decade');
    expect(o.samples).toBe(4);
    expect(o.url).toBe('http://localhost:5190/decks/rail-ai-decade/index.html');
    expect(() => parseArgs([])).toThrow();
    expect(() => parseArgs(['x', '--bogus'])).toThrow();
  });
  it('samples only link and step spans, both ends included', () => {
    const map = {
      beats: [
        {
          id: 'a',
          spans: [
            { role: 'enter', move: 'm', start: 0, end: 1 },
            { role: 'step', move: 'dive', start: 1, end: 2 },
          ],
        },
        { id: 'b', spans: [{ role: 'link', move: 'drop', start: 2, end: 3.5 }] },
      ],
    };
    const rows = sampleTimes(map, 4);
    expect(rows.map((r) => r.move)).toEqual(['dive', 'drop']);
    expect(rows[1].times).toEqual([2, 2.5, 3, 3.5]);
  });
});
