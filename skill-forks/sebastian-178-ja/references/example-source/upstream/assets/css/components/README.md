# Component CSS Packaging

`assets/css/components.css` remains the source-preview compatibility entry. Existing decks can keep linking the single file.

`manifest.json` maps root component classes to component families. The sibling family files (`shared.css`, `process.css`, `time.css`, `text.css`, `data.css`, `structure.css`, `people.css`) are split package sources generated from the full catalog.

`scripts/render.sh --package` scans the deck HTML, detects which root classes are present, and inlines `shared.css` plus only the required family files for the package. If detection fails or no component family is found, it falls back to the full stylesheet.

This keeps authoring simple while preventing every self-contained package from embedding the whole component catalog.

After editing `assets/css/components.css` or `manifest.json`, run `scripts/split-component-css.sh` from the repo root to refresh the family files.
