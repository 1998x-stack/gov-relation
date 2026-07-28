#!/usr/bin/env python3
"""保山市 (Baoshan, Yunnan) leadership network build script.

Data sources
------------
- baoshan.gov.cn — official government leadership page (市政府领导)
- baoshan.gov.cn news reports — current events confirmed as of July 2026
- Baidu Baike / Wikipedia (historical reference, only partially reachable)

Confidence notes
----------------
Current leadership (2026) confirmed via official government website and news reports.
Career biographies for core figures are partial due to degraded web access (Baidu 403,
Baidu Baike timeouts, Exa rate limits). Open questions and uncertainty are explicitly
flagged in person JSON files.

Targets: 市委书记 (Party Secretary), 市长 (Mayor)
Level: 地级市 (prefecture-level city)
Province: 云南省 (Yunnan)
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
import sqlite3  # noqa: used via gov_relation.runner

# ── Metadata ──────────────────────────────────────────────────────────────
SLUG = "保山市"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

# ── Persons (id starts at 1) ─────────────────────────────────────────────
# Leadership confirmed via baoshan.gov.cn as of July 2026.

PERSONS = [
    # ═══ 1. 市委书记 — Party Secretary ═══
    {
        "id": 1,
        "name": "杨军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市委书记",
        "current_org": "中国共产党保山市委员会",
        "source": "保山市人民政府门户网站 (baoshan.gov.cn) — 新闻报道: 全市上半年经济运行分析会议 (2026-07-27)",
    },
    # ═══ 2. 市长 — Mayor ═══
    {
        "id": 2,
        "name": "左广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-01",
        "birthplace": "",
        "education": "研究生，管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市委副书记、市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 (baoshan.gov.cn) — 领导之窗 (2026-03-12)",
    },
    # ═══ 3. 常务副市长 — Executive Deputy Mayor ═══
    {
        "id": 3,
        "name": "范喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市委常委、常务副市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
    # ═══ 4. 副市长 — Vice Mayor ═══
    {
        "id": 4,
        "name": "张各兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市副市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
    # ═══ 5. 副市长 — Vice Mayor ═══
    {
        "id": 5,
        "name": "成德君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市副市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
    # ═══ 6. 副市长 — Vice Mayor ═══
    {
        "id": 6,
        "name": "高康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市副市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
    # ═══ 7. 副市长 — Vice Mayor ═══
    {
        "id": 7,
        "name": "李兴卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市副市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
    # ═══ 8. 副市长（公安）— Vice Mayor (Public Security) ═══
    {
        "id": 8,
        "name": "袁建勋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市副市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
    # ═══ 9. 副市长 — Vice Mayor ═══
    {
        "id": 9,
        "name": "龚翠莲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市副市长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
    # ═══ 10. 市政府秘书长 — Secretary-General ═══
    {
        "id": 10,
        "name": "张志红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保山市人民政府秘书长",
        "current_org": "保山市人民政府",
        "source": "保山市人民政府门户网站 — 市政府领导页",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党保山市委员会", "type": "党委", "level": "地级", "parent": "中国共产党云南省委员会", "location": "保山市"},
    {"id": 2, "name": "保山市人民政府", "type": "政府", "level": "地级", "parent": "云南省人民政府", "location": "保山市"},
    {"id": 3, "name": "保山市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "云南省人大常委会", "location": "保山市"},
    {"id": 4, "name": "中国人民政治协商会议保山市委员会", "type": "政协", "level": "地级", "parent": "云南省政协", "location": "保山市"},
]

# ── Positions ────────────────────────────────────────────────────────────

POSITIONS = [
    # 杨军
    {"person_id": 1, "org_id": 1, "title": "保山市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "主持市委全面工作。2026年7月27日在全市上半年经济运行分析会议上讲话。"},
    # 左广
    {"person_id": 2, "org_id": 2, "title": "保山市人民政府市长、党组书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "主持市人民政府全面工作。负责审计工作。"},
    {"person_id": 2, "org_id": 1, "title": "中共保山市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "兼任"},
    # 范喜
    {"person_id": 3, "org_id": 2, "title": "保山市常务副市长、市政府党组副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张各兴
    {"person_id": 4, "org_id": 2, "title": "保山市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 成德君
    {"person_id": 5, "org_id": 2, "title": "保山市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 高康
    {"person_id": 6, "org_id": 2, "title": "保山市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李兴卫
    {"person_id": 7, "org_id": 2, "title": "保山市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 袁建勋
    {"person_id": 8, "org_id": 2, "title": "保山市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 龚翠莲
    {"person_id": 9, "org_id": 2, "title": "保山市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张志红
    {"person_id": 10, "org_id": 2, "title": "保山市人民政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────

RELATIONSHIPS = [
    # 杨军 <-> 左广: 党政一把手
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记与市长党政工作搭档", "overlap_org": "保山市", "overlap_period": "present"},
    # 杨军 <-> 范喜: 书记与常务副市长
    {"person_a": 1, "person_b": 3, "type": "领导与被领导", "context": "市委常委班子，常务副市长协助市长工作", "overlap_org": "保山市", "overlap_period": ""},
    # 左广 <-> 范喜: 市长与常务副市长
    {"person_a": 2, "person_b": 3, "type": "领导与被领导", "context": "市长与常务副市长的工作协作", "overlap_org": "保山市人民政府", "overlap_period": ""},
    # 左广 <-> 张各兴: 市长与副市长
    {"person_a": 2, "person_b": 4, "type": "领导与被领导", "context": "市长与副市长工作协作", "overlap_org": "保山市人民政府", "overlap_period": ""},
    # 左广 <-> 成德君: 市长与副市长
    {"person_a": 2, "person_b": 5, "type": "领导与被领导", "context": "市长与副市长工作协作", "overlap_org": "保山市人民政府", "overlap_period": ""},
    # 左广 <-> 高康: 市长与副市长
    {"person_a": 2, "person_b": 6, "type": "领导与被领导", "context": "市长与副市长工作协作", "overlap_org": "保山市人民政府", "overlap_period": ""},
    # 左广 <-> 李兴卫: 市长与副市长
    {"person_a": 2, "person_b": 7, "type": "领导与被领导", "context": "市长与副市长工作协作", "overlap_org": "保山市人民政府", "overlap_period": ""},
    # 左广 <-> 袁建勋: 市长与副市长
    {"person_a": 2, "person_b": 8, "type": "领导与被领导", "context": "市长与副市长工作协作", "overlap_org": "保山市人民政府", "overlap_period": ""},
    # 左广 <-> 龚翠莲: 市长与副市长
    {"person_a": 2, "person_b": 9, "type": "领导与被领导", "context": "市长与副市长工作协作", "overlap_org": "保山市人民政府", "overlap_period": ""},
    # 左广 <-> 张志红: 市长与秘书长
    {"person_a": 2, "person_b": 10, "type": "领导与被领导", "context": "市长与市政府秘书长工作协作", "overlap_org": "保山市人民政府办公室", "overlap_period": ""},
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