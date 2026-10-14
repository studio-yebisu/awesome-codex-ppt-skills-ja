/** Contract-anchor detection and scaffold target resolution for the presentation skill. */

export interface ProjectSnapshot {
  files: string[]
  packageJson?: {
    scripts?: Record<string, string>
    workspaces?: string[] | Record<string, string[]>
  }
  presentationIndexContent?: string
}

export interface ContractAnchors {
  buildSetup: boolean
  sceneKit: boolean
  presentationIndex: boolean
}

export const REQUIRED_DEPENDENCIES = {
  runtime: ['react', 'react-dom', 'motion', 'lucide-react'] as const,
  dev: [
    'vite',
    '@vitejs/plugin-react',
    'typescript',
    '@types/react',
    '@types/react-dom',
    '@types/node',
    '@eslint/js',
    'eslint',
    'eslint-plugin-react-hooks',
    'eslint-plugin-react-refresh',
    'globals',
    'typescript-eslint',
    'playwright',
  ] as const,
}

const SCENE_KIT_MARKERS = [
  'src/presentation-kit/types.ts',
  'src/presentation-kit/Presentation.tsx',
  'src/presentation-kit/Stage.tsx',
]

const PRESENTATION_INDEX_MARKERS = ['src/presentations/index.ts']

function hasFile(files: string[], path: string): boolean {
  return files.some((f) => f === path || f.endsWith(`/${path}`))
}

function hasPathPrefix(files: string[], prefix: string): boolean {
  return files.some((f) => f.startsWith(prefix))
}

/** Detect the three contract anchors at the presence level (not byte-identical). */
export function detectAnchors(snapshot: ProjectSnapshot): ContractAnchors {
  const { packageJson, presentationIndexContent } = snapshot

  // Ignore this skill's own bundled templates. Marker matching is suffix-based
  // (so a nested app like `presentations/src/...` still resolves), which means a
  // file list that includes the skill source — e.g. a whole-repo snapshot —
  // would otherwise match markers against `templates/bootstrap/src/...` and
  // report scaffolding that isn't actually installed in the project. Normalize
  // separators first so Windows backslash paths are filtered (and matched) too.
  const files = snapshot.files
    .map((f) => f.replaceAll('\\', '/'))
    .filter((f) => !f.includes('templates/bootstrap/'))

  const buildSetup =
    hasFile(files, 'vite.config.ts') &&
    hasFile(files, 'package.json') &&
    typeof packageJson?.scripts?.build === 'string'

  const sceneKit = SCENE_KIT_MARKERS.every((m) => hasFile(files, m))

  const hasIndexFile = PRESENTATION_INDEX_MARKERS.some((m) => hasFile(files, m))
  const presentationIndex =
    hasIndexFile &&
    typeof presentationIndexContent === 'string' &&
    /export\s+const\s+presentations\b/.test(presentationIndexContent)

  return { buildSetup, sceneKit, presentationIndex }
}

/** Heuristic monorepo detection: workspaces, pnpm-workspace.yaml, or packages/apps layout. */
export function isMonorepo(snapshot: ProjectSnapshot): boolean {
  const { files, packageJson } = snapshot
  if (packageJson?.workspaces) return true
  if (hasFile(files, 'pnpm-workspace.yaml')) return true
  if (hasPathPrefix(files, 'packages/')) return true
  if (hasPathPrefix(files, 'apps/')) return true
  return false
}

/** A repo is already a JS/Node project once it carries a `package.json`. */
function hasPackageJson(snapshot: ProjectSnapshot): boolean {
  return hasFile(snapshot.files, 'package.json')
}

/**
 * Resolve where to scaffold the presentation app:
 *
 *  - **Monorepo** → a self-contained app under `presentations/`, a peer of the
 *    other workspace packages.
 *  - **Empty directory, or an existing standalone JS app** → the repo **root**
 *    (`.`): the repo either becomes the app or already is a JS app the
 *    presentation infra slots into (e.g. adding the scene kit to an app).
 *  - **Any other non-empty repo** (a Python/Go/Rust/etc. project with no
 *    `package.json`) → a self-contained app under `presentation/`, so the
 *    scaffold never drops a JS app on top of an unrelated project at the root.
 *
 * In every non-root case the skill still states the resolved target and asks the
 * user to confirm before writing (see SKILL.md).
 */
export function resolveScaffoldTarget(snapshot: ProjectSnapshot): string {
  if (isMonorepo(snapshot)) return 'presentations'
  const isEmpty = snapshot.files.length === 0
  if (isEmpty || hasPackageJson(snapshot)) return '.'
  return 'presentation'
}

/** Derive a URL slug from a presentation title. */
export function slugFromTitle(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}
