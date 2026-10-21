#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

import fitz
from docx import Document


def pptx_text(path: Path) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(path) as z:
        for name in sorted(n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)):
            xml = z.read(name).decode("utf-8", errors="ignore")
            texts = re.findall(r"<a:t[^>]*>(.*?)</a:t>", xml, flags=re.S)
            chunks.append("\n".join(re.sub(r"\s+", " ", t).strip() for t in texts if t.strip()))
    return "\n\n".join(chunks)


def extract(path: Path, assets_dir: Path) -> tuple[str, dict]:
    suffix = path.suffix.lower()
    manifest = {"source": str(path), "type": suffix.lstrip("."), "assets": []}
    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="replace"), manifest
    if suffix == ".docx":
        doc = Document(str(path))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip()), manifest
    if suffix == ".pdf":
        doc = fitz.open(path)
        text = "\n\n".join(page.get_text("text") for page in doc)
        doc.close()
        return text, manifest
    if suffix == ".pptx":
        assets_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.startswith("ppt/media/"):
                    target = assets_dir / Path(name).name
                    target.write_bytes(z.read(name))
                    manifest["assets"].append(str(target))
        return pptx_text(path), manifest
    raise ValueError(f"Unsupported source type: {suffix}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    input_copy = args.outdir / "input" / args.source.name
    input_copy.parent.mkdir(parents=True, exist_ok=True)
    if args.source.resolve() != input_copy.resolve():
        shutil.copy2(args.source, input_copy)
    assets = args.outdir / "extracted_assets"
    text, manifest = extract(input_copy, assets)
    (args.outdir / "source_content.md").write_text(text.strip() + "\n", encoding="utf-8")
    manifest["content_path"] = str(args.outdir / "source_content.md")
    manifest["asset_dir"] = str(assets)
    manifest["character_count"] = len(text)
    (args.outdir / "source_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
