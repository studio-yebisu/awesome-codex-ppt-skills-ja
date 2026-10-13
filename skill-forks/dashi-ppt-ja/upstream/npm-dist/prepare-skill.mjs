#!/usr/bin/env node
// 本地准备: npm run skill:prepare -- <目录>。两个 publisher 用 --prepared <目录> 复用。
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(import.meta.dirname, '..');
export const SKILL_SUBDIR = path.join('skills', 'dashi-ppt');
const SOURCE_RECORD = 'project/distribution-source.json';
// npm 不分发这两个点文件; .npmrc 在安装时由 npmrc.template 恢复。
const FINGERPRINT_EXCLUDES = [SOURCE_RECORD, '.gitignore', 'project/.npmrc'];
const SOURCE_DIRS = ['src/', 'scripts/', 'packages/', 'assets/', 'references/', 'i18n/'];
const SOURCE_FILES = new Set(['package.json', 'package-lock.json', 'SKILL.md', 'README.md', 'layout-manifest.json', 'LICENSE']);

function hashFiles(root, files) {
  const hash = createHash('sha256');
  for (const file of files.sort()) {
    hash.update(file + '\0');
    hash.update(createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest());
  }
  return hash.digest('hex');
}

function skillFingerprint(skillRoot) {
  const files = [];
  function visit(relativeDir) {
    for (const entry of fs.readdirSync(path.join(skillRoot, relativeDir), { withFileTypes: true })) {
      const relativePath = path.posix.join(relativeDir, entry.name);
      if (FINGERPRINT_EXCLUDES.includes(relativePath)) continue;
      if (entry.isDirectory()) visit(relativePath);
      else files.push(relativePath);
    }
  }
  visit('');
  return hashFiles(skillRoot, files);
}

function sourceState() {
  const git = (...args) => execFileSync('git', args, { cwd: ROOT, encoding: 'utf8' });
  const files = git('ls-files', '-z', '--cached', '--others', '--exclude-standard').split('\0').filter(file =>
    file && (SOURCE_FILES.has(file) || SOURCE_DIRS.some(dir => file.startsWith(dir)))
    && file !== 'assets/vendor/editable-pptx-browser.js'
    && !file.startsWith('packages/html-deck-to-pptx/dist/')
    && fs.existsSync(path.join(ROOT, file))
    && fs.statSync(path.join(ROOT, file)).isFile());
  return {
    commit: git('rev-parse', 'HEAD').trim(),
    dirty: Boolean(git('status', '--porcelain', '--untracked-files=all').trim()),
    inputSha256: hashFiles(ROOT, [...new Set(files)]),
  };
}

export function readPreparedSkill(directory) {
  const root = path.resolve(directory);
  const skillRoot = path.join(root, SKILL_SUBDIR);
  const source = JSON.parse(fs.readFileSync(path.join(skillRoot, SOURCE_RECORD), 'utf8'));
  const version = JSON.parse(fs.readFileSync(path.join(skillRoot, 'project/package.json'), 'utf8')).version;
  if (source.version !== version || source.contentSha256 !== skillFingerprint(skillRoot)
    || source.npmFilesSha256 !== hashFiles(root, ['npm-dist/install.mjs', 'LICENSE'])) {
    throw new Error(`准备目录内容与来源记录不符,请重新运行 skill:prepare: ${root}`);
  }
  return { root, skillRoot, version, source };
}

export function prepareSkill(directory) {
  const root = path.resolve(directory);
  const skillRoot = path.join(root, SKILL_SUBDIR);
  const source = sourceState();
  const recordPath = path.join(skillRoot, SOURCE_RECORD);
  if (fs.existsSync(recordPath)) {
    const previous = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
    if (previous.source.inputSha256 === source.inputSha256 && previous.source.commit === source.commit
      && previous.source.dirty === source.dirty) {
      const prepared = readPreparedSkill(root);
      console.log(`Reused prepared skill v${prepared.version}: ${root}`);
      return prepared;
    }
  }
  fs.mkdirSync(root, { recursive: true });
  execFileSync(process.execPath, [path.join(ROOT, 'scripts/sync-skill.mjs')], {
    cwd: ROOT,
    stdio: 'inherit',
    env: { ...process.env, DASHI_PPT_SKILL_ROOT: skillRoot, DASHI_PPT_SKIP_SOURCE_SYNC: '1' },
  });
  const npmDir = path.join(root, 'npm-dist');
  fs.mkdirSync(npmDir, { recursive: true });
  for (const [from, to] of [
    ['scripts/npm-dist/install.mjs', 'install.mjs'],
    ['scripts/publish-npm-skill.mjs', 'publish-npm-skill.mjs'],
    ['scripts/prepare-skill.mjs', 'prepare-skill.mjs'],
  ]) fs.copyFileSync(path.join(ROOT, from), path.join(npmDir, to));
  fs.writeFileSync(path.join(npmDir, 'README.md'), '# npm-dist\n\nInstaller and release preparation sources, copied from the development repository for audit. Run the release scripts in the development repository.\n');
  fs.copyFileSync(path.join(ROOT, 'LICENSE'), path.join(root, 'LICENSE'));
  const version = JSON.parse(fs.readFileSync(path.join(skillRoot, 'project/package.json'), 'utf8')).version;
  const record = {
    schemaVersion: 1,
    version,
    source,
    contentSha256: skillFingerprint(skillRoot),
    fingerprintExcludes: FINGERPRINT_EXCLUDES,
    npmFilesSha256: hashFiles(root, ['npm-dist/install.mjs', 'LICENSE']),
  };
  fs.writeFileSync(recordPath, JSON.stringify(record, null, 2) + '\n');
  console.log(`Prepared skill v${version}: ${root}\nDEV ${source.commit}${source.dirty ? ' + working-tree changes' : ''}\nSkill SHA-256 ${record.contentSha256}`);
  return { root, skillRoot, version, source: record };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const directory = process.argv[2];
  if (!directory || directory.startsWith('-') || process.argv.length > 3) {
    throw new Error('用法: npm run skill:prepare -- <准备目录>');
  }
  prepareSkill(directory);
}
