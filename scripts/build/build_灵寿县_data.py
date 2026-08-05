#!/usr/bin/env python3
"""
灵寿县领导班子工作关系网络 — Build script
河北省石家庄市灵寿县（县）

Research date: 2026-08-05

CONFIRMED leaders (from official 灵寿县人民政府门户网站 www.lingshou.gov.cn, 2026-03 ~ 2026-07):
- 县委书记 靳军
- 县委副书记、县长 胡万程
- 副县长、公安局局长 孙飞跃 (领导之窗)

Web access was heavily degraded during this investigation (Exa rate-limited, Baidu
search/Baike behind anti-bot verification, Bing/Sogou/360/Google blocked, Wikipedia and
Jina Reader timeouts). Official 灵寿县政府网站 was the only reachable primary source, and
its leadership-window page only statically renders one profile (孙飞跃). Therefore the
broader 常委/副县长 roster and all biographical fields are encoded as plausible/unverified
(see per-claim confidence + data/tmp/hebei_灵寿县/checkpoint_01_research.md).

Per source_fallbacks.md this uses partial-evidence artifact mode: structurally valid
artifacts are produced, uncertainty is explicit, unresolved fields go to open_questions.
"""

import json
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

# Repo root import path (script lives in data/tmp/hebei_灵寿县/)
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build

SLUG = "灵寿县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "灵寿县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "灵寿县_network.gexf")

AS_OF = "2026-08-05"

# ── Persons ────────────────────────────────────────────────────────────
persons = [
    # ── 县委书记 (Party Secretary) — CONFIRMED via official news ──
    {
        "id": 1,
        "name": "靳军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "灵寿县委书记",
        "current_org": "中共灵寿县委员会",
        "source": "http://www.lingshou.gov.cn/ (2026年7月 县委新闻, 灵寿县政府门户网站拓维要闻; 县委书记靳军主持召开县委理论学习中心组集中学习会) [confirmed]",
    },
    # ── 县委副书记、县长 (County Mayor) — CONFIRMED via official news ──
    {
        "id": 2,
        "name": "胡万程",
        "gender": "男",
        "ethnicity": "汉族",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "灵寿县委副书记、县长",
        "current_org": "灵寿县人民政府",
        "source": "http://www.lingshou.gov.cn/ (2026年3月, 县政府县国土空间规划委员会2026年第3次会议: 县长、县国土空间规划委员会主任胡万程主持召开) [confirmed]",
    },
    # ── 副县长、公安局局长 — CONFIRMED via 领导之窗 ──
    {
        "id": 3,
        "name": "孙飞跃",
        "gender": "男",
        "ethnicity": "汉族",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "灵寿县人民政府 / 灵寿县公安局",
        "source": "http://www.lingshou.gov.cn/columns/1ad2aeb9-34d5-4482-9ee2-8bebfb7b6dcd/index.html (领导之窗) [confirmed]",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1, "name": "中共灵寿县委员会", "type": "党委",
        "level": "县处级", "parent": "中共石家庄市委员会", "location": "灵寿县",
    },
    {
        "id": 2, "name": "灵寿县人民政府", "type": "政府",
        "level": "县处级", "parent": "石家庄市人民政府", "location": "灵寿县",
    },
    {
        "id": 3, "name": "灵寿县公安局", "type": "政府",
        "level": "乡科级", "parent": "灵寿县人民政府/石家庄市公安局", "location": "灵寿县",
    },
    {
        "id": 4, "name": "灵寿县人民代表大会常务委员会", "type": "人大",
        "level": "县处级", "parent": "石家庄市人民代表大会常务委员会", "location": "灵寿县",
    },
    {
        "id": 5, "name": "政协灵寿县委员会", "type": "政协",
        "level": "县处级", "parent": "政协石家庄市委员会", "location": "灵寿县",
    },
    {
        "id": 6, "name": "中共灵寿县纪律检查委员会", "type": "党委",
        "level": "县处级", "parent": "中共石家庄市纪律检查委员会", "location": "灵寿县",
    },
    {
        "id": 7, "name": "中共石家庄市委员会", "type": "党委",
        "level": "地厅级", "parent": "中共河北省委员会", "location": "石家庄市",
    },
    {
        "id": 8, "name": "石家庄市人民政府", "type": "政府",
        "level": "地厅级", "parent": "河北省人民政府", "location": "石家庄市",
    },
]

# ── Positions ──
positions = [
    # 靳军 — 县委书记 (现任)
    {"person_id": 1, "org_id": 1, "title": "灵寿县委书记",
     "start_date": "~2022", "end_date": "present", "rank": "县处级正职",
     "note": "至2026年7月仍在任; 来源: 灵寿县政府门户2026年多条领导活动报道 (confirmed). 上任时间~2022 为模型推断 (unverified)"},
    # 胡万程 — 县长 (现任)
    {"person_id": 2, "org_id": 2, "title": "灵寿县委副书记、县长",
     "start_date": "~2024", "end_date": "present", "rank": "县处级正职",
     "note": "至2026年3月任县长兼县国土空间规划委员会主任 (confirmed: official); 上任时间~2024 为推断 (unverified)"},
    # 孙飞跃 — 副县长、公安局长
    {"person_id": 3, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责公安、退役军人、司法、民政、社会稳定、打击盗采自然资源等 (confirmed: 领导之窗)"},
    {"person_id": 3, "org_id": 3, "title": "公安局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管县公安局、县退役军人事务局、县司法局、县民政局 (confirmed: 领导之窗)"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长（党政正职搭档）",
     "overlap_org": "灵寿县", "overlap_period": "~2024-"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "孙飞跃向县长负责，分管公安、政法、民政稳定工作",
     "overlap_org": "灵寿县人民政府", "overlap_period": "present"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县公安局长属县政府序列，纳入县委安全生产/社会稳定领导体系",
     "overlap_org": "灵寿县", "overlap_period": "present"},
]

if __name__ == "__main__":
    print(f"Building {SLUG} network... (staging: {STAGING_DIR})")
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
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")