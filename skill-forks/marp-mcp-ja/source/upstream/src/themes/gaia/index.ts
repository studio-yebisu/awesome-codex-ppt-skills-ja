import type { ThemeDefinition } from "../types.js";
import { titleLayout } from "./layouts/title.js";
import { sectionLayout } from "./layouts/section.js";
import { listLayout } from "./layouts/list.js";
import { tableLayout } from "./layouts/table.js";
import { imageRightLayout } from "./layouts/image-right.js";
import { imageCenterLayout } from "./layouts/image-center.js";

export const gaiaTheme: ThemeDefinition = {
  name: "gaia",
  description:
    "Marp Gaia theme using default layouts (title slide supports lead styling)",
  layouts: {
    title: titleLayout,
    section: sectionLayout,
    list: listLayout,
    table: tableLayout,
    "image-right": imageRightLayout,
    "image-center": imageCenterLayout,
  },
};
