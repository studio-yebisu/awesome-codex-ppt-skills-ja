# PPTX Quality Gate

Run these checks before final delivery.

## Required Checks

- PowerPoint opens the `.pptx` without repair prompts.
- The deck exports to one PNG per slide.
- Slide count matches the intended count.
- Cover, TOC, navigation, body pages, results pages, and closing page match the template style.
- All active navigation labels use the template active style, usually red background and white text.
- TOC order matches the actual slide order and top navigation order.
- No stale template text remains, such as old project names, old dates, placeholder labels, TODOs, GitHub demo text, or example names.
- Text does not overflow or touch card borders in exported PNGs.
- Images preserve aspect ratio and are not clipped in a misleading way.
- Tables remain readable at presentation scale.
- Final deck is editable: text is text where possible, not a screenshot-only slide.
- Chinese fonts are available or embedded where the delivery environment requires them; otherwise template fonts such as Source Han Sans or Founder title fonts may fall back to SimSun.
- TOC, top navigation active state, and any static footer/page-number text agree with the final slide order.

## PowerPoint COM Checks

Use `TextFrame2.TextRange.BoundWidth` and `BoundHeight` against shape dimensions to find risky text boxes. Treat this as a warning signal, not an absolute truth, because mixed Chinese/English text may produce conservative width estimates.

Escalate a warning to a real issue when exported PNGs show:

- text crossing a card or slide boundary
- text clipped at the right/bottom edge
- text touching a red border
- overlapping navigation labels
- figures or captions covering each other

## Visual Review Order

1. Contact sheet for whole-deck rhythm and consistency.
2. Cover and TOC.
3. Dense body/card slides.
4. Figure-heavy slides.
5. Results tables and charts.
6. Summary and thanks slide.

## Fix Patterns

- Prefer shorter wording and manual line breaks over shrinking fonts.
- Preserve template font family and visual hierarchy.
- If a card body is crowded, split the sentence into shorter presentation phrases.
- If English identifiers cause overflow, add spaces around separators or break them across lines.
- If TOC/navigation order changes, update both together.
- If a figure is unreadable, crop less, enlarge it, or replace it with a simplified figure derived from the source.

## Iteration Discipline

- **Dump before you replace.** Real-world template strings differ from what they look like at a glance — `——` (U+2014 EM DASH) vs `—`, half/full-width quotes, trailing whitespace, or hidden run boundaries. Run `scripts/dump_pptx_content.py` first and copy the exact strings; do not retype from a screenshot.
- **Prefer `replace_partial_text` for body paragraphs.** Substring matching with a `min_len` guard recovers gracefully from minor template diffs. Reserve `replace_exact_text` for short, stable tags like navigation labels.
- **Verify with a second dump.** After every fill pass, re-dump the deck (or the affected slides via `--slide 4,8,9`) and diff against intent. Catching a missed replacement before exporting PNG saves a full PowerPoint round-trip.
- **Run overflow + scan together.** Stale text scan and overflow check probe orthogonal failure modes; running both after every iteration prevents shipping a deck that looks clean in one report and broken in the other.
