# Asset Sourcing For Consulting Decks

Use this shortlist when a deck needs premium-looking but free or open assets. Always verify the license on the asset page before embedding a specific file, especially when recognizable people, trademarks, logos, or buildings are visible.

Default policy: network assets are for reference, seed, or mood input only. Do not bundle third-party original files into this repo unless the user explicitly approves a reviewed CC0/public-domain asset. Final bundled assets should be self-generated, strongly transformed, and free of visible brands, people, trademarks, product UI, source marks, and consulting-firm cues.

## Photo And Video Sources

- [Unsplash](https://unsplash.com/license): high-quality editorial and business photography. Free commercial and non-commercial use; attribution is appreciated, and unmodified resale or building a competing image service is not allowed. Good searches: `enterprise technology`, `boardroom`, `data center`, `operations`, `factory automation`.
- [Pexels](https://www.pexels.com/license/): broad business photo and video library. Free commercial use; avoid implying endorsement by depicted people or brands. Good searches: `technology consulting`, `strategy workshop`, `AI office`, `manufacturing automation`.
- [Pixabay](https://pixabay.com/service/license-summary/): large collection across images, video, audio, and vectors. Free use with restrictions on standalone resale, trademarks, misleading use, and recognizable people.

## Illustration, Icon, And SVG Sources

- [Yesicon](https://yesicon.app/): curated index of open-source icon sets with license labels, including Lucide, Tabler, Remix, Iconoir, and IconPark.
- [Atlas Icons](https://iconsatlas.com/): MIT-licensed open-source icon packs with variable stroke styles; useful for monochrome consulting systems.
- [Flowbite Illustrations](https://flowbite.com/illustrations/): MIT-licensed SVG illustrations with attribution requirement; use only when attribution can be carried in appendix or provenance notes.
- [illlustrations.co](https://illlustrations.co/): simple open-source illustrations; useful for placeholder-lite decks when a photo would feel too generic.
- [unDraw](https://undraw.co/): open-license illustration library; useful for fast concept visuals when the style fits the deck.

## Pure JavaScript Visual Libraries

Use these only when the library is vendored locally or the resulting visual is converted into static HTML/CSS/SVG that can be embedded in the final package. Do not add CDN runtime dependencies to generated decks.

- [Chart.js](https://github.com/chartjs/Chart.js/blob/master/LICENSE.md): MIT-licensed canvas charts; useful for quick bar, line, doughnut, and scatter charts when native CSS charts are not enough.
- [Apache ECharts](https://github.com/apache/echarts): Apache-2.0-licensed charting library; use for complex dashboards, maps, Sankey, tree, and dense interaction.
- [Observable Plot](https://github.com/observablehq/plot): ISC-licensed SVG charts; useful for concise grammar-of-graphics charts embedded in static HTML.
- [D3](https://github.com/d3/d3): ISC-licensed low-level visualization toolkit; use when custom layouts or bespoke annotation logic justify the extra code.

## Curation Rules

- Prefer assets with neutral colors, authentic work settings, clean negative space, and no visible brand marks.
- For Mono decks, convert photos to grayscale and crop around clear business action: decision rooms, production lines, customer operations, or infrastructure.
- Avoid decorative AI imagery unless it directly explains the operating model; abstract neural-network backgrounds quickly look generic.
- Keep source records with asset URL, creator, license page, download date, and any attribution text.
- Do not bundle third-party assets into this repo unless the license permits redistribution.

## Web Inspiration Gate

Before using a network asset as reference or seed, record:

- asset URL
- license page URL
- access date
- intended visual role
- whether the original file enters the repo
- transformation approach
- risk notes for people, brands, trademarks, product UI, buildings, or source marks

Default values:

- original file enters the repo: `no`
- transformation approach: `strong transformation; use only abstract theme, mood, or composition principle`
- acceptable bundled output: self-generated bitmap or repo-native CSS/SVG primitive

Do not use network assets as seed/reference when they contain recognizable people, logos, product screenshots, proprietary dashboards, protected trade dress, confidentiality markings, or specific consulting-firm visual identifiers.
