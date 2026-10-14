# Style Library

Style is inferred before it is confirmed. Do not use a fixed default style.

## How To Infer Style

Use:

- Topic
- Industry
- Use case
- Audience
- Tone
- User keywords
- Reference PPT
- Uploaded images, screenshots, documents, or brand materials
- Output purpose: report, pitch, lesson, sales, defense, training, social post

Give 1-3 candidates and explain why. If the user says "随便" or "你看着办", pick the strongest candidate and proceed.

## V1 Style Cards

Use the JSON files in `assets/style-cards/`:

1. `executive-clean`
2. `tech-system`
3. `product-launch`
4. `visual-pitch`
5. `academic-paper`
6. `workshop-training`
7. `editorial-ink`
8. `swiss-grid`
9. `data-room`
10. `xiaohongshu-visual`

Each card includes:

- suitable_for
- unsuitable_for
- palette
- font_pair
- density
- layout_rhythm
- image_treatment
- forbidden_moves
- html_css_variables
- pptx_theme_mapping

## Candidate Mapping Hints

- Boss report, strategy, finance: `executive-clean`, `data-room`
- AI, SaaS, systems, developer tools: `tech-system`, `data-room`
- Product launch, sales, marketing: `product-launch`, `visual-pitch`
- Research, thesis defense, academic course: `academic-paper`, `swiss-grid`
- Training, workshop, classroom: `workshop-training`
- Cultural, writing, narrative, magazine: `editorial-ink`, `swiss-grid`
- Social content, Rednote/Xiaohongshu, visual cards: `xiaohongshu-visual`, `visual-pitch`
