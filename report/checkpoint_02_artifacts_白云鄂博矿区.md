# CHECKPOINT: artifacts_staged

Task: inner_mongolia_白云鄂博矿区 | Date: 2026-08-06

All artifacts written to data/tmp/inner_mongolia_白云鄂博矿区/ and each validated by process_tmp dry-run:

- build_script: data/tmp/inner_mongolia_白云鄂博矿区/build_白云鄂博矿区_data.py  [OK → scripts/build/build_白云鄂博矿区_data.py]
- database: data/tmp/inner_mongolia_白云鄂博矿区/白云鄂博矿区_network.db          [OK → data/database/白云鄂博矿区_network.db]
  - persons=14, organizations=5, positions=16, relationships=15
- gexf: data/tmp/inner_mongolia_白云鄂博矿区/白云鄂博矿区_network.gexf         [OK → data/graph/白云鄂博矿区_network.gexf]
- person_json (14): 20260806-内蒙古自治区-包头市-*.json          [OK → data/persons/]
  - core: 区委书记-邢凯, 区委副书记-区长-牛标 (both validated by json.tool)
- report: report/20260806-内蒙古自治区-包头市-白云鄂博矿区-领导班子.md   [OK → report/]

1 unrecognized file (__pycache__/pyc) was removed before apply.

Validation done: py_compile OK, build script ran to completion, DB rows correct, GEXF well-formed, person JSON parse via json.tool.