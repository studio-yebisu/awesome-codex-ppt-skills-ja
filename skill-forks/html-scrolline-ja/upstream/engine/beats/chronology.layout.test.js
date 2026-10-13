import { expect, it } from 'vitest';
import beat from './chronology.js';

// 회귀: rail 배치 변수가 없어 engine.css가 레일 길이·「지금」 출발점·월 구분 점을 그릴 수 없었다.
it('exposes span, now and lanes for the rail layout and separates the month reel', () => {
  const view = beat.render(
    {
      axis: 'x',
      scale: 'time',
      counter: 'month',
      now: 0.375,
      ground: true,
      events: [
        { date: '2020-01-23', title: 'a' },
        { date: '2020-05-28', title: 'b', weight: 'minor' },
        { date: '2021-01-23', title: 'c' },
      ],
    },
    {},
  );
  expect(view.root.style.getPropertyValue('--sl-span')).toBe('12');
  expect(view.root.style.getPropertyValue('--sl-now')).toBe('37.5%');
  expect(view.parts.event.map((e) => e.style.getPropertyValue('--sl-lane'))).toEqual(['0', '', '1']);
  const counter = view.parts.counter[0];
  expect(counter.textContent.length).toBe(61);
  expect(counter.querySelector('.sl-chronology__sep').textContent).toBe('.');
  expect(view.parts.reel).toHaveLength(6);
  // ground는 트랙 앞(뒤 배경층), 유령 연도는 해마다 한 번
  expect(view.root.firstElementChild).toBe(view.parts.ground[0]);
  expect(view.parts.ghost.map((g) => g.textContent)).toEqual(['2020', '2021']);
});
