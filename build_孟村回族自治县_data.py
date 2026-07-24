#!/usr/bin/env python3
"""
河北省沧州市孟村回族自治县领导班子工作关系网络 — 2026-07-24
research_date: 2026-07-24
sources:
  - mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)
  - mengcun.gov.cn — 全县领导干部树立和践行正确政绩观学习教育读书班开班 (2026-04-08)
  - build_东光县_data.py — 马占芳曾任东光县长 (约2023-约2025)
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
# DB_PATH = DATABASE_DIR / "孟村回族自治县_network.db"
# GEXF_PATH = GRAPH_DIR / "孟村回族自治县_network.gexf"

SLUG = "孟村回族自治县"

# ── PERSONS ──
persons = [
    # ===== Current county leaders (as of 2026-04+) =====
    {
        "id": 1,
        "name": "马占芳",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县委书记",
        "current_org": "中共孟村回族自治县委",
        "source": "mengcun.gov.cn — 全县领导干部树立和践行正确政绩观学习教育读书班开班 (2026-04-08);  build_东光县_data.py — 曾任东光县长 (约2023-约2025)",
    },
    {
        "id": 2,
        "name": "李国德",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县委副书记、县政府党组书记、县长",
        "current_org": "孟村回族自治县人民政府",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23); mengcun.gov.cn — 全县领导干部树立和践行正确政绩观学习教育读书班开班 (2026-04-08)",
    },
    {
        "id": 3,
        "name": "孙志圣",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县委常委、县政府党组副书记、常务副县长",
        "current_org": "孟村回族自治县人民政府",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    {
        "id": 4,
        "name": "孙文华",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政府党组成员、副县长、县公安局局长",
        "current_org": "孟村回族自治县人民政府",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    {
        "id": 5,
        "name": "刘国练",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政府党组成员、副县长",
        "current_org": "孟村回族自治县人民政府",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    {
        "id": 6,
        "name": "李纪元",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政府党组成员、副县长",
        "current_org": "孟村回族自治县人民政府",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    {
        "id": 7,
        "name": "辛梅",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政府党组成员、副县长",
        "current_org": "孟村回族自治县人民政府",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    {
        "id": 8,
        "name": "李国玺",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政府党组成员、县经济开发区党工委副书记、管委会常务副主任",
        "current_org": "孟村回族自治县经济开发区",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    {
        "id": 9,
        "name": "范立军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政府党组成员、县自然资源和规划局党组书记、局长",
        "current_org": "孟村回族自治县自然资源和规划局",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    {
        "id": 10,
        "name": "杨智刚",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政府办公室主任",
        "current_org": "孟村回族自治县人民政府办公室",
        "source": "mengcun.gov.cn — 孟村回族自治县人民政府领导简介 (2025-12-23)",
    },
    # ===== Other current leaders =====
    {
        "id": 11,
        "name": "刘文新",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县人大常委会主任",
        "current_org": "孟村回族自治县人大常委会",
        "source": "mengcun.gov.cn — 全县领导干部树立和践行正确政绩观学习教育读书班开班 (2026-04-08)",
    },
    {
        "id": 12,
        "name": "李红芹",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "孟村回族自治县政协主席",
        "current_org": "中国人民政治协商会议孟村回族自治县委员会",
        "source": "mengcun.gov.cn — 全县领导干部树立和践行正确政绩观学习教育读书班开班 (2026-04-08)",
    },
    # ===== Previous leader reference (from 东光县) =====
    # 马占芳 previously served as 东光县长. The predecessor info is captured in the relationship.
]

# ── ORGANIZATIONS ──
organizations = [
    {"id": 1, "name": "中共孟村回族自治县委", "type": "党委", "level": "县级", "location": "孟村回族自治县"},
    {"id": 2, "name": "孟村回族自治县人民政府", "type": "政府", "level": "县级", "location": "孟村回族自治县"},
    {"id": 3, "name": "孟村回族自治县人大常委会", "type": "人大", "level": "县级", "location": "孟村回族自治县"},
    {"id": 4, "name": "中国人民政治协商会议孟村回族自治县委员会", "type": "政协", "level": "县级", "location": "孟村回族自治县"},
    {"id": 5, "name": "孟村回族自治县公安局", "type": "政府", "level": "县级", "location": "孟村回族自治县"},
    {"id": 6, "name": "孟村回族自治县纪委监委", "type": "党委", "level": "县级", "location": "孟村回族自治县"},
    {"id": 7, "name": "孟村回族自治县经济开发区", "type": "开发区", "level": "县级", "location": "孟村回族自治县"},
    {"id": 8, "name": "孟村回族自治县自然资源和规划局", "type": "政府", "level": "县级", "location": "孟村回族自治县"},
    {"id": 9, "name": "孟村回族自治县人民政府办公室", "type": "政府", "level": "县级", "location": "孟村回族自治县"},
]

# ── POSITIONS ──
positions = [
    # Current top leaders
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "约2025/2026", "end": "present", "rank": "正处级", "note": "前东光县长晋升"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "待查", "end": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    # Government team
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级"},
    {"person_id": 4, "org_id": 2, "title": "县政府党组成员、副县长、县公安局局长", "start": "待查", "end": "present", "rank": "副处级"},
    {"person_id": 5, "org_id": 2, "title": "县政府党组成员、副县长", "start": "待查", "end": "present", "rank": "副处级"},
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长", "start": "待查", "end": "present", "rank": "副处级"},
    {"person_id": 7, "org_id": 2, "title": "县政府党组成员、副县长", "start": "待查", "end": "present", "rank": "副处级"},
    {"person_id": 8, "org_id": 7, "title": "县政府党组成员、县经济开发区党工委副书记、管委会常务副主任", "start": "待查", "end": "present", "rank": "副处级"},
    {"person_id": 9, "org_id": 8, "title": "县政府党组成员、县自然资源和规划局党组书记、局长", "start": "待查", "end": "present", "rank": "正科级"},
    {"person_id": 10, "org_id": 9, "title": "县政府办公室主任", "start": "待查", "end": "present", "rank": "正科级"},
    # Other leaders
    {"person_id": 11, "org_id": 3, "title": "县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级"},
    {"person_id": 12, "org_id": 4, "title": "县政协主席", "start": "待查", "end": "present", "rank": "正处级"},
    # Previous positions (马占芳 at 东光县)
    {"person_id": 1, "org_id": 100001, "title": "东光县委副书记、县长", "start": "约2023", "end": "约2025", "rank": "正处级", "note": "参考build_东光县_data.py"},
]

# ── RELATIONSHIPS ──
relationships = [
    # Top leader partnership
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "马占芳(县委书记)与李国德(县长)搭班子", "overlap_org": "孟村回族自治县", "overlap_period": "约2026-present", "strength": "strong"},
    # Government team overlaps
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "李国德(县长)与孙志圣(常务副县长)搭班子", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "李国德(县长)与孙文华(公安局长)搭班子", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "李国德(县长)与刘国练(副县长)搭班子", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "李国德(县长)与李纪元(副县长)搭班子", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "李国德(县长)与辛梅(副县长)搭班子", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    # Government deputy overlaps
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "孙志圣(常务副县长)与孙文华(公安局长)共事", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "孙志圣(常务副县长)与刘国练(副县长)共事", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "孙志圣(常务副县长)与李纪元(副县长)共事", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "孙志圣(常务副县长)与辛梅(副县长)共事", "overlap_org": "孟村回族自治县人民政府", "overlap_period": "present", "strength": "strong"},
    # Predecessor-successor: 马占芳 from 东光县长
    # Note: The predecessor 县委书记 who was replaced by 马占芳 is unknown at this time
]


if __name__ == "__main__":
    staging = Path(__file__).parent
    db_path = staging / "孟村回族自治县_network.db"
    gexf_path = staging / "孟村回族自治县_network.gexf"

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
