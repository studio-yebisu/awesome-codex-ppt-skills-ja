# Completion Contract

This is a highest-priority rule.

Planning artifacts are not final delivery.

Unless the user explicitly asks for "planning only" or "只规划、不生成", a presentation task is not complete until real presentation files have been generated, rendered, validated, and saved.

## New Deck Completion

A create-PPT task is complete only when these files exist and are non-empty:

- `pptx/final.pptx`
- `preview/final.pdf`
- `preview/slide_01.png` through the last slide PNG
- `qa_report.md`
- `delivery_manifest.json`

Intermediate files such as `requirement_check.md`, `route_decision.md`, `content_plan.md`, `design_spec.md`, `spec_lock.json`, `slides_plan.json`, `asset_plan.json`, and `template_profile.json` are useful, but they do not count as final delivery.

## Existing Deck Edit Completion

An edit task is complete only when these files exist and are non-empty:

- `pptx/edited_final.pptx`
- before and after PNG previews
- `change_plan.md`
- `change_log.md`
- `qa_report.md`
- `delivery_manifest.json`

Do not overwrite the user source file.

## Single-Slide Edit Completion

A single-slide edit is complete only when all conditions are satisfied:

- `pptx/edited_final.pptx` exists.
- The requested target slide changed as intended.
- All non-target slides pass semantic diff.
- Before/after previews exist.
- `locked_slides.json` exists.
- `compare_report.md` or `compare_report.json` exists.
- QA passes.

If a non-target slide changes materially, the task fails until repaired.

## Hard Delivery Rule

Never report a presentation task as complete unless the requested presentation files have actually been generated, rendered, validated, and saved.

If final files are missing, say that the run is blocked or failed and point to the real error in `qa_report.md` and `delivery_manifest.json`.
