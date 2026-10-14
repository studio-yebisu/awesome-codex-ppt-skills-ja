# Artifact Contracts

Every task writes artifacts under `ppt_runs/<date>_<project>/`.

## Required For Every Task

- `requirement_check.md`
- `route_decision.md`
- `qa_report.md`
- `delivery_manifest.json`

## Required For New Decks

- `content_plan.md`
- `design_spec.md`
- `spec_lock.json`
- `slides_plan.json`
- `asset_plan.json`

## Reference PPT Tasks

- `reference_analysis.md`
- `reference_style_profile.json`
- `reference_structure_profile.json`

## Template PPTX Tasks

- `template_profile.md`
- `template_profile.json`

## Existing Deck Edits

- `change_plan.md`
- `change_log.md`
- before/after previews

## Single-Slide Edits

- `single_slide_edit_plan.md`
- `locked_slides.json`
- `preview_before/slide_NN.png`
- `preview_after/slide_NN.png`
- `change_log.md`

## Suggested JSON Shapes

`spec_lock.json`:

```json
{
  "route": "native_pptx",
  "aspect_ratio": "16:9",
  "slide_size": {"width": 13.333, "height": 7.5, "unit": "in"},
  "palette": {},
  "fonts": {},
  "allowed_layouts": [],
  "allowed_components": [],
  "export_targets": ["pptx", "pdf", "png"]
}
```

`slides_plan.json`:

```json
{
  "slides": [
    {
      "slide_id": "slide_01",
      "title": "",
      "purpose": "",
      "slide_type": "cover | toc | divider | content | summary",
      "layout_family": "",
      "content_budget": {"max_words": 80, "max_cards": 4},
      "assets": [],
      "speaker_notes_seed": "",
      "qa_risks": []
    }
  ]
}
```
