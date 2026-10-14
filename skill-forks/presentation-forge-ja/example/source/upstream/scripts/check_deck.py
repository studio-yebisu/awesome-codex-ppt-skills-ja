#!/usr/bin/env python3
"""Look at a built deck the way a reviewer would, with headless Chrome.

Renders the deck's index.html without opening any window, then:

  * reports layout problems on each slide - content poking out of the
    1920x1080 canvas, content cut off inside its own box (a long code line, a
    card too small for its text), images that failed to load;
  * saves a contact sheet of every slide (problem slides outlined in red);
  * saves a full image of each slide with a problem, or of the slides you ask
    for - so you can look at the result before handing the deck over.

Slides are rendered finished: every fragment shown, no animation.

    python3 check_deck.py <deck>                  # report + contact sheet + problem slides
    python3 check_deck.py <deck> --slides 3,5-7   # also these slides (or "all")
    python3 check_deck.py <deck> --no-shots       # report only

<deck> is the deck folder or its index.html - build it first. Images go to a
temporary folder (printed at the end) unless you pass --out. Exit status: 0 no
problems, 1 problems found, 2 could not check (no browser, no index.html).

Needs Chrome, Chromium, Edge or Brave installed (or CHROME_PATH set). Never
installs one: without a browser, say so and skip the visual check.
Standard library only.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DESIGN_W, DESIGN_H = 1920, 1080
REPORT_RE = re.compile(r'<script[^>]*\bid="pf-report"[^>]*>(.*?)</script>', re.DOTALL)

BROWSER_PATHS = {
    "darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ],
    "win32": [
        r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
        r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
        r"%LocalAppData%\Google\Chrome\Application\chrome.exe",
        r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
        r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
    ],
}
BROWSER_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "microsoft-edge", "msedge", "brave-browser", "chrome"]


def find_browser() -> str | None:
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).is_file():
        return env
    for raw in BROWSER_PATHS.get(sys.platform, []):
        path = os.path.expandvars(raw)
        if Path(path).is_file():
            return path
    for name in BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def run_browser(browser: str, url: str, *, width: int, height: int, scale: float = 1.0,
                screenshot: Path | None = None, timeout: float = 90) -> str:
    """Render url headlessly; return the DOM after scripts ran, or write a
    screenshot. Some Chrome builds never exit after a headless job, so this
    watches for the result and then stops the browser itself."""
    with tempfile.TemporaryDirectory(prefix="pf-chrome-", ignore_cleanup_errors=True) as profile:
        out_path = Path(profile) / "dom.html"
        cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
               "--no-first-run", "--no-default-browser-check", "--disable-extensions",
               "--disable-background-networking", "--disable-component-update",
               "--use-mock-keychain", f"--user-data-dir={profile}",
               "--virtual-time-budget=4000", f"--window-size={width},{height}",
               f"--force-device-scale-factor={scale}"]
        if sys.platform.startswith("linux"):
            # CI runners and containers often forbid Chrome's sandbox; this
            # only ever renders the deck that was just built on this machine.
            cmd.append("--no-sandbox")
        cmd += [f"--screenshot={screenshot}"] if screenshot else ["--dump-dom"]
        cmd.append(url)

        with open(out_path, "wb") as sink:
            proc = subprocess.Popen(cmd, stdout=sink, stderr=subprocess.DEVNULL)
            deadline = time.time() + timeout
            last_size = -1
            try:
                while time.time() < deadline:
                    if screenshot:
                        if screenshot.is_file():
                            size = screenshot.stat().st_size
                            if size and size == last_size:
                                break
                            last_size = size
                    elif b"</html>" in out_path.read_bytes()[-64:]:
                        break
                    if proc.poll() is not None and not screenshot:
                        break
                    time.sleep(0.25)
                else:
                    raise TimeoutError(f"the browser did not finish rendering {url}")
            finally:
                if proc.poll() is None:
                    proc.kill()
                proc.wait()
        return "" if screenshot else out_path.read_text(encoding="utf-8", errors="replace")


def parse_slides(spec: str, count: int) -> list[int]:
    if spec == "all":
        return list(range(1, count + 1))
    picked = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        lo, _, hi = part.partition("-")
        start, end = int(lo), int(hi or lo)
        picked.update(n for n in range(start, end + 1) if 1 <= n <= count)
    return sorted(picked)


def describe(issue: dict) -> str:
    where = f"slide {issue['slide']}" + (f" ({issue['file']})" if issue.get("file") else "")
    what = issue.get("element", "")
    text = f' "{issue["text"]}"' if issue.get("text") else ""
    if issue["kind"] == "overflow":
        return f"{where}: {what}{text} goes past the {issue['edge']} edge by {issue['px']}px"
    if issue["kind"] == "clipped":
        return f"{where}: {what}{text} is cut off inside its own box ({issue['px']}px hidden)"
    if issue["kind"] == "image":
        return f"{where}: image failed to load: {issue.get('text', '')}"
    return f"{where}: {issue['kind']}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("deck", help="deck folder, or its built index.html")
    ap.add_argument("--slides", default="", help='also image these slides: "3", "2,5-7" or "all"')
    ap.add_argument("--out", help="folder for the images (default: a temporary folder)")
    ap.add_argument("--scale", type=float, default=0.5,
                    help="slide image scale, 1 = full 1920x1080 (default 0.5)")
    ap.add_argument("--no-shots", action="store_true", help="report only, no images")
    args = ap.parse_args()

    target = Path(args.deck).resolve()
    index = target / "index.html" if target.is_dir() else target
    if not index.is_file():
        print(f"error: no built deck at {index} - run build.py first", file=sys.stderr)
        return 2
    browser = find_browser()
    if not browser:
        print("No Chrome, Chromium, Edge or Brave found (set CHROME_PATH to use another "
              "Chromium browser). Skipping the visual check.", file=sys.stderr)
        return 2

    base_url = index.as_uri()
    try:
        dom = run_browser(browser, base_url + "?pf=sheet", width=DESIGN_W, height=DESIGN_H)
    except (OSError, TimeoutError) as e:
        print(f"error: could not render the deck: {e}", file=sys.stderr)
        return 2
    # The report is the last element the engine adds to the page.
    found = REPORT_RE.findall(dom)
    match = found[-1] if found else None
    if not match:
        print("error: the deck produced no layout report - was it built with this "
              "version of Presentation Forge?", file=sys.stderr)
        return 2
    report = json.loads(match)
    count, issues = report["slides"], report["issues"]

    print(f"Checked {index.name}: {count} slides")
    for issue in issues:
        print(f"  ! {describe(issue)}")
    if issues:
        print(f"{len(issues)} problem(s) found.")
    else:
        print("  no layout problems found")

    if not args.no_shots:
        out = Path(args.out) if args.out else (
            Path(tempfile.gettempdir()) / "presentation-forge-check" / index.parent.name)
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("*.png"):
            old.unlink()
        sheet = out / "sheet.png"
        wanted = sorted(set(parse_slides(args.slides, count)) | {i["slide"] for i in issues})
        shots = {n: out / f"slide-{n:02d}.png" for n in wanted}
        jobs = [(base_url + "?pf=sheet", DESIGN_W, max(int(report.get("sheetHeight") or 0), 400), 1.0, sheet)]
        jobs += [(f"{base_url}?pf=shot#{n}", DESIGN_W, DESIGN_H, args.scale, path)
                 for n, path in shots.items()]
        try:
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(lambda j: run_browser(browser, j[0], width=j[1], height=j[2],
                                                    scale=j[3], screenshot=j[4]), jobs))
        except (OSError, TimeoutError) as e:
            print(f"error: could not capture the slides: {e}", file=sys.stderr)
            return 2
        print(f"Contact sheet: {sheet}" + ("  (problem slides outlined in red)" if issues else ""))
        for n, path in shots.items():
            print(f"Slide {n}: {path}")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
