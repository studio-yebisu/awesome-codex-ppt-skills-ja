/**
 * Academic style - Image-right layout
 */

import type { SlideLayout } from "../../../themes/types.js";

export const imageRightLayout: SlideLayout = {
  name: "image-right",
  description: "Content on left, image on right (60:40 split)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    list: {
      type: "array",
      description: "List items for the content side",
      required: true,
      maxItems: 8,
    },
    imagePath: {
      type: "string",
      description: "Image file path or URL",
      required: true,
    },
    citations: {
      type: "string",
      description: "Citation (no line break)",
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    const items = params.list as string[];
    const listItems = items.map((item) => `- ${item}`).join("\n");
    let slide = `## ${params.heading}\n\n<div class="acad-split">\n\n<div class="acad-split-content">\n\n${listItems}\n\n</div>\n\n![](${params.imagePath})\n\n</div>`;
    if (params.citations) {
      slide += `\n\n> ${params.citations}`;
    }
    return slide;
  },
};
