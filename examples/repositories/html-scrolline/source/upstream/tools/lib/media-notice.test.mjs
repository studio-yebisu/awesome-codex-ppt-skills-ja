// @vitest-environment node
import { expect, it } from 'vitest';
import { mediaNotice, printMediaNotice } from './media-notice.mjs';

it('recommends issuing a stock-video API key only when none is set', () => {
  expect(mediaNotice({})).toMatch(/PEXELS_API_KEY/);
  expect(mediaNotice({})).toMatch(/\.env/);
  expect(mediaNotice({ PEXELS_API_KEY: 'x' })).toBeNull();
  const lines = [];
  expect(printMediaNotice({}, (t) => lines.push(t))).toBe(true);
  expect(printMediaNotice({ PIXABAY_API_KEY: 'x' }, (t) => lines.push(t))).toBe(false);
  expect(lines).toHaveLength(1);
});
