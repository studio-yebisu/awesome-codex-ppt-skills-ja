---
description: Select an HTML slide theme from the canonical catalog
---

# Select Theme Workflow

Select one registered HTML theme, copy its files into the project, and learn its API.

## Canonical Catalog

Read `${SKILL_DIR}/templates/index.json`. Treat its `themes` array as the only list of available themes; do not maintain a parallel theme table in workflow prose.

Each catalog entry provides an ID, directory, description, tags, `bestFor`, style, fonts, color variants, signature elements, and required files.

## Selection Process

1. If the user names a registered theme ID or an unambiguous theme name, use it.
2. Otherwise rank all catalog entries against:
   - requested visual direction;
   - content structure and density;
   - audience and presentation setting;
   - typography/language needs;
   - data, code, math, image, or narrative emphasis.
3. Prefer metadata evidence over a fixed topic-to-theme shortcut.
4. In normal mode, recommend up to three candidates with one-line rationales and wait for selection.
5. In unattended mode, choose the highest-ranked candidate. Do not fall back to a permanent default and do not choose randomly.

If the user requests a new theme, follow `${SKILL_DIR}/workflows/create-template.md` instead of inventing theme details in this workflow.

## Copy and Learn

Copy the selected theme:

```bash
cp ${SKILL_DIR}/templates/<theme>/index-template.html <project_path>/
cp ${SKILL_DIR}/templates/<theme>/template.css <project_path>/
```

Verify every file declared by the catalog entry exists. Then read:

1. `${SKILL_DIR}/templates/<theme>/theme.md` for CSS classes, components, color system, typography, and constraints.
2. `${SKILL_DIR}/templates/<theme>/demo.html` for working structures and composition examples.
3. `<project_path>/template.css` before authoring content.

Use theme files as the authority. Do not copy sample content or unrelated decoration from the demo. Some demos contain theme-authoring geometry; never copy a non-data inline style into standard-slide `content.html`. If a required reusable class is missing, add it to `template.css`.

## Continue to Content Design

1. Read `${SKILL_DIR}/references/strategist.md`.
2. Read `${SKILL_DIR}/references/shared-standards.md`.
3. Complete the nine design decisions.
4. Write `<project_path>/content_design_spec.md` with the selected catalog theme ID.
5. Continue with image acquisition and execution in `SKILL.md`.

## File Reference

| File | Purpose |
|---|---|
| `${SKILL_DIR}/templates/index.json` | Canonical theme catalog |
| `${SKILL_DIR}/templates/<theme>/theme.md` | Theme API and constraints |
| `${SKILL_DIR}/templates/<theme>/demo.html` | Working composition examples |
| `${SKILL_DIR}/templates/<theme>/template.css` | Theme styles and components |
| `${SKILL_DIR}/templates/<theme>/index-template.html` | Browser shell |
| `${SKILL_DIR}/workflows/create-template.md` | New-theme workflow |
