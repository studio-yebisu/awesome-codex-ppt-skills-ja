import { describe, expect, it } from 'vitest';
import beat from './chronology.js';
describe('chronology beat', () => {
  it('puts time-scaled events in proportional positions', () => {
    const view = beat.render(
      {
        scale: 'time',
        axis: 'x',
        events: [
          { date: '2020-01-01', title: '시작' },
          { date: '2022-01-01', title: '중간', note: '성장' },
          { date: '2024-01-01', title: '현재' },
        ],
      },
      {},
    );
    expect(beat.fields.events.required).toBe(true);
    expect(view.parts.track).toHaveLength(1);
    expect(view.parts.event.map((n) => n.dataset.position)).toEqual(['0', expect.any(String), '1']);
    expect(Number(view.parts.event[1].dataset.position)).toBeGreaterThan(0.49);
    expect(Number(view.parts.event[1].dataset.position)).toBeLessThan(0.51);
    expect(view.parts.date).toHaveLength(3);
    expect(view.parts.title).toHaveLength(3);
    expect(view.parts.note[0].textContent).toBe('성장');
  });
  it('requires at least events schema field', () => expect(beat.fields.events.required).toBe(true));

  it('renders chronology v2 rail parts and source labels', () => {
    const view = beat.render(
      {
        axis: 'x',
        scale: 'time',
        label: '철도의 시대',
        caption: '도시를 잇는 시간',
        counter: 'year',
        ground: true,
        now: 0.25,
        ticks: 'year',
        events: [
          { date: '2020-01-01', title: '개통', source: 'archive' },
          { date: '2022-01-01', title: '확장', weight: 'minor', source: ['archive', 'report'] },
        ],
      },
      { sources: { archive: { short: '기록원' }, report: { title: '철도 보고서' } } },
    );

    expect(view.parts.dot).toHaveLength(2);
    expect(view.parts.stem).toHaveLength(2);
    expect(view.parts.event.map((event) => event.dataset.weight)).toEqual(['major', 'minor']);
    expect(view.parts.label[0].textContent).toBe('철도의 시대');
    expect(view.parts.caption[0].textContent).toBe('도시를 잇는 시간');
    expect(view.parts.source.map((source) => source.textContent)).toEqual(['기록원', '기록원 · 철도 보고서']);
    expect(view.parts.ground[0].dataset.depth).toBe('0');
    expect(view.parts.ghost).toHaveLength(2);
    expect(view.parts.now[0].style.left).toBe('25%');
    expect(view.parts.tick).toHaveLength(3);
  });

  it('builds year and month counter reels from the first event date', () => {
    const year = beat.render(
      {
        counter: 'year',
        events: [
          { date: '2024-03-09', title: '시작' },
          { date: '2025-01-01', title: '끝' },
        ],
      },
      {},
    );
    const month = beat.render(
      {
        counter: 'month',
        events: [
          { date: '2024-03-09', title: '시작' },
          { date: '2025-01-01', title: '끝' },
        ],
      },
      {},
    );

    expect(year.parts.reel).toHaveLength(4);
    expect(month.parts.reel).toHaveLength(6);
    expect(month.parts.reel.map((reel) => reel.dataset.digit).join('')).toBe('202403');
    month.parts.reel.forEach((reel) => {
      expect(reel.children).toHaveLength(10);
      expect(reel.style.transform).toBe(`translateY(-${Number(reel.dataset.digit) * 10}%)`);
    });
  });
});
