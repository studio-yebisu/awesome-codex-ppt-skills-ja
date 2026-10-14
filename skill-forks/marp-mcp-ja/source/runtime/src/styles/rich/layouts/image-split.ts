import type { SlideLayout } from "../../../themes/types.js";

export const imageSplitLayout: SlideLayout = {
  name: "image-split",
  description: "Image on the left with content list on the right (40:60 split)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    imageUrl: {
      type: "string",
      description: "Image URL or path",
      required: true,
    },
    items: {
      type: "array",
      description: "List items for the content side",
      required: true,
      maxItems: 8,
    },
  },
  template: (params) => {
    const items = params.items as string[];
    const listItems = items.map((item) => `- ${item}`).join("\n");
    return `## ${params.heading}\n\n<div class="image-split">\n\n![](${params.imageUrl})\n\n<div class="split-content">\n\n${listItems}\n\n</div>\n</div>`;
  },
};
