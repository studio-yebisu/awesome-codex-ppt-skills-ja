# Grouped charts and linked synthetic traffic data

This is a two-page engineering fixture with synthetic vehicles/hour values. It is not an observed transport result or a formally held-out acceptance case.

From the repository root:

```sh
python scripts/update_data_bindings.py examples/data-update/data-bindings.json --check
python scripts/build_chart_image.py examples/data-update/page-spec.json examples/data-update/grouped-column.layout.json work/grouped-column.png
python scripts/build_chart_image.py examples/data-update/page-spec.json examples/data-update/grouped-bar.layout.json work/grouped-bar.png
python scripts/build_editable_ppt.py examples/data-update/scene.json work/grouped-original.pptx --page-spec examples/data-update/page-spec.json
python scripts/update_data_bindings.py examples/data-update/data-bindings.json --set '{"north_after":110}' --output-dir work/traffic-update-draft
```

The original After total is 190, North share 47.4%, and total change -5.0%. Changing `north_after` from 90 to 110 produces 210, 52.4%, and 5.0%, updating both chart series, prose and speaker notes through 26 declared bindings. The preview lists 14 actual changed targets.

The output Page Spec is a review draft with content approval invalidated. Follow `references/data-bindings.md` to review the changes under the task's authorization, rebuild and inspect; old slide images and quality evidence cannot establish the new version's correctness.

Chart images are standalone deterministic data figures. `--replace-region` is a separate operation subject to host image-edit permissions. Construction geometry is not independent visual evidence.

`job.json` demonstrates the resumable pipeline. Copy the fixture into a task directory, supply and approve its slide images, then run `python scripts/run_deck.py task/job.json task-output`. Its original image paths are pending placeholders and will correctly block delivery until prepared. See `references/pipeline.md` for actual review requirements.
