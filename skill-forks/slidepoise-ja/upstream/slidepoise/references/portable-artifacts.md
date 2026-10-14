# Portable presentation artifacts

Keep a presentation reviewable after the authoring session ends. The runtime can package the exact compiled inputs, preserve selected source evidence, and render all pages in one conversion. These operations report file facts. The host Agent still inspects the images and decides whether the result is faithful.

## Render the complete deck

Use a new preview directory for each revision. One LibreOffice conversion produces the complete PDF, and Poppler rasterizes its pages in presentation order.

```bash
python scripts/slidepoise_runtime.py render-deck-preview \
  --pptx deliverables/presentation.pptx \
  --output-dir deliverables/preview-v1
```

The directory contains

- `presentation.pdf`
- `slide-001.png`, `slide-002.png`, and subsequent pages
- one `.source.json` record per page with the source PPTX hash, render hash, page number, DPI, and font environment
- `contact-sheet.png` for sequence review
- `preview-manifest.json` with ordered page bindings and hashes for the PDF and contact sheet
- `rendered-text-evidence.json` with native table words extracted from that PDF and discrepancies for the Agent to inspect

The command prints the evidence path, availability, inspected cell count and discrepancy count. Single-page `render-preview` produces the same evidence for its selected page as `<render-stem>.text-evidence.json`. Both preview paths bind this evidence in the render sidecar. Missing extraction and zero discrepancies are different outcomes. Neither establishes the visual quality of the slide.

`--dpi` defaults to 120. `--font-config` accepts the same optional run-local Fontconfig file as `render-preview`. Use individual full-resolution pages when the contact sheet hides a detail. The command stops when the page count differs from the PowerPoint or the source changes during rendering. A failed conversion leaves no partially published preview directory.

## Preserve a portable deck

Bundle the compiled scenes and their raster sources before sharing a reproducible case. Source images used by several slides are stored once by content hash. Raster paths in the copied scenes become relative to those scenes. The original authoring files stay unchanged.

```bash
python scripts/slidepoise_runtime.py bundle-deck \
  --manifest work/deck-scenes.json \
  --output-dir presentation-bundle \
  --include work \
  --include slides
```

Each optional `--include` copies one explicitly selected source file or directory under `evidence/<name>`. Use distinct names. The bundle output must be outside the included source directories. Evidence retains its exact bytes and authored pointers. It is a record of the source work, and any example rebuild script must resolve its input paths explicitly.

The bundle contains `deck-scenes.json`, `scenes/`, `assets/`, optional `evidence/`, and `bundle.json`. The last file records every bundled file's SHA-256 and byte count, along with slide order. Scene loading checks missing assets, malformed scenes, and incompatible dimensions before rendering. Legacy run-root-relative scene paths remain supported when unambiguous. New bundles declare scene-relative asset paths explicitly.

## Verify and rebuild

Move the bundle to another directory or machine with the SlidePoise runtime available, then verify it before rendering.

```bash
python scripts/slidepoise_runtime.py verify-bundle \
  --bundle-dir presentation-bundle

python scripts/slidepoise_runtime.py render-deck \
  --manifest presentation-bundle/deck-scenes.json \
  --output rebuilt/presentation.pptx
```

Write rebuilt outputs outside the bundle. Verification checks a closed file inventory and reports added, missing, or changed source files. The bundle does not include runtime dependencies or fonts. The preview records the font environment used for inspection, so a different renderer or font installation still needs visual review.

File bindings establish which bytes were bundled. They do not establish who authored the content or issue a visual acceptance decision. Keep host-authored reviews and the exact inspected artifacts with the case when they are useful to understand its design and reconstruction.
