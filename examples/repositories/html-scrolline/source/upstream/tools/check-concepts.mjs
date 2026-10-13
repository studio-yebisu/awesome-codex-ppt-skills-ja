#!/usr/bin/env node
/**
 * 컨셉 CSS 범위 검사(CONTRACTS C11 v2.2, 계약 요청 #49).
 *   node tools/check-concepts.mjs [root]
 * concepts/<id>/layout.css: 선택자는 전부 `.sl-concept-<id>` 범위, 색은 var(--sl-*)만(16진·색 함수·색 이름 금지),
 * `--sl-*` 정의 금지(컨셉 고유 변수는 `--<id>-*`), `!important`·`@import` 금지, @keyframes 이름은 `<id>-`로 시작.
 * decks/<deck>/main.js: 컨셉에 layout.css가 있으면 tokens.css 다음에 import, 다른 컨셉 layout.css는 import 금지,
 * boot에 `mode: import.meta.env.SCROLLINE_MODE`(C15, export가 이 값으로 export 모드를 켠다).
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const AT_ALLOWED = new Set(['media', 'supports', 'container', 'keyframes']);
const COLOR_FN = /\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(/i;
const HEX = /#[0-9a-f]{3,8}\b/i;
// CSS 색 이름(transparent·currentColor는 허용).
const COLOR_NAMES = new Set(
  (
    'aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood ' +
    'cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray ' +
    'darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen ' +
    'darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue ' +
    'firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew ' +
    'hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan ' +
    'lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray ' +
    'lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue ' +
    'mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred ' +
    'midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid ' +
    'palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple ' +
    'rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue ' +
    'slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white ' +
    'whitesmoke yellow yellowgreen'
  ).split(' '),
);

/** 주석 제거(문자열 안 `/*`는 CSS에서 드묾 — 무시). 줄 번호 유지를 위해 개행은 남긴다. */
function stripComments(css) {
  return css.replace(/\/\*[\s\S]*?\*\//g, (c) => c.replace(/[^\n]/g, ' '));
}

/**
 * 아주 작은 CSS 블록 파서. 결과 = [{ kind:'rule', prelude, body, line } | { kind:'at', name, prelude, children, body, line }]
 * 따옴표 안 중괄호는 건너뛴다.
 * @param {string} css
 */
export function parseBlocks(css, offset = 0, base = css) {
  const out = [];
  let i = 0;
  let start = 0;
  const lineAt = (at) => base.slice(0, offset + at).split('\n').length;
  while (i < css.length) {
    const ch = css[i];
    if (ch === '"' || ch === "'") {
      const end = css.indexOf(ch, i + 1);
      i = end < 0 ? css.length : end + 1;
    } else if (ch === ';' && css.slice(start, i).trim().startsWith('@')) {
      // 블록 없는 at-rule(@import 등)
      const prelude = css.slice(start, i).trim();
      const [, name = '', rest = ''] = prelude.match(/^@([\w-]+)\s*([\s\S]*)$/) ?? [];
      out.push({ kind: 'at', name: name.toLowerCase(), prelude: rest, children: [], body: '', line: lineAt(start) });
      start = i += 1;
    } else if (ch === '{') {
      let depth = 1;
      let j = i + 1;
      while (j < css.length && depth) {
        const c = css[j];
        if (c === '"' || c === "'") {
          const end = css.indexOf(c, j + 1);
          j = end < 0 ? css.length : end + 1;
          continue;
        }
        if (c === '{') depth += 1;
        else if (c === '}') depth -= 1;
        j += 1;
      }
      const prelude = css.slice(start, i).trim();
      const body = css.slice(i + 1, j - 1);
      const line = lineAt(start + (css.slice(start, i).length - css.slice(start, i).trimStart().length));
      if (prelude.startsWith('@')) {
        const [, name = '', rest = ''] = prelude.match(/^@([\w-]+)\s*([\s\S]*)$/) ?? [];
        const lower = name.toLowerCase();
        const nested = lower === 'keyframes' || lower === 'font-face' ? [] : parseBlocks(body, offset + i + 1, base);
        out.push({ kind: 'at', name: lower, prelude: rest.trim(), children: nested, body, line });
      } else {
        out.push({ kind: 'rule', prelude, body, line });
      }
      start = i = j;
    } else {
      i += 1;
    }
  }
  return out;
}

/** 쉼표로 선택자 나누기(괄호 안 쉼표는 유지: `:is(a, b)`). */
export function splitSelectors(prelude) {
  const out = [];
  let depth = 0;
  let cur = '';
  for (const ch of prelude) {
    if (ch === '(' || ch === '[') depth += 1;
    else if (ch === ')' || ch === ']') depth -= 1;
    if (ch === ',' && depth === 0) {
      out.push(cur.trim());
      cur = '';
    } else cur += ch;
  }
  if (cur.trim()) out.push(cur.trim());
  return out.map((s) => s.replace(/\s+/g, ' '));
}

/** 선언 목록 → [{ prop, value }] */
function declarations(body) {
  return body
    .split(';')
    .map((d) => d.trim())
    .filter(Boolean)
    .map((d) => {
      const at = d.indexOf(':');
      return at < 0 ? { prop: d, value: '' } : { prop: d.slice(0, at).trim(), value: d.slice(at + 1).trim() };
    });
}

/** 값 안 색 리터럴(따옴표 문자열·url()은 제외). */
export function colorLiteral(value) {
  const bare = value.replace(/(['"])[\s\S]*?\1/g, '""').replace(/url\([^)]*\)/gi, 'url()');
  const hex = bare.match(HEX);
  if (hex) return hex[0];
  const fn = bare.match(COLOR_FN);
  if (fn) return fn[0].replace(/\s+/g, '');
  const name = bare
    .replace(/var\([^)]*\)/g, ' ')
    .split(/[^a-zA-Z-]+/)
    .find((w) => COLOR_NAMES.has(w.toLowerCase()));
  return name ?? null;
}

/**
 * layout.css 1개 검사.
 * @param {string} id 컨셉 id
 * @param {string} css
 * @param {string} file 보고용 경로
 */
export function checkLayoutCss(id, css, file) {
  const violations = [];
  const add = (line, token, message) => violations.push({ file, line, token, rule: 'C11', message });
  const scope = new RegExp(`^\\.sl-concept-${id.replace(/[-]/g, '\\-')}(?![\\w-])`);
  const visit = (blocks) => {
    for (const b of blocks) {
      if (b.kind === 'at') {
        if (!AT_ALLOWED.has(b.name)) add(b.line, `@${b.name}`, `layout.css에서 @${b.name} 금지`);
        else if (b.name === 'keyframes' && !b.prelude.startsWith(`${id}-`))
          add(b.line, b.prelude, `@keyframes 이름은 '${id}-'로 시작해야 함`);
        if (b.name === 'keyframes') checkDecls(b.line, b.body.replace(/[^{};]*\{|\}/g, ';'));
        else visit(b.children);
        continue;
      }
      for (const sel of splitSelectors(b.prelude))
        if (!scope.test(sel)) add(b.line, sel, `선택자는 .sl-concept-${id} 범위 안이어야 함`);
      checkDecls(b.line, b.body);
    }
  };
  const checkDecls = (line, body) => {
    for (const { prop, value } of declarations(body)) {
      if (/!\s*important/i.test(value)) add(line, `${prop}: !important`, '!important 금지(move의 inline 값을 이김)');
      if (prop.startsWith('--sl-')) add(line, prop, `--sl-* 변수는 tokens.css·엔진 몫, 컨셉 고유 변수는 --${id}-*`);
      else if (prop.startsWith('--') && !prop.startsWith(`--${id}-`))
        add(line, prop, `컨셉 고유 변수 이름은 --${id}-*`);
      const color = colorLiteral(value);
      if (color) add(line, `${prop}: ${color}`, '색은 var(--sl-*)만(tokens.css에서 정의)');
    }
  };
  visit(parseBlocks(stripComments(css)));
  return violations;
}

/**
 * @param {string} root 레포 루트
 * @returns {{ concepts: number, layouts: number, violations: Array<{ file: string, line?: number, token: string, rule: string, message: string }> }}
 */
export function checkConcepts(root) {
  const conceptsDir = path.join(root, 'concepts');
  const ids = fs.existsSync(conceptsDir)
    ? fs.readdirSync(conceptsDir, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name)
    : [];
  const violations = [];
  const layouts = new Set();
  for (const id of ids) {
    const rel = `concepts/${id}/layout.css`;
    const abs = path.join(root, rel);
    if (!fs.existsSync(abs)) continue;
    layouts.add(id);
    violations.push(...checkLayoutCss(id, fs.readFileSync(abs, 'utf8'), rel));
  }

  const decksDir = path.join(root, 'decks');
  const decks = fs.existsSync(decksDir)
    ? fs.readdirSync(decksDir, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name)
    : [];
  for (const deck of decks) {
    const rel = `decks/${deck}/main.js`;
    const abs = path.join(root, rel);
    if (!fs.existsSync(abs)) continue;
    const code = fs.readFileSync(abs, 'utf8');
    const concept = code.match(/concepts\/([^/'"]+)\/index\.js/)?.[1];
    if (/\bboot\s*\(/.test(code) && !/mode:\s*import\.meta\.env\.SCROLLINE_MODE/.test(code))
      violations.push({ file: rel, token: 'mode', rule: 'C15', message: 'boot에 mode: import.meta.env.SCROLLINE_MODE 누락(MP4 export 불가)' });
    const imported = [...code.matchAll(/import\s+['"][^'"]*concepts\/([^/'"]+)\/layout\.css['"]/g)].map((m) => m[1]);
    for (const other of imported.filter((c) => c !== concept))
      violations.push({ file: rel, token: `concepts/${other}/layout.css`, rule: 'C11', message: '다른 컨셉 layout.css import 금지' });
    if (concept && layouts.has(concept)) {
      const tokensAt = code.search(new RegExp(`concepts/${concept}/tokens\\.css`));
      const layoutAt = code.search(new RegExp(`concepts/${concept}/layout\\.css`));
      if (layoutAt < 0)
        violations.push({ file: rel, token: `concepts/${concept}/layout.css`, rule: 'C11', message: '컨셉 layout.css import 누락' });
      else if (tokensAt > layoutAt)
        violations.push({ file: rel, token: 'layout.css', rule: 'C11', message: 'layout.css는 tokens.css 다음에 import' });
    }
  }
  return { concepts: ids.length, layouts: layouts.size, violations };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const root = process.argv[2] ?? path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
  const result = checkConcepts(root);
  for (const x of result.violations)
    console.log(`  ${x.rule} ${x.file}${x.line ? `:${x.line}` : ''} '${x.token}' ${x.message}`);
  console.log(`concepts ${result.concepts}, layout ${result.layouts}, 위반 ${result.violations.length}`);
  process.exit(result.violations.length ? 1 : 0);
}
