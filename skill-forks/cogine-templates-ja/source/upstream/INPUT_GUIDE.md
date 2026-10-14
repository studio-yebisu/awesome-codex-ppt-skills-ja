# Input Guide For AI-Assisted Deck Generation

Use this guide when asking an AI agent to create a finished slide deck with this template library. Better input helps the agent choose the right template, preserve the design system, and turn your real content into a deck that is useful instead of generic.

## What To Provide

Give the agent enough context to make presentation decisions:

- Audience: who will read or hear the deck, and what they already know.
- Occasion: board update, sales pitch, class lecture, workshop, research talk, status review, investor meeting, internal planning, or another concrete setting.
- Goal: what the audience should understand, decide, approve, buy, or remember.
- Tone: executive, warm, technical, bold, calm, playful, editorial, premium, practical, or another desired voice.
- Scheme: light, dark, mixed, or no preference.
- Slide count: exact count if fixed, or a range if the agent can choose.
- Source material: outline, article, script, notes, data, quotes, screenshots, links, or brand/product facts.
- Constraints: required sections, required phrases, forbidden claims, legal/compliance requirements, preferred terminology, deadline, or language.

If you have numbers, charts, customer quotes, screenshots, diagrams, or examples, include them. If something is unknown, say that it is unknown instead of letting the agent invent it.

## Supported Input Types

### Structured Slide Outline

Best when you already know the deck structure.

Provide one entry per slide with a title, key message, bullets, and visual suggestion. The agent can map each slide to the closest layout in the chosen template and replace the placeholder content directly.

### Long Script Or Article

Best when your source is a memo, essay, transcript, product brief, report, blog post, or talk script.

Ask the agent to synthesize a slide outline first when the source is long, narrative, repetitive, or not already divided into slides. The outline should identify the deck arc, remove duplicate ideas, preserve important evidence, and choose which details belong in speaker notes or can be omitted.

After you approve the outline, the agent should build the deck from that outline rather than trying to paste the whole source into slides.

### Scattered Notes And Raw Materials

Best when you have fragments: meeting notes, bullet dumps, screenshots, stats, links, customer quotes, product facts, or partial thoughts.

Ask the agent to first sort the material into themes, identify missing decisions, and propose a slide outline. This synthesis step is important because raw notes rarely contain the final deck order, emphasis, or level of detail.

If the agent finds gaps that would change the story, template choice, or slide count, it should ask concise clarifying questions before building the deck.

## Copy-Paste Brief Format

Use this format when starting a deck request:

```txt
Deck goal:

Audience:

Occasion:

Desired tone:

Preferred scheme:

Slide count:

Language:

Required content or sections:

Source material:

Constraints or things to avoid:

Per-slide outline:
1. Title:
   Key message:
   Bullets:
   Visual suggestion:

2. Title:
   Key message:
   Bullets:
   Visual suggestion:

3. Title:
   Key message:
   Bullets:
   Visual suggestion:
```

If you do not have a per-slide outline yet, replace that section with:

```txt
Please synthesize a slide outline first from the source material before choosing or building the final deck.
```

## Per-Slide Detail

For each slide, the most useful inputs are:

- Title: the slide headline or section label.
- Key message: the one sentence the audience should take away.
- Bullets: supporting facts, arguments, examples, or steps.
- Visual suggestion: chart, timeline, comparison table, quote, screenshot, diagram, product image, metric card, process flow, or no preference.

Keep bullets short. A good slide brief usually gives the agent the thinking, not the final paragraph text.

## When Agents Should Synthesize An Outline First

Agents should propose an outline before building the deck when:

- The input is a long script, article, transcript, report, or memo.
- The input is scattered notes or raw research material.
- The requested slide count is much smaller than the source material.
- The audience, occasion, or goal is unclear.
- The source has repeated, conflicting, or low-priority points.
- The user asks for help shaping the story, not only formatting existing slides.

The outline should include slide titles, key messages, rough visual direction, and any open questions that would materially affect the deck. Once the outline is accepted, the agent can select a template and produce the browser-openable HTML deck.
