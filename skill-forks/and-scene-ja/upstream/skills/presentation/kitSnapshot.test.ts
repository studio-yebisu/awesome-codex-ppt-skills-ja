import { readdirSync, readFileSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

/**
 * Drift guard for the deliberately-duplicated scene kit.
 *
 * The canonical kit lives at `src/presentation-kit/`; the skill ships a snapshot
 * copy at `skills/presentation/templates/bootstrap/src/presentation-kit/` that it
 * vendors into user projects. The two are kept **byte-identical** — excluding
 * test files, which only the canonical copy carries. `npm run verify` cannot
 * catch a desync here (it only renders the reference app), so this test does.
 *
 * When this fails: you changed one copy and not the other. Re-sync with
 *   cp <changed canonical file> <matching snapshot file>
 * (or the reverse), then re-run.
 */

const here = dirname(fileURLToPath(import.meta.url))
const repoRoot = resolve(here, '..', '..')
const CANONICAL = join(repoRoot, 'src/presentation-kit')
const SNAPSHOT = join(repoRoot, 'skills/presentation/templates/bootstrap/src/presentation-kit')

const isTestFile = (path: string) => /\.test\./.test(path)

/** Relative paths of every non-test file under `dir`, sorted. */
function kitFiles(dir: string): string[] {
  const out: string[] = []
  const walk = (current: string) => {
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      const full = join(current, entry.name)
      if (entry.isDirectory()) walk(full)
      else if (!isTestFile(entry.name)) out.push(relative(dir, full))
    }
  }
  walk(dir)
  return out.sort()
}

describe('presentation-kit snapshot parity', () => {
  it('canonical and snapshot share the same non-test file set', () => {
    expect(kitFiles(SNAPSHOT)).toEqual(kitFiles(CANONICAL))
  })

  it('every shared file is byte-identical between canonical and snapshot', () => {
    const drifted = kitFiles(CANONICAL).filter((rel) => {
      const canonical = readFileSync(join(CANONICAL, rel), 'utf8')
      const snapshot = readFileSync(join(SNAPSHOT, rel), 'utf8')
      return canonical !== snapshot
    })
    expect(drifted).toEqual([])
  })
})
