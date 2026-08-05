#!/usr/bin/env python3
"""
深泽县领导班子工作关系网络 — Build script
河北省石家庄市深泽县（县级行政区）

Confirmed sources (深泽县人民政府官网 shenze.gov.cn):
- 2026-07-30 深泽要闻「郝英鹏主持召开县委理论学习中心组学习会」: 确认 郝英鹏 = 县委书记
- 2026-07-03 深泽要闻「两优一先表彰大会」: 郝英鹏 以县委书记身份出席并作讲话
- 2026-07-23 深泽要闻「政协深泽县第十一届委员会第一次会议开幕」: 县委书记郝英鹏作讲话
- 2026-02-10 政府工作报告(第17届人大7次会议): 深泽县人民政府县长 孙利北
- 深政发〔2025〕1号 2025-02-13: 郝英鹏 在第十七届人大五次会议上作《政府工作报告》(证明其此前为县长)

Leadership path (confirmed from official reports):
- 郝英鹏: ~2021-2025 任深泽县县长(2025年1月第17届人大五次会议作报告) → 约2026年县第十三次党代会后升任县委书记
- 孙利北: 2026年起任县委副书记、县长(2026年2月第17届人大七次会议作报告)
- 郝英鹏(前县长) → 孙利北(现县长) 为前后任继任关系；郝英鹏(书记) 与 孙利北(县长) 为党政搭档

Research date: 2026-08-05
"""

import os
import sqlite3
import sys

def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent

_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build

AS_OF = "2026-08-05"

# ── PERSONS ──
persons = [
    # ── 县委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "郝英鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "深泽县委书记",
        "current_org": "中共深泽县委员会",
        "source": "https://www.shenze.gov.cn/columns/602cb006-670d-49a0-bd04-ac49cf52a563/202607/31/69c650ff-7dbd-41ba-b0b4-e98f45b6f67a.html",
    },
    # ── 县长 (County Mayor) ──
    {
        "id": 2,
        "name": "孙利北",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "深泽县委副书记、县长",
        "current_org": "深泽县人民政府/中共深泽县委员会",
        "source": "https://www.shenze.gov.cn/columns/bc9f06ed-1fc3-4647-8821-8a861698cb9f/202603/10/d935d91b-990d-40c5-80e4-d46d82d3e9f2.html",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共深泽县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市深泽县",
    },
    {
        "id": 2,
        "name": "深泽县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市深泽县",
    },
    {
        "id": 3,
        "name": "深泽县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "深泽县",
        "location": "河北省石家庄市深泽县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议深泽县委员会",
        "type": "政协",
        "level": "县",
        "parent": "深泽县",
        "location": "河北省石家庄市深泽县",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 郝英鹏 — 县委书记（2026 县第十三次党代会后升任；此前为县长）
    {"person_id": 1, "org_id": 1, "title": "深泽县委书记",
     "start_date": "2026?", "end_date": "present",
     "rank": "正处级", "note": "2026年县第十三次党代会后升任；曾为深泽县县长(2025年在任)"},
    {"person_id": 1, "org_id": 2, "title": "深泽县县长（此前）",
     "start_date": "2021?", "end_date": "2025/2026",
     "rank": "正处级", "note": "2025年1月第十七届人大五次会议作政府工作报告（深政发〔2025〕1号）"},
    # 孙利北 — 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "深泽县委副书记",
     "start_date": "2026?", "end_date": "present",
     "rank": "正处级", "note": "县长通常兼任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "深泽县人民政府县长",
     "start_date": "2026?", "end_date": "present",
     "rank": "正处级", "note": "2026年2月第十七届人大七次会议作政府工作报告；2026年7月新一届人大当选"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 郝英鹏 ↔ 孙利北 — 党政搭档（书记/县长）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "深泽县委书记与县长党政搭档",
     "overlap_org": "中共深泽县委员会/深泽县人民政府",
     "overlap_period": "2026?-present"},
    # 郝英鹏 → 孙利北 — 前后任县长
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "郝英鹏此前为深泽县县长(2025年在任)，后升任县委书记，孙利北继任县长",
     "overlap_org": "深泽县人民政府",
     "overlap_period": "2025-2026"},
]

# =========================================================================
# 5. BUILD
# =========================================================================
if __name__ == "__main__":
    STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(STAGING_DIR, "深泽县_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "深泽县_network.gexf")

    run_build(
        slug="深泽县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete.")