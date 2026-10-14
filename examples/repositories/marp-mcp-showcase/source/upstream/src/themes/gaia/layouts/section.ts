/**
 * Gaia theme - Section layout
 */

import type { SlideLayout } from "../../types.js";
import { withLengthPrompt } from "../../../utils/text-length.js";

export const sectionLayout: SlideLayout = {
  name: "section",
  description: "Section break slide with centered title and subtitle",
  params: {
    title: {
      type: "string",
      description: withLengthPrompt("Section title", 32),
      required: true,
      maxLength: 32,
    },
    subtitle: {
      type: "string",
      description: withLengthPrompt("Section subtitle", 38),
      required: false,
      maxLength: 38,
    },
  },
  template: (params) => {
    let slide = `<br><br><br>\n# ${params.title}\n`;
    if (params.subtitle) {
      slide += `## ${params.subtitle}\n`;
    }
    return slide;
  },
};
