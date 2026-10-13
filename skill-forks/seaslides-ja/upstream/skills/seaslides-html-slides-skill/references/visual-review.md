# Visual Review Rubric

## Purpose

This document is a systematic post-build quality gate for HTML slide presentations. After `html_compiler.py --all` atomically produces root-level `index.html`, both PNG routes, and receipts, the reviewing agent inspects the browser-rendered output to detect defects that source validation alone cannot catch — overflow, collision, readability, rhythm, and vertical-composition issues. Mechanical measurements support that judgment but never replace page-by-page review.

Use [`artifact-ownership.md`](./artifact-ownership.md) to route each confirmed defect to content, theme, runtime, source, or export ownership before applying a correction.

## Hard Rules (Must Fix)

These are critical issues that ALWAYS need correction. Any Hard rule violation on any slide blocks delivery until fixed.

| # | Category | Trigger | What to Look For |
|---|----------|---------|------------------|
| H1 | HTML Structure | Invalid slide structure | Missing `<section class="slide">` wrapper, unresolved slide mode, broken nesting |
| H2 | CSS Class Validity | Undefined CSS class used | Content.html references a class not defined in template.css |
| H3 | TCS Violation | Forbidden inline styles in content.html | Any inline declaration outside the canonical data-geometry allowlist in `shared-standards.md` |
| H4 | Export Readiness | Browser-rendered output is not ready for SVG/PNG/PPTX export | Missing settled math/chart/code rendering, unresolved external assets, animation-only content, or stale copied templates |
| H5 | Speaker Notes Missing | Slide lacks usable `data-notes` | Every `<section class="slide">` must have a non-empty `data-notes="..."` value |
| H6 | Mode Unresolved | Slide lacks a valid light/dark mode | Every slide must explicitly include `light`, `dark`, `hero light`, or `hero dark`, unless the selected theme's `theme.md` documents its default mode |
| H7 | Text Overflow | Text clipped or hidden by container | Truncated words, text running past component boundaries, content cut off at slide edges |
| H8 | Text Overlap | Two text elements overlap | Overlapping headings/body text, labels colliding with other text, unreadable stacked characters |
| H9 | Readability | Contrast ratio below threshold | Light text on light backgrounds, dark text on dark backgrounds, text on WebGL backgrounds without opaque component background |
| H10 | Element Collision | Unintended overlaps between layout elements | Cards overlapping, images covering text, components blocking each other |
| H11 | Missing Elements | Element referenced in design spec is absent | Missing title, absent component, placeholder text still present, slide appears emptier than spec requires |
| H12 | Broken Images | Image fails to load or render | Missing `assets/` files, incorrect `src` paths, broken `<img>` elements |
| H13 | Data Geometry Error | Chart geometry is invalid or contradicts its label | Non-numeric values, forbidden properties, or visibly incorrect bar/step sizes |
| H14 | Gate Failure | Source or final project gate reports failures | Source/TCS errors, stale/missing build artifacts, or DOM-audit blockers |

**Detection order** (check sequentially per slide):

```
H14 (source/final gate output)  -> H1 -> H5 -> H6 (structure)
H2 -> H3 -> H4            (TCS and export readiness)
H7 -> H8 -> H10           (collisions)
H9                         (readability)
H11 -> H12 -> H13         (content completeness)
```

### Hard Rule Details

**H1 -- HTML Structure**: Every slide must be a `<section class="slide ...">` element. Check that nesting is correct, that no `<div>` masquerades as a slide wrapper, and that all required child structure (layout div, components) follows the patterns in `components.md` and `layouts.md`.

**H2 -- CSS Class Validity**: Project-specific component and layout classes used in `content.html` must be supported by the selected theme. Do not apply a naive source-regex gate: runtime classes, shared-library classes, and selector composition make it noisy. Confirm suspicious classes against `theme.md`, `template.css`, the settled DOM/CSSOM, and the browser render.

**H3 -- TCS Violation**: Content.html may use inline style only for numeric data geometry on the class/property allowlist in `shared-standards.md`. Any decorative, typographic, spacing, color, position, or unlisted declaration is a TCS violation. Run `validate_project.py` rather than maintaining another local allowlist.

**H4 -- Export Readiness**: Run the visual build and check `output/browser_pngs/` plus `output/overview.png` for the settled browser state. Math, pseudocode, syntax highlighting, charts, images, and fonts must be visible before export. `dom-audit.json` is the browser-layout truth and must report no blockers. Use `render-fidelity.json` and matching SVG-route PNGs only to investigate browser-to-SVG conversion differences. Copied benchmark templates must be refreshed from the current source template before rerendering old projects.

**H5 -- Speaker Notes Missing**: Every `<section class="slide">` must have a non-empty `data-notes="..."` value. Empty or missing notes fail the source gate because they leave the delivery without usable narration context. For a PPTX delivery, the compiler embeds these values in source order and the delivery validator checks the notes roster and slide relationships; a PPTX with zero or partial notes cannot pass.

**H6 -- Mode Unresolved**: Every slide must resolve to `light`, `dark`, `hero light`, or `hero dark`. Prefer an explicit class. A missing class is valid only when the selected theme's `theme.md` documents the default mode; do not infer validity from incidental CSS inheritance.

**H7 -- Text Overflow**: All text must be fully visible within its container. In SVG export, overflow clips silently. Look for abruptly ending sentences, partial characters at component edges, or content that runs beyond the 1280x720 viewport boundary.

**H8 -- Text Overlap**: No text should overlap other text or obscure readability. Exception: intentional decorative elements at very low opacity.

**H9 -- Readability**: Minimum contrast ratio 4.5:1 for body text, 3:1 for large text (>= 3vw). Components used on dark slides or over WebGL backgrounds MUST have opaque `background` or `background-color` to guarantee readability.

**H10 -- Element Collision**: Layout elements (cards, components, images) must not overlap unless the overlap is intentional. Accidental collisions typically come from incorrect flex sizing, missing explicit widths, or overflow-hidden clipping.

**H11 -- Missing Elements**: Cross-reference the rendered slide against `content_design_spec.md`. Every element described in the spec must be visually present.

**H12 -- Broken Images**: Every `<img>` element must have a valid `src` pointing to an existing file in `assets/`. Check for: missing files, typos in filenames, incorrect relative paths. All images must have `alt` text.

**H13 -- Data Geometry Error**: Data fills may use numeric pixels or percentages as permitted by the canonical allowlist. Verify that rendered lengths/heights match their labels, share an appropriate scale, stay inside their tracks, and remain auditable. The validator checks syntax; visual review checks semantic correctness.

**H14 -- Gate Failure**: Run both required project gates: source validation before build and the final visual gate after it. Any source/TCS error, stale/missing visual artifact, invalid compiler receipt, or DOM-audit blocker is a Hard failure.

## Soft Rules (Should Improve)

These improve quality but are not blocking failures individually. Fix when 3 or more cluster on a single slide.

| # | Category | Trigger | Fix Direction |
|---|----------|---------|---------------|
| S1 | Anti-Monotony | A repeated-layout run feels mechanical or obscures progression | Confirm repetition is intentional; redesign only when it weakens the narrative |
| S2 | Component Diversity | Component vocabulary feels too narrow for the content | Add a component only when it communicates the material better |
| S3 | Typography Hierarchy | Unclear visual distinction between heading levels | Increase size/weight differentiation between `.h-md`, `.h-sm`, body text |
| S4 | Breathing Rhythm | Sustained density harms comprehension | Add a breathing or divider slide at a real narrative pause |
| S5 | Mode Monotony | A long same-mode run weakens hierarchy | Change mode when contrast serves the content |
| S6 | Color Discipline | A hue lacks a communication or selected-theme identity role | Remove the unsupported hue or assign it a stable semantic role |
| S7 | Whitespace Balance | Content is visibly cramped, stranded, or disconnected from the theme's safe geometry | Recompose with the owning layout/container tokens |
| S8 | Vertical Rhythm | Inconsistent spacing between consecutive elements | Normalize spacing to consistent gap values from CSS tokens |
| S9 | Alignment Consistency | Elements that should be aligned drift visually | Verify flex alignment and explicit widths |
| S10 | Image-Text Relationship | Images positioned illogically relative to their descriptions | Move image adjacent to relevant text |
| S11 | Density Adherence | Slide density mismatches its rhythm designation | Adjust content volume to match slide role |
| S12 | Card Design Mismatch | Rounded corners in swiss-international, or hairline-only in editorial | Match card treatment to theme identity |
| S13 | Header Bar Check | Full-width solid rectangle as title container on content slides | Use thin accent line, subtle border, or title directly on background |
| S14 | CJK Spacing | Improper spacing between CJK and Latin characters | Verify font stack includes CJK fallbacks; check character spacing |
| S15 | Typography Weight | All headings use same weight with no variation | Introduce weight hierarchy matching theme identity |

### Soft Rule Details

**S1 -- Anti-Monotony**: After the overview scan, review runs of repeated layouts. Keep them when they create a stable comparison, tutorial, timeline, or analytical grammar. Redesign only accidental or visually tiring repetition.

**S2 -- Component Diversity**: Judge whether the chosen component vocabulary expresses the content effectively. Do not add component types merely to reach a quota.

**S3 -- Typography Hierarchy**: Review the heading usage. If `.h-md` and `.h-sm` are visually indistinguishable, or if body text is nearly the same size as headings, the hierarchy is too flat. Each level should have clear visual differentiation.

**S4 -- Breathing Rhythm**: When a deck contains a sustained dense passage, consider a breathing page at a real pause. Dark or hero modes can carry key statistics, section transitions, or closing statements, but are not mandatory by page count.

**S5 -- Mode Monotony**: Review long same-mode runs for weak hierarchy. Retain a stable mode when it improves continuity; change mode when contrast has a semantic purpose.

**S6 -- Color Discipline**: Confirm that each hue has a communication or selected-theme identity role and that repeated roles stay consistent. Do not apply a universal hue-count limit; a deliberate multi-primary theme and a restrained single-accent theme have different valid contracts.

**S7 -- Whitespace Balance**: First identify the page's vertical mode:
centered cluster, top-to-bottom, split anchors, image hero, or intentional
breathing. Hero, quote, cover, divider, and closing pages may be sparse when the
empty field clearly frames a focal point. A content/data page is not balanced
when its meaningful body is packed into the upper region and the remaining
middle/lower field has no directional or semantic function. A page number,
footer, or decorative rule does not count as a lower content anchor.

When the theme opts in with `data-audit-composition="top-to-bottom"`, inspect
`dom-audit.json` composition telemetry alongside the PNG. The audit excludes
`data-audit-chrome` only from composition; that chrome still participates in
overflow and clipping checks. Bottom gap and active-height findings are
theme-owned review prompts, not universal fill percentages.

Fix a pronounced S7 defect even when no other Soft rule clusters on that slide.
First repair body-height ownership, then redistribute existing semantic groups,
then enlarge a real chart/table/process/media slot or move an existing real
takeaway/source/status anchor. Do not add filler copy, empty components, or
arbitrary spacer nodes.

**S12 -- Card Design Mismatch**: Each theme has specific card treatment rules. In swiss-international and cyber-neon, cards must have zero `border-radius`. In aurora-gradient, cards use 16px radius. In data-dashboard, cards use 8px radius. In editorial-magazine, cards may have 4-8px rounded corners and warm fills. In ink-landscape, cards use vermillion top borders. In mckinsey-minimal, cards use accent top borders with minimal decoration. In ivory-theorem, cards use navy left borders for theorem blocks and warm ivory fills for definition boxes. In chalk-classroom, cards use chalk-style dashed borders (2px dashed) on chalkboard green. In bloomberg-dark, cards use subtle 1px borders on near-black backgrounds with scarlet accent borders for focal cards. Mixing theme treatments produces visual incoherence.

**S13 -- Header Bar Check**: The full-width solid-color rectangle spanning slide width as a title container is the #1 "AI slop" signal. Acceptable alternatives: thin accent underline, typography-only heading with generous top margin, or subtle border-bottom.

**S15 -- Typography Weight**: Each theme has specific weight hierarchies. For swiss-international: display weight 200, body headings 600, labels 500. For editorial-magazine: heading weight 600-700, body 400, meta in monospace. For aurora-gradient: display weight 700, body 400. For cyber-neon: display weight 600-700, metrics in monospace. For data-dashboard: compact sizing with mono metrics. For ink-landscape: serif headings 600-700, body 400. For mckinsey-minimal: clean weight 400-700. For ivory-theorem: serif headings 600-700, body 400, mono for code blocks. For chalk-classroom: handwritten headings 400-700, body 400, approachable weight contrast. For bloomberg-dark: serif headings 400-700, body 400, tabular mono for financial numbers. Uniform weight everywhere kills theme identity.

## Don't-Touch Rules

The reviewer must NOT change these aspects, even if they seem suboptimal:

- **Theme design decisions** -- preserve colors, fonts, and component styles unless they are the root cause of a Hard rule violation or a theme/API defect
- **Content text** -- wording, messaging, and copy written during the Strategist phase
- **Layout architecture** -- column counts, layout class choices from the design spec
- **Slide count or ordering** -- adding, removing, or reordering slides is out of scope
- **Image content** -- what the images depict (only their technical presence and sizing is in scope)
- **Speaker notes content** -- narration text is not a visual review concern (only its presence/absence matters)
- **Template files** -- for an ordinary project issue, fix `content.html`. When the root cause is a reusable theme/API defect, fix the copied `template.css` or `index-template.html`, then rebuild and re-review; do not paper over it with forbidden content inline styles

If a violation can only be fixed by changing a Don't-Touch element, mark it as `needs_human` with a suggested fix description.

## Quantified Thresholds

| Rule | Threshold | How to Verify |
|------|-----------|---------------|
| H1 | Every slide = `<section class="slide ...">` | Structural inspection of content.html |
| H5 | Every slide has non-empty `data-notes` | Attribute and trimmed-value check on all `<section>` elements |
| H6 | Every slide has resolved mode | Explicit class or selected theme's documented default |
| H7 | 0 characters clipped | Check browser PNG baseline, then SVG-route PNG only when diagnosing conversion |
| H8 | 0 unintended text overlaps | Scan for overlapping text regions in rendered output |
| H9 | WCAG AA: 4.5:1 body text, 3:1 large text (>=3vw) | Compare foreground/background hex values from theme tokens |
| H13 | Data geometry matches labels and scales | Inspect chart fills and validator output |
| H14 | Source and final project gates pass | Run the commands below with zero errors |
| S1 | Repeated layouts are intentional | Scan layout sequence in narrative context |
| S5 | Mode changes serve hierarchy | Scan mode sequence in narrative context |
| S6 | Every hue has a stable semantic or theme-identity role | Compare palette roles and repeated use across the deck |
| S7 | Content is neither cramped nor unintentionally stranded | Inspect every browser PNG against the selected theme's vertical mode; use explicit composition telemetry only as supporting evidence |

## Review Workflow

### Step 1: Source Gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --source-only --profile standard-project
```

Check for H14. If errors exist, fix the project source before proceeding.

### Step 2: Visual Build

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all
```

Produces both PNG routes, overview, PDF, `dom-audit.json`, `render-fidelity.json`, and `compile-manifest.json` in one build. `dom-audit.json` is the settled browser-layout truth; `render-fidelity.json` is a review-only comparison of direct browser and SVG-route PNGs; `compile-manifest.json` proves the published artifacts match current inputs and toolchain.

### Step 3: Overview Scan

Review `output/overview.png` and direct-browser `output/browser_pngs/`. Perform a rapid scan for obvious issues:
- Any slide that looks broken, empty, or drastically different from expected
- Obvious overflow or clipping
- Glaring color/contrast issues
- Missing images (broken `<img>` elements)
- Bar charts with zero-width or visibly incorrect fills
- Repeated pages whose meaningful bodies all stop at the same upper position
- Footer-anchored pages with an otherwise empty middle/lower composition

The overview is a routing aid, not the review itself.

### Step 4: Page-by-Page Inspection

Inspect every direct-browser PNG at a projection-like scale. For each slide:
1. Examine the direct-browser PNG first
2. Compare the matching SVG-route PNG and `render-fidelity.json` only if the conversion route differs
3. Check all Hard Rules (H1-H14) -- any failure means fix immediately
4. Identify the page's vertical mode and check whether lower-page whitespace is intentional or dead
5. Check Soft Rules (S1-S15) -- note issues

### Step 5: Fix Protocol

- **Always fix** Hard rule violations -- zero tolerance
- **Fix Soft rule violations** if 3 or more issues cluster on one slide, or if one pronounced S7/S8 composition defect materially weakens the page
- **When fixing**: for ordinary project issues, make minimal changes to `content.html`; for reusable theme/API root causes, fix the copied template/theme source. Preserve design intent.
- **After fixing**: re-run the source gate, rebuild with `--all`, and verify the browser baseline did not introduce new issues
- **After 3 unsuccessful fix-build iterations**, stop repeating the same correction, reassess artifact ownership/root cause, and report only if the next step needs user authority or a broader design decision

### Step 6: Final Visual Gate and Sign-off

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --require-build --artifact-profile visual
```

- All Hard rules pass across all slides -> proceed to delivery. If PPTX is requested, run `html_compiler.py <project> --all --include-pptx` and then the delivery-profile gate; do not append a standalone PPTX export.
- Remaining minor Soft advisories -> acceptable, note in review; a pronounced uncorrected S7/S8 issue is not a clean visual sign-off
- If a Hard rule cannot be fixed without violating Don't-Touch rules -> flag to user with explanation and suggested approach

## Iteration Protocol

```
Iteration 1: Source gate -> --all build -> Browser overview scan -> Fix Hard violations
Iteration 2: Re-scan -> Fix remaining Hard + clustered Soft -> Source gate -> --all build
Iteration 3: Final verification only -- if issues remain, report to user
```

**Termination conditions**:
- **Clean exit**: Zero Hard violations and no pronounced uncorrected composition/readability issue -> status = pass
- **Fixed exit**: Had violations, all resolved within 3 iterations -> status = fixed
- **Escalation**: Cannot resolve within 3 iterations or fix requires Don't-Touch changes -> status = needs_human

**Rollback discipline**: If a fix introduces a new Hard violation that did not exist before, revert the change immediately and try an alternative approach. If no alternative exists, mark as `needs_human`.
