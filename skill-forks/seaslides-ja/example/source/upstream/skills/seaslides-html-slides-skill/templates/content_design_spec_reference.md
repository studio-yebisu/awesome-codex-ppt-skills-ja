# {project_name} - Content Design Specification

> **Purpose**: Plan the narrative, slide-level content, theme usage, images, and speaker notes before authoring `content.html`. The Executor uses this file as the content source of truth.
>
> **Boundary**: Record intended classes and layouts here, but keep CSS implementation in `template.css` and browser-shell dependencies in `index-template.html`.

Replace bracketed placeholders and remove unused optional rows. Match the user's language in field values while preserving these section headings.

## Contents

- [I. Project Information](#i-project-information)
- [II. Theme Selection](#ii-theme-selection)
- [III. Narrative Framework](#iii-narrative-framework)
- [IV. Visual Direction](#iv-visual-direction)
- [V. Content Outline](#v-content-outline)
- [VI. Image Resource List](#vi-image-resource-list)
- [VII. Speaker Notes Plan](#vii-speaker-notes-plan)
- [Executor Handoff Checklist](#executor-handoff-checklist)

## I. Project Information

| Item | Value |
|---|---|
| **Project Name** | {project_name} |
| **Page Format** | [16:9 / 4:3] |
| **Canvas** | [1280x720 / 960x720 / other scenario-owned size] |
| **Page Count** | [planned range] |
| **Style Objective** | [General / Academic] |
| **Target Audience** | [role, expertise, context] |
| **Core Message** | [one sentence] |
| **Use Case** | [talk, report, course, pitch, etc.] |
| **Language** | [language and terminology requirements] |
| **Created Date** | {date_str} |

## II. Theme Selection

| Property | Value |
|---|---|
| **Catalog Theme ID** | [ID from `templates/index.json`] |
| **Theme Directory** | [`templates/<theme-id>/`] |
| **Theme API** | [`theme.md`] |
| **Palette / Variant** | [named palette or CSS variable overrides] |
| **Typography** | [display, body, mono, CJK fonts] |
| **Supported Modes Used** | [light / dark / hero light / hero dark] |
| **Visual Character** | [brief content-relevant description] |

### Runtime and Rich-Content Needs

Include only dependencies the content actually needs.

| Need | Rendering Path | Slides |
|---|---|---|
| Math | [MathJax / none] | [slide numbers] |
| Code | [Prism language classes / none] | [slide numbers] |
| Pseudocode | [pseudocode.js / none] | [slide numbers] |
| Charts | [theme components / SVG / browser library / none] | [slide numbers] |
| Other browser dependency | [name / none] | [slide numbers] |

## III. Narrative Framework

| Item | Decision |
|---|---|
| **Narrative Arc** | [Hook-Context-Core-Shift-Takeaway / SCQA / Academic Funnel / custom] |
| **Audience Already Knows** | [brief answer] |
| **Knowledge Gap** | [brief answer] |
| **Likely Misconception** | [brief answer] |
| **Desired Takeaway / Action** | [brief answer] |

### Title Spine / Ghost Deck Test

List slide titles in order. They should communicate the argument without body content.

1. [Slide 1 title]
2. [Slide 2 title]
3. [...]

## IV. Visual Direction

| Item | Decision |
|---|---|
| **Visual Premise** | [how the visual language reinforces the core message] |
| **Cross-Page Continuity** | [recurring cue(s), planned transition/reset points, and why] |
| **Vertical Composition Strategy** | [how content pages alternate centered cluster, top-to-bottom, split anchors, image hero, and intentional breathing] |
| **Image Treatment** | [dominant framing/crop/caption approach; theme owns CSS] |
| **Typography Delivery Plan** | [language, delivery medium, and theme/project-local weight-token decisions] |
| **Optional Crop-Safe Background** | [local asset, focal point, safe regions, contrast plan, or none] |

## V. Content Outline

| Slide # | Type | Title | Narrative Function | Rhythm | Mode | Layout | Vertical Mode | Components | Key Content | Image / Composition |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | cover | [title] | hook | anchor | hero dark | [theme layout] | intentional breathing / image hero | [theme classes] | [subtitle, author, context] | [file / P skeleton + optional M-A-C / none] |
| 2 | content | [action title] | ground | breathing | light | [theme layout] | [centered cluster / top-to-bottom / split anchors / image hero] | [theme classes] | [actual claims and evidence] | [file / P skeleton + optional M-A-C / none] |
| N | ending | [takeaway] | resolve | anchor | [mode] | [theme layout] | intentional breathing / centered cluster | [theme classes] | [closing message or action] | [file / P skeleton + optional M-A-C / none] |

Use only layouts and component classes documented by the selected theme or explicitly planned for addition to `template.css`. Repetition is acceptable when it communicates comparison, sequence, or continuity.

### Per-Slide Detail

Add a detail block whenever the summary row does not give the Executor enough information to author the slide without reopening the source.

#### Slide {N} - {Title}

| Property | Value |
|---|---|
| **Purpose** | [what this slide must accomplish] |
| **Layout and Hierarchy** | [regions, reading order, column proportions] |
| **Vertical Composition** | [mode, body-height owner, lower-page role, and real lower anchor or intentional negative space] |
| **Theme Classes** | [actual classes from `theme.md` / planned reusable additions] |
| **Rich Content** | [math, code, chart, table, pseudocode, or none] |
| **Image and Alt Text** | [filename, placement, alt text, or none] |
| **Image Composition and Framing** | [P structure; useful M, prepared A, or cross-page C; target slot ratio and fit; crop permission/safe area/focal point; theme-supported padding/alignment/frame treatment; caption/source or none] |
| **Source / Citation** | [source reference or none] |

**Content**

- [claim, evidence, data point, quotation, or explanation]
- [additional content needed for implementation]

**Speaker-note intent**: [context to say aloud rather than render]

### Artifact and Issue Ownership

Assign one accountable owner for each handoff area. These labels clarify triage; they do not create a new workflow role or automated routing.

| Area | Accountable Owner | What They Resolve |
|---|---|---|
| **content** | [name / role] | claims, outline, notes, citations, and semantic HTML content |
| **theme** | [name / role] | reusable tokens, components, visual treatment, and theme fidelity |
| **runtime** | [name / role] | browser dependencies and settled-render behavior |
| **export** | [name / role] | assembly outputs and browser/SVG/PPTX delivery differences |
| **source** | [name / role] | source availability, attribution, permissions, and source-to-claim correspondence |

## VI. Image Resource List

| Filename | Purpose | Source / Acquire Via | Status | Intended Slides | Layout Role | P/M/A/C Composition | Framing / Crop Safety | Alt Text / Caption / Source |
|---|---|---|---|---|---|---|---|---|
| [filename] | [narrative purpose] | [user / source / web / AI] | [ready / pending / excluded] | [numbers] | [hero / side / background / diagram / decorative] | [P skeleton; optional M treatment; prepared A dependency; C relationship] | [slot ratio, contain/cover, crop permission, focal point, safe region, theme treatment] | [text] |

If no images are needed, write `None` and explain why. Use relevant and user-required assets; record the reason for excluding material source images.

## VII. Speaker Notes Plan

| Item | Decision |
|---|---|
| **Tone** | [conversational / analytical / pedagogical / executive] |
| **Audience Address** | [direct, formal, instructional, etc.] |
| **Terminology / Pronunciation** | [requirements or none] |
| **Timing Emphasis** | [slides that need more or less dwell time] |
| **Citation Guidance** | [how sources should be mentioned aloud] |

Every slide receives a `data-notes` attribute. Use notes for delivery context, transitions, caveats, and explanations that should not crowd the visual canvas.

## Executor Handoff Checklist

- [ ] Theme ID exists in `templates/index.json` and its `theme.md` was read.
- [ ] Every planned slide has a title, mode, layout, vertical mode, components, and implementable content.
- [ ] Math, code, pseudocode, charts, and browser dependencies are identified.
- [ ] Image paths, statuses, uses, alt text, and intentional exclusions are recorded.
- [ ] Visual Direction records cross-page continuity and any intentional resets.
- [ ] Image-led pages record useful P/M/A/C composition responsibilities when they help execution; letters, IDs, and coverage are not quotas.
- [ ] Screenshots preserve the original UI by default and record slot ratio, fit, crop permission, focal/safe areas, and truthful caption/source when needed.
- [ ] Any background image is local, optional, and verified crop-safe for its target canvas.
- [ ] Artifact and issue ownership is assigned for content, theme, runtime, export, and source.
- [ ] Titles pass the Ghost Deck Test.
- [ ] Repeated layouts and mode choices are intentional rather than quota-driven.
- [ ] Content pages do not rely on a footer or page number to disguise a top-packed body.
- [ ] Speaker-note intent is clear for every slide.
