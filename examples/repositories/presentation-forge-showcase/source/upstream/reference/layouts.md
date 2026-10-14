# Layouts: choosing a shape for each slide

A deck is a first draft of **the user's** talk, built from **their** brief. Its
structure comes from what they want to say - never from an example deck, and
never from a fixed sequence of slide types. This file is a menu: for each slide,
pick the shape that best carries its one idea.

## What is fixed, and what is not

- **Fixed:** a title slide first, and a closing slide last (the takeaway and the
  next step, or the contact/thanks the user asked for).
- **Everything else is a choice made from the content.** In particular:
  - an **agenda** only for a deck long enough to need a map (roughly 12+ slides);
  - **section dividers** only when the talk really has 2-4 parts;
  - a **quote** slide only when the user gave a real quote, or one with a source
    that genuinely makes the point - never an invented "inspirational" line;
  - a **footer** only when it helps (a confidential mark, the event name, a
    brand); not by default;
  - no "Thank you / Questions?" slide unless the user wants one.
- Match the user's request on length: a 5-minute talk is about 5-7 slides.

## The menu

Each shape: what it is for, and the markup it starts from. Components are
detailed in [`components.md`](components.md), motion in [`motion.md`](motion.md).

| Shape | Use it when… | Built from |
| :-- | :-- | :-- |
| **Title** | always, first | `slide--title`: `.eyebrow`, `.display`, `.lead` |
| **Big statement** | one sentence must land on its own | `.display` or `.title` alone, maybe a `.lead` |
| **Assertion + bullets** | 3-5 supporting points | `.title` + `ul.bullets` |
| **Key figure(s)** | a number is the point | `.title` + `.stats` (one `stat--hero` for a single figure) |
| **Chart** | comparing amounts or a trend | `.title` + `.bars` (or `--vertical`), `.ring` for one share |
| **Before / after**, **pros / cons** | two sides of something | `.two-col` with a `.card` per side |
| **Comparison** | options against criteria | `.title` + `table.compare` |
| **Process** | steps in order, a pipeline, a method | `.title` + `ol.steps` |
| **Timeline** | dates, history, a roadmap | `.title` + `ol.timeline` |
| **Feature grid** | 3-6 parallel things (offers, team, benefits) | `.title` + `.grid` of `.card`s with icon tiles |
| **Image + text** | a screenshot, photo or diagram is the evidence | `.two-col`: `<img src="assets/…">` + short text |
| **Code** | showing real code | `.title` + `pre > code` with `.line` spans |
| **Quote** | a real quote with its source | `blockquote` + attribution |
| **Section divider** | entering one of 2-4 parts | `slide--section`: `.eyebrow`, `.display`, `.lead` |
| **Closing** | always, last | `slide--conclude`: the takeaway + the next step |

## Variety without noise

- Let the content decide: a number → a figure slide; a sequence → steps or a
  timeline; a choice → a comparison. Don't force bullets onto everything.
- Avoid three slides in a row with the same shape, unless they are a deliberate
  series.
- Keep one idea per slide. If a shape gets crowded (more items than the limits in
  `components.md`), split the slide rather than shrinking the text.
