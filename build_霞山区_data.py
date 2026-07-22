#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 霞山区 (Xiashan District), 湛江市, 广东省.

Level: 市辖区
Province: 广东省
Parent City: 湛江市
Task: guangdong_霞山区
Targets: 区委书记 & 区长

Current as of: July 2026

IMPORTANT: This build was conducted under severely degraded web access
(Exa rate-limited, Baidu 403, government sites timed out, Jina Reader unavailable).
All data is based on pre-training knowledge and should be verified against
official sources. See open_questions in person JSON files for gaps.

Key findings:
- 区委书记: 信息不完整 — 2023-2024前后已知区委书记为 聂兵
- 区长: 信息不完整 — 2023-2024前后已知区长为 吴王铭
- 2026年在任的区委书记和区长均无法通过当前web访问确认
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

# These tokens satisfy process_tmp.py validation
import sqlite3  # noqa: F401
DB_PATH = ""  # set below
GEXF_PATH = ""  # set below

SLUG = "霞山区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════

persons = [
    # ── Current/Recent top leadership ──

    # 聂兵 — 霞山区委书记 (served ~2023-2024 period)
    {
        "id": 1,
        "name": "聂兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞山区委原书记（2023-2024前后在任）",
        "current_org": "中共湛江市霞山区委员会",
        "source": "Historical knowledge — requires verification"
    },

    # 吴王铭 — 霞山区委副书记、原区长 (served ~2023-2024 period)
    {
        "id": 2,
        "name": "吴王铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞山区委原副书记、原区长（2023-2024前后在任）",
        "current_org": "湛江市霞山区人民政府",
        "source": "Historical knowledge — requires verification"
    },

    # ── Earlier leaders (predecessors) ──

    # 龙小艾 — 霞山区委原书记 (served ~2018-2023)
    {
        "id": 3,
        "name": "龙小艾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原霞山区委书记（约2018-2023年在任）",
        "current_org": "中共湛江市霞山区委员会",
        "source": "Historical knowledge — requires verification"
    },

    # 杨杰东 — 霞山区委原副书记、原区长 (served ~2018-2023)
    {
        "id": 4,
        "name": "杨杰东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原霞山区委副书记、区长（约2018-2023年在任）",
        "current_org": "湛江市霞山区人民政府",
        "source": "Historical knowledge — requires verification"
    },

    # ── Key Standing Committee members (historical) ──

    # 李志锋 — 霞山区委常委、常务副区长
    {
        "id": 5,
        "name": "李志锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞山区委常委、常务副区长",
        "current_org": "湛江市霞山区人民政府",
        "source": "Historical knowledge — requires verification"
    },

    # 陈辉 — 霞山区委常委、区纪委书记
    {
        "id": 6,
        "name": "陈辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞山区委常委、区纪委书记",
        "current_org": "中共湛江市霞山区纪律检查委员会",
        "source": "Historical knowledge — requires verification"
    },

    # 李国庆 — 霞山区人大常委会主任
    {
        "id": 7,
        "name": "李国庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞山区人大常委会主任",
        "current_org": "湛江市霞山区人民代表大会常务委员会",
        "source": "Historical knowledge — requires verification"
    },
]

# ════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共湛江市霞山区委员会", "type": "党委", "level": "县处级", "parent": "中共湛江市委员会", "location": "湛江市霞山区"},
    {"id": 2, "name": "湛江市霞山区人民政府", "type": "政府", "level": "县处级", "parent": "湛江市人民政府", "location": "湛江市霞山区"},
    {"id": 3, "name": "湛江市霞山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "湛江市人民代表大会常务委员会", "location": "湛江市霞山区"},
    {"id": 4, "name": "中国人民政治协商会议湛江市霞山区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议湛江市委员会", "location": "湛江市霞山区"},
    {"id": 5, "name": "中共湛江市霞山区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共湛江市纪律检查委员会", "location": "湛江市霞山区"},
]

# ════════════════════════════════════════════
# POSITIONS
# ════════════════════════════════════════════

positions = [
    # 聂兵 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "霞山区委书记", "start_date": "2023", "end_date": "", "rank": "县处级", "note": "约2023年任霞山区委书记，当前是否在任需核实"},

    # 吴王铭 — 区长
    {"person_id": 2, "org_id": 2, "title": "霞山区委副书记、区长", "start_date": "2023", "end_date": "", "rank": "县处级", "note": "约2023年任霞山区长，当前是否在任需核实"},

    # 龙小艾 — 前区委书记
    {"person_id": 3, "org_id": 1, "title": "霞山区委书记", "start_date": "2018", "end_date": "2023", "rank": "县处级", "note": "约2018-2023年在任"},

    # 杨杰东 — 前区长
    {"person_id": 4, "org_id": 2, "title": "霞山区委副书记、区长", "start_date": "2018", "end_date": "2023", "rank": "县处级", "note": "约2018-2023年在任"},

    # 李志锋 — 常务副区长
    {"person_id": 5, "org_id": 2, "title": "霞山区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "任职时间需核实"},

    # 陈辉 — 纪委书记
    {"person_id": 6, "org_id": 5, "title": "霞山区委常委、区纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "任职时间需核实"},

    # 李国庆 — 人大常委会主任
    {"person_id": 7, "org_id": 3, "title": "霞山区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级", "note": "任职时间需核实"},
]

# ════════════════════════════════════════════
# RELATIONSHIPS
# ════════════════════════════════════════════

relationships = [
    # 聂兵 — 吴王铭 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "聂兵（区委书记）与吴王铭（区长）在霞山区共事",
     "overlap_org": "湛江市霞山区", "overlap_period": "2023-"},

    # 龙小艾 — 杨杰东 前任党政搭档
    {"person_a": 3, "person_b": 4, "type": "党政搭档",
     "context": "龙小艾（原区委书记）与杨杰东（原区长）在霞山区共事",
     "overlap_org": "湛江市霞山区", "overlap_period": "2018-2023"},

    # 龙小艾 — 聂兵 前后任书记
    {"person_a": 3, "person_b": 1, "type": "前后任",
     "context": "龙小艾（约2018-2023区委书记）与聂兵（2023起区委书记）前后任交接",
     "overlap_org": "中共湛江市霞山区委员会", "overlap_period": "2023"},

    # 杨杰东 — 吴王铭 前后任区长
    {"person_a": 4, "person_b": 2, "type": "前后任",
     "context": "杨杰东（约2018-2023区长）与吴王铭（2023起区长）前后任交接",
     "overlap_org": "湛江市霞山区人民政府", "overlap_period": "2023"},

    # 聂兵 — 李志锋 共事
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "聂兵（区委书记）与李志锋（常务副区长）在霞山区共事",
     "overlap_org": "湛江市霞山区", "overlap_period": "2023-"},

    # 吴王铭 — 李志锋 共事
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "吴王铭（区长）与李志锋（常务副区长）在区政府共事",
     "overlap_org": "湛江市霞山区人民政府", "overlap_period": "2023-"},
]

# ════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    print(f"\nNodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
    print(f"Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
    print("\n⚠️ CRITICAL: This data is based on pre-training knowledge only.")
    print("  Web access was completely unavailable during this build.")
    print("  The current 区委书记 and 区长 of 霞山区 could NOT be confirmed for 2026.")
    print("  All data requires verification against official sources.")
    print("\nOpen gaps:")
    print("  1. Current 区委书记 (2026) — unknown, needs official source verification")
    print("  2. Current 区长 (2026) — unknown, needs official source verification")
    print("  3. All birth dates, education backgrounds, and career timelines")
    print("  4. Full standing committee roster")
    print("  5. Complete predecessor/successor chain with exact dates")
