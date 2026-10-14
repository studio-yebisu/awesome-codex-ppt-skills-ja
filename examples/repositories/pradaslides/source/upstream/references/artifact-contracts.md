# Artifact contracts

These JSON files are an optional, durable renderer-neutral representation. Use them when the user requests planning artifacts, the work is collaborative or resumable, traceability is high-stakes, or the selected tooling needs file-backed contracts. For ordinary one-shot work, keep the same fields as an internal working model and do not emit the files.

The logical production chain always remains:

`brief → source ledger + asset manifest → capability route → design system + layout manifest → deck plan + visual-generation decision → authoring source → previews → QA → exports`

The chain describes reasoning ownership, not mandatory filesystem output. Materializing one contract does not require publishing it to the user.

## `capability-profile.json` and `execution-plan.json`

`capability-profile.json` declares verified model, tool, and runtime capabilities. Each entry uses `available`, `unavailable`, `unknown`, or `delegated`. A delegated capability requires a named provider and permission to use separate tools. Run `scripts/resolve_capabilities.py` to produce `execution-plan.json`, which owns the selected operating mode, artifact route, media fallbacks, QA route, warnings, and blocking external gates.

Keep environment capability separate from user intent. Do not put model availability in `brief.json`, and do not mutate the brief when tools change.

`execution-plan.json` includes a `creative_route`. When generation is usable it requires an opportunity audit and recommends intent-fit visual jobs, a small candidate budget, a distinctness rule, and a visual-review route. Resolve the actual creative choice in `visual-generation-plan.json`.

## `brief.json`

Required top-level fields:

```json
{
  "schema_version": "1.0",
  "project": "Example deck",
  "task_mode": "new",
  "primary_intent": "business-proposal",
  "secondary_intent": null,
  "audience": {
    "who": "Operations leadership",
    "context": "Decision meeting",
    "prior_state": "Concerned about cycle time but unsure of the cause",
    "desired_state": "Aligned on a 90-day pilot",
    "decision_authority": "COO",
    "objections": ["Implementation disruption", "Data quality"]
  },
  "communication_job": "By the end, operations leadership should approve a 90-day pilot because the proposed workflow addresses the two verified bottlenecks with bounded implementation risk.",
  "central_takeaway": "A bounded pilot can reduce the two largest delays without a full-system replacement.",
  "final_action": "Approve pilot scope, owner, and start date",
  "delivery": {
    "mode": "hybrid",
    "duration_minutes": 20,
    "slide_count_target": 12,
    "aspect_ratio": "16:9",
    "language": "en",
    "output_formats": ["pptx", "pdf"],
    "editability": "native-preferred"
  },
  "brand": {
    "status": "none",
    "assets": [],
    "constraints": []
  },
  "source_policy": {
    "research_allowed": true,
    "citations": "visible-for-key-claims",
    "confidentiality": "internal"
  },
  "invariants": [],
  "assumptions": [],
  "open_questions": []
}
```

Allowed `task_mode`: `new`, `redesign`, `fill-template`, `enhance-existing`, `critique`, `plan-only`.

Allowed `primary_intent`: `portfolio`, `work-results`, `business-proposal`, `sales`, `investor-pitch`, `strategy-decision`, `research-technical`, `teaching-workshop`, `keynote-launch`, `report-async`, `template-system`.

Allowed `delivery.mode`: `speaking`, `hybrid`, `reading`.

## `design-system.json`

`design-system.json` owns the visual direction and quality floor independently of any one renderer. Required groups:

- `direction`: communication mode, visual cluster, 3–5 behavioral character terms, reference principles, and avoid list;
- `art_direction`: visual thesis, selected reference scope and anti-copy rule, material language, edge language, image roles/treatments/reuse policy, native-versus-raster strategy, and 3–8 slide families;
- `canvas`: fixed dimensions, safe margin, columns, gutter, and baseline;
- `typography`: display/body/mono families, fallback policy, type scale, line budgets, and a product-specific `selection` rationale based on archetype, positioning, audience, personality, proof density, and interaction model;
- `color`: semantic colors and light/dark/accent tone palettes;
- `furniture`: default/optional wayfinding elements and motif limit;
- `rhythm`: topology variety, repetition limits, tone shifts, and card-grid limit;
- `quality_floor`: thumbnail, squint, evidence scale, contrast, copy fit, reference floor, and target-runtime checks.

Validate with `scripts/validate_design_system.py`.

## `layout-manifest.json`

`layout-manifest.json` separates relational topology from style. It contains:

- topologies such as `stage`, `split`, `spine`, `axis`, `matrix`, `stack`, `network`, `mosaic`, `field`, and `frame`;
- layouts that declare compatible roles/relationships, required and optional slots, media/item capacity, density, tones, fidelity, and guardrails.

Use a known `layout_id` in the deck plan. A `custom-*` layout is allowed only with `layout_rationale`. Validate the registry with `scripts/validate_layout_manifest.py`.

## `source-ledger.json`

```json
{
  "schema_version": "1.0",
  "sources": [
    {
      "id": "S01",
      "kind": "supplied-file",
      "title": "Quarterly operations report",
      "uri_or_path": "sources/operations-q2.pdf",
      "publisher_or_owner": "Operations",
      "date": "2026-06-30",
      "retrieved": null,
      "location": "p. 14",
      "supports": ["C03"],
      "status": "verified",
      "license_or_permission": "internal",
      "notes": "Cycle-time definition excludes rework"
    }
  ],
  "claims": [
    {
      "id": "C03",
      "text": "Two approval queues account for most observed delay.",
      "class": "supplied-fact",
      "source_ids": ["S01"],
      "status": "verified",
      "slide_ids": ["P04"]
    }
  ]
}
```

Allowed claim `class`: `supplied-fact`, `external-fact`, `calculation`, `judgment`, `assumption`, `scenario`, `quote`.

Allowed status: `verified`, `needs-check`, `scenario`, `excluded`, `confidential`.

## `asset-manifest.json`

`scripts/analyze_assets.py` writes the technical fields. The agent must fill the semantic and placement fields after viewing the assets or video keyframes.

```json
{
  "schema_version": "1.0",
  "root": "assets",
  "assets": [
    {
      "id": "A01",
      "path": "assets/product-demo.mp4",
      "kind": "video",
      "sha256": "...",
      "bytes": 12345678,
      "duplicate_of": null,
      "technical": {
        "width": 1920,
        "height": 1080,
        "aspect": 1.7778,
        "orientation": "landscape",
        "duration_seconds": 28.4,
        "video_codec": "h264",
        "audio_codec": "aac",
        "keyframes": [
          "previews/video-keyframes/A01-start.jpg",
          "previews/video-keyframes/A01-middle.jpg",
          "previews/video-keyframes/A01-end.jpg"
        ]
      },
      "semantic": {
        "role": "video-demo",
        "subject": "Checkout prototype",
        "message": "The complete checkout now takes three visible steps",
        "focal_point": "center",
        "text_safe_regions": [],
        "crop_tolerance": "none",
        "rights": "owned",
        "sensitivity": "internal prototype",
        "alt_text": "Prototype walkthrough of the three-step checkout"
      },
      "placement": {
        "recommended": "embedded demo with poster frame and static fallback",
        "avoid": ["autoplay with sound", "cropping interface labels"],
        "journey_phases": ["proof", "resolution"],
        "slide_candidates": ["P07"]
      }
    }
  ]
}
```

## `deck-plan.json`

```json
{
  "schema_version": "1.1",
  "project": "Example deck",
  "communication_job": "By the end, operations leadership should approve a 90-day pilot because the proposed workflow addresses the two verified bottlenecks with bounded implementation risk.",
  "design_direction": {
    "name": "Measured operational clarity",
    "communication_mode": "hybrid",
    "visual_cluster": "corporate-editorial",
    "character": ["precise", "calm", "credible"],
    "grid": "12-column with 0.55-inch outer margins",
    "type": "Large claim titles, neutral sans body, tabular numerals",
    "palette": "Warm white, charcoal, cobalt evidence accent, amber risk accent",
    "media": "Real process screenshots, one original conceptual hero, native diagrams, restrained charts",
    "topology_rhythm": "stage → axis → split → frame → spine → matrix → stage; two intentional tone shifts",
    "reference_quality_floor": "Decisive scale contrast, inspectable proof, varied silhouettes, and coherent dark/light rhythm"
  },
  "slides": [
    {
      "id": "P01",
      "role": "cover",
      "journey_phase": "orientation",
      "job": "Frame the decision",
      "audience_question": "What are we deciding today?",
      "title": "A 90-day path to remove the two largest approval delays",
      "claim": null,
      "evidence_ids": [],
      "visual_role": "Establish operational context",
      "visual_form": "Full-bleed process detail with title safe zone",
      "layout_family": "cover-hero",
      "layout_id": "hero-decision",
      "topology": "stage",
      "tone": "dark",
      "emphasis": "decision headline",
      "slot_budget": {
        "headline_lines": 2,
        "body_words": 0,
        "peer_items": 3,
        "media": 1
      },
      "density": "speaking",
      "transition": "First, quantify where time is actually lost.",
      "speaker_notes_purpose": "Set scope and decision deadline",
      "source_ids": [],
      "asset_ids": [],
      "media_plan": null
    },
    {
      "id": "P02",
      "role": "content",
      "journey_phase": "tension",
      "job": "Quantify the bottleneck",
      "audience_question": "Where is cycle time being lost?",
      "title": "Two approval queues create 63% of measured waiting time",
      "claim": "Two approval queues create 63% of measured waiting time.",
      "evidence_ids": ["C03"],
      "visual_role": "Compare delay contribution",
      "visual_form": "Sorted horizontal bars with two queues highlighted",
      "layout_family": "chart-led",
      "layout_id": "ranked-evidence-axis",
      "topology": "axis",
      "tone": "light",
      "emphasis": "two highlighted queues",
      "slot_budget": {
        "headline_lines": 2,
        "body_words": 18,
        "peer_items": 6,
        "media": 0
      },
      "density": "hybrid",
      "transition": "The delay is concentrated enough for a bounded intervention.",
      "speaker_notes_purpose": "Explain measurement window and exclusions",
      "source_ids": ["S01"],
      "asset_ids": [],
      "media_plan": null
    }
  ]
}
```

Allowed slide `role`: `cover`, `section`, `content`, `pause`, `closing`, `appendix`.

Allowed `journey_phase`: `attention`, `orientation`, `tension`, `insight`, `proof`, `resolution`, `decision`, `retention`.

Every `content` slide requires non-empty `claim`, `evidence_ids`, `visual_role`, `visual_form`, and `transition`. Every slide using the default manifest requires `layout_id`, `topology`, `tone`, `emphasis`, and `slot_budget`. `evidence_ids` may contain a judgment/assumption claim ID, but the source ledger must make its class explicit.

Every slide with `asset_ids` requires a resolved `media_plan`. Under strict visual validation, slides with multiple assets also require `media_plan.asset_treatments`: one object per used asset with `asset_id`, `treatment`, `placement`, `crop_mode`, `focal_anchor`, `text_safe_region`, `fallback`, and `alt_text`. Per-asset treatment prevents a logo, hero, screenshot, and video from accidentally inheriting the same crop or fallback behavior. Logos and assets with `crop_tolerance: none` accept only `contain` or `none` crop modes.

## `visual-generation-plan.json`

This artifact proves that generation capability was activated or consciously declined.

```json
{
  "schema_version": "1.0",
  "capability_status": "available",
  "decision": "use",
  "decision_reason": "A custom cover hero will express orchestration without pretending to be operational evidence.",
  "budget": {
    "image_candidates": 2,
    "final_unique_images": 1,
    "video_candidates": 0
  },
  "operations": [
    {
      "id": "IMG-P01-01",
      "slide_ids": ["P01"],
      "purpose": "Create a distinctive cover entry",
      "use_case": "stylized-concept",
      "asset_type": "full-bleed cover hero",
      "narrative_job": "turn fragmented handoffs into one controlled path",
      "composition": "16:9; calm left text-safe field; focal object on right",
      "difference_from_other_visuals": "Conceptual hero; later slides use native evidence and supplied UI",
      "prompt": "Provider-ready prompt",
      "constraints": ["no text", "no logo", "no UI", "brand-safe"],
      "avoid": ["stock office", "flowchart boxes", "sci-fi neon"],
      "expected_output": "assets/generated/P01-orchestration-hero.png",
      "review": {
        "required": true,
        "reviewer": "vision-capable current agent",
        "checks": ["prompt adherence", "crop", "artifacts", "distinctness", "brand fit"]
      },
      "fallback": "typographic hero with native process motif",
      "provenance": {
        "provider": "declared image tool",
        "model": null,
        "created_at": null,
        "prompt_saved": true
      },
      "status": "planned"
    }
  ]
}
```

Allowed `decision`: `pending`, `use`, `skip`, `unavailable`, `delegated`. `pending` is invalid when authoring begins. Every final generated asset must also appear in `asset-manifest.json` with generated provenance and reviewed semantic placement.

## `reference-benchmark.json`

This artifact owns the reference-relative quality verdict for a rendered candidate. It records the target runtime, the selected or floor-only role of every supplied reference, the transferable principle and anti-copy constraint, twelve universal craft criteria, render evidence, blockers, and repair history.

Scores are invalid without a rationale and evidence path. `status: final` requires all universal criteria at or above their declared floors, every applicable criterion marked `pass`, a slide montage and console capture, and an empty blocker list. Use `not-applicable` only for reference-specific style relevance; it cannot exempt a universal criterion.

```bash
python scripts/validate_reference_benchmark.py <project-dir>/reference-benchmark.json --require-final
```

## `qa-report.json`

```json
{
  "schema_version": "1.0",
  "artifact": "exports/example-deck.pptx",
  "generated_at": "2026-07-22T12:00:00Z",
  "checks": [
    {
      "id": "render-all-slides",
      "category": "visual",
      "status": "passed",
      "evidence": "previews/montage.png and previews/slides/",
      "notes": "All 12 slides inspected at full resolution"
    }
  ],
  "issues": [
    {
      "slide_id": "P06",
      "severity": "minor",
      "category": "alignment",
      "observation": "Source line sits 4 px above footer baseline",
      "repair": "Aligned source to global footer token",
      "status": "closed"
    }
  ],
  "summary": {
    "blocking_open": 0,
    "major_open": 0,
    "minor_open": 0,
    "verdict": "passed"
  }
}
```

## Ownership

| Artifact | Owns | Does not own |
|---|---|---|
| `capability-profile.json` | verified availability and provider of model/tool/runtime capabilities | user intent or slide content |
| `execution-plan.json` | capability-derived route, handoff policy, fallbacks, and external gates | actual QA verdict |
| `brief.json` | user intent, constraints, assumptions, invariants | slide copy or layout |
| `source-ledger.json` | provenance and claim class | narrative order or geometry |
| `asset-manifest.json` | media identity, technical facts, semantic role, rights, and placement constraints | slide argument or final geometry |
| `design-system.json` | visual direction, art-direction tokens, image system, rhythm, furniture, native/raster policy, and quality floor | slide-specific claim or final coordinates |
| `layout-manifest.json` | relational topologies, reusable layouts, slots, limits, and fidelity | which layout a specific slide must use |
| `visual-generation-plan.json` | generation decision, operations, prompts, uniqueness, provenance, and review | factual proof or final slide placement |
| `deck-plan.json` | audience journey, slide jobs, claims, topology/layout choice, visual intent | final geometry |
| authoring source | final visible composition and editable objects | factual provenance |
| rendered previews | visual evidence for QA | editable source |
| `reference-benchmark.json` | reference mapping, evidence-backed craft scores, floor failures, and repair history | visual source, copied layout, or authoring geometry |
| `qa-report.json` | checks, issues, repairs, verdict | the fixes themselves |

When artifacts disagree, repair the downstream artifact from its owner. Do not copy a derived fact into a second source of truth.
