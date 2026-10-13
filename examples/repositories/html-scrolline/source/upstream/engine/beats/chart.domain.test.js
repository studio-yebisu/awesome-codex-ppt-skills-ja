import { expect, it } from 'vitest';
import chart from './chart.js';

const height = (view, i) => Number(view.parts.mark[i].getAttribute('height'));

// zoom 요청: 전후 비교 차트(-53 → -3)가 자동 영역이면 -3이 -53과 같은 깊이로 그려졌다.
it('widens the value range with domain and exposes the range on the plot', () => {
  const base = { kind: 'bar', categories: ['a', 'b', 'c'], series: [{ name: 's', values: [-1, -3, -1] }] };
  const auto = chart.render(base, {});
  const fixed = chart.render({ ...base, domain: { min: -53 } }, {});
  expect(auto.parts.plot[0].dataset).toMatchObject({ min: '-3', max: '0' });
  expect(fixed.parts.plot[0].dataset).toMatchObject({ min: '-53', max: '0' });
  expect(height(fixed, 1) / height(auto, 1)).toBeCloseTo(3 / 53, 5);
  // 데이터보다 좁은 domain은 무시(잘리지 않음)
  const narrow = chart.render({ ...base, domain: { min: -2, max: 1 } }, {});
  expect(narrow.parts.plot[0].dataset).toMatchObject({ min: '-3', max: '1' });
});

it('accepts domain in the field schema', () => {
  expect(chart.fields.domain.fields).toHaveProperty('min');
  expect(chart.fields.domain.fields).toHaveProperty('max');
});
