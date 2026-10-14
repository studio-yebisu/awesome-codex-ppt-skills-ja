# Maintaining SlidePoise

Use this workflow only when the user explicitly asks to modify the framework, stable skill, or a profile.

1. Identify the layer first. Stable reasoning and host workflow belong in the skill. Runtime mechanics belong in the framework. Configurable design and resource selections belong in an external profile. Visual references, icons and components belong in shared Library Sets.
2. Never add profile assets or visual references to the installed skill.
3. Modify a profile under `<profiles-root>/<profile-id>`. For user-facing Agent operations, prefer `slidepoise profile create` and `slidepoise profile update`. Use `slidepoise library create` and `slidepoise library add-resource` for all reusable asset kinds. Profiles select set IDs and optional item IDs. Preserve stable IDs and provenance when moving legacy profile catalogs into shared sets. Creating a profile copies its style and selection without copying resource files. These commands edit the same installed profiles and catalogs shown by Console.
4. Remote logos and generic icons stay in a run cache unless the user requests persistent reuse. Selecting a visual-reference set does not enable its publisher's icons or grant additional artwork permissions.
5. Do not add a script when host-Agent visual reasoning is the correct mechanism. Scripts may measure, transform, package, and check objective contracts.
6. Never encode one slide's IDs, coordinates, wording, bend pattern, or observed defect into generic runtime code.
7. Mechanical checks emit facts, measurements, blocking structural findings, and artifact bindings. They must not emit an overall validity, quality, acceptance, or release verdict. A host-Agent reasoning review consumes this evidence and owns the checkpoint decision.
8. Visually inspect representative rendered outputs whenever behavior can alter appearance. Include connector overlays when connector code changes.
9. Run profile catalog preflight, config preflight, stable boundary audit, targeted Python tests, Node syntax checks, representative OpenCV measurement, generation-context construction, text fitting, Slide Master construction, multi-slide assembly, and a PowerPoint render comparison.
10. Package the stable skill independently. Install or update the framework and profiles with `slidepoise setup`.
11. Treat `references/user-language.md` as the product-wide user language contract. Review new Panel, Console, checkpoint, and generated-artifact copy against it. Use mechanical searches only as evidence. Do not auto-rewrite user-authored content or let a script issue a writing-quality verdict.
12. Keep deck orchestration flexible. Stable slide IDs, ordered scene assembly, and objective package checks belong in runtime. Page count, outline revisions, invalidation scope, review timing, and visual acceptance belong to the host Agent.
