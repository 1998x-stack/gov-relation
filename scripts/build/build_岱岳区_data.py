#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 岱岳区 (Daiyue District), 泰安市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_岱岳区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.daiyue.gov.cn — 岱岳区人民政府官方网站 (区政府领导页面)
  - www.daiyue.gov.cn — 新闻文章确认区委书记为刘国成 (2026-07-23)
  - baike.baidu.com/item/苗明峻 — Baidu Baike for Miao Mingjun
  - Inference: 刘国成previously served in Tai'an city before Daiyue appointment

Confidence notes:
  - 苗明峻: confirmed via gov leadership page + Baidu Baike (birth 1975-09, 研究生/法学硕士)
  - 刘国成: confirmed name/role as of 2026-07-23 via official news; full biography unverified
  - 孙启龙 (区政协主席): confirmed name/role via official news
  - 钱振华 (区人大常委会主任): confirmed name/role via official news
  - 副区长 list: confirmed via gov leadership page
  - Web search degraded: Exa rate-limited, Baidu 403 for 刘国成
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "岱岳区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_岱岳区"
if _CURRENT_DIR.name == "shandong_岱岳区":
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
# IDs: 1-2 core (区委书记/区长), 3-4 人大/政协, 5-6 区委副书记/常委副区长,
#       7-10 other standing committee, 11+ deputies, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘国成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 待查
        "birthplace": "",  # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共泰安市岱岳区委员会",
        "source": "https://www.daiyue.gov.cn/art/2026/7/23/art_47148_10381618.html",
        "confidence": "confirmed",
        "notes": "2026年7月23日主持召开区委常委会。此前简历待查——可能曾在泰安市其他区县或市直部门任职后调任岱岳区委书记。"
    },
    {
        "id": 2,
        "name": "苗明峻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "",  # 百度百科未标注籍贯
        "education": "研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "岱岳区人民政府",
        "source": "https://baike.baidu.com/item/苗明峻",
        "confidence": "confirmed",
        "notes": "曾任泰安市农业经济发展服务中心主任（站长）；2022.04-2024.02 泰安市统计局局长；2024.01 任岱岳区副区长、代区长；2024.02 任岱岳区区长。泰安市第十八届人大代表。一级调研员。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "钱振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "岱岳区人民代表大会常务委员会",
        "source": "https://www.daiyue.gov.cn/art/2026/7/23/art_47148_10381618.html",
        "confidence": "confirmed",
        "notes": "2026年7月列席区委常委会会议。此前简历待查。"
    },
    {
        "id": 4,
        "name": "孙启龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议泰安市岱岳区委员会",
        "source": "https://www.daiyue.gov.cn/art/2026/7/23/art_47148_10381618.html",
        "confidence": "confirmed",
        "notes": "2026年7月列席区委常委会会议。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区委常委 / 区政府党组成员
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "裴敦友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员",
        "current_org": "中共泰安市岱岳区委员会",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示其为区委常委和区政府党组成员。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 副区长
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "尹延涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。此前简历待查。"
    },
    {
        "id": 7,
        "name": "黄新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。此前简历待查。"
    },
    {
        "id": 8,
        "name": "迟建勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。此前简历待查。"
    },
    {
        "id": 9,
        "name": "卞飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。2026-07-24陪同苗明峻督导民生/防汛等工作。此前简历待查。"
    },
    {
        "id": 10,
        "name": "齐瑞金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。此前简历待查。"
    },
    {
        "id": 11,
        "name": "朱荣斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。此前简历待查。"
    },
    {
        "id": 12,
        "name": "杨晓妍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。此前简历待查。"
    },
    {
        "id": 13,
        "name": "王小明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岱岳区人民政府",
        "source": "https://www.daiyue.gov.cn/col/col47152/index.html",
        "confidence": "confirmed",
        "notes": "区政府领导页面显示为副区长。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (limited data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "【待查】前任区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "unverified",
        "notes": "刘国成的前任区委书记待查。可能为泰安市副市级领导兼任或由泰安市直部门调任。"
    },
    {
        "id": 31,
        "name": "【待查】前任区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "unverified",
        "notes": "苗明峻的前任区长待查。苗明峻于2024年1月任代区长、2月任区长。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共泰安市岱岳区委员会", "type": "党委", "level": "市辖区", "parent": "泰安市", "location": "山东省泰安市岱岳区"},
    {"id": 2, "name": "岱岳区人民政府", "type": "政府", "level": "市辖区", "parent": "泰安市", "location": "山东省泰安市岱岳区"},
    {"id": 3, "name": "岱岳区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "泰安市", "location": "山东省泰安市岱岳区"},
    {"id": 4, "name": "中国人民政治协商会议泰安市岱岳区委员会", "type": "政协", "level": "市辖区", "parent": "泰安市", "location": "山东省泰安市岱岳区"},
    {"id": 5, "name": "泰安市统计局", "type": "政府", "level": "地级市", "parent": "泰安市", "location": "山东省泰安市"},
    {"id": 6, "name": "泰安市农业经济发展服务中心", "type": "事业单位", "level": "地级市", "parent": "泰安市", "location": "山东省泰安市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘国成
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年7月在职"},
    # 苗明峻
    {"person_id": 2, "org_id": 6, "title": "主任（站长）", "start": "", "end": "2022-04", "rank": "", "note": "泰安市农业经济发展服务中心"},
    {"person_id": 2, "org_id": 5, "title": "局长", "start": "2022-04", "end": "2024-02", "rank": "正处级", "note": "泰安市统计局局长"},
    {"person_id": 2, "org_id": 2, "title": "副区长、代区长", "start": "2024-01", "end": "2024-02", "rank": "正处级", "note": "岱岳区代理区长"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2024-02", "end": "present", "rank": "正处级", "note": "岱岳区人民政府区长、党组书记，一级调研员"},
    # 钱振华
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 孙启龙
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 裴敦友
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "区政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副区长们
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
# All current relationships are co-leadership in the same district
# Stronger relationship evidence requires deeper biographical research

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长搭班，共同领导岱岳区工作",
        "overlap_org": "中共泰安市岱岳区委员会/岱岳区人民政府",
        "overlap_period": AS_OF,
        "strength": "strong",
        "confidence": "confirmed",
        "source": "https://www.daiyue.gov.cn/art/2026/7/23/art_47148_10381618.html"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "superior_subordinate",
        "context": "区长与副区长（卞飞），卞飞陪同苗明峻督导民生及防汛工作",
        "overlap_org": "岱岳区人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "https://www.daiyue.gov.cn/art/2026/7/24/art_47148_10381686.html"
    },
]


# ── Person JSON Helper ───────────────────────────────────────────────────────

def write_person_json(person: dict, extra: dict | None = None) -> str:
    """Write a person JSON to PJSON_DIR and return its filename."""
    job_slug = person["current_post"].replace("/", "_")
    fname = f"{TODAY}-山东省-泰安市-{job_slug}-{person['name']}.json"
    path = PJSON_DIR / fname

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "泰安市",
            "region": "岱岳区",
            "job": person["current_post"],
            "task_id": "shandong_岱岳区",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"daiyue_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"institution": person["education"], "period": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": person["confidence"] == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": _career_timeline_for(person),
        "organizations": [],
        "relationships": _relationships_for(person),
        "governance_record": _governance_record_for(person),
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if person["id"] == 2 else "unknown",
            "systems_experience": [],
            "geographic_pattern": ["泰安市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "No public risk signals found in available sources", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": person["notes"], "url": person["source"], "publisher": "岱岳区人民政府", "published_at": AS_OF, "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": person["confidence"],
            "current_role": "confirmed",
            "career_completeness": "partial" if not person["birth"] else "partial",
            "relationship_confidence": "low",
            "biggest_gap": f"完整履历待查" if not person["birth"] else "完整履历待查"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的完整履历", "why_it_matters": "核心领导背景未知", "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示", f"{person['name']} 泰安"], "last_attempted": TODAY},
            {"priority": "high", "question": f"{person['name']}的出生年月和籍贯", "why_it_matters": "身份识别关键信息", "suggested_queries": [f"{person['name']} 出生"], "last_attempted": TODAY}
        ]
    }

    if extra:
        data.update(extra)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


def _career_timeline_for(person: dict) -> list:
    """Build career timeline from positions."""
    if person["id"] == 2:
        return [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到2022年之前的完整任职履历", "confidence": "unverified", "source_ids": []},
            {"start": "unknown", "end": "2022-04", "org": "泰安市农业经济发展服务中心", "title": "主任（站长）", "level": "", "location": "泰安市", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2022-04", "end": "2024-02", "org": "泰安市统计局", "title": "局长", "level": "正处级", "location": "泰安市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2022年4月任泰安市统计局局长", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2024-01", "end": "2024-02", "org": "岱岳区人民政府", "title": "副区长、代区长", "level": "正处级", "location": "泰安市岱岳区", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2024-02", "end": "present", "org": "岱岳区人民政府", "title": "区长", "level": "正处级", "location": "泰安市岱岳区", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "岱岳区区长、党组书记、一级调研员", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 1:
        return [
            {"start": "unknown", "end": "present", "org": "中共泰安市岱岳区委员会", "title": "区委书记", "level": "正处级", "location": "泰安市岱岳区", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2026年7月在职，主持区委常委会", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前任职履历完全未知", "confidence": "unverified", "source_ids": []},
        ]
    return [
        {"start": "unknown", "end": "present", "org": person["current_org"], "title": person["current_post"], "level": "", "location": "泰安市岱岳区", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": person["confidence"], "source_ids": ["S001"]}
    ]


def _relationships_for(person: dict) -> list:
    """Build relationship list for this person."""
    rs = []
    for r in relationships:
        other_id = r["person_b"] if r["person_a"] == person["id"] else (r["person_a"] if r["person_b"] == person["id"] else None)
        if other_id is not None:
            other = next((p for p in persons if p["id"] == other_id), None)
            if other:
                rs.append({
                    "person": other["name"],
                    "person_id": f"daiyue_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": r["strength"],
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": r["confidence"],
                    "source_ids": []
                })
    return rs


def _governance_record_for(person: dict) -> list:
    """Build governance record for this person."""
    if person["id"] == 2:
        return [
            {"period": "2026-07", "domain": "public_security", "achievement_or_event": "督导民生领域、防汛及群众回迁安置等重点工作", "role_in_event": "区长督导落实", "measurable_outcome": "现场检查山口镇、范镇、角峪镇", "location": "岱岳区", "confidence": "confirmed", "source_ids": ["S001"]}
        ]
    elif person["id"] == 1:
        return [
            {"period": "2026-07-23", "domain": "economic_development", "achievement_or_event": "主持区委常委会，研究上半年经济社会发展形势", "role_in_event": "区委书记主持会议并部署工作", "measurable_outcome": "研究全区经济社会发展和安全工作", "location": "岱岳区", "confidence": "confirmed", "source_ids": ["S001"]}
        ]
    return []


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Building {SLUG} network...")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs
    core_ids = [1, 2]
    for pid in core_ids:
        person = next(p for p in persons if p["id"] == pid)
        fname = write_person_json(person)
        print(f"  Person JSON: {fname}")

    print(f"\nDone. Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {PJSON_DIR}")


if __name__ == "__main__":
    main()
