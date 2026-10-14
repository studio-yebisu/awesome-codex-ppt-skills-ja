import { defaultStyle } from "./default/index.js";
import { richStyle } from "./rich/index.js";
import { minimalStyle } from "./minimal/index.js";
import { darkStyle } from "./dark/index.js";
import { corporateStyle } from "./corporate/index.js";
import { academicStyle } from "./academic/index.js";
import { techStyle } from "./tech/index.js";
import { warn } from "../utils/logger.js";
const builtinStyles = {
    default: defaultStyle,
    rich: richStyle,
    minimal: minimalStyle,
    dark: darkStyle,
    corporate: corporateStyle,
    academic: academicStyle,
    tech: techStyle,
};
const externalStyles = new Map();
let activeStyle = defaultStyle;
export function getActiveStyle() {
    return activeStyle;
}
export function setActiveStyle(styleName) {
    const style = getStyle(styleName);
    if (!style) {
        throw new Error(`Unknown style "${styleName}"`);
    }
    activeStyle = style;
}
export function getStyle(styleName) {
    const external = externalStyles.get(styleName);
    if (external)
        return external.def;
    return builtinStyles[styleName];
}
export function getAvailableStyleNames() {
    return [...Object.keys(builtinStyles), ...externalStyles.keys()];
}
/**
 * Register a style discovered outside the built-in registry (e.g. via the
 * marp-cli `themeSet` configuration). Collisions with built-in names are
 * rejected; collisions between externals replace the previous entry.
 */
export function registerExternalStyle(def, source) {
    if (Object.prototype.hasOwnProperty.call(builtinStyles, def.name)) {
        warn(`External style "${def.name}" collides with a built-in style; skipping.`, { source });
        return false;
    }
    if (externalStyles.has(def.name)) {
        warn(`External style "${def.name}" already registered; replacing previous entry.`, { previousSource: externalStyles.get(def.name)?.source, source });
    }
    externalStyles.set(def.name, { def, source });
    return true;
}
export function getExternalStyles() {
    return Array.from(externalStyles.values());
}
/** Test-only: clear all externally registered styles. */
export function clearExternalStyles() {
    externalStyles.clear();
}
export { builtinStyles as styles };
