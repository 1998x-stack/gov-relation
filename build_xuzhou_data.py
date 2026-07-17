#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 徐州市 (Xuzhou City) leadership network.

Covers: City-level leadership (市委书记, 市长, 人大主任, 政协主席, etc.),
10 districts/counties (区委书记 + 区长/县长/市长), predecessors,
and the city-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/xuzhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/xuzhou_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委 ──
    # 1. 宋乐伟 — 徐州市委书记
    {"id":1,"name":"宋乐伟","gender":"男","ethnicity":"汉族","birth":"1969-10","birthplace":"山东潍坊","education":"","party_join":"","work_start":"","current_post":"徐州市委书记","current_org":"中共徐州市委员会","source":""},
    # 2. 沈峻峰 — 徐州市长
    {"id":2,"name":"沈峻峰","gender":"男","ethnicity":"汉族","birth":"1970-03","birthplace":"江苏如皋","education":"","party_join":"","work_start":"","current_post":"徐州市长","current_org":"徐州市人民政府","source":""},
    # 3. 王安顺 — 徐州市人大常委会主任
    {"id":3,"name":"王安顺","gender":"男","ethnicity":"汉族","birth":"1964-04","birthplace":"安徽淮北","education":"","party_join":"","work_start":"","current_post":"徐州市人大常委会主任","current_org":"徐州市人大常委会","source":""},
    # 4. 韩冬梅 — 徐州市政协主席
    {"id":4,"name":"韩冬梅","gender":"女","ethnicity":"汉族","birth":"1966-10","birthplace":"江苏新沂","education":"","party_join":"","work_start":"","current_post":"徐州市政协主席","current_org":"政协徐州市委员会","source":""},

    # 5. 王剑锋 — 前徐州市长 (2021-2025)
    {"id":5,"name":"王剑锋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"前徐州市长","current_org":"徐州市人民政府","source":""},
    # 6. 庄兆林 — 前徐州书记→江西省委宣传部长
    {"id":6,"name":"庄兆林","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"江西省委宣传部长","current_org":"中共江西省委","source":""},
    # 7. 周铁根 — 前徐州书记→退休/省人大
    {"id":7,"name":"周铁根","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"前徐州市委书记（退休/省人大）","current_org":"中共徐州市委员会","source":""},
    # 8. 张国华 — 前徐州书记→河北雄安
    {"id":8,"name":"张国华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"河北雄安（前徐州书记）","current_org":"河北雄安新区","source":""},

    # ── District/County leadership ──
    # 9. 龚维芳 — 铜山区委书记 (女)
    {"id":9,"name":"龚维芳","gender":"女","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"铜山区委书记","current_org":"中共铜山区委员会","source":""},
    # 10. 王维峰 — 丰县县委书记 (2022.02任)
    {"id":10,"name":"王维峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"丰县县委书记","current_org":"中共丰县委员会","source":""},
    # 11. 高建民 — 睢宁县委书记
    {"id":11,"name":"高建民","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"睢宁县委书记","current_org":"中共睢宁县委员会","source":""},
    # 12. 王伟 — 邳州市委书记
    {"id":12,"name":"王伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"邳州市委书记","current_org":"中共邳州市委员会","source":""},

    # ── 10 Districts/Counties — placeholder members for missing data ──
    # 鼓楼区
    {"id":13,"name":"鼓楼区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"鼓楼区委书记","current_org":"中共鼓楼区委员会","source":""},
    {"id":14,"name":"鼓楼区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"鼓楼区长","current_org":"鼓楼区人民政府","source":""},

    # 云龙区
    {"id":15,"name":"云龙区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"云龙区委书记","current_org":"中共云龙区委员会","source":""},
    {"id":16,"name":"云龙区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"云龙区长","current_org":"云龙区人民政府","source":""},

    # 贾汪区
    {"id":17,"name":"贾汪区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"贾汪区委书记","current_org":"中共贾汪区委员会","source":""},
    {"id":18,"name":"贾汪区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"贾汪区长","current_org":"贾汪区人民政府","source":""},

    # 泉山区
    {"id":19,"name":"泉山区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"泉山区委书记","current_org":"中共泉山区委员会","source":""},
    {"id":20,"name":"泉山区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"泉山区长","current_org":"泉山区人民政府","source":""},

    # 铜山区长 (placeholder)
    {"id":21,"name":"铜山区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"铜山区长","current_org":"铜山区人民政府","source":""},

    # 丰县县长
    {"id":22,"name":"丰县县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"丰县县长","current_org":"丰县人民政府","source":""},

    # 沛县
    {"id":23,"name":"沛县县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"沛县县委书记","current_org":"中共沛县委员会","source":""},
    {"id":24,"name":"沛县县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"沛县县长","current_org":"沛县人民政府","source":""},

    # 睢宁县县长
    {"id":25,"name":"睢宁县县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"睢宁县县长","current_org":"睢宁县人民政府","source":""},

    # 新沂市
    {"id":26,"name":"新沂市委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"新沂市委书记","current_org":"中共新沂市委员会","source":""},
    {"id":27,"name":"新沂市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"新沂市长","current_org":"新沂市人民政府","source":""},

    # 邳州市长
    {"id":28,"name":"邳州市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"邳州市长","current_org":"邳州市人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Xuzhou city-level core ──
    {"id":1,"name":"中共徐州市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省徐州市"},
    {"id":2,"name":"徐州市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省徐州市"},
    {"id":3,"name":"徐州市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省徐州市"},
    {"id":4,"name":"政协徐州市委员会","type":"政协","level":"地级","parent":"","location":"江苏省徐州市"},
    {"id":5,"name":"中共徐州市纪律检查委员会","type":"党委","level":"地级","parent":"中共徐州市委员会","location":"江苏省徐州市"},

    # ── 5 Districts — Party committees ──
    {"id":6,"name":"中共鼓楼区委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市鼓楼区"},
    {"id":7,"name":"中共云龙区委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市云龙区"},
    {"id":8,"name":"中共贾汪区委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市贾汪区"},
    {"id":9,"name":"中共泉山区委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市泉山区"},
    {"id":10,"name":"中共铜山区委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市铜山区"},

    # ── 3 Counties — Party committees ──
    {"id":11,"name":"中共丰县委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市丰县"},
    {"id":12,"name":"中共沛县委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市沛县"},
    {"id":13,"name":"中共睢宁县委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市睢宁县"},

    # ── 2 County-level cities — Party committees ──
    {"id":14,"name":"中共新沂市委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市新沂市"},
    {"id":15,"name":"中共邳州市委员会","type":"党委","level":"县级","parent":"中共徐州市委员会","location":"江苏省徐州市邳州市"},

    # ── 5 Districts — Governments ──
    {"id":16,"name":"鼓楼区人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市鼓楼区"},
    {"id":17,"name":"云龙区人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市云龙区"},
    {"id":18,"name":"贾汪区人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市贾汪区"},
    {"id":19,"name":"泉山区人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市泉山区"},
    {"id":20,"name":"铜山区人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市铜山区"},

    # ── 3 Counties — Governments ──
    {"id":21,"name":"丰县人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市丰县"},
    {"id":22,"name":"沛县人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市沛县"},
    {"id":23,"name":"睢宁县人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市睢宁县"},

    # ── 2 County-level cities — Governments ──
    {"id":24,"name":"新沂市人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市新沂市"},
    {"id":25,"name":"邳州市人民政府","type":"政府","level":"县级","parent":"徐州市人民政府","location":"江苏省徐州市邳州市"},

    # ── External / other orgs needed ──
    {"id":26,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":27,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":28,"name":"中共江西省委","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":29,"name":"河北省雄安新区","type":"政府","level":"省级","parent":"","location":"河北省雄安新区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 宋乐伟 ──
    {"id":1,"person_id":1,"org_id":1,"title":"徐州市委书记","start":"2022-05","end":"","rank":"副部级","note":"2022.05到任，前省应急管理厅长"},
    {"id":2,"person_id":1,"org_id":1,"title":"徐州市委副书记","start":"2022-03","end":"2022-05","rank":"副部级","note":"先任副书记后任书记"},

    # ── 沈峻峰 ──
    {"id":3,"person_id":2,"org_id":2,"title":"徐州市长","start":"2025-06","end":"","rank":"副部级","note":"2025.06到任，前省纪委副书记"},
    {"id":4,"person_id":2,"org_id":1,"title":"徐州市委副书记","start":"2025-06","end":"","rank":"副部级","note":""},

    # ── 王安顺 ──
    {"id":5,"person_id":3,"org_id":3,"title":"徐州市人大常委会主任","start":"","end":"","rank":"正厅级","note":""},

    # ── 韩冬梅 ──
    {"id":6,"person_id":4,"org_id":4,"title":"徐州市政协主席","start":"","end":"","rank":"正厅级","note":""},

    # ── 王剑锋 ──
    {"id":7,"person_id":5,"org_id":2,"title":"徐州市长","start":"2021","end":"2025","rank":"副部级","note":"2021-2025任徐州市长，去向待查"},

    # ── 庄兆林 ──
    {"id":8,"person_id":6,"org_id":1,"title":"徐州市委书记","start":"","end":"","rank":"副部级","note":"前徐州书记，现任江西省委宣传部长"},
    {"id":9,"person_id":6,"org_id":28,"title":"江西省委宣传部长","start":"","end":"","rank":"副部级","note":""},

    # ── 周铁根 ──
    {"id":10,"person_id":7,"org_id":1,"title":"徐州市委书记","start":"","end":"","rank":"副部级","note":"前徐州书记，已退休/省人大"},

    # ── 张国华 ──
    {"id":11,"person_id":8,"org_id":1,"title":"徐州市委书记","start":"","end":"","rank":"副部级","note":"前徐州书记，现任河北雄安"},
    {"id":12,"person_id":8,"org_id":29,"title":"河北雄安","start":"","end":"","rank":"副部级","note":""},

    # ── 龚维芳（铜山区委书记）──
    {"id":13,"person_id":9,"org_id":10,"title":"铜山区委书记","start":"","end":"","rank":"正厅级","note":"女"},

    # ── 王维峰（丰县县委书记）──
    {"id":14,"person_id":10,"org_id":11,"title":"丰县县委书记","start":"2022-02","end":"","rank":"正厅级","note":"2022.02任，接替被免职的娄海"},

    # ── 高建民（睢宁县委书记）──
    {"id":15,"person_id":11,"org_id":13,"title":"睢宁县委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 王伟（邳州市委书记）──
    {"id":16,"person_id":12,"org_id":15,"title":"邳州市委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 鼓楼区（placeholder）──
    {"id":17,"person_id":13,"org_id":6,"title":"鼓楼区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":18,"person_id":14,"org_id":16,"title":"鼓楼区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 云龙区（placeholder）──
    {"id":19,"person_id":15,"org_id":7,"title":"云龙区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":20,"person_id":16,"org_id":17,"title":"云龙区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 贾汪区（placeholder）──
    {"id":21,"person_id":17,"org_id":8,"title":"贾汪区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":22,"person_id":18,"org_id":18,"title":"贾汪区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 泉山区（placeholder）──
    {"id":23,"person_id":19,"org_id":9,"title":"泉山区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":24,"person_id":20,"org_id":19,"title":"泉山区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 铜山区长（placeholder）──
    {"id":25,"person_id":21,"org_id":20,"title":"铜山区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 丰县县长（placeholder）──
    {"id":26,"person_id":22,"org_id":21,"title":"丰县县长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 沛县（placeholder）──
    {"id":27,"person_id":23,"org_id":12,"title":"沛县县委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":28,"person_id":24,"org_id":22,"title":"沛县县长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 睢宁县县长（placeholder）──
    {"id":29,"person_id":25,"org_id":23,"title":"睢宁县县长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 新沂市（placeholder）──
    {"id":30,"person_id":26,"org_id":14,"title":"新沂市委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":31,"person_id":27,"org_id":24,"title":"新沂市长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 邳州市长（placeholder）──
    {"id":32,"person_id":28,"org_id":25,"title":"邳州市长","start":"","end":"","rank":"正厅级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 宋乐伟 ↔ 沈峻峰（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"宋乐伟（徐州市委书记）与沈峻峰（市长）为徐州市党政一把手搭档","overlap_org":"徐州市","overlap_period":"2025-06至今"},

    # ── 王剑锋→沈峻峰（前后任市长）──
    {"id":2,"person_a":5,"person_b":2,"type":"前后任","context":"王剑锋（2021-2025徐州市长）→ 沈峻峰（2025.06接任市长）","overlap_org":"徐州市人民政府","overlap_period":"不重叠（前后任）"},

    # ── 庄兆林→宋乐伟（前后任书记）──
    {"id":3,"person_a":6,"person_b":1,"type":"前后任","context":"庄兆林（前徐州书记）→ 宋乐伟（2022.05接任书记）","overlap_org":"中共徐州市委员会","overlap_period":"不重叠（前后任）"},

    # ── 周铁根→庄兆林（前后任书记）──
    {"id":4,"person_a":7,"person_b":6,"type":"前后任","context":"周铁根（前徐州书记）→ 庄兆林（接任书记后调江西）","overlap_org":"中共徐州市委员会","overlap_period":"不重叠（前后任）"},

    # ── 张国华→周铁根（前后任书记）──
    {"id":5,"person_a":8,"person_b":7,"type":"前后任","context":"张国华（前徐州书记→河北雄安）→ 周铁根（接任书记）","overlap_org":"中共徐州市委员会","overlap_period":"不重叠（前后任）"},

    # ── 各区委书记↔区长/县长/市长（党政搭档）──
    {"id":6,"person_a":13,"person_b":14,"type":"党政搭档","context":"鼓楼区委书记与鼓楼区长党政搭档","overlap_org":"鼓楼区","overlap_period":""},
    {"id":7,"person_a":15,"person_b":16,"type":"党政搭档","context":"云龙区委书记与云龙区长党政搭档","overlap_org":"云龙区","overlap_period":""},
    {"id":8,"person_a":17,"person_b":18,"type":"党政搭档","context":"贾汪区委书记与贾汪区长党政搭档","overlap_org":"贾汪区","overlap_period":""},
    {"id":9,"person_a":19,"person_b":20,"type":"党政搭档","context":"泉山区委书记与泉山区长党政搭档","overlap_org":"泉山区","overlap_period":""},
    {"id":10,"person_a":9,"person_b":21,"type":"党政搭档","context":"龚维芳（铜山区委书记）与铜山区长党政搭档","overlap_org":"铜山区","overlap_period":""},
    {"id":11,"person_a":10,"person_b":22,"type":"党政搭档","context":"王维峰（丰县县委书记）与丰县县长党政搭档","overlap_org":"丰县","overlap_period":""},
    {"id":12,"person_a":23,"person_b":24,"type":"党政搭档","context":"沛县县委书记与沛县县长党政搭档","overlap_org":"沛县","overlap_period":""},
    {"id":13,"person_a":11,"person_b":25,"type":"党政搭档","context":"高建民（睢宁县委书记）与睢宁县县长党政搭档","overlap_org":"睢宁县","overlap_period":""},
    {"id":14,"person_a":26,"person_b":27,"type":"党政搭档","context":"新沂市委书记与新沂市长党政搭档","overlap_org":"新沂市","overlap_period":""},
    {"id":15,"person_a":12,"person_b":28,"type":"党政搭档","context":"王伟（邳州市委书记）与邳州市长党政搭档","overlap_org":"邳州市","overlap_period":""},

    # ── 市区联系：各区委/县委书记向市委书记汇报 ──
    {"id":16,"person_a":1,"person_b":13,"type":"隶属关系","context":"宋乐伟（市委书记）领导鼓楼区委书记","overlap_org":"徐州市","overlap_period":""},
    {"id":17,"person_a":1,"person_b":15,"type":"隶属关系","context":"宋乐伟（市委书记）领导云龙区委书记","overlap_org":"徐州市","overlap_period":""},
    {"id":18,"person_a":1,"person_b":17,"type":"隶属关系","context":"宋乐伟（市委书记）领导贾汪区委书记","overlap_org":"徐州市","overlap_period":""},
    {"id":19,"person_a":1,"person_b":19,"type":"隶属关系","context":"宋乐伟（市委书记）领导泉山区委书记","overlap_org":"徐州市","overlap_period":""},
    {"id":20,"person_a":1,"person_b":9,"type":"隶属关系","context":"宋乐伟（市委书记）领导龚维芳（铜山区委书记）","overlap_org":"徐州市","overlap_period":""},
    {"id":21,"person_a":1,"person_b":10,"type":"隶属关系","context":"宋乐伟（市委书记）领导王维峰（丰县县委书记）","overlap_org":"徐州市","overlap_period":""},
    {"id":22,"person_a":1,"person_b":23,"type":"隶属关系","context":"宋乐伟（市委书记）领导沛县县委书记","overlap_org":"徐州市","overlap_period":""},
    {"id":23,"person_a":1,"person_b":11,"type":"隶属关系","context":"宋乐伟（市委书记）领导高建民（睢宁县委书记）","overlap_org":"徐州市","overlap_period":""},
    {"id":24,"person_a":1,"person_b":26,"type":"隶属关系","context":"宋乐伟（市委书记）领导新沂市委书记","overlap_org":"徐州市","overlap_period":""},
    {"id":25,"person_a":1,"person_b":12,"type":"隶属关系","context":"宋乐伟（市委书记）领导王伟（邳州市委书记）","overlap_org":"徐州市","overlap_period":""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "市委书记" in post and "市委" in post:
        return "200,30,30"  # deep red for party secretary
    if "市长" in post or "区长" in post or "县长" in post:
        return "30,80,200"  # deep blue for mayor/district head
    if "副书记" in post:
        return "220,60,60"
    if "副市长" in post or "副区长" in post:
        return "60,120,220"
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"
    if "组织部长" in post or "统战部长" in post or "宣传部长" in post or "政法委" in post:
        return "180,90,180"
    if "政协" in post:
        return "180,160,220"
    if "人大" in post:
        return "160,200,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>徐州市（地级市）领导班子 + 10区县市工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
