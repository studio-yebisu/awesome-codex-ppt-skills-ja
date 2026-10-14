import type { SlideLayout } from "../../../themes/types.js";

export const highlightBoxLayout: SlideLayout = {
  name: "highlight-box",
  description: "Minimal message box for key takeaways",
  params: {
    heading: {
      type: "string",
      description: "Box heading",
      required: true,
      maxLength: 80,
    },
    content: {
      type: "string",
      description: "Box content text",
      required: false,
      maxLength: 500,
    },
  },
  template: (params) => {
    let inner = `<h3>${params.heading}</h3>`;
    if (params.content) {
      inner += `\n<p>${params.content}</p>`;
    }
    return `<div class="min-highlight">\n${inner}\n</div>`;
  },
};
