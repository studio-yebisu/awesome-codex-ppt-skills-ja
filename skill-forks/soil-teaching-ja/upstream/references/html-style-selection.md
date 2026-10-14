# Mode C Content-Driven Style Selection

Use an explicit user style as the source of truth. When no style is specified, recommend a small set of relevant choices and ask the user to select one during the Phase 1 confirmation. Do not mix or average families.

## Style Confirmation Procedure

1. Skip the question when the user already supplied a clear visual direction, template, brand system, or reference deck.
2. Otherwise offer 2-4 concise choices. Put one content-based recommendation first and explain each option in one short sentence.
3. Always include `Structured Teaching — Current default` as an option, even when another family is the recommendation.
4. State: `如果沒有偏好，我會沿用目前核定的 Structured Teaching 風格。`
5. Treat `沒有意見`, `你決定`, `照預設`, or a plan confirmation that does not address style as approval to use the current default. Do not block production with another style question.
6. Record the final family, palette, typography, motion, and image policy in the deck-level style brief.

Example choice format:

- `Structured Teaching — Current default`: warm white, black hierarchy, cool gray frames, muted orange emphasis; best for concepts and procedures.
- `Workshop Facilitation`: stronger task prompts and response areas; best for hands-on practice and discussion.
- `Research / Evidence`: neutral evidence-first tables and claims; best for reports or source comparison.
- `Hand-Drawn Teaching`: editable labels with restrained hand-drawn diagrams; best when concrete metaphors improve understanding.

Offer only the choices relevant to the material; replace the less relevant examples with `Narrative / Conviction` when the content is reflective or story-led.

## Approved Default: Structured Teaching

Use this style when the user has no preference:

- Warm white background `#F7F4EE`
- Ink black `#16191D`, muted gray `#62676D`, structural gray `#CDD1D4`
- One muted orange accent `#E65327`
- Microsoft JhengHei-first system sans-serif typography
- Stable top-left page number and section label, left-aligned titles, framed tasks and takeaways
- Editable HTML/CSS/SVG teaching diagrams, no raster images by default
- Subtle transitions; instructional progressive reveal only when sequencing matters

## Selection Order

Use this order to rank the recommendation:

1. Communication purpose
2. Learner task
3. Dominant information relationship
4. Presentation setting
5. Visual tone

Record the selected family and a one-sentence reason in the Phase 1 style brief.

## Style Families

### Narrative / Conviction

Choose for speeches, beliefs, reflective essays, stories, manifestos, and identity-oriented teaching.

- Large statements and generous whitespace
- Strong pacing between slides
- One visual metaphor or restrained shape system
- Minimal labels and restrained motion
- Avoid dense grids and dashboard styling

### Structured Teaching

Choose for concept explanation, knowledge organization, course instruction, procedures, and misconception correction.

- Clear frames, groups, hierarchy, comparisons, and processes
- Stable title and content zones
- One accent color for signaling
- Diagrams built with HTML/CSS/SVG
- Avoid decorative illustration that does not teach the relationship

### Workshop Facilitation

Choose for discussion, hands-on work, reflection prompts, group activities, and classroom practice.

- Prominent task instruction
- Clear sequence, time or material cues only when supplied
- Response frames, prompts, and action states
- High projection readability
- Avoid adding unrequested timers, scoring, or interaction logic

### Research / Evidence

Choose for reports, data, literature, findings, argumentation, and evidence comparison.

- Charts, tables, citations, and claims take priority
- Neutral palette and restrained decoration
- Visible units, labels, sources, and uncertainty
- Use native SVG or HTML where practical
- Avoid turning evidence into generic card grids

### Hand-Drawn Teaching

Choose when the user asks for a hand-drawn SOIL look or the content strongly benefits from concrete teaching metaphors.

- White background, black line language, gray texture, sparse accent color
- Editable HTML labels around local illustrations or inline SVG
- Use the Mode A YAML only when the user explicitly asks Mode C to match that old visual family
- Do not automatically inherit Mode A page furniture or fixed takeaway bar

## Tie-Breaking

When two families seem plausible, choose the family that best supports the dominant learner task. Prefer the more restrained family when visual complexity would not improve understanding. Surface a genuine conflict instead of blending incompatible patterns.

## Style Brief Fields

Include:

- Family
- One-sentence rationale
- Background and palette direction
- Typography direction
- Motion level: none, subtle, or instructional
- Image policy: none, optional, or required
- Repeated page furniture, if any
