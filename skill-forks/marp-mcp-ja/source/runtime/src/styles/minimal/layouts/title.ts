import type { SlideLayout } from "../../../themes/types.js";

export const titleLayout: SlideLayout = {
  name: "title",
  description: "Clean black title slide with white text",
  className: "min-title",
  params: {
    heading: {
      type: "string",
      description: "Main heading text",
      required: true,
      maxLength: 80,
    },
    content: {
      type: "string",
      description: "Content like author info (markdown supported, keep concise)",
      required: false,
      maxLength: 500,
    },
    backgroundImage: {
      type: "string",
      description: "Optional background image path or URL",
      required: false,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: min-title -->\n`;
    if (params.backgroundImage) {
      slide += `\n![bg brightness:0.3](${params.backgroundImage})\n`;
    }
    slide += `\n# ${params.heading}`;
    if (params.content) {
      slide += `\n\n${params.content}`;
    }
    return slide;
  },
};
