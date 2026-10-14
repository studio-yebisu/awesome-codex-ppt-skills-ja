import type { SlideLayout } from "../../../themes/types.js";

export const sectionLayout: SlideLayout = {
  name: "section",
  description: "Simple black section divider slide",
  className: "min-section",
  params: {
    title: {
      type: "string",
      description: "Section title",
      required: true,
      maxLength: 80,
    },
    subtitle: {
      type: "string",
      description: "Subtitle or description",
      required: false,
      maxLength: 200,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: min-section -->\n\n## ${params.title}`;
    if (params.subtitle) {
      slide += `\n\n${params.subtitle}`;
    }
    return slide;
  },
};
