# Agent Compatibility

`mbb-page-maker` follows the Agent Skills directory format: one skill folder with `SKILL.md`, `references/`, `templates/`, `assets/`, and `scripts/`.

Some installers use `.agents/skills/<skill-name>/` as the canonical shared location. Not every agent runtime scans that location directly. If a tool shows `Unknown skill: mbb-page-maker` but the files exist, the skill was installed but not linked into that tool's discovery path.

## Discovery Paths

Common discovery paths:

| agent | expected project path | expected user/global path |
| --- | --- | --- |
| Claude Code | `.claude/skills/mbb-page-maker/SKILL.md` | `~/.claude/skills/mbb-page-maker/SKILL.md` |
| Cursor | `.cursor/skills/mbb-page-maker/SKILL.md` | `~/.cursor/skills/mbb-page-maker/SKILL.md` |
| Codex-style clients | `.codex/skills/mbb-page-maker/SKILL.md` | `~/.codex/skills/mbb-page-maker/SKILL.md` |
| OpenCode-style clients | `.opencode/skills/mbb-page-maker/SKILL.md` | `~/.opencode/skills/mbb-page-maker/SKILL.md` |
| OpenClaw-style clients | `.openclaw/skills/mbb-page-maker/SKILL.md` | `~/.openclaw/skills/mbb-page-maker/SKILL.md` |
| Hermes-style clients | `.hermes/skills/mbb-page-maker/SKILL.md` | `~/.hermes/skills/mbb-page-maker/SKILL.md` |

The canonical shared path remains `.agents/skills/mbb-page-maker/`. Agent-specific paths should be symlinks or copies pointing to the canonical package, not hand-maintained duplicates.

## Recommended Install

For broad agent support, prefer an installer command that targets all detected agents:

```bash
npx skills add https://github.com/NomiciAI/mbb-page-maker --agent '*'
```

If that still leaves an agent unable to find the skill, link adapters from the workspace root:

```bash
.agents/skills/mbb-page-maker/scripts/link-agent-adapters.sh .
```

For global installs:

```bash
~/.agents/skills/mbb-page-maker/scripts/link-agent-adapters.sh --global
```

The script creates symlinks from the agent-specific skill directories back to the canonical package. It refuses to overwrite an existing non-symlink directory with different content.

## Claude Code Unknown Skill

Claude Code discovers skills from `.claude/skills/`, `~/.claude/skills/`, or plugin `skills/` directories. A package that exists only under `.agents/skills/mbb-page-maker/` can still be read manually by Claude as normal files, but `/mbb-page-maker` or `Skill(mbb-page-maker)` will fail because the skill registry never indexed it.

Fix:

```bash
mkdir -p .claude/skills
ln -sfn ../../.agents/skills/mbb-page-maker .claude/skills/mbb-page-maker
```

For global installs:

```bash
mkdir -p ~/.claude/skills
ln -sfn ~/.agents/skills/mbb-page-maker ~/.claude/skills/mbb-page-maker
```

Restart Claude Code if `.claude/skills/` did not exist when the session started.
