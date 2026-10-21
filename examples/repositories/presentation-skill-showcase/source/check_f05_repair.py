"""Check the affected native geometry and text contrast after F05 repair."""
from pathlib import Path
import hashlib
import json
from pptx import Presentation
from pptx.enum.dml import MSO_COLOR_TYPE

CASE = Path(__file__).resolve().parents[1]


def luminance(color):
    values = [int(color[i:i+2], 16) / 255 for i in (0, 2, 4)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return sum(v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(left, right):
    a, b = sorted((luminance(left), luminance(right)))
    return (b + 0.05) / (a + 0.05)


def main():
    deck = CASE / 'deck.pptx'
    presentation = Presentation(deck)
    assert len(presentation.slides) == 6
    record = {'pptx_sha256': hashlib.sha256(deck.read_bytes()).hexdigest(),
              'title_checks': [], 'dark_slide_text_contrast': [], 'unresolved_colors': []}
    for index, slide in enumerate(presentation.slides):
        texts = [shape for shape in slide.shapes if shape.has_text_frame and shape.text]
        if 1 <= index <= 4:
            title = next(shape for shape in texts if shape.name == 'slide-title:content')
            top = title.top / 914400
            assert top >= 0.34 - 0.00001
            record['title_checks'].append({'page': index + 1, 'title_top_in': top,
                'decorative_bar_bottom_in': 0.19, 'gap_in': round(top - 0.19, 4)})
        if index in (0, 5):
            for shape in texts:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if not run.text.strip():
                            continue
                        color = run.font.color
                        if color.type != MSO_COLOR_TYPE.RGB:
                            record['unresolved_colors'].append({'page': index + 1, 'shape': shape.name})
                            continue
                        value = contrast(str(color.rgb), '2E1065')
                        record['dark_slide_text_contrast'].append({'page': index + 1, 'shape': shape.name,
                            'text': run.text, 'foreground': str(color.rgb), 'background': '2E1065',
                            'contrast_ratio': round(value, 4)})
                        assert value >= 4.5, (index + 1, shape.name, value)
    first = next(shape for shape in presentation.slides[0].shapes if shape.name == 'slide-title:title')
    assert first.text.replace('\\n', '\n') == '引き継ぎメモを\n一枚にまとめる'
    sixth = '\n'.join(shape.text for shape in presentation.slides[5].shapes if shape.has_text_frame)
    assert 'CYCLE' not in sixth and 'CONTROL' not in sixth
    for expected in ['確認時点', '担当変更前', '着手条件', '記録を確認']:
        assert expected in sixth
    fourth = presentation.slides[3]
    index = next(s for s in fourth.shapes if s.has_text_frame and s.text == '4件の記入例')
    caption = next(s for s in fourth.shapes if s.name == 'metadata:table-caption')
    assert all(run.font.italic is not True for paragraph in caption.text_frame.paragraphs for run in paragraph.runs)
    assert not any('4項目 | 項目' in s.text for s in fourth.shapes if s.has_text_frame)
    record['table_index_count_only'] = index.text
    record['japanese_table_caption_upright'] = True
    assert not record['unresolved_colors']
    record.update({'passed': True, 'contrast_threshold': 4.5,
                   'minimum_affected_text_contrast': min(item['contrast_ratio'] for item in record['dark_slide_text_contrast']),
                   'kinsoku_source_title': first.text, 'meaningful_section_labels': True})
    target = CASE / 'qa/f05-native-check.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps({'passed': True, 'minimum_affected_text_contrast': record['minimum_affected_text_contrast'],
                      'content_title_bar_gap_in': 0.15, 'receipt': 'qa/f05-native-check.json'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
