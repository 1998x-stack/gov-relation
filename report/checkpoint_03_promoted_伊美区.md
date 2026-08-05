# CHECKPOINT: promoted — 伊美区 (2026-08-05)

`scripts/process_tmp.py data/tmp/heilongjiang_伊美区 --apply` applied cleanly.
Canonical destinations verified present:

- scripts/build/build_伊美区_data.py  (+ root build_伊美区_data.py copy per task canonical list)
- data/database/伊美区_network.db
- data/graph/伊美区_network.gexf
- data/persons/20260805-黑龙江省-伊春市-区委书记-张正强.json
- data/persons/20260805-黑龙江省-伊春市-区长-张斐.json
- data/persons/20260805-黑龙江省-伊春市-区委副书记-迟鑫.json
- report/20260805-黑龙江省-伊春市-伊美区-调研报告.md
- report/open_gaps.md  (伊美区 section appended)

Validation before apply: py_compile OK, DB 4 tables OK, GEXF nodes/edges OK, all person JSONs valid via json.tool, process_tmp dry-run clean (no SKIP).