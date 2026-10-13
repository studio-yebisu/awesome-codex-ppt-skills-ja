# Project Management Tools

This document describes the tools for managing HTML Slides presentation projects.

## Project Manager

The `project_manager.py` script provides unified project management functionality.

### Initialize a New Project

Create a new HTML Slides project with the standard directory structure.

```bash
python3 project_manager.py init <project_name> --dir projects
```

#### Created Structure
```
projects/project_name_YYYYMMDD/
├── README.md             # Project metadata
├── assets/               # Images and resources
├── output/               # Assembled and exported files
└── sources/              # Imported and normalized source material
```

Theme selection later adds `index-template.html` and `template.css`; the
Executor creates `content.html`.

### Import Source Files

Copy or move source files into the project.

```bash
python3 project_manager.py import-sources <project_path> <source_files...> [--move | --copy]
```

#### Options
- `--move`: Move files instead of copying
- `--copy`: Explicitly copy files (mutually exclusive with `--move`)

Sources are copied by default, regardless of location. Use `--move` only when the caller explicitly wants to relocate the original.

## Assembly and Validation

`html_compiler.py --all` atomically assembles `index.html` and emits both render routes and build receipts. `validate_project.py` has separate source and current-build artifact gates.

### Validate, Build, and Review Final Output

For standard slides, validate source before every build, then review the browser PNG baseline and validate the current visual artifact set.

```bash
python3 validate_project.py <project_path> --source-only --profile standard-project
python3 html_compiler.py <project_path> --all
python3 validate_project.py <project_path> --require-build --artifact-profile visual
```

`output/browser_pngs/` and `output/dom-audit.json` are the layout baseline. `output/pngs/` and `output/render-fidelity.json` diagnose SVG-route conversion differences. The build also publishes `output/overview.png` and `output/compile-manifest.json`.

### Build PPTX for Delivery

When PowerPoint is requested, include it in the full build and then use the delivery artifact profile.

```bash
python3 html_compiler.py <project_path> --all --include-pptx
python3 validate_project.py <project_path> --require-build --artifact-profile delivery
```

## Batch Validation

The `batch_validate.py` script validates multiple projects at once.

```bash
python3 batch_validate.py --dir ../examples --source-only
python3 batch_validate.py --dir ./projects --source-only --verbose
python3 batch_validate.py --dir ./projects --require-build --artifact-profile visual
python3 batch_validate.py --dir ./projects --require-build --artifact-profile delivery
python3 batch_validate.py --dir ./projects --source-only --export report.txt
```

#### Options
- `--dir`: Root directory containing HTML Slides projects (default: `.`)
- `--verbose, -v`: Show detailed validation messages
- `--source-only`: **source-only** profile — validates source/TCS without assembling or inspecting artifacts.
- `--require-build --artifact-profile visual|delivery`: **current-build** profile — validates an existing current compiler receipt and its visual or delivery artifact set without assembling.
- Choose exactly one of `--source-only` or `--require-build`; batch validation never assembles projects.
- `--fail-on-review`: Treat validator review warnings as failures.
- `--export`: Export report to a text file

## Best Practices

1. **Always initialize projects** with `project_manager.py init` to ensure correct structure
2. **Run the source gate, atomic build, browser-first review, and current-build gate**; do not treat standalone assembly as delivery evidence
3. **Use descriptive project names** for easy identification
4. **Keep assets organized** in the assets/ directory
5. **Use `html_compiler.py --all --include-pptx` for PPTX delivery**; direct `svg_to_pptx.py` is legacy diagnostic tooling

## Troubleshooting

### Project Not Found
Ensure you're using the correct project path relative to the current directory.

### Validation Fails
Check that all required files and directories exist in the project.

### Import Issues
Verify source files exist and you have read permissions.
