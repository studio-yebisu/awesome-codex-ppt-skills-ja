import { describe, expect, it } from 'vitest';
import beat from './photo.js';
describe('photo beat', () => {
  it('renders frame/media and optional caption', () => {
    const view = beat.render(
      { src: 'assets/a.webp', alt: '풍경', caption: '사진', focus: { x: 0.2, y: 0.8 } },
      { asset: (p) => `/base/${p}` },
    );
    expect(beat.fields.src.required).toBe(true);
    expect(view.parts.frame).toHaveLength(1);
    expect(view.parts.media[0].src).toContain('/base/assets/a.webp');
    expect(view.parts.media[0].alt).toBe('풍경');
    expect(view.parts.caption[0].textContent).toBe('사진');
  });
  it('declares missing src invalid', () => expect(beat.fields.src.required).toBe(true));
  it('formats array sources in a source part', () => {
    const view = beat.render(
      { src: 'assets/a.webp', alt: '풍경', source: ['s1', 's2'] },
      { sources: { s1: { short: '사진가' }, s2: { title: '아카이브' } } },
    );
    expect(beat.fields.source.type).toBe('any');
    expect(view.parts.source[0].textContent).toBe('사진가 · 아카이브');
  });
});
