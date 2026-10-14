# Unified CLI and runtime diagnosis

[Homepage](../README.en.md) · [简体中文](cli.md)

`slidemuse.py` provides one entry point for existing local tools on Python 3.10+. Run it from the repository or installed skill root, or supply its full path from another directory. Task paths remain relative to your working directory.

```sh
python slidemuse.py --help
python slidemuse.py --version
python slidemuse.py doctor
```

The launcher prefers `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` elsewhere, relative to its own directory, and otherwise uses the current interpreter. It computes the path after relocation rather than trusting stale `.skill-python` contents. The environment must still match the OS and base Python. No activation, uv, pipx, or new library is required.

## Common commands

| Command | Existing tool | Purpose |
|---|---|---|
| `init task --mode editable` | `scripts/init_deck.py` | Initialize prepared specifications without overwriting a job |
| `check task/job.json task-output` | `scripts/run_deck.py --check` | Read-only preflight |
| `run task/job.json task-output` | `scripts/run_deck.py` | Build, render, evaluate or resume |
| `render deck.pptx previews` | `scripts/render_deck.py` | Render an actual PPTX |
| `validate page-spec.json --strict` | `scripts/validate_page_spec.py` | Validate specifications |
| `audit deck.pptx --scene scene.json` | `scripts/audit_editability.py` | Check native objects |
| `review task/job.json task-output` | `scripts/review_panel.py` | Export a review panel or import records |
| `sample --verify --output sample-output` | `showcase/editable-irena/reproduce.py` | Rebuild all six public sample decks |

Prefix each command with `python slidemuse.py`. Arguments pass through unchanged, and `<command> --help` displays the original tool's help. Advanced tools remain available as `scripts/*.py`; use the installed `.venv` interpreter or the path recorded in `.skill-python` for direct invocation.

Pipeline exit codes are preserved: 0 means the requested command succeeded, possibly only saving a requested stage; 1 means failed checks or blocked input; 3 means review is pending. Invalid arguments normally return 2. `check` is read-only and never creates a workspace or approves assets. Options such as `run --stop-after` and `run --status` remain controlled by the original script. Content approval, style selection and visual review follow the existing Skill contract.

## Diagnose the environment

```sh
python slidemuse.py doctor --json
python slidemuse.py doctor --require-renderer --backend powerpoint
```

Diagnosis installs nothing, uses no network, does not launch PowerPoint, and does not write task files. It checks the Python 3.10 minimum and dependency installation, numeric minimum versions and imports. Each import probe has a 15-second limit. Missing or broken dependencies produce a failure and repair command. Renderer checks cover Windows PowerPoint registration and PowerShell, or LibreOffice and Poppler on PATH; discovery does not prove rendering succeeds.

The parser supports this repository's `package>=numeric-version` format. Ambiguous prerelease versions and unsupported future constraints explicitly fail. A missing renderer warns with exit code 0 by default, permitting specification checks and compilation; `--require-renderer` makes a missing selected backend fail with exit code 1. Invalid arguments return 2. JSON includes `schema_version`, `skill_version`, `status`, `python`, `skill_root` and individual `checks`.

If the isolated Python cannot start, use a known working Python to invoke `python scripts/doctor.py --json` directly and diagnose that interpreter. Repair the isolated installation by rerunning the repository installer. Sanitize local paths before sharing reports.

Diagnosis does not test the host agent's document reading, vision or image generation. The public sample starts with approved images and structured inputs; reproduction does not establish host image-generation availability.
