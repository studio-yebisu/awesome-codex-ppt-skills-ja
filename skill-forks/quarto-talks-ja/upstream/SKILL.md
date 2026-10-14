---
name: quarto-talks
description: Turn source material into a restrained Quarto RevealJS talk using the quarto-talks format. Use for papers, manuscripts, documents, figures, code, bibliographies, or existing slide decks when the requested output is an argument-led presentation.
---

# Quarto Talks

Produce a readable RevealJS presentation with the `quarto-talks-revealjs` format. The template is a visual baseline, not an automatic editor. Make the intellectual decisions before styling slides.

## Non-negotiable principles

1. A slide is a beat in an argument, not a rectangular container waiting to be filled.
2. Delete before shrinking, decorating, or complicating.
3. Empty space is useful. A slide may contain one claim, question, quotation, equation, figure, or code excerpt.
4. Use ordinary Quarto and RevealJS syntax. Prefer Markdown and fenced divs to custom machinery.
5. Unless the user explicitly requests another visual system, retain the format's white canvas, blue accent, system-serif headings, system-sans body, and monospace code face. Do not introduce ad hoc colours, per-slide font families, or remote fonts.

Never invent a citation, quotation, equation, empirical result, statistical significance claim, model output, figure, or successful code execution. If an item cannot be verified or reproduced, omit it or state the limitation plainly.

## Priority rules

These rules take precedence over lower-level stylistic guidance.

### Length discipline

Infer the likely talk duration from the user's request. When duration is unspecified, assume a standard 15 to 20 minute academic presentation.

For a standard talk:

- aim for roughly 16 to 24 slides total;
- treat 24 slides as a soft limit;
- above 28 slides, actively look for material to delete, merge, or carry orally;
- do not exceed 32 slides unless the user explicitly requests a longer lecture, workshop, or rapid-fire visual format.

Section dividers, quotations, questions, and sparse statement slides still count as slides.

Do not create a new slide for every inferential step. Delete intermediate propositions that the speaker can carry orally. Prefer a shorter deck with a clear argument over exhaustive coverage.

### Writing style

Avoid these patterns throughout slide titles and body text:

- contrastive corrective constructions such as "not X but Y", "not X. Y.", "the point is not X", and close variants;
- em dashes;
- excessive colons, especially in slide titles;
- aphoristic mini-verdicts;
- symmetrical slogan-like phrasing;
- chains of polished thesis headlines;
- generic AI presentation language.

Use natural, direct sentences. Vary syntax. Let evidence, quotations, figures, cases, and questions sometimes appear without immediately packaging them into a verbal verdict.

Before finishing, inspect the deck specifically for these patterns and rewrite them where found.

### Sources and bibliography

Create a `references.bib` file alongside the deck. Include every source cited or used as evidence, and add a `doi`, `url`, or both when possible so entries provide usable links. Validate each source against the original publication, publisher page, DOI record, or another authoritative record before citing it or relying on it. Do not add unverified search results or collected leads to the bibliography.

## Inputs

Inspect all relevant supplied material before drafting. Inputs may include `.qmd`, `.md`, `.tex`, `.docx`, `.pdf`, image files, bibliography files, code, data, and existing Quarto or Beamer presentations.

- Preserve source files.
- Record which claims, quotations, figures, and citations have verifiable sources.
- Check asset paths, licenses when relevant, and whether executable code has the dependencies and data it needs.
- Treat an old deck as evidence, not as a layout to reproduce blindly.

If audience or duration is not stated, infer cautiously from context and label the assumption in the working notes. A useful default pace is roughly one substantive beat per minute, with fewer slides for dense technical material.

## Workflow

### 1. Establish the brief

Identify:

- audience and what they probably know;
- likely duration and setting;
- the one sentence the audience should remember;
- the evidence needed to make that sentence credible;
- constraints such as required acknowledgements, citations, or accessibility needs.

Ask only for information that would materially change the talk. Otherwise make a conservative assumption and proceed.

### 2. Extract the intellectual spine

Write the argument as a short sequence of beats before writing slide prose. Each beat should do one job: establish an object, create a puzzle, pose a question, advance a claim, show evidence, qualify an inference, draw an implication, or land the ending. A beat is not automatically a separate slide: keep adjacent inferential steps together when the audience understands their relationship better in one composition.

For a research paper, usually look for:

- object;
- puzzle;
- research question;
- argument;
- main evidence;
- implications;
- ending.

This is a diagnostic list, not a mandatory order. Do not force conceptual, methodological, or exploratory work into a standard empirical-paper arc.

### 3. Select ruthlessly

Keep only material that serves the spine. Prefer one decisive result over a catalogue. Move robustness checks, secondary mechanisms, dense tables, and derivations to an appendix only when the setting requires them.

Build cadence rather than making every slide equally sparse or equally dense. A compact explanatory slide can be followed by a quotation, question, equation, figure, or section transition that gives the audience time to reset. Whitespace should mark a change in argumentative pace, not merely decorate a slide.

Vary slide forms when the material warrants it. After storyboarding, inspect runs of similar slides: replace a chain of statements with ordinary explanation, evidence, a figure, a table, mathematics, code, a genuine question, or a transition where one of those forms better carries the argument. Do not vary form merely for novelty.

Let evidence appear before interpretation when the audience can productively read the pattern. Give enough orientation to know what to inspect, then state or discuss the inference; do not always pre-announce the conclusion and reduce the evidence to decoration.

Do not manufacture sparse statement slides merely because a sentence can stand alone. Use one only when the audience benefits from a pause, emphasis, or genuine change of phase. When a sparse slide earns its place, keep it short enough to be large, vertically centred, and visually decisive; do not repeat the same claim on the adjacent slide.

As a drafting threshold, an ordinary slide will often hold one short paragraph and up to three short bullets, or four to five short bullets without the paragraph. This is a diagnostic, not a quota. If core material needs inline font sizing below roughly `0.75em`, delete, split, shorten, or move it before using `.smaller`.

### 4. Match form to purpose

Use the smallest semantic vocabulary that works:

| Class | Use it for |
|---|---|
| `.statement` | one important claim or transition |
| `.question` | a real question that moves the argument |
| `.quote` | one verified quotation with a source |
| `.visual` | a figure whose takeaway can be read at presentation distance |
| `.math` | one equation or a short derivation |
| `.code` | a short excerpt that can remain comfortably readable |

Ordinary slides need no class. Use normal Markdown for prose, lists, tables, citations, speaker notes, columns, fragments, and appendices.

Use RevealJS's native `.center` slide class when an ordinary slide contains one main object or one short interpretive block that should sit in the middle. Do not centre a multi-part explanation, long list, dense table, or full bibliography.

Use level-one headings as occasional section transitions when the argument genuinely changes phase. A section slide should name the new intellectual move, not just announce a generic topic. Use columns only when the relationship is itself visual: a true comparison, a sequence, or a result beside the evidence that explains it. Prefer simple `50/50` comparisons or `30/70` evidence layouts. When the argument contains a genuine mechanism, process, or sequence, show the relationship in one simple composition when that is clearer than narrating each link on a separate slide; do not invent a diagram for a merely rhetorical list.

Examples:

```markdown
## The mechanism is local {.statement}

It changes incentives at the point of decision.

## What would we observe without the policy? {.question}

## The outcome changes after adoption {.visual}

![Outcome by month](figures/outcome.svg){fig-alt="Describe the pattern, axes, and groups."}
```

Avoid repetitive bullet slides, generic scene-setting, decorative boxes, stock imagery, and section slides that do no argumentative work.

Form-specific judgment:

- **Statement:** use a full sparse slide for a claim the audience must retain, especially after a dense explanation. Keep the claim brief enough to project at large size. If it merely summarizes the previous bullet list, delete one of them.
- **Question:** pose a question only when the talk will answer it or use it to open a real uncertainty. Do not turn every topic heading into a question.
- **Quotation:** use one verified quotation when its exact wording or voice matters. Give it a source and generous space. If only the idea matters, paraphrase it as a statement instead.
- **References and citations:** let one or two essential sources function as a readable visual object. Keep a longer bibliography comfortably legible, and split or move it rather than reducing it to document-sized text.
- **Figure:** when a figure is primary evidence, let it stand nearly full-width on its own slide. A takeaway title is useful when the inference should lead; a neutral orienting title is better when the audience should inspect the evidence before hearing the interpretation. Pair the figure with prose or a second panel only when the relationship must be visible simultaneously. Never make the audience choose between reading a paragraph and decoding a plot.
- **Table:** use a table for an exact comparison, usually with a small number of rows and columns in the main talk. Prefer direct labels and minimal horizontal rules. Move exhaustive model output or taxonomies to an appendix.
- **Mathematics:** place one main equation, or two tightly connected equations, at the visual centre. Introduce only the symbols needed for that step. Put definitions beneath or on the next slide rather than wrapping a long derivation into a small box.
- **Code:** show a teaching step, not a file. Roughly 8–12 visible lines is a useful warning threshold. Split setup, transformation, and output into separate beats; keep a short explanation beside or below the excerpt. Never imply execution from syntax highlighting alone.

### 5. Draft readable source

Start from `template.qmd` or use this header:

```yaml
---
title: "Specific title"
subtitle: "Optional explanatory subtitle"
author: "Name"
date: today
bibliography: references.bib
format:
  quarto-talks-revealjs: default
---
```

Write informative slide titles. Give each slide one primary audience task, but keep tightly connected inferential steps together when separating them would create a mechanical slide-by-slide chain. Put detail in speaker notes when it matters to delivery but not to the projected argument.

Audience legibility outranks preserving every qualification or exact phrase on screen. If ordinary content cannot remain comfortably readable from the back of a room, simplify or split it before changing font size.

For figures:

- prefer an existing source figure if it is legible and permitted;
- otherwise reproduce it only when the underlying data and method are available;
- preserve units, labels, uncertainty, and source notes;
- add meaningful `fig-alt` text;
- never redraw a figure in a way that changes the evidence;
- prefer a white or transparent plot background, direct labels, restrained colour, and text large enough to survive projection;
- remove redundant plot titles when the slide title already states the takeaway.

For mathematics, show only the notation needed for the current step. Define symbols before using them and use `.math` when an equation is the visual centre of the slide.

For code, show the shortest excerpt that carries the idea. Do not claim it ran unless it was executed successfully in the current environment. Do not use `.smaller` merely to fit a long block.

For citations and quotations, reuse supplied bibliographies where possible. Verify quotation wording and page information against the source. A references slide can use a standard `#refs` div.

### 6. Render and inspect

Render with:

```bash
quarto render talk.qmd
```

Open the rendered HTML and inspect every slide at a normal presentation viewport. Check:

- missing images, bibliography entries, fonts, or other assets;
- accidental departures from the required white, blue, serif/sans, and monospace visual system when the user did not request an override;
- clipped or overflowing content;
- text, code, equations, labels, and citations that are too small;
- sparse slides whose main text is not genuinely large or vertically centred;
- ordinary content slides that are merely technically readable rather than comfortable at presentation distance;
- slides that feel awkwardly left-heavy when one centred object or short block would compose better;
- figures whose takeaway is not visible at a glance;
- poor colour contrast or missing alt text;
- accidental claims of causality, certainty, or execution;
- too many consecutive slides with the same layout;
- evidence that is repeatedly interpreted before the audience has a chance to see it;
- mechanisms or sequences fragmented across slides when one clear visual relationship would be easier to understand;
- no visual relief after several dense explanatory slides;
- weak hierarchy between serif headings, body text, code, captions, and source notes;
- a weak opening or an ending that merely says “thank you.”

Fix obvious problems and render again. Prefer changing the edit over adding CSS. Use `.smaller` or `.scrollable` only for exceptional appendix material, never as the first repair.

## Completion report

When handing off the deck, report:

- output path;
- render command and result;
- sources used and any assumptions;
- omitted or unreproducible material;
- remaining visual or factual limitations.
