import type { StyleDefinition } from "../../themes/types.js";
import { minimalCss } from "./css.js";
import { titleLayout } from "./layouts/title.js";
import { sectionLayout } from "./layouts/section.js";
import { contentLayout } from "./layouts/content.js";
import { listLayout } from "./layouts/list.js";
import { tableLayout } from "./layouts/table.js";
import { imageRightLayout } from "./layouts/image-right.js";
import { imageCenterLayout } from "./layouts/image-center.js";
import { quoteLayout } from "./layouts/quote.js";
import { twoColumnLayout } from "./layouts/two-column.js";
import { bigStatementLayout } from "./layouts/big-statement.js";
import { statisticsLayout } from "./layouts/statistics.js";
import { highlightBoxLayout } from "./layouts/highlight-box.js";
import { pullQuoteLayout } from "./layouts/pull-quote.js";
import { agendaLayout } from "./layouts/agenda.js";
import { comparisonLayout } from "./layouts/comparison.js";

export const minimalStyle: StyleDefinition = {
  name: "minimal",
  description: "Clean, flat design with typography focus and minimal decoration",
  compatibleThemes: [],
  css: minimalCss,
  layouts: {
    title: titleLayout,
    section: sectionLayout,
    content: contentLayout,
    list: listLayout,
    table: tableLayout,
    "image-right": imageRightLayout,
    "image-center": imageCenterLayout,
    quote: quoteLayout,
    "two-column": twoColumnLayout,
    "big-statement": bigStatementLayout,
    statistics: statisticsLayout,
    "highlight-box": highlightBoxLayout,
    "pull-quote": pullQuoteLayout,
    agenda: agendaLayout,
    comparison: comparisonLayout,
  },
};
