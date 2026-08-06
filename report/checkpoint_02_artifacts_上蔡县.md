# CHECKPOINT 02 — ARTIFACTS STAGED

task_id: henan_上蔡县 | date: 2026-08-06

## Staged in data/tmp/henan_上蔡县/
- build_上蔡县_data.py  (新的规范构建脚本, 使用 gov_relation.runner.run_build)
- 上蔡县_network.db (persons=9, organizations=5, positions=14, relationships=9)
- 上蔡县_network.gexf (nodes=14, edges=9, viz namespace OK)
- 2026-08-06-河南省-驻马店市-县委书记-李超.json
- 2026-08-06-河南省-驻马店市-县长-李慧阳.json
- report/2026-08-06-河南省-驻马店市-上蔡县-领导班子工作关系网络调查报告.md
- checkpoint_01_research.md

## 扩散
- report/open_gaps.md 已在本仓 canonical 位置追加"上蔡县"缺口区段（Critical: 李超/李慧阳 履历；High: 前任书记/县长、李超任书记起始、县委其他常委分工）。

## 待办 (validation)
1. py_compile build script
2. run build script (产出 DB/GEXF/双 JSON)
3. json.tool 校验两个 person JSON
4. scripts/process_tmp.py dry-run
5. 通过后 --apply 提升