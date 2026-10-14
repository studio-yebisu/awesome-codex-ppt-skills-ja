/**
 * Academic style - Section divider layout
 */

import type { SlideLayout } from "../../../themes/types.js";

export const sectionLayout: SlideLayout = {
  name: "section",
  description: "Maroon section divider with optional number",
  className: "acad-section",
  params: {
    number: {
      type: "string",
      description: "Section number (e.g., '01', '1')",
      required: false,
      maxLength: 5,
    },
    title: {
      type: "string",
      description: "Section title",
      required: true,
      maxLength: 40,
    },
    subtitle: {
      type: "string",
      description: "Section subtitle",
      required: false,
      maxLength: 80,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: acad-section -->\n\n`;
    if (params.number) {
      slide += `<span class="acad-section-num">${params.number}</span>\n\n`;
    }
    slide += `## ${params.title}`;
    if (params.subtitle) {
      slide += `\n\n${params.subtitle}`;
    }
    return slide;
  },
};
