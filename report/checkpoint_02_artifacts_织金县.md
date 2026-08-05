# Checkpoint: Artifacts Staged

**Task**: guizhou_织金县 | **Date**: 2026-08-05
**Status**: All artifacts written to data/tmp/guizhou_织金县/

- build_织金县_data.py
- 织金县_network.db (SQLite, 20 persons / 8 orgs / 27 positions / 20 relationships)
- 织金县_network.gexf (GEXF 1.3 + viz)
- 20260805-贵州省-毕节市-县委书记-杨志伟.json
- 20260805-贵州省-毕节市-县长-马丽飞.json
- 20260805-贵州省-毕节市-织金县-领导班子调查报告.md
- report/open_gaps.md appended (织金专节)

Validation: py_compile OK, DB/GEXF built OK, person JSONs valid (json.tool)
Next: process_tmp.py dry run, then --apply promote, then inventory.
