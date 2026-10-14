/**
 * Default theme - Table layout
 */

import type { SlideLayout } from "../../types.js";
import { withLengthPrompt } from "../../../utils/text-length.js";

export const tableLayout: SlideLayout = {
  name: "table",
  description: "Table slide with description (max 7 rows)",
  params: {
    heading: {
      type: "string",
      description: withLengthPrompt("Slide heading", 54),
      required: true,
      maxLength: 54,
    },
    tableMarkdown: {
      type: "string",
      description:
        "Table in markdown format (max 7 rows excluding header, keep content concise for better width fit)",
      required: true,
    },
    description: {
      type: "string",
      description: withLengthPrompt("Table description below table", 75, {
        note: "no line break",
      }),
      required: false,
      maxLength: 75,
    },
    citations: {
      type: "string",
      description: withLengthPrompt("Citation", 130, {
        note: "no line break",
      }),
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    let slide = "";
    if (params.heading) {
      slide += `## ${params.heading}\n\n`;
    }

    slide += params.tableMarkdown;

    if (params.description) {
      slide += `\n\n${params.description}`;
    }

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
