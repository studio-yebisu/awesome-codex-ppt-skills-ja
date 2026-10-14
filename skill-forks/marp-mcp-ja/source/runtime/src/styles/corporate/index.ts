import type { StyleDefinition } from "../../themes/types.js";
import { corporateCss } from "./css.js";
import { titleLayout } from "./layouts/title.js";
import { sectionLayout } from "./layouts/section.js";
import { contentLayout } from "./layouts/content.js";
import { listLayout } from "./layouts/list.js";
import { tableLayout } from "./layouts/table.js";
import { twoColumnLayout } from "./layouts/two-column.js";
import { threeColumnLayout } from "./layouts/three-column.js";
import { statisticsLayout } from "./layouts/statistics.js";
import { processLayout } from "./layouts/process.js";
import { agendaLayout } from "./layouts/agenda.js";
import { imageRightLayout } from "./layouts/image-right.js";
import { highlightBoxLayout } from "./layouts/highlight-box.js";
import { quoteLayout } from "./layouts/quote.js";
import { imageCenterLayout } from "./layouts/image-center.js";
import { bigStatementLayout } from "./layouts/big-statement.js";
import { sidebarLayout } from "./layouts/sidebar.js";
import { progressBarLayout } from "./layouts/progress-bar.js";
import { chartBarLayout } from "./layouts/chart-bar.js";
import { pullQuoteLayout } from "./layouts/pull-quote.js";
import { quadrantLayout } from "./layouts/quadrant.js";

export const corporateStyle: StyleDefinition = {
  name: "corporate",
  description: "Professional business style with navy color scheme, structured layouts",
  compatibleThemes: [],
  css: corporateCss,
  layouts: {
    title: titleLayout,
    section: sectionLayout,
    content: contentLayout,
    list: listLayout,
    table: tableLayout,
    "two-column": twoColumnLayout,
    "three-column": threeColumnLayout,
    statistics: statisticsLayout,
    process: processLayout,
    agenda: agendaLayout,
    "image-right": imageRightLayout,
    "highlight-box": highlightBoxLayout,
    quote: quoteLayout,
    "image-center": imageCenterLayout,
    "big-statement": bigStatementLayout,
    sidebar: sidebarLayout,
    "progress-bar": progressBarLayout,
    "chart-bar": chartBarLayout,
    "pull-quote": pullQuoteLayout,
    quadrant: quadrantLayout,
  },
};
