# SlideMuse 2.11.0 engineering regression · 2026-10-02

This release adds grouped bar/column rendering and explicit numeric dependency updates. It preserves the completed three-case scoped acceptance; it does not resume the deferred 30-material target or establish a general first-pass success rate.

## Changed behavior

- The deterministic chart builder and endpoint auditor support grouped horizontal bars and vertical columns, including positive, negative and zero values. Series identity, a shared zero baseline and numeric-axis direction are checked. Stacked/logarithmic charts are excluded.
- Optional dependency contracts preview and synchronize declared source numbers, arithmetic, chart/table leaves, prose and notes. Current inconsistent bindings block updates. Draft exports leave originals unchanged and invalidate visible-content approval; unknown dependencies still require review.
- Delivery scoring can explicitly check the contract and reject inconsistent declared targets. Existing frozen benchmark batches are not silently extended with the new optional contract.

## Verification

- Local full suite: 335 tests on Windows/Python 3.14; Ruff and strict Page Spec validation. New negative controls cover missing/wrong grouped bars, swapped series identity, reversed axes, invalid formulas, stale dependent prose/notes, changed inputs after preview, approval invalidation and attempted report overwrites.
- Existing policy/statistics/reconstruction cases: five delivery branches re-evaluated using current code, all pass. Three native decks rebuilt and rendered through PowerPoint; all 16 pages are pixel-identical to the previous delivered native renders. Historical sealed records are unchanged. This is a compatibility regression using existing semantic reviews, not a new independent review of source truth.
- New two-page synthetic transport fixture: both original and modified native PPTX exports rendered through PowerPoint and visually inspected. Changing North's After value from90 to110 updates the chart data and 14 bound targets: total190→210, North share47.4%→52.4%, total change-5.0%→5.0%, prose and speaker notes. Both native structure audits verify the real embedded chart workbooks without errors or warnings.
- Standalone grouped column and bar PNGs inspected; tests independently sample actual color pixels for positive/negative/zero geometry. Construction coordinates are not reused as visual observations.

The new fixture is explicitly synthetic and a preview of changed engineering inputs, not a formally held-out material or a source-grounded transport result. Complex artwork remains raster. Formula-backed external workbooks, automatic dependency discovery, universal font fidelity and semantic truth are outside the new checks.

Local detailed logs, rebuilt decks and render comparisons: `slidemuse-2.11.0-验证` beside the source checkout. Remote CI, release archive and installed-runtime verification are recorded there after publication; this document's local results do not by themselves claim remote completion.
