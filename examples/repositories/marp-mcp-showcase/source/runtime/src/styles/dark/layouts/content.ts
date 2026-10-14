import type { SlideLayout } from "../../../themes/types.js";

export const contentLayout: SlideLayout = {
  name: "content",
  description: "Free-form markdown content slide on dark background",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    body: {
      type: "string",
      description: "Free-form markdown body",
      required: true,
    },
  },
  template: (params) => {
    let slide = `## ${params.heading}\n\n`;
    slide += params.body;
    return slide;
  },
};
