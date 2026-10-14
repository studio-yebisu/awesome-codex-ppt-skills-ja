# Warm Editorial Style

Use this optional built-in style for mathematical exposition, research narratives, and talks that benefit from a quieter editorial character. It is not the default. Use the bundled restrained light style unless the user requests this style or asks for a warmer, more literary visual identity.

The reusable starter is [template-169.tex](template-169.tex), and the shared macros are in [theme.tex](theme.tex).

## Identity

Warm Editorial combines an ivory canvas, dark brown and charcoal typography, muted terracotta and sage accents, serif display titles, and sans-serif explanatory text. It should feel measured and academic rather than nostalgic or decorative.

## Canvas and Hierarchy

- Use a 16:9 canvas with a safe area of roughly `0.8–1.0 cm`.
- Reserve a stable title band ending near `1.3 cm` from the top edge.
- Use an editorial reading order: a clear title, one dominant object, and short interpretive text.
- Prefer open regions and fine rules over many filled cards. A box should communicate grouping, not merely occupy space.

## Palette

| Role | Default |
| --- | --- |
| Background | `#F7F2E8` |
| Main text | `#2F3437` |
| Display title | `#5C433B` |
| Primary accent | `#B66A50` |
| Secondary accent | `#7D9276` |
| Rules and borders | `#C9BBA8` |
| Pale surface | `#FFFDFC` |
| Muted text | `#77716B` |

Use terracotta for emphasis and sage for secondary structure. Do not use both as saturated fills across large areas.

## Typography

- Use a serif face for slide titles, short statements, and displayed quotations or propositions.
- Use a sans-serif face for body text, labels, legends, diagrams, and tables.
- Use a math font designed to accompany the serif display face. The bundled theme uses TeX Gyre Pagella Math; do not fall back to an unrelated default math family.
- Typical sizes: `16–19 pt` for slide titles, `8–10 pt` for section headings, `6.8–8.5 pt` for body text, and `5.8–7 pt` for labels.
- Keep body text at or above `6.5 pt`. Reflow or split content before reducing it further.
- Use italic serif text sparingly for definitions, interpretation, or a single highlighted claim.
- Set short slide prose and narrow text panels ragged-right. Do not fully justify them, and do not allow automatic hyphenation in headings.
- Use the shared body macros for explanatory prose. They cap interword stretch explicitly so narrow columns retain natural spacing; do not replace them with justified text or a bare alignment setting.
- Use `\WarmBodyText` for ordinary explanations and `\WarmBodySmall` only for compact readouts. Both define family, weight, size, leading, and ragged-right composition. Use `\WarmDisplayMath` for normal displayed formulas so color and scale remain consistent.
- Break long explanations into complete short paragraphs. Avoid a single avoidable word on the final line, and do not compensate with stretched interword spacing.
- If a key word still cannot fit without a forced split, rewrite the text or reallocate width before reducing the font.

## Containers and Spacing

- Prefer thin rules, aligned text blocks, and small accent marks to repeated filled cards.
- When a container is necessary, use the pale surface with a thin stone border and `0.18–0.30 cm` internal padding.
- Keep visible whitespace above and below rules. Titles, paragraphs, and formulas must never visually touch a separator.
- Use one shared vertical rhythm across peer blocks; asymmetry is acceptable only when it strengthens the reading order.
- On a title slide, keep the eyebrow and accent mark inside the safe area, but place the main title low enough to create visible space above the title block. Do not cluster the entire composition against the top edge.

## Diagrams and Data Graphics

- Use the shared [diagram guidance](../../references/diagram-design.md).
- Keep diagram labels sans-serif even when slide titles are serif.
- Use pale, large-radius subsystem containers; lightly bordered inner cards; and compact sans-serif role tags. Tags should use sand or a low-saturation accent rather than a strong fill.
- Use `warm/flow` for the primary path, `warm/return` for callbacks, and `warm/optional` for conditional paths. Use `warm/edge label` only on a short straight segment and `warm/adjacent label` for curved or descriptive paths.
- Use terracotta for the current or focal state, sage for alternatives or stable structure, and charcoal or muted gray for connectors.
- Show a current graph state with a soft fill, an outline, or a separated tag. Never place a terracotta dot directly on the node border.
- Prefer direct labels to boxed legends when the figure remains clear.

## Validation

Follow the shared [render and review loop](../../references/review-loop.md). The warmer palette and serif titles do not justify reduced contrast, decorative clutter, or smaller text.
