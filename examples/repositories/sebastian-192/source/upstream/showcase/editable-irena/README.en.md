# Six-slide editable IRENA sample

This Chinese presentation summarizes selected material from IRENA's *Renewable capacity statistics 2025*. Open the finished deck to edit text, move a chart, and change native table/chart data, or rebuild it from the included Scene and Page Spec inputs.

[Offline viewer](index.html) · [中文](README.md) · [Official report](https://www.irena.org/Publications/2025/Mar/Renewable-capacity-statistics-2025)

## Download and open

- [Editable PPTX](decks/editable.pptx): six slides with native text, one native table and three native charts with embedded workbooks.
- [Image PPTX](decks/image.pptx): the six approved page images.
- [Edit demonstration](demo.mp4): actual PowerPoint exports showing the before/after results of each edit.
- [Complete sample ZIP](https://github.com/helloo1568/slidemuse/raw/refs/heads/main/showcase/editable-irena/sample.zip): finished decks, source report, page images, build inputs, pinned runtime scripts and verification records.

The deck uses Microsoft YaHei. Font substitution can change wrapping and appearance. The editable version simplifies fills and uses native chart axes/ticks; it preserves the declared content but differs visually from the image version.

## Try the four independent edits

Save a copy of `editable.pptx`. Each exercise starts from the original deck.

| Exercise | Location | Expected result | Finished example |
| :--- | :--- | :--- | :--- |
| Text | Slide 6, time paragraph | Replace 解读 with 阅读 and update the explanatory note | [text-edit.pptx](decks/text-edit.pptx) |
| Move | Slide 3, native bar chart | Move +8/-4 canvas pixels; axes and labels move with the chart | [object-move.pptx](decks/object-move.pptx) |
| Table | Slide 2, 2024 capacity | Practice value 4,450,000 MW, difference 587,119 MW and growth 15.2% | [table-edit.pptx](decks/table-edit.pptx) |
| Chart | Slide 3, solar value | Practice value 460 GW, total 593 GW and solar share 77.6% | [chart-edit.pptx](decks/chart-edit.pptx) |

Click a text box or table cell to edit it. Select the chart to move it; right-click and choose **Edit Data** to open its embedded workbook.

Changed data pages visibly identify the exercise as synthetic. These values and derived results are not new IRENA statistics. A manual data edit also requires updating prose, calculations, source boundaries and speaker notes. The sample includes synchronized exercise inputs; it does not claim that PowerPoint automatically updates every paragraph.

## Rebuild all six decks

Python 3.10 or newer is required. After extracting the complete ZIP, run in the sample directory:

```sh
python -m pip install -r runtime/requirements.txt
python reproduce.py --verify
```

For a Git checkout, run from the repository root:

```sh
python -m pip install -r requirements.txt
python showcase/editable-irena/reproduce.py --verify
```

The sample's `outputs/` directory contains six decks, speaker notes and `reproduction.json`. Every native deck is checked for object structure, chart caches, embedded workbook data and declared notes.

On Windows with PowerPoint, export all 36 pages with:

```sh
python reproduce.py --verify --render --backend powerpoint
```

On Linux, install LibreOffice, Poppler and the required fonts, then use `--render --backend libreoffice`. Actual appearance depends on the renderer and fonts and needs visual inspection. Building and object checks do not require PowerPoint.

Use `--output` for a separate build directory and `--runtime` for another SlideMuse root. `--verify` checks the published hashes. Omit that option when rebuilding intentionally modified inputs in your own copy.

## Sources and verification

The included [75-page report](source/IRENA_Renewable_Capacity_Statistics_2025.pdf) remains © IRENA 2025. PDF page 2 specifies attribution and copyright-year requirements for reuse; inclusion in this MIT repository does not relicense the report. [Source metadata](source/source.json) records the official URL, hash, check date and cited PDF page numbers. The official download checked on 2026-10-06 matches the historically reviewed source.

The deck covers selected 2024 statistics and the original 2025 report-time scenario. It distinguishes capacity from generation, and stock from additions.

[Historical independent review](evidence/historical-review.md) refers to the corrected v2.10.0 `attempt-002` case. [Current verification](evidence/verification.json) identifies the public files and the current rebuild checks separately. [Manifest](manifest.json) binds the published files and previews. [Reconstruction limitations](evidence/historical-limitations.md) describes visual differences.

This is a bounded accepted case, not evidence of a general success rate. Reproduction starts from the approved images and structured inputs; it does not rerun image generation.
