---
description: Create and validate a new HTML slide theme from an existing SeaSlides theme contract
---

# Create a New HTML Slide Theme

Use this workflow only when the user requests a new theme or the catalog cannot meet a material design requirement. Theme creation follows the same TCS and rendering gates as a normal deck.

## 1. Confirm the Design Brief

Confirm or infer only what is needed:

- lowercase hyphenated theme ID and display name;
- intended audience, use cases, and visual character;
- palette and typography direction;
- required slide modes, layouts, components, and data visuals;
- the closest existing base theme from `${SKILL_DIR}/templates/index.json`.

If an existing catalog theme already meets the brief with token overrides or a small reusable class addition, customize it in the project instead of creating a new catalog entry.

## 2. Create a Project-Local Working Theme

Start from the closest registered theme. Copy its `template.css`,
`index-template.html`, `demo.html`, and `theme.md` into a project-local theme
working directory, retaining `demo.html` as the theme-demo entry. Do not edit
the catalog copy in place. If the work instead targets an ordinary presentation
project, keep that project's separate `content.html` and copy only the theme
shell/styles it needs.

When no project exists:

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py init <theme-id> --dir projects
```

Read `${SKILL_DIR}/references/template-designer.md`, the selected base theme's `theme.md`, and its rendered demo before editing.

## 3. Author the Theme Contract

Produce these project files:

| File | Required contents |
|---|---|
| `theme_design_spec.md` | Follow `${SKILL_DIR}/templates/theme_design_spec_reference.md`: design intent, palette, typography, modes, layout vocabulary, components, and asset plan |
| `template.css` | Theme tokens and reusable visual/layout/component classes |
| `index-template.html` | Browser shell and dependencies; no slide content |
| `demo.html` | Demo slides covering the APIs that the theme actually exposes |
| `theme.md` | Follow `${SKILL_DIR}/templates/theme_reference.md`, grounded in the selected base theme's actual API |

Follow the standard-slide TCS contract in `${SKILL_DIR}/references/shared-standards.md`. Demo content should prove the theme's intended range without filling numeric component, decoration, or layout quotas. A strong theme has a coherent visual world, readable hierarchy, stable browser rendering, and components that solve real content structures.

## 4. Assemble, Validate, and Review

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --entry demo.html --source-only --profile theme-demo
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all --entry demo.html
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --entry demo.html --require-build --profile theme-demo --artifact-profile visual
```

Review `output/overview.png` and representative `output/browser_pngs/` first; browser PNGs and `dom-audit.json` are the layout truth. Use SVG-route PNGs and `render-fidelity.json` only to diagnose conversion differences. Fix all compile, missing-reference, overflow, clipping, TCS, DOM-blocker, and legibility failures. When PPTX is requested, build it in the same sequence with `html_compiler.py <project_path> --all --include-pptx --entry demo.html`, then run the delivery artifact profile with `--entry demo.html --profile theme-demo`. Check that:

- every documented class exists and every demo class is documented;
- all declared CSS custom properties resolve;
- light, dark, hero, content, and ending behavior is coherent when those modes are supported;
- data visuals use the canonical inline data-geometry allowlist;
- the design remains identifiable without relying on irrelevant sample content;
- `index.html`, SVGs, both PNG routes, overview, DOM audit, fidelity report, and compile manifest are current; `output/slides.pptx` is present when requested.

Use `${SKILL_DIR}/workflows/visual-review.md` for the final visual pass.

## 5. Keep Local or Register Explicitly

Keep the theme project-local by default. Only modify the shared catalog when the user explicitly asks to install the theme for reuse.

For a catalog installation, create `${SKILL_DIR}/templates/<theme-id>/` containing:

- `template.css`;
- `index-template.html`;
- `demo.html` (the validated project `content.html`);
- `theme.md`;
- any referenced local assets.

Then add one complete entry to `${SKILL_DIR}/templates/index.json`. The directory and catalog entry must agree on ID, filenames, description, tags, best-use cases, fonts, palettes, and signature features. Re-run assembly and validation from a clean project created from the registered theme.

## 6. Report Completion

Report the theme ID, project path, whether it was catalog-installed, files produced, validation result, and any intentionally unsupported modes or components. Do not claim catalog availability when the theme remains project-local.
