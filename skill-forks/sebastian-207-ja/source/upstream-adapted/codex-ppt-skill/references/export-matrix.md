# Export Matrix

## Default Outputs

- `pptx/final.pptx`
- `preview/final.pdf`
- `preview/slide_XX.png`
- `qa_report.md`
- `delivery_manifest.json`

## Optional Outputs

- HTML
- `speaker_notes.md`
- social cover
- `reference_analysis.md`
- `change_log.md`

## delivery_manifest.json Must Record

- route
- source artifacts
- output files
- QA status
- editable level
- image generation status
- known limitations

## Editable Levels

- `editable`: mostly native PPT objects
- `balanced_editable`: key text/data editable, supporting visuals may be raster
- `partly_editable`: mixed native and image/HTML-derived content
- `non_editable_image_pages`: full-slide raster pages

## Route Export Notes

- `template_pptx`: primary output is editable PPTX; PDF/PNG previews prove render quality.
- `native_pptx`: primary output is editable PPTX; PDF/PNG previews required.
- `html_slides`: HTML/PDF/PNG are stable; PPTX is best-effort.
- `image_first`: PPTX is a container of full-slide images; record editability limitation.
