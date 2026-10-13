import { describe, expect, it } from 'vitest';
import { add, root, sourceText } from './helpers.js';
import { validateSchema } from '../util/schema.js';
import { beatTypes } from './index.js';
describe('beat helpers', () => {
  it('creates roots and array parts', () => {
    const parts = {};
    const view = root('text', {});
    add(parts, 'block', document.createElement('div'));
    expect(view.dataset.beat).toBeUndefined();
    expect(parts.block).toHaveLength(1);
  });

  it('formats source ids with short names, titles, and an id fallback', () => {
    const rc = { sources: { s1: { short: 'Reuters', title: 'Reuters News' }, s2: { title: 'Full title' } } };
    expect(sourceText(rc, ['s1', 's2', 'gone'])).toBe('Reuters · Full title · gone');
  });
});

const fixtures = {
  text: { text: '문장' },
  photo: { src: 'assets/a.webp', alt: '사진' },
  video: { src: 'assets/a.mp4', poster: 'assets/a.webp', alt: '영상', mode: 'play' },
  number: { value: 1, label: '값' },
  chart: { kind: 'bar', categories: ['A'], series: [{ name: '값', values: [1] }] },
  chronology: {
    events: [
      { date: '2020', title: '시작' },
      { date: '2021', title: '끝' },
    ],
  },
  compare: { items: [{ label: 'A' }, { label: 'B' }] },
  quote: { text: '인용', by: '사람' },
  prompt: { text: '질문' },
  code: { code: 'x()', lang: 'js' },
};
describe('C4 field schemas', () => {
  it.each(Object.keys(fixtures))('%s accepts a valid fixture', (type) =>
    expect(validateSchema(beatTypes[type].fields, fixtures[type])).toEqual([]),
  );
  it.each(Object.keys(fixtures))('%s rejects a missing required field fixture', (type) =>
    expect(validateSchema(beatTypes[type].fields, {})).not.toEqual([]),
  );
});
