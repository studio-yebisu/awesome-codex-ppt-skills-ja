# 🎨 PPT Design System

> A design system skill distilled from [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) × [Open Design](https://github.com/nexu-io/open-design).
>
> **5 themes × 10 layouts × 3-tier typography system**, supporting both HTML and PPTX output.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-8A2BE2)](https://www.codebuddy.cn)

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 🎨 | **5 Refined Themes** | Indigo, Monocle, Forest, Dune, Minimal — covering engineering/business/training/creative/data scenarios |
| 📐 | **10 Layout Templates** | Cover, Big Numbers, Pipeline, Comparison, Quote — copy-paste ready |
| 🔤 | **3-Tier Typography** | Serif titles × Sans body × Mono metadata, magazine-grade typesetting |
| 📄 | **Dual Output** | HTML (best visual quality) + PPTX (editable, shareable) |
| 🚫 | **Anti-Pattern Checklist** | Built-in P0/P1/P2 quality gates to prevent AI slop |
| 🧩 | **WorkBuddy Native** | Install once, trigger with natural language |

---

## 🖌 5 Themes

| Theme | Scenario | Palette |
|-------|----------|---------|
| 🟦 **Indigo Porcelain** | Engineering reports, technical proposals | `#0a1f3d` + `#f1f3f5` |
| ⬛ **Monocle Classic** | Business presentations, project pitches | `#0a0a0b` + `#f1efea` |
| 🟩 **Forest Ink** | Training courses, educational materials | `#1a2e1f` + `#f5f1e8` |
| 🟫 **Dune** | Creative showcases, design sharing | `#1f1a14` + `#f0e6d2` |
| ⬜ **Minimal Data** | Data reports, dashboards | `#0c0c09` + `#f4f4f1` |

---

## 🚀 Quick Start

### Installation

Clone or download the repo to your WorkBuddy skills directory:

```bash
cp -r ppt-design-system ~/.workbuddy/skills/ppt-design-system
```

### Usage

After installation, tell WorkBuddy:

> _"Create a project progress report PPT"_
> _"Use Indigo Porcelain theme for quarterly review"_
> _"Make a training deck with Forest Ink"_

The system will guide through the workflow:
1. Confirm scenario → pick theme
2. Choose output format (HTML or PPTX)
3. Select layouts → fill content
4. Self-check → deliver

---

## 📂 Project Structure

```
ppt-design-system/
├── SKILL.md                    # Skill definition (workflow + design rules)
├── README.md / README.en.md    # Documentation
├── LICENSE                     # MIT License
├── .gitignore
├── references/
│   ├── themes.md               # 5 themes with CSS variables
│   ├── layouts.md              # 10 layout templates + CSS
│   └── presets.md              # Scenario recommendations
├── assets/
│   └── template.html           # Ready-to-run HTML template
└── examples/
    └── ...                     # Demo files
```

---

## 🙏 Credits

This skill is inspired by:

- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) by [歸藏](https://x.com/op7418) — Magazine-style web PPT skill
- [Open Design](https://github.com/nexu-io/open-design) by nexu-io — Open-source Claude Design alternative

---

## 📄 License

[MIT License](LICENSE)
