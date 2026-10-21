# Release Manifest

Release directory:

```text
C:\Users\Administrator\Documents\ppt\publish\codex-ppt-skill-github
```

## Included

- `codex-ppt-skill/SKILL.md`
- `codex-ppt-skill/agents/openai.yaml`
- `codex-ppt-skill/references/`
- `codex-ppt-skill/scripts/`
- `codex-ppt-skill/design-system/`
- `codex-ppt-skill/assets/`
- `codex-ppt-skill/examples/`
- `codex-ppt-skill/evals/`
- root `README.md`
- root `requirements.txt`
- root `package.json`
- root `.gitignore`
- root `LICENSE`

## Excluded

- `.venv/`
- `node_modules/`
- `ppt_runs/`
- `outputs/`
- `_reference_skills/`
- `incoming_assets/`
- `capability_tests/`
- `backups/`
- Python cache files
- local generated fallback images under `assets/generated/`
- user source PPT/PDF/DOCX/XLSX files
- environment files or keys

## Validation

- Skill frontmatter validation: PASS
- Runtime output directory scan: PASS
- Cache/private-key file scan: PASS
- Secret-value scan: no secret values found

The words `API key`, `secret`, and `token` may appear in safety policy text. They are policy terms, not credential values.

## Notes

This repository package does not include the cloned third-party reference repositories or user test materials. Public users can still use the skill, and they can optionally build their own local reference library.
