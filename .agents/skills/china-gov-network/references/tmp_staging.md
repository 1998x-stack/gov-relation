# data/tmp Staging Workflow

Use this workflow for new queue-driven investigations. It keeps the repository root and
canonical data directories clean while subagents generate intermediate files.

## Rule

Write all new artifacts to:

```text
data/tmp/<task_id>/
```

Do not write new `build_*_data.py` files directly into the repository root during research.
Do not write new `.db`, `.gexf`, person JSON, or reports directly to canonical folders until
the staged set validates.

## Accepted Staged Files

```text
data/tmp/<task_id>/build_<slug>_data.py
data/tmp/<task_id>/<slug>_network.db
data/tmp/<task_id>/<slug>_network.gexf
data/tmp/<task_id>/YYYYMMDD-{province}-{city}-{job}-{name}.json
data/tmp/<task_id>/YYYYMMDD-[地区]-[主题].md
data/tmp/<task_id>/YYYYMMDD-[地区]-[主题].html
data/tmp/<task_id>/*.log
```

## Promotion

Dry run:

```bash
python3 scripts/process_tmp.py data/tmp/<task_id>
```

Promote valid files by copying:

```bash
python3 scripts/process_tmp.py data/tmp/<task_id> --apply
```

Move instead of copy only after reviewing the dry run:

```bash
python3 scripts/process_tmp.py data/tmp/<task_id> --move
```

Overwrite existing canonical files only when intentionally replacing a prior artifact:

```bash
python3 scripts/process_tmp.py data/tmp/<task_id> --apply --overwrite
```

## Validation Performed

The processor checks:

- build scripts contain `sqlite3`, `DB_PATH`, and `GEXF_PATH`
- SQLite databases contain `persons`, `organizations`, `positions`, `relationships`
- GEXF files contain recognizable graph/nodes/edges XML
- person JSON parses and contains `identity`, `career_timeline`, `source_register`

Unrecognized files stay in `data/tmp` and are not promoted.

