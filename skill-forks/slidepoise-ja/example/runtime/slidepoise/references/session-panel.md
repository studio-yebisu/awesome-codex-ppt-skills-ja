# Session style panel

The optional session panel is a lightweight editor for the current presentation's style and asset overrides. It is not a workflow dashboard, project manager, approval surface, artifact browser, or progress tracker.

Open it only when the user asks to inspect or change current-presentation settings, or when visual controls would materially simplify the choice. The conversation remains the primary place for outlines, generated images, comparisons, feedback, and deliverables.

## Session binding

Create or attach a run in conversation, then open the panel with

```bash
slidepoise panel --run /absolute/path/to/presentation
```

Preserve the returned panel ID for the conversation. A panel must be bound to a known run. Do not show a presentation picker or ask the user to manage run folders in the browser.

## Supported controls

The panel may show and edit

- inherited Profile
- density guidance
- display and body fonts
- palette and icon treatment
- selected Library Sets
- current-presentation uploads and required assets
- which values are inherited and which are overridden

An override changes only the current presentation. It never mutates the parent Profile. Reusable changes belong in the Console.

## Agent adoption

Panel writes create durable session events. Read pending changes before the next affected operation and acknowledge them after they influence the work. Polling at every scripted step is unnecessary. A long-running image or render call may finish before the new setting is adopted.

If the host cannot open the embedded browser, share the local URL only when the user still wants the controls. Panel availability never blocks presentation creation.
