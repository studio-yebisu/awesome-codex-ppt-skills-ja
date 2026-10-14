import type { StyleDefinition } from "../../themes/types.js";
import { richCss } from "./css.js";
import { titleLayout } from "./layouts/title.js";
import { sectionLayout } from "./layouts/section.js";
import { listLayout } from "./layouts/list.js";
import { tableLayout } from "./layouts/table.js";
import { imageRightLayout } from "./layouts/image-right.js";
import { imageCenterLayout } from "./layouts/image-center.js";
import { imageSplitLayout } from "./layouts/image-split.js";
import { timelineLayout } from "./layouts/timeline.js";
import { cardGridLayout } from "./layouts/card-grid.js";
import { statisticsLayout } from "./layouts/statistics.js";
import { highlightBoxLayout } from "./layouts/highlight-box.js";
import { twoColumnPanelLayout } from "./layouts/two-column-panel.js";
import { threeColumnPanelLayout } from "./layouts/three-column-panel.js";
import { imageComparisonLayout } from "./layouts/image-comparison.js";
import { contentLayout } from "./layouts/content.js";
import { quoteLayout } from "./layouts/quote.js";
import { processLayout } from "./layouts/process.js";
import { twoColumnLayout } from "./layouts/two-column.js";
import { bigStatementLayout } from "./layouts/big-statement.js";
import { sidebarLayout } from "./layouts/sidebar.js";
import { progressBarLayout } from "./layouts/progress-bar.js";
import { chartBarLayout } from "./layouts/chart-bar.js";
import { timelineHorizontalLayout } from "./layouts/timeline-horizontal.js";
import { pullQuoteLayout } from "./layouts/pull-quote.js";
import { bentoGridLayout } from "./layouts/bento-grid.js";

export const richStyle: StyleDefinition = {
  name: "rich",
  description: "Rich visual style with cards, timelines, grids, gradients, and more",
  compatibleThemes: [],
  css: richCss,
  layouts: {
    title: titleLayout,
    section: sectionLayout,
    list: listLayout,
    table: tableLayout,
    "image-right": imageRightLayout,
    "image-center": imageCenterLayout,
    "image-split": imageSplitLayout,
    timeline: timelineLayout,
    "card-grid": cardGridLayout,
    statistics: statisticsLayout,
    "highlight-box": highlightBoxLayout,
    "two-column-panel": twoColumnPanelLayout,
    "three-column-panel": threeColumnPanelLayout,
    "image-comparison": imageComparisonLayout,
    content: contentLayout,
    quote: quoteLayout,
    process: processLayout,
    "two-column": twoColumnLayout,
    "big-statement": bigStatementLayout,
    sidebar: sidebarLayout,
    "progress-bar": progressBarLayout,
    "chart-bar": chartBarLayout,
    "timeline-horizontal": timelineHorizontalLayout,
    "pull-quote": pullQuoteLayout,
    "bento-grid": bentoGridLayout,
  },
};
