import { describe, expect, it } from 'vitest';
import beat from './chart.js';
const data = {
  kind: 'bar',
  categories: ['Q1', 'Q2'],
  series: [{ name: '매출', values: [10, 20] }],
  source: 's1',
};
describe('chart beat', () => {
  it('creates a contract SVG and indexed series marks', () => {
    const view = beat.render(data, {});
    expect(beat.fields.kind.required).toBe(true);
    expect(view.parts.plot[0].getAttribute('viewBox')).toBe('0 0 1600 900');
    expect(view.parts.mark).toHaveLength(2);
    expect(view.parts.mark.map((m) => `${m.dataset.series}/${m.dataset.index}`)).toEqual(['0/0', '0/1']);
    expect(view.parts.axis).toHaveLength(1);
    expect(view.parts.label).toHaveLength(2);
    expect(view.parts.legend[0].textContent).toBe('매출');
    expect(view.parts.source[0].textContent).toBe('s1');
  });
  it('requires categories and series', () => {
    expect(beat.fields.categories.required).toBe(true);
    expect(beat.fields.series.required).toBe(true);
  });

  // v2: #9 #11 #12
  it('renders positioned copy layers for the base and each state', () => {
    const view = beat.render(
      {
        ...data,
        title: 'Base conclusion',
        dek: 'Base context',
        unit: '억원',
        notes: [{ index: 1, text: 'Base note' }],
        states: [
          { name: 'detail', title: 'Detailed conclusion' },
          { name: 'final', dek: 'Final context' },
        ],
      },
      {},
    );

    expect(view.parts.title.map((element) => element.dataset.state)).toEqual(['base', 'detail', 'final']);
    expect(view.parts.dek.map((element) => element.textContent)).toEqual([
      'Base context',
      'Base context',
      'Final context',
    ]);
    expect(view.parts.note).toHaveLength(3);
    expect(view.parts.note[0].dataset.index).toBe('1');
    expect(view.parts.note[0].dataset.series).toBe('0');
    expect(view.parts.note[0].style.left).toMatch(/%$/);
    expect(view.parts.note[0].style.top).toMatch(/%$/);
    expect(view.parts.title[1].style.visibility).toBe('hidden');
    expect(view.parts.title[1].style.opacity).toBe('0');
    expect(view.parts.unit.map((element) => element.textContent)).toEqual(['억원', '억원', '억원']);
  });

  // v2: #10 #11
  it('draws horizontal bars in category order with widths proportional to their values', () => {
    const view = beat.render(
      {
        ...data,
        orient: 'h',
        categories: ['small', 'large'],
        series: [{ name: 'value', values: [10, 20] }],
      },
      {},
    );
    const [small, large] = view.parts.mark;
    expect(Number(small.getAttribute('width'))).toBeLessThan(Number(large.getAttribute('width')));
    expect(Number(small.getAttribute('y'))).toBeLessThan(Number(large.getAttribute('y')));
  });

  // v2: #10
  it('uses a zero baseline and directions for negative bars without NaN geometry', () => {
    const view = beat.render(
      {
        ...data,
        categories: ['loss', 'gain'],
        series: [{ name: 'change', values: [-10, 20] }],
      },
      {},
    );
    const [loss, gain] = view.parts.mark;
    const baseline = Number(view.parts.baseline[0].getAttribute('y1'));
    expect(view.parts.baseline).toHaveLength(1);
    expect(loss.dataset.sign).toBe('neg');
    expect(gain.dataset.sign).toBe('pos');
    expect(Number(loss.getAttribute('y'))).toBe(baseline);
    expect(Number(loss.getAttribute('height'))).toBeGreaterThan(0);
    expect(
      [...view.parts.mark, ...view.parts.baseline].every((element) => !element.outerHTML.includes('NaN')),
    ).toBe(true);
  });

  // v2: #10
  it('keeps an all-zero chart finite', () => {
    const view = beat.render({ ...data, series: [{ name: 'zero', values: [0, 0] }] }, {});
    expect(view.root.outerHTML).not.toContain('NaN');
    expect(view.parts.baseline).toBeUndefined();
  });

  // v2: #27 #41
  it('uses source short names and joins an array with a middle dot', () => {
    const view = beat.render(
      { ...data, source: ['s1', 's2'] },
      { sources: { s1: { title: 'Long first source', short: 'First' }, s2: { title: 'Second source' } } },
    );
    expect(view.parts.source[0].textContent).toBe('First · Second source');
  });
});
