# Artifact Ownership and Visual Correction

Use this reference when a build or visual review finds a problem. It keeps one source of authority per fact and prevents a derived artifact from becoming an accidental editing target.

## Artifact Authority

| Artifact | Authority / Owner | Derived? | Correction or Rebuild |
|---|---|---:|---|
| `sources/` originals and direct user Markdown | Source owner | No | Correct or replace only with user/source authority |
| `*.md.receipt.json` | Source converter | Yes | Rerun the owning converter; never edit a pass receipt by hand |
| `content_design_spec.md` | Strategist | No | Update when the underlying claims, narrative, theme, or visual direction deliberately changes |
| `content.html` | Content executor | No | Correct slide claims, hierarchy, notes, and semantic structure |
| `template.css` | Theme owner | No | Correct reusable layout, tokens, components, and theme-wide visual defects |
| `index-template.html` | Runtime/shell owner | No | Correct navigation, dependency loading, and settled-render hooks |
| root `index.html` | Assembler | Yes | Rebuild; never make a durable fix here |
| `output/dom-audit.json` | Browser audit | Yes | Fix its owning source, then rebuild |
| `output/render-fidelity.json` | Export comparison | Yes | Diagnose the conversion route; do not distort a correct browser layout to silence it |
| SVG, PNG, overview, PDF, PPTX, compile manifest | Compiler/export owner | Yes | Rebuild from current source; never patch delivery output as the source fix |

## Issue Ownership

Assign the narrowest owner supported by evidence:

1. A wrong or excessive claim, missing note, or one-off semantic structure belongs to `content.html`.
2. Repeated spacing, component geometry, theme typography, or reusable layout failure belongs to `template.css` and its theme documentation.
3. Missing or unsettled math, code, charts, fonts, navigation, or overview behavior belongs to `index-template.html` or the common runtime.
4. A browser-correct page that changes only in the SVG/PPTX route belongs to the exporter. Keep the browser source intact while diagnosing conversion fidelity.
5. A source mismatch, unsupported conversion, or stale conversion receipt returns to the source converter or Strategist; do not rewrite the slide to conceal it.

`data-audit-owner` may mark a meaningful DOM region when the generic browser audit would otherwise report many descendants. It groups evidence only; it does not override the ownership rules above.

## Correction Ladder

Apply the first step that preserves the intended claim and theme:

1. Remove accidental duplication or tighten nonessential copy.
2. Recompose with existing semantic theme classes.
3. Add or correct a reusable project/theme component.
4. Correct runtime settlement or an export conversion defect at its owner.
5. Return upstream when the source, claim, theme, or visual direction must change.

After any source correction, rerun the source gate, `html_compiler.py --all`, browser-first visual review, and the final visual gate. When PPTX is required, use the same-build `--all --include-pptx` delivery gate.
