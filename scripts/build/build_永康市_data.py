#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 永康市 (Yongkang City, Zhejiang) leadership network.

归口地区: 浙江省金华市代管县级市
数据来源:
- 永康市人民政府网站 (yk.gov.cn) — 领导活动新闻, 2026年7月确认
- Baidu Baike — 胡勇春、郑云涛简历 (部分信息)
- 金华市委组织部 — 任前公示 (信息有限)
数据时效：2026-07-28
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "永康市"
PROVINCE = "浙江省"
PARENT_CITY = "金华市"
TODAY = "2026-07-28"

DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# DATA — hardcoded research data
# Sources: yk.gov.cn official leadership news 2026-07, Baidu Baike
# ═══════════════════════════════════════════════════════════════════════════

PERSONS = [
    # ── 市委书记 ──
    {
        "id": 1,
        "name": "胡勇春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永康市委书记",
        "current_org": "中共永康市委员会",
        "source": "https://www.yk.gov.cn/",  # confirmed via 领导活动 news: 胡勇春郑云涛走访慰问高温期间坚守岗位劳动者 (2026-07-24)
    },
    # ── 市委副书记、市长 ──
    {
        "id": 2,
        "name": "郑云涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永康市委副书记、市长",
        "current_org": "永康市人民政府",
        "source": "https://www.yk.gov.cn/",  # confirmed: 郑云涛在检查安全生产工作时强调 (2026-07-17); 郑云涛在企业开展四大双千活动 (2026-06-26)
    },
    # ── 前任市委书记 ──
    {
        "id": 3,
        "name": "章旭升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（前任永康市委书记）",
        "current_org": "待查",
        "source": "待查",
        "notes": "前任永康市委书记，胡勇春前任。2019-2020年左右任永康市委书记，后调任金华市其他职务或晋升。",
    },
    # ── 前任市长 ──
    {
        "id": 4,
        "name": "张群环",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年（推测）",
        "birthplace": "浙江金东（推测）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查",
        "current_org": "待查",
        "source": "待查",
        "notes": "曾任永康市市长（约2019-2022），后调任金华其他职务",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共永康市委员会", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": PROVINCE},
    {"id": 2, "name": "永康市人民政府", "type": "政府", "level": "县级", "parent": PARENT_CITY, "location": PROVINCE},
    {"id": 3, "name": "中共金华市委员会", "type": "党委", "level": "地市级", "parent": PROVINCE, "location": PROVINCE},
]

POSITIONS = [
    # -- 胡勇春 --
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "约2022-2023", "end_date": "至今", "rank": "正处级"},
    # -- 郑云涛 --
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "约2022-2023", "end_date": "至今", "rank": "正处级"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "约2022-2023", "end_date": "至今", "rank": "正处级"},
    # -- 章超升 (前任市委书记) --
    {"person_id": 3, "org_id": 1, "title": "市委书记", "start_date": "约2019", "end_date": "约2022-2023", "rank": "正处级"},
    # -- 张群环 (前任市长) --
    {"person_id": 4, "org_id": 2, "title": "市长", "start_date": "约2019", "end_date": "约2022", "rank": "正处级"},
]

RELATIONSHIPS = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "永康市党政主要领导搭班子",
        "overlap_org": "中共永康市委员会",
        "overlap_period": "约2022至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "胡勇春接替章超升担任永康市委书记",
        "overlap_org": "中共永康市委员会",
        "overlap_period": "约2022-2023",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "郑云涛接替张群环担任永康市市长",
        "overlap_org": "永康市人民政府",
        "overlap_period": "约2022",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    gexf_size = os.path.getsize(GEXF_PATH) if os.path.exists(GEXF_PATH) else 0
    print(f"Database: {DB_PATH} ({db_size} bytes)")
    print(f"GEXF graph: {GEXF_PATH} ({gexf_size} bytes)")
    print(f"Persons: {len(PERSONS)}")
    print(f"Organizations: {len(ORGANIZATIONS)}")
    print(f"Positions: {len(POSITIONS)}")
    print(f"Relationships: {len(RELATIONSHIPS)}")
    print("Build complete.")