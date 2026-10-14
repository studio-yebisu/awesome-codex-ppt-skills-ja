# Capability-aware orchestration

PradaSlides must fit the actual host. A strong workflow is not the same thing as pretending every agent has vision, image generation, video generation, PowerPoint authoring, or a renderer.

## First principle

Separate three layers:

1. **Model cognition** — text reasoning, image understanding, and video understanding.
2. **Creative services** — image generation/editing, video generation, search, OCR, and transcription. These may be built into one model or exposed as separate tools/models.
3. **Production runtime** — code execution, filesystem access, PPTX/web authoring, rendering, export, and round-trip inspection.

Record verified availability in `capability-profile.json`. `unknown` is not `available`. A capability with status `delegated` is usable only when `separate_tools_allowed` is true and a concrete provider/handoff exists.

Run:

```bash
python scripts/resolve_capabilities.py --profile <project-dir>/capability-profile.json --brief <project-dir>/brief.json --scan-local --output <project-dir>/execution-plan.json
```

The execution plan is a routing decision, not a claim that the tools are fit. Test important constraints such as slide notes, editable charts, video codecs, fonts, and rendering.

## Operating modes

| Mode | What is available | Media behavior | Acceptable delivery |
|---|---|---|---|
| `text-only` | text reasoning only | use supplied descriptions/filenames; ask for semantic clarification when placement changes meaning | strategy, copy, deck plan; artifact only if an independent authoring and QA route exists |
| `text-plus-vision` | text reasoning + image understanding | inspect supplied images and video keyframes; use native diagrams or supplied assets | full content/media planning; no invented imagery |
| `text-plus-generation` | text + image/video generation but no visual understanding | generation is unverified; require user/external vision approval before critical use | draft assets with explicit review gate |
| `multimodal` | text + vision, optionally image/video generation | inspect inputs, perform a generation-opportunity audit, create useful original visuals, inspect outputs, repair | full workflow when production runtime also exists |
| `orchestrated-multimodel` | capabilities live in separate models/tools | use explicit handoff packets and stable file artifacts | full workflow if every critical handoff has validation and fallback |

Do not equate a multimodal model with a slide runtime. A model may understand and generate images but still lack filesystem, PPTX authoring, or rendering.

## Creative activation rule

Capability detection must change the plan. If image or video generation is usable, first honor the user's generation preference, then read `generative-visuals.md` and resolve an internal `use`, `skip`, `unavailable`, or `delegated` decision before authoring. Persist it as `visual-generation-plan.json` only when planning artifacts are enabled. Do not leave generation as a passive option.

- Default to at least one original image candidate when the user requests a polished, distinctive, visual, launch-quality, portfolio-quality, or reference-matched deck and supplied media does not already perform the needed hero/concept job.
- Generate for a named communication job, slide, topology, crop, and text-safe zone.
- Keep actual logos, people, UI, data, charts, and proof sourced or native.
- Use each final generated hero once by default; generate a different asset for a different narrative job.
- Record a concrete reason when generation is skipped despite being available.
- Inspect generated outputs with vision. If vision is unavailable, keep them out of the final artifact until an external reviewer approves them.

## Capability fallbacks

### No image understanding

- Run technical asset inventory, but label semantic fields `pending`.
- Use filenames, dimensions, alpha, and user-provided captions only as hints.
- Do not infer identity, emotion, sensitive content, focal point, rights, or message from metadata.
- Ask for a contact-sheet review or asset captions only when the answer changes the outline or placement.
- Do not mark `asset-manifest.json` reviewed without a human or vision-capable reviewer.

### No video understanding

- If keyframe extraction and image understanding are available, inspect representative frames and label the review `keyframe-only`.
- Obtain transcript/captions when spoken content matters.
- Do not claim motion, timing, or audio quality was reviewed from still frames.
- If neither video nor image understanding is available, use user-supplied summary and provide a static poster/fallback.

### No image generation

- Prefer supplied media, licensed search when permitted, native shapes, charts, diagrams, typography, or intentionally image-free layouts.
- Never insert a blank decorative image slot merely because a template expects one.
- Do not substitute an unrelated stock image for evidence.

### Image generation available

- Run the opportunity audit; do not equate availability with optional inaction.
- Generate a small candidate set tied to the deck plan and design system.
- Save the final asset in the project and add it to `asset-manifest.json` with generated provenance and a non-evidence semantic role.
- Verify distinctness, crop safety, artifacts, factual implication, brand fit, and target-runtime rendering.
- Keep exact copy, logos, UI, diagrams, charts, and labels out of the generated bitmap.

### Generation without vision

- Send a precise generation packet, save prompt/model/seed or equivalent provenance, and mark the result `needs-visual-review`.
- Do not use generated content for exact charts, logos, UI screenshots, legal/medical evidence, or core slide copy.
- Require a vision-capable model or user to check prompt adherence, artifacts, text errors, brand risk, and suitability before final placement.

### No code execution or filesystem

- Produce a complete deck plan, slide copy, media plan, and renderer instructions in the response or supported document surface.
- Do not promise an editable PPTX.
- If a native presentation connector exists, treat it as the authoring runtime and verify its export/preview capabilities separately.

### No slide renderer

- Structural/package inspection is still useful but cannot replace visual QA.
- Deliver as a draft with a blocking external render-review gate, or choose `plan-only` when final-quality artifact creation cannot be verified.
- Never say every slide was visually inspected.

## Handoff packet for separate models/tools

Every delegated creative operation should carry:

```json
{
  "operation_id": "IMG-P04-01",
  "capability": "image_generation",
  "provider": "declared tool or model",
  "purpose": "What communication job this asset performs",
  "inputs": ["brief.json", "deck-plan.json#P04", "asset-manifest.json#A02"],
  "prompt": "Provider-ready instruction without unsupported assumptions",
  "constraints": ["16:9", "no rendered text", "brand-safe"],
  "expected_output": "assets/generated/P04-hero.png",
  "acceptance_checks": ["prompt adherence", "safe crop", "no text artifacts"],
  "fallback": "native diagram",
  "provenance": {"model": null, "version": null, "seed": null, "created_at": null},
  "status": "planned"
}
```

The authoring agent remains responsible for the deck. A delegated model owns only its declared output.

## Capability-to-workflow matrix

| Task | Minimum capability | Stronger route | Required fallback |
|---|---|---|---|
| understand a photo/logo/screenshot | image understanding or human caption | image understanding + contact sheet | pending semantic review |
| understand a video | video understanding | keyframes + transcript + video understanding | poster and user summary |
| create a hero image | image generation | generation + vision QA | native visual or licensed asset |
| create a diagram/chart | text reasoning + native shapes/chart runtime | code + editable vector output | detailed visual specification |
| create PPTX | native PPTX authoring | authoring + PowerPoint round-trip | web/PDF/plan route disclosed |
| final visual QA | slide rendering + image understanding | independent renderers + montage | external review gate |

## Honesty rules

- State what was inspected versus inferred.
- State whether media was understood directly, through keyframes/transcripts, or from user captions.
- State whether generated assets were visually reviewed.
- State whether generation was used, skipped with reason, unavailable, or delegated.
- State whether PPTX editability and round-trip behavior were tested.
- A fallback changes the delivery claim; reflect it in `qa-report.json` and the final handoff.
