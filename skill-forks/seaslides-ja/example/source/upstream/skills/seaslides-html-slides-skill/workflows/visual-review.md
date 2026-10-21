---
description: Post-assembly visual quality review for HTML slides
---

# Visual Review Workflow

> Quality gate after assembly produces index.html. Validates structure, TCS compliance, browser export readiness, and visual quality.

## Trigger

After Step 7.2 assembly in the main pipeline produces root-level `index.html`. This corresponds to Step 7.3 in SKILL.md.

## Process

```
Source Gate --> Build --> Review Browser Baseline --> Fix --> Rebuild --> Final Gate (max 3)
```

---

## Step 1: Run Validation

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --source-only --profile standard-project
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all
```

Fix any reported violations before proceeding. Common issues:
- `<style>` or `<script>` tags in content.html (TCS violation)
- Inline `style="..."` attributes outside the canonical data-geometry allowlist
- Slides with neither an explicit mode nor the selected theme's documented default
- Undefined CSS classes not in template.css

---

## Step 2: Review Browser Baseline

Inspect `output/overview.png`, then every settled browser-rendered PNG at a
projection-like scale. The overview routes attention but cannot prove small
text, internal spacing, or vertical composition. Treat browser PNGs and zero
blockers in `output/dom-audit.json` as layout truth. Use SVG-route
`output/pngs/` and `output/render-fidelity.json` only to diagnose conversion
differences; they do not replace browser review.

For each page, identify whether its vertical mode is a centered cluster,
top-to-bottom body, split anchors, image hero, or intentional breathing page.
Do not confuse a footer at the safe bottom with a balanced body: content packed
at the top with a dead middle/lower field remains a composition defect.

---

## Step 3: Apply Review Rubric

### Hard Rules (must fix)

| Check | Criteria |
|-------|----------|
| **HTML structure** | Every slide is a `<section class="slide ...">` with proper nesting |
| **CSS class validity** | Only classes defined in `template.css` are used; no invented classes |
| **TCS compliance** | Zero `<style>`, `<script>`, `<link>` in content.html; inline style only for canonical data geometry |
| **Speaker notes** | Every `<section>` has a `data-notes="..."` attribute with real content (not empty) |
| **Mode classes** | Every slide has one of: `light`, `dark`, `hero light`, `hero dark` |
| **Export readiness** | Math/chart/code rendering is settled; images and fonts resolve; browser DOM audit has no blockers. SVG-route fidelity findings are conversion diagnostics. |
| **Image references** | Required/relevant images are used; paths and exclusions are valid |

### Soft Rules (fix if 3+ violations cluster on one slide)

| Check | Criteria |
|-------|----------|
| **Anti-monotony: layout** | Repeated layouts are intentional and support comparison or sequence |
| **Anti-monotony: mode** | Mode changes serve hierarchy rather than a fixed cadence |
| **Component diversity** | Component vocabulary is sufficient for the content without quota-filling |
| **Typography hierarchy** | Correct font family per theme; proper size hierarchy visible |
| **Content density** | Balanced content per slide -- not too sparse, not overflowing |
| **Vertical composition** | Empty space has a clear framing/anchoring role; content pages are not stranded at the top |
| **`data-anim` attributes** | Animation attributes present on slides where transitions add value |
| **Color restraint** | Accent color in max 2-3 element types per slide |
| **Dense-then-breathe** | Sustained dense passages include breathing room where comprehension needs it |
| **Hero cadence** | Hero slides appear only at meaningful emphasis or transition points |

---

## Step 4: Fix and Re-assemble

If issues are found:

1. **Edit `content.html`** -- fix structural, class, or content issues
2. **Edit `template.css`** -- fix reusable layout ownership or component geometry at the theme/API owner; do not use content inline-style workarounds
3. **Re-run the source gate and rebuild**:
   ```bash
   python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --source-only --profile standard-project
   python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all
   ```
4. **Re-review** the new browser baseline.

After 3 unsuccessful iterations on the same issue, stop repeating the same
repair and reassess its owner/root cause. Continue with a different safe fix;
report to the user when resolution requires broader authority or a design
decision.

---

## Decision Table

| Review Result | Action |
|--------------|--------|
| All Hard rules pass and no pronounced composition/readability issue remains | Run the visual artifact gate; status: **pass** |
| Hard violations found and fixed within 3 iterations | Run the visual artifact gate; status: **fixed** |
| Hard violation requires architectural change | Status: **needs_human** -- report to user with suggested fix |
| 3 iterations exhausted with remaining Hard violations | Status: **needs_human** -- report to user for guidance |

---

## Inputs

- Assembled HTML: `<project_path>/index.html`
- Content source: `<project_path>/content.html`
- Theme CSS: `<project_path>/template.css` (read-only reference)
- Design spec: `<project_path>/content_design_spec.md`
- Validation output from `validate_project.py`

## Outputs

- Fixed `content.html` (if issues found and correctable)
- Re-assembled root-level `index.html` (if fixes applied)
- Review status: pass / fixed / needs_human

Before reporting pass/fixed, run:

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --require-build --artifact-profile visual
```

When PPTX is requested, rebuild with `--all --include-pptx` and use the delivery artifact profile instead.

---

## Quick Review Profile

A quick or draft request may reduce deep inspection, but it never skips visual
review. Inspect the overview plus representative high-risk pages appropriate to
the deck, such as an opening page, a dense page, an image-led page, or a
chart/code/technical page. Do not impose a fixed sample count or invent a page
category that the deck does not contain.

The quick profile may be reported only as `draft` or `quick-review`; it cannot
produce a final `pass`. Final delivery still requires page-by-page browser PNG
inspection and the final artifact gate.

---

## Related

- `${SKILL_DIR}/references/checklist.md` -- P0/P1/P2/P3 graded quality issues
- `${SKILL_DIR}/references/components.md` -- CSS class catalog and component reference
- `${SKILL_DIR}/references/shared-standards.md` -- TCS rules and HTML/CSS constraints
- `${SKILL_DIR}/scripts/docs_html/browser_dom_export.md` -- Browser DOM export behavior and checks
