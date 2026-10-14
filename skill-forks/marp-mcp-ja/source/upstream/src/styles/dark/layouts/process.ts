import type { SlideLayout } from "../../../themes/types.js";

export const processLayout: SlideLayout = {
  name: "process",
  description: "Dark horizontal process flow with numbered steps and arrows",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    steps: {
      type: "array",
      description: "Process step labels",
      required: true,
      maxItems: 6,
    },
  },
  template: (params) => {
    const steps = params.steps as string[];
    const stepItems = steps
      .map((step, i) => {
        const html = `<div class="dk-process-step">\n<div class="dk-process-step-number">${i + 1}</div>\n<div class="dk-process-step-label">${step.trim()}</div>\n</div>`;
        if (i < steps.length - 1) {
          return html + `\n<div class="dk-process-arrow">→</div>`;
        }
        return html;
      })
      .join("\n");
    return `## ${params.heading}\n\n<div class="dk-process-steps">\n${stepItems}\n</div>`;
  },
};
