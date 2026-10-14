---
name: paper2ppt
description: >-
  Use when a user wants an editable PowerPoint or PPTX made from a scientific or academic paper, paper PDF, DOI, PMID, arXiv link, article text, abstract with figure legends, or research notes for a journal club, group meeting, lab meeting, paper sharing, thesis seminar, or research talk; also when they ask for 论文转PPT, 文献汇报, 组会PPT, or 论文解读PPT. Not for general-purpose slide decks, business presentations, slide-image reconstruction, or paper-search-only requests.
---

# Paper2PPT

## Non-negotiable output

- Create an editable `.pptx` when authoring exists; never stop at an outline.
- Default to Simplified Chinese, 12-16 slides, and 15-20 minutes; adapt as requested.
- Add speaker notes and source labels to every result slide.
- Do not fabricate claims, values, mechanisms, methods, figures, or citations.

## Preflight

Resolve `<SKILL_DIR>` to this loaded `SKILL.md`'s directory: Claude Code substitutes `${CLAUDE_SKILL_DIR}`; Codex uses the absolute path in its available-skills entry. Never locate helpers from the current working directory. Before analysis, run `python "<SKILL_DIR>/scripts/preflight.py" INPUT --output PATH --json`; add `--create-output` deliberately. Use `--native-authoring` or `--native-pdf` only after confirming equivalent authoring or extraction; neither bypasses source/output failures. Verify audience, duration, language, template, and source sufficiency.

## Source sufficiency

Classify source sufficiency as `full-paper`, `partial-paper`, or `notes-only`; record it in `qa_report.md`.

Never imply unsupported full-paper knowledge. Reconstruct design, values, mechanisms, or diagrams only when every component and relationship is source-supported; otherwise omit. Label reconstructions and distinguish them from an original paper figure.

## Core workflow

1. Read [the evidence-first workflow](references/workflow.md) when generating from source, extracting figures, or doing substantive build or revision.
2. Extract only source-supported questions, gaps, design, claims, evidence, validation, limitations, and implications.
3. Build and use a claim-to-source map before drafting slides.
4. Classify the paper. Read [the paper-type routes](references/paper-types.md) when the user has not fixed the narrative or slide plan and the task is not a narrow repair; otherwise follow the supplied structure or repair scope.
5. Plan one claim per slide; build with notes and attribution, then run the quality gates.

For a narrow existing-deck audit or repair, load only guidance relevant to the requested change.

## Evidence and attribution

- Treat figures as evidence, not decoration.
- Preserve figure labels, scales, colorbars, statistics, and qualifiers.
- Never use AI-generated imagery as data evidence.
- Give each result slide a conclusion-style title, one claim, a source label, and evidence/limit notes.
- Trace assets by source location, figure or table, panel, crop status, and destination slide.

Read [adaptive slide design](references/slide-design.md) only when designing or revising layouts or correcting visual defects.

## Tool routing

Use available presentation tools; otherwise use PyMuPDF/Pillow and `python-pptx`. Install only when permitted.

After preflight, read [tool routing](references/tool-routing.md) when selecting or falling back between extraction, authoring, notes, or rendering tools.

## Quality gates

Run all available gates before delivery:

1. Content: verify sources, numbers, labels, marked inferences, and source sufficiency.
2. Structural: reopen the PPTX; verify editability, media, notes, sources, and files.
3. Visual: render every slide when possible; inspect clipping, overlap, readability, contrast, and figures. Otherwise record unavailable visual QA in `qa_report.md`.

Use exact states: `pass` only when all three gates pass;
`structurally-verified-with-disclosure` only when content and structural QA pass
and visual QA is unavailable solely because no renderer exists; `blocked` for
unresolved content/structure, failed editable authoring/reopening, or unresolved
visual failure when a renderer is available.

Read [quality gates](references/quality-gates.md) before final verification or when fixing QA failures.

## Output contract

Create only:

- `presentation_zh.pptx` by default, or `presentation_<language-code>.pptx` when the user explicitly requests another language;
- `qa_report.md`;
- `asset_manifest.md` and `assets/` only when assets are extracted.

Do not create PDF, XLSX, outline, script, or source-map deliverables by default.

## Failure handling

- On access failure, request a local PDF; never bypass access controls.
- Use OCR only after ordinary text extraction fails.
- Narrow claims and mark uncertainty for partial material.
- If an optional template is invalid, use a neutral academic layout; stop only when the template is mandatory.
- Without editable authoring, fail before extensive analysis and name the missing capability.

## Completion checklist

- [ ] Confirm the PPTX opens and matches language, duration, and audience.
- [ ] Record sufficiency and claim-to-source outcomes.
- [ ] Verify each result slide's claim, source, figure integrity, and notes.
- [ ] Complete all available QA; disclose unresolved limits in `qa_report.md`.
- [ ] Deliver only the minimal outputs.
