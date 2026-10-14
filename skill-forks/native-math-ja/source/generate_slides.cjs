const pptxgen = require("pptxgenjs");
const fs = require("fs");
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Studio Yebisu";
pres.title = "平均の、その先。";

// Theme — short alias T
const T = {
  "bg": {
    "title": "2D3436",
    "content": "FFFFFF",
    "section": "2D3436"
  },
  "tx": {
    "pri": "2D3436",
    "sec": "555555",
    "mut": "8C8C8C",
    "wh": "FFFFFF"
  },
  "ac": {
    "pos": "0173B2",
    "neg": "DE8F05",
    "emp": "029E73"
  },
  "chart": [
    "0173B2",
    "DE8F05",
    "029E73",
    "CC78BC"
  ],
  "cardFill": "0173B215",
  "divider": "D0D0D0"
};

// Typography — default baselines (scale up when content is sparse, see QA density check)
const F = {
  cover:    { face: "Shippori Mincho", size: 48 },
  section:  { face: "Shippori Mincho", size: 36 },
  title:    { face: "Shippori Mincho", size: 22 },
  subtitle: { face: "BIZ UDPGothic", size: 18 },
  body:     { face: "BIZ UDPGothic", size: 15 },
  small:    { face: "BIZ UDPGothic", size: 12 },
  caption:  { face: "BIZ UDPGothic", size: 11 },
  stat:     { face: "Shippori Mincho", size: 60 },
  cardTitle:{ face: "Shippori Mincho", size: 18 },
  tblHead:  { face: "BIZ UDPGothic", size: 13 },
  tblCell:  { face: "BIZ UDPGothic", size: 12 },
};

// Layout constants
const SW = 10, SH = 5.625, M = 0.5;
const CW = SW - 2 * M;       // content width (9")
const CY = 0.9;              // content top Y (below title bar)
const CH = SH - CY - M;      // content height (4.225")

// Slide Masters
pres.defineSlideMaster({
  title: "TITLE_SLIDE",
  background: { color: T.bg.title },
  objects: [
    { rect: { x: 0, y: 4.8, w: SW, h: 0.825, fill: { color: "000000", transparency: 30 } } }
  ]
});
pres.defineSlideMaster({
  title: "SECTION_SLIDE",
  background: { color: T.bg.section }
});
pres.defineSlideMaster({
  title: "CONTENT_SLIDE",
  background: { color: T.bg.content },
  objects: [
    { rect: { x: 0, y: 0, w: SW, h: 0.7, fill: { color: T.bg.title } } }
  ]
});
pres.defineSlideMaster({
  title: "THANK_YOU",
  background: { color: T.bg.title }
});

// Formula manifest — supports OMML (native math) and image (PNG/SVG) entries
const manifest = JSON.parse(fs.readFileSync("formulas/manifest.json", "utf8"));

// OMML placeholder — inject_omml.py replaces these post-generation
function addMathText(slide, id, x, y, w, h, opts = {}) {
  slide.addText(`{{MATH:${id}}}`, {
    x, y, w, h,
    fontFace: opts.fontFace || F.body.face,
    fontSize: opts.fontSize || F.body.size,
    color: opts.color || T.tx.pri,
    align: opts.align || "center",
    valign: opts.valign || "middle",
    margin: 0, shrinkText: true
  });
}

// Centered formula — auto-routes OMML vs image based on manifest
function addFormula(slide, id, y, targetH = 0.4) {
  const f = manifest[id];
  if (!f || f.error) return;
  if (f.render === "omml") {
    addMathText(slide, id, M, y, CW, targetH);
    return;
  }
  if (f.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(f.file, "utf8")).toString("base64");
    const scale = targetH / (f.height_pt / 72);
    const w = (f.width_pt / 72) * scale;
    slide.addImage({ data: "image/svg+xml;base64," + b64, x: (SW - w) / 2, y, w, h: targetH });
  } else {
    const dpi = f.dpi || 600;
    const scale = targetH / (f.height_px / dpi);
    const w = (f.width_px / dpi) * scale;
    slide.addImage({ path: f.file, x: (SW - w) / 2, y, w, h: targetH });
  }
}

// Left-aligned formula — auto-routes OMML vs image
function addFormulaAt(slide, id, x, y, maxW, targetH) {
  const f = manifest[id];
  if (!f || f.error) return;
  if (f.render === "omml") {
    addMathText(slide, id, x, y, maxW, targetH, { align: "left" });
    return;
  }
  if (f.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(f.file, "utf8")).toString("base64");
    let scale = targetH / (f.height_pt / 72);
    let w = (f.width_pt / 72) * scale, h = targetH;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ data: "image/svg+xml;base64," + b64, x, y, w, h });
  } else {
    const dpi = f.dpi || 600;
    let scale = targetH / (f.height_px / dpi);
    let w = (f.width_px / dpi) * scale, h = targetH;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ path: f.file, x, y, w, h });
  }
}

// Card with formula body — auto-routes OMML vs image
function addCardFormula(sl, x, y, w, h, color, title, formulaId, fH) {
  chk("cardFormula", y, h);
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w, h,
    fill: { color: "FFFFFF" }, shadow: mkSh() });
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h,
    fill: { color } });
  const px = x + 0.25, pw = w - 0.4;
  sl.addText(title, { x: px, y: y + 0.1, w: pw, h: 0.4,
    fontFace: F.cardTitle.face, fontSize: F.cardTitle.size, bold: true,
    color: T.tx.pri, valign: "top", margin: [0, 0, 0, 0], shrinkText: true });
  addFormulaAt(sl, formulaId, px, y + 0.55, pw, fH || (h - 0.7));
}

// Factory: card shadow (NEVER reuse option objects directly)
const mkSh = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 });

// Diagram manifest (optional — only when diagrams/ exists)
const dManifest = (() => {
  try { return JSON.parse(fs.readFileSync("diagrams/manifest.json", "utf8")); }
  catch { return {}; }
})();

// Centered diagram
function addDiagram(slide, id, y, targetH, maxW = CW) {
  const d = dManifest[id];
  if (!d || d.error) return;
  let w, h = targetH;
  if (d.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(d.file, "utf8")).toString("base64");
    const scale = targetH / (d.height_pt / 72);
    w = (d.width_pt / 72) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ data: "image/svg+xml;base64," + b64, x: (SW - w) / 2, y, w, h });
  } else {
    const dpi = d.dpi || 300;
    const scale = targetH / (d.height_px / dpi);
    w = (d.width_px / dpi) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ path: d.file, x: (SW - w) / 2, y, w, h });
  }
}

// Positioned diagram (for two-column layouts)
function addDiagramAt(slide, id, x, y, maxW, targetH) {
  const d = dManifest[id];
  if (!d || d.error) return;
  let w, h = targetH;
  if (d.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(d.file, "utf8")).toString("base64");
    const scale = targetH / (d.height_pt / 72);
    w = (d.width_pt / 72) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ data: "image/svg+xml;base64," + b64, x, y, w, h });
  } else {
    const dpi = d.dpi || 300;
    const scale = targetH / (d.height_px / dpi);
    w = (d.width_px / dpi) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ path: d.file, x, y, w, h });
  }
}

// Extracted figure with caption (source attribution)
// Aspect-ratio-aware: wide images (ratio>1.6) use full-width centered,
// normal/tall images (ratio≤1.6) use left-figure + right-text layout via addFigureWithText.
function addFigure(slide, id, y, targetH, caption) {
  addDiagram(slide, id, y, targetH - 0.3);
  if (caption) {
    slide.addText(caption, {
      x: M, y: y + targetH - 0.25, w: CW, h: 0.25,
      fontFace: F.caption.face, fontSize: F.caption.size,
      color: T.tx.mut, align: "center", italic: true, margin: 0
    });
  }
}

// Figure + text side-by-side layout (aspect-ratio-aware)
// For images with ratio ≤ 1.6: figure on left, bullets/text on right
// figRatio = original image width / height (read from manifest or measured)
// textItems: array of strings for right-side bullets
function addFigureWithText(slide, id, y, targetH, figRatio, textItems, caption) {
  const d = dManifest[id];
  if (!d || d.error) return;
  const gap = 0.3;
  // Compute figure width from height and ratio, cap at 60% of CW
  let figH = targetH - (caption ? 0.3 : 0);
  let figW = figH * figRatio;
  const maxFigW = CW * 0.6;
  if (figW > maxFigW) { const s = maxFigW / figW; figW = maxFigW; figH *= s; }
  const textX = M + figW + gap;
  const textW = CW - figW - gap;
  // Image (left)
  addDiagramAt(slide, id, M, y, figW, figH);
  // Bullets (right)
  if (textItems && textItems.length > 0) {
    addBullets(slide, textItems, textX, y, textW, figH);
  }
  // Caption (below figure)
  if (caption) {
    slide.addText(caption, {
      x: M, y: y + targetH - 0.25, w: figW, h: 0.25,
      fontFace: F.caption.face, fontSize: F.caption.size,
      color: T.tx.mut, align: "center", italic: true, margin: 0
    });
  }
}

// Speaker notes (optional — add after all slide content)
function addNotes(slide, text) {
  slide.addNotes(text);
}

// Themed chart (auto-applies theme colors and clean styling)
function addChart(sl, type, data, x, y, w, h, opts = {}) {
  chk("chart", y, h);
  sl.addChart(type, data, {
    x, y, w, h,
    chartColors: opts.chartColors || T.chart,
    chartArea: { fill: { color: T.bg.content }, roundedCorners: true },
    catAxisLabelColor: T.tx.sec, valAxisLabelColor: T.tx.sec,
    catAxisLabelFontFace: F.tblCell.face, catAxisLabelFontSize: F.tblCell.size,
    valAxisLabelFontFace: F.tblCell.face, valAxisLabelFontSize: F.tblCell.size,
    valGridLine: { color: T.divider, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: opts.showLegend !== undefined ? opts.showLegend : data.length > 1,
    legendPos: opts.legendPos || "b",
    legendFontFace: F.caption.face, legendFontSize: F.caption.size, legendColor: T.tx.sec,
    ...opts,
  });
}

// --- Slide builders ---

function sTitle(sl, txt) {
  sl.addText(txt, { x: M, y: 0.08, w: CW, h: 0.55,
    fontFace: F.title.face, fontSize: F.title.size, bold: true,
    color: T.tx.wh, margin: [0, 6, 0, 0], shrinkText: true });
}

function sectionSlide(title) {
  const sl = pres.addSlide({ masterName: "SECTION_SLIDE" });
  sl.addText(title, { x: M, y: SH / 2 - 0.5, w: CW, h: 1,
    fontFace: F.section.face, fontSize: F.section.size, bold: true,
    color: T.tx.wh, align: "center", valign: "middle" });
  sl.addShape(pres.shapes.RECTANGLE, { x: SW / 2 - 1.5, y: SH / 2 + 0.4,
    w: 3, h: 0.04, fill: { color: T.ac.pos } });
  return sl;
}

// --- Content helpers ---

function addBullets(sl, items, x, y, w, h, opts = {}) {
  chk("bullets", y, h);
  const arr = items.map((t, i) => ({
    text: t, options: {
      bullet: true, breakLine: i < items.length - 1,
      fontSize: opts.fontSize || F.body.size,
      fontFace: opts.fontFace || F.body.face,
      color: opts.color || T.tx.pri,
    }
  }));
  sl.addText(arr, { x, y, w, h, valign: "top", margin: [4, 6, 4, 4], shrinkText: true });
}

function addCard(sl, x, y, w, h, color, title, body) {
  chk("card", y, h);
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w, h,
    fill: { color: "FFFFFF" }, shadow: mkSh() });
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h,
    fill: { color } });
  // px: 0.19" clear of accent bar. pw: 0.15" from right edge.
  const px = x + 0.25, pw = w - 0.4;
  sl.addText(title, { x: px, y: y + 0.1, w: pw, h: 0.4,
    fontFace: F.cardTitle.face, fontSize: F.cardTitle.size, bold: true,
    color: T.tx.pri, valign: "top", margin: [0, 0, 0, 0], shrinkText: true });
  sl.addText(body, { x: px, y: y + 0.48, w: pw, h: h - 0.62,
    fontFace: F.body.face, fontSize: F.body.size,
    color: T.tx.sec, valign: "top", margin: [2, 0, 8, 0], shrinkText: true });
}

function addTable(sl, headers, rows, x, y, w, colW, rowH = 0.35) {
  chk("table", y, rowH * (rows.length + 1));
  const hRow = headers.map(h => ({ text: h, options: {
    fill: { color: T.bg.title }, color: T.tx.wh,
    bold: true, fontFace: F.tblHead.face, fontSize: F.tblHead.size,
    align: "center", valign: "middle"
  }}));
  const dRows = rows.map((row, i) => row.map(cell => {
    const isObj = typeof cell === "object" && cell !== null;
    const txt = isObj ? cell.text : String(cell);
    const base = {
      fill: { color: i % 2 === 0 ? "FFFFFF" : "F0F2F5" },
      fontFace: F.tblCell.face, fontSize: F.tblCell.size,
      color: T.tx.pri, valign: "middle"
    };
    return { text: txt, options: isObj ? { ...base, ...cell.options } : base };
  }));
  sl.addTable([hRow, ...dRows], { x, y, w, colW, border: { pt: 0.5, color: "E0E0E0" } });
}

// Continuation table page — repeats header, adds " (cont'd)" to slide title
function addTableCont(sl, title, headers, rows, x, y, w, colW, rowH = 0.35) {
  sTitle(sl, title + " (cont'd)");
  addTable(sl, headers, rows, x, y, w, colW, rowH);
}

function addNumCard(sl, num, title, body, x, y, w, h, color) {
  addCard(sl, x, y, w, h, color, title, body);
  sl.addShape(pres.shapes.OVAL, { x: x + w - 0.4, y: y - 0.15,
    w: 0.35, h: 0.35, fill: { color } });
  sl.addText(String(num), { x: x + w - 0.4, y: y - 0.15, w: 0.35, h: 0.35,
    fontFace: F.title.face, fontSize: 14, bold: true,
    color: "FFFFFF", align: "center", valign: "middle", margin: 0 });
}

function addFlow(sl, steps, y, h = 0.6) {
  const n = steps.length;
  const gap = 0.25, arrowW = 0.2;
  const totalArrows = (n - 1) * (gap + arrowW);
  const boxW = (CW - totalArrows) / n;
  let cx = M;
  steps.forEach((step, i) => {
    sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y, w: boxW, h,
      fill: { color: T.ac.pos, transparency: 88 },
      line: { color: T.ac.pos, width: 1.5 }, rectRadius: 0.08 });
    sl.addText(step, { x: cx, y, w: boxW, h,
      fontFace: F.small.face, fontSize: F.small.size,
      color: T.tx.pri, align: "center", valign: "middle", margin: 0 });
    if (i < n - 1) {
      const ax = cx + boxW + gap / 2;
      sl.addText("→", { x: ax, y, w: arrowW, h,
        fontFace: F.body.face, fontSize: 18, color: T.tx.mut,
        align: "center", valign: "middle", margin: 0 });
    }
    cx += boxW + gap + arrowW;
  });
}

function cols2() {
  const gap = 0.3, colW = (CW - gap) / 2;
  return {
    left:  { x: M, w: colW },
    right: { x: M + colW + gap, w: colW },
    colW, gap
  };
}

// Boundary check: warn if element bottom exceeds slide content area
function chk(label, y, h) {
  const bot = y + h;
  if (bot > SH - M + 0.05) console.warn(`OVERFLOW: ${label} bottom=${bot.toFixed(2)}" > limit=${(SH-M).toFixed(2)}"`);
}

// Gap check: verify element starts below previous element's bottom with minimum gap
let _lastBot = 0;
function gap(label, y, minGap = 0.08) {
  if (_lastBot > 0 && y < _lastBot + minGap)
    console.warn(`OVERLAP: ${label} y=${y.toFixed(2)}" < prev bottom + gap=${(_lastBot+minGap).toFixed(2)}"`);
}
function trackBot(y, h) { _lastBot = y + h; }
function resetBot() { _lastBot = 0; }


// Japanese educational slides. Original T/F/masters/math/chart/table helpers above.
function text(sl,t,x,y,w,h,size=18,color=T.tx.pri,face=F.body.face,bold=false){sl.addText(t,{x,y,w,h,fontSize:size,fontFace:face,color,bold,margin:0,valign:'mid',shrinkText:true,breakLine:false})}
function foot(sl,n,dark=false){text(sl,'学習用の仮想データ / 調査結果ではありません',.5,5.17,8.3,.2,10,dark?'C5CDD0':T.tx.mut);text(sl,String(n).padStart(2,'0'),9,5.12,.5,.3,11,dark?'FFFFFF':T.tx.mut,'Manrope')}
function dots(sl,vals,y,color,dark=false){
 const x=.9,w=4.4;
 sl.addShape(pres.ShapeType.line,{x,y:y+.27,w,h:0,line:{color:dark?'758084':'C9D0D3',width:.7}});
 vals.forEach(v=>sl.addShape(pres.ShapeType.ellipse,{x:x+w*v/10-.075,y:y+.195,w:.15,h:.15,line:{color,transparency:100},fill:{color}}));
}
// 01: dark cover, substantive native dot plots.
{
 const s=pres.addSlide({masterName:'TITLE_SLIDE'});
 text(s,'DATA / 5分の学習ノート',.55,.55,8.9,.35,14,'F3B156','Manrope',true);
 text(s,'平均の、\nその先。',.55,1.12,5.1,1.7,48,'FFFFFF','Shippori Mincho',true);
 text(s,'同じ「5」に、\n違う散らばり。',.58,3.35,4.6,1,24,'FFFFFF');
 text(s,'A',5.5,1.65,.5,.4,18,'60B5E2','Manrope',true); text(s,'4   5   6',6.05,1.65,3.1,.4,22,'FFFFFF','Manrope');
 text(s,'B',5.5,2.9,.5,.4,18,'F5B451','Manrope',true); text(s,'0   5   10',6.05,2.9,3.1,.4,22,'FFFFFF','Manrope');
 [1.15,2.4].forEach((dy,i)=>{const vals=i?[0,5,10]:[4,5,6];const color=i?'F5B451':'60B5E2';const x=6.05,w=3.1,y=dy+1.05;s.addShape(pres.ShapeType.line,{x,y,w,h:0,line:{color:'758084',width:.7}});vals.forEach(v=>s.addShape(pres.ShapeType.ellipse,{x:x+w*v/10-.065,y:y-.065,w:.13,h:.13,line:{color,transparency:100},fill:{color}}));});
 text(s,'0',5.96,4, .4,.3,12,'C5CDD0','Manrope');text(s,'10点',8.83,4,.6,.3,12,'C5CDD0');foot(s,1,true);
}
// 02: original native-table helper, with original OMML helper.
{
 const s=pres.addSlide({masterName:'CONTENT_SLIDE'});sTitle(s,'平均は、中心を表す');
 text(s,'3件ずつの得点。どちらが、中心に集まっている？',.55,1.03,9,.5,19);
 F.tblCell.size=22;F.tblHead.size=16;
 const c=t=>({text:String(t),options:{fontFace:'Manrope',align:'center'}});
 addTable(s,['データ','1件目','2件目','3件目'],[[c('A'),c(4),c(5),c(6)],[c('B'),c(0),c(5),c(10)]],.6,1.92,4.4,[1.2,1.07,1.07,1.06],.6);
 addMathText(s,'mean',5.4,1.68,4,1.05,{fontSize:27});
 addMathText(s,'mean-a',.65,3.77,4.4,1,{fontSize:25,color:T.ac.pos});
 addMathText(s,'mean-b',5.25,3.77,4.1,1,{fontSize:25,color:T.ac.neg});
 text(s,'足して、件数で割る。平均だけでは、散らばりは見えない。',.65,4.83,8.7,.25,14,T.tx.sec);foot(s,2);
}
// 03: formula and native bar chart, not an image renderer.
{
 const s=pres.addSlide({masterName:'CONTENT_SLIDE'});sTitle(s,'分散は、ずれを二乗して平均する');
 text(s,'平均からのずれ。二乗すると、正負が打ち消し合わない。',.6,.95,8.9,.45,17);
 addMathText(s,'variance',.6,1.55,8.8,1.1,{fontSize:29});
 F.tblCell.size=12;F.caption.size=11;
 addChart(s,pres.ChartType.bar,[{name:'A',labels:['1件目','2件目','3件目'],values:[1,0,1]},{name:'B',labels:['1件目','2件目','3件目'],values:[25,0,25]}],.6,2.75,4.5,1.77,{showLegend:true,chartColors:[T.ac.pos,T.ac.neg],catAxisLabelFontSize:10,valAxisLabelFontSize:10,valAxisMinVal:0,valAxisMaxVal:25,valAxisMajorUnit:5,showValue:false,showTitle:false,showBorder:false,showCatName:false});
 text(s,'二乗したずれの大きさ',.8,4.54,4.1,.25,11,T.tx.sec);
 addMathText(s,'var-a',5.3,2.83,4.05,.78,{fontSize:24,color:T.ac.pos});
 addMathText(s,'var-b',5.3,3.92,4.05,.78,{fontSize:24,color:T.ac.neg});
 text(s,'全3件を「全体」として計算。分母はn（ここでは3）。',.6,4.84,8.9,.22,12,T.tx.sec);foot(s,3);
}
// 04: original native-chart helper plus native radical formulas.
{
 const s=pres.addSlide({masterName:'CONTENT_SLIDE'});sTitle(s,'標準偏差で、元の単位に戻す');
 text(s,'分散の単位は「点の二乗」。平方根で「点」に戻す。',.6,.97,8.9,.45,18);
 addMathText(s,'sd',.6,1.62,3.1,1,{fontSize:37});
 text(s,'平均からの広がりを\n同じ単位で比べる目安。',4.7,1.7,4.6,.82,21);
 addMathText(s,'sd-a',.65,2.9,4.15,1.05,{fontSize:26,color:T.ac.pos});
 addMathText(s,'sd-b',5.2,2.9,4.15,1.05,{fontSize:26,color:T.ac.neg});
 addChart(s,pres.ChartType.bar,[{name:'標準偏差',labels:['A','B'],values:[.8164965809,4.082482905]}],.7,4.07,8.6,.85,{barDir:'bar',showLegend:false,varyColors:true,chartColors:[T.ac.pos,T.ac.neg],catAxisLabelFontFace:'Manrope',catAxisLabelFontSize:12,catAxisLabelFrequency:'1',valAxisMinVal:0,valAxisMaxVal:5,valAxisMajorUnit:1,valAxisLabelFontSize:10,valGridLine:{color:'D0D0D0',width:.4},showValue:false});
 foot(s,4);
}
// 05: dark conclusion, editable summary table and a concrete reading habit.
{
 const s=pres.addSlide({masterName:'THANK_YOU'});
 text(s,'平均と散らばりを、\n一緒に読む',.6,.58,8.8,1.2,35,'FFFFFF','Shippori Mincho',true);
 text(s,'平均',.6,2.3,2.4,.4,18,'C5CDD0');text(s,'中心の位置',3.3,2.3,5.6,.4,25,'FFFFFF');
 text(s,'標準偏差',.6,3.03,2.4,.4,18,'C5CDD0');text(s,'中心からの広がり',3.3,3.03,5.6,.4,25,'FFFFFF');
 s.addTable([[{text:'',options:{fill:{color:T.bg.title}}},{text:'A',options:{color:'60B5E2'}},{text:'B',options:{color:'F5B451'}}],[['平均（点）','5','5']].flat(),[['標準偏差（点）','0.82','4.08']].flat()],{x:.65,y:3.84,w:8.6,colW:[4,2.3,2.3],rowH:.34,fontFace:F.body.face,fontSize:16,color:'FFFFFF',fill:{color:T.bg.title},border:{type:'solid',color:'677276',pt:.4},margin:5,align:'center'});
 text(s,'※ 全体の分散を使用。標本から推定する不偏分散とは区別。',.65,4.94,8.7,.2,11,'C5CDD0');foot(s,5,true);
}
pres.writeFile({fileName:'source/deck-placeholders.pptx'}).then(()=>console.log('Original theme/helpers: 5 Japanese slides generated.'));
