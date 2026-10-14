/**
 * Gaia theme - Table layout
 */

import type { SlideLayout } from "../../types.js";
import { withLengthPrompt } from "../../../utils/text-length.js";

export const tableLayout: SlideLayout = {
  name: "table",
  description: "Table slide with description (max 5 rows)",
  params: {
    heading: {
      type: "string",
      description: withLengthPrompt("Slide heading", 38),
      required: true,
      maxLength: 38,
    },
    tableMarkdown: {
      type: "string",
      description:
        "Table in markdown format (max 5 rows excluding header, keep content concise for better width fit)",
      required: true,
    },
    description: {
      type: "string",
      description: withLengthPrompt("Table description below table", 60, {
        note: "no line break",
      }),
      required: false,
      maxLength: 60,
    },
    citations: {
      type: "string",
      description: withLengthPrompt("Citation", 90, {
        note: "no line break",
      }),
      required: false,
      maxLength: 90,
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
