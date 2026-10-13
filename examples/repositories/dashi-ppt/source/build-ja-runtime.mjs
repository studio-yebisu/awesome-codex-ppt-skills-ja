import fs from 'node:fs';
import {buildClientRuntime} from "file:///M:/Codex/Projects/awesome-codex-ppt-skills-ja/.build/dashi-ja-source/skills/dashi-ppt/project/src/components/themes/runtime-build.mjs";
import {buildThemeRegistrySource} from "file:///M:/Codex/Projects/awesome-codex-ppt-skills-ja/.build/dashi-ja-source/skills/dashi-ppt/project/src/components/themes/theme-registry-codegen.mjs";
const registryPath="M:\\Codex\\Projects\\awesome-codex-ppt-skills-ja\\examples\\repositories\\dashi-ppt\\source\\ja-theme-registry.jsx";
fs.writeFileSync(registryPath,buildThemeRegistrySource(['theme05'],{importPrefix:"M:/Codex/Projects/awesome-codex-ppt-skills-ja/.build/dashi-ja-source/skills/dashi-ppt/project/dist/theme-runtime/",fromModules:true,generated:false}));
buildClientRuntime({root:"M:\\Codex\\Projects\\awesome-codex-ppt-skills-ja\\.build\\dashi-ja-source\\skills\\dashi-ppt\\project",outFile:"M:\\Codex\\Projects\\awesome-codex-ppt-skills-ja\\.build\\dashi-ja-source\\skills\\dashi-ppt\\project\\dist\\theme-runtime\\imported-theme-runtime.theme05.js",registryPath});
