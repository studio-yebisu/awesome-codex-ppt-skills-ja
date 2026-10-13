# Navigation and the questions — building a deck you can PRESENT FROM

**Read this when the deck will be presented live and the room can interrupt** — a defense, a
guidance or thesis committee, a conference talk, a board or steering readout, a training session,
any deck with an appendix. Skip it for a deck that will only be read.

A finished deck is a linear file. A *presented* deck is a thing somebody navigates under pressure,
in front of people, while being asked about slide 14. Those are different artifacts, and until the
components below existed this library could only build the first one.

**Measured before this page was written:** `grep -rn "hlinkClick" scripts/` found the string in
exactly one place — `_EA_FOLLOWERS`, a constant listing which elements follow the East-Asian font
slot — and `click_action` appeared in no file at all. The
library had no way to make a deck jump. Every "backup slide" it had ever built was reachable only by
arrowing past everything in between — which is the reason prepared answers go unused.

---

## 1. The three components

Look them up the usual way — `python3 scripts/sigs.py link agenda back_link`, or
`--example agenda` for a runnable call. The short version:

```python
dk.link(shape, target_slide)          # a shape JUMPS to another slide
dk.link(shape_or_run, "https://…")    # a shape or a text RUN opens a URL
dk.agenda(slide, x, y, w, items, active=1, targets=[…])   # contents page / section progress
dk.back_link(slide, home, label="Back to agenda")         # the other half of a jump
```

**`link`** writes a real PowerPoint slide action, so the jump works in Keynote and Google Slides
too, and it survives save/reopen (pinned in `tests/test_qa_backup.py` against the *reopened* file,
never the in-memory object).

🔴 **The URL is scheme-guarded — `http:` · `https:` · `mailto:` · `doi:` and nothing else.** A link
target routinely arrives from the material a deck was built from, and that material is untrusted
input. `javascript:` / `file:` / `data:` in a delivered deck is someone else's machine, not a
citation.

🔴 **A slide jump must hang off a SHAPE.** PowerPoint has no run-level jump. Asking a text run for
one raises, naming the shape to pass instead, because the alternative — doing nothing quietly — is
how a contents page that clicks nowhere gets shipped.

**`agenda`** is the deck's map: numbered rows, one optionally accented, so the same helper is both
the contents page and the section-progress page a long deck repeats between parts. Pass `targets`
and it becomes a live jump table. A target list that does not match the item list is **refused** —
a half-wired agenda's dead row is exactly the one you will click in front of the room.

**`back_link`** is the return chip. Its width is **measured from the label, never assumed**, and the
measurement is script-aware: a CJK glyph is full-width (1em), so `返回目录` is credited at its real
width instead of being priced like the four Latin letters of `Back`. A label too long for its chip
is refused with both numbers rather than clamped, because the caption is set unwrapped and a clamped
chip runs its text off the slide. (Both defects were real, and both were found by rendering the chip
rather than by reading the code: the first draft used a fixed 1.25in pill and `Back to agenda`
wrapped straight through the chip's own bottom edge.)

## 2. Where jumps belong

- **A contents page you present from.** `agenda(..., targets=[...])` on the opening map, repeated
  with a different `active` between parts.
- **Backup slides after the close.** The Q&A slides, parked past the closing slide so they never
  appear in the linear run, each reachable from the slide whose question they answer.
- **A detail slide behind a headline.** The methods table, the full cohort, the sensitivity
  analysis — linked from a chip on the slide that states the result, so the deck stays a visual aid
  and the detail is one click away rather than deleted or crammed in.
- **A source that can be opened.** `dk.link(run, "https://doi.org/…")` on a citation run, next to
  `source_note` / `sources_page`.

Every slide you can jump TO needs a way back. That is what `back_link` is for, and the gate reports
a backup slide that links nowhere.

## 3. The Q&A backup gate

Record the questions you expect from THIS room, each with the slide that answers it:

```jsonc
"content": {
  "qa": [
    {"question": "Why not compressed sensing as the baseline?", "slide": 14},
    {"question": "What is the failure mode at 12x?",            "slide": 15}
  ]
}
```

`scripts/check_qa_backup.py` runs on **both** gate paths (`render_deck.py --gate-check` and
`codex_delivery_gate.py`) and checks the BUILT file:

| finding | severity | what it means |
|---|---|---|
| `PREPARED BUT UNREACHABLE` | block | the slide exists and nothing links to it — during questions it can only be reached by arrowing |
| `NO SLIDE` | block | the recorded slide number is outside the deck (usually an appendix that was cut) |
| `NO QUESTION` | block | a slide recorded without the question it answers — the question is the part that gets rehearsed |
| `MALFORMED` | block | the entry is not `{"question": …, "slide": …}` |
| `NO WAY BACK` | note | reachable, but links nowhere: after the answer, the room watches you arrow backwards |

**Nothing recorded is NOT CHECKED, out loud.** Anticipating questions is a practice, not a law, and
a gate that demanded it of every deck would only teach authors to record `[]` to clear a red light.
An explicitly empty list reads the same way, so the scaffold's own `"qa": []` never reports as
checked-and-clean.

Waive in writing when the answer genuinely lives elsewhere — a separate appendix deck, a handout:
`{"qa_backup": {"waived": "<why>"}}`. Like every other floor here, the waiver is recorded **beside**
the finding, never instead of it.

## 4. Writing the questions

The questions are worth as much as the slides. Two rules that keep them honest:

- **Write down what the room will actually ask, not what is easy to answer.** The committee
  question you are dreading is the one that needs the backup slide; the one you would enjoy does
  not need a slide at all.
- 🔴 **A backup slide is bound by every rule the deck is.** It is built from the same material, held
  to the same never-invent floor, and linted like any other page. A backup slide answering a number
  the source never stated is a fabricated claim that happens to be parked at the end.

An audience brief (`content.audience_brief` — *what this room has to decide*) is where the
questions come from: each decision the audience faces has a question attached to it, and the ones
your deck does not already answer on a slide are the ones that need a backup.
