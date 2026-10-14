import type { SlideLayout } from "../../../themes/types.js";

export const sidebarLayout: SlideLayout = {
  name: "sidebar",
  description: "Main content with sidebar for supplementary info or references",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    content: {
      type: "string",
      description: "Main content (markdown supported)",
      required: true,
    },
    sidebarTitle: {
      type: "string",
      description: "Sidebar heading",
      required: false,
      maxLength: 60,
    },
    sidebarItems: {
      type: "array",
      description: "Sidebar items",
      required: true,
      maxItems: 8,
    },
  },
  template: (params) => {
    const items = params.sidebarItems as string[];
    const sidebarList = items.map((item) => `<li>${item}</li>`).join("\n");
    let sidebarInner = "";
    if (params.sidebarTitle) {
      sidebarInner += `<h4>${params.sidebarTitle}</h4>\n`;
    }
    sidebarInner += `<ul>\n${sidebarList}\n</ul>`;

    return `## ${params.heading}\n\n<div class="corp-sidebar-layout">\n<div class="corp-sidebar-main">\n\n${params.content}\n\n</div>\n<div class="corp-sidebar">\n${sidebarInner}\n</div>\n</div>`;
  },
};
