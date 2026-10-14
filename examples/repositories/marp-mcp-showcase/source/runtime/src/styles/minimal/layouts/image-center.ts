import type { SlideLayout } from "../../../themes/types.js";

export const imageCenterLayout: SlideLayout = {
  name: "image-center",
  description: "Centered image slide, clean and minimal",
  className: "min-img-center",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    imagePath: {
      type: "string",
      description: "Image file path or URL",
      required: true,
    },
    description: {
      type: "string",
      description: "Image description below image",
      required: false,
      maxLength: 75,
    },
    caption: {
      type: "string",
      description: "Image caption displayed below",
      required: false,
      maxLength: 120,
    },
    citations: {
      type: "string",
      description: "Citation (no line break)",
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: min-img-center -->\n\n`;
    if (params.heading) {
      slide += `## ${params.heading}\n\n`;
    }

    slide += `<div class="min-image-center-wrap">\n\n![h:380](${params.imagePath})\n\n</div>`;

    if (params.caption) {
      slide += `\n\n<p class="min-image-caption">${params.caption}</p>`;
    }

    if (params.description) {
      slide += `\n\n${params.description}`;
    }

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
