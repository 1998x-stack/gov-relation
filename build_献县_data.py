#!/usr/bin/env python3
"""
河北省沧州市献县领导班子工作关系网络 — 2026-07-24
research_date: 2026-07-24
sources:
  - xianxian.gov.cn — 献县人民政府网站 (confirmed operational as of 2026-07-21)
  - 领导介绍页面 (动态生成，无法直接获取URL)

research_note:
  所有搜索渠道受限（Exa限流/Baidu403/Jina超时/Bing超时/Google被屏蔽）。
  献县人民政府网站(www.xianxian.gov.cn)可访问但领导介绍页面为JavaScript动态生成，
  无法直接获取当前领导班子名录。
  本脚本为partial-evidence模式——领导姓名留待后续补充。
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
# DB_PATH = DATABASE_DIR / "献县_network.db"
# GEXF_PATH = GRAPH_DIR / "献县_network.gexf"

SLUG = "献县"

# ── PERSONS ──
# Current leaders unknown due to search restrictions.
# Placeholder records for confirmed organization nodes.
persons = [
    # ===== County leadership placeholder =====
    {
        "id": 1,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "献县县委书记",
        "current_org": "中共献县县委",
        "source": "信息待补充",
    },
    {
        "id": 2,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "献县县委副书记、县长",
        "current_org": "献县人民政府",
        "source": "信息待补充",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {"id": 1, "name": "中共献县县委", "type": "党委", "level": "县级", "parent": "沧州市", "location": "献县"},
    {"id": 2, "name": "献县人民政府", "type": "政府", "level": "县级", "parent": "沧州市", "location": "献县"},
    {"id": 3, "name": "献县人大常委会", "type": "人大", "level": "县级", "parent": "沧州市", "location": "献县"},
    {"id": 4, "name": "献县政协", "type": "政协", "level": "县级", "parent": "沧州市", "location": "献县"},
    {"id": 5, "name": "献县纪委监委", "type": "党委", "level": "县级", "parent": "沧州市", "location": "献县"},
    {"id": 6, "name": "献县公安局", "type": "政府", "level": "县级", "parent": "沧州市", "location": "献县"},
    {"id": 7, "name": "献县经济开发区", "type": "开发区", "level": "县级", "parent": "沧州市", "location": "献县"},
    {"id": 8, "name": "中共沧州市委", "type": "党委", "level": "地市级", "parent": "河北省", "location": "沧州市"},
]

# ── POSITIONS ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "信息待补充"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "待查", "end": "present", "rank": "正处级", "note": "信息待补充"},
]

# ── RELATIONSHIPS ──
# No person-level relationships can be confirmed without names.
relationships = []


if __name__ == "__main__":
    staging = Path(__file__).parent
    db_path = staging / "献县_network.db"
    gexf_path = staging / "献县_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\n✅ Build complete for {SLUG}")
    print(f"   DB:   {db_path}")
    print(f"   GEXF: {gexf_path}")
    print(f"   Persons: {len(persons)}")
    print(f"   Orgs:    {len(organizations)}")
    print(f"   Pos:     {len(positions)}")
    print(f"   Rel:     {len(relationships)}")
    print(f"\n⚠️  PARTIAL EVIDENCE MODE: All cadre names are placeholders.")
    print(f"   Search channels were unavailable (Exa rate-limited, Baidu 403, Jina/Bing timeout).")
    print(f"   Update with actual names when search channels recover.")
