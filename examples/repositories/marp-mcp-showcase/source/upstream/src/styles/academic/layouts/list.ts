/**
 * Academic style - List layout
 */

import type { SlideLayout } from "../../../themes/types.js";

export const listLayout: SlideLayout = {
  name: "list",
  description: "Bullet point list with optional citations",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    list: {
      type: "array",
      description: "List items (max 8 items)",
      required: true,
      maxItems: 8,
      maxLength: 70,
    },
    citations: {
      type: "string",
      description: "Citation (no line break)",
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    let slide = `## ${params.heading}\n\n`;
    const list = params.list as string[];
    list.forEach((item: string) => {
      slide += `- ${item}\n`;
    });
    if (params.citations) {
      slide += `\n> ${params.citations}`;
    }
    return slide;
  },
};
