import type { ThemeDefinition } from "../types.js";
import { titleLayout } from "./layouts/title.js";
import { sectionLayout } from "./layouts/section.js";
import { listLayout } from "./layouts/list.js";
import { tableLayout } from "./layouts/table.js";
import { imageRightLayout } from "./layouts/image-right.js";
import { imageCenterLayout } from "./layouts/image-center.js";
import { contentLayout } from "./layouts/content.js";

export const defaultTheme: ThemeDefinition = {
  name: "default",
  description:
    "Standard Marp theme using directives for footers and built-in layouts",
  layouts: {
    title: titleLayout,
    section: sectionLayout,
    list: listLayout,
    table: tableLayout,
    "image-right": imageRightLayout,
    "image-center": imageCenterLayout,
    content: contentLayout,
  },
};
