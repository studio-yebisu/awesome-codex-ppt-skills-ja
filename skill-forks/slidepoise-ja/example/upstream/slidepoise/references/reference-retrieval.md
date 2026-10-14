# Retrieve references for each slide

Automatically retrieve visual-reference candidates before designing each slide. Search for the communication job and relationships the slide must explain. Shared deck identity provides continuity, while each page needs suitable evidence for its own composition. The host Agent inspects actual pages and owns selection. Retrieval supplies recall and file facts, never an aesthetic verdict.

## Retrieve from intent

Use the page's current intent and resolved configuration.

```bash
python scripts/retrieve_references.py \
  --config work/resolved-config.json \
  --intent work/slide-intent.json \
  --output work/reference-candidates.json \
  --sheet work/reference-candidates.png
```

Paths in this example are relative to a one-slide run. A deck page uses its page-local intent and output paths with the shared resolved config. Resolve configuration before retrieval so the run's selected set and item IDs use the latest shared catalog records. The command indexes only enabled local references and renders a labelled sheet of candidate previews. Whole-set selections include newly registered references. Explicit item subsets exclude unchecked pages. It does not search the web, infer hidden slide meaning from pixels, verify publishers, or choose generation inputs. Use `--catalog` to include a run-local catalog of user or newly retrieved source pages. Keep the index outside the stable skill.

Query from the audience question, communication job, slide role and semantic relationships. Add `--query` when the intent needs useful synonyms. For example, explaining system responsibilities and shared state calls for ownership, layers, dependencies and feedback. A decision page may need options, evaluation criteria and a recommendation. Matching the subject alone will miss useful structures in other industries.

Keep role and relationship metadata meaningful when indexing genuine source pages. Record observations such as a dependency diagram, comparison matrix or evidence-led recommendation after inspecting the page. These are searchable descriptions, not a closed layout taxonomy. Sparse tags, weak matches or an empty result call for a broader query, nearby page inspection or additional suitable sources. Never fill a reference quota with an unrelated page.

The command's lexical recall score, matched terms and matched fields explain search ordering. They do not establish relevance, authenticity or acceptance. The result limit is a browsing convenience. It is not a required reference count or quality threshold.

## Additional catalogs and private files

Relative `path` and `preview_path` values resolve from the catalog directory. By default, previews must stay inside that directory. When a private catalog intentionally points to files elsewhere, declare each allowed directory with `--asset-root`.

```bash
python scripts/retrieve_references.py \
  --config work/resolved-config.json \
  --intent work/slide-intent.json \
  --catalog /private/library/catalog.json \
  --asset-root /private/reference-images \
  --output work/reference-candidates.json \
  --sheet work/reference-candidates.png
```

Keep private catalogs and images outside the repository. Adding a catalog for a run leaves its sources local to that run. When the user requests reusable references, register them in a shared Library Set and select the set or its individual items for the intended profiles using `profile-authoring.md`. Paths, hashes and provenance still pass through the selection checks.

When the user asks to anonymize an internal deck for a private reference library, keep the source separate and make a derived copy. Remove identifying content from editable text, imagery, inherited slide furniture, notes, metadata and embedded documents. Inspect every rendered page and any retained raster diagrams. Placeholder substitution should preserve the relationships and density that make the layout useful. Record the derivative origin and privacy scope in the catalog. Anonymization does not grant redistribution rights. Only the reviewed derivative should enter retrieval or generation inputs. Review it again as a composition in its own right. If removing confidential material leaves empty evidence areas, broken grouping or visibly unbalanced regions, exclude that page from the active library unless the user wants it repaired. Preserving geometry alone does not make a useful visual reference.

An inspected catalog record may set `retrieval_eligible` to `false`, for example for a cover or contact page that remains useful as source context. This host-authored flag excludes it from normal results. Use `--include-ineligible` only when that context is relevant. Eligibility expresses a recorded use decision and does not establish aesthetic quality.

The bundled `pwc-public-references` Library Set provides genuine published sources for this workflow. The `pwc-public` profile selects it by default, and other profiles may also select it. Its complete Strategy& deck supports neighboring-page inspection as well as individual-page retrieval. Private user references remain in external user-owned sets.

## Check source and inspect the page

The default `--authenticity authentic` filter requires recorded non-generated provenance and a source with a page locator. This classification reports catalog metadata. The host still verifies the original document or user-provided file and the selected page. Do not claim independent verification merely because a record passed the filter.

Retain the publisher or creator, source URL or original local file, document title, exact source page, canonical preview path, generated-origin status, and applicable usage or attribution information. Bind the inspected files with hashes in the selection or review record. Preserve original source files when available. A screenshot needs a traceable page or user-provided origin. An image-only source remains an image reference and is never described as an editable component.

Catalog records can carry `id`, `path` or `preview_path`, `name`, `description`, `tags`, `roles`, `layout`, `relationships`, `source` and `source_page`. Retain origin in `provenance`, including `generated_reference`, `source_type`, `source` and `source_page`. Populate these fields from known source facts. Do not set `generated_reference` to `false` merely to make a record eligible. Additional source metadata stays with the record.

Inspect the retrieval sheet to compare possibilities, then open promising pages at a useful resolution. Check their reading order, hierarchy, relationships, evidence presentation and content density against this page's job. Read neighboring pages when the visual depends on deck context. Generic descriptions and thumbnails cannot replace this inspection. Verify any requested publisher or source family through its actual origin, not its visual resemblance or filename.

Distinguish published or user-authored source material from generated examples. Preserve generated provenance through copies, reimports, renaming and profile inheritance. A generic label such as `user_or_agent_added` does not establish authentic origin. Unknown provenance stays unknown until verified. Generated examples are eligible only when the user or active direction permits them as such. They cannot substitute for a request for genuine source slides. `--authenticity exclude-generated` retains unknown records for investigation. `--authenticity any` also exposes generated examples. Neither option grants permission to select an unsuitable source.

## Select for a stated purpose

Keep retrieval results in `work/reference-candidates.json`. They are a candidate pool, separate from the host-authored `selected_visual_references` in the resource draft. Select only pages whose useful role can be explained from inspection. No fixed number or one-reference-per-layout rule applies.

Copy the result's `reference_retrieval` block unchanged into the resource draft alongside your selected references. It records `selection_mode: host_selected`, the authenticity policy, exclusions and source catalogs. The compiler uses this block to preserve host selection, suppress automatic profile-reference additions and check selected references against the same source restrictions. It never promotes retrieved candidates into selected references.

For each selection, retain its qualified `resource_id`, canonical file and provenance, then write a concrete reason that covers

- the communication job it helps this page perform
- the observed treatment to borrow, such as separating responsibilities from a shared dependency
- incidental content or geometry that should not transfer, such as source claims, category count or brand palette

Record candidate IDs considered, files inspected and the selection rationale in a page-local reference review. Reusing the same page across slides is valid when each use has a defensible purpose. Repeating a generic rationale about clarity, colour or typography does not explain that purpose. One reference may inform shared identity while another informs a page-specific relationship. Keep those roles explicit.

Pass only selected visual references to the generation context. Use `full_resolution_attachment` when a selected page's fine detail matters. Review the prepared resource manifest and compiled attachment list so no unselected candidate, disallowed profile default or rejected source slips in. A useful authentic source may inform composition without authorizing reuse of its logo, factual claims, data or exact artwork. Import facts only through the slide's separate evidence and source obligations.

## Respect rejection and changed direction

Record user rejection with its stated scope and reason in the run. An individual page, a source family and an entire visual direction are different scopes. Preserve the user's decision across agents and later turns. Apply exclusions before retrieving and selecting again, including known copied files or renamed IDs. Do not remove unrelated references without a reason.

Pass repeatable `--exclude-id` arguments for individual IDs or `--exclusions work/reference-exclusions.json` for recorded exclusions. The JSON fields are `ids`, `canonical_paths`, `sha256`, `source_families` and `source_types`. Use the known identities that match the user's stated scope and retain a human-readable reason in the run's decision record. These filters preserve a decision already made by the user or host. They do not judge visual quality.

When the user rejects generated references or asks for a genuine publisher's work, exclude the rejected source family and its derived guidance from subsequent generation. Review shared design prose, inherited reference priorities, always-attached defaults, context sheets and compiled prompts as well as the image list. Re-resolve session settings and recompile affected requests. Preserve the rejected pass for traceability and keep useful factual research separately available.

This is a correction to the current run unless the user asks to evolve a persistent profile. Removing a resource from one profile changes that profile's selection and preserves the shared asset for other profiles. Do not silently delete shared assets or promote a temporary user upload into the permanent library. An empty eligible candidate set calls for honest further retrieval or a stated source limitation. It never justifies recycling a rejected reference.
