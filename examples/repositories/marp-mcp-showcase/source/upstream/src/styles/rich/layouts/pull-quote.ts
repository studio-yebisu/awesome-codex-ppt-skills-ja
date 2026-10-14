import type { SlideLayout } from "../../../themes/types.js";

export const pullQuoteLayout: SlideLayout = {
  name: "pull-quote",
  description: "Decorative impact quote with large quotation marks, centered layout",
  className: "rich-pull-quote",
  params: {
    quote: {
      type: "string",
      description: "The quote text (short, impactful)",
      required: true,
      maxLength: 200,
    },
    attribution: {
      type: "string",
      description: "Quote attribution",
      required: false,
      maxLength: 80,
    },
    context: {
      type: "string",
      description: "Additional context or source",
      required: false,
      maxLength: 120,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: rich-pull-quote -->\n\n`;
    slide += `<div class="pull-quote-wrap">\n<p class="pull-quote-text">${params.quote}</p>`;
    if (params.attribution) {
      slide += `\n<p class="pull-quote-attr">— ${params.attribution}</p>`;
    }
    if (params.context) {
      slide += `\n<p class="pull-quote-ctx">${params.context}</p>`;
    }
    slide += `\n</div>`;
    return slide;
  },
};
