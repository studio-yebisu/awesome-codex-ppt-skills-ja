#!/usr/bin/env node
/**
 * 모듈마다 테스트 존재 검사(plan/CONTRACTS.md C17 check-tests).
 * engine/**·moves/**의 .js(테스트·index.js·types.js·constants.js·testing.js·moves/_shared/·__fixtures__ 제외)는
 * 옆에 <name>.test.js가 있어야 한다. 첫 30줄 안에 '@stub'이 있으면 면제.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const EXEMPT = new Set(['index.js', 'types.js', 'constants.js', 'testing.js']);
const SKIP_DIRS = new Set(['node_modules', 'dist', '__fixtures__', '_shared']);

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.js') && !e.name.endsWith('.test.js') && !EXEMPT.has(e.name)) out.push(p);
  }
  return out;
}

/** @returns {{ checked: number, stubs: string[], missing: string[] }} */
export function checkTests(root) {
  const files = ['engine', 'moves'].flatMap((d) => walk(path.join(root, d)));
  const stubs = [];
  const missing = [];
  for (const f of files) {
    const rel = path.relative(root, f).split(path.sep).join('/');
    const head = fs.readFileSync(f, 'utf8').split('\n').slice(0, 30).join('\n');
    if (head.includes('@stub')) stubs.push(rel);
    else if (!fs.existsSync(f.replace(/\.js$/, '.test.js'))) missing.push(rel);
  }
  return { checked: files.length, stubs, missing };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const root = path.resolve(process.argv[2] || path.join(path.dirname(fileURLToPath(import.meta.url)), '..'));
  const r = checkTests(root);
  for (const m of r.missing) console.log(`테스트 없음: ${m}`);
  console.log(`check-tests: 모듈 ${r.checked}, 스텁 ${r.stubs.length}, 테스트 누락 ${r.missing.length}`);
  process.exit(r.missing.length ? 1 : 0);
}
