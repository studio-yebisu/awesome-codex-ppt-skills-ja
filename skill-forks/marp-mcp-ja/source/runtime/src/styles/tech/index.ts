import type { StyleDefinition } from "../../themes/types.js";
import { techCss } from "./css.js";
import { titleLayout } from "./layouts/title.js";
import { sectionLayout } from "./layouts/section.js";
import { contentLayout } from "./layouts/content.js";
import { listLayout } from "./layouts/list.js";
import { twoColumnLayout } from "./layouts/two-column.js";
import { statisticsLayout } from "./layouts/statistics.js";
import { quoteLayout } from "./layouts/quote.js";
import { highlightBoxLayout } from "./layouts/highlight-box.js";
import { featureGridLayout } from "./layouts/feature-grid.js";
import { roadmapLayout } from "./layouts/roadmap.js";

export const techStyle: StyleDefinition = {
  name: "tech",
  description:
    "Modern tech/startup style with violet-cyan gradient accents, strong typography for product demos and engineering talks",
  compatibleThemes: [],
  css: techCss,
  layouts: {
    title: titleLayout,
    section: sectionLayout,
    content: contentLayout,
    list: listLayout,
    "two-column": twoColumnLayout,
    statistics: statisticsLayout,
    quote: quoteLayout,
    "highlight-box": highlightBoxLayout,
    "feature-grid": featureGridLayout,
    roadmap: roadmapLayout,
  },
};
