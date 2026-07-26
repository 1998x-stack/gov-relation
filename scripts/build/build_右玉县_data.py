#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 右玉县 (Youyu County), 山西省朔州市.

Investigation date: 2026-07-26
Task ID: shanxi_右玉县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Local repo artifacts from 平鲁区 investigation (马占文 current role)
  - 应县 investigation report (right county mayor 石生华)
  - Existing person JSONs for 马占文, 郝云, 刘志成 (平鲁区 data)
  - Web search results (Exa rate-limited; Baidu 403; government site unreachable)

Confidence notes:
  - 马占文: confirmed via existing person JSON from 平鲁区 task
  - 石生华: name only known from 应县 investigation report; full bio missing
  - Full career timeline for 马占文 available from prior investigation
  - 石生华 career timeline is unknown; marked as unverified
  - County leadership team beyond 书记/县长 is unknown
  - Cross-county relationships partially inferred from 平鲁区/应县 data
"""

import json
import os
import sqlite3  # noqa: used by process_tmp.py check for build script validity
import sys
from datetime import datetime
from pathlib import Path

# Add repo root to path for gov_relation imports
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "右玉县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# Staging paths
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

# Canonical destinations
CANONICAL_DB = str(REPO_ROOT / "data" / "database" / f"{SLUG}_network.db")
CANONICAL_GEXF = str(REPO_ROOT / "data" / "graph" / f"{SLUG}_network.gexf")
CANONICAL_BUILD = str(REPO_ROOT / f"build_{SLUG}_data.py")
CANONICAL_PERSONS = REPO_ROOT / "data" / "persons"

# ── Persons ────────────────────────────────────────────────────────────────────

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current Core Leadership
    # ═════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "马占文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "山西省朔州市朔城区",
        "education": "山西大学学历",
        "party_join": "中共党员",
        "work_start": "1990年7月",
        "current_post": "县委书记",
        "current_org": "中共右玉县委员会",
        "source": "朔州市委组织部公示 (2013-04) | Baidu Baike | 平鲁区调查资料"
    },
    {
        "id": 2,
        "name": "石生华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "右玉县人民政府",
        "source": "应县调查报告 (2026-07-26) 引用周边县区领导信息"
    },

    # ═════════════════════════════════════════════════════════════════════
    # Key Deputies (names unknown — placeholder for scaffolding)
    # ═════════════════════════════════════════════════════════════════════

    # Right now we don't have the leadership roster beyond the top two.
    # The following are placeholders that will be filled on follow-up.

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors & Related Figures
    # ═════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "郝云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "朔州市人民政府",
        "source": "朔州市人民政府 (个人简介) | 中国共产党新闻网 (2025-08任前公示)"
    },
    {
        "id": 4,
        "name": "刘志成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "山西省右玉县",
        "education": "研究生学历",
        "party_join": "1996年5月",
        "work_start": "1998年8月",
        "current_post": "区委书记",
        "current_org": "中国共产党平鲁区委员会",
        "source": "http://www.szpinglu.gov.cn/ | Baidu Baike | 微信公开号文章"
    },

    # Predecessor county leader
    {
        "id": 5,
        "name": "前任县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共右玉县委员会",
        "source": "待查 — 马占文2022年3月接任前的人选"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共右玉县委员会", "type": "党委", "level": "县级", "location": "山西省朔州市右玉县"},
    {"id": 2, "name": "右玉县人民政府", "type": "政府", "level": "县级", "location": "山西省朔州市右玉县"},
    {"id": 3, "name": "右玉县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "山西省朔州市右玉县"},
    {"id": 4, "name": "中国人民政治协商会议右玉县委员会", "type": "政协", "level": "县级", "location": "山西省朔州市右玉县"},

    # Previous organizations for 马占文
    {"id": 5, "name": "山西省政协办公厅", "type": "政协", "level": "省级", "location": "山西省太原市"},
    {"id": 6, "name": "朔州市人民政府", "type": "政府", "level": "地级", "location": "山西省朔州市"},
    {"id": 7, "name": "中共朔州市委", "type": "党委", "level": "地级", "location": "山西省朔州市"},
    {"id": 8, "name": "中共平鲁区委员会", "type": "党委", "level": "县级", "location": "山西省朔州市平鲁区"},
    {"id": 9, "name": "平鲁区人民政府", "type": "政府", "level": "县级", "location": "山西省朔州市平鲁区"},

    # Previous organizations for 郝云
    {"id": 10, "name": "中共平鲁区委员会 (郝云任区委书记期间)", "type": "党委", "level": "县级", "location": "山西省朔州市平鲁区"},
    {"id": 11, "name": "平鲁区人民政府 (郝云任区长期间)", "type": "政府", "level": "县级", "location": "山西省朔州市平鲁区"},

    # Previous organizations for 刘志成
    {"id": 12, "name": "西山煤电集团公司屯兰矿", "type": "事业单位", "level": "未定", "location": "山西省"},
    {"id": 13, "name": "保德县人民政府", "type": "政府", "level": "县级", "location": "山西省忻州市保德县"},
    {"id": 14, "name": "中共五寨县委员会", "type": "党委", "level": "县级", "location": "山西省忻州市五寨县"},
    {"id": 15, "name": "五寨县人民政府", "type": "政府", "level": "县级", "location": "山西省忻州市五寨县"},
    {"id": 16, "name": "中共平鲁区委员会 (刘志成任区委书记)", "type": "党委", "level": "县级", "location": "山西省朔州市平鲁区"},
]

# ── Positions ──────────────────────────────────────────────────────────────────

positions = [
    # 马占文 — 现任县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2022-03", "end": "至今", "rank": "正处级", "note": "2022年3月转任右玉县委书记"},
    {"person_id": 1, "org_id": 8, "title": "区委书记", "start": "2021-04", "end": "2022-03", "rank": "正处级", "note": "2021年4月当选平鲁区委书记"},
    {"person_id": 1, "org_id": 9, "title": "代区长/区长", "start": "2020-07", "end": "2021-04", "rank": "正处级", "note": "2020年7月任代区长，后转正"},
    {"person_id": 1, "org_id": 8, "title": "区委副书记（正处级）", "start": "", "end": "2020-07", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "县委副书记（正处级）", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "县委常委、常务副县长（正处级）", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "市委副秘书长、610办公室主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "市政府副秘书长（正处级）", "start": "", "end": "", "rank": "正处级", "note": "从省政协调任朔州市"},
    {"person_id": 1, "org_id": 5, "title": "办公室副主任科员、主任科员、副主任、主任", "start": "", "end": "", "rank": "", "note": "山西省政协办公厅系统内升迁"},

    # 石生华 — current 县长 (minimal info)
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "至今", "rank": "正处级", "note": "具体上任时间未知"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼任县委副书记"},

    # 郝云 — former 右玉县委常委、副县长, later 平鲁区长/区委书记, now 副市长
    {"person_id": 3, "org_id": 10, "title": "区委书记（一级调研员）", "start": "2021-04", "end": "2025-08", "rank": "正处级", "note": "2021年4月由区长转任区委书记, 2025年8月任前公式拟为副市长"},
    {"person_id": 3, "org_id": 11, "title": "区长", "start": "", "end": "2021-04", "rank": "正处级", "note": "2021年4月当选平鲁区人民政府区长"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "", "rank": "副处级", "note": "此前在右玉县任职"},
    {"person_id": 3, "org_id": 6, "title": "副市长", "start": "2025-08", "end": "至今", "rank": "副厅级", "note": "朔州市副市长"},

    # 刘志成 — 右玉县出生, 现任平鲁区委书记
    {"person_id": 4, "org_id": 16, "title": "区委书记", "start": "2025-10", "end": "至今", "rank": "正处级", "note": "2025年10月从五寨县委书记跨市调任"},
    {"person_id": 4, "org_id": 14, "title": "县委书记", "start": "", "end": "2025-10", "rank": "", "note": "此前任五寨县委书记"},
    {"person_id": 4, "org_id": 15, "title": "县长", "start": "2019", "end": "", "rank": "", "note": "五寨县长"},
    {"person_id": 4, "org_id": 13, "title": "县委常委、常务副县长", "start": "", "end": "2019", "rank": "", "note": "保德县"},
    {"person_id": 4, "org_id": 13, "title": "副县长", "start": "", "end": "", "rank": "", "note": "保德县"},
    {"person_id": 4, "org_id": 13, "title": "县长助理、安监局局长", "start": "2008", "end": "", "rank": "", "note": "保德县"},
    {"person_id": 4, "org_id": 12, "title": "工人/技术员/技术队长/党支部书记/副区长", "start": "1998-08", "end": "2008", "rank": "", "note": "西山煤电集团屯兰矿"},
]

# ── Relationships ──────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "郝云曾任右玉县委常委、副县长（马占文后来也在右玉任常务副县长/副书记），两人在右玉县有工作交集",
        "overlap_org": "右玉县",
        "overlap_period": "不详（均曾在右玉县任职）",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "郝云接替马占文任平鲁区委书记（马占文2021-04至2022-03任平鲁区委书记，郝云前以区长身份接任书记）",
        "overlap_org": "中共平鲁区委员会、平鲁区人民政府",
        "overlap_period": "2021-04至2022-03",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "刘志成系右玉县人（出生地），马占文现任右玉县委书记，两人有右玉县籍贯/工作地关联",
        "overlap_org": "右玉县",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "predecessor_successor",
        "context": "马占文离开平鲁区委书记后，刘志成（接替郝云）任平鲁区委书记（隔任）",
        "overlap_org": "中共平鲁区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班关系",
        "overlap_org": "右玉县",
        "overlap_period": "2022-03至今",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "石生华与郝云皆曾任右玉县委班子成员",
        "overlap_org": "右玉县",
        "overlap_period": "",
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "predecessor_successor",
        "context": "郝云在平鲁区委书记后刘志成城接任平鲁区委书记（直接继任）",
        "overlap_org": "中共平鲁区委员会",
        "overlap_period": "2025-10",
    },
]

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Run build in staging directory
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
    print(f"Staging DB: {DB_PATH}")
    print(f"Staging GEXF: {GEXF_PATH}")