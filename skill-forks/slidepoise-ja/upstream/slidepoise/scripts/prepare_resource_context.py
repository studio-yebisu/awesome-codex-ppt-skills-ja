#!/usr/bin/env python3
"""Resolve the resource pool and build one generation context sheet."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from prepare_generation import augment_profile_core_references, augment_selected_components, enforce_resource_budgets, validate_resources, build_style_context
from make_asset_contact_sheet import collect_resource_review_items, build_contact_sheet, _svg_to_image

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def prepare_generation_previews(resources: dict, directory: Path) -> None:
    """Prepare raster transport for SVG references without replacing originals."""
    for field, path_key in (("selected_visual_references", "canonical_file"),
                            ("selected_components", "preview_file"),
                            ("selected_assets", "canonical_file")):
        for item in resources.get(field, []):
            if not item.get(path_key):
                continue
            source = Path(item[path_key]).expanduser().resolve()
            if source.suffix.lower() != '.svg':
                continue
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            image = _svg_to_image(source, 1024)
            if image is None:
                raise SystemExit(f"Could not prepare an SVG image attachment for {source}. Check the SVG rasterizer.")
            # Bind the bytes actually rasterized, even if a source is edited
            # concurrently with context preparation.
            if hashlib.sha256(source.read_bytes()).hexdigest() != source_hash:
                raise SystemExit(f"SVG source changed during context preparation. Run it again. {source}")
            directory.mkdir(parents=True, exist_ok=True)
            preview = directory / f'{source_hash}.png'
            image.save(preview, format='PNG')
            item['generation_preview'] = {
                'path': str(preview.resolve()), 'sha256': hashlib.sha256(preview.read_bytes()).hexdigest(),
                'source': {'path': str(source), 'sha256': source_hash},
                'dimensions_px': list(image.size), 'format': 'png',
            }

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--config',type=Path,required=True)
    p.add_argument('--intent',type=Path,required=True)
    p.add_argument('--resources',type=Path,required=True,help='Host-authored draft resource selection')
    p.add_argument('--output-resources',type=Path,required=True)
    p.add_argument('--sheet',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--columns',type=int,default=4)
    args=p.parse_args()
    config=load(args.config); intent=load(args.intent); resources=load(args.resources)
    profile=config.get('resolved_profile',{}) or {}
    resources=augment_profile_core_references(profile,resources,config.get('libraries'))
    resources=augment_selected_components(resources,str(profile.get('profile_id') or ''),config.get('libraries'))
    enforce_resource_budgets(config,resources); validate_resources(intent,resources)
    prepare_generation_previews(resources,args.sheet.parent / (args.sheet.stem + '-assets'))
    items=collect_resource_review_items(resources)
    resources['style_context']=build_style_context(config)
    sheet=build_contact_sheet(items,args.sheet,columns=args.columns,style_context=resources['style_context'],style_direction=resources.get('style_direction'))
    resources['generation_context_sheet']={
      'path':sheet['path'], 'labels':sheet['labels'], 'asset_count':sheet['asset_count'],
      'rendered_preview_count':sheet['rendered_preview_count'], 'purpose':'combined_style_assets_approval_and_generation'
    }
    args.output_resources.parent.mkdir(parents=True,exist_ok=True)
    args.output_resources.write_text(json.dumps(resources,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    manifest={'sheet':sheet,'style_context':resources['style_context'],'style_direction':resources.get('style_direction',{}),'selection_reasoning':resources.get('selection_reasoning',{}),'items':[{'asset_id':i.get('asset_id'),'label':i.get('contact_sheet_label'),'role':i.get('role'),'canonical_file':i.get('canonical_file') or i.get('preview_file')} for i in items]}
    args.manifest.parent.mkdir(parents=True,exist_ok=True)
    args.manifest.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'resources':str(args.output_resources.resolve()),'sheet':sheet,'manifest':str(args.manifest.resolve())},indent=2,ensure_ascii=False))

if __name__=='__main__': main()
