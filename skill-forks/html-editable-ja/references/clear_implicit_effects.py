"""Case adapter: a flat HTML input must not acquire Office theme shadows.

The original converter stays unchanged. Called immediately after its assemble,
before the original structural check and page-by-page visual audit.
"""
from pathlib import Path
from zipfile import ZipFile
import json
import re
from lxml import etree


def clear_implicit_effects(pptx):
    pptx = Path(pptx)
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    with ZipFile(pptx) as archive:
        content = {info.filename: (info, archive.read(info.filename)) for info in archive.infolist()}
    changes = []
    for name, (info, data) in content.items():
        if not re.fullmatch(r'ppt/slides/slide\d+\.xml', name):
            continue
        tree = etree.fromstring(data)
        count = 0
        for ref in tree.findall('.//p:style/a:effectRef', ns):
            if ref.get('idx') != '0':
                ref.set('idx', '0')
                count += 1
        if count:
            content[name] = (info, etree.tostring(tree, encoding='UTF-8', xml_declaration=True, standalone=True))
        changes.append({'part': name, 'implicit_effect_refs_cleared': count})
    temporary = pptx.with_suffix('.flat.tmp')
    with ZipFile(temporary, 'w') as archive:
        for info, data in content.values():
            archive.writestr(info, data)
    temporary.replace(pptx)
    report = {'scope': 'This case has no CSS shadows; clear implicit native shape theme effects only.',
              'original_converter_modified': False, 'geometry_text_fonts_unchanged': True, 'parts': changes}
    report_path = Path(__file__).parent / 'qa/implicit-effects.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + '\n', 'utf-8')
    print('[case-adapter] Cleared implicit theme effects before original Stage5 checks.')
