# Academic Blueprint Template

Use this reference when turning an academic paper into a user-approved image PPT blueprint. The blueprint is the production source of truth for thumbnail design, sample pages, final imagegen prompts, QA, and PPTX packaging.

## Alignment Summary

Before extraction and blueprinting, ask concise questions only for missing high-impact information. Then present an `Alignment Summary` for user confirmation.

Required fields:

- paper file or source text;
- use case: thesis defense, seminar, course report, research talk, proposal defense, or other;
- audience: teachers, teachers and classmates, committee, industry audience, or mixed;
- target slide count or presentation duration; target slide count is a planning reference, not a strict limit;
- output mode: imagegen-generated full-page images embedded into PPTX by default;
- school, logo, student name, student ID, major, advisor, date, and any fields to omit;
- paper type and preferred chapter structure;
- preferred visual direction or reference thumbnail;
- required source figures, tables, formulas, and metrics to preserve;
- closing page wording and audience;
- assumptions that Codex inferred from the paper.

If the user provides duration but no page count, suggest a budget before blueprinting: maximum one slide per minute; typical academic budgets are 8-10 content slides for 10 minutes, 12-14 for 15 minutes, 15-18 for 20 minutes, and 30-40 for a 45-minute seminar. Ask the user to accept or revise the suggested budget, then treat it as a design reference rather than a hard cap.

Do not proceed when the user rejects or materially edits the summary. Revise and ask for confirmation again.

Default blueprint structure includes section divider pages for the main academic parts unless the user explicitly asks to omit or compress them. If page count is tight, ask whether to preserve section dividers or use a compact structure.

When drafting the blueprint, use the target count as guidance only. The final slide count is determined by actual academic communication needs and must be confirmed in `blueprint approval`.

## Academic Input Pack

After alignment, extract the paper into a compact source pack:

- title, author metadata, abstract, keywords, and research problem;
- paper type and chapter outline;
- research gap, research questions, and claimed contributions;
- theories, models, methods, datasets, variables, and experimental setup;
- exact formulas, tables, metrics, and named methods;
- figure inventory with redraw/preserve decisions needed; prefer imagegen redraw for charts and analytical figures while preserving source values, trends, axes, labels, legends, and metric numbers exactly;
- conclusions, limitations, and outlook;
- source locations for claims, figures, tables, and numbers.

## Narrative Spine

Create a short academic storyline before the page list:

```text
Research context -> research gap -> research question -> method/design -> evidence/results -> contribution -> limitations/outlook -> correction-request closing
```

For each major section, define one section-level governing message. A governing message is the page or section's main claim, not a decorative title.

Good governing messages:

- "平台生态的互补性与替代性并存，导致创新扩散机制呈现双路径特征。"
- "模型在故障早期识别中提升召回率，但仍需通过误报控制验证工程可用性。"

Weak governing messages:

- "研究背景"
- "实验结果"
- "本章内容如下"

## Deck Blueprint Fields

Each slide entry must include:

```text
Slide:
Page type:
Section:
Title:
Governing message:
Evidence role:
Visual opportunity:
Candidate visual directions:
Source evidence:
Must-preserve evidence:
Imagegen redraw permission:
Chart/key-finding annotation plan:
Unverified or missing facts:
Layout intent:
QA risks:
```

Field guidance:

- `Page type`: cover, contents, section divider, background, literature, method, framework, experiment, source figure, comparison table, summary, outlook, standalone closing.
- `Governing message`: one precise academic claim or communicative purpose for the page.
- `Evidence role`: what evidence or reasoning job this page performs. Use this instead of a fixed evidence-shape field.
- `Visual opportunity`: where imagegen can create a more expressive academic slide instead of a fixed card/table/box layout.
- `Candidate visual directions`: 2-3 possible visual carriers. Do not lock a single shape in the blueprint; the final carrier is chosen later by combining the evidence role with the approved thumbnail/sample visual contract.
- `Source evidence`: paper section, figure/table number, exact quoted fact, or extracted source location.
- `Must-preserve evidence`: exact names, Chinese terms, formulas, metrics, indicator meanings, captions, axis labels, school metadata, and closing wording.
- `Imagegen redraw permission`: for charts and analytical figures, prefer `redraw with exact values/trends` unless the user requests original preservation or exact redraw quality is unsafe. Direct original preservation must be explicit.
- `Chart/key-finding annotation plan`: how the slide will mark the main finding on the chart or table, such as callout arrow, highlight, label, shaded region, or focal color. Do not leave chart pages without interpretation.
- `Unverified or missing facts`: mark unsupported numbers, citations, cases, chart values, or claims as `needs user confirmation`. Do not include them in image prompts until confirmed.
- `Layout intent`: brief composition guidance, not a full image prompt.
- `QA risks`: Chinese readability, formula fidelity, metric drift, figure hallucination, citation drift, page count mismatch, or closing-page wording.

## User Revision Loop

After drafting the blueprint, show it to the user and ask whether it is approved. If not approved, ask the user to specify revisions in natural language. Accept page-level changes such as:

- "第 6 页的 governing message 改成强调机制差异，而不是平台对比。"
- "把 ROC 曲线单独成页，不要和混淆矩阵放在同一页。"
- "目录改为 5 个部分，增加理论与文献综述。"
- "第 12 页删掉，把训练过程和模型比较合并。"
- "尾页只写恳请各位老师批评指正，不要出现 Q&A。"

Apply the changes, re-display the revised blueprint, and wait again. Do not enter thumbnail design until the user explicitly approves the blueprint.

## Approval Record

Save the approved blueprint to `qa/deck-blueprint.md` with:

- alignment summary reference;
- academic input pack summary;
- narrative spine;
- final slide count;
- full slide blueprint;
- user approval note or timestamp;
- unresolved assumptions and risks, if any.
