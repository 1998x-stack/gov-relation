#!/usr/bin/env python3
"""汉台区（汉中市）领导班子工作关系网络 — 构建脚本"""

from __future__ import annotations

import sqlite3  # noqa: used by gov_relation.runner via import
import sys
from pathlib import Path

# Ensure project root is on sys.path
_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "汉台区"
STAGING = Path(__file__).parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── 人员定义 ──────────────────────────────────────────────────────────
PERSONS = [
    {
        "id": 1,
        "name": "待查_区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委书记",
        "current_org": "中共汉中市汉台区委员会",
        "source": "汉中市政府官网",
    },
    {
        "id": 2,
        "name": "待查_区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区区长",
        "current_org": "汉台区人民政府",
        "source": "汉中市政府官网",
    },
    {
        "id": 3,
        "name": "待查_区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委副书记",
        "current_org": "中共汉中市汉台区委员会",
        "source": "",
    },
    {
        "id": 4,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委常委、常务副区长",
        "current_org": "汉台区人民政府",
        "source": "",
    },
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委常委、区纪委书记、区监委主任",
        "current_org": "中共汉中市汉台区纪律检查委员会",
        "source": "",
    },
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委常委、组织部部长",
        "current_org": "中共汉中市汉台区委组织部",
        "source": "",
    },
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委常委、宣传部部长",
        "current_org": "中共汉中市汉台区委宣传部",
        "source": "",
    },
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委常委、政法委书记",
        "current_org": "中共汉中市汉台区委政法委员会",
        "source": "",
    },
    {
        "id": 9,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区委常委、统战部部长",
        "current_org": "中共汉中市汉台区委统战部",
        "source": "",
    },
    {
        "id": 10,
        "name": "钟洪江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉中市市长（原汉中市市长）",
        "current_org": "汉中市人民政府",
        "source": "Wikipedia - Hanzhong page infobox",
    },
    {
        "id": 11,
        "name": "待查_汉中市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉中市委书记",
        "current_org": "中共汉中市委员会",
        "source": "",
    },
    {
        "id": 12,
        "name": "待查_汉台区政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区政协主席",
        "current_org": "政协汉中市汉台区委员会",
        "source": "",
    },
    {
        "id": 13,
        "name": "待查_汉台区人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉台区人大常委会主任",
        "current_org": "汉中市汉台区人民代表大会常务委员会",
        "source": "",
    },
]

# ── 组织定义 ──────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共汉中市汉台区委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市委员会", "location": "陕西省汉中市汉台区"},
    {"id": 2, "name": "汉台区人民政府", "type": "政府", "level": "县处级", "parent": "汉中市人民政府", "location": "陕西省汉中市汉台区"},
    {"id": 3, "name": "中共汉中市汉台区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市汉台区委员会", "location": "陕西省汉中市汉台区"},
    {"id": 4, "name": "中共汉中市汉台区委组织部", "type": "党委", "level": "县处级", "parent": "中共汉中市汉台区委员会", "location": "陕西省汉中市汉台区"},
    {"id": 5, "name": "中共汉中市汉台区委宣传部", "type": "党委", "level": "县处级", "parent": "中共汉中市汉台区委员会", "location": "陕西省汉中市汉台区"},
    {"id": 6, "name": "中共汉中市汉台区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市汉台区委员会", "location": "陕西省汉中市汉台区"},
    {"id": 7, "name": "中共汉中市汉台区委统战部", "type": "党委", "level": "县处级", "parent": "中共汉中市汉台区委员会", "location": "陕西省汉中市汉台区"},
    {"id": 8, "name": "汉中市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "陕西省汉中市"},
    {"id": 9, "name": "中共汉中市委员会", "type": "党委", "level": "地厅级", "parent": "中共陕西省委员会", "location": "陕西省汉中市"},
    {"id": 10, "name": "政协汉中市汉台区委员会", "type": "政协", "level": "县处级", "parent": "政协汉中市委员会", "location": "陕西省汉中市汉台区"},
    {"id": 11, "name": "汉中市汉台区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "汉中市人民代表大会常务委员会", "location": "陕西省汉中市汉台区"},
]

# ── 任职关系 ──────────────────────────────────────────────────────────
POSITIONS = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "汉台区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区委全面工作"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "汉台区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作"},
    # 区委副书记
    {"person_id": 3, "org_id": 1, "title": "汉台区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 常务副区长
    {"person_id": 4, "org_id": 2, "title": "汉台区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 3, "title": "汉台区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 组织部长
    {"person_id": 6, "org_id": 4, "title": "汉台区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 宣传部长
    {"person_id": 7, "org_id": 5, "title": "汉台区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 政法委书记
    {"person_id": 8, "org_id": 6, "title": "汉台区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 统战部长
    {"person_id": 9, "org_id": 7, "title": "汉台区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 钟洪江 - 汉中市市长
    {"person_id": 10, "org_id": 8, "title": "汉中市市长", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "Wikipedia记载; 可能已不再担任"},
    # 汉中市委书记
    {"person_id": 11, "org_id": 9, "title": "汉中市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "Wikipedia记载为'Vacant'，可能已更新"},
    # 政协主席
    {"person_id": 12, "org_id": 10, "title": "汉台区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 人大常委会主任
    {"person_id": 13, "org_id": 11, "title": "汉台区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── 工作关系 ──────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长，汉台区党政主要领导搭档关系", "overlap_org": "中共汉中市汉台区委员会/汉台区人民政府", "overlap_period": "待查"},
    # 区委书记—区委副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委副书记", "overlap_org": "中共汉中市汉台区委员会", "overlap_period": "待查"},
    # 区委书记—纪委书记
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与纪委书记（同级监督关系）", "overlap_org": "中共汉中市汉台区委员会", "overlap_period": "待查"},
    # 区委书记—组织部长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与组织部部长（干部管理）", "overlap_org": "中共汉中市汉台区委员会", "overlap_period": "待查"},
    # 区长—常务副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "汉台区人民政府", "overlap_period": "待查"},
    # 政法委书记—区委书记
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与政法委书记", "overlap_org": "中共汉中市汉台区委员会", "overlap_period": "待查"},
    # 宣传部长—区委书记
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与宣传部部长", "overlap_org": "中共汉中市汉台区委员会", "overlap_period": "待查"},
    # 统战部长—区委书记
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记与统战部部长", "overlap_org": "中共汉中市汉台区委员会", "overlap_period": "待查"},
    # 区级—市级领导关系
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "汉台区委书记与汉中市委书记（上下级领导关系）", "overlap_org": "中共汉中市委员会/中共汉中市汉台区委员会", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "汉台区区长与汉中市市长（上下级领导关系）", "overlap_org": "汉中市人民政府/汉台区人民政府", "overlap_period": "待查"},
]


def main() -> None:
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    run_build(
        slug=f"{SLUG}领导班子关系图",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
