// @vitest-environment node
import { expect, it } from 'vitest';
import { scanText } from './check-secrets.mjs';

it('flags keys and key assignments, not ordinary text', () => {
  expect(scanText('const k = "sk-ant-' + 'a'.repeat(24) + '"').map((h) => h.name)).toEqual([
    'openai/anthropic key',
  ]);
  expect(scanText('PEXELS_API_KEY=' + 'b'.repeat(20))).toHaveLength(1);
  expect(scanText('Set PEXELS_API_KEY in .env')).toHaveLength(0);
  expect(scanText('import gsap from "gsap"')).toHaveLength(0);
});
