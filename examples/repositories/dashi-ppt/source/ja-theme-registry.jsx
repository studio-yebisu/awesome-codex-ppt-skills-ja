// JAD-201:主题注册表 —— client-runtime 经 `@dashi/theme-registry` 引入,
// renderDeck 打包时把别名指向本文件(全主题)或裁剪版(单/少主题 deck)。
import React from 'react';
import { runtimePages as theme05Pages } from 'M:/Codex/Projects/awesome-codex-ppt-skills-ja/.build/dashi-ja-source/skills/dashi-ppt/project/dist/theme-runtime/theme05.module.mjs';

export const runtimePages = [
  ...theme05Pages,
];

export const themeOverrides = {

};

export function wrapThemeImageProviders(element, values) {
  return element;
}
