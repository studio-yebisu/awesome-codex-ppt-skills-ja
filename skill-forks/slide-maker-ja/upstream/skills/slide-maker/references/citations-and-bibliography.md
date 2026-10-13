# Citations — read the .bib, never retype it

**Read this when the deck cites published work** — a defense, a journal club, a lab meeting, a
grant or conference talk, a literature review, any deck with a references page. Skip it for a deck
that cites nothing.

**Measured before this machinery existed:** `sources_page` rendered a list of strings and
`source_note` rendered a provenance line of strings. Nothing read a bibliography, nothing linked an
in-text marker to a reference list, and nothing could tell a correct year from a remembered one.
Every citation in every deck this skill had ever built was typed by hand — which is exactly where a
year drifts by one and a middle author disappears. On a slide, a misattributed result is a claim
about a real person's work.

---

## 1. The shape of it

```python
import citations as cit

db = cit.parse_bibtex(open("refs.bib", encoding="utf-8").read())
keys = ["lustig2007", "schlemper2018", "zbontar2018"]          # in CITED order
entries = [db[k] for k in keys]

# on a content slide — the marker comes from the SAME entry as the reference line
dk.text(s, 0.7, 2.0, 8.6, 1.2,
        [[("Compressed sensing set the baseline %s." % cit.in_text(entries[0], "numeric", 1),
           16, dk.DEEP, False, False, dk.FONT)]])

# the references page
cit.reference_page(ref_slide, entries, style="numeric")
```

`python3 scripts/sigs.py reference_page --example` prints a runnable call; `citations` is one of
the modules `sigs.py --list` covers, so the helpers are found the same way as every other.

Two styles, `numeric` (`[1]`) and `author-year` (`(Lustig et al., 2007)`). They are **slide**
reference lines — enough for a reader to identify the work and find it — not a journal's
copy-edited style. A deck is not a manuscript.

Non-English decks: `in_text(..., etal="等", amp="与")`. A hardcoded "et al." puts English into an
otherwise Chinese sentence, and the gate reads full-width `（张三等，2020）` markers too. The particle
is joined without a space when it is CJK, because Chinese does not space one.

🔴 **Two papers by the same first author in the same year need the a/b letter**, on the marker AND
on the reference line — without it both are `(Smith, 2020)`, which is ambiguous to the reader and
indistinguishable to the gate, so an uncited second paper reads as cited. `cit.suffixes(entries)`
assigns them in cited order and `reference_page` already applies them; pass `suffix=` to `in_text`
and `format_reference` when you write a marker yourself. A bare `(Smith, 2020)` over two such
entries is reported as `AMBIGUOUS MARKER`, not as a dangling one.

**Names the parser gets right, and why they are hard.** A doubly-braced author
(`author = {{World Health Organization}}`) is ONE atomic name — that is what the braces mean — so
it is not cited as "W. H. Organization", and a ` and ` inside such a name does not split it.
`and others` is BibTeX's own *et al.*, not a person. A `Jr.`/`Sr.`/`III` suffix is never mistaken
for a given name, in either the three-part `King, Jr., Martin Luther` form or plain
`Martin Luther King Jr.`.

## 2. 🔴 It refuses rather than filling in

An entry with no **author**, no **title** or no **year** is not formatted with `n.d.` or `Anon.` —
`format_reference` raises, naming the key and the field. Under this skill's never-invent floor a
plausible-looking citation is worse than a missing one: nobody downstream can tell it from a real
one, and neither can the author six months later. Fill the field in the .bib (the publisher's page
or the DOI record has it) or drop the citation.

The same rule covers what you must NOT do by hand: never type a reference line beside the
bibliography instead of deriving it. That second copy is the thing that goes stale.

## 3. What the gate checks

Record the plan, and `scripts/check_citations.py` checks the BUILT file on **both** gate paths:

```jsonc
"content": {"citations": {"bib": "refs.bib", "style": "numeric",
                          "keys": ["lustig2007", "schlemper2018"]}}
```

| finding | severity | what it means |
|---|---|---|
| `DANGLING MARKER` | block | `[7]` over a six-entry list — the leftover of a cut slide, and what an audience member looks up |
| `NOT IN THE LIST` | block | a cited key that appears in no reference list on any slide: the marker points at a page that is not in the deck |
| `NO SUCH ENTRY` | block | a cited key the bibliography does not contain |
| `INCOMPLETE ENTRY` | block | no author / title / year — the line cannot be built without inventing a field |
| `AMBIGUOUS MARKER` | block | the marker matches two entries — same first author, same year, no a/b letter |
| `DUPLICATE KEY` | block | a cited key is defined twice in the .bib; BibTeX keeps the first, so the citation may resolve to the wrong paper |
| `NOT A BIBLIOGRAPHY` | block | the file parses to zero entries — the wrong file, or a format this reads nothing of |
| `UNCITED` | note | an entry in the list that no slide points to: padding, and in a defense it reads as padding |

The bibliography path is resolved **inside the deck folder** and refused if it escapes — a record
is written by a build, and a build's record is not a licence to read anywhere on the machine.

**Nothing recorded is NOT CHECKED, out loud.** Most decks cite nothing, and a gate demanding a
bibliography of every deck would only teach authors to record an empty one. Waive in writing when a
marker legitimately resolves somewhere else (a handout, a linked preprint):
`{"citations": {"waived": "<why>"}}`.

## 4. Link the DOIs — and give the deck its own link colour

**The reference page's layout differs by style, and it is not cosmetic:** the numeric style hangs
`[n]` in a gutter, author-year has no gutter at all because its marker IS the opening of the line.
Measured on a render: setting an author-year marker in the gutter sized for `[1]` piled
`(Smith & van der Berg, 2020a)` through the three rows below it — while both lints passed and this
gate reported clean. The page is worth looking at, not just gating.

`reference_page` links every DOI it has, so a reference is one click from the paper. It also calls
**`dk.set_link_color(slide, ink)`** by default, and that is not decoration:

🔴 **A renderer paints a linked run in the THEME's hyperlink colour whatever fill the run itself
carries.** Measured on a rendered page: the two entries that happened to have a DOI came out in
bright underlined blue and the third in the deck's navy — one list, two typographies, decided by
whether a field existed in the .bib. The run's own `<a:solidFill>` cannot win that fight; the theme
is where a link's colour lives. Call `dk.set_link_color(prs, dk.DEEP)` once beside `set_palette` on
any deck with links; pass `link_style="theme"` to `reference_page` to leave the theme alone.

## 5. Where citations sit in the deck

- **On the slide**, next to the claim they support — a marker is chrome, so it rides in the
  reference line's mono/muted register, never competing with the takeaway.
- **`source_note`** still owns the *data* provenance line (where THIS chart's numbers came from).
  It and a citation marker are different jobs: one defends a number, the other attributes an idea.
- **The references page** goes after the close, with the Q&A backup slides
  (`references/navigation-and-qa.md`) — and a citation run can be linked with `dk.link(run, url)`
  so a curious reader lands on the paper rather than a search box.
