# Design Spec

Generate `design_spec.md` for human review and `spec_lock.json` for execution.

## design_spec.md

Include:

- Chosen style and backup candidates
- Why the style fits the user, topic, audience, and scenario
- Palette
- Font pair
- Layout rhythm
- Density
- Image treatment
- Chart/diagram treatment
- Typography hierarchy
- What not to do

## spec_lock.json

Use machine-readable values:

- route
- aspect ratio and slide size
- palette hex values
- fonts and fallbacks
- margins and spacing
- allowed layouts/components
- image strategy
- export targets

After a sample is approved, do not silently change `spec_lock.json`. If the direction changes, write a change note and ask when the change is material.

## Strategist / Executor Boundary

Strategist writes content and design artifacts. Executor creates slides from locked artifacts. QA validates outputs. Do not let Executor invent a new style mid-run.
