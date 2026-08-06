CHECKPOINT:artifacts_staged

# Phase 2/3 — Artifacts Staged

## Staged files (data/tmp/hubei_应城市/)
- build_应城市_data.py — canonical build script (runner.run_build API)
- 应城市_network.db — SQLite, 4 tables (19 persons, 10 orgs, 21 positions, 19 relationships)
- 应城市_network.gexf — GEXF graph (persons colored by role + org nodes + person/org + person/person edges)
- 19× data/persons JSON (YYYYMMDD-湖北省-孝感市-{job}-{name}.json)

## Validation so far (staging)
- py_compile: OK
- script execution: OK (DB+GEXF+person JSON generated)
- json.tool: 19/19 person JSON valid
- GEXF XML well-formed: OK
