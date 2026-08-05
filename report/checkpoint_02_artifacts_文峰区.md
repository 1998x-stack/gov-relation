# CHECKPOINT:artifacts_staged

Date: 2026-08-05
Task: henan_文峰区

## Staged artifacts (in data/tmp/henan_文峰区/)
- build_文峰区_data.py (rewritten, 15 persons / 10 orgs / 27 positions / 16 relationships)
- 文峰区_network.db (regenerated)
- 文峰区_network.gexf (regenerated)
- 20260805-河南省-安阳市-区委书记-崔元锋.json
- 20260805-河南省-安阳市-代区长-关永贞.json
- 20260805-河南省-安阳市-前任区长-刘学平.json
- 20260805-文峰区-领导班子工作关系网络调查报告.md

## Persons encoded
confirmed: 崔元锋(书记), 关永贞(代区长), 刘学平(前任区长/被查)
plausible roster: 刘会敏, 郭艳芬, 李冬跃, 史红峰, 田晟强, 李卫华, 吴进善, 肖承飞, 张贤利, 王军, 汤宾鹏

## Validation plan
- py_compile build script
- run build script (regenerates db+gexf)
- python3 -m json.tool on each person json
- python3 scripts/process_tmp.py data/tmp/henan_文峰区 (dry run)

Known caveat: 多名 roster 姓名来自受限来源，标注 plausible，需正式源复核。
