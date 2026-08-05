#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新安县 (Xin'an County), 洛阳市, 河南省.

Level: 县
Province: 河南省
Parent city: 洛阳市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: henan_新安县

Research date: 2026-08-05
Primary source: 新安县人民政府官网 http://www.xinan.gov.cn/ (政府领导 pages + official news)

Current status (as of 2026-08-05):
- 县委书记: 王智 (confirmed via official news — 县委书记、县人武部党委第一书记)
- 县长: 崔占科 (confirmed via official government leader profile — 县委副书记、县政府党组书记、县长)

Government leadership roster confirmed via 政府领导 pages (9 members):
  崔占科（县长）, 刘忻（常务副县长）, 宋良（宣传部长兼副县长）, 程嘉（挂职副县长）,
  刘国栋（副县长）, 李然（挂职副县长）, 赵卫锋（副县长/公安局长）, 李航（副县长）, 张利博（副县长）

Confidence notes:
  Web search (Exa) was rate-limited and Baidu/Bing/Jina Reader timed out during research.
  The official 新安县人民政府 website (www.xinan.gov.cn) was fully accessible and provided
  the government leaders' profiles and current news confirming the party secretary.
  Current roster and identity fields are confirmed from official sources.
  Full career histories of 王智 and 崔占科 before their current posts, the predecessor
  县委书记, and the remaining party-committee standing members (纪委书记/组织部长/政法书记/
  专职副书记) are NOT yet confirmed from official pages; these are encoded as open gaps
  (confidence: unverified/plausible).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "新安县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

# Canonical destinations (used when the promoted script is re-run directly)
CANONICAL_DB = _REPO_ROOT / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = _REPO_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_PERSONS = _REPO_ROOT / "data" / "persons"

import sqlite3  # noqa: F811, E402

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ Core Leadership (Primary Targets) ═══
    {
        "id": 1,
        "name": "王智",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共新安县委书记",
        "current_org": "中共新安县委员会",
        "source": "confirmed — 新安县政府官网新闻（2026-08-03/07-31：县委书记王智主持县委常委会、议军会议）",
    },
    {
        "id": 2,
        "name": "崔占科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县人民政府县长",
        "current_org": "新安县人民政府",
        "source": "confirmed — 新安县政府官网政府领导页（崔占科 个人简历）",
    },
    # ═══ Government Leadership Team (confirmed) ═══
    {
        "id": 3,
        "name": "刘忻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-04",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县委常委、县政府党组副书记、常务副县长",
        "current_org": "新安县人民政府",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    {
        "id": 4,
        "name": "宋良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-03",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县委常委、宣传部部长，县政府党组成员、副县长",
        "current_org": "中共新安县委宣传部",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    {
        "id": 5,
        "name": "程嘉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "",
        "education": "博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县人民政府副县长（挂职一年）",
        "current_org": "新安县人民政府",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    {
        "id": 6,
        "name": "刘国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-04",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "新安县人民政府",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    {
        "id": 7,
        "name": "李然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-08",
        "birthplace": "",
        "education": "博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长（挂职两年）",
        "current_org": "新安县人民政府",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    {
        "id": 8,
        "name": "赵卫锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长，县公安局局长、三级高级警长",
        "current_org": "新安县公安局",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    {
        "id": 9,
        "name": "李航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-08",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "新安县人民政府",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    {
        "id": 10,
        "name": "张利博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-02",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "新安县人民政府",
        "source": "confirmed — 新安县政府官网政府领导页",
    },
    # ═══ Party Committee Standing Committee (names not yet on government site) ═══
    {
        "id": 11,
        "name": "（纪委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县委常委、纪委书记、监委主任",
        "current_org": "中共新安县纪律检查委员会",
        "source": "待查 — 需通过新安县纪委或洛阳市委组织部公示确认",
    },
    {
        "id": 12,
        "name": "（组织部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县委常委、组织部长",
        "current_org": "中共新安县委组织部",
        "source": "待查",
    },
    {
        "id": 13,
        "name": "（政法委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县委常委、政法委书记",
        "current_org": "中共新安县委政法委员会",
        "source": "待查",
    },
    {
        "id": 14,
        "name": "（县委副书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新安县委副书记（专职）",
        "current_org": "中共新安县委员会",
        "source": "待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共新安县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "河南省洛阳市新安县"},
    {"id": 2, "name": "新安县人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "河南省洛阳市新安县"},
    {"id": 3, "name": "新安县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南省洛阳市新安县"},
    {"id": 4, "name": "中国人民政治协商会议新安县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河南省洛阳市新安县"},
    {"id": 5, "name": "中共新安县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共新安县委员会", "location": "河南省洛阳市新安县"},
    {"id": 6, "name": "新安县监察委员会", "type": "党委", "level": "县处级", "parent": "中共新安县委员会", "location": "河南省洛阳市新安县"},
    {"id": 7, "name": "中共新安县委组织部", "type": "党委", "level": "县处级", "parent": "中共新安县委员会", "location": "河南省洛阳市新安县"},
    {"id": 8, "name": "中共新安县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共新安县委员会", "location": "河南省洛阳市新安县"},
    {"id": 9, "name": "中共新安县委宣传部", "type": "党委", "level": "县处级", "parent": "中共新安县委员会", "location": "河南省洛阳市新安县"},
    {"id": 10, "name": "新安县公安局", "type": "政府", "level": "县处级", "parent": "新安县人民政府", "location": "河南省洛阳市新安县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王智 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "新安县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "到任时间待确认；兼任县人武部党委第一书记"},
    # 崔占科 — 县长
    {"person_id": 2, "org_id": 2, "title": "新安县人民政府县长", "start": "", "end": "present", "rank": "县处级正职", "note": "到任时间待确认"},
    {"person_id": 2, "org_id": 1, "title": "新安县委副书记、县政府党组书记", "start": "", "end": "present", "rank": "县处级副职", "note": "兼任县委副书记、县政府党组书记"},
    # 刘忻 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "新安县委常委、县政府党组副书记、常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "常务副县长"},
    {"person_id": 3, "org_id": 1, "title": "新安县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "县委常委会成员"},
    # 宋良 — 宣传部长、副县长
    {"person_id": 4, "org_id": 9, "title": "新安县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "县委宣传部部长"},
    {"person_id": 4, "org_id": 2, "title": "县政府党组成员、副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 程嘉 — 挂职副县长
    {"person_id": 5, "org_id": 2, "title": "新安县人民政府副县长（挂职一年）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    # 刘国栋 — 副县长
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 李然 — 挂职副县长
    {"person_id": 7, "org_id": 2, "title": "县政府党组成员、副县长（挂职两年）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    # 赵卫锋 — 副县长、公安局长
    {"person_id": 8, "org_id": 2, "title": "县政府党组成员、副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "新安县公安局党委书记、局长、三级高级警长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 李航 — 副县长
    {"person_id": 9, "org_id": 2, "title": "县政府党组成员、副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张利博 — 副县长
    {"person_id": 10, "org_id": 2, "title": "县政府党组成员、副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # Party committee standing members (待确认)
    {"person_id": 11, "org_id": 5, "title": "新安县委常委、纪委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 11, "org_id": 6, "title": "新安县监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 12, "org_id": 7, "title": "新安县委常委、组织部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 13, "org_id": 8, "title": "新安县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 14, "org_id": 1, "title": "新安县委副书记（专职）", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王伟 ↔ 崔防科 (core leadership pair: 书记+县长)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长党政主要领导搭档关系，共同主持新安县委常委会和县政府重要工作",
        "overlap_org": "中共新安县委员会/新安县人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 王伟 ↔ 刘琪（书记与常务副县长）
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委书记与常务副县长在新安县委常委会和县政府党组层面均有工作交集",
        "overlap_org": "中共新安县委员会/新安县人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "plausible",
    },
    # 崔占科 ↔ 刘琪（县役与常务副县长）
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长在县政府党组和县政府班子中的上下级工作关系",
        "overlap_org": "新安县人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "plausible",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    pid = person["id"]
    is_top = "县委书记" in person["current_post"] or (person["current_post"].find("县长") != -1 and "副县" not in person["current_post"])
    admin_rank = "县处级正职" if is_top else "县处级副职"

    career_entries = []
    for pos in positions:
        if pos["person_id"] == pid:
            note = pos["note"]
            conf = "plausible"
            if "待确认" not in note and "待核实" not in note and "待查" not in note:
                conf = "confirmed" if pid in (1, 2, 3) else "plausible"
            career_entries.append({
                "start": pos["start"] if pos["start"] else "unknown",
                "end": pos["end"] if pos["end"] else "unknown",
                "org": _org_name(pos["org_id"]),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "河南省洛阳市新安县",
                "system": "party" if "县委" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": "县委书记" in pos["title"] or "县长" in pos["title"],
                "notes": note,
                "confidence": conf,
                "source_ids": ["S001", "S002", "S003"] if pid in (1, 2, 3) else [],
            })

    if not career_entries:
        career_entries = [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": admin_rank,
                "location": "河南省洛阳市新安县",
                "system": "party" if "书记" in person["current_post"] and "副" not in person["current_post"].split("书记")[0] else "government",
                "rank": admin_rank,
                "is_key_promotion": is_top,
                "notes": "完整履历需通过洛阳市委组织部任前公示或媒体披露补充。",
                "confidence": "unverified",
                "source_ids": [],
            }
        ]

    rels_out = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        rels_out.append({
            "person": _person_name(other_id),
            "person_id": f"xin_an_{_slugify_name(_person_name(other_id))}",
            "relationship_type": r["type"],
            "strength": "strong" if r["type"] == "overlap" else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r.get("confidence", "plausible"),
            "source_ids": [],
        })

    orgs_out = []
    for pos in positions:
        if pos["person_id"] == pid:
            orgs_out.append({
                "org_id": pos["org_id"],
                "name": _org_name(pos["org_id"]),
                "type": _org_type(pos["org_id"]),
                "level": "县处级",
                "location": "河南省洛阳市新安县",
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "洛阳市",
            "region": "新安县",
            "job": person["current_post"],
            "task_id": "henan_新安县",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": f"xin_an_{_slugify_name(person['name'])}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person["education"],
                    "study_type": "unknown",
                    "source_ids": [0],
                }
            ] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "https://www.xinan.gov.cn/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": admin_rank,
            "as_of": AS_OF,
            "is_current_confirmed": not ("待确认" in person["name"]),
            "source_ids": [],
        },
        "career_timeline": career_entries,
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
                "summary": "无法充分评估 — 公开履历不完整",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "公开报道有限，暂无法对工作风格作出可靠推断。",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断需要公开报道、讲话和政府工作报告作为依据。当前阶段证据不足以进行可靠分析。",
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "memberships": len(orgs_out),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "在本次调研条件下未发现公开廉洁风险信号。此状态不代表无问题，仅表示在有限条件下未发现。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "新安县人民政府官网 — 政府领导（崔占科）",
                "url": "https://www.xinan.gov.cn/2026/01-04/1033438.html",
                "publisher": "新安县人民政府",
                "published_at": "2026-01-04",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "崔占科（县长）个人简历官方页。",
            },
            {
                "id": "S002",
                "title": "新安县人民政府官网 — 政府领导（全体）",
                "url": "https://www.xinan.gov.cn/wzsy/zwgk/zfld/",
                "publisher": "新安县人民政府",
                "published_at": "2026",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "新安县政府领导班子全体成员（含挂职）名单与简历。",
            },
            {
                "id": "S003",
                "title": "新安要闻 — 县委书记王智主持县委常委会/议军会议",
                "url": "https://www.xinan.gov.cn/2026/08-03/1077300.html",
                "publisher": "新安县融媒体中心",
                "published_at": "2026-08-03",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方新闻确认 县委书记、县人武部党委第一书记 为王智。",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "王智的县委书记到任时间与其此前任职、前任县委书记去向、其余县委常委会成员（纪委、组织、政法、专职副书记）等未获官方独立核实。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}在现任职务之前担任什么职务？到任时间为何？",
                "why_it_matters": "核心目标人物履历，用于判断晋升路径和跨县交流背景。",
                "suggested_queries": [
                    f"{person['name']} 新安县 县委书记 任命",
                    f"{person['name']} 任职公示",
                    "洛阳市 组织部 新安 干部任免",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "前任新安县委书记是谁？去哪了？",
                "why_it_matters": "深入了解前任去向有助于反推本地干部流动与可能的跨县交流网络。",
                "suggested_queries": [
                    "新安县 前任 县委书记",
                    "新安县 县委书记 卸任",
                    "洛阳市 县处级 干部 交流",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "新安县委常委会其他成员（纪委书记、组织部长、政法书记、专职副书记）实名人选？",
                "why_it_matters": "构建完整县级领导班子网络图。",
                "suggested_queries": [
                    "新安县委 领导班子",
                    "新安县 领导分工",
                    "新安县 任前公示 县委",
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
    return name.replace("（", "_").replace("）", "").replace(" ", "_")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_jsons():
    """Write individual person JSON files for the core figures."""
    core_ids = {1, 2, 3, 4}  # 书记王智、县长崔占科、常务副县长刘忻、宣传部长宋良
    for p in persons:
        if p["id"] not in core_ids:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)
        name_part = _slugify_name(p["name"])
        fname = f"{TODAY}-河南省-洛阳市-{_slugify_job(p['current_post'])}-{name_part}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")


def _slugify_job(post: str) -> str:
    if "县委书记" in post:
        return "县委书记"
    if "县长" in post and "副县长" not in post:
        return "县长"
    if "常务副县长" in post:
        return "常务副县长"
    if "县委副书记" in post or ("副书记" in post and "县委" in post):
        return "县委副书记"
    if "纪委书记" in post:
        return "纪委书记"
    if "组织部长" in post:
        return "组织部长"
    if "宣传部长" in post:
        return "宣传部长"
    if "政法" in post:
        return "政法书记"
    if "副县长" in post:
        return "副县长"
    if "部长" in post:
        return "部长"
    return post.replace(" ", "_")


def main():
    print(f"=== Building network for {SLUG} ===")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()

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

    print(">>> Writing person JSON files...")
    write_person_jsons()
    print()

    print("=== Build complete ===")
    print(f"  Database:  {DB_PATH} ({os.path.getsize(DB_PATH)} bytes)")
    print(f"  GEXF:      {GEXF_PATH} ({os.path.getsize(GEXF_PATH)} bytes)")
    print(f"  Persons:   {len(persons)}")
    print(f"  Orgs:      {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    print()

    # Copy staged artifacts to canonical repo locations so re-running the
    # promoted script stays consistent with process_tmp promotion.
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    for p in persons:
        if p["id"] not in {1, 2, 3, 4}:
            continue
        job = _slugify_job(p["current_post"])
        name_part = _slugify_name(p["name"])
        src = PERSONS_DIR / f"{TODAY}-河南省-洛阳市-{job}-{name_part}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Canonical person JSON: {dst}")

    print(f"\n  Canonical DB:  {CANONICAL_DB}")
    print(f"  Canonical GEXF:{CANONICAL_GEXF}")
    print()
    print("NOTE: Current roster confirmed from official government site (2026-01/08).")
    print("      Full pre-seat careers of 王智/崔占科, predecessor 书记, and remaining")
    print("      县委常委 (纪委/组织/政法/专职副书记) remain open gaps.")


if __name__ == "__main__":
    main()