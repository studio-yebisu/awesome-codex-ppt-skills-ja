import type { SlideLayout } from "../../../themes/types.js";

export const quoteLayout: SlideLayout = {
  name: "quote",
  description: "Dark quote slide with attribution",
  className: "dk-quote",
  params: {
    quote: {
      type: "string",
      description: "The quote text",
      required: true,
    },
    attribution: {
      type: "string",
      description: "Quote attribution (e.g. author name)",
      required: false,
      maxLength: 80,
    },
    content: {
      type: "string",
      description: "Additional content below the quote",
      required: false,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: dk-quote -->\n\n`;

    slide += `> ${params.quote}`;
    if (params.attribution) {
      slide += `\n>\n> — ${params.attribution}`;
    }

    if (params.content) {
      slide += `\n\n${params.content}`;
    }

    return slide;
  },
};
