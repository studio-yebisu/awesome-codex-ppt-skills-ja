import { expect, it } from 'vitest';
import { partFree } from './skip.js';

it('drops skipped parts, the handed node and its descendants', () => {
  const frame = document.createElement('div');
  const media = document.createElement('img');
  frame.append(media);
  const other = document.createElement('p');
  const parts = { frame: [frame], media: [media], caption: [other] };
  const ctx = { skipParts: ['caption'], skipNodes: [frame], beat: { part: (n) => parts[n] ?? [] } };
  expect(partFree(ctx, 'frame')).toEqual([]);
  expect(partFree(ctx, 'media')).toEqual([]);
  expect(partFree(ctx, 'caption')).toEqual([]);
  expect(partFree({ ...ctx, skipParts: [], skipNodes: [] }, 'caption')).toEqual([other]);
});
