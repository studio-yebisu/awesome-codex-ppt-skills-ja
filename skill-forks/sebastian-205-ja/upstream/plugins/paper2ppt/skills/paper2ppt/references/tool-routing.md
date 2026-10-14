# Tool routing

Route by discovered capability, not by client name. Codex and Claude Code may expose different tools, so inspect the active environment before committing to an extraction, authoring, notes, or rendering path.

## Route in order

1. Run the deterministic preflight described below, then inspect any native skills or tools that the CLI cannot discover.
2. If a native presentation artifact capability can create an editable PPTX, write speaker notes, and support the required QA, read its instructions and use it.
3. For PDF extraction, use a discovered native PDF capability when available. Otherwise use PyMuPDF; use Pillow for pixel-preserving crops without resampling, thumbnails, and contact sheets; prefer PNG or another lossless output when appropriate.
4. If no qualifying native authoring capability exists, use `python-pptx` 1.0.2 or newer. Create editable slides and write notes through `slide.notes_slide.notes_text_frame`.
5. For rendering, prefer an environment-provided renderer, then an existing LibreOffice or `soffice` installation. If neither exists, run structural QA only and disclose that visual QA was unavailable.
6. Fail during preflight when no editable PPTX authoring path exists. Do not perform extensive analysis and then substitute an outline.

Do not assume a platform-specific skill name exists. Select a capability only after inspecting its contract and confirming it satisfies the output requirements.

## Deterministic preflight

Use `<SKILL_DIR>` resolved by the main Skill. Never use the current working directory to locate packaged helpers:

```text
python "<SKILL_DIR>/scripts/preflight.py" INPUT --output PATH [--create-output] [--native-authoring] [--native-pdf] [--json]
```

The helper recognizes local PDF, Markdown/text, and PPTX-template paths plus DOI, PMID/PMCID, arXiv, and HTTP(S) identifiers. It does not fetch remote inputs; resolve remote access with the active agent before analysis. It preserves ordinary URL query parameters needed for source identity, but removes userinfo, fragments, and credential-bearing query parameters from reports and warns when redaction occurs. It requires module discovery plus distribution metadata for `python-pptx` 1.0.2+, PyMuPDF 1.24+, and Pillow 10+ without importing package code. It checks the output directory without creating it unless `--create-output` is explicit and reports renderer discovery separately.

Use `--json` for the stable `ok`, `source`, `output`, `capabilities`, `warnings`, and `errors` result. Exit `0` means the source and local authoring route are viable, `1` means a required input, capability, or writable output is missing, and argparse returns `2` for invalid usage. Native client capabilities may improve extraction or rendering after this deterministic baseline, but they do not justify ignoring a failed source or output check.

When the baseline fails only because `python-pptx` is missing, inspect the native capability contract. Rerun with `--native-authoring` only after confirming editable PPTX authoring, speaker notes, artifact reopening, and QA support. For an available local PDF missing PyMuPDF, add `--native-pdf` only after confirming page-grounded text and figure extraction. If both dependencies are missing and both native contracts qualify, use both flags. Each flag records a warning and bypasses only its named dependency; source and output failures remain fatal.

## Capability matrix

| Need | Preferred capability | Fallback | Accept only when |
| --- | --- | --- | --- |
| Text, metadata, and figures from PDF | Discovered native PDF capability | PyMuPDF | Page references and figure fidelity remain traceable |
| Crops and contact sheets | Native image operation | Pillow | Aspect ratio and source resolution are preserved |
| Editable PPTX authoring | Native presentation artifact capability | `python-pptx` 1.0.2+ | Slides remain object-level editable |
| Speaker notes | Native notes support | `slide.notes_slide.notes_text_frame` | Notes reopen in the PPTX package |
| Slide rendering | Environment renderer | Existing LibreOffice/`soffice` | Every slide can be rendered consistently |
| Structural QA | Native presentation inspector | OOXML ZIP/XML inspection | Media, relationships, notes, dimensions, and bounds are checked |

## Fallback conditions

- Fall back from a native capability when it cannot preserve editability, cannot write notes, omits source labels, or cannot expose an artifact for QA.
- Fall back from native PDF extraction when it cannot return page-grounded text or figures at usable resolution.
- Fall back to structural QA only when authoring succeeds but no renderer is installed or exposed. Record the exact missing capability in `qa_report.md`.
- Stop when the PPTX cannot be authored or reopened, the mandatory template cannot be read, or the available extraction path cannot support the requested claims.

## Portability and dependency rules

- Do not require PowerPoint or Keynote GUI automation.
- Do not hardcode platform-specific font or application paths. Use `pathlib`, discovered executables, installed fonts, and project-local output paths.
- Do not require a separate LLM API key; use the active agent's existing capabilities.
- Do not install packages unless environment policy permits it. Prefer already available dependencies and report any missing requirement during preflight.
- Keep intermediate files inside a project-local working directory and deliver only the output contract.
