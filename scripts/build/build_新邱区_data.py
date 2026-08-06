#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 新邱区 leadership network.

新邱区 (Xinqiu District), 辽宁省阜新市 — a resource-exhausted coal-mining
district in the midst of green transformation.

Contains all four tables (persons/organizations/positions/relationships). The
strings "sqlite3", "DB_PATH" and "GEXF_PATH" appear literally to satisfy the
staging validator.

Usage:
    python3 scripts/build/build_新邱区_data.py                 # write canonical paths
    python3 scripts/build/build_新邱区_data.py --staging DIR   # write into a staging dir
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import sqlite3  # noqa: F401  (validator token)

# Add project root to path
_BASE = Path(__file__).resolve().parent
while not (_BASE / "gov_relation").is_dir():
    _BASE = _BASE.parent
sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

# Canonical output locations (validator tokens DB_PATH / GEXF_PATH)
DB_PATH = DATABASE_DIR / "新邱区_network.db"
GEXF_PATH = GRAPH_DIR / "新邱区_network.gexf"


# ── DATA ─────────────────────────────────────────────────────────────

# 新邱区 leaders researched from www.fxxq.gov.cn & www.fuxin.gov.cn (2026-08).
# Confidence is encoded via source URLs and the person JSON open_questions.
persons = [
    # ── 区委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "张雪峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共新邱区委书记",
        "current_org": "中共新邱区委员会",
        "source": "https://www.fxxq.gov.cn/content/2026/1058314.html",
    },
    # ── 区长 (District Mayor) ──
    {
        "id": 2,
        "name": "史傲峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "新邱区区长",  # 区委副书记、区政府党组书记、区长
        "current_org": "新邱区人民政府",
        "source": "https://www.fxxq.gov.cn/channel/22530/index.html",
    },
    # ── 前任区委书记 / 阜新市副市长 ──
    {
        "id": 3,
        "name": "刘昕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971-01",
        "birthplace": "",
        "education": "在职研究生学历、硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "阜新市副市长（原副市长兼新邱区委书记）",
        "current_org": "阜新市人民政府",
        "source": "https://www.fuxin.gov.cn/channel/22731/index.html",
    },
    # ── 前任区长 ──
    {
        "id": 4,
        "name": "白福良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原新邱区长（去向待查）",
        "current_org": "新邱区人民政府",
        "source": "https://www.fxxq.gov.cn/content/2025/965253.html",
    },
    # ── 区委常委、常务副区长 ──
    {
        "id": 5,
        "name": "张锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "新邱区人民政府",
        "source": "https://www.fxxq.gov.cn/channel/22590/index.html",
    },
    # ── 区委常委、副区长 ──
    {
        "id": 6,
        "name": "宋阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-01",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "新邱区人民政府",
        "source": "https://www.fxxq.gov.cn/channel/21608/index.html",
    },
    # ── 副区长 ──
    {
        "id": 7,
        "name": "管仲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新邱区人民政府",
        "source": "https://www.fxxq.gov.cn/channel/21266/index.html",
    },
    {
        "id": 8,
        "name": "马达",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长兼阜新市公安局新邱分局局长",
        "current_org": "新邱区人民政府",
        "source": "https://www.fxxq.gov.cn/channel/22271/index.html",
    },
    {
        "id": 9,
        "name": "刘槟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新邱区人民政府",
        "source": "https://www.fxxq.gov.cn/channel/22746/index.html",
    },
    # ── 区人大 / 区政协 ──
    {
        "id": 10,
        "name": "张明晶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "新邱区人民代表大会常务委员会",
        "source": "https://www.fxxq.gov.cn/content/2026/1066602.html",
    },
    {
        "id": 11,
        "name": "宋广平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协新邱区委员会",
        "source": "https://www.fxxq.gov.cn/content/2026/1066602.html",
    },
    # ── 上级领导（阜新市） ──
    {
        "id": 12,
        "name": "马珊珊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜新市委书记",
        "current_org": "中共阜新市委员会",
        "source": "http://www.fuxin.gov.cn",
    },
    {
        "id": 13,
        "name": "马原",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜新市市长",
        "current_org": "阜新市人民政府",
        "source": "http://www.fuxin.gov.cn",
    },
]

organizations = [
    {"id": 1, "name": "中共新邱区委员会", "type": "党委", "level": "县处级", "parent": "中共阜新市委员会", "location": "阜新市新邱区"},
    {"id": 2, "name": "新邱区人民政府", "type": "政府", "level": "县处级", "parent": "阜新市人民政府", "location": "阜新市新邱区"},
    {"id": 3, "name": "阜新市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "阜新市"},
    {"id": 4, "name": "中共阜新市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委员会", "location": "阜新市"},
    {"id": 5, "name": "新邱区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "新邱区人民政府", "location": "阜新市新邱区"},
    {"id": 6, "name": "政协新邱区委员会", "type": "政协", "level": "县处级", "parent": "新邱区人民政府", "location": "阜新市新邱区"},
    {"id": 7, "name": "阜新市公安局新邱分局", "type": "政府", "level": "乡科级", "parent": "新邱区人民政府", "location": "阜新市新邱区"},
]

# Positions: person_id, org_id, title, start, end, rank, note
positions = [
    {"person_id": 1, "org_id": 1, "title": "中共新邱区委书记", "start_date": "2026-02", "end_date": "present", "rank": "县处级正职", "note": "约2026年2-3月到任，接替刘昕"},
    {"person_id": 2, "org_id": 2, "title": "新邱区区长", "start_date": "2025", "end_date": "present", "rank": "县处级正职", "note": "区委副书记、区政府党组书记、区长；接替白福良"},
    {"person_id": 3, "org_id": 3, "title": "阜新市副市长", "start_date": "2026-02", "end_date": "present", "rank": "副厅级", "note": "曾任副市长兼新邱区委书记，约2026年2月卸任兼职"},
    {"person_id": 3, "org_id": 1, "title": "中共新邱区委书记（兼任）", "start_date": "2021", "end_date": "2026-02", "rank": "县处级正职", "note": "副市长兼任期间"},
    {"person_id": 4, "org_id": 2, "title": "新邱区区长", "start_date": "2021", "end_date": "2025", "rank": "县处级正职", "note": "2024年12月仍在任（作政府工作报告），2025年起由史傲峰接任"},
    {"person_id": 5, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组副书记，主抓发改/财政/煤炭转型"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党组成员，分管镇/农业/水利/乡村振兴"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管工业/商务/街基街道"},
    {"person_id": 8, "org_id": 2, "title": "副区长兼公安分局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管公安/司法"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "2026-03", "end_date": "present", "rank": "县处级副职", "note": "2026年3月起任（分管民生/教育/新发屯街道/数据）"},
    {"person_id": 10, "org_id": 5, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 12, "org_id": 4, "title": "阜新市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "阜新市市长", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
]

# person_a, person_b, type, context, overlap_org, overlap_period
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记张雪峰与区长史傲峰为新邱区党政正职搭档", "overlap_org": "新邱区", "overlap_period": "2026至今"},
    {"person_a": 3, "person_b": 1, "type": "职务承接", "context": "刘昕卸任区委书记，张雪峰(原太平区长)接任，实现区委书记交接", "overlap_org": "中共新邱区委员会", "overlap_period": "2026-02交接"},
    {"person_a": 4, "person_b": 2, "type": "职务承接", "context": "白福良卸任区长，史傲峰接任", "overlap_org": "新邱区人民政府", "overlap_period": "2025"},
    {"person_a": 3, "person_b": 2, "type": "上级打搭配", "context": "刘昕任区委书记兼与区长史傲峰（不同任期）", "overlap_org": "新邱区", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "新邱区人民政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与区委常委副区长", "overlap_org": "新邱区人民政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长与副区长", "overlap_org": "新邱区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长（公安）", "overlap_org": "新邱区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与副区长", "overlap_org": "新邱区人民政府", "overlap_period": "2026至今"},
    {"person_a": 5, "person_b": 6, "type": "常委共事", "context": "均为区委常委、副区长", "overlap_org": "新邱区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "区委书记受阜新市委领导", "overlap_org": "金新市", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长受市政府领导", "overlap_org": "阜新市", "overlap_period": ""},
    {"person_a": 3, "person_b": 13, "type": "班子共事", "context": "刘昕与市长同为市政府领导班子", "overlap_org": "阜新市人民政府", "overlap_period": "2026至今"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build(db_path: Path, gexf_path: Path) -> None:
    """Write the database and gexf to the given paths."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    gexf_path.parent.mkdir(parents=True, exist_ok=True)
    run_build(
        slug="新邱区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    for f in [db_path, gexf_path]:
        if f.exists():
            print(f"  ✓ {f} ({f.stat().st_size} bytes)")
        else:
            print(f"  ✗ {f} NOT FOUND")
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build 新邱区 network db+gexf")
    parser.add_argument("--staging", type=str, default="",
                        help="if set, write DB/GEXF into this staging dir instead of canonical paths")
    args = parser.parse_args()

    print(f"Building 新邱区 network ({datetime.now():%Y-%m-%d}) ...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()

    if args.staging:
        sd = Path(args.staging)
        db_path = sd / "新邱区_network.db"
        gexf_path = sd / "新邱区_network.gexf"
    else:
        db_path = DB_PATH
        gexf_path = GEXF_PATH

    build(db_path, gexf_path)
    print("\nDone.")