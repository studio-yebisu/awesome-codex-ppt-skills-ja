# SeaSlides HTML Slides Toolset

This directory contains scripts for source conversion, project setup, HTML assembly, SVG/PPTX export, and image generation.

## Directory Layout

- Top-level `scripts/`: runnable entry scripts
- `scripts/html_to_svg/`: browser DOM HTML → SVG and PNG rendering helpers
- `scripts/svg_finalize/`: SVG post-processing utilities
- `scripts/svg_to_pptx/`: SVG → DrawingML → PPTX converter
- `scripts/source_to_md/`: source file → Markdown converters
- `scripts/image_backends/`: AI image generation providers
- `scripts/image_sources/`: web image search providers
- `scripts/docs_html/`: HTML pipeline documentation

## Quick Start

Typical end-to-end workflow:

```bash
# 1. Convert source material to Markdown
python3 scripts/source_to_md/pdf_to_md.py <file.pdf>

# 2. Initialize project
python3 scripts/project_manager.py init <project_name>
python3 scripts/project_manager.py import-sources <project_path> <source_files...> --copy

# 3. AI generates content.html using template classes

# 4. Source/TCS gate
python3 scripts/validate_project.py <project_path> --source-only --profile standard-project

# 5. Compile the atomic visual build (assembles index.html too)
python3 scripts/html_compiler.py <project_path> --all

# 6. Final visual gate: current receipt + visual artifacts
python3 scripts/validate_project.py <project_path> --require-build --artifact-profile visual

# 7. If PPTX is required, include it in one delivery build and validate it
python3 scripts/html_compiler.py <project_path> --all --include-pptx
python3 scripts/validate_project.py <project_path> --require-build --artifact-profile delivery
```

Add `--exact-name` only for deterministic benchmark/test directories; normal projects keep the dated suffix.

## Script Index

| Area | Primary scripts | Documentation |
|------|-----------------|---------------|
| Conversion | `source_to_md/pdf_to_md.py`, `doc_to_md.py`, `ppt_to_md.py`, `web_to_md.py`, `excel_to_md.py` | [docs/conversion.md](./docs/conversion.md) |
| Project management | `project_manager.py`, `validate_project.py`, `batch_validate.py` | [docs/project.md](./docs/project.md) |
| HTML pipeline | `assemble.py`, `validate_project.py`, `html_compiler.py` | [docs_html/browser_dom_export.md](./docs_html/browser_dom_export.md) |
| SVG export | `html_to_svg/browser_dom_to_svg.mjs` | See `--help` |
| PPTX export | `html_compiler.py --all --include-pptx` | Standard delivery; `svg_to_pptx.py` is internal/legacy diagnostic tooling |
| Image tools | `image_gen.py`, `image_search.py`, `analyze_images.py`, `source_inventory.py` | [docs/image.md](./docs/image.md) |

## High-Frequency Commands

Project setup:
```bash
python3 scripts/project_manager.py init <project_name>
python3 scripts/project_manager.py import-sources <project_path> <source_files...> --copy
```

Source gate and visual build:
```bash
python3 scripts/validate_project.py <project_path> --source-only --profile standard-project
python3 scripts/html_compiler.py <project_path> --all
python3 scripts/validate_project.py <project_path> --require-build --artifact-profile visual
```

PPTX delivery:
```bash
python3 scripts/html_compiler.py <project_path> --all --include-pptx
python3 scripts/validate_project.py <project_path> --require-build --artifact-profile delivery
```

Image generation:
```bash
python3 scripts/image_gen.py "A modern futuristic workspace"
python3 scripts/image_gen.py --list-backends
python3 scripts/analyze_images.py <project_path>/assets
```

## Recommendations

- Keep new runnable scripts at the top level of `scripts/`
- Move provider-specific or helper internals into subdirectories
- Prefer the unified entry points `project_manager.py`, `html_compiler.py`, and `image_gen.py`
- `dom-audit.json` is the browser-layout truth; it records settled-DOM blockers.
- `render-fidelity.json` records review-only differences between direct-browser and SVG-route PNGs.
- `compile-manifest.json` is the current-source receipt for the recursive local input closure, toolchain, renderer/runtime versions, assembled HTML, and artifacts.
- Always pass the source gate, visually review browser PNGs, and pass the appropriate current-build gate before delivering.

## Related Docs

- [Conversion Tools](./docs/conversion.md)
- [Project Tools](./docs/project.md)
- [Image Tools](./docs/image.md)
- [Browser DOM Export](./docs_html/browser_dom_export.md)
- [Troubleshooting](./docs/troubleshooting.md)
