"""Install a deck's Google Fonts for the current Windows user, so PowerPoint shows the same type as the HTML deck.

Usage: python install-fonts.py <deck.html | style.css>

Reads the Google Fonts @import of the deck (or style), downloads the TTF files (cache: ~/.cache/slidefly/fonts),
copies them to %LOCALAPPDATA%\\Microsoft\\Windows\\Fonts and registers them under HKCU. No admin rights; remove
them from Settings > Personalization > Fonts. Fonts already installed are skipped.
"""
import ctypes
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx_fonts import CACHE, _get, _names, _tables, faces  # noqa: E402


def css_of(path):
    if path.suffix == '.css':
        return [path.read_text(encoding='utf-8')]
    from pptx_deck import load
    return load(path)[2]


def main():
    if len(sys.argv) < 2 or os.name != 'nt':
        print(__doc__ if len(sys.argv) < 2 else 'Windows only: on macOS open the .ttf files from ~/.cache/slidefly/fonts to install.')
        return 2
    import winreg
    dest = Path(os.environ['LOCALAPPDATA']) / 'Microsoft' / 'Windows' / 'Fonts'
    dest.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows NT\CurrentVersion\Fonts')
    done = 0
    for fam, italic, weight, url in faces(css_of(Path(sys.argv[1]))):
        src = CACHE / url.rsplit('/', 1)[-1]
        if not src.exists():
            src.write_bytes(_get(url))
        data = src.read_bytes()
        full = _names(data, _tables(data)).get(4, b'').decode('utf-16-be') or f'{fam} {weight}'
        target = dest / f'{full.replace(" ", "")}.ttf'
        if target.exists():
            print('  already installed:', full)
            continue
        shutil.copyfile(src, target)
        winreg.SetValueEx(key, f'{full} (TrueType)', 0, winreg.REG_SZ, str(target))
        ctypes.windll.gdi32.AddFontResourceW(str(target))
        done += 1
        print('  installed:', full)
    ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001D, 0, 0, 0, 1000, None)   # WM_FONTCHANGE to running apps
    print(f'{done} font file(s) installed. Restart PowerPoint to see them.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
