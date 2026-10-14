# Writing a great deck (and its speaker notes)

This guide is about the *content*: how to write a presentation and its text well
from the start, and what to put in the speaker notes. Read it whenever you author
a deck (Workflow 1). The mechanics (classes, build, theming) live in `SKILL.md`
and `template/docs/writing-slides.md`; this file is about quality.

The golden rule: **the slide is what the audience SEES; the notes are what the
speaker SAYS.** They are different texts with different jobs. Write both.

## 1. Decide the spine before writing any slide

Get these straight first, then everything else follows:

- **One core message.** If the audience remembers a single sentence, what is it?
  Write it down. Every slide must earn its place against it.
- **The audience.** Their level, what they already know, what they care about.
  This sets vocabulary, depth, and which arguments land.
- **The arc.** A talk is a story, not a list. Build it from what the user wants
  to say, in their order of ideas; a common shape is a title that frames the
  topic and promise, why it matters now, a body that builds point by point, and
  a close that states the takeaway and the next step. Adapt it - it is not a
  template to fill.
- **The takeaway per part.** One sentence each. When the talk has 2-4 real
  parts, `slide--section` dividers can mark them; a short talk usually needs
  none.

Plan this arc explicitly before writing slides. A deck written outline-first reads
as a coherent argument; a deck written slide-by-slide reads as disconnected notes.

## 2. One idea per slide (assertion-evidence)

The strongest, best-researched slide structure is **assertion-evidence**:

- **Title = the assertion.** Make the slide title a full, specific sentence that
  states the point, not a topic label. "Caching cut p99 latency by 40%", not
  "Performance". The audience should grasp the point from the title alone.
- **Body = the evidence.** Support that one assertion with the lightest thing that
  proves it: a few bullets, a two-column contrast, a chart or image, a short code
  block, a quote. Everything on the slide answers the title and nothing else.
- **One idea per slide.** If a slide carries two ideas, split it. Decks with one
  idea per slide are understood and remembered better.

## 3. Write the on-slide text tight

The slide supports the speaker; it is not the script. So:

- **Few words.** Short phrases, not sentences, in bullets. If a bullet wraps past
  two lines, cut it. Aim for a handful of bullets, not a paragraph.
- **Parallel and concrete.** Start bullets the same grammatical way; prefer
  concrete nouns and active verbs over vague abstractions.
- **No wall of text.** If you are tempted to write full prose on a slide, that
  prose belongs in the notes. The slide keeps the headline and the evidence.
- **Consistent terms.** Use the same word for the same thing throughout; don't
  swap synonyms that make the audience wonder if you mean something new.
- **Match the language** to the audience (and the deck's `lang`). Write real
  content from the brief; if you must invent specifics to fill a thin brief, keep
  them plausible and flag them so the user can correct them.

## 4. Speaker notes: what to put in `<aside class="notes">`

Notes are the spoken track, visible only in presenter mode. Good notes make a
talk sound natural and keep the speaker on time. Put them on (almost) every
content slide.

**Include:**

- **The narration** - what the speaker actually says to make the slide's point:
  the explanation, the example, the "why it matters". This is the prose that did
  NOT go on the slide.
- **1-2 key points per slide**, as short phrases or keywords, not a wall of text.
  Notes are scannable cues, not a word-for-word essay.
- **A transition cue** to the next slide ("then move to the cost trade-off...") so
  the talk flows instead of lurching slide to slide.
- **Delivery cues** where useful: "PAUSE here", "ask the room who has hit this",
  "click to reveal the second point", "slow down".
- **Things easy to forget**: exact figures, a name, a source, the precise wording
  of a definition or quote, the answer to a question you expect.

**Avoid:**

- **Copying the slide text** into the notes - that is redundant. Notes add what is
  NOT shown.
- **A full word-for-word script** you will read in a monotone. Write cues you can
  speak from, not a transcript. (For purely virtual talks you can keep fuller
  notes, but still structured and scannable.)
- **Cramming** - more than ~2 ideas of notes per slide usually means the slide
  should be split.

**Format:** short bulleted phrases in a conversational tone, easy to glance at and
keep talking. In this engine:

```html
<aside class="notes">
  <p>Hook: most teams over-index on throughput and ignore tail latency.</p>
  <ul>
    <li>Give the concrete number: p99 was 800ms before caching.</li>
    <li>PAUSE - let the 40% land.</li>
    <li>Transition: "but caching is not free" -> next slide on cost.</li>
  </ul>
</aside>
```

## 5. Map it onto the engine

- assertion -> `h1`/`.title` (or `.display` on the title slide)
- evidence -> the shape that fits it, from [`layouts.md`](layouts.md): `.bullets`,
  a figure (`.stats`), a chart (`.bars`, `.ring`), a process (`.steps`), a
  `.timeline`, a `table.compare`, a `.grid` of cards, `.two-col`, `blockquote`,
  `pre > code`, an `<img>` from `assets/` - see [`components.md`](components.md)
- section breaks -> a `slide--section` divider with the part's one-sentence
  takeaway, when the talk has real parts
- build-up -> `class="fragment"` to reveal points one at a time when the order of
  reveal carries meaning (a list of arguments, a before/after, a punchline)
- motion -> what the chosen level calls for, from [`motion.md`](motion.md)
- the spoken track -> `<aside class="notes">`

## 6. Self-check before you finish

- Does each slide's title state a point you could agree or disagree with?
- Could a stranger get each slide's message from the title plus a 3-second glance?
- Is there any slide with two ideas? Split it.
- Is any slide a wall of text? Move the prose to the notes.
- Do the slide titles, read in order, tell the whole story on their own?
- Does every content slide have notes that say something the slide does not show?
- Does the close state the single takeaway and a clear next step?
