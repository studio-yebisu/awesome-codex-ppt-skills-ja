# Icon family and variant review

Use Remix Icon for generic public icons. Compare its canonical line and fill variants at the intended size. Use `resource-library.md` for retrieval. A generated generic icon can lead to a post-generation Remix search. Preserve a good composition while resolving its symbols to suitable canonical assets.

## Remix Icon pairs

Read when generic public icons are useful. Remix Icon supplies most concepts as one 24 x 24 line/fill pair. When `remote_sources.remix_icon.enabled` is true, retrieve both official SVGs before generation with `scripts/fetch_remix_icon_pair.py --config work/resolved-config.json`. Keep them in the run cache and retain the pair provenance.

Both candidates belong on the generation context sheet. The context sheet does not select the winner. The image model may use either as visual vocabulary. After selecting the generated slide for reconstruction, inspect the actual icon slots and choose the canonical reconstruction variant.

## Post-generation visual decision

Choose with the whole composition visible and inspect relevant close-ups. Consider these together.

- Apparent weight at the final slot size. Fine line details can collapse in a small slot. A filled mark can become visually blunt when enlarged.
- Foreground and background contrast after the profile treatment is applied.
- The surrounding visual grammar. Rules, outlined containers, sparse typography, and thin connectors often support line icons. Dense color fields, compact callouts, and strong focal emphasis may support fill icons.
- Local hierarchy. A fill icon may provide intentional emphasis. Do not use it merely because the icon is important semantically.
- Peer consistency. Icons in one `icon_treatment_group` use one variant. Create separate treatment groups when the composition genuinely calls for separate hierarchy levels.
- Silhouette fidelity. Select the variant whose mass, negative space, and optical footprint most closely match the approved target.

Do not reduce this choice to a score, background-color lookup, slot-size threshold, or automatic line-versus-fill rule. Code may verify that both candidates were considered and that peers agree. The Agent owns the choice.

For the chosen entity, record `icon_variant`, `upstream_asset_id`, and `icon_variant_review`. The review identifies the paired candidate asset IDs, states that it occurred after generation review, and gives concrete visual observations. The chosen `upstream_asset_id` must name the matching variant. Mechanical evidence establishes consistency and evidence presence only. It does not issue the visual verdict.

Remix icons may be recolored according to the active profile. Keep the SVG aspect ratio and original paths. Do not use a Remix icon as a logo, trademark, or brand identity. Retain the Remix Icon License v1.0 notice with fetched files.
