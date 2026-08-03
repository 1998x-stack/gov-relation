#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 朝阳市 (Chaoyang), 辽宁省.

Level: 地级市 (prefecture-level city)
Province: 辽宁省
Targets: 市委书记 (Party Secretary), 市长 (Mayor)
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]  # data/tmp/liaoning_朝阳市/ → repo root
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "朝阳市_network.db"
GEXF_PATH = STAGING_DIR / "朝阳市_network.gexf"

TODAY = datetime.now().strftime("%Y%m%d")

# ──────────────────────────────────────────────
# PERSONS
# ──────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "老颜武",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共朝阳市委员会",
        "source": "official — ln.gov.cn 2026-02-01: 省委决定老颜武同志任中共朝阳市委书记",
    },
    {
        "id": 2,
        "name": "张耀鼎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "current_post": "市委副书记、市长",
        "current_org": "朝阳市人民政府",
        "source": "official — chaoyang.gov.cn: 张耀鼎，1979年8月生，大学学历、学士学位，中共党员。现任朝阳市委副书记，市长、市政府党组书记",
    },
    {
        "id": 3,
        "name": "蒋涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "朝阳市人民政府",
        "source": "official — chaoyang.gov.cn: 蒋涛，1978年1月生，在职研究生学历，硕士学位，中共党员，现任朝阳市委常委，市政府党组副书记、副市长",
    },
    {
        "id": 4,
        "name": "孙永东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年2月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "current_post": "市委常委、副市长",
        "current_org": "朝阳市人民政府",
        "source": "official — chaoyang.gov.cn: 孙永东，1968年2月生，大学学历，学士学位，中共党员。现任朝阳市委常委，市政府党组成员、副市长",
    },
    {
        "id": 5,
        "name": "刘文俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年5月",
        "birthplace": "",
        "education": "在职大学学历，学士学位",
        "current_post": "市委常委、秘书长，市政府党组成员",
        "current_org": "中共朝阳市委员会",
        "source": "official — chaoyang.gov.cn: 刘文俊，1970年5月生，在职大学学历，学士学位，中共党员。现任朝阳市委常委，朝阳市委秘书长，市政府党组成员",
    },
    {
        "id": 6,
        "name": "张新天",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "current_post": "副市长、市公安局局长",
        "current_org": "朝阳市人民政府",
        "source": "official — chaoyang.gov.cn: 张新天，1974年10月生，在职研究生学历，硕士学位，中共党员，现任朝阳市政府党组成员、副市长，市公安局党委书记、局长，督察长",
    },
    {
        "id": 7,
        "name": "高宇恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "current_post": "副市长",
        "current_org": "朝阳市人民政府",
        "source": "official — chaoyang.gov.cn: 高宇恒，1972年10月生，研究生学历，硕士学位，无党派。现任朝阳市政府副市长",
    },
    {
        "id": 8,
        "name": "孙淼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "current_post": "副市长",
        "current_org": "朝阳市人民政府",
        "source": "official — chaoyang.gov.cn: 孙淼，1977年6月生，研究生学历，博士学位，中共党员，现任朝阳市政府党组成员、副市长",
    },
    {
        "id": 9,
        "name": "郭喜春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "在职大学学历，学士学位",
        "current_post": "市政府秘书长",
        "current_org": "朝阳市人民政府",
        "source": "official — chaoyang.gov.cn: 郭喜春，1973年6月生，在职大学学历，学士学位，中共党员，现任朝阳市政府秘书长兼市政府办公室主任",
    },
    {
        "id": 10,
        "name": "单义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "current_post": "前任市委书记（已离任）",
        "current_org": "",
        "source": "media — 辽宁日报2026-02-01: 老颜武同志任中共朝阳市委书记（接替单义）",
    },
    {
        "id": 11,
        "name": "谢卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "current_post": "前任市长（已离任）",
        "current_org": "",
        "source": "inferred — 老颜武于2021年左右接任市长，前任为谢卫东",
    },
]

# ──────────────────────────────────────────────────────────────────
# ORGANIZATIONS
# ──────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共朝阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委员会", "location": "辽宁省朝阳市"},
    {"id": 2, "name": "朝阳市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "辽宁省朝阳市"},
    {"id": 3, "name": "朝阳市人大常委会", "type": "人大", "level": "地厅级", "parent": "辽宁省人大常委会", "location": "辽宁省朝阳市"},
    {"id": 4, "name": "政协朝阳市委员会", "type": "政协", "level": "地厅级", "parent": "政协辽宁省委员会", "location": "辽宁省朝阳市"},
    {"id": 5, "name": "中共朝阳市纪律检查委员会", "type": "纪委", "level": "地厅级", "parent": "中共辽宁省纪律检查委员会", "location": "辽宁省朝阳市"},
    {"id": 6, "name": "中共朝阳市委组织部", "type": "党委", "level": "地厅级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市"},
    {"id": 7, "name": "中共朝阳市委宣传部", "type": "党委", "level": "地厅级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市"},
    {"id": 8, "name": "中共朝阳市委政法委员会", "type": "党委", "level": "地厅级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市"},
    {"id": 9, "name": "中共朝阳市委统一战线工作部", "type": "党委", "level": "地厅级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市"},
    {"id": 10, "name": "朝阳市公安局", "type": "政府", "level": "地厅级", "parent": "朝阳市人民政府", "location": "辽宁省朝阳市"},
]

# ──────────────────────────────────────────────────────────────────
# POSITIONS
# ──────────────────────────────────────────────────────────────────
positions = [
    # 老颜武
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2026-02", "end": "present", "rank": "正厅级", "note": "2026年2月辽宁省委决定任市委书记"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start": "2021?", "end": "2026-02", "rank": "正厅级", "note": "2021年左右任市长，2026年2月升任市委书记"},
    # 张耀鼎
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "unknown", "end": "2026-03", "rank": "副厅级", "note": "任市长前担任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start": "2026-03", "end": "present", "rank": "正厅级", "note": "2026年3月30日市人代会选举为市长"},
    # 蒋涛
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "市政府党组副书记、副市长（常务）", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    # 孙永东
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    # 刘文俊
    {"person_id": 5, "org_id": 1, "title": "市委常委、市委秘书长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "市政府党组成员", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    # 张新天
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 10, "title": "市公安局局长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    # 高宇恒
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "副厅级", "note": "无党派"},
    # 孙淼
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    # 郭喜春
    {"person_id": 9, "org_id": 2, "title": "市政府秘书长兼办公室主任", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    # 单义（前任书记）
    {"person_id": 10, "org_id": 1, "title": "市委书记", "start": "2023-05", "end": "2026-01", "rank": "正厅级", "note": "2023年5月任市委书记，2026年初卸任"},
    # 谢卫东（前任市长）
    {"person_id": 11, "org_id": 2, "title": "市长", "start": "2019", "end": "2021?", "rank": "正厅级", "note": "前任市长，后由老颜武接任"},
]

# ──────────────────────────────────────────────────────────────────
# RELATIONSHIPS
# ──────────────────────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政领导搭档", "context": "市委书记与市长，党政主要领导", "overlap_org": "朝阳市", "overlap_period": "2026-03至今"},
    # 前任与现任
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor", "context": "单义为前任市委书记，老颜武接任", "overlap_org": "中共朝阳市委员会", "overlap_period": "2023-2026"},
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "老颜武接替谢卫东任市长", "overlap_org": "朝阳市人民政府", "overlap_period": "2019-2021"},
    # 市委常委班子
    {"person_a": 1, "person_b": 3, "type": "党委领导班子", "context": "市委书记与常务副市长/常委", "overlap_org": "中共朝阳市委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 4, "type": "党委领导班子", "context": "市委书记与常委副市长", "overlap_org": "中共朝阳市委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 5, "type": "党委领导班子", "context": "市委书记与市委秘书长", "overlap_org": "中共朝阳市委员会", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 3, "type": "政府领导班子", "context": "市长与常务副市长", "overlap_org": "朝阳市人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 4, "type": "政府领导班子", "context": "市长与副市长", "overlap_org": "朝阳市人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 6, "type": "政府领导班子", "context": "市长与副市长/公安局长", "overlap_org": "朝阳市人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 7, "type": "政府领导班子", "context": "市长与副市长（无党派）", "overlap_org": "朝阳市人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 8, "type": "政府领导班子", "context": "市长与副市长", "overlap_org": "朝阳市人民政府", "overlap_period": "2026至今"},
    {"person_a": 3, "person_b": 4, "type": "政府领导班子", "context": "常务副市长与副市长", "overlap_org": "朝阳市人民政府", "overlap_period": "2026至今"},
]


def main():
    run_build(
        slug="朝阳市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n--- Summary ---")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()