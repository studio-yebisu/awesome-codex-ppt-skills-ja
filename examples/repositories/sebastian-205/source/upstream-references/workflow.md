# Evidence-First Workflow

Use this reference after preflight. Keep the root Skill's evidence and output contracts authoritative.

## Contents

- [Progress checklist](#progress-checklist)
- [1. Preflight and workspace](#1-preflight-and-workspace)
- [2. Extract the source](#2-extract-the-source)
- [3. Build the claim-to-source ledger](#3-build-the-claim-to-source-ledger)
- [4. Plan the evidence arc](#4-plan-the-evidence-arc)
- [5. Select and prepare figures](#5-select-and-prepare-figures)
- [6. Build slides and notes](#6-build-slides-and-notes)
- [7. Run the QA loop](#7-run-the-qa-loop)
- [8. Revise and deliver](#8-revise-and-deliver)

## Progress checklist

Maintain this checklist while working:

- [ ] Preflight input, authoring path, output path, and renderer.
- [ ] Classify source sufficiency.
- [ ] Extract metadata, argument, evidence, and limits.
- [ ] Complete the claim-to-source ledger.
- [ ] Select a paper-type arc or follow the supplied structure or repair scope.
- [ ] Select only evidence-bearing figures and record provenance.
- [ ] Build the editable PPTX and speaker notes.
- [ ] Run content, structural, and available visual QA.
- [ ] Revise failures and rerun affected checks.
- [ ] Deliver only the minimal output set.

## 1. Preflight and workspace

1. Identify each input: local PDF, URL, DOI, PMID, arXiv record, pasted text, abstract and legends, notes, supplements, or template.
2. Resolve remote identifiers through lawful accessible sources. Request a local PDF when full text is blocked.
3. Confirm duration, audience, language, required emphasis, and template only when they are specified or materially ambiguous.
4. Choose a project-local output directory and avoid overwriting source files.
5. Prove that an editable PPTX can be authored before spending time on full analysis.
6. Detect a renderer separately; authoring success does not prove visual quality.
7. Record `full-paper`, `partial-paper`, or `notes-only` before extracting claims.

## 2. Extract the source

Use a staged strategy to control cost and unsupported interpretation.

### Pass A: establish scope

- Extract title, authors, venue, year, DOI or stable identifier, abstract, headings, figure legends, table captions, and page anchors.
- Determine whether text is selectable. Use OCR only after normal extraction fails.
- Identify missing sections, unreadable pages, unavailable supplements, and ambiguous figure references.
- Downgrade source sufficiency if the material cannot support the apparent input type.

### Pass B: establish the argument

- Read the introduction portions needed to identify the problem and gap.
- Read results around candidate claims and their cited figures or tables.
- Read methods needed to interpret design, cohorts, datasets, controls, endpoints, and statistics.
- Read discussion and limitations without treating speculation as measured evidence.
- Stop extracting material that does not support a planned claim or necessary context.

### Pass C: resolve evidence

- Revisit exact pages for quantitative values, group definitions, conditions, baselines, uncertainty, and statistical qualifiers.
- Check figure legends against panels and main text.
- Distinguish source statements from your synthesis and label inference explicitly.
- Do not infer omitted experiments, full workflows, mechanisms, or values from legends alone.

## 3. Build the claim-to-source ledger

Create an internal ledger before drafting slides. Use one row per candidate claim with these fields:

| Field | Record |
|---|---|
| Claim ID | Stable short identifier |
| Proposed claim | One bounded statement |
| Claim type | Context, method, result, validation, limitation, or implication |
| Source location | Page and section, figure/table and panel, or note identifier |
| Evidence detail | Value, comparison, observation, or quotation paraphrase |
| Support level | Direct, author interpretation, or labeled inference |
| Source sufficiency | Full-paper, partial-paper, or notes-only |
| Caveat | Missing control, uncertainty, scope, or access limitation |
| Destination | Planned slide number or excluded |

Reject or narrow any claim without adequate support. Keep the ledger internal unless the user requests it; summarize unresolved mapping issues in `qa_report.md`.

## 4. Plan the evidence arc

1. Classify the paper. Read [the paper-type routes](paper-types.md) when the user has not fixed the narrative or slide plan and the task is not a narrow repair; otherwise follow the supplied structure or repair scope.
2. State the audience's final takeaway in one sentence.
3. Allocate the slide budget across problem, gap, approach, evidence, validation, limitations, and implications.
4. Default to 12-16 slides for 15-20 minutes, but adapt to requested duration and complexity.
5. Write conclusion-style titles that make bounded claims.
6. Assign one main claim and its ledger entries to each result slide.
7. Prefer a dedicated slide over shrinking dense multi-panel evidence below presentation readability.
8. Remove slides that only repeat chronology, decorate the deck, or lack supported evidence.

Treat the plan as a hypothesis. Change it when the evidence forms a clearer arc.

## 5. Select and prepare figures

Select figures only after claims are mapped.

- Prefer the smallest set of panels that directly supports the evidence arc.
- Use original embedded images when reliable; otherwise render only relevant pages at sufficient resolution and crop carefully.
- Preserve panel labels, axes, units, legends, scales, colorbars, statistics, and qualifiers needed to interpret the evidence.
- Do not redraw a chart unless every value is explicitly available and editability materially helps; verify all transcribed values.
- Never replace missing experimental data with generated imagery.
- Create a reconstructed explanatory diagram only when every component and relationship is source-supported; otherwise omit it. Label permitted reconstructions and distinguish them from an original paper figure.
- Keep microscopy scale bars and image conditions visible.
- Split dense figures across slides when different panels support distinct claims.

For every extracted asset, record:

- filename;
- paper identifier and source page;
- figure or table number and panel;
- extraction method and crop status;
- preserved labels or deliberate exclusions;
- destination slide and supported Claim ID.

Write those records to `asset_manifest.md`. Create `assets/` only when at least one asset is extracted.

## 6. Build slides and notes

Use an editable authoring path and a neutral academic layout unless a valid template is supplied.

For every slide:

1. Use a title that states the slide's point.
2. Keep one main claim; use supporting bullets only when needed to interpret it.
3. Size the evidence for projected readability rather than decorative balance.
4. Put a concise source label on every result slide.
5. Add speaker notes that explain the claim, evidence, caveat, and transition without inventing details.

For result-slide notes, include:

- what the audience should inspect;
- what comparison or pattern supports the claim;
- the important quantitative or statistical qualifier;
- the limitation or uncertainty;
- the link to the next claim.

Keep citations and technical labels legible. Preserve important English terms when translating them avoids ambiguity.

## 7. Run the QA loop

### Content QA

- Trace every slide claim back to the ledger.
- Recheck numbers, units, cohort or dataset names, baselines, statistics, and causal wording.
- Confirm that partial-paper and notes-only decks do not imply full-paper review.
- Confirm every inference and reconstruction is visibly labeled.
- Confirm conclusions distinguish results from author interpretation and your synthesis.

### Structural QA

- Reopen the `.pptx` with a PPTX parser.
- Confirm slide count, expected dimensions, editability, media relationships, and absence of broken assets.
- Confirm speaker notes and source labels exist on every result slide.
- Confirm output filenames and the conditional asset files match the contract.

### Rendered visual QA

When a renderer exists, render every slide and inspect both individual slides and a contact sheet.

- Check clipping, overlap, off-slide objects, missing glyphs, low contrast, and inconsistent margins.
- Check titles, labels, citations, figures, axes, colorbars, and scale bars at presentation size.
- Check that no visual or text becomes unreadable merely to preserve a layout.
- Revise the deck, rerender affected slides, and repeat until failures are resolved.

When no renderer exists, do not claim visual QA passed. Record the unavailable check and residual risk in `qa_report.md`.

## 8. Revise and deliver

Write `qa_report.md` with:

- source sufficiency and unavailable material;
- authoring and rendering paths used;
- content, structural, and visual QA status;
- unsupported candidates removed or narrowed;
- remaining limitations and unperformed checks.

Deliver `presentation_zh.pptx` and `qa_report.md` by default. When the user explicitly requests another language, use `presentation_<language-code>.pptx`. Add `asset_manifest.md` and `assets/` only when assets were extracted. Do not add PDF, XLSX, outline, script, or source-map outputs unless requested.
