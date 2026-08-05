# CHECKPOINT:artifacts_staged

Artifacts written to staging dir `data/tmp/heilongjiang_桦南县/`:
- [x] build_桦南县_data.py  (build script, run_build pattern, 16 persons / 9 orgs / 17 positions / 12 relationships)
- [x] 桦南县_network.db       (SQLite: persons, organizations, positions, relationships — verified)
- [x] 桦南县_network.gexf     (GEXF graph — verified)
- [x] 20260805-黑龙江省-佳木斯市-县委书记-徐永刚.json (json.tool OK)
- [x] 20260805-黑龙江省-佳木斯市-县长-程显峰.json (json.tool OK)
- [x] 20260805-黑龙江省-佳木斯市-桦南县调查报告.md
- [x] open_gaps.md

Validation:
- py_compile: OK
- build run into GOV_REL_DATABASE_DIR=<staging>: OK (DB tables + 2 person JSON written)
- json.tool (both core person JSON): OK
- scripts/process_tmp.py dry run: all valid (1 skip = __pycache__/.pyc, unrecognized — not required)

Research basis: official 桦南县人民政府 领导之窗 (www.huanan.gov.cn) — current roster + individual bio pages,
accessed 2026-08-05 via direct curl (TLS -k). All current role & identity claims = confirmed.
Predecessor / cross-county rotation = open_gaps (external search engines blocked in this env).