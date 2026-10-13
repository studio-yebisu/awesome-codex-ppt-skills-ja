import { expect, it } from 'vitest';
import { eventPart } from './event-part.js';

const events = [
  { date: '2021', title: 'a' },
  { date: '2022', title: 'b', media: 'b.jpg' },
  { date: '2023', title: 'c' },
  { date: '2024', title: 'd', media: 'd.jpg' },
];

it('maps an event index to the sparse media part index', () => {
  expect(eventPart(events, 'media', 3)).toEqual({ part: 'media', index: 1 });
  expect(eventPart(events, 'media', 1)).toEqual({ part: 'media', index: 0 });
  expect(eventPart(events, 'media', -1)).toEqual({ part: 'media', index: 1 });
});

it('keeps per-event parts and events without the part on their own index', () => {
  expect(eventPart(events, 'title', 2)).toEqual({ part: 'title', index: 2 });
  expect(eventPart(events, 'dot', -1)).toEqual({ part: 'dot', index: -1 });
  expect(eventPart(events, 'media', 0)).toEqual({ part: 'media', index: 0 });
  expect(eventPart(events, 'media', 2)).toEqual({ part: 'media', index: 2 });
});
