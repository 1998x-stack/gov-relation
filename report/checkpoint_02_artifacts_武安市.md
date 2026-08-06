# CHECKPOINT:artifacts_staged

Artifacts staged under data/tmp/hebei_武安市/ :

- build_武安市_data.py        (py_compile OK)
- 武安市_network.db           (persons 11, organizations 6, positions 14, relationships 10; all 4 tables present)
- 武安市_network.gexf         (well-formed XML, nodes+edges present)
- 20260806-武安市-领导班子工作关系网络调查报告.md
- 20260806-武安市-领导班子工作关系网络-情报简报.html
- 20260806-河北省-邯郸市-{职务}-{姓名}.json  × 11  (all validate via json.tool)
  - 董志毅(书记), 李同强(市长), 马晓斌, 尹建东, 连希梅, 王增平, 温金良, 胡存喜, 巩奎永, 李广奇, 武建生
- checkpoint files

Next: run scripts/process_tmp.py dry run → promote with --apply → inventory → verify canonical paths.