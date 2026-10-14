"""Suggest 3 styles and one storytelling pattern for a deck, shuffled on every run.

Usage: python pick-styles.py "<mục đích, người xem, chất mong muốn>" [--parts N] [--seed N] [--no-history]
  --parts N  deck dài chia N phần: mỗi phần một nhịp kể khác nhau, slide chương xen kẽ nền

Why: the same brief on every machine used to give the same 3 "safe" styles, so a whole
class got look-alike decks. Each run now draws, at random among fitting candidates:
  1. hợp      a style whose mood / best_for match the brief best (random among the top 8)
  2. khác nền a fitting style on the other background (light vs dark)
  3. bất ngờ  a style outside the top group, for a fresh look
Styles used in the last runs on this machine (~/.slidefly/history.json) are skipped first.
It also draws one storytelling pattern (cách kể) with a suggested order of slide kinds.
"""
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
HISTORY = Path.home() / '.slidefly' / 'history.json'
KEEP = 9   # remember the last 3 runs

STORIES = [
    ('Mở bằng câu hỏi', 'cover > qa > agenda > section > content/process > compare-table > statement > cta'),
    ('Mở bằng một con số', 'cover > big-number > agenda > chapter > stats/bento > before-after > countdown > closing'),
    ('Mở bằng một tình huống', 'cover > split-photo hoặc portrait-quote > before-after > process > content > statement > cta'),
    ('Kết luận trước, giải thích sau', 'cover > statement > bento (tóm tắt) > section > content/two-col > compare-table > closing'),
]

# Rhythm of one part in a long deck (after its chapter slide). Drawn without repeats, so part 2
# does not replay part 1's order of slide kinds.
BEATS = [
    ('Hỏi rồi đáp', 'qa > content (frame split-left) > process (frame band) > statement'),
    ('Số liệu dẫn đường', 'big-number > stats (frame rail) hoặc bento > compare-table (frame band)'),
    ('Trước và sau', 'before-after > process (frame bottom) > content (frame numbered)'),
    ('Cho xem tận mắt', 'diagram + khung giao diện bên trái > diagram > content (frame diagonal)'),
    ('Xếp hạng', 'countdown > two-col (frame stack) > statement'),
    ('Vẽ ra cho dễ thấy', 'diagram (network, funnel...) > content (frame zigzag) > portrait-quote'),
    ('Chia ô', 'bento (frame corner) > timeline > content (frame poster)'),
    ('Khung lớn', 'content (frame split-right) > stats (frame poster) > two-col (frame frame)'),
]


def part_plan(n: int, rng: random.Random) -> list[str]:
    """One beat per part; even parts get the flooded chapter backdrop so chapters alternate too."""
    beats = rng.sample(BEATS, min(n, len(BEATS)))
    beats += [rng.choice(BEATS) for _ in range(n - len(beats))]
    out = []
    for i, (name, order) in enumerate(beats, 1):
        chap = 'chapter data-stage="closing" data-brand="corner"' if i % 2 == 0 else 'chapter'
        out.append(f'phần {i:<3} {name}: {chap} > {order}')
    return out


SERIOUS = {'trang', 'trọng', 'hội', 'đồng', 'nghiên', 'cứu', 'luận', 'án', 'văn', 'chính', 'sách', 'tài', 'chính', 'pháp', 'lý', 'y', 'tế'}
PLAYFUL = {'tinh', 'nghịch', 'tếu', 'hồn', 'nhiên', 'bừa', 'arcade', 'neon', 'geek', 'vui', 'tươi', 'nhộn'}


STOP = {'bài', 'cho', 'và', 'của', 'các', 'những', 'một', 'trước', 'với', 'theo', 'có', 'là', 'deck', 'slide'}


def words(text: str) -> set[str]:
    text = unicodedata.normalize('NFC', text.lower())
    return {w for w in re.findall(r'\w+', text) if len(w) > 1}


def pairs(text: str) -> set[str]:
    """Two-syllable words inside each comma-separated phrase."""
    out = set()
    for part in re.split(r'[,;.()/]', unicodedata.normalize('NFC', text.lower())):
        ws = re.findall(r'\w+', part)
        out |= {f'{a} {b}' for a, b in zip(ws, ws[1:])}
    return out


def main() -> int:
    argv = sys.argv[1:]   # brief words only: drop flags and the number after --seed / --parts
    args = [a for i, a in enumerate(argv) if not a.startswith('--') and (i == 0 or argv[i - 1] not in ('--seed', '--parts'))]
    if not args:
        print(__doc__)
        return 1
    seed = next((int(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == '--seed' and i + 1 < len(sys.argv)), None)
    rng = random.Random(seed)
    brief = words(' '.join(args))
    styles = json.loads((SK / 'assets' / 'styles' / 'index.json').read_text(encoding='utf-8'))
    use_history = '--no-history' not in sys.argv
    recent = set(json.loads(HISTORY.read_text(encoding='utf-8'))) if use_history and HISTORY.exists() else set()

    def score(s):
        # Vietnamese words are mostly two syllables ("trang trọng" vs "sang trọng"): match word pairs,
        # single syllables only break ties
        text = ', '.join(s['mood']) + ', ' + s['best_for']
        return 3 * len(pairs(' '.join(args)) & pairs(text)) + len((brief - STOP) & (words(text) - STOP)) * 0.2

    # a serious brief never gets a toy-like style, not even as the surprise
    serious = bool(brief & SERIOUS)
    if serious:
        styles = [s for s in styles if not words(' '.join(s['mood'])) & PLAYFUL]
    ranked = sorted(styles, key=lambda s: (-score(s), rng.random()))
    fresh = lambda pool: [s for s in pool if s['slug'] not in recent] or pool   # noqa: E731
    top = fresh([s for s in ranked[:8] if score(s) > 0] or ranked[:8])
    first = rng.choice(top)
    other = [s for s in ranked if s['scheme'] != first['scheme']]
    second = rng.choice(fresh([s for s in other if score(s) > 0][:10] or other[:10]))
    rest = fresh([s for s in ranked[8:] if s not in (first, second)])
    third = rng.choice(rest)
    story = rng.choice(STORIES)

    for tag, s in (('hợp', first), ('khác nền', second), ('bất ngờ', third)):
        print(f"{tag:9} {s['slug']:20} {s['name']} ({s['scheme']}): {s['best_for']}")
    print(f"cách kể  {story[0]}: {story[1]}")
    parts = next((int(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == '--parts' and i + 1 < len(sys.argv)), 0)
    for line in part_plan(parts, rng):
        print(line)
    if use_history:
        HISTORY.parent.mkdir(parents=True, exist_ok=True)
        last = json.loads(HISTORY.read_text(encoding='utf-8')) if HISTORY.exists() else []
        HISTORY.write_text(json.dumps((last + [first['slug'], second['slug'], third['slug']])[-KEEP:]), encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
