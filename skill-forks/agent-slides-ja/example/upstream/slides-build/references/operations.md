# Complete Operation Reference

All operations for `slides.json` ops. Use `--docs method:render` for the live schema.

## Slide Management

| Op | Required params | Optional params |
|---|---|---|
| `add_slide` | — | `layout_index`, `layout_name`, `hidden` |
| `delete_slide` | `slide_index` | — |
| `move_slide` | `from_index`, `to_index` | — |

## Text & Content

| Op | Required params | Optional params |
|---|---|---|
| `add_text` | `slide_index`, `text`, `left`, `top`, `width`, `height` | `font_size`, `bold`, `font_name`, `font_color` |
| `add_notes` | `slide_index`, `text` | — |
| `set_semantic_text` | `slide_index`, `role`, `text` | — |
| `set_placeholder_text` | `slide_index`, `placeholder_idx`, `text` | `text_xml`, `left`, `top`, `width`, `height` |
| `set_title_subtitle` | `slide_index` | `title`, `subtitle` |
| `replace_text` | `slide_index`, `old`, `new` | — |
| `set_core_properties` | — | `title`, `subject`, `author`, `keywords` |

## Images & Media

| Op | Required params | Optional params |
|---|---|---|
| `add_image` | `slide_index`, `path`, `left`, `top` | `width`, `height` |
| `set_placeholder_image` | `slide_index`, `placeholder_idx`, `path` | crop params, position/size |
| `set_image_crop` | `slide_index`, `image_index` | crop params |
| `add_media` | `slide_index`, `path`, `left`, `top`, `width`, `height` | `mime_type`, `poster_path` |

## Shapes

| Op | Required params | Optional params |
|---|---|---|
| `add_rectangle` | `slide_index`, `left`, `top`, `width`, `height`, `fill_color` | `border_color`, `border_width` |
| `add_rounded_rectangle` | `slide_index`, `left`, `top`, `width`, `height`, `fill_color` | `corner_radius`, `border_color`, `border_width` |
| `add_oval` | `slide_index`, `left`, `top`, `width`, `height`, `fill_color` | `border_color`, `border_width` |
| `add_line_shape` | `slide_index`, `x1`, `y1`, `x2`, `y2` | `color`, `line_width` |
| `add_raw_shape_xml` | `slide_index`, `shape_xml` | `rel_images`, `rel_parts`, `rel_external` |

## Icons

| Op | Required params | Optional params |
|---|---|---|
| `add_icon` | `slide_index`, `icon_name`, `left`, `top` | `size` (default 0.75), `color` (6-digit hex) |

**Built-in icons (2):** `generic_circle`, `generic_square`. Case-insensitive partial name matching (e.g., "circle" matches "generic_circle").

**Template-extracted icons:** If `/slides-extract` found vector shapes in the template, they are in the project's `icons/` directory and available when `icon_pack_dir` is set in the design profile. Check the extraction report for the icon count and names.

## Tables

| Op | Required params | Optional params |
|---|---|---|
| `add_table` | `slide_index`, `rows`, `left`, `top`, `width`, `height` | `table_xml` |
| `update_table_cell` | `slide_index`, `table_index`, `row`, `col`, `text` | — |

## Charts — Creation

| Op | Required params | Optional params |
|---|---|---|
| `add_bar_chart` | `slide_index`, `categories`, `series`, `left`, `top`, `width`, `height` | `style`, `orientation` (`"column"` or `"bar"`, default `"column"`), `chart_space_xml` |
| `add_line_chart` | `slide_index`, `categories`, `series`, `left`, `top`, `width`, `height` | `style` |
| `add_area_chart` | `slide_index`, `categories`, `series`, `left`, `top`, `width`, `height` | `style` |
| `add_pie_chart` | `slide_index`, `categories`, `series`, `left`, `top`, `width`, `height` | `style` |
| `add_doughnut_chart` | `slide_index`, `categories`, `series`, `left`, `top`, `width`, `height` | `style` |
| `add_scatter_chart` | `slide_index`, `series`, `left`, `top`, `width`, `height` | `style` |
| `add_bubble_chart` | `slide_index`, `series`, `left`, `top`, `width`, `height` | `style` |
| `add_radar_chart` | `slide_index`, `categories`, `series`, `left`, `top`, `width`, `height` | `style` |
| `add_combo_chart_overlay` | `slide_index`, `categories`, `bar_series`, `line_series`, `left`, `top`, `width`, `height` | — |

## Charts — Styling

| Op | Required params | Optional params |
|---|---|---|
| `set_chart_title` | `slide_index`, `chart_index`, `text` | — |
| `set_chart_style` | `slide_index`, `chart_index`, `style_id` | — |
| `set_chart_legend` | `slide_index`, `chart_index` | `visible`, `position`, `include_in_layout` |
| `set_chart_data_labels` | `slide_index`, `chart_index` | `enabled`, `show_value`, `show_category_name`, `show_series_name`, `number_format` |
| `set_chart_data_labels_style` | `slide_index`, `chart_index` | `position`, `font_size`, `show_legend_key`, `number_format_is_linked` (NO `number_format` — use `set_chart_data_labels` for that) |
| `set_chart_plot_style` | `slide_index`, `chart_index` | `vary_by_categories`, `gap_width`, `overlap` |
| `set_chart_series_style` | `slide_index`, `chart_index`, `series_index` | `fill_color_hex`, `invert_if_negative` |
| `set_chart_series_line_style` | `slide_index`, `chart_index`, `series_index` | `line_color_hex`, `line_width_pt` |
| `set_chart_axis_scale` | `slide_index`, `chart_index` | `minimum`, `maximum`, `major_unit`, `show_major_gridlines`, `number_format` |
| `set_chart_axis_titles` | `slide_index`, `chart_index` | `category_title`, `value_title` |
| `set_chart_axis_options` | `slide_index`, `chart_index` | `axis`, `reverse_order`, `tick_label_position`, `visible` |
| `set_chart_secondary_axis` | `slide_index`, `chart_index` | `enable`, `series_indices` |
| `update_chart_data` | `slide_index`, `chart_index`, `categories`, `series` | — |

## Slide Appearance

| Op | Required params | Optional params |
|---|---|---|
| `set_slide_background` | `slide_index`, `color_hex` | — |
