#!/usr/bin/env node
/**
 * 의존 방향 검사(plan/CONTRACTS.md C1 R0~R5).
 *   node tools/check-deps.mjs [root] [--json]
 * 층: engine(0) < moves(1) < concepts(2) < decks(3) < site(4). tools·루트 설정은 층 밖.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const LAYERS = ['engine', 'moves', 'concepts', 'decks', 'site'];
const RANK = Object.fromEntries(LAYERS.map((l, i) => [l, i]));
const SKIP_DIRS = new Set(['node_modules', 'dist', '__fixtures__', '.git', '.cache', 'out']);
const SRC_EXT = /\.(m?js)$/;
const RESOLVABLE_EXT = /\.(m?js|css|json|ya?ml|svg|png|jpe?g|webp|avif|mp4|woff2?)$/;

/** 다른 층에서 들어올 수 있는 공개 진입점(R2) */
function isPublicEntry(rel, fromTest) {
  if (rel === 'engine/index.js' || rel === 'engine/engine.css' || rel === 'moves/index.js') return true;
  if (rel === 'engine/testing.js') return fromTest;
  return /^concepts\/[^/]+\/(index\.js|tokens\.css|layout\.css)$/.test(rel);
}

/** 외부 패키지 허용 위치(R5). true = 허용 */
const PACKAGE_RULES = {
  gsap: (rel) => rel.startsWith('engine/'),
  lenis: (rel) => rel === 'engine/scroll.js',
  vitest: (rel, isTest) => isTest,
  'happy-dom': (rel, isTest) => isTest || rel === 'engine/testing.js',
  yaml: () => false,
  three: () => false,
};

const isTestFile = (rel) => /\.test\.m?js$/.test(rel);

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (SRC_EXT.test(e.name)) out.push(p);
  }
  return out;
}

/** import·export from·동적 import 지정자 목록. 주석 안의 것은 무시 */
export function specifiers(code) {
  const src = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:'"`])\/\/.*$/gm, '$1');
  const out = [];
  const re =
    /\bimport\s+(?:[\w*{}\s,$]+\s+from\s+)?['"]([^'"]+)['"]|\bexport\s+[\w*{}\s,$]+\s+from\s+['"]([^'"]+)['"]|\bimport\s*\(\s*['"]([^'"]+)['"]\s*\)/g;
  let m;
  while ((m = re.exec(src))) out.push(m[1] ?? m[2] ?? m[3]);
  return out;
}

const layerOf = (rel) => {
  const top = rel.split('/')[0];
  return top in RANK ? top : null;
};
const packageName = (spec) =>
  spec.startsWith('@') ? spec.split('/').slice(0, 2).join('/') : spec.split('/')[0];

/**
 * @param {string} root 레포 루트
 * @returns {{ files: number, edges: number, violations: Array<{ file: string, spec: string, rule: string, message: string }> }}
 */
export function checkDeps(root) {
  const files = LAYERS.flatMap((l) => walk(path.join(root, l)));
  const violations = [];
  const graph = new Map();
  let edges = 0;
  const v = (file, spec, rule, message) => violations.push({ file, spec, rule, message });

  for (const abs of files) {
    const rel = path.relative(root, abs).split(path.sep).join('/');
    const layer = layerOf(rel);
    const test = isTestFile(rel);
    const deps = [];
    graph.set(rel, deps);
    for (const spec of specifiers(fs.readFileSync(abs, 'utf8'))) {
      if (spec.startsWith('.') || spec.startsWith('/')) {
        if (!RESOLVABLE_EXT.test(spec.replace(/\?.*$/, ''))) {
          v(rel, spec, 'R0', '상대 import는 확장자를 명시해야 함');
          continue;
        }
        const target = path
          .relative(root, path.resolve(path.dirname(abs), spec.replace(/\?.*$/, '')))
          .split(path.sep)
          .join('/');
        const tLayer = layerOf(target);
        if (!tLayer) {
          v(
            rel,
            spec,
            'R1',
            target.startsWith('tools/')
              ? '층 안에서 tools/ import 금지'
              : `층 밖 파일 import 금지: ${target}`,
          );
          continue;
        }
        if (RANK[tLayer] > RANK[layer]) {
          v(rel, spec, 'R1', `상향 의존 금지: ${layer} → ${tLayer}`);
          continue;
        }
        if (tLayer !== layer) {
          if (!isPublicEntry(target, test)) v(rel, spec, 'R2', `다른 층은 공개 진입점만: ${target}`);
        } else {
          const a = rel.split('/');
          const b = target.split('/');
          const atLayerRoot = a.length === 2; // moves/index.js 같은 층 루트 파일
          const sibling = a[1] !== b[1];
          if (
            sibling &&
            !atLayerRoot &&
            ['concepts', 'decks', 'moves'].includes(layer) &&
            !(layer === 'moves' && b[1] === '_shared')
          ) {
            v(rel, spec, 'R4', `형제 격리 위반: ${a.slice(0, 2).join('/')} → ${b.slice(0, 2).join('/')}`);
          }
        }
        if (SRC_EXT.test(target)) {
          deps.push(target);
          edges++;
        }
        continue;
      }
      if (spec.startsWith('virtual:')) continue;
      if (spec.startsWith('node:')) {
        if (!test) v(rel, spec, 'R5', 'node: 내장 모듈은 tools·테스트에서만');
        continue;
      }
      const pkg = packageName(spec);
      const rule = PACKAGE_RULES[pkg];
      if (!rule) v(rel, spec, 'R5', `허용 목록에 없는 패키지: ${pkg}`);
      else if (!rule(rel, test)) v(rel, spec, 'R5', `${pkg}는 이 위치에서 import 금지`);
    }
  }

  // R3 순환: Tarjan SCC
  let index = 0;
  const idx = new Map();
  const low = new Map();
  const stack = [];
  const on = new Set();
  const strong = (n) => {
    idx.set(n, index);
    low.set(n, index++);
    stack.push(n);
    on.add(n);
    for (const w of graph.get(n) || []) {
      if (!graph.has(w)) continue;
      if (!idx.has(w)) {
        strong(w);
        low.set(n, Math.min(low.get(n), low.get(w)));
      } else if (on.has(w)) low.set(n, Math.min(low.get(n), idx.get(w)));
    }
    if (low.get(n) === idx.get(n)) {
      const comp = [];
      let w;
      do {
        w = stack.pop();
        on.delete(w);
        comp.push(w);
      } while (w !== n);
      const selfLoop = comp.length === 1 && (graph.get(n) || []).includes(n);
      if (comp.length > 1 || selfLoop)
        v(comp.sort()[0], comp.sort().join(' → '), 'R3', `순환 의존 ${comp.length}개 파일`);
    }
  };
  for (const n of graph.keys()) if (!idx.has(n)) strong(n);

  return { files: files.length, edges, violations };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const args = process.argv.slice(2);
  const root = path.resolve(
    args.find((a) => !a.startsWith('--')) || path.join(path.dirname(fileURLToPath(import.meta.url)), '..'),
  );
  const res = checkDeps(root);
  if (args.includes('--json')) console.log(JSON.stringify(res, null, 2));
  else {
    for (const x of res.violations) console.log(`${x.rule} ${x.file}  '${x.spec}'  ${x.message}`);
    console.log(`check-deps: 파일 ${res.files}, 내부 간선 ${res.edges}, 위반 ${res.violations.length}`);
  }
  process.exit(res.violations.length ? 1 : 0);
}
