"""Portable native deck rebuild. No catalog, cache or PowerPoint dependency."""
from pathlib import Path
import argparse, json
import build_sol_editorial_showcase as design

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--input',type=Path,default=root/'input/storyline.json')
parser.add_argument('--output',type=Path,default=root/'deck-rebuilt.pptx')
args=parser.parse_args()
story=json.loads(args.input.read_text(encoding='utf-8-sig'))
design.builder.MckEngine=design.EditorialEngine
design.builder.DeckBuilder.build(story,str(args.output.resolve()))
