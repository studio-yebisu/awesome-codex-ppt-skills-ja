import type { SlideLayout } from "../../../themes/types.js";

export const quoteLayout: SlideLayout = {
  name: "quote",
  description: "Stylized pull quote with violet left border, large quote mark, and attribution",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    quote: {
      type: "string",
      description: "The quote text (max 300 chars)",
      required: true,
      maxLength: 300,
    },
    attribution: {
      type: "string",
      description: "Who said it (person name, title, or company)",
      required: false,
      maxLength: 100,
    },
    context: {
      type: "string",
      description: "Additional context (e.g. source, date, or role)",
      required: false,
      maxLength: 120,
    },
  },
  template: (params) => {
    const attribution = params.attribution
      ? `\n<p class="tech-quote-attribution">— ${params.attribution}</p>`
      : "";
    const context = params.context
      ? `\n<p class="tech-quote-context">${params.context}</p>`
      : "";

    return (
      `## ${params.heading}\n\n` +
      `<div class="tech-quote-box">\n` +
      `<span class="tech-quote-mark">"</span>\n` +
      `<p class="tech-quote-text">${params.quote}</p>` +
      attribution +
      context +
      `\n</div>`
    );
  },
};
