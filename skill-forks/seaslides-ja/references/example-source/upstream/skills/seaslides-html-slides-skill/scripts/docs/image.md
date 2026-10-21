# Image Tools

This document describes the tools for image generation and analysis.

## Image Generator

The `image_gen.py` script generates images using various AI backends.

### Generate Image

```bash
python3 image_gen.py "A modern futuristic workspace"
```

### Specify Backend

```bash
python3 image_gen.py "A serene mountain landscape" --backend stable-diffusion
```

### Custom Output

```bash
python3 image_gen.py "Abstract geometric patterns" -o output.png
```

### Custom Aspect Ratio

```bash
python3 image_gen.py "Portrait style image" --aspect-ratio 9:16
```

### Custom Size

```bash
python3 image_gen.py "High resolution image" --image-size 2048x2048
```

### List Available Backends

```bash
python3 image_gen.py --list-backends
```

### Check Available Backends

Check which backends have API keys configured:

```bash
python3 image_gen.py --check-available
```

#### Options
- `--backend, -b`: Backend to use (e.g., gemini, openai, openrouter, minimax, qwen, zhipu, etc.)
- `--output, -o`: Output path for generated image
- `--aspect-ratio, -a`: Aspect ratio (default: 16:9)
- `--image-size, -s`: Image size (512px/1K/2K/4K, default: 1K)
- `--list-backends`: List all available backends
- `--check-available`: Check which backends have API keys configured

## Image Analyzer

The `analyze_images.py` script analyzes image files in a directory.

### Analyze Directory

```bash
python3 analyze_images.py ./assets
```

### Specify Canvas Format

```bash
python3 analyze_images.py ./assets --canvas ppt169
```

#### Output Information
- File dimensions (width x height)
- Aspect ratio and orientation category
- Canvas-aware layout dimensions (image area, text area)
- File size
- Markdown snippet for strategist prompts
- CSV export

## Source Inventory

The `source_inventory.py` script scans a project's `sources/` directory and
produces a complete inventory (file listing, markdown content, image analysis
with HTML/CSS layout guidance) as Markdown on stdout.

### Scan Sources

```bash
python3 source_inventory.py <sources_dir>
```

#### Output Sections

1. **Source File Inventory** -- categorized file listing (markdown, images, PDFs, other)
2. **Source Content** -- full text of all `.md` files
3. **Source Images** -- table with dimensions, orientation, and recommended HTML/CSS layout

The output is designed for direct embedding into LLM prompts.

## Image Backends

13 backends are supported across 3 tiers:

| Tier | Backends |
|------|----------|
| **Core** | gemini, openai, minimax |
| **Extended** | qwen, zhipu, volcengine, stability, bfl, ideogram |
| **Experimental** | siliconflow, fal, replicate, openrouter |

Configure by setting `IMAGE_BACKEND` and the provider's API key in environment or `.env`:

```bash
export IMAGE_BACKEND=openai
export OPENAI_API_KEY=sk-...
```

Run `python3 image_gen.py --check-available` to verify which backends are ready.

## Supported Image Formats

The image tools support the following formats:

- JPG/JPEG
- PNG
- GIF
- BMP
- TIFF
- WebP
- SVG

## Using Images in HTML Slides

### Basic Image Tag

```html
<img src="assets/photo.png" alt="Description" style="max-width: 100%; height: auto;">
```

### Constrained Size

```html
<img src="assets/chart.png" alt="Chart" style="width: 50%; height: auto;">
```

### Full-Bleed Background Image

```html
<section class="slide" style="background-image: url('assets/bg.jpg'); background-size: cover;">
  <h1>Title Over Image</h1>
</section>
```

### Side-by-Side Layout

```html
<div style="display: flex; gap: 1rem;">
  <img src="assets/left.png" alt="Left" style="flex: 1; max-width: 48%;">
  <img src="assets/right.png" alt="Right" style="flex: 1; max-width: 48%;">
</div>
```

### SVG Export Considerations

When targeting browser-based SVG export:
- Use local project assets or data URIs for deterministic batch output
- Prefer `<img>` tags for semantic images and CSS backgrounds for decoration only
- Ensure images are accessible from the assembled root-level `index.html`
- Inspect browser PNGs and the DOM audit for layout; use SVG-route PNGs and fidelity findings only to diagnose conversion behavior when using filters, masks, or complex backgrounds

## Configuration

Image settings are defined in `config.py`:

```python
IMAGE_SETTINGS = {
    'supported_formats': ['.jpg', '.jpeg', '.png', ...],
    'max_width': 3840,
    'max_height': 2160,
    'default_aspect_ratio': '16:9',
    'default_size': '1024x1024'
}
```

## Best Practices

### Image Generation
1. **Use descriptive prompts**: More specific prompts yield better results
2. **Match aspect ratio to use case**: 16:9 for presentations, 9:16 for mobile
3. **Choose appropriate size**: Higher for print, lower for web
4. **Test different backends**: Results vary by provider
5. **Review generated images**: AI may produce unexpected results

### Image Analysis
1. **Regularly analyze assets**: Track image usage and quality
2. **Generate manifests**: Keep documentation of image resources
3. **Check aspect ratios**: Ensure images match slide dimensions
4. **Monitor file sizes**: Large images slow assembly and SVG export
5. **Validate formats**: Ensure all images are supported

## Common Issues

### Generation Fails
- Check API keys and credentials
- Verify network connectivity
- Review backend-specific error messages
- Try alternative backend

### Image Too Large
- Reduce image size
- Use more efficient format (WebP)
- Compress existing images
- Consider external hosting

### Aspect Ratio Issues
- Calculate correct dimensions
- Use standard ratios (16:9, 4:3, 1:1)
- Check image analyzer output
- Resize images appropriately

## Requirements

### Core
- `Pillow` (PIL): Image processing
  - Install: `pip install Pillow`

### Backend-Specific
Each backend may have additional requirements:
- DALL-E: `openai` package
- Stable Diffusion: Various packages
- Other backends: Check documentation

## Tips

1. **Batch generate images**: Script multiple generations for efficiency
2. **Use version control**: Track generated images
3. **Organize by project**: Keep images in project-specific directories
4. **Document prompts**: Save successful prompts for reuse
5. **Optimize for web**: Compress images before use in presentations
