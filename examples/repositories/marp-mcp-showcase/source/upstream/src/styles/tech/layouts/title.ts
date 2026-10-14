import type { SlideLayout } from "../../../themes/types.js";

export const titleLayout: SlideLayout = {
  name: "title",
  description: "Gradient title slide with optional tagline and event/company name",
  params: {
    heading: {
      type: "string",
      description: "Presentation title (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    subtitle: {
      type: "string",
      description: "Tagline or brief description of the presentation",
      required: false,
      maxLength: 150,
    },
    meta: {
      type: "string",
      description: "Event name, date, or company (displayed in small text at the bottom)",
      required: false,
      maxLength: 100,
    },
  },
  template: (params) => {
    const subtitle = params.subtitle
      ? `\n<p class="tech-title-subtitle">${params.subtitle}</p>`
      : "";
    const meta = params.meta
      ? `\n<p class="tech-title-meta">${params.meta}</p>`
      : "";
    return (
      `<div class="tech-title-slide">\n` +
      `<h1 class="tech-title-heading">${params.heading}</h1>` +
      subtitle +
      meta +
      `\n</div>`
    );
  },
};
