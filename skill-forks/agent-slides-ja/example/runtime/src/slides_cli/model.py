from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

NullableNumber = float | None


class AddSlideOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_slide"]
    layout_index: int | None = None
    layout_name: str | None = None
    hidden: bool = False


class AddTextOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_text"]
    slide_index: int
    text: str
    left: float
    top: float
    width: float
    height: float
    font_size: int = 20
    bold: bool = False
    font_name: str | None = None
    font_color: str | None = None


class AddBarChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_bar_chart"]
    slide_index: int
    categories: list[str]
    series: list[tuple[str, list[NullableNumber]]]
    style: Literal["clustered", "stacked", "percent_stacked"] = "clustered"
    orientation: Literal["column", "bar"] = "column"
    chart_space_xml: str | None = None
    left: float
    top: float
    width: float
    height: float


class AddLineChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_line_chart"]
    slide_index: int
    categories: list[str]
    series: list[tuple[str, list[NullableNumber]]]
    style: Literal[
        "line",
        "line_markers",
        "stacked",
        "stacked_markers",
        "percent_stacked",
        "percent_stacked_markers",
    ] = "line"
    left: float
    top: float
    width: float
    height: float


class AddPieChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_pie_chart"]
    slide_index: int
    categories: list[str]
    series: list[tuple[str, list[NullableNumber]]]
    style: Literal["pie", "exploded", "pie_of_pie", "bar_of_pie"] = "pie"
    left: float
    top: float
    width: float
    height: float


class AddAreaChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_area_chart"]
    slide_index: int
    categories: list[str]
    series: list[tuple[str, list[NullableNumber]]]
    style: Literal["area", "stacked", "percent_stacked"] = "area"
    left: float
    top: float
    width: float
    height: float


class AddDoughnutChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_doughnut_chart"]
    slide_index: int
    categories: list[str]
    series: list[tuple[str, list[NullableNumber]]]
    style: Literal["doughnut", "exploded"] = "doughnut"
    left: float
    top: float
    width: float
    height: float


class AddScatterChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_scatter_chart"]
    slide_index: int
    series: list[tuple[str, list[tuple[float, float]]]]
    style: Literal["markers", "line", "line_no_markers", "smooth", "smooth_no_markers"] = "markers"
    left: float
    top: float
    width: float
    height: float


class AddRadarChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_radar_chart"]
    slide_index: int
    categories: list[str]
    series: list[tuple[str, list[NullableNumber]]]
    style: Literal["radar", "filled", "markers"] = "radar"
    left: float
    top: float
    width: float
    height: float


class AddBubbleChartOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_bubble_chart"]
    slide_index: int
    series: list[tuple[str, list[tuple[float, float, float]]]]
    style: Literal["bubble", "bubble_3d"] = "bubble"
    left: float
    top: float
    width: float
    height: float


class AddComboChartOverlayOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_combo_chart_overlay"]
    slide_index: int
    categories: list[str]
    bar_series: list[tuple[str, list[NullableNumber]]]
    line_series: list[tuple[str, list[NullableNumber]]]
    left: float
    top: float
    width: float
    height: float


class AddImageOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_image"]
    slide_index: int
    path: str
    left: float
    top: float
    width: float | None = None
    height: float | None = None


class AddTableOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_table"]
    slide_index: int
    rows: list[list[str]]
    left: float
    top: float
    width: float
    height: float
    table_xml: str | None = None
    font_size: int | None = None


class AddRectangleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_rectangle"]
    slide_index: int
    left: float
    top: float
    width: float
    height: float
    fill_color: str
    border_color: str | None = None
    border_width: float | None = None


class AddRoundedRectangleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_rounded_rectangle"]
    slide_index: int
    left: float
    top: float
    width: float
    height: float
    fill_color: str
    corner_radius: int = 5000
    border_color: str | None = None
    border_width: float | None = None


class AddOvalOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_oval"]
    slide_index: int
    left: float
    top: float
    width: float
    height: float
    fill_color: str
    border_color: str | None = None
    border_width: float | None = None


class AddLineShapeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_line_shape"]
    slide_index: int
    x1: float
    y1: float
    x2: float
    y2: float
    color: str = "000000"
    line_width: float = 1.0


class AddRawShapeXmlOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_raw_shape_xml"]
    slide_index: int
    shape_xml: str
    rel_images: list[tuple[str, str]] = Field(default_factory=list)
    rel_parts: list[tuple[str, str, str, str, str]] = Field(default_factory=list)
    rel_external: list[tuple[str, str, str]] = Field(default_factory=list)


class AddIconOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_icon"]
    slide_index: int
    icon_name: str
    left: float
    top: float
    size: float = 0.75
    color: str | None = None


class ReplaceTextOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["replace_text"]
    slide_index: int
    old: str
    new: str


class DeleteSlideOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["delete_slide"]
    slide_index: int


class MoveSlideOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["move_slide"]
    from_index: int
    to_index: int


class AddNotesOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_notes"]
    slide_index: int
    text: str


class AddMediaOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_media"]
    slide_index: int
    path: str
    left: float
    top: float
    width: float
    height: float
    mime_type: str = "video/unknown"
    poster_path: str | None = None


class SetCorePropertiesOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_core_properties"]
    title: str | None = None
    subject: str | None = None
    author: str | None = None
    keywords: str | None = None


class UpdateTableCellOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["update_table_cell"]
    slide_index: int
    table_index: int
    row: int
    col: int
    text: str
    font_size: int | None = None


class UpdateChartDataOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["update_chart_data"]
    slide_index: int
    chart_index: int
    categories: list[str]
    series: list[tuple[str, list[NullableNumber]]]


class SetSlideBackgroundOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_slide_background"]
    slide_index: int
    color_hex: str


class SetPlaceholderTextOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_placeholder_text"]
    slide_index: int
    placeholder_idx: int
    text: str
    text_xml: str | None = None
    left: float | None = None
    top: float | None = None
    width: float | None = None
    height: float | None = None


class SetPlaceholderImageOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_placeholder_image"]
    slide_index: int
    placeholder_idx: int
    path: str
    crop_left: float | None = None
    crop_right: float | None = None
    crop_top: float | None = None
    crop_bottom: float | None = None
    left: float | None = None
    top: float | None = None
    width: float | None = None
    height: float | None = None


class SetTitleSubtitleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_title_subtitle"]
    slide_index: int
    title: str | None = None
    subtitle: str | None = None


class SetSemanticTextOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_semantic_text"]
    slide_index: int
    role: Literal["title", "subtitle", "body", "footer", "date", "slide_number"]
    text: str


class SetChartLegendOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_legend"]
    slide_index: int
    chart_index: int
    visible: bool = True
    position: Literal["right", "left", "top", "bottom", "corner"] = "right"
    include_in_layout: bool | None = None
    font_size: int | None = None


class SetChartStyleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_style"]
    slide_index: int
    chart_index: int
    style_id: int


class SetImageCropOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_image_crop"]
    slide_index: int
    image_index: int
    crop_left: float | None = None
    crop_right: float | None = None
    crop_top: float | None = None
    crop_bottom: float | None = None


class SetChartTitleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_title"]
    slide_index: int
    chart_index: int
    text: str


class SetChartAxisTitlesOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_axis_titles"]
    slide_index: int
    chart_index: int
    category_title: str | None = None
    value_title: str | None = None


class SetChartAxisOptionsOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_axis_options"]
    slide_index: int
    chart_index: int
    axis: Literal["category", "value"] = "value"
    reverse_order: bool | None = None
    major_tick_mark: Literal["none", "inside", "outside", "cross"] | None = None
    minor_tick_mark: Literal["none", "inside", "outside", "cross"] | None = None
    tick_label_position: Literal["none", "low", "high", "next_to_axis"] | None = None
    visible: bool | None = None
    crosses: Literal["automatic", "minimum", "maximum"] | None = None
    crosses_at: float | None = None
    font_size: int | None = None


class SetChartDataLabelsOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_data_labels"]
    slide_index: int
    chart_index: int
    enabled: bool = True
    show_value: bool | None = None
    show_category_name: bool | None = None
    show_series_name: bool | None = None
    number_format: str | None = None


class SetChartDataLabelsStyleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_data_labels_style"]
    slide_index: int
    chart_index: int
    position: (
        Literal[
            "best_fit",
            "center",
            "inside_base",
            "inside_end",
            "outside_end",
            "left",
            "right",
            "above",
            "below",
        ]
        | None
    ) = None
    show_legend_key: bool | None = None
    number_format_is_linked: bool | None = None
    font_size: int | None = None


class SetChartAxisScaleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_axis_scale"]
    slide_index: int
    chart_index: int
    minimum: float | None = None
    maximum: float | None = None
    major_unit: float | None = None
    minor_unit: float | None = None
    show_major_gridlines: bool | None = None
    show_minor_gridlines: bool | None = None
    number_format: str | None = None


class SetChartPlotStyleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_plot_style"]
    slide_index: int
    chart_index: int
    vary_by_categories: bool | None = None
    gap_width: int | None = None
    overlap: int | None = None
    plot_area_x: float | None = None
    plot_area_y: float | None = None
    plot_area_w: float | None = None
    plot_area_h: float | None = None


class SetChartSeriesStyleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_series_style"]
    slide_index: int
    chart_index: int
    series_index: int
    fill_color_hex: str | None = None
    invert_if_negative: bool | None = None


class SetChartSeriesLineStyleOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_series_line_style"]
    slide_index: int
    chart_index: int
    series_index: int
    line_color_hex: str | None = None
    line_width_pt: float | None = None


class SetChartSecondaryAxisOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_secondary_axis"]
    slide_index: int
    chart_index: int
    enable: bool = True
    series_indices: list[int] | None = None


class SetLineSeriesMarkerOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_line_series_marker"]
    slide_index: int
    chart_index: int
    series_index: int
    style: Literal[
        "auto",
        "none",
        "circle",
        "dash",
        "diamond",
        "dot",
        "plus",
        "square",
        "star",
        "triangle",
        "x",
    ] = "circle"
    size: int | None = None


class SetLineSeriesSmoothOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_line_series_smooth"]
    slide_index: int
    chart_index: int
    series_index: int
    smooth: bool = True


class SetChartSeriesTrendlineOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_series_trendline"]
    slide_index: int
    chart_index: int
    series_index: int
    trend_type: Literal["linear", "exp", "log", "movingAvg", "poly", "power"] = "linear"


class SetChartSeriesErrorBarsOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_series_error_bars"]
    slide_index: int
    chart_index: int
    series_index: int
    value: float
    direction: Literal["x", "y"] = "y"
    bar_type: Literal["both", "plus", "minus"] = "both"


class SetChartComboSecondaryMappingOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["set_chart_combo_secondary_mapping"]
    slide_index: int
    chart_index: int
    series_indices: list[int]


Operation = (
    AddSlideOp
    | AddTextOp
    | AddBarChartOp
    | AddLineChartOp
    | AddPieChartOp
    | AddAreaChartOp
    | AddDoughnutChartOp
    | AddScatterChartOp
    | AddRadarChartOp
    | AddBubbleChartOp
    | AddComboChartOverlayOp
    | AddImageOp
    | AddTableOp
    | AddRectangleOp
    | AddRoundedRectangleOp
    | AddOvalOp
    | AddLineShapeOp
    | AddRawShapeXmlOp
    | AddIconOp
    | ReplaceTextOp
    | DeleteSlideOp
    | MoveSlideOp
    | AddNotesOp
    | AddMediaOp
    | SetCorePropertiesOp
    | UpdateTableCellOp
    | UpdateChartDataOp
    | SetSlideBackgroundOp
    | SetPlaceholderTextOp
    | SetPlaceholderImageOp
    | SetTitleSubtitleOp
    | SetSemanticTextOp
    | SetChartLegendOp
    | SetChartStyleOp
    | SetImageCropOp
    | SetChartTitleOp
    | SetChartAxisTitlesOp
    | SetChartAxisOptionsOp
    | SetChartDataLabelsOp
    | SetChartDataLabelsStyleOp
    | SetChartAxisScaleOp
    | SetChartPlotStyleOp
    | SetChartSeriesStyleOp
    | SetChartSeriesLineStyleOp
    | SetChartSecondaryAxisOp
    | SetLineSeriesMarkerOp
    | SetLineSeriesSmoothOp
    | SetChartSeriesTrendlineOp
    | SetChartSeriesErrorBarsOp
    | SetChartComboSecondaryMappingOp
)


class OperationBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operations: list[Annotated[Operation, Field(discriminator="op")]] = Field(default_factory=list)


class OperationEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int
    op: str
    status: Literal["planned", "applied", "failed"]
    detail: str | None = None
    duration_ms: int | None = None


class OperationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: bool
    dry_run: bool
    events: list[OperationEvent]
    applied_count: int = 0
    failed_index: int | None = None
