# Scientific visual baseline

This baseline is derived from the approved 12-page CAR T single-cell atlas
case. It is a reusable quality target for scientific and clinical research
decks, not a template to copy slide-for-slide.

## Design tokens

- Canvas: 16:9, light field `#F5F8FA`, 0.72 in outer margin, 12-column editorial grid.
- Type: Aptos Display for titles, Aptos for body text, Consolas for labels and source lines.
- Minimum visible body text: 12 pt. Smaller text is allowed only for metadata that
  is explicitly marked as such and is not required to understand the page.
- Palette roles: navy for interpretation, cobalt for cellular/analysis evidence,
  cyan for method and structure, orange for clinical or boundary emphasis, green
  for functional/preclinical evidence.
- Image treatment: paper-white frame, cover-fit crop, meaningful crop only,
  always paired with a visible source or figure caption.
- Decoration: fine rules and evidence markers; no ornamental gradients or
  persistent dashboard guides.

## Narrative contract

Scientific decks should preserve the evidence ladder:

1. clinical phenotype or observed signal;
2. cohort, sample, and assay design;
3. resolved cellular state or pattern;
4. candidate mechanism or network;
5. longitudinal or functional validation;
6. preclinical intervention or engineering direction;
7. bounded conclusion and unresolved limits.

Use explicit language for evidence level: `observed`, `resolved`, `proposed`,
and `tested`. Do not convert association into mechanism, or preclinical function
into clinical efficacy.

## Page archetypes

Use intentional variation. A research deck should not repeat one card grid.

| Archetype | Required visual anchor | Required support |
|---|---|---|
| Clinical timeline | duration axis or cohort comparison | definition, next question, source |
| Study pipeline | cohort → product → assay → analysis flow | sample counts and readout roles |
| Atlas map | enlarged UMAP or state map | legend, interpretation boundary |
| Strata axis | ordered groups or duration bars | cohort facts and associative caveat |
| Convergent evidence | one dominant figure composition | orthogonal readout labels |
| Mechanism network | network or cluster evidence | candidate-mechanism boundary |
| Longitudinal data | time series or collection windows | discovery/validation split |
| Preclinical sequence | editable experiment timeline | model, n, readouts, efficacy boundary |
| Engineering workflow | exposure → product → test | dose, culture context, preclinical boundary |
| Evidence ladder | rising evidence levels | figure refs and semantic distinctions |
| Bounded close | contribution plus evidence map | limits and unresolved question |

## Density and layout rules

- Every data page needs one focal evidence object, one sentence-level takeaway,
  and one explicit evidence boundary.
- Preserve process information: cohort, sampling, assay, comparison, timing,
  and readout are first-class content, not optional annotations.
- Do not shrink body text to fit more information. Edit, split, or change the
  composition instead.
- Keep captions and page numbers inside a safe bottom zone; captions may not
  touch divider rules or the slide edge.
- A crop may remove irrelevant material, but never crop away axes, legends,
  labels, comparison groups, or the result needed to support the claim.
- Tables are for compact comparison, not for reproducing an unreadable paper
  panel. If a table becomes dense, use a visual axis plus selected facts.

## Baseline QA requirements

The final PNG review must verify:

- 12-page or explicitly documented page count and 16:9 dimensions;
- page numbers are continuous and match the narrative order;
- all data pages have source attribution;
- body text is at least 12 pt unless clearly metadata;
- no text, caption, image, or axis is clipped or overlapped;
- images are not stretched and no partial neighboring panel remains after crop;
- page-specific evidence boundaries are visible;
- final deck is reopened, rendered, and visually inspected after every material revision.

Run `skill/scripts/check_scientific_baseline.py` for structural and text-level
checks, then complete the PNG visual gates in `qa-and-delivery.md`.
