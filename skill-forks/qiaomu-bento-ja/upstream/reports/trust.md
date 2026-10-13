# Trust report

## Trust boundary

- Skill source: local package.
- Format authority: release-locked MIT-licensed bento shell and official
  documentation snapshots bundled in this skill; exact provenance is in
  `upstream.lock.json`.
- Remote inline execution: forbidden.
- Secrets: none required. Signing keys, tokens, cookies and account credentials
  are outside scope.
- File writes: plan, JSON, report and new `.bento.html` outputs only by default.
- Subprocesses: Python and browser launch; an upstream project shell gate is
  optional compatibility evidence, not a runtime dependency.
- Maintenance network: `scripts/sync_upstream.py` reads only the official
  GitHub release API, release asset and raw files for `nyblnet/bento`. Normal
  deck generation makes no upstream request.
- Automation: the scheduled workflow can push an automation branch and open a
  PR; it cannot merge or bypass the browser-review gate.

## rollback boundary

The default build refuses an existing output path. Editing an existing deck
produces a sibling output and leaves the source untouched. `--overwrite` is an
explicit user-authorized escape hatch; it is not used by the fixture eval.

Upstream refresh stages and validates the complete coherent release before a
replacement transaction. A failed download, malformed asset or checksum gate
restores the previous snapshot. The workflow never writes directly to `main`.

## Evidence

- `file-backed fixture`: `evals/fixtures/minimal-deck.json`.
- `input_files`: fixture JSON plus the bundled pinned bento shell.
- `output contract`: one parseable `.bento.html`, stable/minted identity report,
  structural validation and shell gates.
- `reports/output-eval.json` records a standalone fixture build with no bento
  checkout when executed.
- `reports/upstream-sync-eval.json` proves successful refresh, idempotent
  recheck, malformed-release rejection and rollback without network access.

## missing evidence

- Cross-platform browser review has not been run.
- The included example has one human/browser review; cross-platform review is
  still missing evidence.
- No provider-backed telemetry exists; none is claimed.
