// @vitest-environment node
import { describe, expect, it } from 'vitest';
import { formatReport, parseArgs, probeSource, shotName, summarize } from './smoke.mjs';

const stop = (over = {}) => ({
  index: 0,
  name: 'b-a',
  beat: 'b-a',
  t: 1,
  errors: [],
  visibleBeats: ['b-a'],
  texts: 2,
  overlaps: [],
  clipped: [],
  minFont: 18,
  textSample: [],
  ...over,
});

describe('smoke args', () => {
  it('defaults to the aside driver on port 5190 and switches to chrome for shots', () => {
    expect(parseArgs(['rail-ai-decade'])).toMatchObject({ deck: 'rail-ai-decade', port: 5190, driver: 'aside', shots: false });
    expect(parseArgs(['rail-ai-decade', '--shots', '--port', '5191'])).toMatchObject({ port: 5191, driver: 'chrome', shots: true });
  });
  it('rejects bad ids, unknown options and shots without chrome', () => {
    expect(() => parseArgs([])).toThrow(/smoke\.mjs <deckId>/);
    expect(() => parseArgs(['Bad Id'])).toThrow(/invalid deck id/);
    expect(() => parseArgs(['a', '--nope'])).toThrow(/unknown option/);
    expect(() => parseArgs(['a', '--shots', '--driver', 'aside'])).toThrow(/--driver chrome/);
  });
});

describe('smoke report', () => {
  it('counts errors, empty stops, overlaps, clipped and tiny text', () => {
    const report = {
      deck: 'd',
      driver: 'chrome',
      viewport: { w: 1920, h: 1080 },
      bootError: null,
      pageErrors: ['late'],
      stops: [
        stop(),
        stop({ index: 1, name: 'b-b', errors: ['x'], visibleBeats: [], overlaps: [{ a: 'a', b: 'b', area: 90 }], minFont: 12 }),
        stop({ index: 2, name: 'b-c', clipped: [{ text: 't', rect: {}, visible: 0.5 }] }),
      ],
    };
    expect(summarize(report)).toEqual({ stops: 3, errors: 2, empty: ['b-b'], overlaps: 1, clipped: 1, tinyText: ['b-b'], mediaPending: [] });
    const text = formatReport(report);
    expect(text).toContain('EMPTY');
    expect(text).toContain('stops 3 · errors 2 · empty 1 · overlaps 1 · clipped 1 · tiny 1');
  });
  it('names shots by one-based stop number and keeps the probe free of a literal dynamic import', () => {
    expect(shotName(0)).toBe('stop-01.png');
    expect(shotName(37)).toBe('stop-38.png');
    expect(probeSource('rail-ai-decade')).not.toMatch(/import\(/);
    expect(probeSource('rail-ai-decade')).toContain('"rail-ai-decade"');
  });
});
