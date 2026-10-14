# SlideMuse 2.9.0 acceptance · 2026-10-01

## Observable gaps and changes

Image-deck export previously omitted the optional speaker notes in the content draft. Editable export supported legacy Scene notes, but object/delivery auditing did not verify them against the actual PPTX. Adding speaker notes to a page also needed export invalidation without regenerating its unchanged picture.

This release adds optional `speaker_notes` to Page Spec and Scene, exact save/reopen checks for both builders, upstream notes/order validation through editable `--page-spec`, an actual-notes audit integrated into the scorecard, and a source-referenced Markdown companion. Notes-only changes reuse images but rebuild exported decks. Legacy undeclared Page Specs and legacy Scene notes remain readable; explicit empty notes reject residual text. Page Spec work records are not inferred as presenter content.

Official [Slidev exporting](https://sli.dev/guide/exporting.html) and [Marp Markdown](https://github.com/marp-team/marp-core/blob/main/docs/markdown.md) informed the design. No third-party code was copied or required. The image-first workflow and existing content/style authorization gates remain in place.

## Local validation

- 226 tests passed; Ruff and skill validation passed. Real note mutation tests reject missing/changed/reordered notes, mismatched Scene, and missing upstream notes even when recorded text/visual checks pass. Notes checking preserves the existing unresolved-content reconstruction workflow; it does not imply semantic approval.
- The approved 8-page city-transport example was copied into a separate validation workspace with speaker notes added as development regression data. Existing approved artifacts were not overwritten.
- Both new PPTX variants were rendered with PowerPoint, visually inspected and evaluated with current hash-bound evidence. Both scorecards passed, all eight declared notes matched, and 61 known semantic elements remained intact.
- Image-deck render pixels matched the previous render on every page. All eight editable slide XML parts matched the previous build; render antialiasing pixels differed slightly, with no newly observed clipping. Pixel equality is not a universal quality threshold.
- Source page images remained byte-identical. Actual bar endpoints were remeasured, checks passed. Notes-only planning reused all eight pictures and required rebuilt exports; clearing page 3's notes failed the independent audit.

## Content-depth validation and limits

Paper/long-policy content-stage review expanded formula-variable explanations and verified a paper source conflict. Additional risk checks distinguish training parallelism from autoregressive generation, and policy targets from observed effects; they are not claimed as errors in previously generated paper/policy decks. The targeted material-reading reference covers these cases; source conflicts must be recorded and scope narrowed or verified. This is current-Agent semantic review, not an independent blind evaluation.

Only the statistics example completed a full visual export regression. Paper/policy material did not receive new style/image generation. Notes auditing verifies declared text fidelity, not semantic depth, source truth or performance. Complex formulas remain independent raster objects when native recovery is unsupported; this release does not implement KaTeX or native Office equations.

Release CI, published-package hashes and actual installation are verified separately before final delivery; local tests alone do not establish remote release completion.
