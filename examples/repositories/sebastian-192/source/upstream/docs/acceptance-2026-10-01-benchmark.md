# SlideMuse 2.10.0 engineering acceptance · 2026-10-01

This is engineering evidence and development validation, not the 30-material acceptance result.

- Windows/Python 3.14: all **304 tests passed**; Ruff and skill-format validation passed.
- Benchmark records freeze source identities and rubric bytes, preserve first/final attempts, retain missing/aborted cases in the denominator, rerun actual delivery checks, and bind Scene assets including auditing references.
- Independent code review reproduced two defects before repair: an unbound Scene reference image and a chart cache-only edit with stale embedded workbook data. Regression tests now reject both; a changed/deleted auditing reference invalidates old results, while cache-only/workbook-only edits and unverified formula cells fail native chart auditing.
- A verified Page Spec projection excludes generation/work prompts and author notes. Tests reject changed content, unknown fields added after resealing, and overwriting the source. Objective invocation records still require separate isolation from author quality judgments.

A six-page Transformer reading prototype has actual image and native PPTX exports, PowerPoint renders and independent component review. It contains 256 native editable objects. The original table edit exercise left its dependent calculation and notes stale; its failed modification finding is preserved. A separate synthetic exercise updates the table, difference, notes and visible synthetic disclosure, and has been rebuilt and rendered. Formal paper values remain unchanged.

The prototype was not registered before generation and its reviewers encountered author work fields. It cannot be counted as a formally frozen first-delivery pass or an unexposed independent acceptance result. Six further primary-source development candidates were collected across the six material categories; they are source snapshots, not completed cases. The full 30-material/10-holdout objective remains active and unverified.

Embedded chart auditing currently verifies literal cells generated from the supported Scene chart data. Formula-backed external workbooks need a separate verified data contract; cached formula results cannot establish equivalence.
