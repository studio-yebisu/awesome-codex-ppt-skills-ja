import { describe, expect, it } from 'vitest';
import beat from './compare.js';
describe('compare beat', () => {
  it('renders compared items and verdict', () => {
    const view = beat.render(
      {
        items: [
          { label: 'A', value: 1200, text: '빠름' },
          { label: 'B', value: 800 },
        ],
        verdict: 'A를 선택',
      },
      { lang: 'ko', sources: { s1: { short: '통계청', title: '국가통계' } } },
    );
    expect(beat.fields.items.required).toBe(true);
    expect(view.parts.item).toHaveLength(2);
    expect(view.parts.divider).toHaveLength(1);
    expect(view.parts.value[0].textContent).toBe('1,200');
    expect(view.parts.verdict[0].textContent).toBe('A를 선택');
  });
  it('renders an array source in one source part', () => {
    const view = beat.render(
      { items: [{ label: 'A' }, { label: 'B' }], source: ['s1', 's2'] },
      { sources: { s1: { short: 'A' }, s2: { title: 'B source' } } },
    );
    expect(beat.fields.source.type).toBe('any');
    expect(view.parts.source[0].textContent).toBe('A · B source');
  });
  it('requires items', () => expect(beat.fields.items.required).toBe(true));
});
