#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 细河区 leadership network.

Usage:
    python3 scripts/build/build_细河区_data.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (区委书记) ──
    # 区委书记 name not confirmed from available web sources as of 2026-07-25
    {
        "id": 1,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共细河区委书记",
        "current_org": "中共细河区委员会",
        "source": "https://www.fxxh.gov.cn/channel/11314/index.html",
    },
    # ── Current District Mayor (区长) ──
    {
        "id": 2,
        "name": "李霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "细河区区长",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/channel/11314/index.html",
    },
    # ── Deputy Mayors / 区委常委 ──
    {
        "id": 3,
        "name": "张旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/999562.html",
    },
    {
        "id": 4,
        "name": "梅琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（原常务）",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/980665.html",
    },
    {
        "id": 5,
        "name": "顾若冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/999562.html",
    },
    {
        "id": 6,
        "name": "任千伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原区委常委、副区长",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/980665.html",
    },
    {
        "id": 7,
        "name": "张翠",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/999562.html",
    },
    {
        "id": 8,
        "name": "朱艳伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/999562.html",
    },
    {
        "id": 9,
        "name": "舒显赫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/999562.html",
    },
    {
        "id": 10,
        "name": "刘洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（公安）",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/999562.html",
    },
    {
        "id": 11,
        "name": "陈瞳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原副区长（公安）",
        "current_org": "细河区人民政府",
        "source": "https://www.fxxh.gov.cn/content/2025/980665.html",
    },
    # ── 阜新市领导（上级） ──
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
]

organizations = [
    {"id": 1, "name": "中共细河区委员会", "type": "党委", "level": "县处级", "parent": "中共阜新市委员会", "location": "阜新市细河区"},
    {"id": 2, "name": "细河区人民政府", "type": "政府", "level": "县处级", "parent": "阜新市人民政府", "location": "阜新市细河区"},
    {"id": 3, "name": "中共阜新市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委员会", "location": "阜新市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "中共细河区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任区委书记姓名待确认"},
    {"person_id": 2, "org_id": 2, "title": "细河区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "截至2025年8月在任"},
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2025年8月起任常务副区长"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长（常务）", "start_date": "", "end_date": "2025-08", "rank": "县处级副职", "note": "2025年1月任常务副区长，2025年8月分工调整"},
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管文旅、数据、营商环境"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "2025-08", "rank": "县处级副职", "note": "2025年1月分管住建交通农业，8月已不在分工名单"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管科技、民政、生态环境"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管教育体育、卫健、市场监管"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管工业、农业、商务、退役军人"},
    {"person_id": 10, "org_id": 2, "title": "副区长（公安）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管公安、司法"},
    {"person_id": 11, "org_id": 2, "title": "副区长（公安）", "start_date": "", "end_date": "2025-08", "rank": "县处级副职", "note": "2025年1月任副区长（公安），8月由刘洋接替"},
    {"person_id": 12, "org_id": 3, "title": "阜新市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长是细河区党政正职关系", "overlap_org": "细河区", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "细河区人民政府", "overlap_period": "2025-08至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "细河区人民政府", "overlap_period": "2025-01至2025-08"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长与副区长", "overlap_org": "细河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长与副区长", "overlap_org": "细河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长", "overlap_org": "细河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与副区长", "overlap_org": "细河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长（公安）", "overlap_org": "细河区人民政府", "overlap_period": "2025-08至今"},
    {"person_a": 4, "person_b": 6, "type": "常委共事", "context": "均为区委常委、副区长", "overlap_org": "细河区人民政府", "overlap_period": "2025-01至2025-08"},
    {"person_a": 3, "person_b": 5, "type": "常委共事", "context": "均为区委常委、副区长", "overlap_org": "细河区人民政府", "overlap_period": "2025-08至今"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "区委书记受阜新市委领导", "overlap_org": "阜新市", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长受阜新市委领导", "overlap_org": "阜新市", "overlap_period": ""},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    slug = "细河区"
    db_path = DATABASE_DIR / "细河区_network.db"
    gexf_path = GRAPH_DIR / "细河区_network.gexf"

    print(f"Building {slug} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()

    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # Verify output
    for f in [db_path, gexf_path]:
        if f.exists():
            print(f"  ✓ {f.name} ({f.stat().st_size} bytes)")
        else:
            print(f"  ✗ {f} NOT FOUND")
            sys.exit(1)

    print("\nDone.")
