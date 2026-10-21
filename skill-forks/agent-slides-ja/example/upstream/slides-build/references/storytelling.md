# Storytelling Rules

Rules for structuring presentation narratives. Every rule here must influence a concrete generation decision — archetype choice, title wording, section structure, or slide count.

---

## 1. WWWH Framework (before any planning)

Answer these four questions before writing the storyline:

1. **Who** is your audience? Write the story they need to hear, not the one you want to tell.
2. **Why** are you telling this story? Define the objective: compel action, provoke reaction, or create common understanding.
3. **What** is the key message? Frame around the "so what". Include as little as necessary — be ruthless about cutting.
4. **How** can you communicate it? Choose archetypes and visual patterns that make the message stick.

## 2. Pyramid Principle (mandatory)

Structure every deck **top-down**: lead with the answer, then support it.

- **Deck level:** Executive summary states the conclusion. Each section is a supporting argument. Each slide within a section provides evidence.
- **Slide level:** The action title IS the answer. The body provides evidence.

### Mapping to archetypes

| Structural role | Typical archetypes |
|---|---|
| Conclusion / recommendation | `executive_summary`, `big_statement` |
| Section boundary | `section_divider` |
| Supporting argument | `content_bullets`, `two_column`, `three_column`, `four_column` |
| Evidence / data | `bar_chart`, `line_chart`, `pie_chart`, `table`, `matrix_2x2` |
| Process / sequence | `process_flow`, `icon_grid` |
| Framing / emphasis | `quote`, `big_statement` |
| Opening / closing | `title_slide`, `title_slide` (or dedicated end layout) |

Choose archetypes that match the structural role — don't pick a chart archetype for a qualitative argument or bullets for a data point.

## 3. SCQA Framework

Use Situation-Complication-Question-Answer to structure the opening:

1. **Situation** — shared context the audience already knows
2. **Complication** — what changed or went wrong
3. **Question** — the strategic question this raises
4. **Answer** — your recommendation

Map this to slides: the `executive_summary` action title states the Answer. If the deck warrants it, use 1-2 `content_bullets` or `big_statement` slides before the exec summary to set up Situation and Complication. For short decks (< 8 slides), fold SCQA into the exec summary body text.

## 4. Action Titles (mandatory)

Every content slide title must be an action title — a complete sentence stating the slide's key takeaway.

**Bad** (topic titles): "Market Overview", "Q3 Results", "Customer Segments"

**Good** (action titles): "The European market grew 12% YoY, driven by SMB", "Three segments represent 80% of margin; mid-market is underserved"

Rules the agent must enforce:
- Complete sentence: subject + verb + object
- States the "so what" — the conclusion, not the topic
- Maximum 2 lines (~120 characters). If longer, simplify or split into two slides.
- Reading only the titles of the deck must tell the full story.

Exceptions: `title_slide`, `section_divider`, and `quote` archetypes use descriptive or thematic titles, not action titles.

## 5. Body Proves Title (mandatory)

The content below each action title must contain evidence that makes the title undeniably true. If the body is too generic for the claim, either:
- Make the body more specific (add data, examples, mechanisms)
- Narrow the title to what the body actually proves

A slide where the body doesn't prove the title is misleading — fix the mismatch before generating ops.

## 6. One Message Per Slide

Each slide communicates **exactly one insight**. If the action title requires "and" to connect two unrelated points, split into two slides.

**Test:** Can you write a single action title that captures everything on this slide? If not, split it.

## 7. MECE Groupings

All groupings must be Mutually Exclusive and Collectively Exhaustive:
- Deck sections: no overlap, no gaps in the argument
- Chart categories: exhaustive breakdown
- Column content in multi-column layouts: parallel structure, no redundancy

## 8. The Isomorphism Principle (layout selection)

The visual structure must mirror the conceptual relationship. Pick archetypes and layouts by the relationship you're communicating, not by item count.

| If the evidence shows... | Use | Why |
|---|---|---|
| Equal pillars/themes | `three_column` / `four_column` | Equal columns = equal weight |
| Concepts to unpack | `icon_grid` | Icon + label + description = concept unpacking |
| Categories with structured details | Split-panel layout | Category + detail rows = taxonomy |
| Independent capabilities (no order) | `two_column` / grid pattern | Grid = no hierarchy implied |
| Ranked priorities (order matters) | `content_bullets` (vertical stack) | Top-to-bottom = importance order |
| Sequential phases (A feeds B feeds C) | `process_flow` / `timeline` | Left-to-right = temporal sequence |
| Contrasting approaches | `two_column` | Side-by-side = contrast |
| High-impact single message | `big_statement` | Full-slide emphasis = importance |

**Anti-patterns:**
- Equal columns for unequal items (size should reflect weight)
- Grids for hierarchies (use vertical stack instead)
- Flows/arrows for non-sequential items
- Vertical stacks for truly equal peers (use columns)

## 9. Key Message vs. Detail Slides

Determine the viewing mode before planning — it changes density, font sizes, and background treatment.

| Attribute | Key Message Slide | Detail Slide |
|-----------|------------------|--------------|
| **Purpose** | Projected — briefly glanced at | Printed or viewed on a device |
| **Text size** | Large (18pt body minimum) | Standard (14pt body minimum) |
| **Text density** | Minimal, plenty of whitespace | More detail allowed |
| **Approach** | Key ideas supporting speaking points | Comprehensive evidence and analysis |

Ask the audience context during planning (Step 1). If the deck is projected, default to Key Message style. If shared digitally, default to Detail style. A single deck can mix both — use Key Message for executive summary and recommendation slides, Detail for appendix and backup data.

## 10. Source Attribution

Every data point must have a source. Generate a source line for each slide that contains numbers or claims:
- Format: `Source: [Organization], [Publication], [Year]`
- Place as the last text element on the slide, small font (9-10pt)

If the user provides no source data, use `Source: Illustrative` or `Source: [To be confirmed]` — never omit.

## 11. Section Structure

Adapt section count and depth to the target slide count:

| Target slides | Recommended sections | Notes |
|---|---|---|
| 5-8 | 2-3 | Fold SCQA into exec summary. Minimal section dividers. |
| 9-15 | 3-4 | One section divider per argument. |
| 16-25 | 4-6 | Full SCQA opening. Section dividers + multiple evidence slides per section. |
| 26+ | 5-8 | Consider an appendix section for supporting detail. |

Always include: `title_slide` (first), `executive_summary` (early), at least one `section_divider` (for decks > 8 slides).

## 12. Archetype Variety

Avoid monotony — don't use the same archetype more than 3 times consecutively. Alternate between text-heavy (bullets, columns) and visual (charts, process flows, icon grids) archetypes. For decks > 10 slides, use at least 4 distinct archetypes.

## 13. Layout Variety

In any deck > 6 slides, use at least 2-3 different template layouts. Never repeat the same layout for 3+ consecutive content slides. Use split-panel and accent layouts for visual punctuation between standard white slides.

## 14. Sanity Check (before finalizing)

Before generating ops, verify the plan against these questions:

- Does each slide have only one message?
- Can you read only the titles and understand the full story?
- Does every body prove its title?
- Are all groupings MECE?
- Does the layout match the conceptual relationship (isomorphism)?
- Are sources present for every data claim?
- Does every element pass the **remove-it test**? (Would removing it reduce comprehension? If not, cut it.)
