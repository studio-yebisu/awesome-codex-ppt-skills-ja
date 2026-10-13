#!/usr/bin/env node
/**
 * 두 모자 검사(plan/ARCHITECTURE.md §8, CONTRACTS C17).
 *   node tools/check-hat.mjs <base>..<head>
 * 커밋마다 trailer 'Hat: feature|refactor|none' 필수(merge 커밋 제외).
 *   feature  = *.test.* 추가·수정 1개 이상
 *   refactor = 기존 *.test.* 수정·삭제 0(이름 변경 R100만 허용)
 *   none     = 문서·계획·자산 커밋: 코드(*.js·*.mjs·*.css) 변경 0
 */
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const git = (cwd, args) => execFileSync('git', args, { cwd, encoding: 'utf8' });
const TEST = /\.test\.m?js$/;
const CODE = /\.(m?js|css)$/;

/** @returns {Array<{ commit: string, message: string }>} */
export function checkHat(root, range) {
  const out = [];
  const commits = git(root, ['rev-list', '--no-merges', '--reverse', range]).split('\n').filter(Boolean);
  for (const c of commits) {
    const body = git(root, ['show', '-s', '--format=%B', c]);
    const hat = body.match(/^Hat:\s*(feature|refactor|none)\s*$/m)?.[1];
    if (!hat) {
      out.push({ commit: c, message: 'Hat: trailer 없음' });
      continue;
    }
    const changes = git(root, ['diff-tree', '--no-commit-id', '--root', '-r', '-M', '--name-status', c])
      .split('\n')
      .filter(Boolean)
      .map((l) => l.split('\t'));
    const tests = changes.filter((p) => TEST.test(p.at(-1)));
    if (hat === 'none') {
      const code = changes.filter((p) => p.slice(1).some((file) => CODE.test(file)));
      if (code.length)
        out.push({ commit: c, message: `none인데 코드 변경: ${code.map((p) => p.at(-1)).join(', ')}` });
      continue;
    }
    if (hat === 'feature' && !tests.some(([s]) => s === 'A' || s === 'M'))
      out.push({ commit: c, message: 'feature인데 테스트 추가·수정 없음' });
    if (hat === 'refactor') {
      const bad = tests.filter(([s]) => s === 'M' || s === 'D' || (s.startsWith('R') && s !== 'R100'));
      if (bad.length)
        out.push({
          commit: c,
          message: `refactor인데 기존 테스트 변경: ${bad.map((p) => p.at(-1)).join(', ')}`,
        });
    }
  }
  return out;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const range = process.argv[2];
  if (!range) {
    console.error('사용: node tools/check-hat.mjs <base>..<head>');
    process.exit(2);
  }
  const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
  const r = checkHat(root, range);
  for (const x of r) console.log(`${x.commit.slice(0, 8)} ${x.message}`);
  console.log(`check-hat: 위반 ${r.length}`);
  process.exit(r.length ? 1 : 0);
}
