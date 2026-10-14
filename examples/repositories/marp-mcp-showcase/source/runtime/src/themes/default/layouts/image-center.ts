/**
 * Default theme - Image-center layout
 */

import type { SlideLayout } from "../../types.js";
import { withLengthPrompt } from "../../../utils/text-length.js";

export const imageCenterLayout: SlideLayout = {
  name: "image-center",
  description: "Slide with centered image (fixed h:350)",
  params: {
    heading: {
      type: "string",
      description: withLengthPrompt("Slide heading", 54),
      required: true,
      maxLength: 54,
    },
    imagePath: {
      type: "string",
      description:
        "Image file path (local paths supported, e.g., ./attachments/image.png)",
      required: true,
    },
    description: {
      type: "string",
      description: withLengthPrompt("Image description below image", 75),
      required: false,
      maxLength: 75,
    },
    citations: {
      type: "string",
      description: withLengthPrompt("Citation", 130, {
        note: "no line break",
      }),
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    let slide = "";

    if (params.heading) {
      slide += `## ${params.heading}\n\n`;
    }

    slide += `![h:450](${params.imagePath})`;

    if (params.description) {
      slide += `\n\n${params.description}`;
    }

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
