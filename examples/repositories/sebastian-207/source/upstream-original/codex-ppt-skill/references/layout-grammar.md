# Layout Grammar

Default 16:9 decks use a 12-column grid, stable left/right safe margins, fixed title axis, 8 pt-derived spacing, consistent card padding, consistent line width, and a stable footer position.

## Locked Rules

- Same title axis across content slides.
- Same safe margin across the deck unless a cover or divider deliberately breaks it.
- Same radius and line-width system per deck.
- No random decoration to fill empty space.
- No layout invented outside the 24 archetypes unless the user explicitly asks for experimental design.
- A visual slot is part of the layout contract. If a slide uses a right-side, left-side, top-strip, or full-bleed visual area, `asset_plan.json` must declare the matching `image_slot`, `aspect_ratio`, and `integration_treatment`.
- Empty space must be named: breathing room, text safe zone, chart focus, image field, or navigation pause. Unnamed blank space is a QA failure.
