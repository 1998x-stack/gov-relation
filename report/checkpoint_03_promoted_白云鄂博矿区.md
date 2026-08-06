# CHECKPOINT: promoted

Task: inner_mongolia_白云鄂博矿区 | Date: 2026-08-06

All staged artifacts were validated by dry-run and promoted with process_tmp.py --apply.

Promoted to canonical paths:
- scripts/build/build_白云鄂博矿区_data.py  (root symlink build_白云鄂博矿区_data.py created for inventory/root access)
- data/database/白云鄂博矿区_network.db  (persons=14, organizations=5, positions=16, relationships=15)
- data/graph/白云鄂博矿区_network.gexf
- data/persons/20260806-内蒙古自治区-包头市-*.json  (14 files, incl. core 邢凯 区委书记 and 牛标 区长)
- report/20260806-内蒙古自治区-包头市-白云鄂博矿区-领导班子.md
- report/checkpoint_01_research_白云鄂博矿区.md, report/checkpoint_02_artifacts_白云鄂博矿区.md

Note: checkpoint filenames were suffixed with the region (per repo convention) to avoid clobbering other tasks' generic checkpoint files in report/.

Canonical rebuild verified idempotent: python3 scripts/build/build_白云鄂博矿区_data.py re-produced identical DB/person output.