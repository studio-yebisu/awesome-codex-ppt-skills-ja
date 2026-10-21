# Typography System

Use Chinese-capable fonts first. A deck may use at most two font families and three weights per page. Chinese body text defaults to left alignment and should not shrink below 16 pt for projection decks.

## Default Ranges

- Cover title: 34-52 pt
- Section title: 28-40 pt
- Content title: 24-32 pt
- Body: 16-22 pt
- Chart labels: 12-16 pt
- Auxiliary text: 11-14 pt
- KPI numbers: 30-52 pt

## Font Profiles

- modern-corporate
- technology-clean
- academic-sans
- academic-serif
- editorial-modern
- government-formal
- education-friendly
- premium-minimal

Each profile resolves to a real fallback chain recorded in `design-system/tokens/typography.json` and verified by `scripts/font_inventory.py`.
