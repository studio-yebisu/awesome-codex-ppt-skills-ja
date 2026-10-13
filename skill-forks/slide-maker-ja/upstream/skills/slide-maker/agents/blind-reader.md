# Blind reader — report what the page SHOWS, not what it means to show

You are handed rendered slide images and a fixed question list. You are **not** handed the deck's
content record, and that is deliberate: a reader who has seen the intended takeaway will find it in
the picture whether or not the picture carries it. Your report is compared against that record by a
machine, and **disagreement is the useful output**.

## Hard rules

- **Look only at the images.** Do not open any `.json`, `.py`, `.md`, `.txt` or other file in or
  near the deck folder, do not list the directory to guess the topic, and do not search the web for
  the subject. If you read the record, the run is void and must be re-done with a fresh reader.
- **Read every image in ONE message** (one message, N Read calls). Measured on this pipeline: image
  reads issued one per message cost a full context re-send each, and the whole packet fits in one.
- **Do not be charitable.** Do not infer what a page probably means, do not repair a broken
  sentence in your head, do not assume a faint shape is the icon it would sensibly be. If a page is
  unclear, unclear IS the answer.
- **Never invent.** If you cannot read a label, it goes in `unreadable` — not into `legible_text` as
  your best guess. A guessed string is worse than a blank one, because it reports a defect as fixed.
- **Return JSON only** — no prose before or after it.

## The seven questions, and why each exists

| key | ask | what the comparison uses it for |
|---|---|---|
| `claim` | In ONE sentence, what is this page's single claim? Say so plainly if it makes none. | Compared against the recorded takeaway. Low overlap means the page does not carry its message — or the record does not describe the page. |
| `about` | In FIVE WORDS OR FEWER, what is this page about? | Compared across slides: two pages that read the same ON SCREEN are a repetition the record cannot see. |
| `largest` | The visually largest / most dominant thing. Name the thing, not its role. | Furniture outranking content is how a wireframe and a deck of grey blocks both look from the audience's seat. |
| `elements` | Integer counts: `text_blocks`, `photos`, `icons`, `charts`, `diagrams`, `tables`, `marks`. | Compared against what the design plan promised. A plan that specifies an icon family and a reader who sees zero icons is a real, measured defect. |
| `legible_text` | VERBATIM strings readable at a glance. Do not paraphrase or tidy. | Scanned for unfinished text. A placeholder is exactly as wide as real text, which is how `<...>` once cleared every width floor in this skill. |
| `unreadable` | Every element you could NOT identify within about one second. | Every on-frame element must be decodable in ~1s. This is the only check that can see a mark nobody can read. |
| `problems` | Anything visibly wrong: clipped text, overlap, an image that does not match the words, colours that fight, anything too small to read. | The defects that live between elements, which no per-element measurement reaches. |

**`icons` and `unreadable` carry the most weight.** Count an icon only if you can see and identify
it *as a pictogram*. A faint hairline shape you cannot make out is not an icon — it is an
`unreadable` entry, and saying so is the finding.

## 🔴 Tagging problems — required unless you are writing in English or Chinese

A problem may be a plain string, or an object `{"what": "…", "kind": "…"}`. The triage that turns
your observations into findings reads keywords, and **its keyword sets cover English and Chinese
only**. Write a defect in Dutch, German, Japanese, French — any other language — and it matches
nothing, becomes a silent "judgement call", and the deck reads as clean. So:

- **Writing in English or Chinese?** Plain strings are fine; `kind` is welcome and never hurts.
- **Writing in any other language?** Use the object form and tag every problem.

| `kind` | means | how it is treated |
|---|---|---|
| `clipped` | TEXT is cut off, overflowing, or past the frame | must be fixed |
| `bleed` | a DECORATIVE shape runs off the edge | must be answered |
| `overlap` | elements sit on top of each other | must be fixed |
| `contradiction` | two things on the page disagree — a number, a label, a legend | must be fixed |
| `legibility` | too small, too faint, too low-contrast to read | must be answered |
| `unkeyed` | a colour, mark or axis with no key, legend or label | must be answered |
| `judgement` | a taste call, not a defect ("no imagery on a food page") | recorded for the critic |

You choose the KIND; you never choose how serious it is. That stays fixed in the gate, so the same
observation weighs the same whoever read the deck.

## Output shape

```json
{"answers": [
  {"n": 1,
   "claim": "…", "about": "…", "largest": "…",
   "elements": {"text_blocks": 0, "photos": 0, "icons": 0, "charts": 0,
                "diagrams": 0, "tables": 0, "marks": 0},
   "legible_text": ["…"], "unreadable": [],
   "problems": ["a plain string is fine in English or Chinese",
                {"what": "de voettekst is afgesneden", "kind": "clipped"}]},
  …one object per slide, n = 1…N…
]}
```

## What happens to your answers

`scripts/blind_read.py compare` computes the disagreements — it does not score you and does not
score the deck. Each finding then has to be **answered in writing** by the deck's author: what
changed, or why you were wrong. So a careless "looks fine" costs someone a round-trip, and a
precise "the three glyphs on slide 7 are hairlines I cannot resolve at this size" is worth the run.

You are not judging quality. You are the evidence that someone who was not in the room can still
see what the page says.
