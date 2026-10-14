# Content Density & Visual Quality Rules

Rules for ensuring every content slide has sufficient visual richness. These apply regardless of template or brand.

---

## 1. Minimum Visual Structure

Every content slide (not title, section divider, quote, or end slides) must have **at least one** of:
- Structured layout (columns, cards, grid)
- Data visualization (chart, table, big numbers)
- Visual accent (colored panel from template layout, icon, accent bar)

A slide with only plain text on a white background is **unfinished**. Add structure before finalizing.

## 2. Visual Hierarchy (mandatory for rich slides)

Each content slide should create clear hierarchy through text sizing:

| Level | Purpose | Size range | Style |
|---|---|---|---|
| Heading / category label | Section within slide | 18-22pt | Bold, brand color |
| Body | Main content | 14-16pt | Regular, dark text |
| Secondary / caption | Supporting detail | 11-14pt | Regular, medium gray |
| Source line | Attribution | 9-10pt | Regular, light gray |

Use the template's `primary_color_hex` (from design profile) for heading accents. Use dark text color (typically `333333` or `575757`) for body — never pure black `000000`.

## 3. Content Area Fill

Content should fill **60%+ of the available content area** (the space between the title and footer). A slide that uses only the top third looks empty; one that fills edge-to-edge looks cramped.

Target zones:
- **Content start:** Below the action title (typically y ≈ 1.8-2.1")
- **Content end:** Above the source line (typically y ≈ 6.5-6.8")

## 4. Split-Panel Composition

For split-panel layouts (colored panel + content panel):

**Colored panel (accent side):**
- Big callout numbers (28-36pt bold, contrast color)
- Category labels or thematic text (20-24pt bold)
- Keep sparse — this panel is for emphasis, not detail

**Content panel (detail side):**
- Action title at the top (first `add_text`)
- Structured content: repeating header+body pairs
- Each header at 18-22pt bold, body at 14-16pt regular

## 5. Callout Numbers

For data-heavy slides, use 1-3 big callout numbers to anchor the message:
- Number: 28-36pt bold, brand color or white (depending on background)
- Label: 14-18pt regular, positioned directly below
- Place in colored panels, card headers, or a dedicated KPI row

## 6. Card / Block Patterns

When presenting 2-6 parallel items, use card patterns:
- Background rectangles to create visual separation
- Consistent card sizing across the row/grid
- Green/brand accent bar (thin line or border) at top of each card
- Content inset 0.1-0.15" from card edges

## 7. Bullet Limits

Maximum 6 bullets per slide. If you have more:
- Split into two slides
- Convert to a structured layout (columns, cards, table)
- Promote key items to headings with sub-bullets

## 8. Font Size Minimums

- **Body text:** 14pt minimum on full-width slides. Never go below 14pt for primary content.
- **Narrow boxes** (< 2" wide): 11pt acceptable. Use `autofit` as safety net.
  - Cards/columns < 3" wide: use 13pt body, 11pt caption.
  - Cards/columns < 2" wide: use 11pt body, 9pt caption.
  - Below 1.5" wide: reconsider the layout — switch to fewer, wider columns.
- **Labels / captions:** 9pt minimum.
- **If content doesn't fit at minimum sizes**, split into multiple slides — don't shrink fonts.

## 9. Icon Consistency

When using icons across a slide (icon grids, card headers, column layouts):
- Use the **same size** for all icons on one slide (e.g., all `0.75` or all `0.55`).
- Use the **same color** for all icons on one slide — either all white (on dark bg) or all brand color (on light bg). Don't mix.
- Align icons to the same y position across columns/cards.
- If one item has no natural icon match, either find a generic alternative or remove icons from all items — inconsistent icon presence is worse than no icons.

## 10. Alignment & Spacing

- Title labels and bullet content within cards should share the same x offset.
- Maintain at least 0.15" between title bottom and first content element.
- Content must never overlap with the action title area.
- Parallel items (columns, cards) should have identical y positions and heights.
- **Body text alignment:** Left-align body text. Center alignment only for titles, card labels, big callout numbers, and single-line captions. Never center multi-line body text or bullet lists.

## 11. Table Alignment

- **Header row:** Center-aligned text, bold, brand color or white on colored header bar.
- **Data cells:** Left-align text columns, right-align numeric columns.
- **Consistent column widths:** Size columns proportional to their content, but keep all rows the same height.
- Leave 0.5" clearance between table bottom and footer/source text.

## 12. Source Lines (every data slide)

Every slide containing numbers, percentages, or factual claims must end with:
- Source text at the bottom of the content area
- Font size: 9-10pt, light gray color
- Format: `Source: [Organization], [Publication], [Year]`
