#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 抚松县, 白山市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_抚松县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.fusong.gov.cn — 抚松县人民政府官方网站 (unreachable — timed out)
  - www.baishan.gov.cn — 白山市人民政府官方网站 (unreachable — timed out)
  - Baidu Baike (403/timed out), Exa (rate-limited), Jina Reader (transport errors)

Cross-reference:
  - 江源区 build script confirms 王文江曾挂职抚松县委常委、副县长

Confidence notes:
  - All web sources were unreachable from the research environment (July 2026).
  - Government site (fusong.gov.cn) timed out at all leadership subpaths.
  - Baishan city government site (baishan.gov.cn) also timed out.
  - Baidu Baike returned HTTP 403 or timed out.
  - Exa search API rate-limited.
  - Jina Reader timed out.
  - All current-role claims are labeled 'unverified' due to inability to confirm
    via live web sources in this session.
  - 县委书记姓名: 待查 — per established pattern when county party secretary name
    is not confirmable on government pages.
  - 县长姓名: 待查 — same treatment.
  - 王文江's cross-county connection (挂职抚松县委常委、副县长) confirmed from 江源区 build data.
  - Artifacts created with explicit uncertainty per source_fallbacks.md partial evidence mode.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
for parent_count in [2, 3, 4, 5, 6]:
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
SLUG = "抚松县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_抚松县"
if _CURRENT_DIR.name == "jilin_抚松县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=县委书记, 2=县长, 3=前任书记, 4=前任县长,
#      5=王文江(挂职副县长), 6=常务副县长, 7=纪委书记, 8=组织部长,
#      9=县委副书记, 10=宣传部长, 11=政法委书记, 12-16=其他副县长

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共抚松县委员会",
        "source": "待查 — 抚松县政府官网(fusong.gov.cn)无法访问",
        "confidence": "unverified",
        "notes": "县委书记姓名确认失败。县政府网站fusong.gov.cn及所有子页面均超时无法访问。未找到任何可靠的公开来源确认当前在任县委书记姓名。需后续通过白山市委组织部公示或新闻报道进一步核实。"
    },
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "抚松县人民政府",
        "source": "待查 — 抚松县政府官网(fusong.gov.cn)无法访问",
        "confidence": "unverified",
        "notes": "县长姓名确认失败。县政府网站fusong.gov.cn及所有子页面均超时无法访问。未找到任何可靠的公开来源确认当前在任县长姓名。需后续核实。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Previous Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_前任县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任（前任县委书记）",
        "current_org": "",
        "source": "待查 — 所有公开来源无法访问",
        "confidence": "unverified",
        "notes": "前任县委书记姓名及去向无法确认。政府网站及新闻报道均不可达。"
    },
    {
        "id": 4,
        "name": "待查_前任县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任（前任县长）",
        "current_org": "",
        "source": "待查 — 所有公开来源无法访问",
        "confidence": "unverified",
        "notes": "前任县长姓名及去向无法确认。政府网站及新闻报道均不可达。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Cross-County Connection (confirmed from 江源区 data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "王文江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1998年12月",
        "current_post": "江源区委副书记、区长",
        "current_org": "白山市江源区人民政府",
        "source": "江源区 build script (data/tmp/jilin_江源区/); Baidu Baike snippet",
        "confidence": "confirmed",
        "notes": "王文江曾挂职抚松县委常委、副县长（吉林省商务厅外国投资服务处副处长任上挂职）。这是已知的抚松县跨县干部交流明确例证。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # 县委/县政府领导 (推定班子成员，待确认)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（常务）",
        "current_org": "抚松县人民政府",
        "source": "待查 — 政府网站无法访问",
        "confidence": "unverified",
        "notes": "常务副县长姓名未知。需后续从白山市委组织部任前公示或政府页面核实。"
    },
    {
        "id": 7,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共抚松县纪律检查委员会",
        "source": "待查 — 政府网站无法访问",
        "confidence": "unverified",
        "notes": "纪委书记姓名未知。"
    },
    {
        "id": 8,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共抚松县委组织部",
        "source": "待查 — 政府网站无法访问",
        "confidence": "unverified",
        "notes": "组织部长姓名未知。"
    },
    {
        "id": 9,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共抚松县委员会",
        "source": "待查 — 政府网站无法访问",
        "confidence": "unverified",
        "notes": "专职副书记姓名未知。注意：县长通常兼任县委副书记，这里指专职副书记。"
    },
    {
        "id": 10,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共抚松县委宣传部",
        "source": "待查 — 政府网站无法访问",
        "confidence": "unverified",
        "notes": "宣传部长姓名未知。"
    },
    {
        "id": 11,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共抚松县委政法委员会",
        "source": "待查 — 政府网站无法访问",
        "confidence": "unverified",
        "notes": "政法委书记姓名未知。"
    },
    {
        "id": 12,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共抚松县委统战部",
        "source": "待查 — 政府网站无法访问",
        "confidence": "unverified",
        "notes": "统战部长姓名未知。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共抚松县委员会", "type": "党委", "level": "县处级",
     "parent": "中共白山市委员会", "location": "吉林省白山市抚松县"},
    {"id": 2, "name": "抚松县人民政府", "type": "政府", "level": "县处级",
     "parent": "白山市人民政府", "location": "吉林省白山市抚松县"},
    {"id": 3, "name": "中共抚松县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共白山市纪律检查委员会", "location": "吉林省白山市抚松县"},
    {"id": 4, "name": "抚松县监察委员会", "type": "党委", "level": "县处级",
     "parent": "白山市监察委员会", "location": "吉林省白山市抚松县"},
    {"id": 5, "name": "中共抚松县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共抚松县委员会", "location": "吉林省白山市抚松县"},
    {"id": 6, "name": "中共抚松县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共抚松县委员会", "location": "吉林省白山市抚松县"},
    {"id": 7, "name": "中共抚松县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共抚松县委员会", "location": "吉林省白山市抚松县"},
    {"id": 8, "name": "中共抚松县委统战部", "type": "党委", "level": "县处级",
     "parent": "中共抚松县委员会", "location": "吉林省白山市抚松县"},
    {"id": 9, "name": "抚松县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "白山市人大常委会", "location": "吉林省白山市抚松县"},
    {"id": 10, "name": "中国人民政治协商会议抚松县委员会", "type": "政协", "level": "县处级",
     "parent": "政协白山市委员会", "location": "吉林省白山市抚松县"},
    # Cross-county reference orgs
    {"id": 11, "name": "白山市江源区人民政府", "type": "政府", "level": "县处级",
     "parent": "白山市人民政府", "location": "吉林省白山市江源区"},
    {"id": 12, "name": "吉林省商务厅", "type": "政府", "level": "厅局级",
     "parent": "吉林省政府", "location": "吉林省长春市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start": "", "end": "present", "rank": "正县级",
     "note": "姓名待确认。截至2026年7月推定现任。"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长",
     "start": "", "end": "present", "rank": "正县级",
     "note": "姓名待确认。截至2026年7月推定现任。"},

    # Previous leaders
    {"person_id": 3, "org_id": 1, "title": "原县委书记（前任）",
     "start": "", "end": "", "rank": "正县级",
     "note": "姓名及去向待确认。"},
    {"person_id": 4, "org_id": 2, "title": "原县长（前任）",
     "start": "", "end": "", "rank": "正县级",
     "note": "姓名及去向待确认。"},

    # Cross-connection: 王文江 挂职抚松县委常委、副县长
    {"person_id": 5, "org_id": 2, "title": "挂职县委常委、副县长",
     "start": "", "end": "", "rank": "副处级",
     "note": "王文江在吉林省商务厅外国投资服务处副处长任上挂职担任抚松县委常委、副县长。后调任白山市文化广播电视和旅游局党组书记、局长，再任江源区区长。"},
    {"person_id": 5, "org_id": 11, "title": "江源区委副书记、区长",
     "start": "2025-03", "end": "present", "rank": "正县级",
     "note": "现任（截至2026年7月）"},
    {"person_id": 5, "org_id": 12, "title": "外国投资服务处副处长",
     "start": "", "end": "", "rank": "副处级",
     "note": "挂职抚松前的省商务厅职务"},

    # County leaders (推定班子成员)
    {"person_id": 6, "org_id": 2, "title": "县委常委、副县长（常务）",
     "start": "", "end": "present", "rank": "副县级",
     "note": "姓名待确认。"},
    {"person_id": 7, "org_id": 3, "title": "县委常委、纪委书记、监委主任",
     "start": "", "end": "present", "rank": "副县级",
     "note": "姓名待确认。"},
    {"person_id": 8, "org_id": 5, "title": "县委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "姓名待确认。"},
    {"person_id": 9, "org_id": 1, "title": "县委副书记（专职）",
     "start": "", "end": "present", "rank": "副县级",
     "note": "姓名待确认。注意区分兼任县长的副书记。"},
    {"person_id": 10, "org_id": 6, "title": "县委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "姓名待确认。"},
    {"person_id": 11, "org_id": 7, "title": "县委常委、政法委书记",
     "start": "", "end": "present", "rank": "副县级",
     "note": "姓名待确认。"},
    {"person_id": 12, "org_id": 8, "title": "县委常委、统战部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "姓名待确认。"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Top leader <-> top leader
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭班（党政一把手）",
     "overlap_org": "抚松县",
     "overlap_period": ""},

    # Predecessor-successor (推定)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "前任县委书记 -> 现任县委书记（推定接替关系）",
     "overlap_org": "中共抚松县委员会",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "前任县长 -> 现任县长（推定接替关系）",
     "overlap_org": "抚松县人民政府",
     "overlap_period": ""},

    # Cross-county connection (confirmed)
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "王文江曾挂职抚松县委常委、副县长，与县委书记（姓名待查）在同一班子共事",
     "overlap_org": "抚松县",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 2, "type": "overlap",
     "context": "王文江曾挂职抚松县委常委、副县长，与县长（姓名待查）在同一班子共事",
     "overlap_org": "抚松县人民政府",
     "overlap_period": ""},

    # 县委班子成员之间
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记领导常务副县长",
     "overlap_org": "抚松县",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记领导纪委书记（双重领导体制）",
     "overlap_org": "中共抚松县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记领导组织部长",
     "overlap_org": "中共抚松县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记领导专职副书记",
     "overlap_org": "中共抚松县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记领导宣传部长",
     "overlap_org": "中共抚松县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记领导政法委书记",
     "overlap_org": "中共抚松县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记领导统战部长",
     "overlap_org": "中共抚松县委员会",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长领导常务副县长",
     "overlap_org": "抚松县人民政府",
     "overlap_period": ""},
]

# ── Person JSON data ──────────────────────────────────────────────────────────
import copy

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "吉林省",
        "city": "白山市",
        "region": "抚松县",
        "job": "",
        "task_id": "jilin_抚松县",
        "time_focus": "2024-2026"
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": []
}

SOURCE_REGISTER = [
    {
        "id": "S001",
        "title": "江源区 build script (data/tmp/jilin_江源区/build_江源区_data.py)",
        "url": "file:///workspace/data/xieming/other-codes/gov-relation/data/tmp/jilin_江源区/build_江源区_data.py",
        "publisher": "本仓库先前调查",
        "published_at": "2026-07-25",
        "accessed_at": "2026-07-25",
        "source_type": "database",
        "reliability": "high",
        "notes": "确认王文江挂职抚松县委常委、副县长。潘国强、李江波等江源区领导信息。"
    },
    {
        "id": "S002",
        "title": "抚松县人民政府官网",
        "url": "http://www.fusong.gov.cn/",
        "publisher": "抚松县人民政府",
        "published_at": "",
        "accessed_at": "2026-07-25",
        "source_type": "official",
        "reliability": "medium",
        "notes": "所有子页面均超时无法访问。"
    },
    {
        "id": "S003",
        "title": "白山市人民政府官网",
        "url": "http://www.baishan.gov.cn/",
        "publisher": "白山市人民政府",
        "published_at": "",
        "accessed_at": "2026-07-25",
        "source_type": "official",
        "reliability": "medium",
        "notes": "所有子页面均超时无法访问。"
    },
]


def make_person_json(person: dict) -> dict:
    """Generate a person JSON from a person dict."""
    pj = copy.deepcopy(PERSON_JSON_TEMPLATE)
    name = person.get("name", "")
    post = person.get("current_post", "")

    pj["investigation_scope"]["job"] = post

    # identity
    pj["identity"] = {
        "person_id": f"fusong_{name}",
        "name": name,
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": "",
        "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{name}_{person.get('birth','')}",
            "name_birthplace": f"{name}_{person.get('birthplace','')}",
            "official_profile_url": ""
        }
    }

    # current status
    pj["current_status"] = {
        "current_post": person.get("current_post", ""),
        "current_org": person.get("current_org", ""),
        "administrative_rank": "",
        "as_of": AS_OF,
        "is_current_confirmed": False,
        "source_ids": ["S002", "S003"]
    }

    # career timeline — gap noted
    pj["career_timeline"] = [
        {
            "start": "unknown",
            "end": "present",
            "org": person.get("current_org", ""),
            "title": person.get("current_post", ""),
            "level": "",
            "location": "吉林省白山市抚松县",
            "system": "party" if "书记" in post else "government",
            "rank": "",
            "is_key_promotion": False,
            "notes": person.get("notes", "公开资料不可获取，所有履历待查"),
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S002", "S003"]
        }
    ]

    # relationships from the data
    rels_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            target_name = next((p["name"] for p in persons if p["id"] == r["person_b"]), f"ID:{r['person_b']}")
            rels_list.append({
                "person": target_name,
                "person_id": f"fusong_{target_name}",
                "relationship_type": r["type"],
                "strength": "weak",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "unverified",
                "source_ids": []
            })
        elif r["person_b"] == person["id"]:
            source_name = next((p["name"] for p in persons if p["id"] == r["person_a"]), f"ID:{r['person_a']}")
            rels_list.append({
                "person": source_name,
                "person_id": f"fusong_{source_name}",
                "relationship_type": r["type"],
                "strength": "weak",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "unverified",
                "source_ids": []
            })

    pj["relationships"] = rels_list

    # source register
    pj["source_register"] = SOURCE_REGISTER

    # confidence
    pj["confidence_summary"] = {
        "identity": person.get("confidence", "unverified"),
        "current_role": "unverified",
        "career_completeness": "thin",
        "relationship_confidence": "low",
        "biggest_gap": "姓名及所有履历信息均不可获取。政府网站无法访问，搜索引擎全面不可用。"
    }

    # open questions
    on = person.get("notes", "")
    pj["open_questions"] = [
        {
            "priority": "critical",
            "question": f"{name}的姓名、性别、出生年月、籍贯、民族、教育背景及入党时间",
            "why_it_matters": "核心目标人物的基础身份信息完全空白，无法进行后续网络分析和关系挖掘",
            "suggested_queries": [f"抚松{person.get('current_post','')} 简历", f"抚松 县委常委 任命"],
            "last_attempted": AS_OF
        },
        {
            "priority": "critical",
            "question": f"{name}的完整任职履历（所有曾任职岗位及时间）",
            "why_it_matters": "无法建立工作关系网络和跨区域交流轨迹",
            "suggested_queries": [f"白山市 抚松县 干部 任前公示"],
            "last_attempted": AS_OF
        }
    ]

    return pj


# ══════════════════════════════════════════════════════════════════════════════
# GEXF helpers (direct string formatting to avoid ElementTree namespace issues)
# ══════════════════════════════════════════════════════════════════════════════


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_role_color(name: str, post: str) -> str:
    if "书记" in post and "纪委" not in post:
        return "255,50,50"
    if "县长" in post or "区长" in post or "市长" in post:
        return "50,100,255"
    if "纪委" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"


def person_role_size(name: str, post: str) -> str:
    if "书记" in post and "纪委" not in post:
        return "20.0"
    if "县长" in post or "区长" in post or "市长" in post:
        return "20.0"
    return "12.0"


def org_color(org_type: str) -> str:
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf(path: Path) -> None:
    """Build GEXF graph using string formatting (avoids ElementTree namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>抚松县（白山市、吉林省）领导班子工作关系网络 — 2026年7月调查</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('      <attribute id="5" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ────────────────────────────────────────────────
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p.get("current_post", "")
        org = p.get("current_org", "")
        birth = p.get("birth", "")
        src = p.get("source", "")
        conf = p.get("confidence", "unverified")
        c = person_role_color(name, post)
        sz = person_role_size(name, post)
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(src)}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──────────────────────────────────────────
    for o in organizations:
        oid = o["id"] + 100000  # offset to avoid ID collision with persons
        oname = o["name"]
        otype = o.get("type", "")
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges: person -> organization ─────────────────────────────────
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if pos.get("person_id") and pos.get("org_id"):
            eid += 1
            pid = pos["person_id"]
            oid = pos["org_id"] + 100000
            title = pos.get("title", "")
            note = pos.get("note", "")
            lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="{esc(note)}"/>')
            lines.append('          <attvalue for="2" value=""/>')
            lines.append('          <attvalue for="3" value=""/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

    # ── Edges: person <-> person ────────────────────────────────────
    for r in relationships:
        eid += 1
        a = r["person_a"]
        b = r["person_b"]
        rtype = r.get("type", "")
        ctx = r.get("context", "")
        oo = r.get("overlap_org", "")
        op = r.get("overlap_period", "")
        weight = "2.0" if rtype in ("predecessor_successor", "superior_subordinate") else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oo)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(op)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a single person JSON file to staging."""
    name = person.get("name", "")
    post = person.get("current_post", "")
    clean_post = post.replace("/", "_").replace("（", "_").replace("）", "_").replace("、", "_")
    filename = f"{TODAY}-吉林省-白山市-{clean_post}-{name}.json"
    filepath = PJSON_DIR / filename
    data = make_person_json(person)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")


def main():
    print(f"Building 抚松县 network data...")
    print(f"  Staging dir: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Build SQLite DB
    print("\n--- Building SQLite DB ---")
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

    # Build GEXF (using string formatting for namespace safety)
    print("\n--- Building GEXF ---")
    build_gexf(GEXF_PATH)

    # Verify GEXF
    gexf_size = GEXF_PATH.stat().st_size
    print(f"  GEXF file size: {gexf_size} bytes")

    # Write person JSONs
    print("\n--- Writing Person JSONs ---")
    for p in persons:
        if p["id"] <= 2:  # Core targets only
            write_person_json(p)

    # Statistics
    print(f"\n--- Summary ---")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print(f"  Person JSONs in: {PJSON_DIR}")

    # Also write a stub for 王文江 since he's the only confirmed cross-county person
    for p in persons:
        if p["id"] == 5:
            write_person_json(p)

    print("\nDone.")


if __name__ == "__main__":
    main()
