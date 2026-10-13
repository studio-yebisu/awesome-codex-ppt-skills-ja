# Resume-Execute Split Workflow

## Purpose

Allows splitting presentation generation across two chat sessions when:
- The deck is very long (30+ slides)
- Context window limits are approaching
- The user wants to review the plan before execution

## When to Use

- Deck >= 25 slides with Rich/Canvas complexity
- User explicitly requests "plan first, generate later"
- Context usage exceeds 70% after Strategist phase

## Phase A: Planning Session

### Deliverables
1. Complete `content_design_spec.md` (all sections filled)
2. `template.css` (theme fully configured with CSS custom properties and component classes)
3. Image manifest (`assets/image_prompts.json`) if images needed
4. Summary of decisions made

### Exit Criteria
- All 9 Strategist confirmations complete
- Design spec has full slide-by-slide outline
- The source gate passes for the configured template and any existing content
- User approves the plan

### Handoff Artifact
Save all files to the project directory. The project directory itself IS the handoff artifact.

## Phase B: Execution Session

### Entry
User provides the project directory path (or it's the same session continuing after approval).

### Process
1. Read `content_design_spec.md` -- this is the single source of truth
2. Read `template.css` -- understand available CSS classes and custom properties
3. Read `theme.md` -- understand slide types, component classes, and layout API
4. Generate `content.html` following the design spec exactly, using `<section class="slide">` elements with appropriate CSS classes from the theme
5. Generate/acquire images if specified in manifest
6. Run the source gate, build with `html_compiler.py --all`, and visually review the browser PNG baseline
7. Pass the visual artifact gate; when requested, rebuild with `--all --include-pptx` and pass the delivery profile
8. Deliver output

### Rules
- Do NOT deviate from the design spec without user approval
- Do NOT re-ask confirmations that were decided in Phase A
- If something is ambiguous in the spec, make a reasonable choice and note it

## File Structure at Handoff

```
project/
├── content_design_spec.md   <- Source of truth (from Phase A)
├── template.css             <- Theme styles (from Phase A)
├── index-template.html      <- HTML skeleton (from Phase A)
├── theme.md                 <- Theme API reference
├── content.html             <- To be generated (Phase B)
├── index.html               <- Assembled output (Phase B, via html_compiler.py --all)
├── assets/
│   ├── image_prompts.json   <- If images needed (from Phase A)
│   └── *.png/jpg            <- Generated in Phase B
└── output/                  <- Generated in Phase B (SVGs, both PNG routes, receipts, optional PPTX)
```

## Resumption Protocol

When starting Phase B:
1. Identify project directory
2. Read `content_design_spec.md` completely
3. Read `template.css` to understand available CSS classes and custom properties
4. Read `theme.md` to understand the component API and slide types
5. Confirm understanding: "I'm resuming execution for [project]. The design spec calls for [N] slides with [complexity] complexity using [theme]. Shall I proceed?"
6. Begin writing `content.html`

## Context Optimization

Phase B should be efficient with context:
- Don't re-read strategist.md or design-guide.md (decisions already baked into spec)
- Load only: design spec + template.css + theme.md + relevant executor reference
- This leaves maximum context for the actual HTML/CSS content generation

## When to Trigger

The user opens a new chat (or continues an existing one) and signals resumption. Recognize any of:

| Pattern | Example |
|---------|---------|
| "resume execution projects/<name>" | "resume execution projects/quarterly_report_20250521" |
| Project path + continuation semantic | "continue generating projects/quarterly_report_20250521" |
| Chinese variants | "continue projects/quarterly_report_20250521" |

### Sanity Check

Before executing, verify Phase A artifacts exist:

| File | Required | Reason |
|------|----------|--------|
| `content_design_spec.md` | Always | Slide outline and design decisions |
| `template.css` | Always | Theme CSS implementation |
| `index-template.html` | Always | HTML skeleton for assembly |
| `theme.md` | Always | Theme API reference |
| `assets/image_prompts.json` | Only if images planned | Image generation manifest |

If any required artifact is missing, report which one(s) and stop. Do NOT fall back into Phase A automatically.

## Hand-back

Finish only after the source gate, full build, browser-baseline review, and visual artifact gate pass. Browser PNGs and DOM audit are layout truth; SVG-route output and fidelity findings diagnose conversion. If PPTX is requested, build with `--all --include-pptx` and pass the delivery profile before reporting the output paths.
