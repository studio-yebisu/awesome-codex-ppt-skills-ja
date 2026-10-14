"""SlideFly -> PPTX: the boilerplate parts every package needs (one master, one blank layout, a theme)."""
from xml.sax.saxutils import escape

from pptx_xml import NS, PKG, REL

HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
CT = 'application/vnd.openxmlformats-officedocument'
IMG_TYPES = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'gif': 'image/gif', 'svg': 'image/svg+xml', 'webp': 'image/webp'}


def theme(fonts):
    major, minor = (escape(f, {'"': '&quot;'}) for f in fonts)
    clr = ''.join(f'<a:{n}><a:srgbClr val="{v}"/></a:{n}>' for n, v in (
        ('dk1', '000000'), ('lt1', 'FFFFFF'), ('dk2', '1F2937'), ('lt2', 'F3F4F6'), ('accent1', '2563EB'), ('accent2', 'DB2777'),
        ('accent3', '059669'), ('accent4', 'D97706'), ('accent5', '7C3AED'), ('accent6', 'DC2626'), ('hlink', '2563EB'), ('folHlink', '7C3AED')))
    solid = '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    ln = '<a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    return (f'{HEAD}<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="SlideFly"><a:themeElements>'
            f'<a:clrScheme name="SlideFly">{clr}</a:clrScheme>'
            f'<a:fontScheme name="SlideFly"><a:majorFont><a:latin typeface="{major}"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
            f'<a:minorFont><a:latin typeface="{minor}"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
            f'<a:fmtScheme name="SlideFly"><a:fillStyleLst>{solid * 3}</a:fillStyleLst><a:lnStyleLst>{ln * 3}</a:lnStyleLst>'
            '<a:effectStyleLst>' + '<a:effectStyle><a:effectLst/></a:effectStyle>' * 3 + '</a:effectStyleLst>'
            f'<a:bgFillStyleLst>{solid * 3}</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>')


TREE = ('<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>')


def package_parts(n, title, fonts, images):
    exts = sorted({fname.rsplit('.', 1)[-1].lower() for imgs in images for fname, _ in imgs.values()})
    defaults = ''.join(f'<Default Extension="{x}" ContentType="{IMG_TYPES.get(x, "application/octet-stream")}"/>' for x in exts)
    slides_ct = ''.join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="{CT}.presentationml.slide+xml"/>' for i in range(1, n + 1))
    parts = {
        '[Content_Types].xml': (
            f'{HEAD}<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            f'<Default Extension="xml" ContentType="application/xml"/>{defaults}'
            f'<Override PartName="/ppt/presentation.xml" ContentType="{CT}.presentationml.presentation.main+xml"/>'
            f'<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="{CT}.presentationml.slideMaster+xml"/>'
            f'<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="{CT}.presentationml.slideLayout+xml"/>'
            f'<Override PartName="/ppt/theme/theme1.xml" ContentType="{CT}.theme+xml"/>'
            f'<Override PartName="/ppt/presProps.xml" ContentType="{CT}.presentationml.presProps+xml"/>'
            f'<Override PartName="/ppt/viewProps.xml" ContentType="{CT}.presentationml.viewProps+xml"/>'
            f'<Override PartName="/ppt/tableStyles.xml" ContentType="{CT}.presentationml.tableStyles+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            f'<Override PartName="/docProps/app.xml" ContentType="{CT}.extended-properties+xml"/>{slides_ct}</Types>'),
        '_rels/.rels': (
            f'{HEAD}<Relationships xmlns="{PKG}"><Relationship Id="rId1" Type="{REL}/officeDocument" Target="ppt/presentation.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            f'<Relationship Id="rId3" Type="{REL}/extended-properties" Target="docProps/app.xml"/></Relationships>'),
        'docProps/core.xml': (
            f'{HEAD}<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(title) + '</dc:title><dc:creator>SlideFly</dc:creator></cp:coreProperties>'),
        'docProps/app.xml': (f'{HEAD}<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                             f'<Application>SlideFly</Application><Slides>{n}</Slides></Properties>'),
        'ppt/presentation.xml': (
            f'{HEAD}<p:presentation {NS} saveSubsetFonts="1"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            '<p:sldIdLst>' + ''.join(f'<p:sldId id="{255 + i}" r:id="rId{i + 10}"/>' for i in range(1, n + 1)) + '</p:sldIdLst>'
            '<p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>'),
        'ppt/_rels/presentation.xml.rels': (
            f'{HEAD}<Relationships xmlns="{PKG}"><Relationship Id="rId1" Type="{REL}/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
            f'<Relationship Id="rId2" Type="{REL}/theme" Target="theme/theme1.xml"/>'
            f'<Relationship Id="rId3" Type="{REL}/presProps" Target="presProps.xml"/>'
            f'<Relationship Id="rId4" Type="{REL}/viewProps" Target="viewProps.xml"/>'
            f'<Relationship Id="rId5" Type="{REL}/tableStyles" Target="tableStyles.xml"/>'
            + ''.join(f'<Relationship Id="rId{i + 10}" Type="{REL}/slide" Target="slides/slide{i}.xml"/>' for i in range(1, n + 1))
            + '</Relationships>'),
        'ppt/presProps.xml': f'{HEAD}<p:presentationPr {NS}/>',
        'ppt/viewProps.xml': f'{HEAD}<p:viewPr {NS}/>',
        'ppt/tableStyles.xml': f'{HEAD}<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}}"/>',
        'ppt/theme/theme1.xml': theme(fonts),
        'ppt/slideMasters/slideMaster1.xml': (
            f'{HEAD}<p:sldMaster {NS}>{TREE}<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
            'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
            '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>'),
        'ppt/slideMasters/_rels/slideMaster1.xml.rels': (
            f'{HEAD}<Relationships xmlns="{PKG}"><Relationship Id="rId1" Type="{REL}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            f'<Relationship Id="rId2" Type="{REL}/theme" Target="../theme/theme1.xml"/></Relationships>'),
        'ppt/slideLayouts/slideLayout1.xml': f'{HEAD}<p:sldLayout {NS} type="blank" preserve="1">{TREE}<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>',
        'ppt/slideLayouts/_rels/slideLayout1.xml.rels': (
            f'{HEAD}<Relationships xmlns="{PKG}"><Relationship Id="rId1" Type="{REL}/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>'),
    }
    return parts
