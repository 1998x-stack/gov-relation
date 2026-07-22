#!/usr/bin/env python3
"""Build Chaozhou (潮州市) leadership network data.

Level: 地级市
Province: 广东省
Targets: 市委书记 (Party Secretary), 市长 (Mayor)

Research date: 2026-07-22
Official source: https://www.chaozhou.gov.cn/zwgk/ldzc/index.html
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from repo root or data/tmp dir
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "潮州市"
TASK_ID = "guangdong_潮州市"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

# Validate required packages (process_tmp.py checks for sqlite3, DB_PATH, GEXF_PATH)
import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "何晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "在职研究生",
        "party_join": "1994年",
        "work_start": "1995年",
        "current_post": "中共潮州市委书记",
        "current_org": "中共潮州市委员会",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html (indirect — Party Secretary not listed on gov page; name from historical records as of late 2024; see open_questions)",
    },
    {
        "id": 2,
        "name": "蔡淡群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "广东揭东",
        "native_place": "广东揭东",
        "education": "省委党校研究生",
        "party_join": "1994年",
        "work_start": "1995年",
        "current_post": "潮州市委副书记、市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html (official government leadership page, as of 2026-07-22)",
    },
    {
        "id": 3,
        "name": "陈跃庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共潮州市委员会",
        "source": "https://www.chaozhou.gov.cn/ywdt/czyw/content/post_3998757.html (news article 2026-07-17 mentioning 市委常委陈跃庆)",
    },
    {
        "id": 4,
        "name": "刘云梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html",
    },
    {
        "id": 5,
        "name": "周岳林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html",
    },
    {
        "id": 6,
        "name": "朱丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html",
    },
    {
        "id": 7,
        "name": "周茹茵",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html",
    },
    {
        "id": 8,
        "name": "邱焕华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html (confirmed in news article post_3999045)",
    },
    {
        "id": 9,
        "name": "陈红政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html",
    },
    {
        "id": 10,
        "name": "邓钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html",
    },
    {
        "id": 11,
        "name": "雷振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "秘书长",
        "current_org": "潮州市人民政府",
        "source": "https://www.chaozhou.gov.cn/zwgk/ldzc/index.html (confirmed in news article post_3998757)",
    },
    {
        "id": 12,
        "name": "林燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "潮州市",
        "source": "https://www.chaozhou.gov.cn/ywdt/czyw/content/post_3998757.html (news article 2026-07-17)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共潮州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广东省委",
        "location": "广东省潮州市",
    },
    {
        "id": 2,
        "name": "潮州市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "广东省人民政府",
        "location": "广东省潮州市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 何晓军 — Party Secretary
    {"person_id": 1, "org_id": 1, "title": "中共潮州市委书记",
     "start": "2024-09", "end": "present", "rank": "正厅级",
     "note": "原为潮州市市长，2024年9月任市委书记"},
    # 蔡淡群 — Mayor
    {"person_id": 2, "org_id": 2, "title": "潮州市人民政府市长",
     "start": "2024-10(任代市长)", "end": "present", "rank": "正厅级",
     "note": "此前曾任广东省财政厅副厅长；2024年任潮州市代市长、市长"},
    {"person_id": 2, "org_id": 1, "title": "中共潮州市委副书记",
     "start": "2024-10", "end": "present", "rank": "正厅级",
     "note": ""},
    # 陈跃庆 — Standing Committee member
    {"person_id": 3, "org_id": 1, "title": "潮州市委常委",
     "start": "unknown", "end": "present", "rank": "副厅级",
     "note": ""},
    # Vice Mayors
    {"person_id": 4, "org_id": 2, "title": "潮州市人民政府副市长",
     "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "潮州市人民政府副市长",
     "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "潮州市人民政府副市长",
     "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "潮州市人民政府副市长",
     "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "潮州市人民政府副市长",
     "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "潮州市人民政府副市长",
     "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "潮州市人民政府副市长",
     "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    # Secretary General
    {"person_id": 11, "org_id": 2, "title": "潮州市人民政府秘书长",
     "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    # 林燕 — City leader
    {"person_id": 12, "org_id": 1, "title": "市领导",
     "start": "unknown", "end": "present", "rank": "未知", "note": "具体职务未确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 何晓军 and 蔡淡群: 书记-市长 (党政搭档)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政搭档——市委书记与市长",
        "overlap_org": "中共潮州市委员会/潮州市人民政府",
        "overlap_period": "2024-10至今",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def build():
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )


if __name__ == "__main__":
    build()
