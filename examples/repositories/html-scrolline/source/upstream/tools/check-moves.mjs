#!/usr/bin/env node
/**
 * move 정적 계약 검사(CONTRACTS C5·C10).
 *   node tools/check-moves.mjs [root]
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MOVE_EXT = /\.js$/;
const TEST_FILE = /\.test\.js$/;
const THREE_D_PROPS =
  /\b(?:rotateX|rotateY|rotationX|rotationY|z|translateZ|transformPerspective|perspective)\b|preserve-3d/g;
const DIRECT_GSAP = /\b(?:import|export)\s+(?:[\s\S]*?\s+from\s+)?['"]gsap['"]/g;
const GSAP_PLUGIN = /\b(?:import|export)\s+(?:[\s\S]*?\s+from\s+)?['"]gsap\/[^'"]+['"]/g;

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(file, out);
    else if (MOVE_EXT.test(entry.name) && !TEST_FILE.test(entry.name)) out.push(file);
  }
  return out;
}

function withoutComments(code) {
  return code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:'"`])\/\/.*$/gm, '$1');
}

function matches(code, expression) {
  expression.lastIndex = 0;
  return expression.test(code);
}

/**
 * @param {string} root 레포 루트
 * @returns {{ files: number, violations: Array<{ file: string, token: string, rule: string, message: string }> }}
 */
export function checkMoves(root) {
  const files = walk(path.join(root, 'moves'));
  const violations = [];
  const add = (file, token, rule, message) => violations.push({ file, token, rule, message });

  for (const abs of files) {
    const file = path.relative(root, abs).split(path.sep).join('/');
    const code = withoutComments(fs.readFileSync(abs, 'utf8'));
    const family = file.split('/')[1];
    const exportedFamily = code.match(/\bfamily\s*:\s*['"]([^'"]+)['"]/)?.[1];

    if (family !== 'camera' && matches(code, THREE_D_PROPS)) {
      add(file, code.match(THREE_D_PROPS)[0], 'C10', '3D 속성은 camera family에서만 사용 가능');
    }
    if (/\.from\s*\(/.test(code)) add(file, '.from(', 'C5', 'tl.from() 사용 금지');
    if (/\bvar\s*\(/.test(code)) add(file, 'var(', 'C5', 'CSS var() 직접 읽기 금지; 색은 ctx.colors 사용');
    if (/\b(?:Math\.random|Date\.now|performance\.now)\b/.test(code)) {
      add(
        file,
        code.match(/\b(?:Math\.random|Date\.now|performance\.now)\b/)[0],
        'C5',
        '비결정적 시간·난수 사용 금지',
      );
    }
    if (matches(code, DIRECT_GSAP)) add(file, 'gsap', 'C1', 'gsap 직접 import 금지; ctx.gsap 사용');
    if (matches(code, GSAP_PLUGIN)) add(file, 'gsap/*', 'C1', '플러그인 직접 import 금지; ctx.plugins 사용');
    if (exportedFamily && exportedFamily !== family) {
      add(file, exportedFamily, 'C5', `family 값은 폴더명과 같아야 함: ${family}`);
    }
  }

  return { files: files.length, violations };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const root = path.resolve(process.argv[2] || path.join(path.dirname(fileURLToPath(import.meta.url)), '..'));
  const result = checkMoves(root);
  for (const violation of result.violations) {
    console.log(`${violation.rule} ${violation.file}  '${violation.token}'  ${violation.message}`);
  }
  console.log(
    `${result.violations.length ? 'FAIL' : 'ok  '} moves  파일 ${result.files}, 위반 ${result.violations.length}`,
  );
  process.exit(result.violations.length ? 1 : 0);
}
