import type { SlideLayout } from "../../../themes/types.js";

export const highlightBoxLayout: SlideLayout = {
  name: "highlight-box",
  description: "Dark gradient message box for key takeaways or announcements",
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
    return `<div class="dk-highlight">\n${inner}\n</div>`;
  },
};
