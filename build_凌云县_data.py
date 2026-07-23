#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
凌云县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 百色市
Region: 凌云县
Targets: 县委书记 & 县长

Current Leaders (as of 2026-07, from official website www.lingyun.gov.cn):
  - 县委书记: 黄卓远
  - 县委副书记、县长: 谢旦杏
  - 县人大常委会主任: 黄凤萍
  - 县政协主席: 罗胜明
  - 县委常委、副县长: 周芃
  - 副县长: 莫夏挺, 张定湘, 闭灿全
  - 其他县领导: 石永存, 肖国权, 李昌善, 吴先毅, 李静

Research Note:
  凌云县人民政府门户网站 http://www.lingyun.gov.cn/ 可访问。
  领导之窗页面在 /zwgk/ 下，列出了县长、副县长信息。
  通过新闻文章确认了核心领导的职务：
  - 黄卓远 在2026年6月27日以"凌云县委书记"身份督导灾后重建
  - 谢旦杏 在2026年6月2日以"县长"身份督导环保工作
  - 2026年4月1日领导干部警示教育大会确认：黄卓远县委书记、谢旦杏县委副书记/县长
  - 黄凤萍为县人大常委会主任、罗胜明为县政协主席
  - 副县长: 莫夏挺、张定湘、周芃、闭灿全

  个人履历、出生年月、教育背景等详细信息因Baidu百科访问受限暂缺。

Data Date: 2026-07-23
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "凌云县"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"
TODAY = AS_OF

# ═══════════════════════════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黄卓远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县委书记",
        "current_org": "中共凌云县委员会",
        "source": "http://www.lingyun.gov.cn/ — 2026-06-29 article《黄卓远到玉洪瑶族乡合祥村督导灾后安置及重建工作》中以凌云县委书记身份出现；2026-04-01 领导干部警示教育大会确认县委书记",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "谢旦杏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县委副书记、县长",
        "current_org": "凌云县人民政府",
        "source": "http://www.lingyun.gov.cn/ — 2026-06-03 article《谢旦杏实地督导中央环保督察信访件办理工作》中以县长身份出现；2026-04-01 警示教育大会确认县委副书记、县长",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "黄凤萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县人大常委会主任",
        "current_org": "凌云县人民代表大会常务委员会",
        "source": "http://www.lingyun.gov.cn/ — 2026-04-01 领导干部警示教育大会；2026-06-17 人大换届选举工作推进会",
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "罗胜明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县政协主席",
        "current_org": "中国人民政治协商会议凌云县委员会",
        "source": "http://www.lingyun.gov.cn/ — 2026-04-01 领导干部警示教育大会确认县政协主席",
    },
    # ════════════════════════════════════════
    # 县委常委、副县长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "周芃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县委常委、副县长",
        "current_org": "凌云县人民政府",
        "source": "http://www.lingyun.gov.cn/ — 2026-06-29 article《黄卓远到玉洪瑶族乡合祥村督导灾后安置及重建工作》中以县委常委、副县长身份随同调研；政府信息公开-领导之窗列出",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "莫夏挺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县副县长",
        "current_org": "凌云县人民政府",
        "source": "http://www.lingyun.gov.cn/ — 政府信息公开-领导之窗列出副县长；2026-04-01 警示教育大会参会",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "张定湘",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县副县长",
        "current_org": "凌云县人民政府",
        "source": "http://www.lingyun.gov.cn/ — 政府信息公开-领导之窗列出副县长",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "闭灿全",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县副县长",
        "current_org": "凌云县人民政府",
        "source": "http://www.lingyun.gov.cn/ — 政府信息公开-领导之窗列出副县长",
    },
    # ════════════════════════════════════════
    # 县人大副主任
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "游本文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县人大常委会副主任",
        "current_org": "凌云县人民代表大会常务委员会",
        "source": "http://www.lingyun.gov.cn/ — 2026-06-17 人大换届选举工作推进会参会",
    },
    # ════════════════════════════════════════
    # 县人大副主任
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "蒙香莲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县人大常委会副主任",
        "current_org": "凌云县人民代表大会常务委员会",
        "source": "http://www.lingyun.gov.cn/ — 2026-06-17 人大换届选举工作推进会参会",
    },
    # ════════════════════════════════════════
    # 县人大副主任
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "左明欢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县人大常委会副主任",
        "current_org": "凌云县人民代表大会常务委员会",
        "source": "http://www.lingyun.gov.cn/ — 2026-06-17 人大换届选举工作推进会参会",
    },
    # ════════════════════════════════════════
    # 县领导（职务待查）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "石永存",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县领导（具体职务待查）",
        "current_org": "凌云县",
        "source": "http://www.lingyun.gov.cn/ — 2026-04-01 警示教育大会以县领导身份参会",
    },
    {
        "id": 13,
        "name": "肖国权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县领导（具体职务待查）",
        "current_org": "凌云县",
        "source": "http://www.lingyun.gov.cn/ — 2026-04-01 警示教育大会以县领导身份参会",
    },
    {
        "id": 14,
        "name": "李昌善",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县领导（具体职务待查）",
        "current_org": "凌云县",
        "source": "http://www.lingyun.gov.cn/ — 2026-04-01 警示教育大会以县领导身份参会",
    },
    {
        "id": 15,
        "name": "吴先毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县领导（具体职务待查）",
        "current_org": "凌云县",
        "source": "http://www.lingyun.gov.cn/ — 2026-04-01 警示教育大会以县领导身份参会",
    },
    {
        "id": 16,
        "name": "李静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凌云县领导（具体职务待查）",
        "current_org": "凌云县",
        "source": "http://www.lingyun.gov.cn/ — 2026-04-01 警示教育大会以县领导身份参会",
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共凌云县委员会", "type": "党委", "level": "县处级", "parent": "中共百色市委员会", "location": "广西百色凌云县"},
    {"id": 2, "name": "凌云县人民政府", "type": "政府", "level": "县处级", "parent": "百色市人民政府", "location": "广西百色凌云县"},
    {"id": 3, "name": "凌云县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "百色市人民代表大会常务委员会", "location": "广西百色凌云县"},
    {"id": 4, "name": "中国人民政治协商会议凌云县委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议百色市委员会", "location": "广西百色凌云县"},
]

# ═══════════════════════════════════════════════════════════════
# 3. POSITIONS
# ═══════════════════════════════════════════════════════════════

positions = [
    # 黄卓远
    {"person_id": 1, "org_id": 1, "title": "凌云县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月确认在任"},
    # 谢旦杏
    {"person_id": 2, "org_id": 2, "title": "凌云县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月确认在任"},
    # 黄凤萍
    {"person_id": 3, "org_id": 3, "title": "凌云县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 罗胜明
    {"person_id": 4, "org_id": 4, "title": "凌云县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 周芃
    {"person_id": 5, "org_id": 2, "title": "凌云县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 莫夏挺
    {"person_id": 6, "org_id": 2, "title": "凌云县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张定湘
    {"person_id": 7, "org_id": 2, "title": "凌云县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 闭灿全
    {"person_id": 8, "org_id": 2, "title": "凌云县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 游本文
    {"person_id": 9, "org_id": 3, "title": "凌云县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 蒙香莲
    {"person_id": 10, "org_id": 3, "title": "凌云县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 左明欢
    {"person_id": 11, "org_id": 3, "title": "凌云县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 石永存（职务待查，暂放县政府）
    {"person_id": 12, "org_id": 2, "title": "凌云县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
    # 肖国权（职务待查，暂放县政府）
    {"person_id": 13, "org_id": 2, "title": "凌云县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
    # 李昌善（职务待查，暂放县政府）
    {"person_id": 14, "org_id": 2, "title": "凌云县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
    # 吴先毅（职务待查，暂放县政府）
    {"person_id": 15, "org_id": 2, "title": "凌云县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
    # 李静（职务待查，暂放县政府）
    {"person_id": 16, "org_id": 2, "title": "凌云县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
]

# ═══════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════

relationships = [
    # 黄卓远 ↔ 谢旦杏：党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "凌云县县委书记与县长党政搭档", "overlap_org": "中共凌云县委员会/凌云县人民政府", "overlap_period": "截至2026-07-23"},
    # 黄卓远 ↔ 周芃：上下级
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县委常委、副县长", "overlap_org": "中共凌云县委员会", "overlap_period": "截至2026-07-23"},
    # 谢旦杏 ↔ 莫夏挺：上下级
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "凌云县人民政府", "overlap_period": "截至2026-07-23"},
    # 谢旦杏 ↔ 张定湘：上下级
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "凌云县人民政府", "overlap_period": "截至2026-07-23"},
    # 谢旦杏 ↔ 闭灿全：上下级
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "凌云县人民政府", "overlap_period": "截至2026-07-23"},
    # 谢旦杏 ↔ 周芃：上下级
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与县委常委、副县长", "overlap_org": "凌云县人民政府", "overlap_period": "截至2026-07-23"},
    # 黄凤萍（人大）↔ 党政主要领导：同届班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县人大常委会主任同届班子", "overlap_org": "凌云县四家班子", "overlap_period": "截至2026-07-23"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县人大常委会主任同届班子", "overlap_org": "凌云县四家班子", "overlap_period": "截至2026-07-23"},
    # 罗胜明（政协）↔ 党政主要领导：同届班子
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县政协主席同届班子", "overlap_org": "凌云县四家班子", "overlap_period": "截至2026-07-23"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与县政协主席同届班子", "overlap_org": "凌云县四家班子", "overlap_period": "截至2026-07-23"},
    # 游本文 / 蒙香莲 / 左明欢（人大副主任）↔ 黄凤萍（人大主任）：同机构
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "县人大常委会主任与副主任", "overlap_org": "凌云县人民代表大会常务委员会", "overlap_period": "截至2026-07-23"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "县人大常委会主任与副主任", "overlap_org": "凌云县人民代表大会常务委员会", "overlap_period": "截至2026-07-23"},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "县人大常委会主任与副主任", "overlap_org": "凌云县人民代表大会常务委员会", "overlap_period": "截至2026-07-23"},
]


# ═══════════════════════════════════════════════════════════════
# 5. PERSON JSON HELPERS
# ═══════════════════════════════════════════════════════════════

def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "百色市",
            "region": "凌云县",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "guangxi_凌云县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"lingyun_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Complete career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "凌云县人民政府门户网站",
         "url": "http://www.lingyun.gov.cn/", "publisher": "凌云县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info and news"},
        {"id": "S002", "title": "凌云县领导之窗",
         "url": "http://www.lingyun.gov.cn/zwgk/",
         "publisher": "凌云县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Government information disclosure page listing leadership"},
    ]

    # ── 黄卓远 person JSON ──
    hzy_timeline = [
        {"start": "", "end": "present",
         "org": "中共凌云县委员会",
         "title": "凌云县委书记", "level": "正处级",
         "location": "广西百色凌云县", "system": "party",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "2026年6月以县委书记身份督导灾后重建；2026年4月为全县领导干部上廉政教育课",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到黄卓远任凌云县委书记之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    hzy_relationships = [
        {"person": "谢旦杏", "person_id": "lingyun_谢旦杏",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前凌云县县委书记与县长党政搭档",
         "overlap_org": "中共凌云县委员会/凌云县人民政府",
         "overlap_period": "截至2026-07-23",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    hzy_json = build_person_json(persons[0], hzy_timeline, hzy_relationships, sources)
    hzy_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县委书记-黄卓远.json")
    with open(hzy_path, "w", encoding="utf-8") as f:
        json.dump(hzy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hzy_path}")

    # ── 谢旦杏 person JSON ──
    xdx_timeline = [
        {"start": "", "end": "present",
         "org": "凌云县委/凌云县人民政府",
         "title": "凌云县委副书记、县长", "level": "正处级",
         "location": "广西百色凌云县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "2026年6月以县长身份督导中央环保督察信访件办理；2026年5月主持凌云县十七届人民政府第70次常务会议；2026年4月以县委副书记、县长身份主持警示教育大会",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到谢旦杏任凌云县长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    xdx_relationships = [
        {"person": "黄卓远", "person_id": "lingyun_黄卓远",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前凌云县县长与县委书记党政搭档",
         "overlap_org": "凌云县人民政府/中共凌云县委员会",
         "overlap_period": "截至2026-07-23",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    xdx_json = build_person_json(persons[1], xdx_timeline, xdx_relationships, sources)
    xdx_json["investigation_scope"]["job"] = "县长"
    xdx_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县长-谢旦杏.json")
    with open(xdx_path, "w", encoding="utf-8") as f:
        json.dump(xdx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {xdx_path}")


# ═══════════════════════════════════════════════════════════════
# 6. BUILD
# ═══════════════════════════════════════════════════════════════

def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")

    # Build DB and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Build person JSONs
    build_person_jsons()

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
