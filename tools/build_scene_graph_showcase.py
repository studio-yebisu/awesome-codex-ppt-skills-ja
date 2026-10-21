"""Run the original OutlineSpec/create_from_outline -> beautify API route."""
from pathlib import Path
import json, sys, importlib.metadata as metadata

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/scene-graph-showcase' if (ROOT/'examples').exists() else ROOT


def build():
    src=CASE/'source'
    sys.path.insert(0,str(src/'runtime'))
    import ppt_scene_graph
    from ppt_scene_graph import create_from_outline, beautify
    from ppt_scene_graph.pipeline import OutlineSpec, SlideSpec
    from ppt_scene_graph.design import load_theme, FONT_SIZES
    import pptx
    sys.path.insert(0,str(src))
    from theme_layout_adapter import prepare_draft, migrate_decor, record as repair_record
    payload=json.loads((CASE/'input/outline.json').read_text(encoding='utf-8'))
    outline=OutlineSpec(title=payload['title'],subtitle=payload['subtitle'],slides=[SlideSpec(**x) for x in payload['slides']])
    create_from_outline(outline,theme='designhub_warm',output_path=str(CASE/'draft.pptx'))
    geometry=prepare_draft(CASE/'draft.pptx',outline.slides)
    # The original beautify validation accepts display names, not documented short keys.
    projection=load_theme('projection')
    beautify(str(CASE/'draft.pptx'),theme=projection.name,output_path=str(CASE/'deck.pptx'))
    decor=migrate_decor(CASE/'deck.pptx',load_theme('designhub_warm'),projection)
    repair_record(src/'theme-layout-repair.json',geometry,decor)
    mapping={'draft_theme_key':'designhub_warm','draft_theme_name':load_theme('designhub_warm').name,'final_theme_key':'projection','beautify_theme_argument':projection.name,'reason_for_display_name':'Original beautify checks list_themes() display names; projection short key would be rejected','font_title':projection.font_title,'font_body':projection.font_body,'font_sizes_pt':{k:v.pt for k,v in FONT_SIZES.items()},'font_size_note':'These are upstream code choices, not empirically verified optimal sizes','final_palette':{key:str(getattr(projection,key)) for key in ['bg','text_title','text_body','primary','secondary','accent']},'nontext_shape_note':'Original beautify leaves existing fills. Explicit local adapter migrates old primary/accent fills and normalizes/deduplicates left bars; not unmodified upstream behavior.','source_factories':[x.type for x in outline.slides]}
    (CASE/'input/theme-source-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    record={'route':'Original OutlineSpec/SlideSpec -> create_from_outline(designhub_warm) -> draft.pptx -> original beautify(load_theme(projection).name) -> deck.pptx','source_package':'source/runtime/ppt_scene_graph','pptx_engine_path':str(Path(pptx.__file__).relative_to(CASE)),'pptx_version':pptx.__version__,'parse_slide_available':hasattr(ppt_scene_graph,'parse_slide'),'evaluate_run':False,'theme_source_map':'input/theme-source-map.json','dependency_versions':{k:metadata.version(k) for k in ['lxml','Pillow','typing_extensions','XlsxWriter']},'native_elements':'text boxes and rectangle shapes from original factories/decor','local_changes':'Japanese font mapping; original factories and size tokens retained. Explicit local geometry adapter separates section number/title and cover subtitle; final decor adapter migrates old fills and deduplicates bars. See theme-layout-repair.json.','notes_support':'SlideSpec.notes field accepted but original create code does not write speaker notes; manuscript notes remain in input'}
    (src/'BUILD.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Original API route completed: draft and projection deck, no evaluate.')


if __name__=='__main__':build()
