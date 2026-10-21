"""Apply pypdf stream compression to the current rendered PDF, as a local adapter.

This does not execute or replace the upstream Ghostscript gate.
"""
from pathlib import Path
import hashlib
import json
from pypdf import PdfReader, PdfWriter

CASE = Path(__file__).resolve().parents[1]
source = CASE / 'deck.pdf'
target = CASE / 'deck-lite.pdf'
reader = PdfReader(source)
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
for page in writer.pages:
    page.compress_content_streams()
with target.open('wb') as stream:
    writer.write(stream)
assert len(PdfReader(target).pages) == len(reader.pages)
receipt = {
    'author': 'Codex',
    'method': 'pypdf compress_content_streams; local PDF adapter',
    'input': 'deck.pdf',
    'output': 'deck-lite.pdf',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'output_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    'original_bytes': source.stat().st_size,
    'compressed_bytes': target.stat().st_size,
    'pages': len(reader.pages),
    'smaller': target.stat().st_size < source.stat().st_size,
    'original_ghostscript_gate': 'not executed; Ghostscript unavailable',
    'claim': 'A separate stream-compressed PDF was written. Size reduction is not assumed.'
}
(CASE / 'source/pdf-compression-repair.json').write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
