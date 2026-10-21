"""Output-only SVG label placement adapter for aws-html-showcase pages 2 and 3.

The input PPTX step labels are left-aligned text boxes (PowerPoint renders them left-aligned;
no alignment flag was lost in conversion). This adapter declares a presentation change beyond
the original geometry: 15 labels are drawn at the x centre of an explicitly assigned shape with
text-anchor="middle". y, font and text stay as in the source. The Presentation object, input PPTX
and source bbox facts are only read, never modified. Not original upstream behaviour.
No imports: works on the python-pptx objects passed in by the caller.
"""

ADAPTER_ID = 'aws-html-showcase/pages02-03-label-center/v2'
PAGE_IDX = 2
SLIDE_COUNT = 5
CANVAS_PX = (1600, 900)
TOL = 0.01

# Exact page-3 shape order in input/deck.pptx (as recorded in extraction/native-shapes.json).
SHAPE_ORDER = ('C129', 'R130', 'C131', 'P132', 'L133', 'P134', 'L135', 'P136', 'L137', 'P138',
               'T139', 'T140', 'T141', 'T142', 'T143', 'T144', 'T145', 'T146', 'T147', 'T148',
               'T149', 'T150', 'T151', 'L152', 'T153', 'T154', 'T155', 'T156')

# target shape: (geometry, fill, source bbox_px [x, y, w, h])
TARGETS = {
    'C129': ('ellipse', 'd62828', (132.5, 326.25, 165.0, 165.0)),
    'R130': ('rect', '003049', (517.5, 326.25, 165.0, 165.0)),
    'C131': ('ellipse', 'd62828', (902.5, 326.25, 165.0, 165.0)),
    'P132': ('custGeom', 'ffd60a', (1253.75, 313.75, 220.0, 188.75)),
}

# label: (target shape, text, font family, font size px, source bbox_px [x, y, w, h])
LABELS = {
    'T140': ('C129', '01', 'Manrope', 43.75, (92.5, 547.5, 50.762, 65.625)),
    'T141': ('C129', '入口', 'Zen Kaku Gothic New', 46.25, (92.5, 608.75, 88.809, 69.375)),
    'T142': ('C129', 'ひとこと案内', 'BIZ UDPMincho', 30.0, (92.5, 688.75, 159.902, 45.0)),
    'T143': ('R130', '02', 'Manrope', 43.75, (477.5, 547.5, 50.762, 65.625)),
    'T144': ('R130', '見る', 'Zen Kaku Gothic New', 46.25, (477.5, 608.75, 88.809, 69.375)),
    'T145': ('R130', '作品を比べる', 'BIZ UDPMincho', 30.0, (477.5, 688.75, 172.519, 45.0)),
    'T146': ('C131', '03', 'Manrope', 43.75, (862.5, 547.5, 50.762, 65.625)),
    'T147': ('C131', '話す', 'Zen Kaku Gothic New', 46.25, (862.5, 608.75, 88.809, 69.375)),
    'T148': ('C131', '短い問いを置く', 'BIZ UDPMincho', 30.0, (862.5, 688.75, 197.715, 45.0)),
    'T149': ('P132', '04', 'Manrope', 43.75, (1247.5, 547.5, 50.762, 65.625)),
    'T150': ('P132', '持ち帰る', 'Zen Kaku Gothic New', 46.25, (1247.5, 608.75, 177.617, 69.375)),
    'T151': ('P132', '次の一歩を添える', 'BIZ UDPMincho', 30.0, (1247.5, 688.75, 229.219, 45.0)),
}


class LayoutAdapterError(ValueError):
    pass


def _fail(msg):
    raise LayoutAdapterError('layout_adapter: ' + msg + ' (input is not the expected aws-html-showcase deck.pptx)')


def _scale(prs):
    scale = CANVAS_PX[0] / prs.slide_width
    if abs(prs.slide_height * scale - CANVAS_PX[1]) > TOL:
        _fail('slide size is not 16:9 / %d x %d after normalization' % CANVAS_PX)
    return scale


def _bbox(sh, scale):
    return [round(v * scale, 3) for v in (sh.left, sh.top, sh.width, sh.height)]


def _same(a, b):
    return len(a) == len(b) and all(abs(x - y) <= TOL for x, y in zip(a, b))


def _check_target(sh, name, scale):
    geom, fill, bbox = TARGETS[name]
    el = sh._element
    if geom == 'custGeom':
        if not el.xpath('./p:spPr/a:custGeom/a:pathLst/a:path') or el.xpath('./p:spPr/a:prstGeom'):
            _fail(name + ' is not a custom-path triangle')
    elif el.xpath('./p:spPr/a:prstGeom/@prst') != [geom]:
        _fail(name + ' geometry is not ' + geom)
    if [v.lower() for v in el.xpath('./p:spPr/a:solidFill/a:srgbClr/@val')] != [fill]:
        _fail(name + ' fill is not #' + fill)
    actual = _bbox(sh, scale)
    if not _same(actual, bbox):
        _fail('%s bbox %r != source %r' % (name, actual, list(bbox)))
    return actual


def _check_label(sh, name, prs, scale):
    _, text, family, size_px, bbox = LABELS[name]
    if not sh.has_text_frame or sh.text != text:
        _fail('%s text is not %r' % (name, text))
    actual = _bbox(sh, scale)
    if not _same(actual, bbox):
        _fail('%s bbox %r != source %r' % (name, actual, list(bbox)))
    runs = [r for p in sh.text_frame.paragraphs for r in p.runs if r.text]
    if not runs:
        _fail(name + ' has no text runs')
    for r in runs:
        if r.font.size is None:
            _fail(name + ' run has no explicit font size')
        px = r.font.size.pt * CANVAS_PX[0] / (prs.slide_width / 914400 * 72)
        if abs(px - size_px) > TOL or (r.font.name or 'Zen Kaku Gothic New') != family:
            _fail('%s font is not %s %.2fpx' % (name, family, size_px))
    el = sh._element
    algn = el.xpath('./p:txBody/a:p/a:pPr/@algn') + el.xpath('./p:txBody/a:lstStyle/a:lvl1pPr/@algn')
    if any(a != 'l' for a in algn):
        _fail('%s is not a left-aligned text box (algn=%r)' % (name, algn))
    return actual, 'left (algn="l")' if algn else 'left (algn unset; text box default)'


def label_alignment(prs, slide, idx):
    """Return {label shape.name: placement record} for idx 2; {} for every other page."""
    # Codex follow-up: page2 labels use the centres of their actual source shapes.
    if idx == 1:
        scale = _scale(prs); by_name = {sh.name: sh for sh in slide.shapes}; records = {}
        for label, target, expected in [('T120','R114','場所'),('T121','C115','作品'),('T122','P116','言葉')]:
            sh=by_name[label]; shape=by_name[target]
            if sh.text != expected: _fail('page2 label content changed: '+label)
            box=_bbox(sh,scale); shape_box=_bbox(shape,scale)
            records[label]={'target_shape':target,'source_bbox_px':box,'source_alignment':'left; original input preserved','render_x_px':round(shape_box[0]+shape_box[2]/2,3),'render_anchor':'middle','content':expected}
        return records
    if idx != PAGE_IDX:
        return {}
    if len(prs.slides) != SLIDE_COUNT:
        _fail('slide count %d != %d' % (len(prs.slides), SLIDE_COUNT))
    if slide.slide_id != prs.slides[PAGE_IDX].slide_id:
        _fail('slide passed for idx 2 is not the third slide of prs')
    scale = _scale(prs)
    shapes = list(slide.shapes)
    names = tuple(sh.name for sh in shapes)
    if names != SHAPE_ORDER:
        _fail('page-3 shape names/order/count differ: %r' % (names,))
    by_name = dict(zip(names, shapes))
    centers = {}
    for name in TARGETS:
        x, _, w, _ = _check_target(by_name[name], name, scale)
        centers[name] = round(x + w / 2, 3)
    records = {}
    for name, (target, text, _, _, _) in LABELS.items():
        bbox, alignment = _check_label(by_name[name], name, prs, scale)
        records[name] = {
            'target_shape': target,
            'source_bbox_px': bbox,
            'source_alignment': alignment,
            'render_x_px': centers[target],
            'render_anchor': 'middle',
            'content': text,
        }
    if len(records) != 12:
        _fail('expected 12 labels, got %d' % len(records))
    return records


def audit_document(prs):
    """JSON-friendly declaration of what the adapter changes. Input validation only; no rendering."""
    mappings = []
    for idx, slide in enumerate(prs.slides):
        for name, rec in label_alignment(prs, slide, idx).items():
            mappings.append(dict(page=idx + 1, label=name, **rec))
    if len(mappings) != 15:
        _fail('expected 15 mappings, got %d' % len(mappings))
    return {
        'adapter_id': ADAPTER_ID,
        'scope': {
            'pages': [2,3],
            'labels': ['T120','T121','T122']+list(LABELS),
            'changed_output_attributes': ['svg text x', 'svg text-anchor'],
            'unchanged': ['input/deck.pptx', 'source bbox facts in extraction/native-shapes.json', 'label y/font/text',
                          'shapes/arrows/lines geometry and colors', 'pages 1, 4, 5'],
            'origin': 'declared output presentation adapter; not original aws-html-slides functionality',
        },
        'source_geometry_retained': True,
        'source_textboxes_modified_in_output_only': True,
        'mappings': mappings,
    }
