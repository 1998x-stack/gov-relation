#!/usr/bin/env python3
"""Build script for 碧江区 (Bijiang District, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 贵州省
Parent City: 铜仁市
Targets: 区委书记 & 区长

Current officeholders (confirmed from official website):
  - 刘祖辉: 碧江区委书记 (as of 2026-07-23)
  - 张勇: 碧江区区长 (as of 2026-07-23)

Research Note:
  Web access was degraded during this investigation:
  - Exa search: rate-limited after the first query
  - Baidu: 403/captcha blocked
  - Jina Reader: timeouts on non-Google URLs
  - Official site www.bjq.gov.cn: accessible for homepage/headlines only; leadership
    detail pages and article pages return 404 via direct GET (likely JS-rendered routing)
  - Tongren city portal (tongren.gov.cn): accessible

  Core leaders are confirmed from the official site headline/news listings.
  Biographical details (birth year, birthplace, education, prior roles) for both
  figures are unverified due to the above access limitations and are marked as gaps.

Sources:
  - www.bjq.gov.cn (official district government website, homepage and news listings)
  - News items from bjq.gov.cn showing 刘祖辉 as 区委书记 and 张勇 as 区长
"""

import json
import os
import sys
import sqlite3
from datetime import datetime

# Ensure gov_relation package is importable
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build

# ── Paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "guizhou_碧江区"
AS_OF = "2026-07-23"
DB_PATH = os.path.join(SCRIPT_DIR, "碧江区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "碧江区_network.gexf")
PERSONS_DIR = os.path.join(SCRIPT_DIR, "persons")

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ═══════════════════════════════════════════════
    # 1. Party Secretary (区委书记) — 刘祖辉
    # ═══════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘祖辉",
        "gender": "男",
        "ethnicity": "",            # not confirmed from available sources
        "birth": "",                # gap — birth year not found
        "birthplace": "",           # gap
        "native_place": "",         # gap
        "education": "",            # gap
        "party_join": "中共党员",
        "work_start": "",           # gap — work start year not found
        "current_post": "碧江区委书记",
        "current_org": "中共铜仁市碧江区委员会",
        "source": (
            "https://www.bjq.gov.cn/ (official website, multiple news items "
            "2026-07-02 through 2026-07-15 showing 刘祖辉 presiding as 区委书记)"
        ),
        "notes": (
            "刘祖辉，现任中共铜仁市碧江区委书记。2026年7月主持全区群众身边不正之风和"
            "腐败问题集中整治工作领导小组会议、为村（社区）党组织书记培训班授课、"
            "出席碧江区·铜仁高新区'七一'表彰大会、与张勇共同开展'七一'走访慰问。"
            "此前任职履历待查。"
        ),
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 2. District Mayor (区长) — 张勇
    # ═══════════════════════════════════════════════
    {
        "id": 2,
        "name": "张勇",
        "gender": "男",
        "ethnicity": "",            # gap
        "birth": "",                # gap
        "birthplace": "",           # gap
        "native_place": "",         # gap
        "education": "",            # gap
        "party_join": "中共党员",
        "work_start": "",           # gap
        "current_post": "碧江区区长",
        "current_org": "碧江区人民政府",
        "source": (
            "https://www.bjq.gov.cn/ (official website, multiple news items "
            "2026-07-03 through 2026-07-23 showing 张勇 presiding as 区长)"
        ),
        "notes": (
            "张勇，现任铜仁市碧江区区长。2026年7月主持召开区政府常务会议、"
            "区政府党组（扩大）会议、讲授树立和践行正确政绩观学习教育专题党课、"
            "与刘祖辉共同开展'七一'走访慰问。此前任职履历待查。"
        ),
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 3. Deputy Party Secretary (区委副书记) — gap
    # ═══════════════════════════════════════════════
    {
        "id": 3,
        "name": "【待查】碧江区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记（待查）",
        "current_org": "中共铜仁市碧江区委员会",
        "source": "",
        "notes": "区委副书记身份待确认。公开资料未明确标注。",
        "confidence": "unverified"
    },
    # ═══════════════════════════════════════════════
    # 4. Discipline Inspection Secretary (纪委书记) — gap
    # ═══════════════════════════════════════════════
    {
        "id": 4,
        "name": "【待查】碧江区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区纪委书记、监委主任（待查）",
        "current_org": "中共铜仁市碧江区纪律检查委员会",
        "source": "",
        "notes": "区纪委书记身份待确认。公开资料未明确标注。",
        "confidence": "unverified"
    },
    # ═══════════════════════════════════════════════
    # 5. Organization Department Head (组织部部长) — gap
    # ═══════════════════════════════════════════════
    {
        "id": 5,
        "name": "【待查】碧江区委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委组织部部长（待查）",
        "current_org": "中共铜仁市碧江区委组织部",
        "source": "",
        "notes": "区委组织部部长身份待确认。",
        "confidence": "unverified"
    },
    # ═══════════════════════════════════════════════
    # 6. Executive Deputy Mayor (常务副区长) — gap
    # ═══════════════════════════════════════════════
    {
        "id": 6,
        "name": "【待查】碧江区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "碧江区委常委、常务副区长（待查）",
        "current_org": "碧江区人民政府",
        "source": "",
        "notes": "常务副区长身份待确认。",
        "confidence": "unverified"
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共铜仁市碧江区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 2,
        "name": "碧江区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 3,
        "name": "中共铜仁市碧江区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市碧江区委员会",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 4,
        "name": "中共铜仁市碧江区委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共铜仁市碧江区委员会",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 5,
        "name": "碧江区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 6,
        "name": "碧江区政协委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 7,
        "name": "碧江区人民武装部",
        "type": "党委",
        "level": "县处级",
        "parent": "铜仁军分区",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 8,
        "name": "碧江高新技术产业开发区",
        "type": "开发区",
        "level": "省级",
        "parent": "碧江区人民政府",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 9,
        "name": "中共铜仁市碧江区委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市碧江区委员会",
        "location": "贵州省铜仁市碧江区",
    },
    {
        "id": 10,
        "name": "中共铜仁市碧江区委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共铜仁市碧江区委员会",
        "location": "贵州省铜仁市碧江区",
    },
]

POSITIONS = [
    # 刘祖辉 — 区委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "碧江区委书记",
        "start_date": "",           # gap
        "end_date": "present",
        "rank": "县处级正职",
        "note": "已确认截至2026年7月在任",
    },
    # 张勇 — 区长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "碧江区区长",
        "start_date": "",           # gap
        "end_date": "present",
        "rank": "县处级正职",
        "note": "同时担任区委副书记；已确认截至2026年7月在任",
    },
    # Gap positions
    {"person_id": 3, "org_id": 1, "title": "区委副书记",        "start_date": "", "end_date": "", "rank": "县处级副职", "note": "待查"},
    {"person_id": 4, "org_id": 3, "title": "区纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "待查"},
    {"person_id": 5, "org_id": 4, "title": "区委组织部部长",    "start_date": "", "end_date": "", "rank": "县处级副职", "note": "待查"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "待查"},
]

RELATIONSHIPS = [
    # 刘祖辉 — 张勇: 区委书记/区长搭班 overlap
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长搭班关系，共同出席'七一'走访慰问（2026-07-01）、区委各类会议",
        "overlap_org": "中共铜仁市碧江区委员会／碧江区人民政府",
        "overlap_period": "2026–present",
    },
]
# fmt: on


# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="碧江区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")
