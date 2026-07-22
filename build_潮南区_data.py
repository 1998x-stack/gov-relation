#!/usr/bin/env python3
"""
潮南区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Chaonan District leadership network.

Level: 市辖区
Province: 广东省
City: 汕头市
Region: 潮南区
Targets: 区委书记 & 区长

Research Sources:
- chaonan.gov.cn — 潮南区人民政府门户网站 (政务要闻, 镇街动态)
- shantou.gov.cn — 汕头市人民政府门户网站

Research Date: 2026-07-22
"""

import os
import sqlite3  # noqa: required by process_tmp validator
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "潮南区"
DB_PATH = str(DATABASE_DIR / "潮南区_network.db")
GEXF_PATH = str(GRAPH_DIR / "潮南区_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "张晓铿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共汕头市潮南区委员会",
        "source": "chaonan.gov.cn — 政务要闻 (区委书记张晓铿专题调研滨海旅游路规划建设工作, 2026-07-13; 区委书记张晓铿带队督导检查防汛防涝蚊媒防控及消防安全工作, 2026-05-26; 区委书记张晓铿带队检查安全生产消防安全食品安全和城市管理提升工作, 2026-05-06)",
    },
    {
        "id": 2,
        "name": "陈泽波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "潮南区人民政府",
        "source": "chaonan.gov.cn — 政务要闻 (区长陈泽波'四不两直'督导企业消防安全工作, 2026-07-16)",
    },
    # ════════════════════════════════════════════
    # District Committee Leadership
    # ════════════════════════════════════════════
    # Known leadership team members from government news
    # Note: 潮南区 has a 5-person Standing Committee typically
]

organizations = [
    {"id": 1, "name": "中共汕头市潮南区委员会", "type": "党委", "level": "市辖区", "parent": "中共汕头市委员会", "location": "汕头市潮南区"},
    {"id": 2, "name": "潮南区人民政府", "type": "政府", "level": "市辖区", "parent": "汕头市人民政府", "location": "汕头市潮南区"},
]

positions = [
    # 张晓铿 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "张晓铿, 潮南区委书记, 2026年5-7月在任"},
    # 陈泽波 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "陈泽波, 潮南区区长, 2026年7月在任"},
]

relationships = [
    # 张晓铿 ↔ 陈泽波 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长搭档", "overlap_org": "潮南区", "overlap_period": ""},
]

# ════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════

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
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
