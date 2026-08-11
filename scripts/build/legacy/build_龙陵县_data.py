#!/usr/bin/env python3
"""龙陵县 (Longling County, Baoshan, Yunnan) leadership network build script.

Data sources
------------
- longling.gov.cn — official government portal, news articles confirming current leaders
- Homepage news reports: 龙陵县2026年上半年经济运行分析会议 (2026-07-28),
  龙陵县十五届县委常委会第3次会议 (2026-07-28),
  龙陵县第四次全国农业普查工作推进会 (2026-07-22)

Confidence notes
----------------
Current leadership (2026) confirmed via official government website news reports.
Career biographies for core figures are unavailable due to degraded web access
(Baidu 403, Baidu Baike timeouts, Exa rate limits, Google/Bing timeouts).
Open questions and uncertainty are explicitly flagged in person JSON files.

Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Level: 县 (county-level)
Province: 云南省 (Yunnan)
Parent city: 保山市 (Baoshan)
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# Add project root for gov_relation imports
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parents[2].resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ──────────────────────────────────────────────────────────────
SLUG = "龙陵县"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

# ── Persons (id starts at 1) ─────────────────────────────────────────────
# Leadership confirmed via longling.gov.cn news as of July 2026.

PERSONS = [
    # ═══ 1. 县委书记 — Party Secretary ═══
    {
        "id": 1,
        "name": "牛永东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙陵县委书记",
        "current_org": "中国共产党龙陵县委员会",
        "source": "龙陵县人民政府门户网站 (longling.gov.cn) — 新闻报道: 龙陵县2026年上半年经济运行分析会议 (2026-07-28)",
    },
    # ═══ 2. 县长 — County Mayor ═══
    {
        "id": 2,
        "name": "李永标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙陵县委副书记、县长",
        "current_org": "龙陵县人民政府",
        "source": "龙陵县人民政府门户网站 (longling.gov.cn) — 新闻报道: 龙陵县第四次全国农业普查工作推进会 (2026-07-22)",
    },
    # ═══ 3. 县委常委、副县长 — Standing Committee Member, Deputy County Mayor ═══
    {
        "id": 3,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙陵县委常委、县人民政府副县长",
        "current_org": "龙陵县人民政府",
        "source": "龙陵县人民政府门户网站 — 新闻报道: 龙陵县第四次全国农业普查工作推进会 (2026-07-22)",
    },
    # ═══ 4. 县委常委、副县长 — Deputy County Mayor ═══
    {
        "id": 4,
        "name": "孟春来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙陵县委常委、县人民政府副县长",
        "current_org": "龙陵县人民政府",
        "source": "龙陵县人民政府门户网站 — 新闻报道: 龙陵县第四次全国农业普查工作推进会 (2026-07-22)",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党龙陵县委员会", "type": "党委", "level": "县级", "parent": "中国共产党保山市委员会", "location": "龙陵县"},
    {"id": 2, "name": "龙陵县人民政府", "type": "政府", "level": "县级", "parent": "保山市人民政府", "location": "龙陵县"},
    {"id": 3, "name": "龙陵县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "保山市人大常委会", "location": "龙陵县"},
    {"id": 4, "name": "中国人民政治协商会议龙陵县委员会", "type": "政协", "level": "县级", "parent": "保山市政协", "location": "龙陵县"},
]

# ── Positions ────────────────────────────────────────────────────────────

POSITIONS = [
    # 牛永东
    {"person_id": 1, "org_id": 1, "title": "龙陵县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作。2026年7月28日主持十五届县委常委会第3次会议和全县上半年经济运行分析会议。"},
    # 李永标
    {"person_id": 2, "org_id": 2, "title": "龙陵县人民政府县长、党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县人民政府全面工作。2026年7月22日出席第四次全国农业普查工作推进会并讲话。"},
    {"person_id": 2, "org_id": 1, "title": "中共龙陵县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼任"},
    # 刘勇
    {"person_id": 3, "org_id": 2, "title": "龙陵县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年7月22日以县委常委、副县长身份出席第四次全国农业普查工作推进会"},
    {"person_id": 3, "org_id": 1, "title": "龙陵县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 孟春来
    {"person_id": 4, "org_id": 2, "title": "龙陵县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年7月22日以县委常委、副县长身份参加第四次全国农业普查工作推进会"},
    {"person_id": 4, "org_id": 1, "title": "龙陵县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────

RELATIONSHIPS = [
    # 牛永东 <-> 李永标: 党政一把手
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记与县长党政工作搭档", "overlap_org": "龙陵县", "overlap_period": "present"},
    # 牛永东 <-> 刘勇: 书记与常委
    {"person_a": 1, "person_b": 3, "type": "领导与被领导", "context": "县委常委班子，县委领导副县长", "overlap_org": "中国共产党龙陵县委员会", "overlap_period": "present"},
    # 牛永东 <-> 孟春来: 书记与常委
    {"person_a": 1, "person_b": 4, "type": "领导与被领导", "context": "县委常委班子，县委领导副县长", "overlap_org": "中国共产党龙陵县委员会", "overlap_period": "present"},
    # 李永标 <-> 刘勇: 县长与副县长
    {"person_a": 2, "person_b": 3, "type": "领导与被领导", "context": "县长与副县长工作协作", "overlap_org": "龙陵县人民政府", "overlap_period": "present"},
    # 李永标 <-> 孟春来: 县长与副县长
    {"person_a": 2, "person_b": 4, "type": "领导与被领导", "context": "县长与副县长工作协作", "overlap_org": "龙陵县人民政府", "overlap_period": "present"},
    # 刘勇 <-> 孟春来: 常委同事
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "县委常委、副县长共事关系", "overlap_org": "龙陵县人民政府", "overlap_period": "present"},
]

# ── Paths ────────────────────────────────────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═ {SLUG} Leadership Network Builder ═")
    print(f"Date: {TIMESTAMP}")
    print(f"DB:   {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()

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

    print("Done.")