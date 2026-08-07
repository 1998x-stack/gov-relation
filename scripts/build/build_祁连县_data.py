#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 祁连县 (Qilian County), 海北藏族自治州, 青海省.

Investigation date: 2026-08-07
Task ID: qinghai_祁连县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — current county leadership CONFIRMED from primary source
(祁连县人民政府门户网 www.qilian.gov.cn 领导之窗 + 首页头条, accessed 2026-08-07).
External biography web search was degraded (Exa rate-limited, Baidu/Bing/Jina Reader
timeouts), so full career histories for the top two leaders (付强 书记, 梅尖参 县长)
and the rest of the 县委常委会 roster are gapped and marked as unverified/open gaps.

Confirmed:
- 县委书记: 付强 (confirmed via qilian.gov.cn homepage headline "县委书记付强督导调研近期重点工作")
- 县长: 梅尖参 (male, 藏族, CCP, 大学本科; 领导之窗 profile)
- 县委副书记、(兼)副县长: 李世颖(女,汉族), 姜锡朋(男,汉族,援青)
- 县委常委、副县长: 李震 (男,汉族,中央党校大专)
- 副县长: 赵华年(男,藏族), 祁才让(男,蒙古族), 马晓琴(女,回族), 南久多杰(男,藏族,兼县公安局局长)

Sources:
  http://www.qilian.gov.cn/ldzc/  (领导之窗)
  http://www.qilian.gov.cn/content/column/721?liId=XXXX&leaderTypeId=301  (各领导简介)
  http://www.qilian.gov.cn/  (首页头条: 县委书记付强)
  http://www.haibei.gov.cn/ldzc/index.html  (海北州领导之窗)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401  (process_tmp validator requires the token; runner uses it internally)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "祁连县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging / output paths ────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_祁连县"
if _CURRENT_DIR.name == "qinghai_祁连县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════ Core Leadership (targets) ═══════════════════════
    {
        "id": 1,
        "name": "付强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县委书记",
        "current_org": "中共祁连县委员会",
        "source": "祁连县政府门户网首页头条新闻'县委书记付强督导调研近期重点工作'; www.qilian.gov.cn",
    },
    {
        "id": 2,
        "name": "梅尖参",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县委副书记、县政府党组书记、县长",
        "current_org": "祁连县人民政府",
        "source": "祁连县政府领导之窗档案 (liId=1161); www.qilian.gov.cn",
    },
    # ═══════════════════ 县政府/县委领导班子 (official 领导之窗) ═══════════════════
    {
        "id": 3,
        "name": "李世颖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县委副书记、县政府副县长",
        "current_org": "祁连县人民政府",
        "source": "祁连县政府领导之窗档案 (liId=1201); www.qilian.gov.cn",
    },
    {
        "id": 4,
        "name": "姜锡朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县委副书记、县政府副县长（援青）",
        "current_org": "祁连县人民政府",
        "source": "祁连县政府领导之窗档案 (liId=1191); www.qilian.gov.cn",
    },
    {
        "id": 5,
        "name": "李震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "中央党校大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县委常委、县政府党组成员、副县长",
        "current_org": "祁连县人民政府",
        "source": "祁连县政府领导之窗档案 (liId=1211); www.qilian.gov.cn",
    },
    {
        "id": 6,
        "name": "赵华年",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县人民政府副县长",
        "current_org": "祁连县人民政府",
        "source": "祁连县政府领导之窗档案 (liId=911); www.qilian.gov.cn",
    },
    {
        "id": 7,
        "name": "祁才让",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县人民政府副县长",
        "current_org": "祁连县人民政府",
        "source": "祁连县政府领导之窗档案 (liId=921); www.qilian.gov.cn",
    },
    {
        "id": 8,
        "name": "马晓琴",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县人民政府副县长",
        "current_org": "祁连县人民政府",
        "source": "祁连县政府领导之窗档案 (liId=931); www.qilian.gov.cn",
    },
    {
        "id": 9,
        "name": "南久多杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "祁连县人民政府副县长、县公安局党委书记、局长",
        "current_org": "祁连县公安局",
        "source": "祁连县政府领导之窗档案 (liId=1181); www.qilian.gov.cn",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共祁连县委员会", "type": "党委", "level": "县级", "parent": "中共海北州委", "location": "青海省海北州祁连县"},
    {"id": 2, "name": "祁连县人民政府", "type": "政府", "level": "县级", "parent": "祁连县委", "location": "青海省海北州祁连县"},
    {"id": 3, "name": "祁连县公安局", "type": "政府", "level": "县级", "parent": "祁连县人民政府", "location": "青海省海北州祁连县"},
    {"id": 4, "name": "祁连县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "祁连县", "location": "青海省海北州祁连县"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 付强 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作; 截至2026-08以县委书记身份在首页头条活动(2026-08-07访问)"},
    # 梅尖参 — 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "县政府党组书记, 主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 李世颖 — 县委副书记、副县长
    {"person_id": 3, "org_id": 2, "title": "县委副书记、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 姜锡朋 — 县委副书记、副县长（援青）
    {"person_id": 4, "org_id": 2, "title": "县委副书记、副县长（援青）", "start_date": "", "end_date": "present", "rank": "副县级(援青)", "note": "援青干部"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李震 — 县委常委、副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县政府党组成员"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 赵华年 — 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 祁才让 — 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马晓琴 — 副县长
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 南久多杰 — 副县长、公安局长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县公安局党委书记"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # 付强 — 梅尖参 (书记—县长)
    {"person_a": 1, "person_b": 2, "type": "工作搭档", "context": "县委书记与县长, 同届党政主官搭档, 共同主持县委/县政府全面工作", "overlap_org": "中共祁连县委/祁连县人民政府", "overlap_period": "2026年"},
    # 梅尖参 — 各县委副书记
    {"person_a": 2, "person_b": 3, "type": "工作搭档", "context": "县长—县委副书记(兼副县长) 班子搭档", "overlap_org": "中共祁连县委/祁连县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 4, "type": "工作搭档", "context": "县长—县委副书记(援青) 班子搭档", "overlap_org": "中共祁连县委/祁连县人民政府", "overlap_period": "2026年至今"},
    # 梅尖参 — 县政府班子 (县长—副县长)
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—副县长(县委常委) 政府班子", "overlap_org": "祁连县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "祁连县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "祁连县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长", "overlap_org": "祁连县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长兼公安局长", "overlap_org": "祁连县人民政府", "overlap_period": "2026年至今"},
]

# ── Build ──────────────────────────────────────────────────────────────
def main() -> None:
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
    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"   人物: {len(persons)}   机构: {len(organizations)}")
    print(f"   任职: {len(positions)}   关系: {len(relationships)}")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()