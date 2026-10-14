import type { SlideLayout } from "../../../themes/types.js";

export const sectionLayout: SlideLayout = {
  name: "section",
  description: "Section divider slide with gradient background",
  className: "bg-gradient",
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
    let slide = `<!-- _class: bg-gradient -->\n\n## ${params.title}`;
    if (params.subtitle) {
      slide += `\n\n${params.subtitle}`;
    }
    return slide;
  },
};
