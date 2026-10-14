# And Scene

And Scene is an Agent Skill for building animated, morphing browser
presentations. This repository contains the distributable skill, its reusable
React scene kit, scaffold templates, and the worked reference presentation.

## Project Map

- `skills/presentation/SKILL.md`: agent-facing presentation workflow and quality bar
- `skills/presentation/templates/bootstrap/`: complete app scaffold copied into new projects
- `skills/presentation/templates/presentation/`: files for an additional presentation
- `src/presentation-kit/`: canonical vendored React scene kit
- `src/presentations/`: reference presentations and registry
- `scripts/verify.mjs`: deterministic build and browser-render verification
- `scripts/inspect-presentation.mjs`: screenshot capture and visual-quality diagnostics
- `openspec/`: current behavioral specifications and historical changes

## Browser Tooling

Use `chrome-devtools-axi` for agent-driven browser inspection and debugging.
It is installed in the evaluation sandbox and provides a concise CLI over
Chrome DevTools:

```bash
chrome-devtools-axi open http://127.0.0.1:5173/
chrome-devtools-axi snapshot
chrome-devtools-axi screenshot /tmp/and-scene.png
```

Start with `snapshot` to inspect page structure, then use screenshots for visual
composition. Inspect the first, last, and dense or visually important steps;
also inspect a narrow viewport when the presentation is responsive-sensitive.
Use `chrome-devtools-axi --help` for the full command list. Do not invoke the
underlying Chrome DevTools MCP server directly when AXI is available.

Keep deterministic project verification in the repository's Playwright-backed
scripts. AXI is the interactive inspection interface; `npm run verify` remains
the automated browser gate.

## Development Workflow

```bash
npm ci
npm test           # Vitest unit and contract tests
npm run lint       # ESLint
npm run build      # TypeScript and production build
npm run verify     # build plus browser-render verification
npm run inspect -- how-to-make-a-presentation
```

Use test-driven development for behavior changes and bug fixes: add a focused
failing test, implement the smallest fix, then run the targeted test before the
full suite. Tests are not required for prose-only documentation changes.

## Change Guidelines

- Keep `src/presentation-kit/` byte-aligned with
  `skills/presentation/templates/bootstrap/src/presentation-kit/`; the snapshot
  parity tests enforce this for non-test files.
- Keep root verification and inspection scripts aligned with their bootstrap
  template copies when changing scaffolded behavior.
- Preserve the style-neutral kit contract. Presentations own colors,
  typography, spacing, and component treatments; do not add a required CSS
  framework or design system to the kit.
- Preserve stable `data-presentation-*` hooks and active-state semantics unless
  the corresponding skill instructions, templates, tests, and docs change
  together.
- Use `127.0.0.1` for local browser automation to avoid IPv4/IPv6 resolution
  differences.
- Do not commit generated build output, dependency directories, or inspection
  screenshots.

Before reporting completion, run the checks proportional to the change. For a
behavioral or scaffold change, run the full test, lint, build, and verify suite;
also inspect representative steps when visual composition may have changed.

## Commit Messages

Use `type: lowercase description`, where `type` is `fix`, `feat`, `docs`,
`test`, `refactor`, or `chore`.
