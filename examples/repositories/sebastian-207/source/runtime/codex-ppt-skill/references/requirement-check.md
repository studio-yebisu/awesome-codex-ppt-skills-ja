# Requirement Check

Run this before creating, referencing, editing, or exporting any PPT.

## Fields To Check

- Topic, content, or target PPT file
- Use case: report, training, class, pitch, product intro, lesson, social content, review, sales, defense
- Target audience
- Page count
- Style
- Output formats
- Editability requirement
- Reference PPT present
- Template PPT present
- Image generation needed
- Speaker notes needed
- PDF / PNG / HTML needed

## Required vs Optional

Only one thing is absolutely required:

- A topic/content direction, or the PPT/document file to process.

Everything else can be asked, inferred, or filled in Auto Mode.

## Ask Only What Matters

If the user already provided enough information, do not ask again. Restate the interpreted request and proceed.

If key information is missing, ask only the missing high-impact items, usually no more than three:

1. Who is this for?
2. About how many pages?
3. Preferred style or output format?

## Auto Mode

If the user says any of the following, stop asking and infer sensible defaults:

- 随便
- 你看着办
- 自由发挥
- 直接做
- 不用问我
- 按你觉得好的来

Auto Mode defaults:

- Page count: 8-12 slides
- Output: `final.pptx`, `final.pdf`, PNG previews, `qa_report.md`, `delivery_manifest.json`
- Editability: `balanced_editable`
- Style: infer from topic, industry, use case, audience, reference materials, and user keywords
- Image planning: enabled
- QA: required

## Required Output

Write `requirement_check.md` with:

- Interpreted user goal
- Inputs detected
- Missing fields
- Assumptions
- Whether user confirmation is needed
- Whether Auto Mode is active
- Recommended next route candidates
