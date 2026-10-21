# Imagegen Asset Handoff

Use this whenever built-in `$imagegen` is used for a PPT visual asset.

## Image2 Requirement

In Codex PPT runs, required generated raster visuals must come from Codex image2 through built-in `$imagegen`.

This applies to:

- cover hero visuals
- concept illustrations
- scenario illustrations
- abstract metaphors
- in-slide editorial illustrations
- image-first slide art

Local semantic renderers, native diagrams, screenshots, icons, color blocks, and placeholders can be used for planning, drafts, debugging, or explicitly accepted fallback drafts, but they do not count as final qualified image2-generated illustrations.

## Goal

The generated image must become a real project file before it can be inserted into PPTX, HTML, PDF, PNG previews, `asset_plan.json`, or `delivery_manifest.json`.

UI-only inline images are not delivery assets. They are previews until a local path, attachment path, or bytes payload is available.

## Required Workflow

1. Before calling `$imagegen`, create a capture marker:

   ```powershell
   .venv\Scripts\python.exe codex-ppt-skill\scripts\capture_imagegen_asset.py --run-dir <run_dir> --slide-id slide_01 --write-marker
   ```

2. Call built-in `$imagegen` / Codex image2.

3. Immediately run capture. In production, prefer a short watcher so a UI download can be captured without asking the user for the path:

   ```powershell
   .venv\Scripts\python.exe codex-ppt-skill\scripts\capture_imagegen_asset.py --run-dir <run_dir> --slide-id slide_01 --aspect 16:9 --allow-create --watch-seconds 45
   ```

4. If capture succeeds, the script copies the image into:

   - `<run_dir>/images/<slide_id>.png`

   and updates `asset_plan.json`:

   - `status=generated`
   - `output_path=<real local file>`
   - `generation_backend=codex_builtin_imagegen`
   - `capture_status=captured`
   - `capture_source=<original path>`

5. If capture fails, do not pretend image generation succeeded. The script records:

   - `capture_status=not_discoverable`
   - `status=failed`
   - `failed_reason=IMAGEGEN_OUTPUT_NOT_DISCOVERABLE`

## Discovery Locations

The capture script looks for persisted image files in:

- explicit `--candidate` paths
- explicit `--scan-dir` directories
- `<run_dir>`
- `<run_dir>/images`
- project `incoming_assets/`
- project `incoming_assets/imagegen_handoff/`
- project `outputs/`
- project `capability_tests/imagegen_probe/`
- `%USERPROFILE%\.codex\generated_images`
- `%USERPROFILE%\.codex\attachments`
- `%USERPROFILE%\Downloads`
- `%USERPROFILE%\Desktop`
- `%USERPROFILE%\Pictures`
- `%USERPROFILE%\OneDrive\Downloads`
- `%USERPROFILE%\OneDrive\Desktop`
- `%USERPROFILE%\OneDrive\Pictures`
- `%USERPROFILE%\AppData\Local\Temp`

It filters by:

- modification time after the capture marker
- image extension: `.png`, `.jpg`, `.jpeg`, `.webp`
- minimum dimensions
- optional aspect ratio, such as `--aspect 16:9`

## Important Limits

If `$imagegen` / image2 returns only a Codex UI inline image and does not expose a file path, attachment path, or bytes, the script cannot access that image from the workspace filesystem.

In that case:

- mark the required visual as failed
- write the failure to `qa_report.md`
- write the limitation to `delivery_manifest.json`
- ask the user to download the image into `incoming_assets/imagegen_handoff/` or provide the explicit downloaded path only if the watcher cannot discover it
- do not use a locally rendered placeholder as a qualified final image2 asset

## Never Do This

- Do not search for or read API keys.
- Do not call external image APIs.
- Do not use screenshots of the Codex UI as a fake source image.
- Do not mark `image_first` or required image generation E2E as passed unless an actual image file exists in the run directory.
