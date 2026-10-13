# Publication evidence

Date: 2026-07-26

## GitHub

- Repository: https://github.com/joeseesun/qiaomu-bento-ppt
- Visibility: public
- Default branch: `main`
- Initial release commit: `01da128b3631c4d6e102480e687753b203a6fea2`
- Bundled shell present remotely: 598,314 bytes

## npx skills discovery

Command:

```bash
npx skills add joeseesun/qiaomu-bento-ppt --list
```

Evidence:

- Repository cloned successfully.
- `Found 1 skill`.
- `qiaomu-bento-ppt` appeared in the available skill list.

## Clean remote install

Command:

```bash
npx skills add joeseesun/qiaomu-bento-ppt \
  --skill qiaomu-bento-ppt -y --agent universal
```

Evidence:

- Installation completed into a fresh temporary universal-agent directory.
- Installed copy reported `"standalone": true`.
- Installed copy contained the pinned shell and all three upstream references.
- Installed copy ran `evals/output/run_fixture.py` without `BENTO_REPO` or
  `BENTO_SHELL`.
- All new-document, edit, identity, rollback, structure and internal shell-gate
  checks passed.

## Remaining missing evidence

- Cross-platform browser visual review.

## Upstream maintenance update — 2026-07-27

- Pinned official release moved from `v1.0.9` to `v1.0.10`.
- Shell and documentation provenance are machine-locked in
  `upstream.lock.json`.
- A daily workflow checks official releases and opens a review PR only; it
  cannot merge or push directly to `main`.
- Upstream refresh/no-op/rejection/rollback fixture: pass.
- Regenerated example: internal gate and the upstream checkout's old-updater
  splice gate both pass.
- Refreshed shell browser review: editor, presentation and state interaction
  pass with zero console warnings/errors.
