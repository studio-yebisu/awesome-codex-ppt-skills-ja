/**
 * Academic style - Key message layout
 */

import type { SlideLayout } from "../../../themes/types.js";

export const keyMessageLayout: SlideLayout = {
  name: "key-message",
  description: "Conclusion or key takeaway box with maroon highlight",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    title: {
      type: "string",
      description: "Key message title inside the box",
      required: true,
      maxLength: 60,
    },
    message: {
      type: "string",
      description: "Main message text",
      required: true,
      maxLength: 300,
    },
    note: {
      type: "string",
      description: "Additional note below the box",
      required: false,
      maxLength: 150,
    },
  },
  template: (params) => {
    let slide = `## ${params.heading}\n\n`;
    slide += `<div class="acad-key-message">\n`;
    slide += `<h3>${params.title}</h3>\n`;
    slide += `<p>${params.message}</p>\n`;
    slide += `</div>`;
    if (params.note) {
      slide += `\n\n<p class="acad-key-note">${params.note}</p>`;
    }
    return slide;
  },
};
