import type { SlideLayout } from "../../../themes/types.js";

export const tableLayout: SlideLayout = {
  name: "table",
  description: "Business table with navy header and clean rows",
  className: "corp-table",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    tableMarkdown: {
      type: "string",
      description: "Table in markdown format (max 5 rows)",
      required: true,
    },
    description: {
      type: "string",
      description: "Table description below table (no line break)",
      required: false,
      maxLength: 75,
    },
    citations: {
      type: "string",
      description: "Citation (no line break)",
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: corp-table -->\n\n`;
    if (params.heading) {
      slide += `## ${params.heading}\n\n`;
    }

    slide += params.tableMarkdown;

    if (params.description) {
      slide += `\n\n${params.description}`;
    }

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
