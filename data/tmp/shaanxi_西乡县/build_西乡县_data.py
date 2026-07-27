#!/usr/bin/env python3
"""西乡县（汉中市）领导班子工作关系网络 — 构建脚本"""

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

SLUG = "西乡县"
STAGING = Path(__file__).parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

AS_OF = "2026-07-25"

# ── 人员定义 ──────────────────────────────────────────────────────────
# NOTE: Web search was unavailable during research (Exa rate-limited, Baidu/Sogou
# captcha-blocked, gov site pages behind dynamic rendering). Core leaders marked
# as "待查" with open gaps. Update these names once confirmed from:
# - www.snxx.gov.cn (西乡县人民政府) leadership page
# - 汉中市人大任免公告
# - 陕西省委组织部任前公示
PERSONS = [
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "西乡县委书记",
        "current_org": "中共西乡县委员会",
        "source": "需从www.snxx.gov.cn确认",
    },
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "西乡县县长",
        "current_org": "西乡县人民政府",
        "source": "需从www.snxx.gov.cn确认",
    },
    {
        "id": 3,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "西乡县委副书记",
        "current_org": "中共西乡县委员会",
        "source": "",
    },
    {
        "id": 4,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "",
        "work_start": "",
        "current_post": "西乡县委常委、常务副县长",
        "current_org": "西乡县人民政府",
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
        "current_post": "西乡县委常委、县纪委书记、县监委主任",
        "current_org": "中共西乡县纪律检查委员会",
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
        "current_post": "西乡县委常委、组织部部长",
        "current_org": "中共西乡县委组织部",
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
        "current_post": "西乡县委常委、宣传部部长",
        "current_org": "中共西乡县委宣传部",
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
        "current_post": "西乡县委常委、政法委书记",
        "current_org": "中共西乡县委政法委员会",
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
        "current_post": "西乡县委常委、统战部部长",
        "current_org": "中共西乡县委统战部",
        "source": "",
    },
    {
        "id": 10,
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
        "source": "需确认",
    },
    {
        "id": 11,
        "name": "待查_汉中市市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉中市市长",
        "current_org": "汉中市人民政府",
        "source": "需确认",
    },
    {
        "id": 12,
        "name": "待查_西乡县政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西乡县政协主席",
        "current_org": "政协西乡县委员会",
        "source": "",
    },
    {
        "id": 13,
        "name": "待查_西乡县人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西乡县人大常委会主任",
        "current_org": "西乡县人民代表大会常务委员会",
        "source": "",
    },
]

# ── 组织定义 ──────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共西乡县委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市委员会", "location": "陕西省汉中市西乡县"},
    {"id": 2, "name": "西乡县人民政府", "type": "政府", "level": "县处级", "parent": "汉中市人民政府", "location": "陕西省汉中市西乡县"},
    {"id": 3, "name": "中共西乡县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共西乡县委员会", "location": "陕西省汉中市西乡县"},
    {"id": 4, "name": "中共西乡县委组织部", "type": "党委", "level": "县处级", "parent": "中共西乡县委员会", "location": "陕西省汉中市西乡县"},
    {"id": 5, "name": "中共西乡县委宣传部", "type": "党委", "level": "县处级", "parent": "中共西乡县委员会", "location": "陕西省汉中市西乡县"},
    {"id": 6, "name": "中共西乡县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共西乡县委员会", "location": "陕西省汉中市西乡县"},
    {"id": 7, "name": "中共西乡县委统战部", "type": "党委", "level": "县处级", "parent": "中共西乡县委员会", "location": "陕西省汉中市西乡县"},
    {"id": 8, "name": "汉中市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "陕西省汉中市"},
    {"id": 9, "name": "中共汉中市委员会", "type": "党委", "level": "地厅级", "parent": "中共陕西省委员会", "location": "陕西省汉中市"},
    {"id": 10, "name": "政协西乡县委员会", "type": "政协", "level": "县处级", "parent": "政协汉中市委员会", "location": "陕西省汉中市西乡县"},
    {"id": 11, "name": "西乡县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "汉中市人民代表大会常务委员会", "location": "陕西省汉中市西乡县"},
]

# ── 任职关系 ──────────────────────────────────────────────────────────
POSITIONS = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "西乡县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "西乡县县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作"},
    # 县委副书记
    {"person_id": 3, "org_id": 1, "title": "西乡县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 常务副县长
    {"person_id": 4, "org_id": 2, "title": "西乡县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 3, "title": "西乡县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 组织部长
    {"person_id": 6, "org_id": 4, "title": "西乡县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 宣传部长
    {"person_id": 7, "org_id": 5, "title": "西乡县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 政法委书记
    {"person_id": 8, "org_id": 6, "title": "西乡县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 统战部长
    {"person_id": 9, "org_id": 7, "title": "西乡县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 汉中市委书记
    {"person_id": 10, "org_id": 9, "title": "汉中市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "需确认"},
    # 汉中市市长
    {"person_id": 11, "org_id": 8, "title": "汉中市市长", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "需确认"},
    # 政协主席
    {"person_id": 12, "org_id": 10, "title": "西乡县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 人大常委会主任
    {"person_id": 13, "org_id": 11, "title": "西乡县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── 工作关系 ──────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长，西乡县党政主要领导搭档关系", "overlap_org": "中共西乡县委员会/西乡县人民政府", "overlap_period": "待查"},
    # 县委书记—县委副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委副书记", "overlap_org": "中共西乡县委员会", "overlap_period": "待查"},
    # 县委书记—纪委书记
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与纪委书记（同级监督关系）", "overlap_org": "中共西乡县委员会", "overlap_period": "待查"},
    # 县委书记—组织部长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与组织部部长（干部管理）", "overlap_org": "中共西乡县委员会", "overlap_period": "待查"},
    # 县长—常务副县长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "西乡县人民政府", "overlap_period": "待查"},
    # 政法委书记—县委书记
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与政法委书记", "overlap_org": "中共西乡县委员会", "overlap_period": "待查"},
    # 宣传部长—县委书记
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记与宣传部部长", "overlap_org": "中共西乡县委员会", "overlap_period": "待查"},
    # 统战部长—县委书记
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "县委书记与统战部部长", "overlap_org": "中共西乡县委员会", "overlap_period": "待查"},
    # 县—市领导关系
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "西乡县委书记与汉中市委书记（上下级领导关系）", "overlap_org": "中共汉中市委员会/中共西乡县委员会", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "西乡县县长与汉中市市长（上下级领导关系）", "overlap_org": "汉中市人民政府/西乡县人民政府", "overlap_period": "待查"},
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
