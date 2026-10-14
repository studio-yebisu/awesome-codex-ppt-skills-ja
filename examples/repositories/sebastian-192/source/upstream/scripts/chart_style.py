"""Shared, round-trip verifiable native chart appearance settings."""

from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Pt

NS = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
LABEL_POSITIONS = {
    "outside_end": XL_LABEL_POSITION.OUTSIDE_END,
    "inside_end": XL_LABEL_POSITION.INSIDE_END,
    "center": XL_LABEL_POSITION.CENTER,
    "above": XL_LABEL_POSITION.ABOVE,
    "below": XL_LABEL_POSITION.BELOW,
    "best_fit": XL_LABEL_POSITION.BEST_FIT,
}


def set_value(parent, tag, value):
    node = parent.find(NS + tag)
    if node is None:
        node = OxmlElement("c:" + tag)
        if tag == "invertIfNegative" and parent.tag == NS + "dPt":
            parent.insert(1, node)  # dPt order: idx, invertIfNegative, ..., spPr
        else:
            parent.append(node)
    node.set("val", str(value))


def xml_value(parent, tag):
    node = parent.find(NS + tag)
    return node.get("val") if node is not None else None


def apply_style(chart, spec):
    plot = chart.plots[0]
    if spec.get("data_labels"):
        if "data_label_position" in spec:
            plot.data_labels.position = LABEL_POSITIONS[spec["data_label_position"]]
        if "data_label_font_size" in spec:
            plot.data_labels.font.size = Pt(spec["data_label_font_size"])
    if spec["chart_type"] not in ("pie", "doughnut"):
        for name, axis in (("category", chart.category_axis), ("value", chart.value_axis)):
            if name + "_axis_visible" in spec:
                visible = spec[name + "_axis_visible"]
                axis.visible = visible
                axis.tick_label_position = (
                    XL_TICK_LABEL_POSITION.NEXT_TO_AXIS if visible else XL_TICK_LABEL_POSITION.NONE
                )
        if "category_reverse_order" in spec:
            chart.category_axis.reverse_order = spec["category_reverse_order"]
    if "gap_width" in spec:
        plot.gap_width = spec["gap_width"]
    for series, item in zip(chart.series, spec["series"]):
        if "invert_if_negative" in item:
            series.invert_if_negative = item["invert_if_negative"]
        for index, point in enumerate(series.points):
            if "point_colors" in item:
                point.format.fill.solid()
                point.format.fill.fore_color.rgb = RGBColor.from_string(item["point_colors"][index][1:])
                point.format.line.fill.background()
            if "invert_if_negative" in item:
                # point._element is the series node; point.format._element is dPt.
                set_value(point.format._element, "invertIfNegative", int(item["invert_if_negative"]))
    for key, tag in (("hole_size", "holeSize"), ("first_slice_angle", "firstSliceAng")):
        if key in spec:
            set_value(plot._element, tag, spec[key])
    if "plot_layout" in spec:
        area = chart._chartSpace.find(".//" + NS + "plotArea")
        layout = area.find(NS + "layout")
        if layout is None:
            layout = OxmlElement("c:layout")
            area.insert(0, layout)
        old = layout.find(NS + "manualLayout")
        if old is not None:
            layout.remove(old)
        manual = OxmlElement("c:manualLayout")
        for tag, value in (
            ("layoutTarget", "inner"), ("xMode", "edge"), ("yMode", "edge"),
            ("wMode", "factor"), ("hMode", "factor"),
            *((key, spec["plot_layout"][key]) for key in ("x", "y", "w", "h")),
        ):
            set_value(manual, tag, value)
        layout.append(manual)


def style_errors(chart, spec):
    """Read exported objects independently; never reapply styles while auditing."""
    errors = []
    plot = chart.plots[0]
    if spec.get("data_labels"):
        if "data_label_position" in spec and plot.data_labels.position != LABEL_POSITIONS[spec["data_label_position"]]:
            errors.append("data label position")
        if "data_label_font_size" in spec and plot.data_labels.font.size != Pt(spec["data_label_font_size"]):
            errors.append("data label font size")
    if spec["chart_type"] not in ("pie", "doughnut"):
        for name, axis in (("category", chart.category_axis), ("value", chart.value_axis)):
            key = name + "_axis_visible"
            if key in spec and (axis.visible != spec[key] or (
                not spec[key] and axis.tick_label_position != XL_TICK_LABEL_POSITION.NONE
            )):
                errors.append(key)
        if "category_reverse_order" in spec and chart.category_axis.reverse_order != spec["category_reverse_order"]:
            errors.append("category reverse order")
    if "gap_width" in spec and plot.gap_width != spec["gap_width"]:
        errors.append("gap width")
    for series, item in zip(chart.series, spec["series"]):
        if "invert_if_negative" in item and series.invert_if_negative != item["invert_if_negative"]:
            errors.append("series negative fill")
        for index, point in enumerate(series.points):
            if "point_colors" in item:
                try:
                    color = "#" + str(point.format.fill.fore_color.rgb)
                except (AttributeError, ValueError):
                    color = None
                if color != item["point_colors"][index].upper():
                    errors.append(f"point {index} color")
            if "invert_if_negative" in item and xml_value(point.format._element, "invertIfNegative") != str(int(item["invert_if_negative"])):
                errors.append(f"point {index} negative fill")
    for key, tag in (("hole_size", "holeSize"), ("first_slice_angle", "firstSliceAng")):
        if key in spec and xml_value(plot._element, tag) != str(spec[key]):
            errors.append(key)
    if "plot_layout" in spec:
        manual = chart._chartSpace.find(".//" + NS + "manualLayout")
        expected = {"layoutTarget": "inner", "xMode": "edge", "yMode": "edge", "wMode": "factor", "hMode": "factor"}
        if manual is None or any(xml_value(manual, key) != value for key, value in expected.items()):
            errors.append("plot layout modes")
        elif any(xml_value(manual, key) is None or abs(float(xml_value(manual, key)) - value) > 1e-6
                 for key, value in spec["plot_layout"].items()):
            errors.append("plot layout coordinates")
    return errors
