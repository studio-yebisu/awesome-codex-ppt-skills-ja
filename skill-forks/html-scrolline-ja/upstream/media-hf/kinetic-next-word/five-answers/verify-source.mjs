import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../../..');
const source = readFileSync(resolve(root, 'decks/kinetic-next-word/assets/runs/haiku-5runs.md'), 'utf8');
const html = readFileSync(resolve(import.meta.dirname, 'index.html'), 'utf8');
const expected = [...source.matchAll(/^## run \d+ .*\n([^\n]+)$/gm)].map((match) => match[1]);
const literal = html.match(/const answers = \[([\s\S]*?)\n      \];/)?.[1] ?? '';
const actual = [...literal.matchAll(/^\s*"(.*)"[,]?$/gm)].map((match) => JSON.parse(`"${match[1]}"`));
if (expected.length !== 5 || actual.length !== 5 || expected.some((line, index) => line !== actual[index])) {
  throw new Error(`source mismatch: expected ${expected.length} exact runs, found ${actual.length} composition strings`);
}
console.log('five source strings match haiku-5runs.md exactly');
