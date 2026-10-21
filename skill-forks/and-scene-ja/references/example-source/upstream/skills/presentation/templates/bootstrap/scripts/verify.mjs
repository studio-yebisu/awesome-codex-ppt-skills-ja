import { spawn } from 'node:child_process'
import { dirname, join } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { chromium } from 'playwright'

/**
 * Presentation-agnostic verifier for a scaffolded project.
 *
 * Rather than pinning to a single known slug, this reads the project's own
 * registry and renders EVERY registered
 * presentation through all of its steps, failing on any build error, console
 * error, or uncaught page error. A project with no presentations yet still
 * passes (the scaffold builds; there is simply nothing to render).
 *
 * Run via `npm run verify` (which supplies --experimental-strip-types so the
 * TypeScript registry can be imported directly).
 */

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const VITE_BIN = join(ROOT, 'node_modules', '.bin', process.platform === 'win32' ? 'vite.cmd' : 'vite')
const PREVIEW_URL_RE = /http:\/\/127\.0\.0\.1:(\d+)\//

/** @param {string} check @param {string} detail */
function fail(check, detail) {
  console.error(`FAIL [${check}]: ${detail}`)
  process.exit(1)
}

function pass(msg) {
  console.log(`PASS: ${msg}`)
}

function runBuild() {
  return new Promise((resolve, reject) => {
    const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm'
    const child = spawn(npm, ['run', 'build'], { cwd: ROOT, stdio: 'inherit', shell: false })
    child.on('close', (code) => (code === 0 ? resolve() : reject(new Error(`build exited ${code}`))))
    child.on('error', reject)
  })
}

/** Read the project's presentation registry. Returns the list of { slug }. */
async function readRegistry() {
  const registryUrl = pathToFileURL(join(ROOT, 'src/presentations/index.ts')).href
  const mod = await import(registryUrl)
  const presentations = mod.presentations
  if (!Array.isArray(presentations)) {
    throw new Error('src/presentations/index.ts does not export a `presentations` array')
  }
  return presentations
}

/** @param {import('node:child_process').ChildProcess} child */
function childExited(child) {
  return child.exitCode !== null || child.signalCode !== null
}

/** @param {string} baseUrl @param {import('node:child_process').ChildProcess} child */
async function waitForPreview(baseUrl, child, deadlineMs = 30_000) {
  const started = Date.now()
  while (Date.now() - started < deadlineMs) {
    if (childExited(child)) {
      throw new Error(`vite preview exited before ready (code ${child.exitCode})`)
    }
    try {
      const res = await fetch(baseUrl)
      const html = await res.text()
      if (res.ok && html.includes('id="root"')) return
    } catch {
      // server not listening yet
    }
    await new Promise((r) => setTimeout(r, 200))
  }
  throw new Error('vite preview did not become ready within 30s')
}

/** @param {import('node:child_process').ChildProcess} child */
function stopPreview(child) {
  return new Promise((resolve) => {
    if (!child.pid) {
      resolve()
      return
    }
    child.once('close', () => resolve())
    try {
      process.kill(-child.pid, 'SIGTERM')
    } catch {
      child.kill('SIGTERM')
    }
    setTimeout(() => {
      if (!childExited(child)) {
        try {
          process.kill(-child.pid, 'SIGKILL')
        } catch {
          child.kill('SIGKILL')
        }
      }
      resolve()
    }, 3000)
  })
}

function startPreview() {
  return new Promise((resolve, reject) => {
    const child = spawn(
      VITE_BIN,
      ['preview', '--port', '0', '--host', '127.0.0.1'],
      { cwd: ROOT, stdio: ['ignore', 'pipe', 'pipe'], detached: true },
    )

    let output = ''
    let settled = false
    let readyStarted = false

    const cleanup = () => {
      clearTimeout(timer)
      child.stdout?.off('data', onData)
      child.stderr?.off('data', onData)
      child.off('error', onError)
      child.off('close', onClose)
    }
    const rejectWith = async (err) => {
      if (settled) return
      settled = true
      cleanup()
      await stopPreview(child)
      reject(err)
    }
    const resolveWith = (value) => {
      if (settled) return
      settled = true
      cleanup()
      resolve(value)
    }
    const onData = (chunk) => {
      output += chunk.toString()
      const match = output.match(PREVIEW_URL_RE)
      if (!match || readyStarted) return
      readyStarted = true
      const baseUrl = match[0]
      waitForPreview(baseUrl, child)
        .then(() => resolveWith({ child, baseUrl }))
        .catch(rejectWith)
    }
    const onError = (err) => rejectWith(err)
    const onClose = (code) => {
      if (!settled) rejectWith(new Error(`vite preview exited before ready (code ${code})`))
    }
    const timer = setTimeout(() => {
      const detail = output.trim() ? ` Output:\n${output.trim()}` : ''
      rejectWith(new Error(`vite preview did not print a local URL within 30s.${detail}`))
    }, 30_000)

    child.stdout?.on('data', onData)
    child.stderr?.on('data', onData)
    child.on('error', onError)
    child.on('close', onClose)
  })
}

/** Step a single presentation through every step, capturing render errors. */
async function renderPresentation(page, baseUrl, slug) {
  const errors = []
  // Start at 0 so errors during the initial page load (before the step loop
  // runs) are attributed to step 0 rather than a confusing `step null`.
  let failingStep = 0

  const onConsole = (msg) => {
    if (msg.type() === 'error') errors.push({ step: failingStep, msg: msg.text() })
  }
  const onPageError = (err) => errors.push({ step: failingStep, msg: err.message })
  page.on('console', onConsole)
  page.on('pageerror', onPageError)

  try {
    await page.goto(`${baseUrl}${slug}`, { waitUntil: 'load', timeout: 30_000 })

    const progress = page.locator('[data-testid="step-progress"]')
    await progress.waitFor({ timeout: 10_000 })

    const stepCount = Number(await progress.getAttribute('data-step-count'))
    if (!Number.isFinite(stepCount) || stepCount < 1) {
      throw new Error(`${slug}: invalid data-step-count: ${stepCount}`)
    }

    for (let i = 0; i < stepCount; i++) {
      failingStep = i
      const index = Number(await progress.getAttribute('data-step-index'))
      if (index !== i) throw new Error(`${slug} step ${i}: expected index ${i}, got ${index}`)

      if (i < stepCount - 1) {
        await page.keyboard.press('ArrowRight')
        await page.waitForFunction(
          (expected) => {
            const el = document.querySelector('[data-testid="step-progress"]')
            return el && Number(el.getAttribute('data-step-index')) === expected
          },
          i + 1,
          { timeout: 5000 },
        )
      }
    }

    if (errors.length > 0) {
      const first = errors[0]
      throw new Error(`${slug} step ${first.step}: ${first.msg}`)
    }
  } finally {
    page.off('console', onConsole)
    page.off('pageerror', onPageError)
  }
}

/** @param {string} baseUrl @param {Array<{ slug: string }>} presentations */
async function renderCheck(baseUrl, presentations) {
  const browser = await chromium.launch()
  try {
    const page = await browser.newPage()
    for (const { slug } of presentations) {
      await renderPresentation(page, baseUrl, slug)
    }
  } finally {
    await browser.close()
  }
}

async function main() {
  try {
    await runBuild()
    pass('build')

    const presentations = await readRegistry()
    pass(`registry (${presentations.length} presentation${presentations.length === 1 ? '' : 's'})`)

    if (presentations.length === 0) {
      console.log('VERIFY: PASS (no presentations registered yet)')
      return
    }

    const { child, baseUrl } = await startPreview()
    try {
      await renderCheck(baseUrl, presentations)
      pass('render')
    } finally {
      await stopPreview(child)
    }

    console.log('VERIFY: PASS')
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err)
    fail(message.includes(' step ') ? 'render' : 'verify', message)
  }
}

main()
