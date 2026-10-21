import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function readJson(rel, fallback = {}) {
  try {
    return JSON.parse(await fs.readFile(path.join(ROOT, rel), "utf8"));
  } catch {
    return fallback;
  }
}

export function cleanHex(value, fallback = "111827") {
  const v = String(value || fallback).replace("#", "").trim();
  return /^[0-9a-fA-F]{6}$/.test(v) ? v.toUpperCase() : fallback;
}

export async function resolveStyle(spec = {}, styleCard = {}, fontInventory = null) {
  const colorTokens = await readJson("tokens/color.json", { styles: {} });
  const typography = await readJson("tokens/typography.json", { font_families: {}, scale: {} });
  const styleId = spec.style_id || styleCard.style_id || spec.style || "executive-clean";
  const palette = { ...(colorTokens.styles[styleId] || colorTokens.styles["executive-clean"] || {}), ...(styleCard.palette || {}), ...(spec.palette || {}) };
  const fontGroup = typography.font_families[spec.font_profile || styleId] || typography.font_families[styleId] || typography.font_families["modern-corporate"] || {};
  const chooseFont = (explicit, chain = []) => explicit || chain[0] || "Microsoft YaHei UI";
  return {
    id: styleId,
    bg: cleanHex(palette.bg || palette.background, "F7F8FA"),
    fg: cleanHex(palette.fg || palette.primary, "111827"),
    muted: cleanHex(palette.muted || palette.secondary, "64748B"),
    accent: cleanHex(palette.accent, "2563EB"),
    accent2: cleanHex(palette.accent2, "0F766E"),
    surface: cleanHex(palette.surface, "FFFFFF"),
    surface2: cleanHex(palette.surface2 || palette.accent_soft, "EEF2F7"),
    line: cleanHex(palette.line, "D6DEE8"),
    warn: cleanHex(palette.warn, "B45309"),
    headingFont: chooseFont(spec.fonts?.heading, fontGroup.heading),
    bodyFont: chooseFont(spec.fonts?.body, fontGroup.body),
    numberFont: chooseFont(spec.fonts?.number, fontGroup.number),
    scale: { ...(typography.scale || {}), ...(styleCard.type_scale || {}), ...(spec.type_scale || {}) },
  };
}

export function applyTheme(doc, style) {
  doc.layout = "LAYOUT_WIDE";
  doc.author = "codex-ppt-skill";
  doc.company = "Studio Yebisu";
  doc.lang = "ja-JP";
  doc.theme = {
    headFontFace: style.headingFont,
    bodyFontFace: style.bodyFont,
    lang: "ja-JP",
    themeColors: [
      { name: "accent1", color: style.accent },
      { name: "accent2", color: style.accent2 },
      { name: "text1", color: style.fg },
      { name: "background1", color: style.bg },
    ],
  };
}
