# Semantic Visual Brief

This file is the anti-lazy image and layout handoff contract. Read it before generating any image asset or building any slide that has a visual area.

## Principle

Do not generate a generic deck background and then drop it into slides.

Every generated image must be bound to one slide and one visual job:

- what the slide says
- why the slide needs a visual
- where the visual sits in the selected layout
- what aspect ratio the slot needs
- how the visual integrates with native text, chart, or shapes

If a visual cannot be explained through the slide's title and core message, it is decoration and must not be used as a required asset.

## Required Per-Slide Fields

For each slide in `asset_plan.json`, include:

```json
{
  "slide_id": "slide_03",
  "visual_need": "required",
  "asset_type": "concept_illustration",
  "generation_required": true,
  "reason": "This slide explains an abstract workflow and needs a visual model.",
  "image_slot": "right_40",
  "aspect_ratio": "16:10",
  "integration_treatment": "60/40 split",
  "must_not_skip": true,
  "semantic_binding": {
    "bound_to_slide": true,
    "slide_title": "",
    "core_message": "",
    "visual_role": "",
    "layout_archetype": "",
    "intended_composition": "",
    "visual_brief": ""
  },
  "prompt_path": "visual_briefs/slide_03_image_prompt.md"
}
```

## Slot-First Rule

Choose the layout and visual slot before generating the image.

Recommended slots:

- `cover_hero`: cover or closing visual, usually 16:9 or 21:9.
- `right_40`: text left, visual right, usually 16:10.
- `left_40`: visual left, text right, usually 16:10.
- `top_strip`: wide evidence or scene strip, usually 21:9.
- `chart_sidecar`: chart support visual, usually 4:3 or 16:10.
- `image_grid`: several related visuals, all same ratio.
- `background_atmosphere`: only when the image is intentionally full-bleed and content has a safe text zone.

Do not use `background_atmosphere` as the default. Most business and education slides need a placed visual, diagram, chart, or scene, not a wallpaper.

## Prompt Requirements

Every image prompt must include:

- slide title
- slide core message
- visual role
- aspect ratio
- composition and safe area
- style direction from `design_spec.md` or `reference_board.json`
- no title, no body text, no key numbers, no page chrome

Generated images may include short visual labels only when the route is `image_first` or the user explicitly accepts image-baked labels. For editable PPTX routes, titles, body text, chart conclusions, and important numbers stay native.

## Builder Rules

- Native and HTML builders must read `asset_plan.json`.
- If `output_path` exists, insert it using the declared slot and treatment.
- If an asset is required but missing, the builder may draw a lightweight semantic diagram as a draft fallback, but QA must fail until the required generated asset exists or an explicit screenshot/chart/user-asset alternative is recorded.
- Do not use a deck-level background image unless the user explicitly asks for a shared background system and `spec_lock.json` declares `background_image_scope="deck"`.

## QA Rules

QA fails when:

- a required generated image is missing
- a generated image prompt does not mention the slide title or core message
- the same generated image is reused across multiple required slides
- the image is marked as required but has no slot, aspect ratio, or integration treatment
- the visual is a generic background, seed image, gate image, or decorative filler
- right-side blank space exists without a declared visual role

