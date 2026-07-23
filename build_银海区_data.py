#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北海市银海区领导班子工作关系网络 — 数据构建脚本（数据待补充）
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 北海市
Region: 银海区
Targets: 区委书记 & 区长

当前在任 (as of 2026-07-23):
⚠️ Web access to Chinese government sites was unavailable during research.
All data below is marked with appropriate confidence levels.
"""

import json
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "银海区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
AS_OF = "2026-07-23"
PROVINCE = "广西壮族自治区"
PARENT_CITY = "北海市"

# =========================================================================
# 1. PERSONS
# =========================================================================
# Schema: id, name, gender, ethnicity, birth, birthplace, education,
#          party_join, work_start, current_post, current_org, source
#
# NOTE: Due to complete web access failure to Chinese government sites,
# most fields are marked as "待查" (pending verification).
# See report/open_gaps.md for prioritized investigation targets.

persons = [
    # ════════════════════════════════════════
    # Core Target 1: 区委书记 (Party Secretary)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "银海区委书记（待确认）",
        "current_org": "中共北海市银海区委员会",
        "source": "⚠️ 待确认：银海区暂无公开可访问数据，建议通过北海市政府网站或广西组织部任前公示补充"
    },
    # ════════════════════════════════════════
    # Core Target 2: 区长 (District Mayor)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "银海区区长（待确认）",
        "current_org": "银海区人民政府",
        "source": "⚠️ 待确认：银海区暂无公开可访问数据，建议通过北海市政府网站或广西组织部任前公示补充"
    },
    # ════════════════════════════════════════
    # Placeholder for 区委副书记 (Deputy Party Secretary)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "银海区委副书记（待确认）",
        "current_org": "中共北海市银海区委员会",
        "source": "⚠️ 待确认"
    },
    # ════════════════════════════════════════
    # Placeholder for 常务副区长 (Executive Deputy Mayor)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "银海区常务副区长（待确认）",
        "current_org": "银海区人民政府",
        "source": "⚠️ 待确认"
    },
    # ════════════════════════════════════════
    # Placeholder for 纪委书记 (Discipline Secretary)
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "银海区纪委书记（待确认）",
        "current_org": "中共北海市银海区纪律检查委员会",
        "source": "⚠️ 待确认"
    },
    # ════════════════════════════════════════
    # Placeholder for 组织部部长 (Organization Dept Head)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "银海区委组织部部长（待确认）",
        "current_org": "中共北海市银海区委员会组织部",
        "source": "⚠️ 待确认"
    },
    # ════════════════════════════════════════
    # Placeholder for 宣传部部长 (Propaganda Dept Head)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "银海区委宣传部部长（待确认）",
        "current_org": "中共北海市银海区委员会宣传部",
        "source": "⚠️ 待确认"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
# Schema: id, name, type, level, parent, location

organizations = [
    {
        "id": 1,
        "name": "中共北海市银海区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共北海市委员会",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 2,
        "name": "银海区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "北海市人民政府",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 3,
        "name": "中共北海市银海区纪律检查委员会",
        "type": "纪委",
        "level": "市辖区",
        "parent": "中共北海市纪律检查委员会",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 4,
        "name": "中共北海市银海区委员会组织部",
        "type": "党委部门",
        "level": "市辖区",
        "parent": "中共北海市银海区委员会",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 5,
        "name": "中共北海市银海区委员会宣传部",
        "type": "党委部门",
        "level": "市辖区",
        "parent": "中共北海市银海区委员会",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 6,
        "name": "中共北海市银海区委员会政法委员会",
        "type": "党委部门",
        "level": "市辖区",
        "parent": "中共北海市银海区委员会",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 7,
        "name": "北海市银海区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "北海市人大常委会",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议北海市银海区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "北海市政协",
        "location": "广西壮族自治区北海市银海区"
    },
    {
        "id": 9,
        "name": "银海区人民武装部",
        "type": "事业单位",
        "level": "市辖区",
        "parent": "北海军分区",
        "location": "广西壮族自治区北海市银海区"
    },
]

# =========================================================================
# 3. POSITIONS (all placeholder until data is available)
# =========================================================================

positions = [
    # (person_id, org_id, title, start, end, rank, note)
]

# =========================================================================
# 4. RELATIONSHIPS (all placeholder until data is available)
# =========================================================================

relationships = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)
]


# =========================================================================
# 5. BUILD
# =========================================================================

def main():
    print(f"Building {SLUG} network data...")
    
    db_path = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
    gexf_path = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
    
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )
    
    db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    gexf_size = os.path.getsize(gexf_path) if os.path.exists(gexf_path) else 0
    
    print(f"\n{'='*60}")
    print(f"  Summary for {SLUG}")
    print(f"{'='*60}")
    print(f"  Persons:       {len(persons)} (all placeholder)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions:     {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB:            {db_path} ({db_size} bytes)")
    print(f"  GEXF:          {gexf_path} ({gexf_size} bytes)")
    print(f"{'='*60}")
    print(f"  ⚠️  All person data is placeholder. Web access to Chinese\n"
          f"     government sites was unavailable during research.\n"
          f"     See report/open_gaps.md for investigation priorities.")
    print(f"{'='*60}")
    
    # Write summary JSON for inventory tracking
    summary = {
        "slug": SLUG,
        "generated_at": AS_OF,
        "province": PROVINCE,
        "city": PARENT_CITY,
        "region": SLUG,
        "level": "市辖区",
        "persons_count": len(persons),
        "orgs_count": len(organizations),
        "positions_count": len(positions),
        "relationships_count": len(relationships),
        "data_status": "placeholder",
        "note": "All person data is placeholder. Web access was unavailable."
    }
    summary_path = os.path.join(STAGING_DIR, "build_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
