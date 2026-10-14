/**
 * Uncover theme - List layout
 */

import type { SlideLayout } from "../../types.js";
import {
  formatLengthPrompt,
  withLengthPrompt,
} from "../../../utils/text-length.js";

export const listLayout: SlideLayout = {
  name: "list",
  description: "List slide with bullet points (max 8 items)",
  params: {
    heading: {
      type: "string",
      description: withLengthPrompt("Slide heading", 28),
      required: true,
      maxLength: 28,
    },
    list: {
      type: "array",
      description: `List items (max 8 items, each ${formatLengthPrompt(45)})`,
      required: true,
      maxItems: 8,
      maxLength: 45,
    },
    citations: {
      type: "string",
      description: withLengthPrompt("Citation", 100, {
        note: "no line break",
      }),
      required: false,
      maxLength: 100,
    },
  },
  template: (params) => {
    let slide = "";
    if (params.heading) {
      slide += `## ${params.heading}\n\n`;
    }

    const list = params.list as string[];
    list.forEach((item: string) => {
      slide += `- ${item}\n`;
    });

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
