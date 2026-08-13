#!/usr/bin/env python3
import sqlite3  # noqa — used by gov_relation.runner via import
"""Build SQLite database, GEXF graph, and person JSONs for 定边县, 陕西省榆林市.

Investigation date: 2026-07-25
Task ID: shaanxi_定边县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.dingbian.gov.cn — 定边县人民政府官方网站 (primary, accessed July 2026)
  - 定边县政府网站领导之窗: /zfxxgk/fdzdgknr/ldzc/ (政府领导)
  - 定边县新闻动态: /xwdt/dbyw/ (确认李胜元为县委书记, 2026-07-21)
  - 定边县人事任免: /zfxxgk/fdzdgknr/rsrm/

Confidence notes:
  - 李胜元 (县委书记): confirmed via 2026-07-21 news article "李胜元到贺圈镇调研"
  - 郝正军 (县长): confirmed via official 领导之窗 page
  - 党玉飞 (常务副县长): confirmed via official 领导之窗 page
  - 杨红梅, 沈力, 周增余, 吴斌, 黄国栋, 高燕, 王剑, 罗采刚: confirmed via official 领导之窗
  - 刘云霞: confirmed via 2026-07-24 news as 县政协主席
  - Full career histories: NOT available — official site only shows current position summaries
  - Predecessor info: 姬世平 (former 县委书记, mentioned in 2023 article), details unverified
  - Baidu Baike: captcha-blocked, not accessible
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "定边县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_定边县"
if _CURRENT_DIR.name == "shaanxi_定边县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=县委书记, 2=县长, 3-11=县委常委/政府领导, 12=政协主席, 13+=predecessor/other

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 县委书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1, "name": "李胜元", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记", "current_org": "中共定边县委员会",
        "source": "https://www.dingbian.gov.cn/xwdt/dbyw/202607/t20260721_2115905.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2, "name": "郝正军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 3, "name": "党玉飞", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、常务副县长", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 4, "name": "杨红梅", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 5, "name": "沈力", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、宣传部部长", "current_org": "中共定边县委宣传部",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 6, "name": "周增余", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长（挂职）", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 7, "name": "吴斌", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长（挂职）", "current_org": "定边县人民政府",
        "note": "同时任宝应县政府党组成员、副县长（苏陕协作挂职）",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 8, "name": "黄国栋", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长（正县级）", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 9, "name": "高燕", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 10, "name": "王剑", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长、县公安局局长", "current_org": "定边县公安局",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 11, "name": "罗采刚", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 调研员
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12, "name": "王国伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府二级调研员", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    {
        "id": 13, "name": "高俊岩", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府四级调研员", "current_org": "定边县人民政府",
        "source": "https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/ldzc/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14, "name": "刘云霞", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席", "current_org": "政协定边县委员会",
        "source": "https://www.dingbian.gov.cn/xwdt/dbyw/202607/t20260724_2116800.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任领导 (predecessors — partial/unverified)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15, "name": "姬世平", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（前任县委书记）", "current_org": "中共定边县委员会（前任）",
        "note": "2023年6月仍以县委书记身份活动，推测2026年前已调离",
        "source": "https://www.dingbian.gov.cn/xwdt/dbyw/202306/t20230626_1832556.html"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共定边县委员会", "type": "党委", "level": "县处级", "location": "陕西省榆林市定边县"},
    {"id": 2, "name": "定边县人民政府", "type": "政府", "level": "县处级", "location": "陕西省榆林市定边县"},
    {"id": 3, "name": "中共定边县委宣传部", "type": "党委", "level": "乡科级", "location": "陕西省榆林市定边县"},
    {"id": 4, "name": "定边县公安局", "type": "政府", "level": "乡科级", "location": "陕西省榆林市定边县"},
    {"id": 5, "name": "政协定边县委员会", "type": "政协", "level": "县处级", "location": "陕西省榆林市定边县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李胜元
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县处级", "note": "confirmed via 2026-07-21 news"},
    # 郝正军
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    # 党玉飞
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 杨红梅
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 沈力
    {"person_id": 5, "org_id": 1, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "宣传部部长", "start": "", "end": "present", "rank": "乡科级正职", "note": ""},
    # 周增余
    {"person_id": 6, "org_id": 1, "title": "县委常委（挂职）", "start": "", "end": "present", "rank": "副县处级", "note": "挂职"},
    {"person_id": 6, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县处级", "note": "挂职"},
    # 吴斌
    {"person_id": 7, "org_id": 1, "title": "县委常委（挂职）", "start": "", "end": "present", "rank": "副县处级", "note": "苏陕协作挂职，同时任宝应县副县长"},
    {"person_id": 7, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县处级", "note": "挂职"},
    # 黄国栋
    {"person_id": 8, "org_id": 2, "title": "副县长（正县级）", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    # 高燕
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 王剑
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "县公安局局长", "start": "", "end": "present", "rank": "乡科级正职", "note": ""},
    # 罗采刚
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 王国伟
    {"person_id": 12, "org_id": 2, "title": "二级调研员", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    # 高俊岩
    {"person_id": 13, "org_id": 2, "title": "四级调研员", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 刘云霞
    {"person_id": 14, "org_id": 5, "title": "县政协主席", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    # 姬世平（前任）
    {"person_id": 15, "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "", "rank": "正县处级", "note": "2023年6月仍任县委书记，已调离"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# Strong edges: same organization, overlapping time
relationships = [
    # 李胜元 ↔ 郝正军 (党政一把手)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政搭档", "overlap_org": "中共定边县委员会/定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    # 党玉飞 (常务副县长 → 县长助理)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与常务副县长工作搭档", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    # 县委常委间的同僚关系
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与常务副县长同届县委常委会", "overlap_org": "中共定边县委员会", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与副县长同届县委常委会", "overlap_org": "中共定边县委员会", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与宣传部部长同届县委常委会", "overlap_org": "中共定边县委员会", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    # 县政府班子内部关系
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与副县长同届县政府班子", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "县长与副县长（正县级）同届县政府班子", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "县长与副县长同届县政府班子", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "县长与副县长兼公安局长同届县政府班子", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "县长与副县长同届县政府班子", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    # 挂职副县长关系
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与挂职副县长工作关系", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "medium", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "县长与挂职副县长（苏陕协作）工作关系", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "medium", "confidence": "confirmed"},

    # 王剑 → 公安系统
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate",
     "context": "公安局长向县长汇报工作", "overlap_org": "定边县人民政府", "overlap_period": "2026",
     "strength": "strong", "confidence": "confirmed"},

    # 刘云霞（政协主席）
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "县委书记与政协主席党政工作联系", "overlap_org": "定边县", "overlap_period": "2026",
     "strength": "medium", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "县长与政协主席工作联系", "overlap_org": "定边县", "overlap_period": "2026",
     "strength": "medium", "confidence": "confirmed"},

    # 前任-继任关系
    {"person_a": 15, "person_b": 1, "type": "predecessor_successor",
     "context": "姬世平为前任县委书记，李胜元为现任（时序关系，非直接交接确认）",
     "overlap_org": "中共定边县委员会", "overlap_period": "2023-2026",
     "strength": "medium", "confidence": "plausible"},
]

# ── Build ────────────────────────────────────────────────────────────────────
def build():
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    print(f"\nDone. Database: {DB_PATH}")
    print(f"Done. GEXF:     {GEXF_PATH}")

if __name__ == "__main__":
    build()
