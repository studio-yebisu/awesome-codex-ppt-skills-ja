import type { SlideLayout } from "../../../themes/types.js";

export const imageRightLayout: SlideLayout = {
  name: "image-right",
  description: "Text on left, image on right on dark background (60:40 split)",
  className: "dk-img-right",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    list: {
      type: "array",
      description: "List items for the content side",
      required: true,
      maxItems: 10,
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
    let slide = `## ${params.heading}\n\n<div class="dk-split">\n\n<div class="dk-split-content">\n\n${listItems}\n\n</div>\n\n![](${params.imagePath})\n\n</div>`;

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
