#!/usr/bin/env python3
"""Build script for 玉屏侗族自治县 (Yuping Dong Autonomous County, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Current officeholders (confirmed from official website www.yuping.gov.cn):
  - 杨启明: 市委常委、县委书记、大龙开发区党工委书记 (as of 2026-07-23)
  - 田兴国: 县委副书记、县人民政府县长 (as of 2026-07-23)

Research Note:
  Web access was partially degraded:
  - Exa search: rate-limited after first query
  - Baidu: 403/captcha blocked
  - Official site www.yuping.gov.cn: accessible for news and leadership activity pages
  - Tongren city portal (trs.gov.cn): accessible

  Core leaders are confirmed from the official website news listings (领导活动).
  Biographical details (birth year, birthplace, education, prior roles) for both
  figures are unverified due to access limitations and are marked as gaps.

Sources:
  - www.yuping.gov.cn (official county government website, leadership activity pages)
  - News items from yuping.gov.cn showing 杨启明 as 县委书记 and 田兴国 as 县长
  - July 2, 2026: "玉屏侗族自治县·大龙开发区'两优一先'表彰大会" naming both leaders
  - June 30, 2026: "杨启明田兴国开展'七一'走访慰问活动"
  - June 26, 2026: "杨启明在玉屏第一中学讲授思想政治理论课"
  - June 24, 2026: "田兴国到玉屏综合高级中学讲授思政课"
  - June 15, 2026: "杨启明率队赴广东江苏开展招商考察"
  - July 21, 2026: "杨启明调研康养旅居并督导防溺水工作"
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
TASK_ID = "guizhou_玉屏侗族自治县"
AS_OF = "2026-07-23"
DB_PATH = os.path.join(SCRIPT_DIR, "玉屏侗族自治县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "玉屏侗族自治县_network.gexf")
PERSONS_DIR = os.path.join(SCRIPT_DIR, "persons")

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ═══════════════════════════════════════════════
    # 1. Party Secretary (县委书记) — 杨启明
    # ═══════════════════════════════════════════════
    {
        "id": 1,
        "name": "杨启明",
        "gender": "男",
        "ethnicity": "",            # not confirmed from available sources
        "birth": "",                # gap — birth year not found
        "birthplace": "",           # gap
        "native_place": "",         # gap
        "education": "",            # gap
        "party_join": "中共党员",
        "work_start": "",           # gap — work start year not found
        "current_post": "市委常委、县委书记、大龙开发区党工委书记",
        "current_org": "中共铜仁市委员会／中共玉屏侗族自治县委员会／大龙开发区党工委",
        "source": (
            "https://www.yuping.gov.cn/ (official website, multiple news items "
            "2026-06-15 through 2026-07-21 showing 杨启明 presiding as 市委常委、县委书记、大龙开发区党工委书记)"
        ),
        "notes": (
            "杨启明，现任中共铜仁市委常委、玉屏侗族自治县委书记、大龙开发区党工委书记。"
            "2026年7月主持县·大龙开发区'两优一先'表彰大会、调研康养旅居并督导防溺水工作；"
            "2026年6月与田兴国共同开展'七一'走访慰问、到玉屏第一中学讲授思政课、"
            "率队赴广东江苏开展招商考察。此前任职履历待查。"
        ),
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 2. County Mayor (县长) — 田兴国
    # ═══════════════════════════════════════════════
    {
        "id": 2,
        "name": "田兴国",
        "gender": "男",
        "ethnicity": "",            # gap
        "birth": "",                # gap
        "birthplace": "",           # gap
        "native_place": "",         # gap
        "education": "",            # gap
        "party_join": "中共党员",
        "work_start": "",           # gap
        "current_post": "县委副书记、县人民政府县长",
        "current_org": "玉屏侗族自治县人民政府",
        "source": (
            "https://www.yuping.gov.cn/ (official website, multiple news items "
            "2026-06-24 through 2026-07-02 showing 田兴国 presiding as 县长)"
        ),
        "notes": (
            "田兴国，现任玉屏侗族自治县委副书记、县人民政府县长。"
            "2026年7月主持县·大龙开发区'两优一先'表彰大会；"
            "2026年6月与杨启明共同开展'七一'走访慰问、到玉屏综合高级中学讲授思政课。"
            "此前任职履历待查。"
        ),
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 3. 县人大常委会主任 — 吴继滔
    # ═══════════════════════════════════════════════
    {
        "id": 3,
        "name": "吴继滔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "玉屏侗族自治县人民代表大会常务委员会",
        "source": (
            "https://www.yuping.gov.cn/ (2026-07-02 '两优一先'表彰大会报道)"
        ),
        "notes": "从县·大龙开发区'两优一先'表彰大会报道中确认身份。",
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 4. 县政协主席 — 陈飞
    # ═══════════════════════════════════════════════
    {
        "id": 4,
        "name": "陈飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协玉屏侗族自治县委员会",
        "source": (
            "https://www.yuping.gov.cn/ (2026-07-02 '两优一先'表彰大会报道)"
        ),
        "notes": "从县·大龙开发区'两优一先'表彰大会报道中确认身份。",
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 5. 县委常委、县委组织部部长 — 冉雪芹
    # ═══════════════════════════════════════════════
    {
        "id": 5,
        "name": "冉雪芹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委组织部部长",
        "current_org": "中共玉屏侗族自治县委组织部",
        "source": (
            "https://www.yuping.gov.cn/ (2026-07-02 '两优一先'表彰大会报道)"
        ),
        "notes": "从县·大龙开发区'两优一先'表彰大会报道中确认，会上宣读表彰决定。",
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 6. 县委常委、县委办公室主任 — 张云
    # ═══════════════════════════════════════════════
    {
        "id": 6,
        "name": "张云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共玉屏侗族自治县委办公室",
        "source": (
            "https://www.yuping.gov.cn/ (2026-06-26 思政课报道, 2026-06-30 七一慰问报道)"
        ),
        "notes": "从杨启明思政课报道和七一慰问报道中确认身份。",
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════
    # 7. 县领导 — 吴红春（待确认具体职务）
    # ═══════════════════════════════════════════════
    {
        "id": 7,
        "name": "吴红春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（具体职务待确认）",
        "current_org": "玉屏侗族自治县",
        "source": (
            "https://www.yuping.gov.cn/ (2026-06-15 招商考察报道)"
        ),
        "notes": "随杨启明赴广东江苏招商考察。具体职务待查。",
        "confidence": "plausible"
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共玉屏侗族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市玉屏侗族自治县",
    },
    {
        "id": 2,
        "name": "玉屏侗族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市玉屏侗族自治县",
    },
    {
        "id": 3,
        "name": "玉屏侗族自治县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "贵州省铜仁市玉屏侗族自治县",
    },
    {
        "id": 4,
        "name": "政协玉屏侗族自治县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "贵州省铜仁市玉屏侗族自治县",
    },
    {
        "id": 5,
        "name": "中共玉屏侗族自治县委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共玉屏侗族自治县委员会",
        "location": "贵州省铜仁市玉屏侗族自治县",
    },
    {
        "id": 6,
        "name": "中共玉屏侗族自治县委办公室",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共玉屏侗族自治县委员会",
        "location": "贵州省铜仁市玉屏侗族自治县",
    },
    {
        "id": 7,
        "name": "大龙开发区党工委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市玉屏侗族自治县大龙街道",
    },
    {
        "id": 8,
        "name": "大龙开发区管委会",
        "type": "政府",
        "level": "县处级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市玉屏侗族自治县大龙街道",
    },
]

POSITIONS = [
    # 杨启明 — 市委常委、县委书记、大龙开发区党工委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "玉屏侗族自治县委书记",
        "start_date": "",           # gap
        "end_date": "present",
        "rank": "县处级正职",
        "note": "同时担任铜仁市委常委（副厅级）、大龙开发区党工委书记；已确认截至2026年7月在任",
    },
    {
        "person_id": 1,
        "org_id": 7,
        "title": "大龙开发区党工委书记",
        "start_date": "",           # gap
        "end_date": "present",
        "rank": "县处级正职",
        "note": "兼任；已确认截至2026年7月在任",
    },
    # 田兴国 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "玉屏侗族自治县县长",
        "start_date": "",           # gap
        "end_date": "present",
        "rank": "县处级正职",
        "note": "同时担任县委副书记；已确认截至2026年7月在任",
    },
    # 吴继滔 — 县人大常委会主任
    {
        "person_id": 3,
        "org_id": 3,
        "title": "县人大常委会主任",
        "start_date": "",
        "end_date": "present",
        "rank": "县处级正职",
        "note": "已确认截至2026年7月在任",
    },
    # 陈飞 — 县政协主席
    {
        "person_id": 4,
        "org_id": 4,
        "title": "县政协主席",
        "start_date": "",
        "end_date": "present",
        "rank": "县处级正职",
        "note": "已确认截至2026年7月在任",
    },
    # 冉雪芹 — 县委常委、组织部部长
    {
        "person_id": 5,
        "org_id": 5,
        "title": "县委常委、组织部部长",
        "start_date": "",
        "end_date": "present",
        "rank": "县处级副职",
        "note": "已确认截至2026年7月在任",
    },
    # 张云 — 县委常委、县委办公室主任
    {
        "person_id": 6,
        "org_id": 6,
        "title": "县委常委、县委办公室主任",
        "start_date": "",
        "end_date": "present",
        "rank": "县处级副职",
        "note": "已确认截至2026年7月在任",
    },
    # 吴红春 — 县领导
    {
        "person_id": 7,
        "org_id": 2,
        "title": "县领导（具体职务待确认）",
        "start_date": "",
        "end_date": "",
        "rank": "",
        "note": "随杨启明赴广东江苏招商考察（2026年6月）。具体职务待查。",
    },
]

RELATIONSHIPS = [
    # 杨启明 — 田兴国: 县委书记/县长搭班 overlap
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长搭班关系，共同出席'七一'走访慰问（2026-06-30）、县·大龙开发区'两优一先'表彰大会（2026-07-01）",
        "overlap_org": "中共玉屏侗族自治县委员会／玉屏侗族自治县人民政府",
        "overlap_period": "–present",
    },
    # 杨启明 — 张云: 上下级关系（县委办）
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "杨启明作为县委书记，张云作为县委办公室主任，陪同出席思政课讲授等活动",
        "overlap_org": "中共玉屏侗族自治县委员会",
        "overlap_period": "–present",
    },
]
# fmt: on


# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="玉屏侗族自治县",
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
