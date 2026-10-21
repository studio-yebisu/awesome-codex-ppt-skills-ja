#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/link-agent-adapters.sh [workspace]
  scripts/link-agent-adapters.sh --global

Creates agent-specific skill discovery links for mbb-page-maker.

Project mode:
  Source: <workspace>/.agents/skills/mbb-page-maker when present, otherwise this repo.
  Links:  <workspace>/.claude/skills/mbb-page-maker, .cursor/skills/..., etc.

Global mode:
  Source: ~/.agents/skills/mbb-page-maker when present, otherwise this repo.
  Links:  ~/.claude/skills/mbb-page-maker, ~/.cursor/skills/..., etc.
EOF
}

skill_name="mbb-page-maker"
mode="project"
workspace="${1:-$(pwd)}"

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  --global|-g)
    mode="global"
    workspace="$HOME"
    ;;
esac

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_skill_dir="$(cd "${script_dir}/.." && pwd)"

if [[ "$mode" == "project" ]]; then
  workspace="$(cd "$workspace" && pwd)"
  canonical_dir="${workspace}/.agents/skills/${skill_name}"
  base_dir="$workspace"
else
  canonical_dir="${HOME}/.agents/skills/${skill_name}"
  base_dir="$HOME"
fi

if [[ -f "${canonical_dir}/SKILL.md" ]]; then
  source_dir="$canonical_dir"
elif [[ -f "${repo_skill_dir}/SKILL.md" ]]; then
  source_dir="$repo_skill_dir"
else
  echo "Could not find ${skill_name}/SKILL.md in ${canonical_dir} or ${repo_skill_dir}." >&2
  exit 2
fi

link_skill() {
  local skills_dir="$1"
  local target="${skills_dir}/${skill_name}"

  mkdir -p "$skills_dir"

  if [[ -L "$target" || ! -e "$target" ]]; then
    ln -sfn "$source_dir" "$target"
    echo "Linked: ${target} -> ${source_dir}"
    return
  fi

  if [[ -f "${target}/SKILL.md" ]] && cmp -s "${source_dir}/SKILL.md" "${target}/SKILL.md"; then
    echo "Exists: ${target}"
    return
  fi

  echo "Refusing to overwrite existing non-symlink: ${target}" >&2
  echo "Remove it manually or rerun your skill installer with --copy if you want a separate copy." >&2
  exit 3
}

agent_skill_dirs=(
  "${base_dir}/.claude/skills"
  "${base_dir}/.cursor/skills"
  "${base_dir}/.codex/skills"
  "${base_dir}/.opencode/skills"
  "${base_dir}/.openclaw/skills"
  "${base_dir}/.hermes/skills"
)

for skills_dir in "${agent_skill_dirs[@]}"; do
  link_skill "$skills_dir"
done

echo "Done. Restart any agent session that started before these skill directories existed."
