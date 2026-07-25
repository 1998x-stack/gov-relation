#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宜君县, 铜川市, 陕西省.

Level: 县
Province: 陕西省
Parent city: 铜川市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shaanxi_宜君县

Research date: 2026-07-25
Official source: https://www.yijun.gov.cn/ (宜君县人民政府)

Current status (as of 2026-07-25):
- 县委书记: 左小军 (confirmed via official 领导之窗 page)
- 县长: 毛建荣 (confirmed via official 领导之窗 page)

县委领导:
- 书记: 左小军
- 副书记: 毛建荣, 尚东伟
- 常委: 郗晓红, 李保民, 张闯, 何军锋, 王宾宾, 陈伟, 王小会, 顾斌

县政府领导:
- 县长: 毛建荣
- 常务副县长: 王宾宾
- 副县长: 陈伟, 顾斌, 尚晓军, 马国宏, 刘彬

Confidence notes:
  Web search tools (Exa) were rate-limited during research. However, the primary
  government site https://www.yijun.gov.cn/ was accessible and provided the full
  leadership roster and biographies for all core figures. The official leadership
  page (领导之窗) at https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328
  and businessType=330 were directly fetched and confirmed.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "宜君县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 左小军 — 县委书记
    {
        "id": 1,
        "name": "左小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "2001年6月加入中国共产党",
        "work_start": "1999年12月",
        "current_post": "中共宜君县委书记",
        "current_org": "中共宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328 — 官方领导之窗",
    },
    # 2. 毛建荣 — 县长
    {
        "id": 2,
        "name": "毛建荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "陕西咸阳",
        "education": "研究生学历",
        "party_join": "2002年12月加入中国共产党",
        "work_start": "2002年7月",
        "current_post": "宜君县人民政府县长",
        "current_org": "宜君县人民政府",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=330 — 官方领导之窗",
    },
    # ════════════════════════════════════════
    # Leadership Team
    # ════════════════════════════════════════
    # 3. 尚东伟 — 县委副书记
    {
        "id": 3,
        "name": "尚东伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜君县委副书记",
        "current_org": "中共宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328 — 县委领导名单",
    },
    # 4. 郗晓红 — 县委常委
    {
        "id": 4,
        "name": "郗晓红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委",
        "current_org": "中共宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328 — 县委领导名单",
    },
    # 5. 李保民 — 县委常委
    {
        "id": 5,
        "name": "李保民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委",
        "current_org": "中共宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328 — 县委领导名单",
    },
    # 6. 张闯 — 县委常委
    {
        "id": 6,
        "name": "张闯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委",
        "current_org": "中共宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328 — 县委领导名单",
    },
    # 7. 何军锋 — 县委常委
    {
        "id": 7,
        "name": "何军锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委",
        "current_org": "中共宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328 — 县委领导名单",
    },
    # 8. 王宾宾 — 县委常委、常务副县长
    {
        "id": 8,
        "name": "王宾宾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜君县委常委、常务副县长",
        "current_org": "宜君县人民政府",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328/330",
    },
    # 9. 陈伟 — 县委常委、副县长
    {
        "id": 9,
        "name": "陈伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜君县委常委、副县长",
        "current_org": "宜君县人民政府",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328/330",
    },
    # 10. 王小会 — 县委常委
    {
        "id": 10,
        "name": "王小会",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委",
        "current_org": "中共宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328 — 县委领导名单",
    },
    # 11. 顾斌 — 县委常委、副县长
    {
        "id": 11,
        "name": "顾斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜君县委常委、副县长",
        "current_org": "宜君县人民政府",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328/330",
    },
    # 12. 尚晓军 — 副县长
    {
        "id": 12,
        "name": "尚晓军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜君县副县长",
        "current_org": "宜君县人民政府",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=330 — 县政府领导名单",
    },
    # 13. 马国宏 — 副县长
    {
        "id": 13,
        "name": "马国宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜君县副县长",
        "current_org": "宜君县人民政府",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=330 — 县政府领导名单",
    },
    # 14. 刘彬 — 副县长
    {
        "id": 14,
        "name": "刘彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜君县副县长",
        "current_org": "宜君县人民政府",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=330 — 县政府领导名单",
    },
    # 15. 王万学 — 县人大常委会主任
    {
        "id": 15,
        "name": "王万学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "1993年5月入党",
        "work_start": "1989年7月",
        "current_post": "宜君县人大常委会主任",
        "current_org": "宜君县人民代表大会常务委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=329 — 官方领导之窗",
    },
    # 16. 樊斌 — 县政协主席
    {
        "id": 16,
        "name": "樊斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年12月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "1998年8月入党",
        "work_start": "1993年7月",
        "current_post": "宜君县政协主席",
        "current_org": "中国人民政治协商会议宜君县委员会",
        "source": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=331 — 官方领导之窗",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共宜君县委员会", "type": "党委", "level": "县处级", "parent": "中共铜川市委", "location": "陕西省铜川市宜君县"},
    {"id": 2, "name": "宜君县人民政府", "type": "政府", "level": "县处级", "parent": "铜川市人民政府", "location": "陕西省铜川市宜君县"},
    {"id": 3, "name": "宜君县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "陕西省铜川市宜君县"},
    {"id": 4, "name": "中国人民政治协商会议宜君县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "陕西省铜川市宜君县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 左小军 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "宜君县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "主持县委全面工作"},
    # 毛建荣 — 县长
    {"person_id": 2, "org_id": 2, "title": "宜君县人民政府县长", "start": "", "end": "present", "rank": "县处级正职", "note": "领导县政府全面工作，分管县财政局、审计局"},
    {"person_id": 2, "org_id": 1, "title": "宜君县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "兼任县委副书记"},
    # 尚东伟 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "宜君县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 郗晓红 — 县委常委
    {"person_id": 4, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 李保民 — 县委常委
    {"person_id": 5, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张闯 — 县委常委
    {"person_id": 6, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 何军锋 — 县委常委
    {"person_id": 7, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 王宾宾 — 县委常委、常务副县长
    {"person_id": 8, "org_id": 2, "title": "宜君县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 陈伟 — 县委常委、副县长
    {"person_id": 9, "org_id": 2, "title": "宜君县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 王小会 — 县委常委
    {"person_id": 10, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 顾斌 — 县委常委、副县长
    {"person_id": 11, "org_id": 2, "title": "宜君县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "宜阳县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 尚晓军 — 副县长
    {"person_id": 12, "org_id": 2, "title": "宜君县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 马国宏 — 副县长
    {"person_id": 13, "org_id": 2, "title": "宜君县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 刘彬 — 副县长
    {"person_id": 14, "org_id": 2, "title": "宜君县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 王万学 — 县人大常委会主任
    {"person_id": 15, "org_id": 3, "title": "宜君县人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": "主持县人大常委会全盘工作"},
    # 樊斌 — 县政协主席
    {"person_id": 16, "org_id": 4, "title": "宜君县政协主席", "start": "", "end": "present", "rank": "县处级正职", "note": "主持县政协全盘工作"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 左小军 ↔ 毛建荣 (core leadership pair — party secretary and county magistrate)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长党政主要领导搭档关系，共同主持宜君县委常委会和县政府重要会议",
        "overlap_org": "中共宜君县委员会/宜君县人民政府",
        "overlap_period": "截至2026年7月",
        "confidence": "confirmed",
    },
    # 左小军 ↔ 尚东伟 (party secretary — deputy secretary)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委书记与县委副书记工作关系",
        "overlap_org": "中共宜君县委员会",
        "overlap_period": "截至2026年7月",
        "confidence": "confirmed",
    },
    # 毛建荣 ↔ 尚东伟 (county magistrate — deputy secretary)
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "县长与县委副书记同为县委领导班子成员",
        "overlap_org": "中共宜君县委员会",
        "overlap_period": "截至2026年7月",
        "confidence": "confirmed",
    },
    # 左小军 ↔ 王宾宾 (party secretary — executive deputy magistrate)
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "县委书记与常务副县长工作关系",
        "overlap_org": "中共宜君县委员会/宜君县人民政府",
        "overlap_period": "截至2026年7月",
        "confidence": "confirmed",
    },
    # 毛建荣 ↔ 王宾宾 (county magistrate — executive deputy magistrate)
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "县长与常务副县长工作关系",
        "overlap_org": "宜君县人民政府",
        "overlap_period": "截至2026年7月",
        "confidence": "confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] == pid:
            career_entries.append({
                "start": pos["start"] if pos["start"] else "unknown",
                "end": pos["end"] if pos["end"] else "unknown",
                "org": _org_name(pos["org_id"]),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "陕西省铜川市宜君县",
                "system": "party" if "县委" in pos["title"] or "书记" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": "县委书记" in pos["title"] or "县长" in pos["title"] or "主任" in pos["title"] or "主席" in pos["title"],
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })

    rels_out = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other_name = _person_name(other_id)
        rels_out.append({
            "person": other_name,
            "person_id": f"yijun_{_slugify_name(other_name)}",
            "relationship_type": r["type"],
            "strength": "strong",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r.get("confidence", "confirmed"),
            "source_ids": ["S001"],
        })

    orgs_out = []
    seen_orgs = set()
    for pos in positions:
        if pos["person_id"] == pid and pos["org_id"] not in seen_orgs:
            seen_orgs.add(pos["org_id"])
            orgs_out.append({
                "org_id": pos["org_id"],
                "name": _org_name(pos["org_id"]),
                "type": _org_type(pos["org_id"]),
                "level": "县处级",
                "location": "陕西省铜川市宜君县",
            })

    # Build career from known bio for core figures
    if person["id"] == 1:
        # 左小军 full career from official bio
        career_entries = [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市新区咸丰路街道",
                "title": "咸丰路街道党委委员、办事处农经站长",
                "level": "乡科级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "乡科级",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市新区咸丰路街道",
                "title": "咸丰路街道党委委员、办事处副主任",
                "level": "乡科级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "乡科级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市新区咸丰路街道",
                "title": "咸丰路街道党委副书记、办事处主任",
                "level": "乡科级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "乡科级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市新区正阳路街道",
                "title": "正阳路街道党委书记",
                "level": "乡科级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "乡科级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市新区管委会",
                "title": "铜川市新区管委会党工委委员、副主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "县处级副职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市住房和城乡建设局（铜川市地震局）",
                "title": "铜川市住房和城乡建设局（铜川市地震局）党组书记",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市住房和城乡建设局（铜川市地震局）",
                "title": "铜川市住房和城乡建设局（铜川市地震局）党组书记、局长",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "present",
                "org": "中共宜君县委员会",
                "title": "宜君县委书记",
                "level": "县处级",
                "location": "陕西省铜川市宜君县",
                "system": "party",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "主持县委全面工作",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ]
    elif person["id"] == 2:
        # 毛建荣 full career from official bio
        career_entries = [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "宝鸡市人民政府办公室",
                "title": "宝鸡市人民政府办公室社会科副科长",
                "level": "乡科级",
                "location": "陕西省宝鸡市",
                "system": "government",
                "rank": "乡科级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "咸阳市人民政府办公室",
                "title": "咸阳市人民政府办公室综合二科副科长",
                "level": "乡科级",
                "location": "陕西省咸阳市",
                "system": "government",
                "rank": "乡科级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "咸阳市人民政府办公室",
                "title": "咸阳市人民政府办公室综合四科科长",
                "level": "乡科级",
                "location": "陕西省咸阳市",
                "system": "government",
                "rank": "乡科级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "咸阳高新区管委会",
                "title": "咸阳高新区管委会综合办公室主任",
                "level": "县处级",
                "location": "陕西省咸阳市",
                "system": "government",
                "rank": "县处级副职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "咸阳高新区管委会",
                "title": "咸阳高新区党工委委员、管委会副主任、综合办公室主任",
                "level": "县处级",
                "location": "陕西省咸阳市",
                "system": "government",
                "rank": "县处级副职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "咸阳高新区管委会",
                "title": "咸阳高新区党工委副书记、管委会主任",
                "level": "县处级",
                "location": "陕西省咸阳市",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "中共咸阳市渭城区委",
                "title": "咸阳市渭城区委副书记",
                "level": "县处级",
                "location": "陕西省咸阳市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "present",
                "org": "宜君县人民政府",
                "title": "宜君县人民政府县长",
                "level": "县处级",
                "location": "陕西省铜川市宜君县",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "领导县政府全面工作，分管县财政局、审计局。同时兼任宜君县委副书记。",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ]
    elif person["id"] == 15:
        # 王万学 full career from official bio
        career_entries = [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市委组织部",
                "title": "党员电教中心副主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市委组织部",
                "title": "党员电教中心主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市农村党员干部现代远程教育中心",
                "title": "铜川市农村党员干部现代远程教育中心（党员电化教育中心）主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市考核办",
                "title": "铜川市考核办副主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市考核办",
                "title": "铜川市考核办常务副主任（正县）",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市人力资源和社会保障局",
                "title": "铜川市人社局党组成员、市公务员局局长",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市人力资源和社会保障局",
                "title": "铜川市人社局党组成员、市失业和农村养老保险管理中心主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市人力资源和社会保障局",
                "title": "铜川市人社局党组成员、市社会保险管理经办中心主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "present",
                "org": "宜君县人民代表大会常务委员会",
                "title": "宜君县人大常委会党组书记、主任",
                "level": "县处级",
                "location": "陕西省铜川市宜君县",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "主持县人大常委会全盘工作",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ]
    elif person["id"] == 16:
        # 樊斌 full career from official bio
        career_entries = [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市王益区委政法委",
                "title": "王益区委政法委副书记",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市王益区黄堡镇",
                "title": "黄堡镇党委副书记、镇长",
                "level": "乡科级",
                "location": "陕西省铜川市",
                "system": "government",
                "rank": "乡科级正职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市王益区委",
                "title": "王益区委创先办副主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市开发投资有限公司",
                "title": "铜川市开发投资有限公司副总经理",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "other",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "市属国有企业",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "铜川市维稳办",
                "title": "铜川市维稳办副主任",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "中共铜川市印台区委",
                "title": "印台区委常委、政法委书记",
                "level": "县处级",
                "location": "陕西省铜川市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "present",
                "org": "中国人民政治协商会议宜君县委员会",
                "title": "宜君县政协党组书记、主席",
                "level": "县处级",
                "location": "陕西省铜川市宜君县",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "主持县政协全盘工作",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ]

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "铜川市",
            "region": "宜君县",
            "job": person["current_post"],
            "task_id": "shaanxi_宜君县",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": f"yijun_{_slugify_name(person['name'])}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [
                {
                    "period": "unknown",
                    "institution": person.get("education", ""),
                    "major": "",
                    "degree": person.get("education", "") if person.get("education") else "",
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "https://www.yijun.gov.cn/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_entries if career_entries else [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级正职",
                "location": "陕西省铜川市宜君县",
                "system": "party" if "书记" in person["current_post"] or "县委" in person["current_post"] else "government",
                "rank": "县处级正职" if "书记" in person["current_post"] or "县长" in person["current_post"] or "主任" in person["current_post"] or "主席" in person["current_post"] else "县处级副职",
                "is_key_promotion": True,
                "notes": f"职务来源：宜君县人民政府官网领导之窗 https://www.yijun.gov.cn/ld_show.rt?channlId=5512",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "organizations": orgs_out,
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估 — 缺少职位具体起始时间",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "宜君县政府官网领导之窗提供了领导简历，但未展示详细工作风格信息",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断需要公开报道、讲话和政府工作报告作为依据。当前阶段无法进行此分析。",
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "memberships": len(orgs_out),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "在宜君县政府官网领导之窗页面中未发现任何廉洁风险信号。此状态不代表无问题，仅表示在调查范围内未发现问题。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "宜君县人民政府 — 领导之窗",
                "url": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=328",
                "publisher": "宜君县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "县委领导页面",
            },
            {
                "id": "S002",
                "title": "宜君县人民政府 — 县政府领导之窗",
                "url": "https://www.yijun.gov.cn/ld_show.rt?channlId=5512&businessType=330",
                "publisher": "宜君县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "县政府领导页面",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "核心人物（左小军、毛建荣）的职位起始时间、完整教育背景、更早履历缺失；其他县委常委/副县长的具体分工和完整履历信息缺失。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "左小军何时调任宜君县委书记？其前任是谁？",
                "why_it_matters": "需了解县委书记交接时间节点和前任去向",
                "suggested_queries": [
                    "左小军 宜君 任命",
                    "宜君 县委书记 任免",
                    "宜君 前任 县委书记",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "毛建荣何时调任宜君县县长？其前任是谁？",
                "why_it_matters": "需了解县长交接时间节点和前任去向",
                "suggested_queries": [
                    "毛建荣 宜君 县长 任命",
                    "宜君 县长 任免",
                    "宜君 前任县长",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "各县委常委的具体分工是什么？",
                "why_it_matters": "郗晓红、李保民、张闯、何军锋、王小会仍需确认具体分管领域（组织、纪委、政法、宣传、统战等）",
                "suggested_queries": [
                    "宜君县 领导分工",
                    "宜君县委常委 分工",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "左小军和毛建荣的完整教育背景（院校、专业）",
                "why_it_matters": "领导之窗仅列出学历层次，未注明具体院校和专业",
                "suggested_queries": [
                    "左小军 毕业",
                    "毛建荣 毕业 院校",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def _org_name(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["name"]
    return ""


def _org_type(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["type"]
    return ""


def _person_name(person_id: int) -> str:
    for p in persons:
        if p["id"] == person_id:
            return p["name"]
    return ""


def _slugify_name(name: str) -> str:
    """Create a simple slug from a Chinese name."""
    return name.replace("（", "_").replace("）", "").replace(" ", "_")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        skip_placeholders = "待确认" in p["name"]
        if skip_placeholders:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)
        name_part = _slugify_name(p["name"])
        fname = f"{TODAY}-陕西省-铜川市-{_slugify_job(p['current_post'])}-{name_part}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")


def _slugify_job(post: str) -> str:
    """Extract a short job title from a Chinese post string."""
    if "县委书记" in post:
        return "县委书记"
    if "常务副县长" in post:
        return "常务副县长"
    if "副县长" in post:
        return "副县长"
    if "县长" in post:
        return "县长"
    if "副书记" in post:
        return "县委副书记"
    if "人大常委会主任" in post:
        return "县人大常委会主任"
    if "政协主席" in post:
        return "县政协主席"
    if "县委常委" in post:
        return "县委常委"
    return post.replace(" ", "_")


def main():
    print(f"=== Building network for {SLUG} ===")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()

    # 1. Build the relational database + GEXF graph
    print(">>> Building database and GEXF...")
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
    print()

    # 2. Write per-person JSON files
    print(">>> Writing person JSON files...")
    write_person_jsons()
    print()

    # 3. Print summary
    print("=== Build complete ===")
    print(f"  Database:  {DB_PATH} ({os.path.getsize(DB_PATH)} bytes)")
    print(f"  GEXF:      {GEXF_PATH} ({os.path.getsize(GEXF_PATH)} bytes)")
    print(f"  Persons:   {len(persons)}")
    print(f"  Orgs:      {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    print()
    print("Leadership data sourced from official 宜君县人民政府 website (领导之窗).")
    print("Core identities (左小军, 毛建荣) confirmed with full biographies.")
    print("Full roster of 县委常委 and 副县长 confirmed from official listing.")


if __name__ == "__main__":
    main()
