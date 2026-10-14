# Multi-Agent Review

Use this review layer when the host exposes subagents and an independent reading would materially help. It supports deck planning, selected page reviews, and final consistency review without imposing a fixed checkpoint sequence.

## Operating model

The root Agent remains the SlidePoise host Agent and owns the final decision. A reviewer is a bounded, read-only critic. It inspects named artifacts and returns findings. It never edits the run, selects resources, generates an image, or accepts visual quality.

For deck production, a worker may own one isolated slide directory while the parent retains the outline and shared presentation state. Within one slide, keep dependent stages together. Use separate read-only reviewers where an independent reading can expose an omission or mistaken assumption.

## Review checkpoints

### Plan review

Give the reviewer the user request, resolved profile, relevant profile guidance, and draft slide intent. Ask it to find:

- missed or contradicted user instructions
- missing front-half workflow stages such as communication planning, profile resolution, or retrieval
- claims unsupported by the current project
- premature layout restrictions unsupported by the user's requirements or inspected design evidence
- wording that would fail in the intended publication context

The reviewer must distinguish communication structure from visual layout. The initial intent defines hierarchy, relationships, evidence and obligations. A user-specified layout is a requirement. An Agent may develop a composition within the authorised brief after inspecting resources and exploring the visual argument. Check its reasoning and remaining freedom, and keep the selected direction in `style_direction`. Challenge unsupported restrictions without requiring the user to approve routine design choices.

### Style and asset review

Give the reviewer the original request, relevant source materials or project paths, enabled libraries and profile, plus actual page images when available. First ask what identity, evidence or explanatory resources the content warrants. The reviewer should inspect concrete candidates where an omission is plausible and identify pages that benefit from typography or native geometry alone. Then provide the current plan, resource selection and context sheet for comparison. Keep the author's selection reasons and acceptance statements out of the first reading so they cannot define the reviewer's entire scope.

Check both unnecessary assets and missed opportunities supported by the source. Distinguish a user obligation from an Agent proposal. Challenge proposals that prematurely narrow the visual design, including unsupported rejection of an entire resource class. Cite the source asset and the communication role it could serve. Do not recommend icons merely to increase their count. Reuse the existing finding format and revise the existing plan or selection when warranted.

For central named firms or products, check whether the author inspected relevant identity candidates before omitting them. For the composition, ask what the visual helps a cold reader infer beyond the prose. Challenge a familiar table or panel structure when it only mirrors the outline, and retain it when aligned comparison is the explanatory job. Look for meaningful exploration in the actual references, candidate assets and visual alternatives. A populated selection field or attractive typography alone does not establish that work.

### Semantic-map review

Give the reviewer the accepted slide, semantic map, reconstruction handoff, and profile. Ask it to inspect meaningful object coverage, render ownership, intrinsic raster lettering, connector semantics, typography and icon peer groups, canonical asset mappings, and likely reconstruction failure modes.

### Reconstruction review

First give the reviewer the intended audience and actual page image, without the author's intent or explanation. Ask for the meaning they can establish from that page and any context they had to assume. For an unfamiliar journey, this includes the initial need, actor-owned actions and resulting change. Use this first reading to expose missing context before the brief supplies it.

Then give the reviewer the original intent, accepted slide, visual comparison, constructor scene, reconstruction contract and rendered-text evidence. Ask it to identify missing meaning, defects already in the generated design, material visual differences, editability losses, unexplained rasterization, connector defects, text fitting problems, and unsupported patch coordinates. Keep the author's acceptance statements and proposed fixes out of the first reading. The reviewer must open the images and cite visible evidence. Reading the review JSON is insufficient.

### Cross-page visual calibration

Give the reviewer the user requirements, shared deck design, resolved frame and the actual page images together. Generated candidates reveal design drift before reconstruction. Final rendered pages reveal typography and frame drift introduced during construction.

Ask for direct peer comparisons across claim titles, subtitles, supporting text, table headings, data labels and recurring decision treatments. Check font family, apparent size and weight, alignment rhythm, accent meaning, fills and rules. Confirm that generated images exclude the inherited frame and that rendered pages share it. A visually intentional exception needs a communication reason.

The reviewer must identify the specific pages and roles that differ. It must not infer consistency from separate page approvals, a shared Profile name, identical config hashes or aggregate object counts. Mechanical style facts may assist the comparison. The visual judgement remains with the Agent.

## Finding contract

Each finding contains:

- `id`
- `severity` as `material`, `important`, or `minor`
- `criterion`
- `evidence`
- `recommended_action`

The root Agent records one disposition for every material or important finding:

- `accepted` with the resulting revision
- `rejected` with concrete evidence
- `deferred` only when user input or an unavailable dependency is genuinely required

For plan, resources, and semantic mapping, use one independent review followed by one root-Agent correction pass. Do not create an open-ended critic loop. After the correction, the root Agent checks that the cited issues were addressed and continues. If a material disagreement requires a new user decision, stop and ask the user.

Reconstruction is stricter because the released PowerPoint must have no unresolved material visual issue. A reviewer may inspect visual fidelity while another inspects editability, text, connectors, and raster boundaries. Corrections remain focused on concrete findings. After two unsuccessful correction rounds, revisit the relevant upstream artifact. Ask the user only if the remedy changes an agreed requirement or needs an unavailable capability. Repeated failure is a reason to reconsider the approach, not to keep making local adjustments or hand routine debugging to the user.

## Availability fallback

If subagents are unavailable, the root Agent may perform the same checklist in a separate review pass. Lack of subagents never blocks sequential page work or delivery.

## Limits

Multi-Agent review improves coverage. It does not guarantee correctness. Evaluate it against real SlidePoise cases and track whether it catches known failures without producing excessive false alarms.
