# Technical Architecture Decision

## Summary

Full-deck archetype for explaining architecture options, tradeoffs, risks, and a recommended technical path before detailed implementation planning.

## Visual traits

Architecture decision style with control-layer framing, option matrix, capability coverage, swimlane proof path, and decision close.

## Use when

Use for architecture option selection, platform path decisions, build-vs-extend choices, integration-pattern decisions, or technical governance approvals.

## Do not use when

Do not use when the audience already approved the architecture and now needs a detailed rollout, staffing, or delivery governance plan.

## Storyline pattern

Cover, architecture recommendation, target decision model, option tradeoff, capability coverage, proof path, decision close.

## Layout + component stack

Uses `input-process-output-layers`, `matrix-table`, `capability-coverage-map`, `swimlane-process-map`, `decision-log`, and `phase-meeting-plan`.

## Theme / assets

Theme: `assets/themes/blue.css`. Optional generated cover asset: `assets/media/covers/strategy-architecture-cover.jpg`.

## Source inspiration

Source-neutral technical decision and architecture review patterns. No external deck, brand system, or consulting-firm identity is copied.

## Evidence shape

Best with architecture options, requirements, constraints, tradeoffs, integration risks, governance needs, proof milestones, and decision owners.

## Path

`templates/full-decks/technical-architecture-decision/index.html`

## Related showcase patterns

`templates/showcase/technical-architecture-decision-page.html`, `templates/showcase/flow-workplan-variants.html`, `templates/showcase/analysis-table-variants.html`

## Flexible swaps

Swap `matrix-table` for `weighted-scorecard` when option scores are explicit, swap `capability-coverage-map` for `heatmap` when numeric ratings exist, and swap `swimlane-process-map` for `phase-roadmap` when phases matter more than roles.

## When to diverge

Diverge to `technical-implementation-plan` when the question is how to build the approved target architecture.

## Do not copy page order/content

Do not copy the archetype page order, placeholder claims, footer text, or technical labels. Use it only to understand architecture-decision pacing and component combinations.
