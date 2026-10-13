# Output quality scorecard

| Dimension | Gate | Current evidence |
|---|---|---|
| Package | `validate_skill.py` | pass, 2026-07-26 |
| Routing | trigger eval | 14/14 pass, 2026-07-26 |
| Standalone | clean fixture run with bundled shell, no checkout | pass, 2026-07-26 |
| Bundled provenance | SHA-256 + MIT notice | pass |
| Upstream release | coherent release lock + live check | v1.0.10, commit `030a81a`, pass 2026-07-27 |
| Upstream rollback | offline refresh/no-op/malformed fixture | all 6 checks pass, 2026-07-27 |
| Format | `bento_deck.py validate` | standalone file-backed fixture pass |
| Identity | edit preserves; new build mints once | both fixture checks pass |
| Shell | internal gate + project `shell-gate.mjs` | both fixture checks pass |
| Rollback | source hash unchanged; output is separate | fixture check pass |
| Visual quality | editor, presentation, motion, state interaction, console | refreshed v1.0.10 shell passed in Codex in-app Chromium, 2026-07-27; zero warnings/errors |
| Public install | `npx skills add` list + clean remote install | pass, 2026-07-26 |

The example product deck has passed one real Chromium review. Cross-platform
browser review remains missing evidence; the fixture still proves mechanical
construction and validation only.
