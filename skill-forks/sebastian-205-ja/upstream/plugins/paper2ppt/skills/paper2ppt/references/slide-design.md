# Adaptive slide design

Use a neutral, cross-disciplinary visual system. Let evidence determine geometry; do not force evidence into a branded template.

## Set the frame

- Use a stable 16:9 canvas and fixed slide coordinates so content cannot shift with labels or dynamic text.
- Build a clear hierarchy: conclusion-style title, evidence, interpretation, then source. Keep one main claim per slide.
- Use type that remains readable from the back of a room. Start near 28-32 pt for titles, 18-24 pt for body text, and 12-14 pt for captions and sources; enlarge when density permits.
- Use installed font fallbacks rather than file paths. Prefer `Arial` or `Noto Sans` for English and `Noto Sans CJK SC`, `Source Han Sans SC`, `Microsoft YaHei`, or `PingFang SC` for Simplified Chinese.
- Keep letter spacing at zero; never use negative letter spacing or viewport-based font scaling.
- Put explanatory depth in speaker notes instead of shrinking on-slide text.

## Choose geometry from evidence

Make result slides figure-led. Use the figure's aspect ratio, density, and argumentative role to choose a layout:

| Evidence shape or role | Preferred geometry |
| --- | --- |
| Wide plot, image strip, or central result | Near-full-width evidence below the title |
| Figure plus short interpretation | 70/30 or 65/35 asymmetric split |
| Wide evidence plus qualifiers or sub-result | Top/bottom stack |
| One number, definition, or limitation | Compact callout beside the primary evidence |
| Direct comparison | Aligned columns with shared scales and explicit labels |

Treat rigid `50/50` symmetry as the exception, not the default. Do not add empty symmetry padding merely to balance a slide.

For dense multi-panel figures:

1. Crop to the panels that support the slide claim.
2. Split panels across slides when projection readability would otherwise fail.
3. Promote a decisive panel to its own slide when it carries the argument.
4. Preserve axes, scales, labels, legends, colorbars, statistics, and qualifiers.
5. Never distort an image to fill a box; preserve its aspect ratio.

Attach a concise caption and source to the evidence. Record detailed interpretation, caveats, and transitions in notes.

## Use accessible visual encoding

- Maintain strong text/background contrast and verify small labels after rendering.
- Use color to group or emphasize, not to decorate every object.
- Never encode a distinction with red/green alone; add shape, line style, pattern, or direct labels.
- Reuse paper colors when they carry meaning, but explain them and preserve the original legend.
- Avoid decorative stock images, gradients, fake cards, dashboard styling, and ornamental containers.
- Never present AI-generated imagery as experimental data or as a substitute for a paper figure.

## Select an archetype

- **Cover:** title, authors, venue/year, presenter, and minimal identifying context.
- **Background/problem:** one motivating fact or diagram plus the unresolved question.
- **Workflow/method:** ordered stages, inputs/outputs, cohorts, or experimental groups with readable labels.
- **Result/evidence:** conclusion-style title, dominant evidence, short interpretation, source, and notes.
- **Comparison/table:** aligned measures, shared units, highlighted decision criterion, and restrained emphasis.
- **Model/synthesis:** only source-supported components and relationships; label any reconstruction.
- **Limitations/discussion:** explicit evidence boundary, uncertainty, alternatives, and practical implication.

## Render and revise

Render every slide when a renderer exists, then inspect individual pages and a contact sheet. Revise any slide with overlap, clipping, overflow, missing glyphs, low contrast, unreadable labels, excessive density, image distortion, weak hierarchy, or an ambiguous source. Re-render the affected slides, then run the full visual pass again.
