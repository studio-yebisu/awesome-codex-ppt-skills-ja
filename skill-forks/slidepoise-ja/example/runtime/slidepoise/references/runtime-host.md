# Host integration

The host Agent supplies reasoning, image inspection, file access and command execution. SlidePoise supplies the same planning, generation handoff, measurement and PowerPoint reconstruction on every host. Read `image-generation.md` before the first creative call and whenever the user changes generation preferences.

## Installation and discovery

Setup registers the skill with detected Codex, Claude Code and Qoder installations. Use `slidepoise setup --agent claude` or `--agent qoder` to choose explicitly. Repeat `--agent` for several hosts. The installed skill and local framework are identical across hosts.

Claude Code reads `~/.claude/skills/slidepoise/SKILL.md`. Qoder CLI reads `~/.qoder/skills/slidepoise/SKILL.md`. Codex reads `~/.codex/skills/slidepoise/SKILL.md`. Other hosts can load the packaged `SKILL.md` and its references if they support local execution and visual inspection. QoderWork has a separate skill location and is not selected by the Qoder CLI installer.

A detected application or an installed skill does not prove that an image tool is available. Inspect the tools exposed in the active conversation, including tool-search results, MCP tools and installed image-generation skills. Read the actual interface before use. The Console stores preferences and never claims to see another application's current tool inventory.

## Host controls

Use the host's own image reader, terminal and file tools. Adapt command prefixes and file paths to its execution environment. Keep the parent Agent responsible for the presentation. Delegate a bounded image call or a page review only when the host supports it and delegation is authorised. A sequential host performs the same work without subagents.

The session panel and CLI share durable changes. Run `slidepoise run sync <run>` before each affected operation and acknowledge events after applying them. Codex can additionally receive a best-effort notification for an explicitly bound active task. Other hosts use the same checkpoint reads. Do not invent a background callback or resume a host conversation without permission.

In a browser-only chat, proceed only if that environment can access the packaged files, execute the runtime and inspect images. Manual generation supplies images, not missing execution or visual reasoning capabilities.

## Measurement and reconstruction

OpenCV supplies the complete default measurement path. Use `slidepoise_runtime.py reconstruct-slide` and the packaged scene renderer. Never replace creative generation or reconstruction with a custom HTML, SVG or PptxGenJS deck builder.

The internal SAM adapter remains readable for existing explicitly configured runs. It is experimental, disabled by default and has no managed installer or Console control. For a deliberately configured experiment, the host assigns eligible entities, inspects candidates and selects a `sam_candidate_index` before a mask contributes. The host retains semantic and visual authority.

If a required runtime operation fails, repair its inputs or explain the exact blocker. Continue independent work where possible.
