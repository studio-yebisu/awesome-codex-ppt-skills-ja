import type { SlideLayout } from "../../../themes/types.js";

export const bigStatementLayout: SlideLayout = {
  name: "big-statement",
  description: "Dark large impactful statement slide with bold centered text",
  className: "dk-statement",
  params: {
    statement: {
      type: "string",
      description: "The main statement or headline",
      required: true,
      maxLength: 120,
    },
    subtitle: {
      type: "string",
      description: "Optional supporting text below the statement",
      required: false,
      maxLength: 200,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: dk-statement -->\n\n# ${params.statement}`;
    if (params.subtitle) {
      slide += `\n\n${params.subtitle}`;
    }
    return slide;
  },
};
