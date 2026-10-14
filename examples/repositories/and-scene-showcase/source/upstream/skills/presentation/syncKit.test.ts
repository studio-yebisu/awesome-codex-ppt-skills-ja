import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, unlinkSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { afterEach, describe, expect, it, vi } from 'vitest'
// @ts-expect-error - plain-JS CLI module, no type declarations
import { diffKit, main, readKit } from './sync-kit.mjs'

const here = dirname(fileURLToPath(import.meta.url))
const repoRoot = resolve(here, '..', '..')
const CANONICAL = join(repoRoot, 'src/presentation-kit')
const SNAPSHOT = join(repoRoot, 'skills/presentation/templates/bootstrap/src/presentation-kit')

const map = (entries: Record<string, string>) => new Map(Object.entries(entries))

describe('diffKit', () => {
  it('reports an empty diff for identical kits', () => {
    const kit = map({ 'a.ts': '1', 'b/c.ts': '2' })
    expect(diffKit(kit, new Map(kit))).toEqual({
      added: [],
      changed: [],
      removed: [],
      identical: ['a.ts', 'b/c.ts'],
    })
  })

  it('classifies added, changed, removed, and identical files', () => {
    const snapshot = map({ keep: 'same', edit: 'new', fresh: 'added' })
    const target = map({ keep: 'same', edit: 'old', stale: 'local' })
    expect(diffKit(snapshot, target)).toEqual({
      added: ['fresh'],
      changed: ['edit'],
      removed: ['stale'],
      identical: ['keep'],
    })
  })

  it('treats the snapshot as the source of truth (target-only files are "removed")', () => {
    const snapshot = map({})
    const target = map({ 'local-only.ts': 'x' })
    const { added, removed } = diffKit(snapshot, target)
    expect(added).toEqual([])
    expect(removed).toEqual(['local-only.ts'])
  })
})

describe('readKit', () => {
  it('reads the shipped snapshot and excludes test files', () => {
    const snapshot = readKit(SNAPSHOT)
    expect(snapshot.size).toBeGreaterThan(0)
    expect([...snapshot.keys()].some((p) => /\.test\./.test(p))).toBe(false)
    expect(snapshot.has('Presentation.tsx')).toBe(true)
  })

  it('returns an empty map for a missing directory', () => {
    expect(readKit(join(SNAPSHOT, 'does-not-exist')).size).toBe(0)
  })
})

describe('snapshot ↔ canonical parity (agrees with the drift guard)', () => {
  it('shows no drift between the shipped snapshot and the canonical kit', () => {
    const { added, changed, removed } = diffKit(readKit(SNAPSHOT), readKit(CANONICAL))
    expect({ added, changed, removed }).toEqual({ added: [], changed: [], removed: [] })
  })
})

describe('symlink safety on --apply', () => {
  const tmpDirs: string[] = []
  afterEach(() => {
    vi.restoreAllMocks()
    for (const d of tmpDirs.splice(0)) rmSync(d, { recursive: true, force: true })
  })

  it('refuses to write through a symlinked kit file and leaves its target intact', () => {
    const work = mkdtempSync(join(tmpdir(), 'sync-kit-'))
    tmpDirs.push(work)

    // A sentinel file outside the kit that a planted symlink points at.
    const secret = join(work, 'secret.txt')
    writeFileSync(secret, 'do-not-overwrite')

    // Vendored kit = copy of the snapshot, but with one file replaced by a
    // symlink to the sentinel (the attack: --apply would clobber the target).
    const kit = join(work, 'src/presentation-kit')
    mkdirSync(dirname(kit), { recursive: true })
    cpSync(SNAPSHOT, kit, { recursive: true })
    const planted = join(kit, 'Presentation.tsx')
    unlinkSync(planted)
    symlinkSync(secret, planted)

    vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.spyOn(console, 'log').mockImplementation(() => {})
    vi.spyOn(process.stdout, 'write').mockImplementation(() => true)

    const code = main(['--apply', kit])

    expect(code).toBe(2)
    expect(readFileSync(secret, 'utf8')).toBe('do-not-overwrite')
  })

  it('refuses to write through a symlinked parent directory', () => {
    const work = mkdtempSync(join(tmpdir(), 'sync-kit-'))
    tmpDirs.push(work)

    // A directory outside the kit with a sentinel that an escaped write would hit.
    const outside = join(work, 'outside')
    mkdirSync(outside, { recursive: true })
    writeFileSync(join(outside, 'Footer.tsx'), 'do-not-overwrite')

    // Vendored kit = copy of the snapshot, but with the `chrome/` subdir replaced
    // by a symlink to `outside/`. --apply must not write through it.
    const kit = join(work, 'src/presentation-kit')
    mkdirSync(dirname(kit), { recursive: true })
    cpSync(SNAPSHOT, kit, { recursive: true })
    rmSync(join(kit, 'chrome'), { recursive: true, force: true })
    symlinkSync(outside, join(kit, 'chrome'))

    vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.spyOn(console, 'log').mockImplementation(() => {})
    vi.spyOn(process.stdout, 'write').mockImplementation(() => true)

    const code = main(['--apply', kit])

    expect(code).toBe(2)
    expect(readFileSync(join(outside, 'Footer.tsx'), 'utf8')).toBe('do-not-overwrite')
  })
})
