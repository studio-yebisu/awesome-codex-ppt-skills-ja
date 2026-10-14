# agent-slides

Agent skill for generating professional PowerPoint decks. 7 composable skills, a purpose-built CLI, and a Python API.

> **Quick start:** Visit [agent-slides.com](https://agent-slides.com) for docs, examples, and getting started guides.

## Why agent-slides?

Every AI agent can write text, but generating a polished, brand-compliant PowerPoint deck requires workflow knowledge that doesn't fit in a system prompt: when to preflight a project, when to dry-run, how to chain extraction → build → QA stages, how to recover from validation errors.

agent-slides encodes that knowledge in 7 composable skills, backed by a CLI that speaks JSON and a Python API that wraps `python-pptx` into a deterministic, agent-safe layer.

## What's Included

### 7 Skills

| Skill | Command | What it does |
|---|---|---|
| [slides-extract](skills/slides-extract/SKILL.md) | `/slides-extract` | Extract template contracts from a `.pptx` file |
| [slides-build](skills/slides-build/SKILL.md) | `/slides-build` | Build a complete deck from a brief |
| [slides-edit](skills/slides-edit/SKILL.md) | `/slides-edit` | Text edits, layout transforms, ops patches |
| [slides-audit](skills/slides-audit/SKILL.md) | `/slides-audit` | Technical lint: fonts, overlap, contrast |
| [slides-critique](skills/slides-critique/SKILL.md) | `/slides-critique` | Storytelling: action titles, MECE, hierarchy |
| [slides-polish](skills/slides-polish/SKILL.md) | `/slides-polish` | Final pass: notes, metadata, sources |
| [slides-full](skills/slides-full/SKILL.md) | `/slides-full` | End-to-end: extract → preflight → build → audit → critique → polish |

### The CLI

Skills call `uvx --from agent-slides slides ...` under the hood. The CLI provides:

- Declarative JSON operations with dry-run and transactional rollback
- Template extraction (layouts, archetypes, color zones, icons)
- Project preflight checks for extracted contracts, profile paths, icon packs, asset roots, and optional deps
- Validation, linting, and QA with design profiles
- Agent-optimized output (compact JSON, pagination, field masking)
- Runtime schema discovery (`uvx --from agent-slides slides docs json`)

## Installation

```bash
npx skills add https://github.com/mpuig/agent-slides
```

This installs the skills for Claude Code, Cursor, Gemini CLI, or Codex CLI — your choice. Skills call `uvx --from agent-slides slides ...` under the hood, so make sure [uv](https://docs.astral.sh/uv/) is available in your environment.

## Usage

Once installed, use skills in your agent harness:

```
/slides-extract template.pptx    # Extract template contracts
/slides-build                     # Build deck from a brief
/slides-audit                     # Check for technical issues
/slides-full                      # Run the full pipeline
```

Or use the CLI directly:

```bash
# Render a deck from a slides document
uvx --from agent-slides slides render --slides-json @slides.json --profile design-profile.json --output out.pptx

# Extract template contracts
uvx --from agent-slides slides extract template.pptx --output-dir extracted

# Preflight the extracted project before render
uvx --from agent-slides slides preflight --project-dir extracted --profile extracted/design-profile.json

# Validate and lint
uvx --from agent-slides slides validate out.pptx
uvx --from agent-slides slides lint out.pptx --profile design-profile.json --out lint.json

# Inspect and search
uvx --from agent-slides slides inspect out.pptx --summary
uvx --from agent-slides slides find out.pptx --query "pricing" --out results.json

# Schema discovery
uvx --from agent-slides slides docs json
uvx --from agent-slides slides docs schema:slides-document
```

## Typical Workflow

```
/slides-extract  →  preflight  →  /slides-build  →  /slides-audit  →  /slides-critique  →  /slides-polish
                                           ↕              ↕               ↕
                                      /slides-edit   targeted fixes   targeted fixes

Or use /slides-full to run the entire pipeline in one command.
```

## Development

```bash
uv sync --all-groups
uv run ruff check .
uv run ty check
uv run pytest
```

## License

MIT. See [LICENSE](LICENSE).

---

Created by [Marc Puig](https://github.com/mpuig)
