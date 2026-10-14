import type { SlideLayout } from "../../../themes/types.js";

export const sectionLayout: SlideLayout = {
  name: "section",
  description: "Dark full-bleed section divider with cyan eyebrow label and bold heading",
  params: {
    title: {
      type: "string",
      description: "Main section heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    eyebrow: {
      type: "string",
      description: "Small uppercase label displayed above the heading (e.g. 'Part 1', 'Chapter 2')",
      required: false,
      maxLength: 60,
    },
  },
  template: (params) => {
    const eyebrow = params.eyebrow
      ? `<p class="tech-section-eyebrow">${params.eyebrow}</p>\n`
      : "";
    return (
      `<div class="tech-section-slide">\n` +
      eyebrow +
      `<h2 class="tech-section-heading">${params.title}</h2>\n` +
      `</div>`
    );
  },
};
