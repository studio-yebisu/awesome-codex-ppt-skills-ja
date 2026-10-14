import type { StyleDefinition } from "../../themes/types.js";
import { darkCss } from "./css.js";
import { titleLayout } from "./layouts/title.js";
import { sectionLayout } from "./layouts/section.js";
import { contentLayout } from "./layouts/content.js";
import { listLayout } from "./layouts/list.js";
import { tableLayout } from "./layouts/table.js";
import { cardGridLayout } from "./layouts/card-grid.js";
import { timelineLayout } from "./layouts/timeline.js";
import { statisticsLayout } from "./layouts/statistics.js";
import { imageRightLayout } from "./layouts/image-right.js";
import { terminalLayout } from "./layouts/terminal.js";
import { quoteLayout } from "./layouts/quote.js";
import { imageCenterLayout } from "./layouts/image-center.js";
import { processLayout } from "./layouts/process.js";
import { twoColumnLayout } from "./layouts/two-column.js";
import { bigStatementLayout } from "./layouts/big-statement.js";
import { highlightBoxLayout } from "./layouts/highlight-box.js";
import { progressBarLayout } from "./layouts/progress-bar.js";
import { chartBarLayout } from "./layouts/chart-bar.js";
import { timelineHorizontalLayout } from "./layouts/timeline-horizontal.js";
import { codeComparisonLayout } from "./layouts/code-comparison.js";
import { codeShowcaseLayout } from "./layouts/code-showcase.js";

export const darkStyle: StyleDefinition = {
  name: "dark",
  description: "Dark mode style with indigo and emerald accents, developer-friendly",
  compatibleThemes: [],
  css: darkCss,
  layouts: {
    title: titleLayout,
    section: sectionLayout,
    content: contentLayout,
    list: listLayout,
    table: tableLayout,
    "card-grid": cardGridLayout,
    timeline: timelineLayout,
    statistics: statisticsLayout,
    "image-right": imageRightLayout,
    terminal: terminalLayout,
    quote: quoteLayout,
    "image-center": imageCenterLayout,
    process: processLayout,
    "two-column": twoColumnLayout,
    "big-statement": bigStatementLayout,
    "highlight-box": highlightBoxLayout,
    "progress-bar": progressBarLayout,
    "chart-bar": chartBarLayout,
    "timeline-horizontal": timelineHorizontalLayout,
    "code-comparison": codeComparisonLayout,
    "code-showcase": codeShowcaseLayout,
  },
};
