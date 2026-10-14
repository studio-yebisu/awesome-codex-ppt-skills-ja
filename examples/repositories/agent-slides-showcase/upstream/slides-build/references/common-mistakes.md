# Common Mistakes

The most frequent errors in generated decks, ranked by impact. Check these during plan review and QA.

---

## Critical (Destroys the message)

1. **Topic titles instead of action titles** — "Market Overview" tells the reader nothing. Every content slide must have a complete sentence stating the "so what." This is the #1 quality signal.

2. **Too much text on one slide** — If you can't see the "so what" in 5 seconds, there's too much content. Split into multiple slides. One message per slide, always.

3. **Body doesn't prove the title** — The content below each action title must contain evidence that makes the title undeniably true. Generic body + ambitious title = misleading slide.

4. **Missing source lines** — Every data point needs a source. Unsourced numbers destroy credibility. Use `Source: Illustrative` when no real source is available.

5. **Layout doesn't match the relationship (isomorphism violation)** — Equal columns for unequal items, grids for hierarchies, flows for non-sequential content. The visual structure must mirror the conceptual relationship.

## Visual Quality (Looks unprofessional)

6. **No visual hierarchy** — Title must visually dominate (largest, brand color), then headings (bold), then body (regular). Without size and color contrast, everything looks flat.

7. **Slides without visual structure** — Every content slide needs at least one visual element: chart, table, structured layout, or colored accent. Text-only slides are forgettable.

8. **Bullet-heavy slides** — Replace long bullet lists with structured layouts: columns, cards, icon rows, tables. Maximum 6 bullets per slide.

9. **Ignoring template colors** — Use the extracted palette from the design profile and color zones. Don't introduce arbitrary colors that clash with the template's visual identity.

10. **Pure black text** — Most professional templates use dark gray (e.g., `333333`, `575757`) for body text, not `000000`. Check the template's extracted text colors.

## Layout & Structure (Breaks the flow)

11. **Repeating the same layout 3+ times** — Vary layouts across consecutive slides. Alternate between white slides and split-panel/accent layouts.

12. **Cramming content** — Leave breathing room. White space is a design feature. Maintain consistent margins and spacing from the template's content box.

13. **Content overlapping the title** — Content must start below the title area. Never place shapes or text in the title zone (typically y < 1.8").

14. **Wrong archetype for the content** — Using `content_bullets` for data that needs a chart, or `bar_chart` for qualitative arguments. Match archetype to content type.

15. **Missing section dividers** — For decks > 8 slides, section dividers are essential navigation aids. Don't jump between topics without them.

## Content Quality (Weakens the argument)

16. **Vague body content** — "Improve efficiency" tells nobody anything. Name the specific mechanism: "Consolidate 4 regional warehouses into 2 hubs, reducing shipping costs by 18%."

17. **Non-MECE groupings** — Overlapping categories in columns, charts, or sections. Each group must be mutually exclusive and collectively exhaustive.

18. **Inconsistent parallel structure** — Items in columns, cards, or bullet lists should follow the same grammatical pattern. If one starts with a verb, all should.

19. **Missing opening/closing structure** — Every deck needs a title slide and a clear ending. Decks > 10 slides need an executive summary early.

20. **Orphan slides** — A single slide in a "section" of one. Either combine with an adjacent section or add supporting slides.

## Formatting Details

21. **Inconsistent font sizes** — Pick size constants at planning time and reuse them throughout. Body text should be the same size on every content slide.

22. **Centered body text** — Body text should be left-aligned. Center alignment only for titles, card labels, and big callout numbers.

23. **Too many font sizes** — Use at most 4 distinct sizes in a deck: title, heading, body, caption. More than that creates visual noise.

24. **Charts without insight callout** — Every chart needs a highlighted data point or callout that carries the argument. A chart without emphasis is just data, not evidence.

25. **Ignoring the template's content box** — Place content within the extracted `content_box` boundaries. Content outside these bounds may overlap with template decorations (logos, page numbers, borders).

## Production Quality

26. **Visual effects and animations** — Never add shadows, reflections, glow, 3D effects, or animations/transitions. These are distracting in professional settings and break cross-platform rendering. Clean, flat design only.

27. **Failing the remove-it test** — Every element on a slide should earn its place. If removing an element wouldn't reduce comprehension, cut it. Extra logos, decorative shapes, redundant labels, and "nice-to-have" text boxes all add noise.

---

## Pre-Generation Checklist

Before generating ops for each slide, verify:

- [ ] Action title is a complete sentence stating the "so what"
- [ ] Body content will prove the title claim with evidence
- [ ] Archetype matches the content type (isomorphism)
- [ ] Layout differs from the previous 2 slides
- [ ] Content uses at least one visual element beyond plain text
- [ ] Font sizes follow the deck's size constants
- [ ] Source line present for any data claims
- [ ] No more than 6 bullets
- [ ] Content fits within the template's content box
- [ ] No visual effects (shadows, reflections, glow, 3D, animations)
- [ ] Every element passes the remove-it test (would removing it reduce comprehension?)
