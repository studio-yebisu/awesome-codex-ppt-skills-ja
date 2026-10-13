# Troubleshooting Guide

This document provides solutions to common issues with the HTML Slides toolset.

## Installation Issues

### Node.js Not Found

**Error**: `node is not installed or not in PATH`

**Solution**:
```bash
# Install Node.js (required for browser SVG export)
# macOS
brew install node

# Ubuntu/Debian
sudo apt-get install nodejs npm

# Or download from https://nodejs.org/

# Verify installation
node --version
```

### Pandoc Not Found

**Error**: `Pandoc is not installed or not in PATH`

**Solution**:
```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc

# Or download from https://pandoc.org/installing.html

# Verify installation
pandoc --version
```

### Missing Python Packages

**Error**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**:
```bash
# Install all required packages
pip install pymupdf requests beautifulsoup4 Pillow pypdf python-pptx

# Or install specific package
pip install <package_name>
```

## Project Issues

### Project Initialization Fails

**Error**: `Project directory already exists`

**Solution**:
```bash
# Use a different project name
python3 project_manager.py init my-presentation-2

# Or remove existing directory (caution!)
rm -rf my-presentation
```

### Validation Fails

**Error**: `Missing required file: content.html`

**Solution**:
```bash
# Re-initialize the project
python3 project_manager.py init <project_name>

# Or manually create missing files
touch <project_name>/content.html
touch <project_name>/index-template.html
touch <project_name>/template.css
mkdir -p <project_name>/{assets,output}
```

### Import Sources Fails

**Error**: `Source file not found`

**Solution**:
```bash
# Verify file paths are correct
ls -la <source_file>

# Use absolute paths if needed
python3 project_manager.py import-sources <project> /full/path/to/file.pdf

# Check file permissions
chmod 644 <source_file>
```

## Assembly Issues

### Assembly Fails

**Error**: `Missing index-template.html or content.html`

**Solutions**:
```bash
# 1. Check that both files exist in the project directory
ls <project_path>/content.html <project_path>/index-template.html

# 2. Verify source/TCS structure and classes
python3 validate_project.py <project_path> --source-only --profile standard-project

# 3. Build the synchronized artifact set
python3 html_compiler.py <project_path> --all

# 4. Check template.css is present and referenced
ls <project_path>/template.css
```

### Malformed content.html

**Error**: `HTML validation error: unclosed tag` or `Invalid slide structure`

**Solutions**:
```bash
# 1. Validate content.html structure and TCS contract
python3 validate_project.py <project_path> --source-only --profile standard-project

# 2. Check for unclosed HTML tags
# Ensure every <div>, <section>, <span> is properly closed

# 3. Verify slide class usage
# Each slide should use the correct CSS classes from the TCS

# 4. Check for stray characters or encoding issues
file <project_path>/content.html
```

### Missing template.css

**Error**: `template.css not found` or styles not applied

**Solutions**:
```bash
# 1. Verify template.css exists
ls <project_path>/template.css

# 2. Re-initialize the project to regenerate template files
python3 project_manager.py init <project_name>

# 3. Check that index-template.html references template.css
grep "template.css" <project_path>/index-template.html
```

### Content Overflow

**Error**: Content extends beyond slide boundaries

**Solutions**:
```bash
# 1. Reduce content per slide
# - Shorten text
# - Use smaller font sizes via CSS classes
# - Split into multiple slides

# 2. Adjust layout
# - Use CSS grid or flexbox columns
# - Reduce margins and padding
# - Resize images with width/height attributes

# 3. Build and inspect output/browser_pngs/ plus output/dom-audit.json
python3 html_compiler.py <project_path> --all
```

### Font Not Available

**Error**: Font not rendering correctly in browser or SVG export

**Solutions**:
```bash
# 1. Use web-safe fonts or Google Fonts via CDN
# Add to index-template.html <head>:
# <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

# 2. Install fonts locally for SVG export
# macOS: Copy to ~/Library/Fonts/
# Linux: Copy to ~/.local/share/fonts/

# 3. Specify fallback fonts in template.css
# font-family: 'CustomFont', 'Arial', sans-serif;

# 4. Check font availability in Chromium
# Browser export uses the fonts loaded by the assembled HTML
```

### Wrong Slide Count

**Error**: Expected 20 slides, got 18

**Solutions**:
```bash
# 1. Check for missing slide sections
# Review content.html for all <section> or slide <div> elements

# 2. Verify slide delimiters are correct
# Ensure each slide is properly wrapped in its container element

# 3. Check for hidden or collapsed content
# Some CSS classes may hide content unintentionally

# 4. Run the source gate, then inspect browser PNGs and the DOM audit
python3 validate_project.py <project_path> --source-only --profile standard-project
python3 html_compiler.py <project_path> --all
```

## SVG Export Issues

### Browser SVG Rendering Fails

**Error**: `browser_dom_to_svg.mjs failed`, blank SVGs, or missing slides

**Solutions**:
```bash
# 1. Open the assembled HTML in Chromium and check console errors

# 2. Verify Node.js and Playwright dependencies are installed
node --version
npm list playwright

# 3. Install missing npm dependencies
npm install
npx playwright install chromium

# 4. Test through the unified compiler
python3 html_compiler.py <project_path> --all
```

### SVG Output Incorrect

**Error**: Missing images, wrong layout, or blank slides in SVG

**Solutions**:
```bash
# 1. Check image paths relative to root-level index.html

# 2. Verify browser export readiness
# Math, code, charts, and async scripts must finish before capture

# 3. Check font embedding
# Fonts must be loaded by Chromium before export
```

## PPTX Export Issues

### PPTX Generation Fails

**Error**: PPTX output is missing or the delivery artifact gate fails

**Solutions**:
```bash
# 1. Verify the current build receipt and visual artifacts
python3 validate_project.py <project_path> --require-build --artifact-profile visual

# 2. Check python-pptx is installed
pip install python-pptx

# 3. Run the same-build PPTX delivery pipeline
python3 html_compiler.py <project_path> --all --include-pptx
python3 validate_project.py <project_path> --require-build --artifact-profile delivery

# 4. Use output/render-fidelity.json and matching SVG-route PNGs only to diagnose conversion differences
```

### Missing CDN Resources

**Error**: External resources fail to load or render

**Solutions**:
```bash
# 1. Check network connectivity
curl -I https://fonts.googleapis.com

# 2. Use local copies of CDN resources for offline use
# Download CSS/fonts and reference them locally

# 3. Verify CDN URLs in index-template.html are correct
# Check for typos or outdated URLs
```

## Image Issues

### Image Generation Fails

**Error**: `Error generating image: xxx`

**Solutions**:
```bash
# 1. Check backend availability
python3 image_gen.py --list-backends

# 2. Verify API credentials
# Check backend-specific configuration

# 3. Try different backend
python3 image_gen.py "prompt" --backend <other_backend>

# 4. Check network connectivity
ping api.example.com
```

### Image Not Found

**Error**: `Image not found` or broken `<img>` tag

**Solutions**:
```bash
# 1. Verify image path in content.html
# Use relative paths from the project root: <img src="assets/image.png">

# 2. Check image location
# Images should be in the assets/ directory

# 3. Import sources correctly
python3 project_manager.py import-sources <project> image.png --move

# 4. For SVG export, use base64-encoded images or absolute paths
```

### Image Too Large

**Error**: Content overflow due to large image

**Solutions**:
```bash
# 1. Analyze image size
python3 analyze_images.py <project>/assets

# 2. Resize image
# Use image editing software or Python PIL

# 3. Constrain image size in HTML
# <img src="assets/image.png" style="max-width: 50%; height: auto;">

# 4. Use more efficient formats (WebP)
```

## Conversion Issues

### PDF Conversion Fails

**Error**: `PyMuPDF (fitz) is not installed`

**Solution**:
```bash
pip install pymupdf

# Or use pdfplumber
pip install pdfplumber
```

### Webpage Conversion Fails

**Error**: `Error fetching webpage: xxx`

**Solutions**:
```bash
# 1. Check URL is accessible
curl <url>

# 2. Install curl_cffi for sites that reject plain requests
pip install curl_cffi

# 3. Check network connectivity
ping example.com

# 4. Use different user agent
# Modify script to include headers
```

### Pandoc Conversion Fails

**Error**: `Error during conversion: xxx`

**Solutions**:
```bash
# 1. Verify file format is supported
pandoc --list-input-formats

# 2. Check file is not corrupted
file <input_file>

# 3. Try different output format
pandoc -f docx -t markdown -o output.md input.docx

# 4. Use verbose output
pandoc -v input.docx -o output.md
```

## Performance Issues

### Slow Assembly

**Solutions**:
```bash
# 1. Reduce image sizes
# Compress images before importing

# 2. Minimize CSS complexity
# Remove unused styles from template.css

# 3. Reduce number of slides
# Split large presentations into parts

# 4. Check for large inline assets
# Move base64-encoded images to external files
```

### Out of Memory

**Error**: Memory error during SVG export or PPTX generation

**Solutions**:
```bash
# 1. Reduce image resolution
# Resize images to smaller dimensions

# 2. Export in batches
# Split large presentations

# 3. Close other applications
# Free up system memory

# 4. Increase system swap
# Add more virtual memory
```

## Getting Help

### Check Documentation
- [MDN Web Docs](https://developer.mozilla.org/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Script Documentation](./)

### Run Validation
```bash
python3 validate_project.py <project_path> --source-only --profile standard-project
```

### Validate Project
```bash
python3 project_manager.py validate <project_path>
```

## Common Patterns

### Fresh Start
```bash
# Clean and reinitialize
rm -rf <project>
python3 project_manager.py init <project>
python3 project_manager.py import-sources <project> <sources>
```

### Debug Mode
```bash
# Run source gate, full build, then inspect browser PNGs and DOM audit
python3 validate_project.py <project_path> --source-only --profile standard-project
python3 html_compiler.py <project_path> --all
python3 validate_project.py <project_path> --require-build --artifact-profile visual
```

### Test Assembly
```bash
# Quick test with minimal content
echo '<section class="slide"><h1>Test</h1></section>' > test-content.html
python3 assemble.py --content test-content.html --template index-template.html
```

## Additional Resources

- [MDN HTML Reference](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Playwright GitHub](https://github.com/microsoft/playwright)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
