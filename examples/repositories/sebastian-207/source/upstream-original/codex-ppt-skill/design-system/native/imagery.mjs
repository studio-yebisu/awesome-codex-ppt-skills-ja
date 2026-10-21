import fs from "node:fs";
import { surface, visualMotif } from "./components.mjs";

function imageSizingFor(treatment, rect) {
  const t = String(treatment || "").toLowerCase();
  const type = t.includes("contain") || t.includes("icon") || t.includes("logo") || t.includes("diagram") ? "contain" : "cover";
  return { type, w: rect.w, h: rect.h };
}

export function addIntegratedImage(slide, ShapeType, imagePath, rect, style, treatment = "60/40 split") {
  if (imagePath && fs.existsSync(imagePath)) {
    slide.addImage({ path: imagePath, ...rect, sizing: imageSizingFor(treatment, rect) });
    if (treatment === "atmospheric background with overlay") {
      slide.addShape(ShapeType.rect, { ...rect, fill: { color: style.bg, transparency: 28 }, line: { color: style.bg, transparency: 100 } });
    } else if (String(treatment || "").includes("masked")) {
      slide.addShape(ShapeType.rect, { ...rect, fill: { color: style.bg, transparency: 100 }, line: { color: style.line, transparency: 36, width: 0.6 } });
    }
    return true;
  }
  surface(slide, ShapeType, rect, style, { fill: style.surface2, line: style.line, radius: 0.02 });
  visualMotif(slide, ShapeType, { x: rect.x + rect.w * 0.08, y: rect.y + rect.h * 0.15, w: rect.w * 0.84, h: rect.h * 0.7 }, style, "grid");
  return false;
}
