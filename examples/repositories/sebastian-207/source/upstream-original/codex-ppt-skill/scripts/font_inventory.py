#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


TARGETS = [
    "Source Han Sans SC",
    "Noto Sans CJK SC",
    "Microsoft YaHei UI",
    "Microsoft YaHei",
    "DengXian",
    "Source Han Serif SC",
    "Noto Serif CJK SC",
    "SimSun",
    "SimHei",
    "Aptos",
    "Arial",
    "Inter",
    "Georgia",
    "Times New Roman",
]


def scan_windows_fonts() -> dict[str, list[str]]:
    font_dirs = [
        Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
        Path.home() / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts",
    ]
    found: dict[str, list[str]] = {name: [] for name in TARGETS}
    all_files: list[str] = []
    for font_dir in font_dirs:
        if not font_dir.exists():
            continue
        for path in font_dir.glob("*"):
            if path.suffix.lower() not in {".ttf", ".otf", ".ttc"}:
                continue
            all_files.append(path.name)
            low = path.name.lower()
            aliases = {
                "Microsoft YaHei UI": ["msyhl", "msyh", "yahei"],
                "Microsoft YaHei": ["msyh", "yahei"],
                "DengXian": ["deng"],
                "SimSun": ["simsun", "simsunb", "nsimsun"],
                "SimHei": ["simhei"],
                "Arial": ["arial"],
                "Times New Roman": ["times"],
                "Georgia": ["georgia"],
                "Aptos": ["aptos"],
                "Inter": ["inter"],
                "Noto Sans CJK SC": ["notosanscjksc", "noto sans cjk"],
                "Noto Serif CJK SC": ["notoserifcjksc", "noto serif cjk"],
                "Source Han Sans SC": ["sourcehansans", "source han sans"],
                "Source Han Serif SC": ["sourcehanserif", "source han serif"],
            }
            for family, needles in aliases.items():
                if any(n.replace(" ", "") in low.replace(" ", "") for n in needles):
                    found.setdefault(family, []).append(str(path))
    return {k: sorted(set(v)) for k, v in found.items()}


def choose_profiles(found: dict[str, list[str]]) -> dict[str, dict[str, str]]:
    def first(names: list[str], fallback: str) -> str:
        for name in names:
            if found.get(name):
                return name
        return fallback

    sans = first(["Source Han Sans SC", "Noto Sans CJK SC", "Microsoft YaHei UI", "Microsoft YaHei", "DengXian"], "Microsoft YaHei UI")
    alt_sans = first(["DengXian", "Microsoft YaHei UI", "Microsoft YaHei", "Arial"], sans)
    serif = first(["Source Han Serif SC", "Noto Serif CJK SC", "SimSun"], "SimSun")
    number = first(["Aptos", "Arial"], "Arial")
    return {
        "modern-corporate": {"heading": sans, "body": sans, "number": number},
        "technology-clean": {"heading": alt_sans, "body": sans, "number": number},
        "academic-sans": {"heading": sans, "body": sans, "number": number},
        "academic-serif": {"heading": serif, "body": serif, "number": first(["Times New Roman", "Georgia", "Arial"], number)},
        "editorial-modern": {"heading": alt_sans, "body": sans, "number": number},
        "government-formal": {"heading": sans, "body": first(["SimSun", "Microsoft YaHei UI", "Microsoft YaHei"], sans), "number": number},
        "education-friendly": {"heading": sans, "body": sans, "number": number},
        "premium-minimal": {"heading": alt_sans, "body": sans, "number": number},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-json", type=Path, default=Path("font_inventory.json"))
    parser.add_argument("--out-md", type=Path, default=Path("font_inventory.md"))
    args = parser.parse_args()

    found = scan_windows_fonts()
    profiles = choose_profiles(found)
    payload = {
        "status": "AVAILABLE" if any(found.values()) else "UNAVAILABLE_AFTER_INSTALL_ATTEMPT",
        "families": {k: {"available": bool(v), "files": v[:5]} for k, v in found.items()},
        "recommended_profiles": profiles,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# Font Inventory", "", f"Status: `{payload['status']}`", "", "## Families", ""]
    for family, info in payload["families"].items():
        mark = "yes" if info["available"] else "no"
        lines.append(f"- `{family}`: {mark}")
    lines.extend(["", "## Recommended Profiles", ""])
    for profile, mapping in profiles.items():
        lines.append(f"- `{profile}`: heading `{mapping['heading']}`, body `{mapping['body']}`, number `{mapping['number']}`")
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
