---
name: presentation
description: >
  Creates and modifies evolving-scene browser presentations. Use when the user
  asks to "create a presentation", "build a talk", "add steps", "modify a
  presentation", "update/resync the scene kit", or scaffold presentation
  infrastructure. Gathers requirements interactively, bootstraps missing
  scaffolding (monorepo-aware), registers presentations at their own routes,
  resyncs a project's vendored scene kit with the latest snapshot, and
  self-verifies build + render before reporting done.
---

# Presentation skill

Build **evolving-scene presentations**: one shared diagrammatic canvas where
entities morph across steps while captions and navigation guide the audience.
Each presentation is a self-contained folder under `src/presentations/<slug>/`
that composes the reusable **scene kit** at `src/presentation-kit/`.

## When to use

- User asks to create, build, or generate a presentation or talk
- User asks to modify, update, or add steps to an existing presentation
- Project lacks the scene kit or presentation infrastructure and needs bootstrapping
- User asks to update, resync, or pull the latest scene kit into a project whose
  vendored `src/presentation-kit/` has fallen behind the skill (see
  [Updating the vendored kit](#updating-the-vendored-kit))

## Procedure

Work through these phases in order. Do not skip self-verify.

### 1. Gather requirements

Ask **one question at a time**. Cover:

1. **Topic** — what the presentation is about
2. **Visual style** — accents, mood, density (sparse diagram vs. rich layout)
3. **High-level sections** — the major parts of the story, in order
4. **Each step** — after the sections are agreed, flesh them out one by one.
   A "step" means one navigable beat in the presentation: the caption/title plus
   the scene state shown for that moment.
5. **Per-step visuals** — which entities appear, how they relate, and what
   morphs between steps

Rules:

- Do **not** assume details the user can still provide
- Allow the user to proceed with **partial detail** and iterate later — no hard
  completeness gate
- Do **not** start by asking how long the talk should be or how many steps it
  should have. First establish the high-level sections, then expand each section
  into steps. Ask about length/count only after that structure exists, or when
  the user explicitly asks the agent to decide or fill in details.
- If the user says the length/count is TBD, accept that and continue by shaping
  the high-level sections before implementing any steps.
- Define skill-specific terms the first time they are used in user-facing
  conversation. For example: a "step" is one navigable beat of the talk; a
  "hero" entity is the main visual object that carries continuity across the
  scene. Do not front-load a glossary; define terms just before they matter.
- If the prompt already contains topic, style, and all step details, proceed to
  scaffold/generate without further questions
- For **key or complex steps**, optionally draw an **ASCII mockup** of the layout
  and ask the user to confirm before building. Use mockups selectively, not for
  every step

### 2. Resolve target + scaffold if needed

Before creating or modifying a presentation, ensure three **contract anchors**
exist. Detection is **contract-level** (presence of the anchor, not byte-identical
files). Cosmetic differences do not trigger re-scaffolding.

| Anchor | What to look for |
|--------|------------------|
| **Build setup** | `vite.config.ts`, `package.json` with a `build` script |
| **Scene kit** | `src/presentation-kit/types.ts`, `Presentation.tsx`, `Stage.tsx` |
| **Presentation index** | `src/presentations/index.ts` exporting a `presentations` registry |

**Target resolution:**

| Context | Scaffold location |
|---------|-------------------|
| Empty directory, or an existing standalone JS app (a `package.json` at the root, non-monorepo) | Repository root (`.`) |
| Monorepo (`workspaces` in `package.json`, `pnpm-workspace.yaml`, or `packages/` / `apps/` layout) | Self-contained app under `presentations/` |
| Non-empty repo that is **not** a JS app (no root `package.json` — e.g. a Python/Go/Rust project) | Self-contained app under `presentation/` |
| Anchors already present | Use existing app; scaffold only missing anchors |

**Monorepo detection signals:** `package.json` `workspaces`, `pnpm-workspace.yaml`,
or files under `packages/` or `apps/`.

**Why non-JS repos nest:** the bootstrap is a full Vite + React app. Dropping its
`package.json`, `vite.config.ts`, and `src/` at the root of a Python/Go/Rust repo
would collide with the existing project, so the scaffold lands in a dedicated
`presentation/` subfolder instead. Only a truly empty directory or a repo that is
already a JS app gets scaffolded in place at the root.

**Scaffolding steps:**

1. Determine which anchors are missing (all, some, or none)
2. Copy missing pieces from `templates/bootstrap/` in this skill directory.
   Template paths are relative to this `SKILL.md` file, not necessarily to the
   user's current working directory.
   The bootstrap `package.json` ships a neutral `presentation-app` name —
   rename it to suit the target project (e.g. the repo or monorepo package
   name) before installing.
3. **Install dependencies** — never assume they are present. The scaffold must
   ensure this full set:
   - **Runtime:** `react`, `react-dom`, `motion`, `lucide-react`
   - **Dev/build:** `vite`, `@vitejs/plugin-react`, `typescript`,
     `@types/react`, `@types/react-dom`, `@types/node`, the eslint stack
     (`@eslint/js`, `eslint`, `eslint-plugin-react-hooks`,
     `eslint-plugin-react-refresh`, `globals`, `typescript-eslint`), and
     `playwright` (for render checks)
4. Run `npm install` in the resolved target directory

**Non-empty project without scaffolding:** state the resolved target location
(e.g. "I will scaffold into `presentations/`") and proceed only after the user
confirms.

**Already scaffolded:** skip scaffolding and go directly to generate/modify.

Utility helpers in `scaffold.ts` (alongside this file) implement anchor
detection, monorepo heuristics, and target resolution for automated checks.

### 3. Generate or modify

#### Create a new presentation

1. Derive a **slug** from the title (kebab-case, e.g. `how-to-use-this-skill`)
2. Create `src/presentations/<slug>/` from `templates/presentation/`:
   - `entities.ts` — stable `layoutId` namespace for every morphing entity
   - `steps/*.tsx` — one file per step; each exports a `Step` object
   - `Talk.tsx` — imports all steps, renders `<Presentation steps={STEPS} />`
3. Add presentation-owned styling if the user wants a designed look. The kit is
   BYO styles: no colors, fonts, borders, spacing scale, or framework defaults
   are provided by the scaffold. Default to plain CSS in a presentation-local
   stylesheet. Use Tailwind or another styling system only when the host project
   already uses it or the user explicitly requests it.
4. Register in `src/presentations/index.ts`:

```ts
{
  slug: '<slug>',
  title: '<Human title>',
  load: () => import('./<slug>/Talk'),
},
```

5. Preserve all existing registry entries — new presentations must not break others

#### Modify an existing presentation

1. **Identify the target** from the user's request
2. If unspecified or ambiguous, **lists the existing presentations** from
   `src/presentations/index.ts` and asks which to modify
3. Ask only about the **requested changes** (steps, entities, style) — do not
   re-walk the full create flow
4. Make scoped edits to that presentation's `entities.ts`, `steps/*`, or `Talk.tsx`

### 4. Self-verify

Before reporting success:

1. Run `npm run build` in the presentation app directory — must complete with no
   type errors
2. Run a **render check** on the presentation route — at minimum, the first step
   must render without runtime or console errors. Use `npm run verify` when
   available (full multi-step check), or start `npm run preview` and open the
   route in a browser / Playwright
3. Run a **visual composition check** in a browser. Capture or inspect
   screenshots of the first step, the last step, and any dense/key steps at a
   normal desktop viewport; for responsive-sensitive presentations, also inspect
   a narrow viewport. Prefer `npm run inspect -- <slug>` when available; it
   writes project-local screenshots under `artifacts/presentation-inspection/`
   so Playwright resolves from the project's installed dependencies. The helper
   waits for morph/fade animations to settle before each screenshot and prints
   advisory warnings for text/chrome collisions, visually identical active
   navigation states, and unpolished attribution. Check the screenshots and
   warnings for accidental overlap, clipped/off-canvas content, unreadable
   stacking, missing active TOC/progress styling, and collisions with chrome
   such as captions, progress dots, table of contents, or navigation buttons.
   `npm run verify` catches crashes and console errors; it does not prove the
   scene is visually correct.
4. If any check fails, **fix the issues and re-check** — never report success
   on broken output

If Chromium is missing, run `npx playwright install chromium`. Do not run
`--with-deps` unless the environment has OS package privileges and actually
needs browser system dependencies.

### Output format

Report completion in this structure:

1. **Action** — created or modified, with presentation title and route (`/<slug>`)
2. **Files changed** — list of paths written or edited
3. **Verification** — commands run (`npm run build`, render check), visual
   composition check performed, and their result
4. **Follow-ups** — any unresolved questions or partial details the user may want to iterate on (omit if none)

## Updating the vendored kit

The scene kit is **vendored** (shadcn-style): every project owns a copy at
`src/presentation-kit/` rather than depending on a package. That copy does not
update itself when the skill does — there is no version to bump. When the skill
ships a kit fix (a new prop, a bug fix), a project's copy must be **resynced**.

The source of truth is the snapshot this skill ships at
`templates/bootstrap/src/presentation-kit/`, refreshed whenever the plugin is
updated (`claude plugin update`). The `sync-kit.mjs` script (alongside this file)
diffs that snapshot against a project's vendored copy and rewrites it on demand.

**When to resync:** the user reports the kit is out of date, asks to pull kit
updates, or a kit fix shipped in the skill needs to reach an existing project.

**Steps** (run from the consuming project root):

1. **Report drift** — diff the project's copy against the snapshot:

   ```bash
   node <skill-dir>/sync-kit.mjs
   ```

   Exit `0` = in sync; exit `1` = files differ (the diff is printed). Local edits
   to the vendored copy show up as drift too — that is expected, like
   `shadcn diff`.

2. **Apply** — rewrite the project's copy to match the snapshot:

   ```bash
   node <skill-dir>/sync-kit.mjs --apply
   ```

   Added and changed files are written; **target-only files are left untouched**
   (the script never deletes), so local-only additions survive. Pass an explicit
   path as the last argument to target a non-default kit location.

3. **Re-apply local theming, then verify** — if the project had local edits the
   snapshot overwrote, review with `git diff` and re-apply them. Then run
   `npm run build` and a render check (per [Self-verify](#4-self-verify)) before
   reporting done.

Resyncing the kit does **not** touch a project's presentations or its host
config (the `<Presentation>` props it passes) — only the kit files. If a kit
update adds a capability the host should opt into (e.g. a new slot), call that
out so the user can wire it up in their `Talk.tsx`.

## Composing the scene kit

Presentations import from `src/presentation-kit/`. Each presentation supplies
only its own entities and step scenes.

### Step contract

```ts
interface Step<P extends Record<string, unknown> = Record<string, unknown>> {
  id: string          // stable key for AnimatePresence
  era: string         // table-of-contents section label
  title: string      // presenter-mode one-liner
  caption: string    // browse-mode paragraph
  groupKey?: string  // consecutive steps with same groupKey are not remounted
  payload?: P
  Scene: ComponentType<{ step: Step<P> }>
}
```

For strongly typed grouped scenes, define a payload type and use `Step<Payload>`
for the steps, scene props, and `<Presentation steps={STEPS} />` boundary
instead of casting each `payload`.

```tsx
type PhasePayload = { active: 'idea' | 'system'; count: number }

function GroupedScene({ step }: { step: Step<PhasePayload> }) {
  const payload = step.payload
  return <SceneLayer>{/* render from payload */}</SceneLayer>
}

const STEPS: Step<PhasePayload>[] = [
  {
    id: 'idea',
    era: 'shape',
    title: 'The idea appears',
    caption: 'A first shape lands.',
    groupKey: 'main-scene',
    payload: { active: 'idea', count: 1 },
    Scene: GroupedScene,
  },
]

export default function Talk() {
  return <Presentation steps={STEPS} title="Example" initialMode="browse" />
}
```

### Entity continuity (`layoutId`)

Define stable ids in `entities.ts`. Any node that should **morph** across steps
must use the same `layoutId`:

```ts
export const ENTITIES = { hero: 'hero', flow: 'flow' } as const
```

### Smooth morph authoring rules

The original reference implementation relies on authoring discipline as much as
kit code. Follow these rules when generating or modifying step scenes:

- Use a **persistent scene** with shared `groupKey` and `step.payload` for
  consecutive beats that represent one evolving diagram. Do not split a single
  evolving picture into many unrelated `Scene` components unless the whole
  composition should intentionally remount.
- Put stable `layoutId`s only on the entity that should morph. A new visual
  object gets a new id; the same conceptual object keeps the same id.
- Do not put transform or opacity styling directly on an element with
  `layoutId` (`scale`, `rotate`, `opacity`, or Tailwind equivalents such as
  `scale-*`, `rotate-*`, `opacity-*`). Motion uses transforms and opacity during
  layout projection; combine those on a child or wrapper only when it is not the
  shared layout entity.
- Do not put conflicting positioning styles on one element, especially
  `position: relative` plus `position: absolute` through mixed classes. For
  relative offsets, use relative positioning and offsets without adding
  absolute positioning; for true absolute placement, put the absolute
  positioning on a non-`layoutId` wrapper and verify the layout still matches
  the intended design.
- When fixing a smooth-morph issue in an existing presentation, preserve the
  intentional composition. If cards or callouts are meant to overlap, keep that
  overlap and move only the unsafe positioning/opacity/transform utilities to a
  wrapper. Do not flatten, spread out, or otherwise redesign the scene just to
  satisfy the wrapper rule.
- Use `Appear` only for newcomers. Continuing entities with a shared `layoutId`
  should persist and morph; they should not fade out and back in.
- **Let the layout re-center; do not pin it.** The signature move of an
  evolving scene is that each step lays itself out around whatever is currently
  on screen and then *re-aligns* when the next entity appears — one box centered
  alone, two boxes balanced, a row that spreads to frame the tray that grew
  beneath it. Because every entity carries a `layoutId`, those re-alignments
  animate for free. Achieve it by keeping the composition **content-sized and
  centered** (natural widths, `justify-content`/`align-items: center`,
  `align-self: stretch` to match a sibling's width), and let flow do the
  positioning. Do **not** freeze positions with fixed pixel/`ch` widths, fixed
  stage widths, reserved empty slots, or `align-items: flex-start` pinning —
  those hold entities still across steps and kill the re-centering, which is the
  most striking thing the framework does. If two entities must share an edge
  (e.g. a header row framing a panel below it), give them a shared width by
  construction (`align-self: stretch` against a common parent, or one CSS var
  both consume) rather than hardcoding a number. When you need to stop a
  *transient* overshoot during a swap (an exiting element and an entering one
  briefly widening a row), stack them in one grid cell — do not solve it by
  fixing the whole row's width.
- Keep browse-mode chrome in mind while composing scenes. The table of contents
  can occupy the left side on wide browse viewports, and captions/progress/nav
  occupy the lower band. Avoid dense horizontal rows that only fit the raw
  880px stage in isolation; prefer up to three primary boxes per row, compact
  chips, grouped entities, or wrapping/stacking when a concept list grows.
- Intentional overlap is allowed and often useful. When an overlap is part of
  the design and should not be treated as a suspicious visual collision, wrap
  that region in an element with `data-allow-overlap`.

### Node primitives

Compose steps from kit primitives (all accept `layoutId`):

| Primitive | Use for |
|-----------|---------|
| `Box` | Unstyled entity wrapper with optional Lucide icon, label, subtitle |
| `Label` | Unstyled annotation |
| `Arrow` | Unstyled connector (default `→`) |
| `Frame` | Unstyled grouped region with optional frame label |
| `Emphasis` | Unstyled callout wrapper |
| `SymbolChip` | Unstyled icon+label entity with `symbol` or `chip` variant hooks |
| `Appear` | Fade-in for newcomers after persisting entities settle |
| `SceneLayer` | Absolutely-positioned diagram layer (prevents reflow between steps) |

The kit is intentionally **unstyled**. It supplies motion behavior, stable DOM
hooks (`data-node`, `data-node-part`, `data-accent`, `data-variant`, and
`data-presentation-*` chrome hooks), fixed-canvas layout plumbing, active-state
semantics (`aria-current="step"` plus `data-active="true"`), and a bottom-right
attribution link (`made by and-scene`) to the GitHub repository. It must not
impose a palette, font, border treatment, glow, card style, button treatment, or
Tailwind dependency. Every presentation owns its visual system, including chrome
polish.

Kit primitives accept `className` and `style` so presentations can use either
CSS classes or explicit coordinates. For complex diagrams with literal per-step
pixel coordinates, use primitive `style` props or raw `motion.div` elements with
the same `layoutId` discipline.

### Layout pattern

```tsx
import { Box, SceneLayer, Arrow } from '../../presentation-kit'
import { ENTITIES } from '../entities'

function MyScene() {
  return (
    <SceneLayer>
      <div className="flow">
        <Box layoutId={ENTITIES.hero} label="Idea" accent="cyan" />
        <Arrow layoutId={ENTITIES.flow} />
        <Box layoutId={ENTITIES.result} label="Outcome" accent="green" />
      </div>
    </SceneLayer>
  )
}
```

Position entities with the presentation's own classes or styles inside
`SceneLayer`. The kit scales a fixed design canvas (880×380) to fit between
header and footer.

Plain CSS example:

```css
.my-talk .flow {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.my-talk [data-node='box'] {
  border: 2px solid currentColor;
  padding: 1rem 1.5rem;
}

.my-talk [data-accent='cyan'] {
  color: #0f766e;
}

.my-talk [data-presentation-progress-dot][data-active='true'] {
  background: #0f766e;
}

.my-talk [data-presentation-toc-item][data-active='true'] {
  color: #0f766e;
}

.my-talk [data-presentation-attribution] {
  color: #475569;
  font-size: 0.75rem;
  text-decoration: none;
}
```

Optional Tailwind example (only after the project has chosen and installed
Tailwind):

```tsx
<SceneLayer>
  <div className="flex items-center gap-8">
    <Box layoutId={ENTITIES.hero} label="Idea" accent="cyan" className="border-2 px-6 py-4" />
    <Arrow layoutId={ENTITIES.flow} className="text-3xl" />
    <Box layoutId={ENTITIES.result} label="Outcome" accent="green" className="border-2 px-6 py-4" />
  </div>
</SceneLayer>
```

For ad hoc visual checks, put Playwright/screenshot helper scripts under the
project root (for example `scripts/`) rather than a temp scratchpad outside the
project, so imports such as `playwright` resolve from local dependencies. Prefer
the scaffolded `npm run inspect -- <slug>` helper before writing a custom script.
Use `--settle-ms <ms>` only when a presentation deliberately uses longer custom
animations than the default settle wait.

### Adding a step

Copy `templates/single-step/step.tsx` into `steps/`, customize metadata and
layout, then append to the `STEPS` array in `Talk.tsx`.

### Navigation and chrome

The kit provides browse/present modes, captions per step, table of contents,
progress dots, and prev/next controls. Active TOC and progress items expose
`aria-current="step"` and `data-active="true"`, but the presentation must make
that current state visibly distinct in its own CSS. The attribution link also
needs presentation-owned styling so it is legible and intentional rather than a
raw browser-default anchor. Users navigate with →/Space/PageDown (next),
←/PageUp (prev), P (toggle mode), or horizontal swipe.

## Out of scope

This skill does **not**:

- Design or export non-browser slide decks (PowerPoint, Keynote, PDF, images)
- Process or convert existing slide-deck files
- Create unrelated React apps or generic frontend features outside presentations
- Handle image generation, hosting, or publishing

Redirect those requests to the appropriate skill or tool.

## Quality bar

Every generated presentation must:

- Build with `npm run build` — no type errors
- Render its first step without runtime or console errors
- Show a caption per step (browse mode) and support next/previous navigation
- Conform to the evolving-scene model (stable entities morph across steps)
- Pass a browser visual composition check: important steps fit within the fixed
  canvas, intentional overlaps remain readable, and scene content does not
  collide with browse/present chrome
- Make current-step chrome visibly distinct: active TOC/progress states must be
  readable, and the `made by and-scene` attribution must be legible and styled
  by the presentation or host app

## Templates

| Path | Purpose |
|------|---------|
| `templates/bootstrap/` | Full app snapshot for bootstrapping fresh/empty projects |
| `templates/presentation/` | New presentation folder (`entities.ts`, `steps/`, `Talk.tsx`) |
| `templates/single-step/step.tsx` | Template for adding one step |

Replace `{{PLACEHOLDER}}` tokens in templates with gathered content.

## Scripts

| Path | Purpose |
|------|---------|
| `sync-kit.mjs` | Diff/resync a project's vendored `src/presentation-kit/` against the shipped snapshot (see [Updating the vendored kit](#updating-the-vendored-kit)) |
| `templates/bootstrap/scripts/verify.mjs` | Build + render verifier used by scaffolded projects |
| `templates/bootstrap/scripts/inspect-presentation.mjs` | Project-local screenshot helper for visual composition checks |
