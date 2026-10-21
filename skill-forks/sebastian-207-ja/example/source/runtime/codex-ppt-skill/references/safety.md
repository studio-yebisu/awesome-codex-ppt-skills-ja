# Safety

These rules are hard boundaries.

## Secrets

- Do not read API keys.
- Do not print API keys.
- Do not infer or copy API keys.
- Do not read `.env` unless the user explicitly asks and the task requires it; even then, never print secret values.
- Do not ask for `OPENAI_API_KEY` when using built-in `$imagegen`.

## Installation And Global State

- When the user has not authorized installation, do not auto-install dependencies.
- For this Phase 2 upgrade, the user explicitly authorized local dependency installation.
- Use project-local `.venv` for Python packages.
- Use project-local `node_modules` for Node packages.
- Windows official `winget` may be used for missing official Python, Node.js, or LibreOffice.
- Do not execute third-party repository install scripts, `curl | bash`, `irm | iex`, or unknown `install.sh` files.
- Do not install a third-party PPT skill as a replacement for this skill.
- Do not modify global Codex/Claude config or global package locations unless the user explicitly asks.
- Record installation commands, attempts, versions, and outcomes in:
  - `install_log.md`
  - `environment_lock.json`

## User Files

- Do not move or overwrite user source files.
- Copy inputs into the run directory when modification is needed.
- Keep original PPT, template, fixture, document, and image files intact.

## External Services

- Do not upload user documents to external services.
- Do not call third-party image APIs.
- Do not call external OCR, TTS, or generation APIs unless the user explicitly authorizes that specific service.
- Built-in Codex tools such as `$slides` and `$imagegen` may be used when the user requested this skill and has not forbidden them.

If a capability fails after an authorized install attempt, record the real error in `qa_report.md`, `delivery_manifest.json`, and the applicable environment report.
