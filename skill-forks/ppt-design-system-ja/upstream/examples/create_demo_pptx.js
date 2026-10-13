const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "工程技术部";
pres.title = "工程项目进度报告 · 2026年第二季度";

// ===== Design System (蒸馏自 guizang-ppt-skill + Open Design) =====
// 靛蓝瓷色板
const C = {
  INK: "0A1F3D", INK_RGB: "10,31,61", INK_TINT: "152A4A",
  PAPER: "F1F3F5", PAPER_TINT: "E4E8EC",
  ACCENT: "3B82F6", WHITE: "FFFFFF",
  LIGHT: "94A3B8", DIM: "5A7184",
  SUCCESS: "16A34A", WARNING: "D97706",
  DANGER: "DC2626", TEXT: "1E2938",
};
const F = {
  TITLE: "微软雅黑", BODY: "微软雅黑", MONO: "Consolas",
  EN: "Georgia",
};
const makeShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 1, angle: 135, opacity: 0.08 });

// ===== Helper Functions =====
function addChrome(slide, left, right) {
  slide.addText(left, { x: 0.6, y: 0.2, w: 5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: C.LIGHT, charSpacing: 4 });
  slide.addText(right, { x: 6, y: 0.2, w: 3.5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: C.LIGHT, align: "right", charSpacing: 2 });
}

function addAccentLine(slide, y) {
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: y, w: 1.2, h: 0.03, fill: { color: C.ACCENT } });
}

function addKicker(slide, text, y) {
  slide.addText(text, { x: 0.6, y: y, w: 6, h: 0.35, fontFace: F.MONO, fontSize: 10, color: C.LIGHT, charSpacing: 3 });
}

function addSlideTitle(slide, text, y) {
  slide.addText(text, { x: 0.6, y: y, w: 7, h: 0.7, fontFace: F.TITLE, fontSize: 28, color: C.INK, bold: true });
}

function addLead(slide, text, y) {
  slide.addText(text, { x: 0.6, y: y, w: 6.5, h: 0.45, fontFace: F.BODY, fontSize: 11, color: C.DIM });
}

function addFooter(slide, left, right) {
  slide.addText(left, { x: 0.6, y: 5.15, w: 5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: C.LIGHT });
  slide.addText(right, { x: 6, y: 5.15, w: 3.5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: C.LIGHT, align: "right" });
}

function addDarkFooter(slide, left, right) {
  slide.addText(left, { x: 0.6, y: 5.15, w: 5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: "5A7184" });
  slide.addText(right, { x: 6, y: 5.15, w: 3.5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: "5A7184", align: "right" });
}

function addStatCard(slide, x, y, w, h, label, number, unit, note, darkBg) {
  const borderColor = C.ACCENT;
  const textColor = darkBg ? C.WHITE : C.INK;
  const labelColor = darkBg ? "8BA0C0" : C.LIGHT;
  const noteColor = darkBg ? "8BA0C0" : C.LIGHT;
  const bgColor = darkBg ? "152A4A" : "FFFFFF";
  const cardShadow = makeShadow();

  // Card background
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: bgColor },
    shadow: cardShadow,
  });
  // Left accent
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.04, h,
    fill: { color: borderColor },
  });
  // Label
  slide.addText(label, {
    x: x + 0.15, y: y + 0.15, w: w - 0.3, h: 0.25,
    fontFace: F.MONO, fontSize: 8, color: labelColor, charSpacing: 2,
  });
  // Big number
  slide.addText([
    { text: number, options: { fontFace: "Georgia", fontSize: 28, bold: true, color: textColor } },
    { text: unit, options: { fontFace: F.TITLE, fontSize: 13, color: C.LIGHT } },
  ], {
    x: x + 0.15, y: y + 0.4, w: w - 0.3, h: 0.55,
  });
  // Note
  slide.addText(note, {
    x: x + 0.15, y: y + h - 0.35, w: w - 0.3, h: 0.25,
    fontFace: F.BODY, fontSize: 9, color: noteColor,
  });
}

function addDarkSlideTitle(slide, text, y) {
  slide.addText(text, { x: 0.6, y: y, w: 7, h: 0.7, fontFace: F.TITLE, fontSize: 28, color: C.WHITE, bold: true });
}

function addDarkLead(slide, text, y) {
  slide.addText(text, { x: 0.6, y: y, w: 6.5, h: 0.45, fontFace: F.BODY, fontSize: 11, color: "8BA0C0" });
}

// ===================================================================
// SLIDE 1: Cover
// ===================================================================
const s1 = pres.addSlide();
s1.background = { color: C.INK };

// Top accent bar
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.ACCENT } });

// Header
s1.addText("ENGINEERING REPORT", { x: 0.6, y: 0.3, w: 4, h: 0.25, fontFace: F.MONO, fontSize: 8, color: C.LIGHT, charSpacing: 6 });
s1.addText("2026  Q2", { x: 0.6, y: 0.55, w: 3, h: 0.2, fontFace: F.MONO, fontSize: 7, color: C.LIGHT, charSpacing: 4 });

// Decorative "Q2" watermark
s1.addText("Q2", { x: 7, y: 0.3, w: 2.5, h: 1.5, fontFace: F.EN, fontSize: 72, color: "152A4A", bold: true, align: "right" });

// Kicker
s1.addText("内部资料 · 仅供参阅", { x: 0.6, y: 1.5, w: 6, h: 0.35, fontFace: F.MONO, fontSize: 10, color: C.LIGHT, charSpacing: 3 });

// Main title
s1.addText([
  { text: "工程项目进度报告", options: { fontFace: F.TITLE, fontSize: 38, bold: true, color: C.WHITE } },
], { x: 0.6, y: 2.0, w: 7.5, h: 1.0 });

// Subtitle
s1.addText("2026 年第二季度 · 济南北部新城项目", { x: 0.6, y: 2.95, w: 7, h: 0.45, fontFace: F.BODY, fontSize: 16, color: "8BA0C0" });

// Description
s1.addText("涵盖工期进度、预算执行、质量验收、安全管理四大板块，\n本季度累计完成产值 2.86 亿元，整体进度完成 67.3%。", {
  x: 0.6, y: 3.5, w: 5.5, h: 0.65,
  fontFace: F.BODY, fontSize: 11, color: C.LIGHT, lineSpacingMultiple: 1.6,
});

// Meta
s1.addText("工程技术部", { x: 0.6, y: 4.55, w: 2.5, h: 0.25, fontFace: F.MONO, fontSize: 9, color: C.ACCENT, charSpacing: 2 });
s1.addText("2026.05.04  ·  EN-2026-Q2-001", { x: 0.6, y: 4.8, w: 5, h: 0.25, fontFace: F.MONO, fontSize: 8, color: C.LIGHT });

// Footer
s1.addText("济南 · 北部新城项目指挥部", { x: 0.6, y: 5.15, w: 5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: "5A7184" });
s1.addText("— 2026 —", { x: 8, y: 5.15, w: 1.5, h: 0.25, fontFace: F.MONO, fontSize: 7, color: "5A7184", align: "right" });

// ===================================================================
// SLIDE 2: Data Dashboard
// ===================================================================
const s2 = pres.addSlide();
s2.background = { color: C.PAPER };
addChrome(s2, "Quarterly Review · 核心数据", "02 / 05");
addKicker(s2, "KEY METRICS · Q2 2026", 0.65);
addSlideTitle(s2, "本季度关键指标", 1.05);
addLead(s2, "截至 4 月底，六大考核维度均达成阶段性目标。", 1.7);

const cardW = 2.7;
const cardH = 1.3;
const gapX = 0.3;
const startX = 0.6;
const startY = 2.3;

const stats = [
  ["Progress · 工期进度", "67.3", "%", "较计划超前 2.1%"],
  ["Output · 完成产值", "2.86", "亿", "年度目标 42%"],
  ["Quality · 质量合格率", "98.6", "%", "超目标 1.1%"],
  ["Safety · 安全工时", "487", "天", "无事故记录"],
  ["Budget · 预算执行", "94.2", "%", "结余 5.8%"],
  ["Team · 在岗人数", "326", "人", "含分包 8 家"],
];

stats.forEach((s, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = startX + col * (cardW + gapX);
  const y = startY + row * (cardH + 0.25);
  addStatCard(s2, x, y, cardW, cardH, s[0], s[1], s[2], s[3], false);
});

addFooter(s2, "数据截止: 2026.04.30", "数据来源 · 项目管理系统");

// ===================================================================
// SLIDE 3: Milestones
// ===================================================================
const s3 = pres.addSlide();
s3.background = { color: C.INK };

// Top accent
s3.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.ACCENT } });
addChrome(s3, "Schedule · 里程碑节点", "03 / 05");
addKicker(s3, "MILESTONES · 关键路径", 0.65);
addDarkSlideTitle(s3, "项目里程碑一览", 1.05);
addDarkLead(s3, "本季度 6 个里程碑中 5 个已按期达成。", 1.7);

const milestones = [
  ["✅ 已完成", "地基工程验收", "2026.03.15 · 提前 3 天", C.SUCCESS],
  ["✅ 已完成", "主体结构封顶", "2026.04.10 · 按期", C.SUCCESS],
  ["✅ 已完成", "外墙保温工程", "2026.04.22 · 提前 2 天", C.SUCCESS],
  ["🔄 进行中", "机电安装工程", "进度 58% · 预计 06.15", C.ACCENT],
  ["🔲 待启动", "室内精装修", "计划 06.01 进场", C.WARNING],
  ["🔲 待启动", "室外景观工程", "计划 06.20 进场", C.WARNING],
];

milestones.forEach((m, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = startX + col * (cardW + gapX);
  const y = startY + row * (cardH + 0.25);
  const borderColor = m[3];
  const cardBg = "152A4A";

  // Card
  s3.addShape(pres.shapes.RECTANGLE, { x, y, w: cardW, h: cardH, fill: { color: cardBg } });
  s3.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.04, h: cardH, fill: { color: borderColor } });
  // Status label
  s3.addText(m[0], { x: x + 0.15, y: y + 0.12, w: cardW - 0.3, h: 0.22, fontFace: F.MONO, fontSize: 8, color: borderColor, charSpacing: 2 });
  // Title (smaller as milestone name)
  s3.addText(m[1], { x: x + 0.15, y: y + 0.38, w: cardW - 0.3, h: 0.4, fontFace: F.BODY, fontSize: 15, color: C.WHITE, bold: true });
  // Date/note
  s3.addText(m[2], { x: x + 0.15, y: y + cardH - 0.38, w: cardW - 0.3, h: 0.28, fontFace: F.MONO, fontSize: 8, color: "8BA0C0" });
});

addDarkFooter(s3, "关键路径: 地基 → 主体 → 机电 → 精装 → 景观", "Page 03 · Milestones");

// ===================================================================
// SLIDE 4: Pipeline Process
// ===================================================================
const s4 = pres.addSlide();
s4.background = { color: C.PAPER };
addChrome(s4, "Workflow · 管理流程", "04 / 05");
addKicker(s4, "PROCESS · 流水线管理", 0.65);
addSlideTitle(s4, "项目管理流程", 1.05);
addLead(s4, "从立项到竣工，五大阶段协同推进。", 1.7);

function addStepBox(slide, x, y, w, h, nb, title, desc, active) {
  const boxColor = active ? C.WHITE : "FFFFFF";
  const borderColor = active ? C.ACCENT : "CBD5E1";
  const titleColor = active ? C.INK : C.DIM;

  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: boxColor },
    line: { color: borderColor, width: active ? 1.5 : 0.5 },
  });
  slide.addText(nb, { x: x + 0.1, y: y + 0.08, w: w - 0.2, h: 0.2, fontFace: F.MONO, fontSize: 8, color: C.LIGHT });
  slide.addText(title, { x: x + 0.1, y: y + 0.3, w: w - 0.2, h: 0.3, fontFace: F.BODY, fontSize: 12, color: titleColor, bold: true });
  slide.addText(desc, { x: x + 0.1, y: y + h - 0.28, w: w - 0.2, h: 0.22, fontFace: F.BODY, fontSize: 9, color: C.LIGHT });
}

const sec1 = [
  ["01", "可行性研究", "市场调研 · 经济测算", true],
  ["02", "方案设计", "规划方案 · 初步设计", true],
  ["03", "施工图审查", "图纸会审 · 技术交底", true],
  ["04", "招标采购", "分包招标 · 材料采购", true],
];
const sec2 = [
  ["05", "地基与基础", "已完成 ✅", true],
  ["06", "主体结构", "已完成 ✅", true],
  ["07", "机电安装", "进行中 58%", true],
  ["08", "装饰装修", "待启动", false],
];
const sec3 = [
  ["09", "分部分项验收", "随工程进度同步", false],
  ["10", "竣工验收", "计划 2026.12", false],
  ["11", "资料归档", "全过程同步", false],
];

const stepW = 1.95;
const stepH = 0.85;
const stepGap = 0.15;
const sections = [sec1, sec2, sec3];
const sectionLabels = ["01 · 前期阶段", "02 · 施工阶段", "03 · 验收阶段"];
const sectionStartY = [2.3, 3.4, 4.5];

sections.forEach((steps, si) => {
  const sy = sectionStartY[si];
  s4.addText(sectionLabels[si], { x: 0.6, y: sy - 0.55, w: 5, h: 0.25, fontFace: F.MONO, fontSize: 8, color: C.LIGHT, charSpacing: 2 });
  steps.forEach((step, i) => {
    const sx = 0.6 + i * (stepW + stepGap);
    addStepBox(s4, sx, sy, stepW, stepH, step[0], step[1], step[2], step[3]);
  });
});

addFooter(s4, "Page 04 · 管理流程总览", "Process Map");

// ===================================================================
// SLIDE 5: Summary
// ===================================================================
const s5 = pres.addSlide();
s5.background = { color: C.INK };

s5.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.ACCENT } });
addChrome(s5, "Takeaway · 总结与计划", "05 / 05");
s5.addText("NEXT STEPS · 下季度展望", { x: 0.6, y: 0.65, w: 6, h: 0.35, fontFace: F.MONO, fontSize: 10, color: C.LIGHT, charSpacing: 3 });

// Quote
s5.addText([
  { text: "\"工程管理不是管结果，\n是管过程。\"", options: { fontFace: F.TITLE, fontSize: 26, bold: true, color: C.WHITE } },
], { x: 0.6, y: 1.2, w: 6, h: 1.3, lineSpacingMultiple: 1.3 });

// Two columns
const colY = 2.7;
const colW = 3.8;

// Left column - Q2 Summary
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: colY, w: colW, h: 2.0,
  fill: { color: "152A4A" },
});
s5.addText("Q2 总结", { x: 0.8, y: colY + 0.15, w: 3, h: 0.25, fontFace: F.MONO, fontSize: 9, color: C.LIGHT, charSpacing: 2 });

const q2Items = [
  "产值 2.86 亿 · 超计划 3.2%",
  "质量合格率 98.6%",
  "安全事故 0 起",
  "预算结余 5.8%",
];
s5.addText(q2Items.map((t, i) => ({
  text: t,
  options: { bullet: true, breakLine: i < q2Items.length - 1, color: "8BA0C0", fontSize: 13 },
})), { x: 0.8, y: colY + 0.5, w: 3.3, h: 1.3, fontFace: F.BODY });

// Right column - Q3 Plan
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.6 + colW + 0.3, y: colY, w: colW, h: 2.0,
  fill: { color: "152A4A" },
});
s5.addText("Q3 计划", { x: 0.6 + colW + 0.5, y: colY + 0.15, w: 3, h: 0.25, fontFace: F.MONO, fontSize: 9, color: C.LIGHT, charSpacing: 2 });

const q3Items = [
  "完成机电安装 100%",
  "精装修进场 06.01",
  "材料采购提前锁价",
  "专项安全检查",
];
s5.addText(q3Items.map((t, i) => ({
  text: t,
  options: { bullet: true, breakLine: i < q3Items.length - 1, color: "8BA0C0", fontSize: 13 },
})), { x: 0.6 + colW + 0.5, y: colY + 0.5, w: 3.3, h: 1.3, fontFace: F.BODY });

// Closing
s5.addText("感谢各参建单位的通力配合，下季度继续稳扎稳打，确保年底竣工目标。", {
  x: 0.6, y: 4.8, w: 6.5, h: 0.35,
  fontFace: F.BODY, fontSize: 10, color: "8BA0C0",
});

addDarkFooter(s5, "报告编号 EN-2026-Q2-001 · 工程技术部", "— END —");

// ===== Output =====
const outPath = "D:\\OpenClaw Work\\项目对话\\demo-engineering-report.pptx";
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("✅ PPTX saved to: " + outPath);
}).catch(err => {
  console.error("❌ Error:", err);
  process.exit(1);
});
