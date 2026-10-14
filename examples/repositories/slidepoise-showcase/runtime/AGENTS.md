# SlidePoise project instructions

For a user request to install or configure SlidePoise, follow `docs/AGENT_SETUP.md`. It uses the existing installer and shared configuration. The instructions below apply when working on the product itself.

Read `slidepoise/SKILL.md` for every presentation task and follow the references it routes to. The skill directory is the product source of truth. Its packaged configuration, resources, scripts, schemas, and runtime must remain self-contained.

The host Agent owns visual and semantic judgement. Deterministic code may measure, validate, transform files, fit text, and construct PowerPoint objects. It must not replace visual review with a heuristic score or workflow state machine.

The browser surfaces in `webapp/` are optional. Console manages reusable Profiles, Library Sets, and capabilities. The session panel edits current-presentation style and asset overrides only. Conversation handles planning, generated images, review, revision, and delivery.

SAM is an optional measurement enhancement. Keep OpenCV as the complete default measurement route. Load SAM only for host-authored eligible irregular objects, only when the configured checkpoint and optional dependencies are available, and record whether its mask contributed. SAM never decides semantic ownership or visual acceptance.

For changes to the skill itself, also read `slidepoise/references/maintenance.md`. Preserve adaptive Agent control and run the packaged validators before release.
