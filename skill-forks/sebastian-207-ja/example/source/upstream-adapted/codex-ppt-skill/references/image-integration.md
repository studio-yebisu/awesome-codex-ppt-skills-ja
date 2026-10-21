# Image Integration

Images are not dropped into arbitrary rectangles. Each image must choose one treatment: full-bleed hero, 60/40 split, masked editorial crop, atmospheric background with overlay, isolated object/cutout, image grid, device/product frame, or tinted monochrome treatment.

Generated images must not contain core titles, body text, or key numeric conclusions.

Images must be generated slot-first. The builder must know the target `image_slot`, `aspect_ratio`, and `integration_treatment` before the prompt is written. A generic background image is not a valid replacement for a slide-specific concept, scene, evidence, process, or product visual.

Default guidance:

- Cover or closing: `cover_hero`, 16:9, masked editorial crop or full-bleed hero.
- Text plus visual: `right_40` or `left_40`, 16:10, 60/40 split.
- Wide evidence strip: `top_strip`, 21:9, masked editorial crop.
- Data support visual: `chart_sidecar`, 4:3 or 16:10, chart-with-insight sidecar.
- Multiple examples: `image_grid`, same ratio for every image in the group.

`background_atmosphere` is allowed only when the slide has an explicit safe text zone and the image reinforces the page message. Do not use it as wallpaper.
