import { spawn } from 'node:child_process'
import { mkdir } from 'node:fs/promises'
import { dirname, join, resolve, sep } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { chromium } from 'playwright'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const VITE_BIN = join(ROOT, 'node_modules', '.bin', process.platform === 'win32' ? 'vite.cmd' : 'vite')
const OUT_ROOT = join(ROOT, 'artifacts', 'presentation-inspection')
const DEFAULT_SETTLE_MS = 950
const PREVIEW_URL_RE = /http:\/\/127\.0\.0\.1:(\d+)\//

function parseArgs() {
  const args = process.argv.slice(2)
  const opts = { slug: '', width: 1440, height: 900, settleMs: DEFAULT_SETTLE_MS }
  for (let i = 0; i < args.length; i++) {
    const arg = args[i]
    if (arg === '--width') opts.width = Number(args[++i])
    else if (arg === '--height') opts.height = Number(args[++i])
    else if (arg === '--settle-ms') opts.settleMs = Number(args[++i])
    else if (arg === '--slug' || arg === '--route') opts.slug = normalizeSlug(args[++i] ?? '')
    else if (!arg.startsWith('--') && !opts.slug) opts.slug = normalizeSlug(arg)
  }
  if (!Number.isFinite(opts.width) || opts.width < 320) throw new Error(`invalid width: ${opts.width}`)
  if (!Number.isFinite(opts.height) || opts.height < 320) throw new Error(`invalid height: ${opts.height}`)
  if (!Number.isFinite(opts.settleMs) || opts.settleMs < 0) {
    throw new Error(`invalid --settle-ms: ${opts.settleMs}`)
  }
  return opts
}

function normalizeSlug(value) {
  return value.replace(/^https?:\/\/[^/]+/, '').replace(/^\//, '').replace(/\/$/, '')
}

function artifactDirForSlug(slug) {
  const safeName = slug.replace(/[\\/]+/g, '_')
  if (!safeName || safeName.includes('..')) {
    throw new Error(`invalid presentation slug for artifact output: ${slug}`)
  }

  const root = resolve(OUT_ROOT)
  const outDir = resolve(root, safeName)
  if (outDir !== root && outDir.startsWith(`${root}${sep}`)) return outDir
  throw new Error(`presentation artifact output escaped ${OUT_ROOT}: ${slug}`)
}

function runBuild() {
  return new Promise((resolve, reject) => {
    const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm'
    const child = spawn(npm, ['run', 'build'], { cwd: ROOT, stdio: 'inherit', shell: false })
    child.on('close', (code) => (code === 0 ? resolve() : reject(new Error(`build exited ${code}`))))
    child.on('error', reject)
  })
}

async function readRegistry() {
  const registryUrl = pathToFileURL(join(ROOT, 'src/presentations/index.ts')).href
  const mod = await import(registryUrl)
  if (!Array.isArray(mod.presentations)) {
    throw new Error('src/presentations/index.ts does not export a `presentations` array')
  }
  return mod.presentations
}

function childExited(child) {
  return child.exitCode !== null || child.signalCode !== null
}

async function waitForPreview(baseUrl, child, deadlineMs = 30_000) {
  const started = Date.now()
  while (Date.now() - started < deadlineMs) {
    if (childExited(child)) throw new Error(`vite preview exited before ready (code ${child.exitCode})`)
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

async function findOverlapWarnings(page, slug, stepIndex) {
  return page.evaluate(
    ({ slug, stepIndex }) => {
      const selectors = [
        '[data-node-part="label"]',
        '[data-node-part="subtitle"]',
        '[data-node="label"]',
        '[data-presentation-title]',
        '[data-presentation-caption]',
        '[data-presentation-toc-item]',
        '[data-presentation-button]',
      ]

      const rectFor = (el) => {
        const rect = el.getBoundingClientRect()
        if (rect.width < 1 || rect.height < 1) return null
        const style = window.getComputedStyle(el)
        if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) < 0.2) {
          return null
        }
        return {
          left: rect.left,
          right: rect.right,
          top: rect.top,
          bottom: rect.bottom,
          width: rect.width,
          height: rect.height,
        }
      }

      const labelFor = (el) => {
        const hook = Array.from(el.attributes)
          .find((attr) => attr.name.startsWith('data-node') || attr.name.startsWith('data-presentation'))
        const text = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40)
        return `${hook ? hook.name : el.tagName.toLowerCase()}${text ? ` "${text}"` : ''}`
      }

      const items = selectors.flatMap((selector) =>
        Array.from(document.querySelectorAll(selector)),
      )
        .filter((el) => !el.closest('[data-allow-overlap]'))
        .map((el) => ({ el, rect: rectFor(el), label: labelFor(el) }))
        .filter((item) => item.rect)

      const warnings = []
      for (let i = 0; i < items.length; i++) {
        for (let j = i + 1; j < items.length; j++) {
          const a = items[i]
          const b = items[j]
          if (a.el.contains(b.el) || b.el.contains(a.el)) continue
          const left = Math.max(a.rect.left, b.rect.left)
          const right = Math.min(a.rect.right, b.rect.right)
          const top = Math.max(a.rect.top, b.rect.top)
          const bottom = Math.min(a.rect.bottom, b.rect.bottom)
          const width = right - left
          const height = bottom - top
          if (width <= 0 || height <= 0) continue

          const area = width * height
          const smaller = Math.min(a.rect.width * a.rect.height, b.rect.width * b.rect.height)
          if (area < 24 || area / smaller < 0.08) continue

          warnings.push(
            `${slug} step ${stepIndex + 1}: ${a.label} overlaps ${b.label} (${Math.round(area)}px^2)`,
          )
          if (warnings.length >= 10) return warnings
        }
      }
      return warnings
    },
    { slug, stepIndex },
  )
}

export async function findChromeWarnings(page, slug, stepIndex) {
  return page.evaluate(
    ({ slug, stepIndex }) => {
      const isVisible = (el) => {
        if (!el) return false
        const rect = el.getBoundingClientRect()
        const style = window.getComputedStyle(el)
        return (
          rect.width >= 1 &&
          rect.height >= 1 &&
          style.display !== 'none' &&
          style.visibility !== 'hidden' &&
          Number(style.opacity) >= 0.2
        )
      }

      const styleSignature = (el, { includeSize = false } = {}) => {
        const style = window.getComputedStyle(el)
        const rect = el.getBoundingClientRect()
        const parts = [
          style.color,
          style.backgroundColor,
          style.borderTopColor,
          style.borderRightColor,
          style.borderBottomColor,
          style.borderLeftColor,
          style.fontWeight,
          style.opacity,
          style.textDecorationLine,
        ]
        if (includeSize) parts.push(String(Math.round(rect.width)), String(Math.round(rect.height)))
        return parts.join('|')
      }

      const warnings = []
      const progressDots = Array.from(document.querySelectorAll('[data-presentation-progress-dot]'))
        .filter(isVisible)
      const activeProgress = progressDots.find((el) =>
        el.getAttribute('data-active') === 'true' || el.getAttribute('aria-current') === 'step',
      )
      const inactiveProgress = progressDots.find((el) => el !== activeProgress)
      if (!activeProgress && progressDots.length > 1) {
        warnings.push(`${slug} step ${stepIndex + 1}: no active progress dot is exposed`)
      } else if (
        activeProgress &&
        inactiveProgress &&
        styleSignature(activeProgress, { includeSize: true }) ===
          styleSignature(inactiveProgress, { includeSize: true })
      ) {
        warnings.push(
          `${slug} step ${stepIndex + 1}: active progress dot looks identical to inactive dots; style [data-presentation-progress-dot][data-active='true']`,
        )
      }

      const tocItems = Array.from(document.querySelectorAll('[data-presentation-toc-item]'))
        .filter(isVisible)
      const activeToc = tocItems.find((el) =>
        el.getAttribute('data-active') === 'true' || el.getAttribute('aria-current') === 'step',
      )
      const inactiveToc = tocItems.find((el) => el !== activeToc)
      if (!activeToc && tocItems.length > 1) {
        warnings.push(`${slug} step ${stepIndex + 1}: no active table-of-contents item is exposed`)
      } else if (activeToc && inactiveToc && styleSignature(activeToc) === styleSignature(inactiveToc)) {
        warnings.push(
          `${slug} step ${stepIndex + 1}: active table-of-contents item looks identical to inactive items; style [data-presentation-toc-item][data-active='true']`,
        )
      }

      const attribution = document.querySelector('[data-presentation-attribution]')
      if (!attribution) {
        warnings.push(
          `${slug}: attribution is not rendered; pass attribution={null} only for an intentional opt-out`,
        )
      } else if (!isVisible(attribution)) {
        warnings.push(
          `${slug}: attribution is present but not visible; style [data-presentation-attribution] in presentation CSS`,
        )
      } else {
        const style = window.getComputedStyle(attribution)
        const rect = attribution.getBoundingClientRect()
        const fontSize = Number.parseFloat(style.fontSize)
        const defaultLinkBlue = style.color === 'rgb(0, 0, 238)' || style.color === '-webkit-link'
        if (fontSize < 12 || rect.height < 14 || defaultLinkBlue) {
          warnings.push(
            `${slug}: attribution appears too small or browser-default; style [data-presentation-attribution] in presentation CSS`,
          )
        }
      }

      return warnings
    },
    { slug, stepIndex },
  )
}

export function appendInspectionWarnings(warnings, seenAttributionWarnings, additions) {
  for (const warning of additions) {
    const isAttributionWarning = warning.includes(': attribution ')
    if (isAttributionWarning && seenAttributionWarnings.has(warning)) continue
    warnings.push(warning)
    if (isAttributionWarning) seenAttributionWarnings.add(warning)
  }
}

async function capturePresentation(page, baseUrl, slug, width, height, settleMs) {
  const outDir = artifactDirForSlug(slug)
  await mkdir(outDir, { recursive: true })
  await page.setViewportSize({ width, height })
  await page.goto(`${baseUrl}${slug}`, { waitUntil: 'load', timeout: 30_000 })

  const progress = page.locator('[data-testid="step-progress"]')
  await progress.waitFor({ timeout: 10_000 })
  const stepCount = Number(await progress.getAttribute('data-step-count'))
  if (!Number.isFinite(stepCount) || stepCount < 1) {
    throw new Error(`${slug}: invalid data-step-count: ${stepCount}`)
  }

  const written = []
  const warnings = []
  const seenAttributionWarnings = new Set()
  for (let i = 0; i < stepCount; i++) {
    const expectedIndex = Number(await progress.getAttribute('data-step-index'))
    if (expectedIndex !== i) throw new Error(`${slug} step ${i}: expected index ${i}, got ${expectedIndex}`)

    await page.waitForTimeout(settleMs)
    warnings.push(...await findOverlapWarnings(page, slug, i))
    appendInspectionWarnings(warnings, seenAttributionWarnings, await findChromeWarnings(page, slug, i))

    const path = join(outDir, `step-${String(i + 1).padStart(2, '0')}.png`)
    await page.screenshot({ path, fullPage: false })
    written.push(path)

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
  return { written, warnings }
}

async function main() {
  const opts = parseArgs()
  await runBuild()

  const presentations = await readRegistry()
  const selected = opts.slug ? presentations.filter((entry) => entry.slug === opts.slug) : presentations
  if (selected.length === 0) {
    throw new Error(opts.slug ? `presentation not found: ${opts.slug}` : 'no presentations registered')
  }

  const { child, baseUrl } = await startPreview()
  let browser
  try {
    browser = await chromium.launch()
    const page = await browser.newPage()
    for (const { slug } of selected) {
      const { written, warnings } = await capturePresentation(
        page,
        baseUrl,
        slug,
        opts.width,
        opts.height,
        opts.settleMs,
      )
      console.log(`INSPECT: ${slug} (${written.length} screenshot${written.length === 1 ? '' : 's'})`)
      for (const path of written) console.log(path)
      for (const warning of warnings) console.warn(`WARN [inspect-overlap]: ${warning}`)
    }
  } finally {
    await browser?.close()
    await stopPreview(child)
  }
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((err) => {
    console.error(`FAIL [inspect]: ${err instanceof Error ? err.message : String(err)}`)
    process.exit(1)
  })
}
