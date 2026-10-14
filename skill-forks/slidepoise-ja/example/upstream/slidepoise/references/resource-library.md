# Shared resources and current-chat assets

During a run, retrieve visual references for every slide using `scripts/retrieve_references.py --config work/resolved-config.json --intent work/slide-intent.json --output work/reference-candidates.json --sheet work/reference-candidates.png`. Read `reference-retrieval.md` for the indexed search, provenance checks and host selection workflow. This is the default resource step and needs no separate user request.

For general catalog browsing, use `scripts/list_library.py --config work/resolved-config.json --query "keywords"`. This reads the profile's current selected sets and items, session overrides and provider switches used by generation. Resolve configuration before retrieval and again after resource or selection changes so selected IDs refer to current catalog records. Use `--profile <profile_id>` only to browse a shared profile outside a run. Filtering reduces recall only. The host Agent chooses by semantic and visual fit.

## Sources
- `<library-sets-root>/catalog.json` defines shared sets for `visual_references`, `icons` and `components`. Each local set owns its catalog and source files. Profiles own no resource copies.
- A profile's `library_sets` selects sets by kind. Optional `library_items[kind][set_id]` lists the selected item IDs. An absent item selection includes all current and future items in that set. An empty list selects no items. Different profiles can select different subsets of the same set.
- A catalog's item ID stays stable. Use its qualified `resource_id`, formed as `<set-id>:<item-id>`, in downstream selections and reference priorities. Record canonical paths and hashes alongside that ID when binding inspected files.
- Visual references provide style and communication precedents. Never copy their factual content by default. Selecting them grants no additional icon, logo or source-artwork permissions. Select icon and component sets independently.
- Current-chat/user files and supplied project materials contain exact images, icons, logos, screenshots and other subject-specific assets. Inspect relevant source directories or documents before reaching for remote substitutes. A reusable Profile supplies a style and available libraries, not an inventory of the subject being presented.

## Profile-aware selection
Read `resolved_profile.visual_reference_priorities` after config resolution. Only currently selected resources are eligible. A priority cannot re-enable an unchecked item or set. Treat priorities as candidates to inspect alongside references retrieved for the current communication job. Inspect the exact user-supplied reference first when the user names it as the desired direction. Preserve its origin and the intended use. Select references for identifiable jobs such as explaining a dependency, comparing alternatives or showing how evidence supports a decision. Record the observed treatment to borrow and the incidental facts or geometry to leave behind. A visual reference teaches visual language. Semantic intent and user content still determine composition.

The host Agent selects resources by semantic role, visual fit, profile compatibility, identity requirements, and downstream reconstruction value. Do not turn selection into a numeric relevance winner. Respect configured budgets; user-required assets are exempt from the optional-asset cap.

Treat resource selection as part of communication design. Inspect the slide's claims, comparisons, actors, stages, decisions and recurring concepts before deciding that text and geometry are sufficient. A useful icon can make a role or action faster to recognize. A reusable component can carry a familiar information structure. An exact asset can preserve identity. Avoid decoration that adds no meaning.

Record the comparison in the existing `selection_reasoning` field after inspecting candidates. Identify actual files or catalog items and their potential communication roles. A provider name establishes availability only. State why a candidate helps or does not help this page. Do not copy a generic rejection across pages or treat an empty list as evidence that retrieval was unnecessary. Shared choices can be reused where their purpose is shared. A Profile that favours restraint does not prohibit useful imagery.

Keep user requirements in `user_required_assets` and mark selected assets with `user_required` when the user actually requires them. Use `required_for_slide` for an Agent-selected asset that the current design depends on, and `require_exact_identity` when its identity must be preserved. Other selected assets form an optional candidate pool. Put the artwork's intended use in `generation_description`. Keep deliberation and rejected alternatives in `selection_reasoning`, which stays in the host contract and is excluded from the image prompt. Do not move tentative rejections into `avoid`, profile hard rules or user requirements.

Reconsider selection when a generated design reveals a useful visual role or a review exposes missing identity or evidence. An unselected pictogram may suggest a role worth filling with a canonical asset. Evaluate its purpose, retrieve a suitable original when useful, then update the selection and recompile. Remove meaningless graphics after considering their role. Preserve explicit exclusions and closed asset policies. If a Library Set is disabled by a session override, respect that boundary and revisit the setting only within the user's authority.

Exact user-required assets override packaged alternatives. Brand identity requires an exact asset; never substitute a generic icon for a missing logo.

## Research identity and explanatory assets

When named organizations or products are central to a comparison, precedent, ecosystem or example, assess whether recognizable identity would help the reader locate and connect the evidence. When it would, search the enabled Wikimedia or official sources, inspect actual logo candidates and select an appropriate exact mark. A user request for logos where useful calls for this active consideration on the relevant pages. A plain-text treatment remains valid when it communicates better, the mention is incidental or a specific usage restriction applies.

Apply the same initiative to subject-specific evidence and explanatory assets, including product views, physical objects and useful icons. Inspect supplied materials first, then use the relevant available sources. Do not stop at an empty local catalog when remote retrieval is enabled and a useful role remains unresolved.

Record concrete candidate files or source pages and the communication decision under `selection_reasoning`, using a field such as `identity_assets`. A promise to search, an enabled provider or a generic statement that logos are unnecessary is not candidate inspection. Keep a retrieval failure distinct from a visual decision. Try a relevant alternative source when reasonable, and state a genuine limitation accurately.

Use each selected logo as an identity cue with the adjacent evidence or actor it identifies. Preserve its canonical proportions and colours unless an authorised variant is available. Distinguish product identity from parent-company identity. Keep the claim's scope explicit so a source citation cannot be mistaken for a partner badge or endorsement. Do not place every logo in a disconnected row simply to show that assets were used.

An Agent's preference for restraint, a concern about endorsement or a restriction on one asset does not justify a blanket ban on brand marks. Trace actual restrictions to the user or source, evaluate their scope and keep unrelated choices open. There is no logo quota and no requirement to illustrate incidental names.

## Generation context sheet
After retrieval, the selected resource pool is consolidated into `work/generation-context-sheet.png` with `scripts/prepare_resource_context.py`.

Include:
- selected visual/style references;
- selected component previews;
- useful retrieved/packaged icon/image candidates;
- relevant user/current-chat uploads.

Show actual artwork. SVGs must be rendered to real previews; do not display an `SVG` placeholder.

The same sheet can be shown to the user when a style checkpoint would help and is passed to the image model. This keeps the visual direction and resource vocabulary consistent.

For each selected current-chat/exact identity asset:
1. inspect dimensions/aspect ratio when possible;
2. record exact canonical path and intrinsic ratio;
3. author a concise `generation_description`;
4. include it in the context sheet;
5. treat the generated depiction as composition guidance, not the canonical asset;
6. restore the exact file downstream using aspect-preserving contain-fit by default.

If a generated slot is materially incompatible with the canonical asset ratio, revise the upstream composition. Never stretch the asset to fill it.

## Novel illustrations versus known assets
A profile may allow model-generated illustrations even when known reusable assets use a controlled vocabulary. Exact logos, required project icons and supplied user images retain their authentic identity. Generic explanatory symbols have no equivalent identity restriction merely because they are absent from the current catalog.

- Known and reusable visual identity comes from the selected resource pool.
- Novel illustrations are allowed only according to the active profile's `novel_illustrations` guidance and the slide's communication role.
- Novel illustrations must be semantically classified downstream and may enter the optional refinement branch.

## Icons
Use the existing `icon` / `icon_slot` path for icons and pictograms alike. Prefer profile-approved packaged icons when available. The logical icon slot is separate from any optional visible background surface. A generation-only localization boundary is scaffolding, not a reconstructable decorative box.

When a generated design introduces a useful generic symbol, treat it as a retrieval lead. Search Remix Icon for the same meaning and a compatible silhouette before rejecting the composition or removing the visual. Inspect the candidates at the actual slot size beside the surrounding type and rules. Record the chosen canonical asset and any visible difference. Exact brand identity continues to require an authentic source. If no library match preserves the meaning and treatment, use a suitable original crop, a simple native diagram shape or a permitted novel illustration. Read `raster-composition.md` and `illustration-refinement.md` to preserve or improve the artwork, including actual transparent output when useful. Do not replace a distinctive explanatory visual with a weak library match solely to keep every internal stroke editable.

Choose a Remix variant that suits the slide's visual language. Apparent weight depends on viewBox, painted bounds, stroke width, slot size and neighbouring type. Compare real SVGs in the PowerPoint render. Remix outline icons use filled paths. Adjust their apparent weight through canonical variant, symbol choice, scale and surrounding typography. Preserve their geometry and a coherent treatment among peers.

## Remote sets
Check `resolved_config.library_sets.selected` and `resolved_config.remote_sources` before any remote query. Remix Icon and Wikimedia identity assets are remote Library Sets. Selecting a set makes its provider available. A session may override the profile's current set selection without changing the profile. Profiles still govern visual treatment and appropriate use.

When the user requests a temporary source change, update that run's `library_sets` override and resolve the config again. Change the profile's selected sets only when the user wants the choice to recur. Trace which slides use the changed source and revise only those whose inputs changed.

- Remix Icon supplies a consistent line/fill family. Fetch an official pair with `scripts/fetch_remix_icon_pair.py --config work/resolved-config.json`, keep both candidates in the run cache with provenance, and include both on the resource context sheet. Read `icon-variants.md` before choosing the post-generation reconstruction variant.
- Wikimedia Commons is the structured candidate source for exact logos and public media. Use `scripts/search_wikimedia_commons.py`, inspect the exact file page, then use `scripts/fetch_wikimedia_commons_asset.py` only after verifying identity, source, author, license, attribution, and trademark constraints. Commons availability does not itself grant trademark permission.

An official organization site or brand portal remains a valid exact-logo source when the active profile allows it. The Agent chooses an exact official HTTPS asset and records usage terms with `scripts/fetch_remote_asset.py`. Keep copyright provenance and trademark guidance distinct. Resolve an uncertain candidate through another suitable source or an accurate text treatment, and continue independent work. Ask only when an unresolved asset constraint prevents a material user requirement. When the user requests persistent reuse, follow `profile-authoring.md` to register the asset in a shared set and select it for the intended profiles.

## Components
Components provide design grammar without fixing the layout. Select one only when it is structurally useful, carry `component_id` + reason, pass the focused preview through the context sheet, and adapt its sample content, counts and dimensions to the slide. Assign `component_id` downstream only when the accepted target actually uses that grammar.

Imported PPTX components retain their native source and selected page. Resource preparation renders a current preview of that page when needed. If the local renderer is unavailable, use the host's native renderer and supply the matching preview before generation. Image-only precedents remain image-only. Never describe them as editable PowerPoint components.

Reuse stored previews when their binding matches the native source hash, selected page and preview hash. Render again after a source or page change. Carry that source binding into the generation resources. Supported chart and table components provide constructor defaults for native reconstruction. Adapt those defaults to the accepted design and real data. Other imported pages provide native object precedents for semantic reconstruction. A preview alone does not define an arbitrary PowerPoint component emitter.
