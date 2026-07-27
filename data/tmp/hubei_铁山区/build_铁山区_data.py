#!/usr/bin/env python3
"""
黄石市铁山区领导班子工作关系网络 — 数据构建脚本

等级: 市辖区
调查日期: 2026-07-24
信息来源: 黄石经济技术开发区·铁山区合署办公
          铁山区人民政府网站 (tieshan.gov.cn, 网络访问受限)
备注: 铁山区与黄石经济技术开发区（国家级经开区）合署办公，"一套班子、两块牌子"。
      区委书记兼任经开区党工委书记，区长兼任经开区管委会主任。

Task ID: hubei_铁山区
Province: 湖北省
Parent city: 黄石市
Region: 铁山区
Level: 市辖区
Targets: 区委书记 & 区长
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation package is importable
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "铁山区"
TODAY = "2026-07-24"
# 由于合署办公，开发区与铁山区是同一套班子
# 开发区党工委、管委会与区委、区政府合署
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"


def org_id(base: int) -> int:
    """Offset org IDs into the 100000+ range per runner convention."""
    return base + 100000


# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee / 经开区党工委, 2xxx = government / 经开区管委会
# Note: 铁山区与黄石经济技术开发区合署办公，领导班子成员同时兼任经开区职务。
# WARNING: 由于网络访问受限，当前领导班子成员信息无法从官方政府网站直接确认。
# 以下信息基于已知的合署办公组织结构和公开新闻报道推断，标记为"plausible"或"unverified"。

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 铁山区委书记（兼黄石经济技术开发区党工委书记）
    # 注：近年铁山区委书记通常同时担任黄石经济技术开发区党工委书记
    # 2023年前后张育英曾任铁山区委书记/开发区党工委书记
    # 后续接任者通过合署办公结构担任双重职务
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委书记（兼黄石经济技术开发区党工委书记）",
        "current_org": "中共黄石市铁山区委员会（与中共黄石经济技术开发区工作委员会合署）",
        "source": "（网络访问受限，待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 铁山区区长（兼黄石经济技术开发区管委会主任）
    # 注：铁山区区长通常同时担任黄石经济技术开发区管委会主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委副书记、区政府区长（兼黄石经济技术开发区管委会主任）",
        "current_org": "铁山区人民政府（与黄石经济技术开发区管理委员会合署）",
        "source": "（网络访问受限，待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 区委副书记（推定）
    # 注：区级领导班子通常设1-2名副书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委副书记（推定）",
        "current_org": "中共黄石市铁山区委员会",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 区委常委、常务副区长（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委常委、常务副区长（推定）",
        "current_org": "铁山区人民政府",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 区委常委、区纪委书记、监委主任（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委常委、区纪委书记、区监委主任（推定）",
        "current_org": "中共黄石市铁山区纪律检查委员会",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 区委常委、区委组织部部长（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委常委、区委组织部部长（推定）",
        "current_org": "中共黄石市铁山区委组织部",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 区委常委、区委宣传部部长（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委常委、区委宣传部部长（推定）",
        "current_org": "中共黄石市铁山区委宣传部",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 区委常委、区委政法委书记（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区委常委、政法委书记（推定）",
        "current_org": "中共黄石市铁山区委政法委员会",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 铁山区人大常委会主任（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区人大常委会主任（推定）",
        "current_org": "铁山区人大常委会",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 铁山区政协主席（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山区政协主席（推定）",
        "current_org": "铁山区政协",
        "source": "（待确认）",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共黄石市铁山区委员会（与黄石经开区党工委合署）", "type": "党委",
     "level": "县处级", "parent": "中共黄石市委员会", "location": "黄石市铁山区"},
    {"id": 2, "name": "铁山区人民政府（与黄石经开区管委会合署）", "type": "政府",
     "level": "县处级", "parent": "黄石市人民政府", "location": "黄石市铁山区"},
    {"id": 3, "name": "铁山区人大常委会", "type": "人大",
     "level": "县处级", "parent": "黄石市人大常委会", "location": "黄石市铁山区"},
    {"id": 4, "name": "铁山区政协", "type": "政协",
     "level": "县处级", "parent": "黄石市政协", "location": "黄石市铁山区"},
    {"id": 5, "name": "中共黄石市铁山区纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共黄石市纪律检查委员会", "location": "黄石市铁山区"},
    {"id": 6, "name": "中共黄石市铁山区委组织部", "type": "党委",
     "level": "乡科级", "parent": "中共黄石市铁山区委员会", "location": "黄石市铁山区"},
    {"id": 7, "name": "中共黄石市铁山区委宣传部", "type": "党委",
     "level": "乡科级", "parent": "中共黄石市铁山区委员会", "location": "黄石市铁山区"},
    {"id": 8, "name": "中共黄石市铁山区委政法委员会", "type": "党委",
     "level": "乡科级", "parent": "中共黄石市铁山区委员会", "location": "黄石市铁山区"},
    {"id": 9, "name": "黄石经济技术开发区管理委员会", "type": "开发区",
     "level": "国家级", "parent": "黄石市人民政府", "location": "黄石市铁山区"},
    {"id": 10, "name": "中共黄石经济技术开发区工作委员会", "type": "党委",
     "level": "国家级", "parent": "中共黄石市委员会", "location": "黄石市铁山区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 区委书记（兼经开区党工委书记）
    {"person_id": 1001, "org_id": 1, "title": "铁山区委书记（兼黄石经开区党工委书记）",
     "start_date": "", "end_date": "present", "rank": "县处级正职（兼任国家级经开区党工委书记）",
     "note": "主持区委和经开区党工委全面工作. 姓名待确认。"},
    # 区长（兼经开区管委会主任）
    {"person_id": 1002, "org_id": 2, "title": "铁山区区长（兼黄石经开区管委会主任）",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "主持区政府和经开区管委会全面工作. 姓名待确认。"},
    {"person_id": 1002, "org_id": 9, "title": "黄石经济技术开发区管委会主任（兼）",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "合署办公，与区长一人兼任"},
    # 区委副书记
    {"person_id": 1003, "org_id": 1, "title": "铁山区委副书记（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 常务副区长
    {"person_id": 1004, "org_id": 1, "title": "铁山区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 1004, "org_id": 2, "title": "铁山区常务副区长（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 纪委书记
    {"person_id": 1005, "org_id": 5, "title": "铁山区委常委、区纪委书记、区监委主任（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 组织部长
    {"person_id": 1006, "org_id": 6, "title": "铁山区委常委、区委组织部部长（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 宣传部长
    {"person_id": 1007, "org_id": 7, "title": "铁山区委常委、区委宣传部部长（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 政法委书记
    {"person_id": 1008, "org_id": 8, "title": "铁山区委常委、政法委书记（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 人大主任
    {"person_id": 1009, "org_id": 3, "title": "铁山区人大常委会主任（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 政协主席
    {"person_id": 1010, "org_id": 4, "title": "铁山区政协主席（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# 所有关系均为基于合署办公组织结构的推定关系
# 待网络访问恢复后通过官方来源确认

relationships = [
    # 区委书记 ←→ 区长: 党政正职搭档
    {"person_a": 1001, "person_b": 1002, "type": "overlap",
     "context": "党政正职搭档：区委书记—区长，同时兼任经开区正职（待确认姓名）",
     "overlap_org": "中共黄石市铁山区委员会／铁山区人民政府",
     "overlap_period": "推定"},
    # 区委书记 ←→ 区委副书记
    {"person_a": 1001, "person_b": 1003, "type": "superior_subordinate",
     "context": "区委正副书记工作关系（推定）",
     "overlap_org": "中共黄石市铁山区委员会",
     "overlap_period": "推定"},
    # 区委书记 ←→ 常务副区长
    {"person_a": 1001, "person_b": 1004, "type": "superior_subordinate",
     "context": "区委书记—区委常委（推定）",
     "overlap_org": "中共黄石市铁山区委员会",
     "overlap_period": "推定"},
    # 区委书记 ←→ 纪委书记
    {"person_a": 1001, "person_b": 1005, "type": "superior_subordinate",
     "context": "区委书记—纪委书记（推定）",
     "overlap_org": "中共黄石市铁山区委员会",
     "overlap_period": "推定"},
    # 区委书记 ←→ 组织部长
    {"person_a": 1001, "person_b": 1006, "type": "superior_subordinate",
     "context": "区委书记—组织部部长（推定）",
     "overlap_org": "中共黄石市铁山区委员会",
     "overlap_period": "推定"},
    # 区委书记 ←→ 宣传部长
    {"person_a": 1001, "person_b": 1007, "type": "superior_subordinate",
     "context": "区委书记—宣传部部长（推定）",
     "overlap_org": "中共黄石市铁山区委员会",
     "overlap_period": "推定"},
    # 区委书记 ←→ 政法委书记
    {"person_a": 1001, "person_b": 1008, "type": "superior_subordinate",
     "context": "区委书记—政法委书记（推定）",
     "overlap_org": "中共黄石市铁山区委员会",
     "overlap_period": "推定"},
    # 区长 ←→ 常务副区长
    {"person_a": 1002, "person_b": 1004, "type": "superior_subordinate",
     "context": "区长—常务副区长（推定）",
     "overlap_org": "铁山区人民政府",
     "overlap_period": "推定"},
]

# ── Known predecessor info (historical) ──
# 张育英 — 曾任铁山区委书记、黄石经济技术开发区党工委书记（约2019-2023年）
# 后续接任者信息因网络访问受限无法确认


# ── Main ─────────────────────────────────────────────────────────────────────

def write_person_json(person: dict) -> None:
    """Write a person graph JSON file to the staging directory."""
    safe_name = person["name"]
    job_slug_parts = person["current_post"].split("（")[0].split("兼")[0][:12] if "（" in person["current_post"] else person["current_post"]
    if not job_slug_parts:
        job_slug_parts = person["current_post"]
    filename = f"{TODAY.replace('-', '')}-湖北省-黄石市-{job_slug_parts}-{safe_name}.json"
    filepath = STAGING / filename

    is_confirmed = safe_name != "（待确认）"

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "黄石市",
            "region": "铁山区",
            "job": person["current_post"],
            "task_id": "hubei_铁山区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"hubei_huangshi_tieshan_{safe_name}",
            "name": safe_name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{safe_name}_{person.get('birth', '')}",
                "name_birthplace": f"{safe_name}_{person.get('birthplace', '')}",
                "official_profile_url": "https://www.tieshan.gov.cn/（网络访问受限）",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级" if "区长" in person["current_post"] or "人大" in person["current_post"] or "政协" in person["current_post"] else "县处级",
            "as_of": TODAY,
            "is_current_confirmed": is_confirmed,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "",
                "location": "黄石市铁山区",
                "system": "party" if "书记" in person["current_post"] else "government" if "区长" in person["current_post"] else "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": "待补充详细履历",
                "confidence": "plausible" if is_confirmed else "unverified",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "网络访问受限，无法获取公开资料",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因网络访问受限，未找到风险信号。需后续在有网络条件下排查。",
                "date": TODAY,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "铁山区人民政府网站",
                "url": "https://www.tieshan.gov.cn/",
                "publisher": "铁山区人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "medium",
                "notes": "网站不可访问（网络受限），信息基于合署办公结构推断",
            },
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "plausible" if is_confirmed else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "网络访问受限：无法从官方政府网站确认当前领导班子名单；" +
                          "同时无法访问百度百科、新闻报道等来源补充履历和详细信息。"
                          "全部人员的姓名、履历均待确认。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "铁山区委书记的姓名？是否由黄石经开区党工委书记兼任？",
                "why_it_matters": "这是核心调查目标——身份确认的基础",
                "suggested_queries": [
                    "铁山区委书记 2025 2026 现任",
                    "黄石经济技术开发区党工委书记",
                    "铁山区 领导之窗 区委书记",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "critical",
                "question": "铁山区区长的姓名？",
                "why_it_matters": "核心调查目标",
                "suggested_queries": [
                    "铁山区区长 2025 2026 现任",
                    "黄石经济技术开发区管委会主任",
                    "铁山区政府 区长",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": "铁山区领导班子全体成员名单",
                "why_it_matters": "构建完整的领导网络",
                "suggested_queries": [
                    "铁山区委常委名单",
                    "铁山区政府领导分工",
                    "铁山区领导之窗",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": "铁山区委书记和区长的完整履历（出生年月、籍贯、教育背景、任职经历）",
                "why_it_matters": "构建完整的个人图谱和网络分析基础数据",
                "suggested_queries": [
                    "铁山区委书记 简历",
                    "铁山区长 任前公示",
                    "黄石经开区 领导干部 简历",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "medium",
                "question": "前任铁山区委书记/区长的去向",
                "why_it_matters": "交接班和干部流动网络",
                "suggested_queries": [
                    "铁山区委书记 卸任 去向",
                    "铁山区 前任 区长 调任",
                    "黄石市 干部任前公示 铁山",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "medium",
                "question": "铁山区与黄石经济技术开发区合署办公的具体运作模式和领导班子交叉任职情况",
                "why_it_matters": "合署办公模式影响关系网络的形态",
                "suggested_queries": [
                    "开发区铁山区 合署办公 领导班子",
                    "黄石经济技术开发区 铁山区 一体化",
                ],
                "last_attempted": TODAY,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ── Build database & GEXF ────────────────────────────────────────────
    print(f"Building {SLUG} network data…")
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
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # ── Person JSON files ────────────────────────────────────────────────
    print("Writing person graph JSON files…")
    for p in persons:
        write_person_json(p)

    print("Done.")
    print()
    print("=" * 60)
    print("注意: 由于网络访问受限，所有核心人物的姓名均标注为「待确认」。")
    print("请在网络访问恢复后运行以下查询补全信息：")
    print("  1. 铁山区委书记姓名和履历")
    print("  2. 铁山区区长姓名和履历")
    print("  3. 铁山区领导班子全体成员名单")
    print("=" * 60)
