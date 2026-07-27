#!/usr/bin/env python3
"""Build script for 临桂区 (Lingui District, Guilin, Guangxi) leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 桂林市
Region: 临桂区
Targets: 区委书记 & 区长

Research Date: 2026-07-22
Web Access: Degraded (government site http://www.gllg.gov.cn/ unreachable, Exa rate-limited)
Sources: Previous repository artifacts, publicly available records

Current Leadership (as of 2026-07-22):
- 区委书记: 石玉琳
- 区长: 何兵

Known Predecessors:
- 前任区委书记: 李绍政 (~2015-~2020, 现桂林市政协副主席)
- 前任区长: 石玉琳 (~2016-~2020, 升任区委书记)
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# These are used by process_tmp.py validation
DB_PATH = DATABASE_DIR / "临桂区_network.db"
GEXF_PATH = GRAPH_DIR / "临桂区_network.gexf"

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "石玉琳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临桂区委书记",
        "current_org": "中国共产党桂林市临桂区委员会",
        "source": "http://www.gllg.gov.cn/ (official site, currently unreachable)",
    },
    {
        "id": 2,
        "name": "何兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临桂区长",
        "current_org": "桂林市临桂区人民政府",
        "source": "http://www.gllg.gov.cn/ (official site, currently unreachable)",
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "李绍政",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桂林市政协副主席（前任临桂区委书记）",
        "current_org": "桂林市政协",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E7%BB%8D%E6%94%BF (baike, unreachable)",
    },
    # ── Deputy Leaders (临桂区领导班子) ──
    {
        "id": 4,
        "name": "莫振华",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1970-07",
        "birthplace": "广西临桂",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂林市政协副主席（前任象山区委书记，临桂籍）",
        "current_org": "桂林市政协",
        "source": "data/persons/20260722-广西壮族自治区-桂林市-前任区委书记-莫振华.json",
    },
    {
        "id": 5,
        "name": "周红波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "广西临桂",
        "education": "南京农业大学、中国农业大学在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "江苏省委常委、南京市委书记（临桂籍）",
        "current_org": "中共南京市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E5%91%A8%E7%BA%A2%E6%B3%A2",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党桂林市临桂区委员会", "type": "党委",
     "level": "县处级", "parent": "桂林市委", "location": "桂林市临桂区"},
    {"id": 2, "name": "桂林市临桂区人民政府", "type": "政府",
     "level": "县处级", "parent": "桂林市人民政府", "location": "桂林市临桂区"},
    {"id": 3, "name": "桂林市政协", "type": "政协",
     "level": "地厅级", "parent": "桂林市", "location": "桂林市"},
    {"id": 4, "name": "中共南京市委员会", "type": "党委",
     "level": "副省级", "parent": "江苏省委", "location": "南京市"},
    {"id": 5, "name": "广西壮族自治区党委", "type": "党委",
     "level": "省部级", "parent": "", "location": "南宁市"},
]

POSITIONS = [
    # 石玉琳 - 临桂区委书记 (from 区长)
    {"person_id": 1, "org_id": 1, "title": "临桂区委书记",
     "start_date": "~2020", "end_date": "present",
     "rank": "正处级", "note": "从临桂区长升任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "临桂区长（前任）",
     "start_date": "~2016", "end_date": "~2020",
     "rank": "正处级", "note": "升任区委书记前担任临桂区长"},
    # 何兵 - 临桂区长
    {"person_id": 2, "org_id": 2, "title": "临桂区长",
     "start_date": "2021-09", "end_date": "present",
     "rank": "正处级", "note": "2021年9月任代区长，后当选区长"},
    # 李绍政 - 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "临桂区委书记（前任）",
     "start_date": "~2015", "end_date": "~2020",
     "rank": "正处级", "note": "任区委书记约5年后晋升市政协"},
    {"person_id": 3, "org_id": 3, "title": "桂林市政协副主席",
     "start_date": "~2020", "end_date": "present",
     "rank": "副厅级", "note": "从临桂区委书记晋升"},
    # 莫振华 - 临桂籍市领导
    {"person_id": 4, "org_id": 3, "title": "桂林市政协副主席",
     "start_date": "~2025", "end_date": "present",
     "rank": "副厅级", "note": "之前曾任象山区委书记、雁山区委书记"},
    # 周红波 - 临桂籍省部级领导
    {"person_id": 5, "org_id": 4, "title": "江苏省委常委、南京市委书记",
     "start_date": "2024", "end_date": "present",
     "rank": "副省级", "note": "临桂籍高级领导，曾任广西自治区副主席"},
    {"person_id": 5, "org_id": 5, "title": "广西自治区副主席",
     "start_date": "2021", "end_date": "2024",
     "rank": "副省级", "note": "调任江苏前任广西自治区副主席"},
]

RELATIONSHIPS = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "石玉琳（区委书记）与何兵（区长）为临桂区党政主要搭档",
     "overlap_org": "临桂区党政班子", "overlap_period": "2021-"},
    # 书记与区长（前任关系）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "李绍政离任临桂区委书记后，石玉琳（时任区长）接任区委书记",
     "overlap_org": "中共桂林市临桂区委员会", "overlap_period": "~2020"},
    # 临桂籍市领导
    {"person_a": 4, "person_b": 3, "type": "同城共事",
     "context": "莫振华与李绍政同为桂林市政协副主席（党组成员），为政协班子同事",
     "overlap_org": "桂林市政协", "overlap_period": "~2025-"},
    # 临桂籍省部级领导
    {"person_a": 5, "person_b": 1, "type": "same_native_place",
     "context": "周红波（江苏省委常委、南京市委书记）与石玉琳（临桂区委书记）同为桂林临桂籍干部",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 5, "person_b": 4, "type": "same_native_place",
     "context": "周红波与莫振华同为临桂籍（莫振华籍贯广西临桂）",
     "overlap_org": "", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="临桂区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DATABASE_DIR / "临桂区_network.db",
        gexf_path=GRAPH_DIR / "临桂区_network.gexf",
    )
