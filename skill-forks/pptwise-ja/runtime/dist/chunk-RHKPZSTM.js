var __defProp = Object.defineProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};

// src/platform/registry.ts
function findRemoteAssetRef(svgMarkup) {
  const m = /\s(?:xlink:href|href)\s*=\s*["'](https?:\/\/[^"']*)["']/i.exec(svgMarkup);
  return m ? m[1] : null;
}
var current = {};
function installPlatform(p) {
  current = { ...current, ...p };
}
function getPlatform() {
  return current;
}

export {
  __export,
  findRemoteAssetRef,
  installPlatform,
  getPlatform
};
//# sourceMappingURL=chunk-RHKPZSTM.js.map