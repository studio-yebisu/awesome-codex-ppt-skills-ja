# Reference PPT

Reference PPT work must state exactly what is borrowed.

## Modes

- `reference_style`: colors, fonts, visual rhythm, image treatment
- `reference_structure`: section order, page logic, narrative rhythm
- `reference_style_and_structure`: both visual system and organization
- `reference_content_rewrite`: rewrite source content into a new topic; never copy sensitive or unwanted content silently

## Ambiguous Requests

If the user says "参考这个 PPT 做一份新的" without scope, ask:

1. Only reference style?
2. Only reference structure?
3. Reference both style and structure, but rewrite content for the new topic?

If the user says "随便" or "你看着办", default to style + structure while rewriting content for the new topic.

## Required Outputs

- `reference_analysis.md`
- `reference_style_profile.json`
- `reference_structure_profile.json`

Tell the user:

- What was referenced
- What was not referenced
- Whether content was referenced
- Whether style was referenced
- Whether structure was referenced
- Whether original content will be rewritten
- Whether the original template is reused
- Whether placeholders/layouts are preserved
