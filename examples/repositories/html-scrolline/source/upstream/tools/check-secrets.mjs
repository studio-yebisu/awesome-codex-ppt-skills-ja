#!/usr/bin/env node
/** 키·토큰이 추적 파일에 들어가지 않게 막는다(`npm run check`에 포함). 사용: node tools/check-secrets.mjs */
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const SECRET_PATTERNS = [
  ['openai/anthropic key', /\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}/],
  ['aws access key', /\bAKIA[0-9A-Z]{16}\b/],
  ['github token', /\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,})/],
  ['slack token', /\bxox[bap]-[A-Za-z0-9-]{10,}/],
  ['google api key', /\bAIza[0-9A-Za-z_-]{30,}/],
  [
    'key assignment',
    /\b(?:PEXELS|PIXABAY|ELEVENLABS|OPENAI|ANTHROPIC|GEMINI)_API_KEY\s*[:=]\s*['"]?[A-Za-z0-9_-]{12,}/,
  ],
  ['bearer token', /\bBearer\s+[A-Za-z0-9._-]{24,}/],
];
const SKIP = /(^|\/)(node_modules|out|media-src)\/|\.(png|jpe?g|webp|mp4|gif|woff2?|ttf|ico)$/i;

export function scanText(text) {
  const hits = [];
  text.split('\n').forEach((line, i) => {
    for (const [name, re] of SECRET_PATTERNS) if (re.test(line)) hits.push({ line: i + 1, name });
  });
  return hits;
}

export function checkSecrets(root) {
  const files = execFileSync('git', ['ls-files', '-co', '--exclude-standard'], {
    cwd: root,
    encoding: 'utf8',
  })
    .split('\n')
    .filter((f) => f && !SKIP.test(f));
  const violations = [];
  for (const file of files) {
    let text;
    try {
      text = readFileSync(path.join(root, file), 'utf8');
    } catch {
      continue;
    }
    for (const hit of scanText(text)) violations.push({ file, ...hit });
  }
  return { files: files.length, violations };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const { files, violations } = checkSecrets(path.join(path.dirname(fileURLToPath(import.meta.url)), '..'));
  for (const v of violations) console.log(`  ${v.file}:${v.line} ${v.name}`);
  console.log(`${violations.length ? 'FAIL' : 'ok  '} secrets 파일 ${files}, 위반 ${violations.length}`);
  process.exit(violations.length ? 1 : 0);
}
