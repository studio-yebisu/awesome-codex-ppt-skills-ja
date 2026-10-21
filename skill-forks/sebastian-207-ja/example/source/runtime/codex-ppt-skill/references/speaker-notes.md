# Speaker Notes

Treat speaker notes as first-class artifacts.

## Rules

- Use notes to carry detail that would overload slides.
- Do not leak speaker notes into slide body text.
- For HTML route, store notes in sidecar JSON or comments, not visible UI.
- For PPTX route, embed notes when tooling supports it.

## Artifacts

- `speaker_notes.md`
- Optional `notes_manifest.json`

## notes_manifest.json Shape

```json
{
  "slides": [
    {"slide_id": "slide_01", "notes": "Speaker notes here."}
  ]
}
```

Use `scripts/embed_speaker_notes.py` as a V1 interface skeleton.
