#!/usr/bin/env python3
"""防城区（防城港市）领导班子关系网络数据生成脚本。

Generated at: 2026-07-23
Task: guangxi_防城区
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# Ensure gov_relation is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR

# =========================================================================
# Paths
# =========================================================================
TASK_ID = "guangxi_防城区"
STAGING = TMP_DIR / TASK_ID
DB_PATH = STAGING / "防城区_network.db"
GEXF_PATH = STAGING / "防城区_network.gexf"
PERSONS_DIR = STAGING

AS_OF = "2026-07-23"

# =========================================================================
# Data: Persons
# =========================================================================
persons = [
    {
        "id": 1,
        "name": "巩发明",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "防城区委书记",
        "current_org": "中共防城港市防城区委员会",
        "source": "http://www.fcq.gov.cn/yw/fcqyw/t27320325.shtml"
    },
    {
        "id": 2,
        "name": "陈天富",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1981年11月",
        "birthplace": "待查",
        "education": "研究生（广西民族大学公共管理学院社会保障专业）",
        "party_join": "2004年5月",
        "work_start": "2005年7月",
        "current_post": "防城区区长",
        "current_org": "防城区人民政府",
        "source": "http://www.fcq.gov.cn/xxgk/xxgkml/ldzc/qz/"
    },
    {
        "id": 3,
        "name": "杨振强",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长",
        "current_org": "防城区人民政府",
        "source": "http://www.fcq.gov.cn/xxgk/xxgkml/ldzc/"
    },
    {
        "id": 4,
        "name": "陈炜",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、副区长（挂职）",
        "current_org": "防城区人民政府",
        "source": "http://www.fcq.gov.cn/xxgk/xxgkml/ldzc/"
    },
    {
        "id": 5,
        "name": "韦龙",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副区长、防城港市公安局防城分局局长",
        "current_org": "防城区人民政府",
        "source": "http://www.fcq.gov.cn/xxgk/xxgkml/ldzc/"
    },
    {
        "id": 6,
        "name": "曾志惠",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "防城区人民政府",
        "source": "http://www.fcq.gov.cn/xxgk/xxgkml/ldzc/"
    },
    {
        "id": 7,
        "name": "禤立鑫",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "防城区人民政府",
        "source": "http://www.fcq.gov.cn/xxgk/xxgkml/ldzc/"
    },
    {
        "id": 8,
        "name": "唐国海",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区人大常委会主任",
        "current_org": "防城区人大常委会",
        "source": "http://www.fcq.gov.cn/yw/fcqyw/t27234408.shtml"
    },
    {
        "id": 9,
        "name": "陆海滨",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "原防城区委书记（被调查）",
        "current_org": "（原）中共防城港市防城区委员会",
        "source": "https://www.thepaper.cn/newsDetail_forward_22887743"
    },
]

# =========================================================================
# Data: Organizations
# =========================================================================
organizations = [
    {"id": 1, "name": "中共防城港市防城区委员会", "type": "党委", "level": "县处级", "parent": "中共防城港市委员会", "location": "广西防城港市防城区"},
    {"id": 2, "name": "防城区人民政府", "type": "政府", "level": "县处级", "parent": "防城港市人民政府", "location": "广西防城港市防城区"},
    {"id": 3, "name": "防城区人大常委会", "type": "人大", "level": "县处级", "parent": "防城港市人大常委会", "location": "广西防城港市防城区"},
    {"id": 4, "name": "防城区政协", "type": "政协", "level": "县处级", "parent": "政协防城港市委员会", "location": "广西防城港市防城区"},
    {"id": 5, "name": "防城区纪委监委", "type": "纪委", "level": "县处级", "parent": "防城港市纪委监委", "location": "广西防城港市防城区"},
    {"id": 6, "name": "防城港市公安局防城分局", "type": "政府", "level": "乡科级", "parent": "防城区人民政府", "location": "广西防城港市防城区"},
    {"id": 7, "name": "中共防城港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西防城港市"},
    {"id": 8, "name": "防城港市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西防城港市"},
]

# =========================================================================
# Data: Positions
# =========================================================================
positions = [
    # 巩发明 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "防城区委书记", "start_date": "约2025年", "end_date": "至今", "rank": "县处级正职", "note": "原防城区区长升任"},
    {"person_id": 1, "org_id": 2, "title": "防城区区长", "start_date": "约2024年", "end_date": "约2025年", "rank": "县处级正职", "note": "前任区长"},
    # 陈天富 - 区长
    {"person_id": 2, "org_id": 2, "title": "防城区区长", "start_date": "约2025年", "end_date": "至今", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "防城区委副书记", "start_date": "约2025年", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # 杨振强 - 常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "2026年1月", "end_date": "至今", "rank": "县处级正职（正处长级）", "note": "2026年1月任区政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "防城区委常委", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "正处长级常委"},
    # 陈炜 - 挂职副区长
    {"person_id": 4, "org_id": 2, "title": "副区长（挂职）", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 4, "org_id": 1, "title": "防城区委常委", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # 韦龙 - 副区长兼公安局长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "防城港市公安局防城分局局长", "start_date": "待查", "end_date": "至今", "rank": "乡科级正职", "note": "四级高级警长"},
    # 曾志惠 - 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # 禤立鑫 - 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # 唐国海 - 人大主任
    {"person_id": 8, "org_id": 3, "title": "防城区人大常委会主任", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": ""},
    # 陆海滨 - 原书记
    {"person_id": 9, "org_id": 1, "title": "防城区委书记", "start_date": "待查", "end_date": "约2024-2025年", "rank": "县处级正职", "note": "被调查免职"},
]

# =========================================================================
# Data: Relationships
# =========================================================================
relationships = [
    # 巩发明 <-> 陈天富（前后任区长关系）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "巩发明任区长时，陈天富接任区长；巩发明升书记后二人党政搭档", "overlap_org": "防城区人民政府", "overlap_period": "约2025年"},
    # 巩发明 <-> 杨振强（上下级）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与常务副区长", "overlap_org": "防城区委", "overlap_period": "2026年至今"},
    # 陈天富 <-> 杨振强（区长与常务副区长）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "防城区人民政府", "overlap_period": "2026年至今"},
    # 陈天富 <-> 韦龙（区长与副区长）
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与分管公安副区长", "overlap_org": "防城区人民政府", "overlap_period": "至今"},
    # 陈天富 <-> 曾志惠
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "防城区人民政府", "overlap_period": "至今"},
    # 陈天富 <-> 禤立鑫
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "防城区人民政府", "overlap_period": "至今"},
    # 巩发明 <-> 陆海滨（前后任书记）
    {"person_a": 1, "person_b": 9, "type": "predecessor_successor", "context": "陆海滨被调查后，巩发明由区长升任书记", "overlap_org": "中共防城港市防城区委员会", "overlap_period": "约2025年"},
]

# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    run_build(
        slug="防城区领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done: DB={DB_PATH}, GEXF={GEXF_PATH}")
    print(f"Total: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
