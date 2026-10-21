# Art direction and native-PPTX reconstruction

Use this reference when the user asks for a polished, distinctive, portfolio-quality, brand-led, or reference-matched presentation. Read it after `design-and-visuals.md` and before authoring the design system.

## The design-system contract must become art direction

A palette, font list, and grid are necessary but insufficient. Before layout, write `art_direction` in `design-system.json` with:

1. **Visual thesis:** one sentence connecting intent, audience, and desired feeling.
2. **Reference scope:** selected visual cluster, transferable quality floor, and anti-copy rule.
3. **Material language:** background, surface, and depth behavior.
4. **Edge language:** primary/secondary geometry and overlap policy.
5. **Image system:** named image roles, treatments, reuse policy, and factual-media policy.
6. **Native/raster strategy:** which elements remain editable, which may be raster, and prohibited shortcuts.
7. **Slide families:** at least three planned page families with purpose, macro composition, image occupation, and tone.

Do not leave these as adjectives such as “modern,” “premium,” or “minimal.” Write observable constraints such as “ivory textile ground with one dark curved footer anchor,” “large product detail macro as a background layer,” or “native charts with direct labels, no cards around evidence.”

## Art-direction sequence

### 1. Select a visual thesis, not an averaged style

Choose one intent-fit direction. A deck can borrow crop discipline from a fashion reference and proof staging from a technical reference, but it must not average unrelated style clusters into “generic clean modern.”

### 2. Define material language

Material language answers: what does the page feel made of?

- matte paper, quiet linen, gloss, glass, film grain, dark stage, architectural white, or none;
- flat versus layered surfaces;
- shadow direction, opacity, and use limit;
- texture role and contrast budget.

Texture must remain low contrast and local. It must never reduce data or body-text legibility.

### 3. Define edge language

Edge language answers: how do areas meet?

- rectilinear grid;
- rounded editorial window;
- organic curve;
- contained frame;
- hard color block;
- controlled cutout/overlap;
- hairline rule.

Pick a primary edge grammar and one secondary accent at most. Do not apply every available radius, curve, border, and shadow to one deck.

### 3a. Contrast and decorative-geometry gate

Treat color as a relationship between a text role and its **rendered** surface. A light palette token does not authorize light copy if a local panel, mask, or failed dark background leaves a light surface underneath. Set explicit on-light and on-dark roles, then inspect each slide after crop/mask/background rules are applied. Normal text must meet 4.5:1 contrast; supporting or muted text must meet 3:1. Add a scrim only when text intentionally sits on an image, and make the scrim's boundary legible.

Decorative geometry is valid only when it has a named visual job: frame a focal subject, separate two reading zones, expose a material layer, or continue an established brand motif. A giant ellipse, cropped strip, or abstract cutout that interrupts a person/product without adding meaning is a defect, not luxury. Prefer a clean split, contained editorial window, rule, or intentional crop. Do not repeat a decorative mask just because it worked once.

### 4. Define the image system before placing images

Possible roles include:

- `hero`: the first emotional or conceptual entry;
- `process`: authentic work in progress;
- `product`: finished item or interface at inspectable scale;
- `detail`: texture, craft, material, or close observation;
- `context`: environment, team, customer, or place;
- `evidence`: screenshot, artifact, chart, document, or result;
- `texture`: low-contrast ambient material;
- `cutout`: isolated person/object used for composition.

For every asset, resolve its role, focal subject, crop tolerance, safe space for copy, placement, source/provenance, and whether it is fact or illustration. The role determines the composition; never put every photo into a generic right-side rectangle.

### 5. Plan slide families and rhythm

Create a rhythm map before authoring. Use three to six families, for example:

| Family | Job | Typical image occupation | Suitable topologies |
|---|---|---:|---|
| entry | orient or make a high-stakes claim | high | stage, asymmetric split |
| proof | let audience inspect evidence | medium | frame, axis, annotated split |
| mechanism | explain a process or relationship | low to medium | spine, network, field |
| gallery | show selected work or range | high | mosaic, curated strip, contact sheet |
| decision | compare or commit | low | matrix, axis, decision frame |
| close | resolve and leave a memory | low or high | stage, sparse frame |

Vary macro composition, tone, density, and image occupation. Repeat furniture, type roles, and material/edge language. Repetition of an entire page shell is allowed only when it is a deliberate series, such as a four-look collection gallery.

## Atelier editorial direction as a worked principle

For a fashion/atelier portfolio, an appropriate contract could state:

- visual thesis: warm editorial atelier that makes precision and human craft visible;
- material: soft ivory textile/paper with subtle ambient shadow;
- edge: one organic vertical divide, fine rules, dark footer anchor;
- type: high-contrast serif display, short copper script accent, neutral sans utility text;
- image roles: maker/process, mannequin/product, close material detail, collection lookbook;
- rhythm: profile → expertise → timeline → tools → process → details → gallery → close;
- native/raster: native text, rules, cards, timelines, page furniture; local raster photos/textures and approved complex masks.

This is a **principle example**. Do not apply its beige palette, curve, footer, or serif type to a fintech or technical report without an intent-fit rationale.

## Native-PPTX reconstruction

### Default: reconstruct, do not flatten

When editable PPTX is requested, rebuild the visual grammar with native elements whenever possible:

- all audience-facing text;
- shapes, rules, cards, frames, arrows, and masks that the runtime can reproduce reliably;
- charts, tables, exact labels, data marks, and annotations;
- speaker notes, hyperlinks, alt/object names, page furniture, and source lines.

Use raster/vector assets for:

- user-supplied photos and logos;
- licensed/sourced imagery;
- generated illustrative artwork that has passed visual review;
- subtle texture;
- complex silhouette/cutout only when native reconstruction would be unreliable;
- visual details whose fidelity matters more than editability.

### Prohibited shortcuts

- A full generated slide image as the default PPTX background.
- Screenshotting slide copy to match a reference font.
- Rendering exact labels, charts, tables, or data inside a generated image.
- Remote image links in a delivery deck.
- Using a generated person, event, product, or UI as if it were factual proof.

### PPTX-friendly reconstruction patterns

| Reference trait | Native reconstruction route |
|---|---|
| curved split | freeform shape, large partial ellipse, or layered shapes; render-test the silhouette |
| paper/fabric ground | one low-contrast local texture image beneath native content |
| editorial rules | native lines with tokenized stroke and opacity |
| dark footer anchor | native rounded/freeform shape with editable page furniture |
| collage/contact sheet | local images in native frames with controlled crop/contain settings |
| callout/detail label | native text pill/rule positioned outside important crop area |
| shadowed card | native shape with one tokenized subtle shadow; not a screenshot |
| product/UI evidence | local screenshot with native annotation and direct label |

## Generation and media gaps

When image generation is available and the deck is polished, distinctive, portfolio-quality, launch-quality, or reference-matched, run the generation opportunity audit before visual authoring.

- Use generation if a real visual gap remains after supplied/sourced media and native graphics are considered.
- Generate for a named role, crop, safe zone, and slide family—not "an image for the deck." 
- Do not generate factual people, work samples, product UI, charts, labels, or brand marks.
- Inspect each candidate before it becomes a final asset.
- If generation is unavailable, select a deliberate image-light or supplied-media-first direction; do not substitute placeholders.

## Render review: visual parity rather than surface similarity

For a reference-led PPTX, compare the render with the chosen principles:

1. page silhouette and focal mass;
2. type-role contrast and line breaks;
3. material/background depth;
4. edge and overlap discipline;
5. image occupation, crop, and safe copy zones;
6. card restraint and proof scale;
7. family rhythm in the montage;
8. native editability of essential elements;
9. source truth and non-deceptive illustrative media;
10. compatibility in the target office renderer.

Repair the authoring source, not the rendered preview. A candidate with a nice cover but weak body pages does not pass.
