# Clinical and evidence-synthesis figures

The forms a trial, a meta-analysis, a diagnostic-accuracy study or a method-comparison paper is
*made of* — and the fidelity rules each one carries.

## Why this file exists

`design-by-topic.md` lists **Medicine / biotech / clinical** as a first-class domain and tells you
which PRESET to dress it in. Every row in that table is an *aesthetic* row: it changes the palette
and the type, and **none of them changes the FORM vocabulary**. Measured by grep across
`references/`, `scripts/` and `agents/` before these components existed, there were zero hits for
*kaplan-meier*, *forest plot*, *CONSORT*, *PRISMA*, *Bland-Altman* or *ROC*.

The two vocabularies the skill already had are both real and both from somewhere else:

| existing | what it actually covers |
|---|---|
| `designed_charts` (waterfall · marimekko · pareto · radar · slope · dumbbell) | **business analytics** |
| `schematic-diagrams.md` (free-body · optics · circuit · apparatus · vector · wave) | **undergraduate physics** |

So the skill could *style* a clinical deck and could not *draw* one, and the author's only option
was a hand-rolled scatter — which is exactly where the rules below get broken silently, because a
wrong chart is a perfectly well-formed set of shapes and no geometry lint can see it.

## Pick by the question the slide answers

| the question | form | call |
|---|---|---|
| Who got in, who dropped out, who was analysed? | participant flow | `deckkit.consort_flow` |
| Does the same effect hold across studies / subgroups? | forest plot | `designed_charts.forest_plot` |
| Do these two groups differ in time-to-event? | survival curve | `designed_charts.km_curve` |
| Do these two methods MEASURE the same thing? | agreement plot | `designed_charts.bland_altman` |
| How well does this classifier separate two classes? | ROC | `designed_charts.roc_curve` |
| Which classes does the model confuse? | confusion matrix | `deckkit.heat_matrix` (see below) |
| Is this value a mean of MEASUREMENTS, not a count? | distribution | `designed_charts.distribution` |

**A confusion matrix needs no new component.** `heat_matrix(values, row_labels, col_labels,
scale="seq", cell_labels=…)` is one, with two conventions to set yourself: label the axes
*Predicted* (columns) and *Actual* (rows) so the reader knows which way round it is, and say in the
caption whether the cells are COUNTS or ROW-NORMALISED rates — the same matrix tells opposite
stories under the two readings, and an unlabelled one is unreadable on an imbalanced dataset.

## The rules each component owns

These are the ones that are wrong *by default* when the form is hand-rolled. Each is enforced in
code, so you get it right by reaching for the component rather than by remembering.

- **`consort_flow` — the arithmetic is ENFORCED.** Every stage's count minus its documented
  exclusions must equal the next stage's count; it raises with the sum spelled out when it does
  not. A flow diagram whose numbers do not balance is the commonest error in trial and review
  reporting and the first thing a referee adds up by hand. 🔴 **Nothing else in this skill can
  check a claim of this kind** — the lints measure geometry, the critic reads pixels, and both pass
  a diagram that loses fourteen patients between two boxes.
- **`forest_plot` — ratios live on a LOG axis.** An OR/RR/HR is symmetric in log space (0.5 and 2
  are the same effect in opposite directions), so on a linear axis the left half of every CI is
  squashed and the right stretched, and the eye reads an asymmetry that is not in the data. `log`
  defaults to `null == 1`; pass `null=0` for a difference scale. Ticks are forced to plain numbers
  — matplotlib's log formatter renders the null as `10⁰`, and a reader looking for the line at ONE
  should not have to decode an exponent. A non-positive bound on a log axis raises.
- **`km_curve` — survival is a STEP, and the numbers at risk are part of the figure.** The estimate
  changes only AT an observed event; a straight line between observations asserts deaths on days
  nobody was seen. Censoring ticks are what separate "we stopped watching" from "nothing happened".
  The at-risk table is the part reviewers ask for first: a curve whose right tail rests on two
  patients looks identical to one resting on two hundred. Pass raw `(times, events)` — the
  estimator runs here, so there is nothing to get wrong by hand.
- **`bland_altman` — agreement is not correlation.** Two methods can correlate almost perfectly and
  still disagree by a clinically fatal constant, so a scatter of A against B with an r value is the
  classic wrong answer. The limits are `bias ± 1.96·SD of the DIFFERENCES`, drawn and labelled with
  their values, because the number a reader judges is "where do 95% of individual disagreements
  fall, and can my application tolerate that?". A funnel shape means the disagreement grows with
  magnitude — switch to `percent=True`.
- **`roc_curve` — square canvas, chance diagonal, AUC in the legend.** On a stretched axis every
  classifier looks better than it is, and without the diagonal there is no visual anchor for "no
  better than guessing". AUC is printed because the curve alone does not let a reader rank two
  models that cross. Pass raw `(y_true, y_score)`; the curve and the AUC are computed here.

## What this file does NOT cover

No component is supplied for a **phylogenetic tree**, a **chemical reaction scheme**, or a
**theorem–proof structure**. `deckkit.org_tree` is a tidy hierarchy and will draw a small clade
legibly, but it is not a phylogeny (no branch lengths, no support values) — say so rather than
implying one. For a reaction scheme, `schematic-diagrams.md`'s image-tool path with native labels
is the honest route today.

🔴 **And the fidelity floor is unchanged and outranks all of this.** These components make the
*form* correct; they cannot make the *numbers* true. Every count, estimate, interval and p-value
still traces to the source under the never-invent rule, and a plausible-looking curve drawn from
numbers nobody checked is worse than no figure, because it is harder to doubt.
