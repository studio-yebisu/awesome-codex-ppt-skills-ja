// node scripts/publish-npm-skill.mjs [--prepared <目录>] [--dry-run [--output <目录>]]
// dry-run 生成本地 tarball,不查询或写入 registry。已发布版本在准备之前跳过。
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { prepareSkill, readPreparedSkill } from './prepare-skill.mjs';

const ROOT = path.resolve(import.meta.dirname, '..');
const PACKAGE_NAME = 'dashi-ppt-skill';
let preparedDirectory;
let outputDirectory;
let dryRun = false;
for (let index = 2; index < process.argv.length; index += 1) {
  const arg = process.argv[index];
  if (arg === '--dry-run') dryRun = true;
  else if (arg === '--prepared' && process.argv[index + 1]) preparedDirectory = path.resolve(process.argv[++index]);
  else if (arg === '--output' && process.argv[index + 1]) outputDirectory = path.resolve(process.argv[++index]);
  else throw new Error(`未知参数或缺少参数值: ${arg}`);
}
if (outputDirectory && !dryRun) throw new Error('--output 仅用于 --dry-run');

function run(cmd, args, options = {}) {
  return execFileSync(cmd, args, { encoding: 'utf8', ...options });
}

function isPublished(version) {
  try {
    return run('npm', ['view', `${PACKAGE_NAME}@${version}`, 'version', '--registry=https://registry.npmjs.org'], { stdio: 'pipe' }).trim() === version;
  } catch (error) {
    if (/\bE404\b/.test(String(error.stderr))) return false;
    throw error;
  }
}

function main() {
  let prepared = preparedDirectory ? readPreparedSkill(preparedDirectory) : null;
  const version = prepared?.version || JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8')).version;
  if (!/^\d+\.\d+\.\d+$/.test(version)) throw new Error(`非法版本号: ${version}`);
  if (!dryRun && isPublished(version)) {
    console.log(`npm 包 ${PACKAGE_NAME}@${version} 已发布,跳过。`);
    return;
  }

  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dashi-npm-release-'));
  try {
    prepared ||= prepareSkill(path.join(tempRoot, 'prepared'));
    const staging = path.join(tempRoot, 'package');
    fs.cpSync(prepared.skillRoot, path.join(staging, 'skill'), { recursive: true });
    fs.mkdirSync(path.join(staging, 'bin'), { recursive: true });
    fs.copyFileSync(path.join(prepared.root, 'npm-dist/install.mjs'), path.join(staging, 'bin/install.mjs'));
    fs.copyFileSync(path.join(prepared.root, 'LICENSE'), path.join(staging, 'LICENSE'));
    fs.writeFileSync(path.join(staging, 'package.json'), `${JSON.stringify({
      name: PACKAGE_NAME,
      version,
      description: 'Dashi PPT skill installer — offline-editable HTML decks with PPTX/PDF export. 国内可经 npmmirror 安装。',
      bin: { 'dashi-ppt-skill': 'bin/install.mjs' },
      files: ['bin', 'skill', 'LICENSE'],
      license: 'AGPL-3.0-only',
      repository: { type: 'git', url: 'git+https://github.com/chuspeeism/dashi-ppt-skill.git' },
      homepage: 'https://github.com/chuspeeism/dashi-ppt-skill#readme',
      keywords: ['agent-skill', 'ppt', 'presentation', 'claude', 'codex'],
      engines: { node: '>=20' },
    }, null, 2)}\n`);
    fs.writeFileSync(path.join(staging, 'README.md'), [
      '# dashi-ppt-skill',
      '',
      'Installer package for the [Dashi PPT](https://github.com/chuspeeism/dashi-ppt-skill) agent skill.',
      '',
      '```bash',
      '# International',
      'npx dashi-ppt-skill',
      '# 中国大陆(走 npmmirror 镜像)',
      'npx --registry=https://registry.npmmirror.com dashi-ppt-skill',
      '```',
      '',
      'A fresh install prefers the detected ~/.agents/skills directory; an existing single installation is updated in place. If multiple locations are ambiguous, choose one with --dir or explicitly update all with --all.',
      '',
      'Options: `--dir <skills-root>` to target one skills directory, `--all` to update all detected locations, `--list` to show detected locations.',
      '',
      'Licensed under AGPL-3.0; the bundled `html-deck-to-pptx` export engine is proprietary, licensed for use only as part of this skill (see its LICENSE). Installer source: `npm-dist/` in the repository.',
      '',
    ].join('\n'));

    if (dryRun) {
      const destination = outputDirectory || tempRoot;
      fs.mkdirSync(destination, { recursive: true });
      const [packed] = JSON.parse(run('npm', ['pack', '--json', '--pack-destination', destination], { cwd: staging, stdio: 'pipe' }));
      console.log(JSON.stringify({ dryRun: true, version, prepared: prepared.root, source: prepared.source,
        tarball: outputDirectory ? path.join(destination, packed.filename) : null,
        shasum: packed.shasum, integrity: packed.integrity, files: packed.files.length }, null, 2));
      return;
    }

    const output = run('npm', ['publish', '--access', 'public', '--registry=https://registry.npmjs.org'], { cwd: staging, stdio: 'pipe' });
    console.log(output.trim().split('\n').slice(-3).join('\n'));
    console.log(`npm 包 ${PACKAGE_NAME}@${version} 发布完成; Skill SHA-256 ${prepared.source.contentSha256}。`);
    fetch(`https://registry-direct.npmmirror.com/-/package/${PACKAGE_NAME}/syncs`, { method: 'PUT' })
      .then((res) => console.log(`npmmirror 同步已触发(${res.status})`))
      .catch(() => console.log('npmmirror 同步触发失败(将由镜像定时同步)'));
  } finally {
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
}

main();
