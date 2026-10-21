#!/usr/bin/env node
/**
 * Resync a project's vendored scene kit with the snapshot this skill ships.
 *
 * The kit is vendored shadcn-style: every project owns a *copy* at
 * `src/presentation-kit/` rather than depending on a package. That copy goes
 * stale when the skill updates — there is no version to bump and nothing pulls
 * upstream fixes in. This script closes that gap. It diffs the skill's bundled
 * snapshot (`templates/bootstrap/src/presentation-kit/`, refreshed by
 * `claude plugin update`) against a project's vendored copy and, with --apply,
 * rewrites the project copy to match.
 *
 * Run it from the consuming project root:
 *
 *   node <skill-dir>/sync-kit.mjs              # report drift, exit 1 if any
 *   node <skill-dir>/sync-kit.mjs --apply      # write snapshot files into the copy
 *   node <skill-dir>/sync-kit.mjs path/to/kit  # target a non-default kit location
 *
 * The snapshot is the source of truth, so local edits to the vendored copy show
 * up as drift (expected — like `shadcn diff`). Review the printed diff, then
 * `--apply` and use your VCS (`git diff`) to re-apply any local theming the
 * update overwrote. Test files are ignored on both sides; the project copy is
 * never expected to carry them.
 */
import { lstatSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { spawnSync } from 'node:child_process'

const here = dirname(fileURLToPath(import.meta.url))
const SNAPSHOT = join(here, 'templates/bootstrap/src/presentation-kit')

const isTestFile = (path) => /\.test\./.test(path)

/**
 * Map<relPath, content> of every non-test file under `dir` (empty if absent).
 * Symlinks are skipped, never followed — a vendored kit is plain source, so a
 * link here is either a mistake or an attempt to make the tool read/write
 * through it to a file outside the kit.
 */
export function readKit(dir) {
  const out = new Map()
  const walk = (current) => {
    let entries
    try {
      entries = readdirSync(current, { withFileTypes: true })
    } catch {
      return // missing directory → empty kit
    }
    for (const entry of entries) {
      const full = join(current, entry.name)
      if (entry.isSymbolicLink()) continue
      if (entry.isDirectory()) walk(full)
      else if (!isTestFile(entry.name)) out.set(relative(dir, full), readFileSync(full, 'utf8'))
    }
  }
  walk(dir)
  return out
}

/**
 * Compare a `snapshot` kit against a `target` kit. The snapshot is the source of
 * truth:
 *   added     — in snapshot, missing from target (new upstream files)
 *   changed   — in both, differing content
 *   removed   — in target, gone from snapshot (dropped upstream, or local-only)
 *   identical — byte-identical in both
 */
export function diffKit(snapshot, target) {
  const added = []
  const changed = []
  const identical = []
  const removed = []
  for (const [path, content] of snapshot) {
    if (!target.has(path)) added.push(path)
    else if (target.get(path) !== content) changed.push(path)
    else identical.push(path)
  }
  for (const path of target.keys()) {
    if (!snapshot.has(path)) removed.push(path)
  }
  const sort = (a) => a.sort()
  return { added: sort(added), changed: sort(changed), removed: sort(removed), identical: sort(identical) }
}

/**
 * True if any path component of `rel`, walked under `base`, is a symlink.
 * Checking only the leaf is not enough: writeFileSync/mkdirSync traverse a
 * symlinked *parent* directory too, so a planted link anywhere along the path
 * could redirect the write outside the kit.
 */
function hasSymlinkComponent(base, rel) {
  let current = base
  for (const part of rel.split(/[\\/]+/).filter(Boolean)) {
    current = join(current, part)
    if (lstatSync(current, { throwIfNoEntry: false })?.isSymbolicLink()) return true
  }
  return false
}

/** Best-effort unified diff (target → snapshot) via git; empty string if git is absent. */
function diffAgainstTarget(targetDir, rel) {
  const res = spawnSync(
    'git',
    ['--no-pager', 'diff', '--no-index', '--', join(targetDir, rel), join(SNAPSHOT, rel)],
    { encoding: 'utf8' },
  )
  return res.stdout || ''
}

function list(label, files, sigil) {
  if (!files.length) return ''
  return `  ${label} (${files.length}):\n` + files.map((f) => `    ${sigil} ${f}`).join('\n') + '\n'
}

export function main(argv) {
  const apply = argv.includes('--apply')
  const positional = argv.filter((a) => a !== '--apply')
  const targetDir = resolve(positional[0] ?? 'src/presentation-kit')

  const snapshot = readKit(SNAPSHOT)
  if (snapshot.size === 0) {
    console.error(`No kit snapshot found at ${SNAPSHOT} — is the skill installed correctly?`)
    return 2
  }
  const target = readKit(targetDir)
  if (target.size === 0) {
    console.error(
      `No vendored kit at ${targetDir}.\n` +
        `Scaffold one first (the skill's scaffold step), or pass the kit path explicitly.`,
    )
    return 2
  }

  const { added, changed, removed, identical } = diffKit(snapshot, target)
  const drift = added.length + changed.length
  const targetLabel = relative(process.cwd(), targetDir) || '.'

  if (drift === 0 && removed.length === 0) {
    console.log(`✓ Vendored kit at ${targetLabel} is in sync with the snapshot (${identical.length} files).`)
    return 0
  }

  console.log(`Snapshot: ${SNAPSHOT}`)
  console.log(`Target:   ${targetDir}\n`)
  process.stdout.write(list('new upstream', added, '+'))
  process.stdout.write(list('changed', changed, '~'))
  process.stdout.write(list('target-only (left untouched)', removed, '?'))
  console.log('')

  const targetOnlyNote = removed.length
    ? `${removed.length} target-only file(s) left untouched — remove by hand if upstream dropped them.`
    : ''

  if (!apply) {
    if (drift === 0) {
      // Only local-only files differ; nothing to pull from upstream.
      console.log(`✓ ${targetLabel} is up to date with the snapshot (${identical.length} files).`)
      if (targetOnlyNote) console.log(`(${targetOnlyNote})`)
      return 0
    }
    for (const rel of changed) {
      const d = diffAgainstTarget(targetDir, rel)
      if (d) process.stdout.write(d.endsWith('\n') ? d : d + '\n')
    }
    console.log(`${drift} file(s) differ from the snapshot. Re-run with --apply to update ${targetLabel}.`)
    if (targetOnlyNote) console.log(`(${targetOnlyNote})`)
    return 1
  }

  const writes = [...added, ...changed]
  // Refuse to write through a symlink — writeFileSync/mkdirSync follow links, so
  // a planted symlink anywhere along a kit path could redirect a write outside
  // the project. Scan every path component first, before mutating anything, so
  // we fail clean.
  for (const rel of writes) {
    if (hasSymlinkComponent(targetDir, rel)) {
      console.error(`Refusing to write through symlink in path: ${join(targetDir, rel)}`)
      console.error('A vendored kit path component is a symbolic link; aborting so files outside the project are not touched.')
      return 2
    }
  }
  for (const rel of writes) {
    const dest = join(targetDir, rel)
    mkdirSync(dirname(dest), { recursive: true })
    writeFileSync(dest, snapshot.get(rel))
  }
  console.log(`Updated ${drift} file(s) in ${targetLabel}.`)
  if (targetOnlyNote) console.log(targetOnlyNote)
  console.log('Review with `git diff`, then rebuild and re-apply any local theming the update overwrote.')
  return 0
}

const invokedDirectly = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)
if (invokedDirectly) process.exit(main(process.argv.slice(2)))
