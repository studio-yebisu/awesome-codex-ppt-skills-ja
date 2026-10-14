#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");

function parseArgs(argv) {
  const values = {};
  for (let index = 2; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || value === undefined) throw new Error("Use --input <presentation.json> --output <slide.pptx>");
    values[key.slice(2)] = value;
  }
  if (!values.input || !values.output) throw new Error("Use --input <presentation.json> --output <slide.pptx>");
  return values;
}

function hex(value, fallback = "000000") {
  if (!value || value === "none") return fallback;
  return value.replace("#", "").toUpperCase();
}

function geometry(box, dimensions, slideSize) {
  const [x, y, width, height] = box;
  return {
    x: x * slideSize.width / dimensions[0],
    y: y * slideSize.height / dimensions[1],
    w: width * slideSize.width / dimensions[0],
    h: height * slideSize.height / dimensions[1],
  };
}

function pixelPoints(px, dimensions, slideSize) {
  return Math.max(0, Number(px ?? 0) * slideSize.width * 72 / dimensions[0]);
}

function halfPointFloor(value) {
  let units = Number(value) * 2;
  const nearest = Math.round(units);
  // Match the Python fitter at exact half-point boundaries after unit conversion.
  if (Math.abs(units - nearest) <= Math.max(1e-9, 1e-7 * Math.max(Math.abs(units), Math.abs(nearest)))) units = nearest;
  return Math.max(0.5, Math.floor(units) / 2);
}

function resolvedFontSize(style, fallbackPx, dimensions, slideSize) {
  if (style.font_size_pt === undefined) return halfPointFloor(pixelPoints(style.font_size_px ?? fallbackPx, dimensions, slideSize));
  if (typeof style.font_size_pt !== "number" || !Number.isFinite(style.font_size_pt) || style.font_size_pt <= 0) {
    throw new Error("font_size_pt must be a positive finite number");
  }
  return style.font_size_pt;
}

function addTextbox(slide, object, dimensions, slideSize, postprocessHints) {
  const style = object.style ?? {};
  const lineSpacing = style.line_spacing_multiple === undefined ? 1 : style.line_spacing_multiple;
  if (typeof lineSpacing !== "number" || !Number.isFinite(lineSpacing) || lineSpacing <= 0) {
    throw new Error(`Text ${object.id} line_spacing_multiple must be a positive finite number`);
  }
  const pxToPoints = (value) => pixelPoints(value, dimensions, slideSize);
  if (style.char_spacing_px !== undefined) {
    if (typeof style.char_spacing_px !== "number" || !Number.isFinite(style.char_spacing_px)) throw new Error(`Text ${object.id} requires finite character spacing`);
    // DrawingML uses signed hundredths of a point. PptxGenJS omits negative spacing.
    postprocessHints.text_character_spacing[object.id] = Math.round(style.char_spacing_px * slideSize.width * 72 / dimensions[0] * 100);
  }
  const margins = style.margins_px ?? [0, 0, 0, 0];
  const officeMargins = Array.isArray(margins)
    ? [margins[1], margins[2], margins[3], margins[0]].map(pxToPoints)
    : pxToPoints(margins);
  const paragraphs = Array.isArray(object.paragraphs) ? object.paragraphs : null;
  const content = paragraphs && object.bullet_style
    ? paragraphs.map((paragraph, index) => ({
        text: `•  ${paragraph}`,
        options: { breakLine: index < paragraphs.length - 1 },
      }))
    : object.text ?? "";
  slide.addText(content, {
    objectName: object.id,
    ...geometry(object.bbox_px, dimensions, slideSize),
    fontFace: style.font_family ?? "Arial",
    fontSize: resolvedFontSize(style, 20, dimensions, slideSize),
    bold: style.font_weight === "bold" || Number(style.font_weight) >= 600,
    italic: Boolean(style.italic),
    charSpacing: pxToPoints(style.char_spacing_px ?? 0),
    color: hex(style.color, "111111"),
    align: style.alignment ?? "left",
    valign: style.vertical_alignment === "middle" ? "mid" : style.vertical_alignment ?? "top",
    margin: officeMargins,
    breakLine: false,
    fit: style.autofit === "shrink" ? "shrink" : "none",
    paraSpaceBeforePt: 0,
    paraSpaceAfterPt: pxToPoints(style.paragraph_spacing_px ?? 0),
    lineSpacingMultiple: lineSpacing,
    wrap: true,
    isTextBox: true,
  });
}

function addShape(slide, object, dimensions, slideSize, pptx, postprocessHints) {
  const style = object.style ?? {};
  const box = geometry(object.bbox_px, dimensions, slideSize);
  const shapes = {
    rectangle: pptx.ShapeType.rect,
    parallelogram: pptx.ShapeType.parallelogram,
    trapezoid: pptx.ShapeType.trapezoid,
    ellipse: pptx.ShapeType.ellipse,
    rounded_rectangle: pptx.ShapeType.roundRect,
    line: pptx.ShapeType.line,
  };
  const type = shapes[object.shape] ?? pptx.ShapeType.rect;
  if (object.shape === "rounded_rectangle" && Number.isFinite(Number(object.round_rect_adjustment))) {
    postprocessHints.round_rect_adjustments[object.id] = Number(object.round_rect_adjustment);
  }
  const options = {
    objectName: object.id,
    ...box,
    fill: object.shape === "line" || style.fill === "none" ? { color: "FFFFFF", transparency: 100 } : { color: hex(style.fill, "FFFFFF") },
    line: style.stroke === "none" ? { color: "FFFFFF", transparency: 100 } : { color: hex(style.stroke, "D9D9D9"), width: Math.max(0.5, pixelPoints(style.stroke_width_px ?? 1, dimensions, slideSize)) },
  };
  slide.addShape(type, options);
}

function gradientCoordinates(direction) {
  if (direction === "top_left_to_bottom_right") return { x1: "0%", y1: "0%", x2: "100%", y2: "100%" };
  if (direction === "top_right_to_bottom_left") return { x1: "100%", y1: "0%", x2: "0%", y2: "100%" };
  if (direction === "bottom_right_to_top_left") return { x1: "100%", y1: "100%", x2: "0%", y2: "0%" };
  return { x1: "0%", y1: "100%", x2: "100%", y2: "0%" };
}

function applyFillAllTreatment(svg, object) {
  let paint = null;
  let defs = "";
  if (object.recolor_gradient) {
    const gradient = object.recolor_gradient;
    const coords = gradientCoordinates(String(gradient.direction ?? "bottom_left_to_top_right"));
    const gradientId = `scGradient_${String(object.id).replace(/[^A-Za-z0-9_]/g, "_")}`;
    let stops = Array.isArray(gradient.stops) ? gradient.stops : [];
    if (!stops.length) {
      if (!gradient.from || !gradient.to) throw new Error(`Gradient recolor for ${object.id} requires stops or explicit from/to colours`);
      stops = [{ offset: 0, color: gradient.from }, { offset: 1, color: gradient.to }];
    }
    const stopXml = stops.map((stop) => {
      const raw = Number(stop.offset);
      if (!Number.isFinite(raw) || raw < 0 || raw > 1 || !stop.color) throw new Error(`Invalid gradient stop for ${object.id}`);
      return `<stop offset="${raw * 100}%" stop-color="${String(stop.color)}"/>`;
    }).join("");
    defs = `<defs><linearGradient id="${gradientId}" x1="${coords.x1}" y1="${coords.y1}" x2="${coords.x2}" y2="${coords.y2}">${stopXml}</linearGradient></defs>`;
    paint = `url(#${gradientId})`;
  } else if (object.recolor) {
    paint = String(object.recolor);
  }
  if (!paint) return svg;
  let rewritten = svg.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "");
  rewritten = rewritten.replace(/<(path|rect|circle|ellipse|polygon|polyline)\b([^>]*?)(\/?)>/gi, (match, tag, attrs, selfClose) => {
    let cleaned = attrs.replace(/\sfill=(['"]).*?\1/gi, "");
    cleaned = cleaned.replace(/\sstyle=(['"])(.*?)\1/gi, (styleMatch, quote, styleBody) => {
      const next = String(styleBody).replace(/(?:^|;)\s*fill\s*:[^;]*/gi, "").replace(/^;+|;+$/g, "");
      return next ? ` style=${quote}${next}${quote}` : "";
    });
    return `<${tag}${cleaned} fill="${paint}"${selfClose}>`;
  });
  return rewritten.replace(/<svg([^>]*)>/i, (match) => `${match}${defs}`);
}

function addImage(slide, object, dimensions, slideSize) {
  if (object.source_sha256 && createHash("sha256").update(fs.readFileSync(object.source_path)).digest("hex") !== object.source_sha256) {
    throw new Error(`Raster source for ${object.id} changed after scene compilation`);
  }
  let imageSource = { path: object.source_path };
  const isSvg = String(object.source_path).toLowerCase().endsWith(".svg");
  if ((object.recolor_gradient || object.recolor) && isSvg && object.recolor_mode === "fill_all") {
    const svg = applyFillAllTreatment(fs.readFileSync(object.source_path, "utf8"), object);
    imageSource = { data: `data:image/svg+xml;base64,${Buffer.from(svg).toString("base64")}` };
  } else if (object.recolor_gradient && isSvg) {
    const gradient = object.recolor_gradient ?? {};
    if (!gradient.from || !gradient.to) throw new Error(`Gradient recolor for ${object.id} requires explicit from and to colours from the active profile or semantic map`);
    const from = String(gradient.from);
    const to = String(gradient.to);
    const coords = gradientCoordinates(String(gradient.direction ?? "bottom_left_to_top_right"));
    const gradientId = `scGradient_${String(object.id).replace(/[^A-Za-z0-9_]/g, "_")}`;
    const defs = `<defs><linearGradient id="${gradientId}" x1="${coords.x1}" y1="${coords.y1}" x2="${coords.x2}" y2="${coords.y2}"><stop offset="0%" stop-color="${from}"/><stop offset="100%" stop-color="${to}"/></linearGradient></defs>`;
    let svg = fs.readFileSync(object.source_path, "utf8");
    const paint = `url(#${gradientId})`;
    svg = svg.replace(/<svg([^>]*)>/i, (match) => `${match}${defs}`)
      .replaceAll("currentColor", paint)
      .replace(/#000000\b/gi, paint)
      .replace(/#000\b/gi, paint)
      .replace(/(["'])black\1/gi, (match, quote) => `${quote}${paint}${quote}`);
    imageSource = { data: `data:image/svg+xml;base64,${Buffer.from(svg).toString("base64")}` };
  } else if (object.recolor && isSvg) {
    const color = String(object.recolor);
    const svg = fs.readFileSync(object.source_path, "utf8")
      .replaceAll("currentColor", color)
      .replace(/#000000\b/gi, color)
      .replace(/#000\b/gi, color)
      .replace(/(["'])black\1/gi, (match, quote) => `${quote}${color}${quote}`);
    imageSource = { data: `data:image/svg+xml;base64,${Buffer.from(svg).toString("base64")}` };
  }
  let box = geometry(object.bbox_px, dimensions, slideSize);
  if (String(object.source_path).toLowerCase().endsWith(".svg") && object.preserve_aspect_ratio !== false) {
    const svg = fs.readFileSync(object.source_path, "utf8");
    const viewBox = svg.match(/viewBox=["']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)\s*["']/i);
    const width = svg.match(/\bwidth=["']([\d.]+)(?:px)?["']/i);
    const height = svg.match(/\bheight=["']([\d.]+)(?:px)?["']/i);
    const ratio = viewBox ? Number(viewBox[1]) / Number(viewBox[2]) : width && height ? Number(width[1]) / Number(height[1]) : null;
    if (ratio && Number.isFinite(ratio) && ratio > 0) {
      const fittedWidth = Math.min(box.w, box.h * ratio);
      const fittedHeight = fittedWidth / ratio;
      box = { x: box.x + (box.w - fittedWidth) / 2, y: box.y + (box.h - fittedHeight) / 2, w: fittedWidth, h: fittedHeight };
    }
  }
  slide.addImage({
    ...imageSource,
    objectName: object.id,
    altText: object.selected_asset_id ?? object.semantic_role ?? object.id,
    ...box,
  });
}

function transparentBorder() {
  return { type: "solid", color: "FFFFFF", transparency: 100, pt: 0.1 };
}

function tableCellText(value) {
  if (Array.isArray(value)) {
    return value.map(run => {
      if (!run || typeof run !== "object" || Array.isArray(run) || typeof run.text !== "string"
          || (run.options !== undefined && (!run.options || typeof run.options !== "object" || Array.isArray(run.options)))) {
        throw new Error("Table rich text needs text strings and optional formatting objects");
      }
      return { text: run.text, options: { ...(run.options ?? {}) } };
    });
  }
  if (value !== null && typeof value === "object") throw new Error("Table text must be a string or a list of text runs");
  return String(value ?? "");
}

function applyComponentTableStyle(rows, tableStyle, dimensions, slideSize) {
  if (!tableStyle || !Object.keys(tableStyle).length) return rows;
  const rowCount = rows.length;
  const colCount = Math.max(0, ...rows.map((row) => row.length));
  const ruleColor = tableStyle.horizontal_rule_color ? hex(tableStyle.horizontal_rule_color) : null;
  const rulePt = Math.max(0.1, Number(tableStyle.horizontal_rule_width_pt ?? 0.5));
  return rows.map((row, r) => row.map((cell, c) => {
    const normalized = cell && typeof cell === "object" && !Array.isArray(cell)
      ? { text: tableCellText(cell.text), options: { ...(cell.options ?? {}) } }
      : { text: tableCellText(cell), options: {} };
    const options = normalized.options;
    let fill = tableStyle.body_fill;
    if (r === 0 && tableStyle.header_row_fill) fill = tableStyle.header_row_fill;
    else if (c === 0 && tableStyle.first_column_fill) fill = tableStyle.first_column_fill;
    else if (r > 0 && tableStyle.alternate_row_fill && r % 2 === 0) fill = tableStyle.alternate_row_fill;
    if (fill && !options.fill) options.fill = { color: hex(fill) };
    if (tableStyle.text_color && !options.color) options.color = hex(tableStyle.text_color);
    if (r === 0 && tableStyle.header_bold && options.bold === undefined) options.bold = true;
    if (c === 0 && r === 0 && tableStyle.first_column_bold_header && options.bold === undefined) options.bold = true;
    if (!options.border && (ruleColor || tableStyle.vertical_rules === false || tableStyle.horizontal_rules === false)) {
      const none = transparentBorder();
      const horizontal = ruleColor ? { type: "solid", color: ruleColor, pt: rulePt } : none;
      options.border = [
        tableStyle.horizontal_rules === false ? none : horizontal,
        tableStyle.vertical_rules === false ? none : horizontal,
        tableStyle.horizontal_rules === false ? none : horizontal,
        tableStyle.vertical_rules === false ? none : horizontal,
      ];
    }
    return { text: normalized.text, options };
  }));
}

function addTable(slide, object, dimensions, slideSize) {
  const structure = object.structure ?? {};
  const rawRows = structure.rows ?? object.rows ?? structure.data ?? [];
  let rows = rawRows.map((row) => row.map((cell) => {
    if (cell && typeof cell === "object" && !Array.isArray(cell)) {
      const options = { ...(cell.options ?? {}) };
      // Pixel allocations belong to the slide canvas. Legacy options.margin
      // remains in Office points for compatibility with authored native options.
      if (cell.margin_px !== undefined) {
        if (options.margin !== undefined) throw new Error(`Table ${object.id} cell cannot mix margin_px and options.margin`);
        const margins = Array.isArray(cell.margin_px) ? cell.margin_px : [cell.margin_px, cell.margin_px, cell.margin_px, cell.margin_px];
        if (margins.length !== 4 || margins.some(value => typeof value !== "number" || !Number.isFinite(value) || value < 0)) {
          throw new Error(`Table ${object.id} cell requires four finite nonnegative pixel margins`);
        }
        options.margin = margins.map(value => pixelPoints(value, dimensions, slideSize));
      }
      if (cell.rowSpan ?? cell.rowspan) options.rowSpan = cell.rowSpan ?? cell.rowspan;
      if (cell.colSpan ?? cell.colspan) options.colSpan = cell.colSpan ?? cell.colspan;
      return { text: tableCellText(cell.text ?? cell.value), options };
    }
    return tableCellText(cell);
  }));
  if (!rows.length) throw new Error(`Native table ${object.id} has no authored row data`);
  rows = applyComponentTableStyle(rows, structure.table_style ?? {}, dimensions, slideSize);
  const style = object.style ?? {};
  const box = geometry(object.bbox_px, dimensions, slideSize);
  const hasComponentStyle = structure.table_style && Object.keys(structure.table_style).length > 0;
  const options = {
    objectName: object.id,
    ...box,
    border: hasComponentStyle ? transparentBorder() : { type: "solid", color: hex(style.stroke, "B8B8B8"), pt: Math.max(0.5, pixelPoints(style.stroke_width_px ?? 1, dimensions, slideSize)) },
    fill: { color: hex(style.fill, "FFFFFF") },
    color: hex(style.color, "111111"),
    fontFace: style.font_family ?? "Arial",
    fontSize: resolvedFontSize(style, 16, dimensions, slideSize),
    margin: pixelPoints(style.cell_margin_px ?? 6, dimensions, slideSize),
    valign: style.vertical_alignment === "mid" ? "middle" : style.vertical_alignment ?? "top",
    autoFit: false,
    autoPage: false,
  };
  const columnWidths = structure.column_widths_px ?? structure.columns_px;
  if (Array.isArray(columnWidths) && columnWidths.length) {
    const values = columnWidths.length === rows[0].length + 1
      ? columnWidths.slice(1).map((value, index) => Number(value) - Number(columnWidths[index]))
      : columnWidths.map(Number);
    const total = values.reduce((sum, value) => sum + value, 0);
    if (total > 0 && values.length === rows[0].length) options.colW = values.map((value) => box.w * value / total);
  }
  const rowHeights = structure.row_heights_px ?? structure.rows_px;
  if (Array.isArray(rowHeights) && rowHeights.length) {
    const values = rowHeights.length === rows.length + 1
      ? rowHeights.slice(1).map((value, index) => Number(value) - Number(rowHeights[index]))
      : rowHeights.map(Number);
    const total = values.reduce((sum, value) => sum + value, 0);
    if (total > 0 && values.length === rows.length) options.rowH = values.map((value) => box.h * value / total);
  }
  slide.addTable(rows, options);
}

function legendPosition(value) {
  const map = { bottom: "b", left: "l", right: "r", top: "t", topRight: "tr", topright: "tr" };
  return map[String(value ?? "").replace(/[_ -]/g, "")] ?? undefined;
}

function addChart(slide, object, dimensions, slideSize, pptx, slideHints) {
  const structure = object.structure ?? {};
  const aliases = { column: pptx.ChartType.bar, bar: pptx.ChartType.bar, line: pptx.ChartType.line, pie: pptx.ChartType.pie, doughnut: pptx.ChartType.doughnut, area: pptx.ChartType.area, scatter: pptx.ChartType.scatter };
  const typeName = String(structure.type ?? object.chart_type ?? "bar").toLowerCase();
  const type = aliases[typeName];
  if (!type) throw new Error(`Unsupported native chart type ${typeName}`);
  if (!Array.isArray(structure.series) || !structure.series.length) throw new Error(`Editable chart ${object.id} has no authored series data`);
  const series = structure.series.map((item) => {
    const labels = item?.labels ?? structure.categories;
    const values = item?.values;
    if (!Array.isArray(labels) || !Array.isArray(values) || !values.length || labels.length !== values.length || values.some(value => typeof value !== "number" || !Number.isFinite(value))) {
      throw new Error(`Editable chart ${object.id} requires matching category labels and finite numeric values`);
    }
    return { name: String(item.name ?? "Series"), labels: labels.map(String), values: [...values] };
  });
  const style = object.style ?? {};
  if (structure.data_label_position !== undefined && !["b", "bestFit", "ctr", "l", "r", "t", "inBase", "inEnd", "outEnd"].includes(structure.data_label_position)) {
    throw new Error(`Chart ${object.id} data_label_position is not a native label position`);
  }
  if (structure.data_label_colors !== undefined && (!Array.isArray(structure.data_label_colors) ||
      series.some(item => item.values.length !== structure.data_label_colors.length) ||
      structure.data_label_colors.some(value => typeof value !== "string" || !/^#?[0-9a-f]{6}$/i.test(value)))) {
    throw new Error(`Chart ${object.id} data_label_colors requires one six-digit color per category`);
  }
  if (structure.data_font_bold !== undefined && typeof structure.data_font_bold !== "boolean") {
    throw new Error(`Chart ${object.id} data_font_bold must be a boolean`);
  }
  if (structure.data_label_wrap !== undefined && typeof structure.data_label_wrap !== "boolean") {
    throw new Error(`Chart ${object.id} data_label_wrap must be a boolean`);
  }
  if (structure.data_label_position !== undefined || structure.data_label_colors !== undefined || structure.data_label_wrap !== undefined) {
    slideHints.chart_label_treatments[object.id] = {
      position: structure.data_label_position,
      colors: structure.data_label_colors?.map(value => hex(value)),
      wrap: structure.data_label_wrap,
    };
  }
  const options = {
    objectName: object.id,
    ...geometry(object.bbox_px, dimensions, slideSize),
    showTitle: Boolean(structure.title),
    barDir: typeName === "bar" ? "bar" : "col",
    title: structure.title ?? "",
    titleFontFace: structure.title_font_family ?? undefined,
    fontFace: structure.data_font_family ?? undefined,
    catAxisLabelFontFace: structure.data_font_family ?? undefined,
    valAxisLabelFontFace: structure.data_font_family ?? undefined,
    legendFontFace: structure.data_font_family ?? undefined,
    showLegend: structure.show_legend !== false,
    legendPos: legendPosition(structure.legend_position),
    showValue: Boolean(structure.show_values),
    showPercent: Boolean(structure.show_percent),
    dataLabelPosition: structure.data_label_position ?? undefined,
    dataLabelFormatCode: structure.data_label_format_code ?? undefined,
    dataLabelColor: structure.data_label_color ? hex(structure.data_label_color) : undefined,
    dataLabelFontFace: structure.data_font_family ?? undefined,
    dataLabelFontBold: structure.data_font_bold ?? undefined,
    valAxisLabelFormatCode: structure.value_axis_format_code ?? undefined,
    chartColors: structure.colors?.map((value) => hex(value)) ?? undefined,
    showCatName: false,
    showSerName: false,
    border: { color: hex(style.stroke, "FFFFFF"), pt: style.stroke === "none" ? 0 : 0.5 },
  };
  for (const [key, option] of Object.entries({hole_size: "holeSize", gap_width_pct: "barGapWidthPct", value_axis_minimum: "valAxisMinVal", value_axis_maximum: "valAxisMaxVal"})) {
    if (structure[key] === undefined) continue;
    if (typeof structure[key] !== "number" || !Number.isFinite(structure[key])) throw new Error(`Chart ${object.id} ${key} must be a finite number`);
    options[option] = structure[key];
  }
  if (options.valAxisMinVal !== undefined && options.valAxisMaxVal !== undefined && options.valAxisMinVal >= options.valAxisMaxVal) {
    throw new Error(`Chart ${object.id} value_axis_minimum must be less than value_axis_maximum`);
  }
  if (structure.data_font_size_px !== undefined) {
    if (typeof structure.data_font_size_px !== "number" || !Number.isFinite(structure.data_font_size_px) || structure.data_font_size_px <= 0) {
      throw new Error(`Chart ${object.id} data_font_size_px must be a positive finite number`);
    }
    options.dataLabelFontSize = pixelPoints(structure.data_font_size_px, dimensions, slideSize);
  }
  if (structure.bar_grouping) options.barGrouping = String(structure.bar_grouping);
  if (structure.show_category_axis === false) options.catAxisHidden = true;
  if (structure.show_value_axis === false) options.valAxisHidden = true;
  if (structure.category_order === "reverse") options.catAxisOrientation = "maxMin";
  if (structure.plot_layout) {
    const layout = structure.plot_layout;
    if (["x", "y", "w", "h"].some(key => typeof layout[key] !== "number" || !Number.isFinite(layout[key]) || layout[key] < 0 || layout[key] > 1) || layout.w === 0 || layout.h === 0 || layout.x + layout.w > 1 || layout.y + layout.h > 1) {
      throw new Error(`Chart ${object.id} plot_layout must fit inside the chart in relative coordinates`);
    }
    options.layout = { ...layout };
  }
  if (structure.show_value_gridlines === false) options.valGridLine = { color: "FFFFFF", transparency: 100, width: 0.1 };
  else if (structure.show_value_gridlines === true && structure.gridline_color) options.valGridLine = { color: hex(structure.gridline_color), width: 0.75 };
  slide.addChart(type, series, options);
}

function addFreeform(slide, object, dimensions, slideSize, pptx) {
  const box = geometry(object.bbox_px, dimensions, slideSize);
  if (object.path_commands_px?.length) {
    const local = point => ({ x: (point[0] - object.bbox_px[0]) * slideSize.width / dimensions[0], y: (point[1] - object.bbox_px[1]) * slideSize.height / dimensions[1] });
    const points = object.path_commands_px.map(command => {
      if (command.op === "Z") return { close: true };
      const point = local(command.point);
      if (command.op === "M") return { ...point, moveTo: true };
      if (command.op === "L") return point;
      if (command.op === "C") {
        const c1 = local(command.control1), c2 = local(command.control2);
        return { ...point, curve: { type: "cubic", x1: c1.x, y1: c1.y, x2: c2.x, y2: c2.y } };
      }
      throw new Error(`Unsupported authored path operation ${command.op}`);
    });
    const style = object.style ?? {};
    slide.addShape(pptx.ShapeType.custGeom, {
      objectName: object.id, ...box, points,
      fill: { color: hex(style.fill, "FFFFFF"), transparency: style.fill === "none" ? 100 : 0 },
      line: style.stroke === "none"
        ? { color: "FFFFFF", transparency: 100 }
        : { color: hex(style.stroke, "111111"), width: Math.max(0.1, pixelPoints(style.stroke_width_px ?? 1, dimensions, slideSize)), endArrowType: style.end_arrow_type ?? "none", beginArrowType: "none" },
    });
    return;
  }
  const contourCandidates = object.contours_px ?? [];
  const explicit = object.points ?? object.contour ?? object.structure?.points ?? object.structure?.contour;
  const contours = explicit ? [explicit] : contourCandidates;
  if (!contours.length || contours.some(contour => contour.length < 3)) throw new Error(`Freeform ${object.id} has insufficient fitted geometry`);
  if (object.coordinates != null && !["local", "absolute"].includes(object.coordinates)) throw new Error(`Freeform ${object.id} has an unknown coordinate space`);
  const sourceBox = object.bbox_px;
  const points = contours.flatMap(raw => [...raw.map((point, index) => {
    const x = Array.isArray(point) ? point[0] : point.x;
    const y = Array.isArray(point) ? point[1] : point.y;
    const local = object.coordinates === "local";
    const nx = local ? Number(x) / Math.max(1, sourceBox[2]) : (Number(x) - sourceBox[0]) / Math.max(1, sourceBox[2]);
    const ny = local ? Number(y) / Math.max(1, sourceBox[3]) : (Number(y) - sourceBox[1]) / Math.max(1, sourceBox[3]);
    return { x: Math.max(0, Math.min(box.w, nx * box.w)), y: Math.max(0, Math.min(box.h, ny * box.h)), moveTo: index === 0 };
  }), { close: true }]);
  const style = object.style ?? {};
  slide.addShape(pptx.ShapeType.custGeom, {
    objectName: object.id,
    ...box,
    points,
    fill: style.fill === "none" ? { color: "FFFFFF", transparency: 100 } : { color: hex(style.fill, "FFFFFF") },
    line: style.stroke === "none" ? { color: "FFFFFF", transparency: 100 } : { color: hex(style.stroke, "222222"), width: Math.max(0.5, pixelPoints(style.stroke_width_px ?? 1, dimensions, slideSize)) },
  });
}

function addLine(slide, start, end, dimensions, slideSize, style, arrowAtEnd, pptx, name) {
  const x1 = start[0] * slideSize.width / dimensions[0];
  const y1 = start[1] * slideSize.height / dimensions[1];
  const x2 = end[0] * slideSize.width / dimensions[0];
  const y2 = end[1] * slideSize.height / dimensions[1];
  slide.addShape(pptx.ShapeType.line, {
    objectName: name,
    x: Math.min(x1, x2),
    y: Math.min(y1, y2),
    w: Math.abs(x2 - x1),
    h: Math.abs(y2 - y1),
    flipH: x2 < x1,
    flipV: y2 < y1,
    line: {
      color: hex(style.color, "222222"),
      width: Math.max(0.1, pixelPoints(style.width_px ?? 3, dimensions, slideSize)),
      dash: style.dash === "dashed" ? "dash" : "solid",
      endArrowType: arrowAtEnd ? style.end_arrow_type ?? "triangle" : "none",
      beginArrowType: "none",
    },
  });
}

function addPolylineRoute(slide, points, dimensions, slideSize, style, arrowAtEnd, pptx, nextName, slideHints) {
  if (!Array.isArray(points) || points.length < 2) return;
  const name = points.length === 2 ? nextName() : nextName().replace("SC_CONNECTOR__", "SC_FREEFORM_ROUTE__");
  if (arrowAtEnd && style.arrowhead_native_size) {
    slideHints.arrowhead_sizes[name] = style.arrowhead_native_size;
  }
  if (points.length === 2) {
    // A native line preset carries explicit direction through its transform.
    addLine(slide, points[0], points[1], dimensions, slideSize, style, arrowAtEnd, pptx, name);
    return;
  }
  const converted = points.map(point => [
    point[0] * slideSize.width / dimensions[0],
    point[1] * slideSize.height / dimensions[1],
  ]);
  const minX = Math.min(...converted.map(point => point[0]));
  const minY = Math.min(...converted.map(point => point[1]));
  const maxX = Math.max(...converted.map(point => point[0]));
  const maxY = Math.max(...converted.map(point => point[1]));
  const width = Math.max(0.001, maxX - minX);
  const height = Math.max(0.001, maxY - minY);
  const geometryPoints = converted.map((point, index) => ({
    x: point[0] - minX,
    y: point[1] - minY,
    moveTo: index === 0,
  }));
  slide.addShape(pptx.ShapeType.custGeom, {
    // LibreOffice reroutes custom geometry stored as p:cxnSp. Retain authored
    // multi-segment paths as one editable freeform without automatic attachment.
    objectName: name,
    x: minX,
    y: minY,
    w: width,
    h: height,
    points: geometryPoints,
    fill: { color: "FFFFFF", transparency: 100 },
    line: {
      color: hex(style.color, "222222"),
      width: Math.max(0.1, pixelPoints(style.width_px ?? 3, dimensions, slideSize)),
      dash: style.dash === "dashed" ? "dash" : "solid",
      endArrowType: arrowAtEnd ? style.end_arrow_type ?? "triangle" : "none",
      beginArrowType: "none",
    },
  });
}

function addGroupingConnector(slide, object, dimensions, slideSize, pptx, nextName) {
  const boxPx = object.grouping_bbox_px;
  if (!Array.isArray(boxPx) || boxPx.length !== 4) throw new Error(`Grouping connector ${object.id} has no grouping_bbox_px`);
  const family = String(object.connector_family ?? "grouping_bracket");
  const side = String(object.grouping_side ?? "right").toLowerCase();
  const base = geometry(boxPx, dimensions, slideSize);
  const gapPx = Number(object.routing_constraints?.minimum_clearance_px ?? 12);
  const gapX = gapPx * slideSize.width / dimensions[0];
  const gapY = gapPx * slideSize.height / dimensions[1];
  const thickness = Math.max(0.5, pixelPoints(object.style?.width_px ?? 3, dimensions, slideSize));
  const isBrace = family === "grouping_brace";
  const authoredDepth = Number(object.grouping_depth_px ?? 0);
  const desiredDepthPx = authoredDepth > 0 ? authoredDepth : Number(isBrace
    ? object.routing_constraints?.grouping_brace_depth_px ?? 34
    : object.routing_constraints?.grouping_bracket_depth_px ?? 22);
  const depthPx = isBrace
    ? desiredDepthPx * Number(object.routing_constraints?.grouping_brace_preset_depth_factor ?? 1.7)
    : desiredDepthPx;
  const depthX = depthPx * slideSize.width / dimensions[0];
  const depthY = depthPx * slideSize.height / dimensions[1];
  let shapeType = isBrace ? pptx.ShapeType.rightBrace : pptx.ShapeType.rightBracket;
  let shapeBox; let rotate = 0; let anchor;
  if (side === "left") {
    shapeType = isBrace ? pptx.ShapeType.leftBrace : pptx.ShapeType.leftBracket;
    shapeBox = { x: Math.max(0, base.x-gapX-depthX), y: base.y, w: depthX, h: base.h };
    anchor = [boxPx[0]-gapPx, boxPx[1]+boxPx[3]/2];
  } else if (side === "top" || side === "bottom") {
    shapeType = isBrace ? pptx.ShapeType.rightBrace : pptx.ShapeType.rightBracket;
    rotate = 90;
    shapeBox = side === "top"
      ? { x: base.x, y: Math.max(0, base.y-gapY-depthY), w: base.w, h: depthY }
      : { x: base.x, y: base.y+base.h+gapY, w: base.w, h: depthY };
    anchor = [boxPx[0]+boxPx[2]/2, side === "top" ? boxPx[1]-gapPx : boxPx[1]+boxPx[3]+gapPx];
  } else {
    shapeBox = { x: base.x+base.w+gapX, y: base.y, w: depthX, h: base.h };
    anchor = [boxPx[0]+boxPx[2]+gapPx, boxPx[1]+boxPx[3]/2];
  }
  const connectorColor = hex(object.style?.color ?? object.style?.stroke ?? "222222");
  slide.addShape(shapeType, {
    objectName: `${object.id}__${isBrace ? "BRACE" : "BRACKET"}`,
    ...shapeBox, rotate,
    // Keep grouping braces/brackets as editable native PowerPoint AutoShapes.
    // Brace presets require a wider bounding box than their visible indentation;
    // the configured calibration factor maps desired visible depth to preset width.
    fill: { color: "FFFFFF", transparency: 100 },
    line: { color: connectorColor, width: thickness },
  });
  if (Array.isArray(object.targets_px) && object.targets_px.length === 1) {
    const directed = Boolean(object.semantic_intent?.directed);
    addLine(slide, anchor, object.targets_px[0], dimensions, slideSize, object.style, directed, pptx, nextName());
  }
}

function addConnectorGraph(slide, object, dimensions, slideSize, pptx, slideHints) {
  let segment = 0;
  const nextName = () => `SC_CONNECTOR__${object.id}__${segment++}`;
  if (["grouping_bracket", "grouping_brace"].includes(String(object.connector_family ?? ""))) {
    addGroupingConnector(slide, object, dimensions, slideSize, pptx, nextName);
    return;
  }

  // The Python compiler is the sole geometry authority for directional
  // connectors. Rendering does not infer an orientation, add bends, or trace
  // the raster path. If compiled routes are missing, fail rather than silently
  // falling back to an older routing interpretation.
  if (!Array.isArray(object.source_routes_px) || !Array.isArray(object.target_routes_px)) {
    throw new Error(`Connector ${object.id} is missing compiled route geometry`);
  }
  if (object.source_routes_px.length === 0 && object.target_routes_px.length === 0) {
    throw new Error(`Directional connector ${object.id} has no compiled route segments`);
  }
  for (const route of object.source_routes_px) {
    addPolylineRoute(slide, route, dimensions, slideSize, object.style, false, pptx, nextName, slideHints);
  }
  for (const route of object.target_routes_px) {
    const directed = object.arrowhead_treatment !== "none" && object.semantic_intent?.directed !== false;
    const routeStyle = { ...object.style, end_arrow_type: object.arrowhead_treatment === "open_arrow_at_target" ? "arrow" : "triangle" };
    const arrowhead = object.arrowhead ?? {};
    const width = arrowhead.powerpoint_width ?? arrowhead.powerpoint_size ?? "med";
    const length = arrowhead.powerpoint_length ?? arrowhead.powerpoint_size ?? "med";
    if (![width, length].every(value => ["sm", "med", "lg"].includes(value))) {
      throw new Error(`Connector ${object.id} requires sm, med or lg native arrowhead dimensions`);
    }
    routeStyle.arrowhead_native_size = { width, length };
    addPolylineRoute(slide, route, dimensions, slideSize, routeStyle, directed, pptx, nextName, slideHints);
  }
  const junctionStyle = object.junction_style ?? {};
  if (junctionStyle.style === "filled_circle") {
    const diameterPx = Math.max(2, Number(junctionStyle.diameter_px ?? 10));
    const w = diameterPx * slideSize.width / dimensions[0];
    const h = diameterPx * slideSize.height / dimensions[1];
    for (let index = 0; index < (object.junctions_px ?? []).length; index += 1) {
      const point = object.junctions_px[index];
      const cx = point[0] * slideSize.width / dimensions[0];
      const cy = point[1] * slideSize.height / dimensions[1];
      slide.addShape(pptx.ShapeType.ellipse, {
        objectName: `${object.id}__JUNCTION_${index}`,
        x: cx - w / 2, y: cy - h / 2, w, h,
        fill: { color: hex(object.style?.color ?? "222222") },
        line: { color: hex(object.style?.color ?? "222222"), transparency: 100 },
      });
    }
  }
}

function postprocessorPath() {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const candidates = [
    path.resolve(here, "../scripts/postprocess_pptx.py"),
    path.resolve(here, "../../scripts/postprocess_pptx.py"),
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return candidate;
  }
  return null;
}

async function convertTaggedLinesToNativeConnectors(output, postprocessHints = {}) {
  const script = postprocessorPath();
  if (!script) throw new Error("The packaged PowerPoint postprocessor is missing");
  const python = process.env.PYTHON ?? process.env.PYTHON3 ?? (process.platform === "win32" ? "python" : "python3");
  const hintsPath = `${output}.slidepoise-postprocess.json`;
  fs.writeFileSync(hintsPath, JSON.stringify(postprocessHints));
  const result = spawnSync(python, [script, output, "--metadata", hintsPath], { encoding: "utf8" });
  try { fs.unlinkSync(hintsPath); } catch {}
  if (result.status !== 0) {
    throw new Error((result.stderr || result.stdout || "PowerPoint post-processing failed").trim());
  }
  try {
    return JSON.parse(result.stdout || "{}");
  } catch {
    return { converted: 0, textBodiesNormalized: 0, raw: result.stdout.trim() };
  }
}


function masterText(text, boxPx, style, dimensions, slideSize, align = "left") {
  const box = geometry(boxPx, dimensions, slideSize);
  return { text: { text: String(text ?? ""), options: {
    ...box,
    fontFace: style.font_family ?? "Arial",
    fontSize: halfPointFloor(pixelPoints(style.font_size_px ?? 12, dimensions, slideSize)),
    bold: style.font_weight === "bold",
    color: hex(style.text_color ?? "#4A4A4A", "4A4A4A"),
    align,
    valign: "mid",
    margin: 0,
    breakLine: false,
    fit: "shrink",
    objectName: style.object_name,
  } } };
}

function defineFrameMaster(pptx, scene, slideSize, index) {
  const frame = scene.frame ?? {};
  const header = frame.header ?? {};
  const footer = frame.footer ?? {};
  const dimensions = scene.dimensions_px;
  const headerEnabled = header.enabled !== false && Number(header.height_px ?? 0) > 0;
  const footerEnabled = footer.enabled !== false && Number(footer.height_px ?? 0) > 0;
  if (!headerEnabled && !footerEnabled) return null;
  const width = dimensions[0];
  const height = dimensions[1];
  const objects = [];
  if (headerEnabled) {
    const hh = Number(header.height_px);
    const pad = Number(header.outer_padding_px ?? 40);
    const textH = Math.max(16, hh - 10);
    const y = Math.max(1, (hh - textH) / 2);
    objects.push(masterText(header.left_text, [pad, y, width * 0.48 - pad, textH], { ...header, object_name: "SC_MASTER_HEADER_LEFT" }, dimensions, slideSize, "left"));
    const rightStyle = { ...header, text_color: header.secondary_text_color ?? header.text_color, object_name: "SC_MASTER_HEADER_RIGHT" };
    objects.push(masterText(header.right_text, [width * 0.52, y, width * 0.48 - pad, textH], rightStyle, dimensions, slideSize, "right"));
    objects.push({ line: { ...geometry([pad, hh - 1, width - 2 * pad, 0], dimensions, slideSize), line: { color: hex(header.rule_color ?? "#DED7CF", "DED7CF"), width: Math.max(0.5, pixelPoints(header.rule_width_px ?? 1, dimensions, slideSize)) } } });
    if (Number(header.accent_rule_width_px ?? 0) > 0) {
      objects.push({ line: { ...geometry([pad, hh - 1, Number(header.accent_rule_width_px), 0], dimensions, slideSize), line: { color: hex(header.accent_color ?? "#222222", "222222"), width: Math.max(0.5, pixelPoints(2, dimensions, slideSize)) } } });
    }
  }
  let slideNumber = null;
  if (footerEnabled) {
    const fh = Number(footer.height_px);
    const top = height - fh;
    const pad = Number(footer.outer_padding_px ?? 40);
    const textH = Math.max(16, fh - 10);
    const y = top + Math.max(1, (fh - textH) / 2);
    objects.push({ line: { ...geometry([pad, top, width - 2 * pad, 0], dimensions, slideSize), line: { color: hex(footer.rule_color ?? "#DED7CF", "DED7CF"), width: Math.max(0.5, pixelPoints(footer.rule_width_px ?? 1, dimensions, slideSize)) } } });
    objects.push(masterText(footer.left_text, [pad, y, width * 0.35, textH], { ...footer, font_weight: footer.left_font_weight ?? footer.font_weight, object_name: "SC_MASTER_FOOTER_LEFT" }, dimensions, slideSize, "left"));
    const centerStyle = { ...footer, text_color: footer.secondary_text_color ?? footer.text_color, object_name: "SC_MASTER_FOOTER_CENTER" };
    objects.push(masterText(footer.center_text, [width * 0.35, y, width * 0.30, textH], centerStyle, dimensions, slideSize, "center"));
    if (footer.slide_number?.enabled) {
      slideNumber = { ...geometry([width - pad - 160, y, 160, textH], dimensions, slideSize), fontFace: footer.font_family ?? "Arial", fontSize: halfPointFloor(pixelPoints(footer.font_size_px ?? 12, dimensions, slideSize)), color: hex(footer.secondary_text_color ?? footer.text_color ?? "#4A4A4A", "4A4A4A"), align: "right", valign: "middle", margin: 0 };
    }
  }
  const title = `SLIDEPOISE_MASTER_${index}`;
  pptx.defineSlideMaster({ title, background: { color: hex(scene.background ?? "#FFFFFF", "FFFFFF") }, objects, slideNumber });
  return title;
}

function frameMasterKey(scene) {
  const frame = { ...(scene.frame ?? {}) };
  // Page ordinal is supplied by the native slide-number field, not the master.
  delete frame.slide_number;
  return JSON.stringify({ frame, dimensions: scene.dimensions_px, background: scene.background ?? "#FFFFFF" },
    (_key, value) => value && typeof value === "object" && !Array.isArray(value)
      ? Object.fromEntries(Object.keys(value).sort().map(key => [key, value[key]])) : value);
}

async function main() {
  const args = parseArgs(process.argv);
  const spec = JSON.parse(fs.readFileSync(args.input, "utf8"));
  const pptx = new pptxgen();
  const rootScene = Array.isArray(spec.objects) && Array.isArray(spec.dimensions_px) ? spec : null;
  const scenes = Array.isArray(spec.slides) ? spec.slides : spec.slide ? [spec.slide] : rootScene ? [rootScene] : [];
  if (!scenes.length || scenes.some(scene => !scene || typeof scene !== "object")) throw new Error("SlidePoise requires one or more scenes at spec.slides");
  const dimensions = scenes[0].dimensions_px;
  if (!Array.isArray(dimensions) || dimensions.length !== 2) throw new Error("Scene dimensions_px are required");
  if (dimensions.some(value => typeof value !== "number" || !Number.isFinite(value) || value <= 0)) throw new Error("Scene dimensions_px must be positive finite numbers");
  for (const [index, scene] of scenes.entries()) {
    if (!Array.isArray(scene.dimensions_px) || scene.dimensions_px.length !== 2) throw new Error(`Slide ${index + 1} dimensions_px are required`);
    if (scene.dimensions_px[0] !== dimensions[0] || scene.dimensions_px[1] !== dimensions[1]) throw new Error(`Slide ${index + 1} dimensions do not match the first slide`);
  }
  const physicalWidth = 40 / 3;
  const physicalHeight = physicalWidth * Number(dimensions[1]) / Number(dimensions[0]);
  pptx.defineLayout({ name: "SLIDEPOISE_CUSTOM", width: physicalWidth, height: physicalHeight });
  pptx.layout = "SLIDEPOISE_CUSTOM";
  pptx.author = "SlidePoise";
  pptx.subject = "Editable presentation generated from SlidePoise scene contracts";
  pptx.title = spec.title ?? "SlidePoise presentation";
  pptx.company = spec.company ?? "";
  pptx.lang = spec.language ?? "en-US";
  pptx.theme = {
    headFontFace: spec.theme?.display_font ?? "Georgia",
    bodyFontFace: spec.theme?.body_font ?? "Arial",
    lang: spec.language ?? "en-US",
  };
  const slideSize = { width: physicalWidth, height: physicalHeight };
  const postprocessHints = { slides: {} };
  const frameMasters = new Map();
  for (const [index, scene] of scenes.entries()) {
    const slideHints = { round_rect_adjustments: {}, text_character_spacing: {}, chart_label_treatments: {}, arrowhead_sizes: {} };
    postprocessHints.slides[`ppt/slides/slide${index + 1}.xml`] = slideHints;
    const masterKey = frameMasterKey(scene);
    if (!frameMasters.has(masterKey)) frameMasters.set(masterKey, defineFrameMaster(pptx, scene, slideSize, frameMasters.size + 1));
    const masterName = frameMasters.get(masterKey);
    const slide = masterName ? pptx.addSlide(masterName) : pptx.addSlide();
    const background = String(scene.background ?? "#FFFFFF");
    slide.background = { color: hex(background.includes("#") ? background : "#FFFFFF", "FFFFFF") };
    const ordered = [...scene.objects].sort((left, right) => (left.z ?? 0) - (right.z ?? 0));
    for (const object of ordered) {
      if (object.kind === "textbox") addTextbox(slide, object, scene.dimensions_px, slideSize, slideHints);
      else if (object.kind === "shape") addShape(slide, object, scene.dimensions_px, slideSize, pptx, slideHints);
      else if (object.kind === "image") addImage(slide, object, scene.dimensions_px, slideSize);
      else if (object.kind === "connector_graph") addConnectorGraph(slide, object, scene.dimensions_px, slideSize, pptx, slideHints);
      else if (object.kind === "table") addTable(slide, object, scene.dimensions_px, slideSize);
      else if (object.kind === "chart") addChart(slide, object, scene.dimensions_px, slideSize, pptx, slideHints);
      else if (object.kind === "freeform") addFreeform(slide, object, scene.dimensions_px, slideSize, pptx);
      else throw new Error(`Unsupported constructor object kind ${object.kind}`);
    }
    const sources = scene.sources ?? scene.source_references ?? [];
    const speakerNotes = scene.speaker_notes === undefined ? [] : scene.speaker_notes;
    if (!Array.isArray(speakerNotes) || speakerNotes.some(note => typeof note !== "string")) {
      throw new Error("scene.speaker_notes must be an array of strings");
    }
    const notes = [...speakerNotes];
    if (sources.length) notes.push(`[SlidePoise sources]\n${sources.map((item) => typeof item === "string" ? item : JSON.stringify(item)).join("\n")}`);
    if (notes.length) slide.addNotes(notes.join("\n\n"));
  }
  const output = path.resolve(args.output);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  const staging = fs.mkdtempSync(path.join(path.dirname(output), ".slidepoise-render-"));
  try {
    const stagedOutput = path.join(staging, "presentation.pptx");
    await pptx.writeFile({ fileName: stagedOutput });
    await convertTaggedLinesToNativeConnectors(stagedOutput, postprocessHints);
    fs.renameSync(stagedOutput, output);
  } finally {
    fs.rmSync(staging, { recursive: true, force: true });
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
