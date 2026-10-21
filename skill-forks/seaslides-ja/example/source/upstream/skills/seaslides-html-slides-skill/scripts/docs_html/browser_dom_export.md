# Browser DOM SVG Export

The HTML slide pipeline renders `index.html` in Chromium, waits for fonts,
MathJax, pseudocode.js, syntax highlighting, charts, images, and template
scripts to settle, then serializes each `.slide` DOM subtree into SVG.
`output/pngs/` is rendered from those SVGs in Chromium. `output/browser_pngs/`
is captured directly from Chromium before DOM-to-SVG conversion, so it can be
used as the visual baseline when debugging SVG conversion differences.

This route intentionally follows browser layout instead of a separate HTML/CSS
reimplementation. Templates can use normal browser CSS, including grid,
absolute positioning, pseudo-elements, gradients, shadows, filters, and
script-generated DOM, as long as the final slide is visually complete in
Chromium at the target canvas size.

## Export Contract

| Area | Requirement |
|---|---|
| Slide root | Each slide is a `.slide` section with stable 1280x720 sizing unless the project format overrides it. |
| Assets | Relative URLs should resolve from the assembled `index.html`; external network assets are less reproducible and should be avoided. |
| Math | Use `\(...\)` and `\[...\]`; MathJax SVG output is captured by the browser exporter. |
| Code | Use `<pre><code class="language-*">`; template scripts may run syntax highlighting before export. |
| Pseudocode | Use pseudocode.js blocks when the template includes it; KaTeX core remains available only for that library. |
| Charts | Prefer SVG or DOM charts that are present in the final DOM before export. |
| Animations | Export captures a static settled state; author slides so the first settled frame is complete. |

## Quality Checks

1. Run `python ${SKILL_DIR}/scripts/validate_project.py <project> --source-only --profile standard-project`, then `python ${SKILL_DIR}/scripts/html_compiler.py <project> --all`.
2. Inspect `output/overview.png`, every page in `output/browser_pngs/`, and `output/dom-audit.json`; the settled browser route is layout truth, while the overview is only a routing aid.
3. Use `output/pngs/slide_XX.png` and `output/render-fidelity.json` only to diagnose SVG conversion differences.
4. For slides with math, code, charts, or pseudocode, check the corresponding
   `output/svgs/slide_XX.svg` if PPTX text/vector conversion quality matters.
5. Run `python ${SKILL_DIR}/scripts/validate_project.py <project> --require-build --artifact-profile visual`. When PowerPoint is required, rebuild with `html_compiler.py <project> --all --include-pptx` and validate with `--require-build --artifact-profile delivery`.

### Optional Vertical-Composition Contract

The DOM audit always records overall meaningful-content bounds. It records a
separate `verticalBalance` profile after excluding
`[data-audit-chrome]`/`[data-audit-balance-ignore]`. To make a content page
eligible for a composition review item, opt in explicitly:

```html
<section class="slide" data-audit-composition="top-to-bottom">
  <main data-audit-content>...</main>
  <footer data-audit-chrome>...</footer>
</section>
```

The theme may provide these CSS custom properties; zero or missing values
disable the associated check:

| Property | Meaning |
|---|---|
| `--seaslides-nav-safe-bottom` | Reserved inset from the canvas bottom |
| `--seaslides-audit-bottom-gap-max` | Largest acceptable gap from meaningful body content to the safe bottom |
| `--seaslides-audit-active-height-min` | Minimum meaningful top-to-bottom span inside the usable frame, from 0 to 1 |
| `--seaslides-audit-vertical-gap-max` | Optional maximum internal blank band for a top-to-bottom page |

Equivalent numeric `data-audit-*` threshold attributes are interpreted as
canvas pixels, except active-height ratio. CSS lengths may use theme units such
as `vh`; the audit resolves them in Chromium. A top-heavy finding requires
explicit `top-to-bottom` mode, an explicit content root, excessive bottom gap, and
insufficient active height. It remains a review item rather than a blocker.
Pages without the explicit contract receive observation-only telemetry, so
covers, quotes, dividers, and deliberate negative space do not become false
positives. Chrome excluded from composition is still checked for clipping and
canvas overflow.

### Meaningful SVG and Canvas Content

The audit treats an `svg` or `canvas` as meaningful only when it has
`data-audit-meaningful`, `role="img"`, an accessible label, an HTML `title`, or
a direct SVG `<title>`. Text descendants are audited as their own visible
elements. Mark decorative graphics with `aria-hidden="true"` or
`data-audit-ignore`. This keeps off-canvas background art out of content bounds
while preserving blocker checks for charts and diagrams that carry meaning.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---|---|---|
| Blank slide SVG | JavaScript error or no `.slide` elements in assembled HTML | Open root-level `index.html` in Chromium and check console errors. |
| Missing icon/image | Relative path resolves differently after assembly | Use project-relative assets and verify the final `index.html` path. |
| Formula not typeset | MathJax block missing from template or script ran too early | Use the current source template and call `window.__typesetMath` from dynamic render hooks when needed. |
| Chart missing | Chart script renders asynchronously after export starts | Register chart rendering inside `window.__renderDynamicContent` or finish before the exporter captures slides. |
| PPTX text conversion differs from PNG | Browser SVG uses `foreignObject` or complex SVG features | Inspect SVG/PPTX output; preserve image-backed slide elements when editable text is not essential. |

## Implementation Notes

- HTML to SVG: `scripts/html_to_svg/browser_dom_to_svg.mjs`
- SVG to PNG: `scripts/html_to_svg/browser_svg_to_png.mjs`
- HTML to browser PNG: `scripts/html_to_svg/browser_html_to_png.mjs`
- Unified compiler: `scripts/html_compiler.py`

The exporter keeps the browser-rendered DOM as the source of truth. Avoid
adding template constraints solely for a non-browser renderer.
