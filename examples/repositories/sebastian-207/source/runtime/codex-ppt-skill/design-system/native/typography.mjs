export function addText(slide, text, rect, style, role = "body", opts = {}) {
  const fontSize = opts.fontSize || style.scale?.[role] || style.scale?.body || 17;
  slide.addText(text || "", {
    x: rect.x,
    y: rect.y,
    w: rect.w,
    h: rect.h,
    fontFace: opts.fontFace || (role.includes("Title") || role === "statement" ? style.headingFont : style.bodyFont),
    fontSize,
    bold: opts.bold ?? ["coverTitle", "sectionTitle", "slideTitle", "statement", "kpi"].includes(role),
    color: opts.color || style.fg,
    fit: opts.fit || "shrink",
    margin: opts.margin ?? 0.02,
    breakLine: opts.breakLine,
    align: opts.align || "left",
    valign: opts.valign,
    paraSpaceAfterPt: opts.paraSpaceAfterPt,
    paraSpaceBeforePt: opts.paraSpaceBeforePt,
    isTextBox: true,
  });
}

export function addSlideTitle(slide, title, style) {
  addText(slide, title, { x: 0.72, y: 0.48, w: 9.7, h: 0.62 }, style, "slideTitle", { fit: "shrink" });
}

export function addKicker(slide, text, rect, style) {
  addText(slide, String(text || "").toUpperCase(), rect, style, "label", { bold: true, color: style.accent, fontSize: 10.5 });
}

export function addParagraph(slide, text, rect, style, opts = {}) {
  addText(slide, text, rect, style, "body", { fontSize: opts.fontSize || style.scale?.body || 17, color: opts.color || style.fg, paraSpaceAfterPt: 6, ...opts });
}

export function addBullets(slide, items, rect, style, opts = {}) {
  const data = (items || []).filter(Boolean).slice(0, opts.max || 5);
  const runs = data.map((item) => ({ text: item, options: { bullet: { type: "ul" }, breakLine: true } }));
  slide.addText(runs.length ? runs : "", {
    x: rect.x,
    y: rect.y,
    w: rect.w,
    h: rect.h,
    fontFace: style.bodyFont,
    fontSize: opts.fontSize || style.scale?.body || 17,
    color: opts.color || style.fg,
    fit: "shrink",
    margin: opts.margin ?? 0.08,
    paraSpaceAfterPt: opts.paraSpaceAfterPt ?? 8,
    valign: opts.valign,
    breakLine: false,
  });
}
