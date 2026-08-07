CHECKPOINT:artifacts_staged
task_id: qinghai_贵南县

Artifacts staged in data/tmp/qinghai_贵南县/:
- build_贵南县_data.py  (runs clean, produced DB + GEXF)
- 贵南县_network.db  (6 persons, 11 orgs, 14 positions, 6 relationships)
- 贵南县_network.gexf  (valid XML, nodes+edges+viz)
- 20260807-青海省-海南藏族自治州-县委书记-薛顺云.json
- 20260807-青海省-海南藏族自治州-县长-卓玛本.json
- 20260807-青海省-海南藏族自治州-贵南县-领导班子报告.md
- checkpoint_01_research.md

Validation status: py_compile OK, build script run OK, json.tool OK on both person JSONs.
Next: process_tmp.py dry run, then --apply promotion.