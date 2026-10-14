import type { SlideLayout } from "../../../themes/types.js";

export const listLayout: SlideLayout = {
  name: "list",
  description: "Bullet list slide on dark background",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    list: {
      type: "array",
      description: "List items (max 10 items)",
      required: true,
      maxItems: 10,
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
    let slide = ``;
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
