import type { SlideLayout } from "../../../themes/types.js";

export const imageComparisonLayout: SlideLayout = {
  name: "image-comparison",
  description: "Two images side by side with labels for comparison",
  className: "image-comparison",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    image1Url: {
      type: "string",
      description: "First image URL or path",
      required: true,
    },
    image1Label: {
      type: "string",
      description: "Label for the first image",
      required: true,
      maxLength: 60,
    },
    image2Url: {
      type: "string",
      description: "Second image URL or path",
      required: true,
    },
    image2Label: {
      type: "string",
      description: "Label for the second image",
      required: true,
      maxLength: 60,
    },
  },
  template: (params) => {
    return `## ${params.heading}\n\n<div class="image-comparison">\n<div class="comparison-item">\n\n![](${params.image1Url})\n\n<p class="comparison-label">${params.image1Label}</p>\n</div>\n<div class="comparison-item">\n\n![](${params.image2Url})\n\n<p class="comparison-label">${params.image2Label}</p>\n</div>\n</div>`;
  },
};
