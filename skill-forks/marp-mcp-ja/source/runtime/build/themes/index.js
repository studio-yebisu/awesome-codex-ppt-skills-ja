import { defaultTheme } from "./default/index.js";
import { gaiaTheme } from "./gaia/index.js";
import { uncoverTheme } from "./uncover/index.js";
const themes = {
    default: defaultTheme,
    gaia: gaiaTheme,
    uncover: uncoverTheme,
};
let activeTheme = defaultTheme;
export function getActiveTheme() {
    return activeTheme;
}
export function setActiveTheme(themeName) {
    activeTheme = themes[themeName];
}
export function getTheme(themeName) {
    return themes[themeName];
}
export function getAvailableThemeNames() {
    return Object.keys(themes);
}
export { themes };
