/**
 * Academic style - Title slide layout
 */

import type { SlideLayout } from "../../../themes/types.js";

export const titleLayout: SlideLayout = {
  name: "title",
  description: "Academic title slide with author, affiliation, and date",
  className: "acad-title",
  params: {
    heading: {
      type: "string",
      description: "Presentation title (max 80 chars)",
      required: true,
      maxLength: 80,
    },
    subtitle: {
      type: "string",
      description: "Subtitle or session name",
      required: false,
      maxLength: 100,
    },
    author: {
      type: "string",
      description: "Author name(s)",
      required: false,
      maxLength: 100,
    },
    affiliation: {
      type: "string",
      description: "Institution or affiliation",
      required: false,
      maxLength: 100,
    },
    date: {
      type: "string",
      description: "Presentation date or conference name",
      required: false,
      maxLength: 100,
    },
    backgroundImage: {
      type: "string",
      description: "Optional background image path or URL",
      required: false,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: acad-title -->\n`;
    if (params.backgroundImage) {
      slide += `\n![bg brightness:0.4 opacity:0.3](${params.backgroundImage})\n`;
    }
    slide += `\n# ${params.heading}`;
    if (params.subtitle) {
      slide += `\n\n${params.subtitle}`;
    }
    if (params.author) {
      slide += `\n\n**${params.author}**`;
    }
    if (params.affiliation) {
      slide += `\n\n${params.affiliation}`;
    }
    if (params.date) {
      slide += `\n\n${params.date}`;
    }
    return slide;
  },
};
