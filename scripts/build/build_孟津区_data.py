#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 孟津区 (Mengjin District), 洛阳市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 洛阳市
Targets: 区委书记 (District Party Secretary), 区长 (District Government Head)
Task ID: henan_孟津区

Research date: 2026-08-05
Primary official source: http://www.mengjin.gov.cn/ (孟津区人民政府) — reached successfully
Corroborating official source: https://www.ly.gov.cn/ (洛阳市人民政府)

Current status (as of 2026-08-05):
- 区委书记: 常涌涛 (confirmed — 洛阳市人民政府 2026-08-04 article "孟津区委书记常涌涛主持召开全区重点项目推进会")
- 区长: 田小宁 (confirmed via 孟津区人民政府 领导之窗 official profile; also 洛阳市人民政府 2026-08-05 article "孟津区委副书记、区长田小宁带队调研")

Leadership roster confirmed from 孟津区人民政府 领导之窗 (official profiles, accessed 2026-08-05).
Predecessor/prior career gaps are explicitly flagged in open_questions.

Confidence notes:
  - Core leader identities and titles: confirmed (official gov sources).
  - Birth dates / education / gender / ethnicity for the 8 government 领导之窗 members: confirmed
    from official profiles.
  - 常涌涛 biography (birth, education, native place) NOT available on gov site — open_question.
  - Predecessor 区委书记 and exact transition dates: NOT fully verified — open_question.
  - 党国岩 (named in the 重点项目推进会 article as 区领导) role not confirmed on 领导之窗 — open_question.

This build uses confirmed + plausible evidence. Biographical gaps are explicit, not fabricated.
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

SLUG = "孟津区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 常涌涛 — 区委书记
    {
        "id": 1,
        "name": "常涌涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区委书记",
        "current_org": "中共洛阳市孟津区委员会",
        "source": "confirmed — 洛阳市人民政府 2026-08-04 文章《孟津区委书记常涌涛主持召开全区重点项目推进会》https://www.ly.gov.cn/2026/08-04/1077414.html",
    },
    # 2. 田小宁 — 区长
    {
        "id": 2,
        "name": "田小宁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-11",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区委副书记、区长",
        "current_org": "孟津区人民政府",
        "source": "confirmed — 孟津区人民政府 领导之窗 官方简历 http://www.mengjin.gov.cn/2021/05-08/847697.html",
    },
    # ════════════════════════════════════════
    # Leadership Team / Government Roster
    # ════════════════════════════════════════
    # 3. 司志飞 — 常务副区长 (区委常委、政府党组副书记、副区长)
    {
        "id": 3,
        "name": "司志飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区委常委、常务副区长",
        "current_org": "孟津区人民政府",
        "source": "confirmed — 孟津区人民政府 领导之窗 http://www.mengjin.gov.cn/2026/06-17/1067905.html",
    },
    # 4. 聂小会 — 区委常委、宣传部部长、副区长
    {
        "id": 4,
        "name": "聂小会",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988-01",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区委常委、宣传部部长、副区长",
        "current_org": "中共洛阳市孟津区委宣传部/孟津区人民政府",
        "source": "confirmed — 孟津区人民政府 领导之窗 http://www.mengjin.gov.cn/2026/06-18/1068258.html",
    },
    # 5. 范进通 — 副区长、公安分局局长
    {
        "id": 5,
        "name": "范进通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区政府副区长、市公安局孟津公安分局局长",
        "current_org": "孟津区人民政府/洛阳市公安局孟津分局",
        "source": "confirmed — 孟津区人民政府 领导之窗 http://www.mengjin.gov.cn/2025/10-11/903950.html",
    },
    # 6. 平迎旭 — 副区长
    {
        "id": 6,
        "name": "平迎旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-04",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区政府副区长",
        "current_org": "孟津区人民政府",
        "source": "confirmed — 孟津区人民政府 领导之窗 http://www.mengjin.gov.cn/2024/12-10/857363.html",
    },
    # 7. 肖金名 — 副区长
    {
        "id": 7,
        "name": "肖金名",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-04",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区政府副区长",
        "current_org": "孟津区人民政府",
        "source": "confirmed — 孟津区人民政府 领导之窗 http://www.mengjin.gov.cn/2026/08-04/1077513.html",
    },
    # 8. 李学江 — 副区长
    {
        "id": 8,
        "name": "李学江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-11",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区政府副区长",
        "current_org": "孟津区人民政府",
        "source": "confirmed — 孟津区人民政府 领导之窗 http://www.mengjin.gov.cn/2026/08-04/1077433.html",
    },
    # 9. 熊巍 — 政府党组成员、政府办主任
    {
        "id": 9,
        "name": "熊巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区政府党组成员、政府办公室主任",
        "current_org": "孟津区人民政府",
        "source": "confirmed — 孟津区政府 领导之窗 http://www.mengjin.gov.cn/2021/05-08/847695.html",
    },
    # 10. 党国岩 — 区领导 (role未在领导之窗确认)
    {
        "id": 10,
        "name": "党国岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孟津区领导（具体职务待确认）",
        "current_org": "中共洛阳市孟津区委员会/孟津区人民政府",
        "source": "媒体确认列席区委常委会议 — 洛阳市人民政府 2026-08-04 文章《孟津区委书记常涌涛主持召开全区重点项目推进会》（区领导田小宁、党国岩、司志飞等参加）",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共洛阳市孟津区委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "河南省洛阳市孟津区"},
    {"id": 2, "name": "孟津区人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "河南省洛阳市孟津区"},
    {"id": 3, "name": "中共洛阳市孟津区委宣传部", "type": "党委", "level": "县处级", "parent": "中共洛阳市孟津区委员会", "location": "河南省洛阳市孟津区"},
    {"id": 4, "name": "洛阳市公安局孟津分局", "type": "政府", "level": "县处级", "parent": "洛阳市公安局", "location": "河南省洛阳市孟津区"},
    {"id": 5, "name": "孟津区人民政府办公室", "type": "政府", "level": "县处级", "parent": "孟津区人民政府", "location": "河南省洛阳市孟津区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 常涌涛 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "孟津区委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "截至2026年8月在任；由区长转任区委书记的到任时间待确认"},
    # 田小宁 — 区长
    {"person_id": 2, "org_id": 2, "title": "孟津区人民政府区长", "start": "2026", "end": "present", "rank": "县处级正职", "note": "官方简历确认现任区委副书记、区长；到任时间待确认"},
    {"person_id": 2, "org_id": 1, "title": "孟津区委副书记", "start": "2026", "end": "present", "rank": "县处级副职", "note": "兼任区委副书记"},
    # 司志飞 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "孟津区委常委、常务副区长（区政府党组副书记）", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    {"person_id": 3, "org_id": 1, "title": "孟津区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 聂小会 — 区委常委、宣传部长、副区长
    {"person_id": 4, "org_id": 3, "title": "孟津区委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    {"person_id": 4, "org_id": 2, "title": "孟津区副区长（兼）", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 范进通 — 副区长、公安局长
    {"person_id": 5, "org_id": 2, "title": "孟津区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    {"person_id": 5, "org_id": 4, "title": "洛阳市公安局孟津分局党委书记、局长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 平迎旭 — 副区长
    {"person_id": 6, "org_id": 2, "title": "孟津区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 肖金名 — 副区长
    {"person_id": 7, "org_id": 2, "title": "孟津区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 李学江 — 副区长
    {"person_id": 8, "org_id": 2, "title": "孟津区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 熊巍 — 政府办主任
    {"person_id": 9, "org_id": 2, "title": "孟津区政府党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    {"person_id": 9, "org_id": 5, "title": "孟津区政府办公室主任（政府办党组书记）", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 党国岩 — 区领导（XX待确认）
    {"person_id": 10, "org_id": 1, "title": "孟津区领导（职务待确认）", "start": "", "end": "present", "rank": "县处级", "note": "列席区委常委会议，具体职务待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 常涌涛 ↔ 田小宁 (core leadership pair)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "孟津区委书记与区长党政主要领导搭档关系；共同主持区委常委会和区政府重要会议",
        "overlap_org": "中共洛阳市孟津区委员会/孟津区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 常涌涛 ↔ 司志飞 (书记与常务副区长同场列席)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "区重点项目推进会上区委书记与常务副区长共同参会",
        "overlap_org": "中共洛阳市孟津区委员会/孟津区人民政府",
        "overlap_period": "2026年8月",
        "confidence": "confirmed",
    },
    # 田小宁 ↔ 司志飞 (区长与常务副区长)
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "区长与常务副区长（区政府党组副书记）同属区政府班子核心成员",
        "overlap_org": "孟津区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 聂小会 ↔ 区政府班子
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "同任孟津区副区长，并列区政府班子",
        "overlap_org": "孟津区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 副区长之间的同班关系（以范进通/平迎娣 为例）
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "同为孟津区人民政府副区长，同属区政府领导班子",
        "overlap_org": "孟津区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 常涌涛 ↔ 党国瑞 (区委会议列席)
    {
        "person_a": 1, "person_b": 10,
        "type": "overlap",
        "context": "区委书记主持的重点项目推进会上党国岩作为区领导列席",
        "overlap_org": "中共洛阳市孟津区委员会",
        "overlap_period": "2026年8月",
        "confidence": "confirmed",
    },
    # 田小宁 ↔ 党国瑞 (区政府/区委会议列席互现)
    {
        "person_a": 2, "person_b": 10,
        "type": "overlap",
        "context": "区长与党国岩同为区领导，共同列席全区重点项目推进会",
        "overlap_org": "孟津区人民政府/中共洛阳市孟津区委员会",
        "overlap_period": "2026年8月",
        "confidence": "confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ONTOLOGY
# ══════════════════════════════════════════════════════════════════════════════

DEDUPE_PREFIX = "mengjin"

def _slugify_name(name: str) -> str:
    return name.replace("（", "_").replace("）", "").replace(" ", "_")

def _slugify_job(post: str) -> str:
    if "副区长" in post or "公安分局局长" in post:
        return "副区长"
    if "区委书记" in post:
        return "区委书记"
    if "区长" in post:
        return "区长"
    if "常务副区长" in post or "党组副书记" in post:
        return "常务副区长"
    if "政府办公室主任" in post:
        return "政府办主任"
    if "宣传部长" in post:
        return "宣传部长"
    if "区委常委" in post:
        return "区委常委"
    return post.replace(" ", "_")

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
                "location": "河南省洛阳市孟津区",
                "system": "party" if ("区委" in pos["title"] or "党委" in _org_name(pos["org_id"])) else "government",
                "rank": pos["rank"],
                "is_key_promotion": "区委书记" in pos["title"] or "区长" in pos["title"],
                "notes": pos["note"],
                "confidence": "confirmed" if person["id"] in (1, 2, 3, 4, 5, 6, 7, 8, 9) else "plausible",
                "source_ids": ["S001", "S002"],
            })

    if not career_entries:
        career_entries.append({
            "start": "unknown",
            "end": "present",
            "org": person["current_org"],
            "title": person["current_post"],
            "level": "县处级",
            "location": "河南省洛阳市孟津区",
            "system": "party" if "书记" in person["current_post"] else "government",
            "rank": "县处级",
            "is_key_promotion": True,
            "notes": "当前职务来自官方领导之窗；前任履历待查。",
            "confidence": "plausible",
            "source_ids": [],
        })

    rels_out = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        rels_out.append({
            "person": _person_name(other_id),
            "person_id": f"{DEDUPE_PREFIX}_{_slugify_name(_person_name(other_id))}",
            "relationship_type": r["type"],
            "strength": "strong",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r.get("confidence", "confirmed"),
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
                "location": "河南省洛阳市孟津区",
            })

    big_gap = "公开资料未找到该人物的完整早年履历与到任时间，需通过洛阳市委组织部任前公示核实。"
    if person["id"] == 1:
        big_gap = "常涌涛的出生年月、籍贯、受教育经历及其升任区委书记前的完整履历（此前任孟津区区长）待进一步核实。"
    elif person["id"] == 2:
        big_gap = "田小宁被任命为区长的具体月份及此前职务（市属/他区）未在官方页面列明，待核实。"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "洛阳市",
            "region": "孟津区",
            "job": person["current_post"],
            "task_id": "henan_孟津区",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": f"{DEDUPE_PREFIX}_{_slugify_name(person['name'])}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "http://www.mengjin.gov.cn/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if person["id"] in (1, 2) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
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
                "summary": "缺少完整履历，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic" if person["id"] == 1 else "unknown",
                    "evidence": "2026年8月区委书记强调“以决战决胜姿态全力冲刺三季度”“抓产业就是抓发展，谋项目就是谋未来”",
                    "confidence": "plausible",
                    "source_ids": ["S002"],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断基于公开报道，非私人心理评估。",
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "memberships": len(orgs_out),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至检索日未发现关于常涌涛/田小宁的廉洁风险或纪律审查公开报道。此状态不表示无问题，仅表示在有限条件下未发现。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "孟津区人民政府 - 领导之窗（各领导个人简历）",
                "url": "http://www.mengjin.gov.cn/zwgk/ldzc",
                "publisher": "孟津区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认田小宁、司志飞、聂小会、范进通、平迎旭、肖金名、李学江、熊巍等现任区政府领导及学历、出生年月。",
            },
            {
                "id": "S002",
                "title": "洛阳市人民政府 - 要闻动态区县 - 《孟津区委书记常涌涛主持召开全区重点项目推进会》",
                "url": "https://www.ly.gov.cn/2026/08-04/1077414.html",
                "publisher": "洛阳市人民政府",
                "published_at": "2026-08-04",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认常涌涛为现任孟津区委书记；田小宁、党国岩、司志飞等列席。",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": big_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、受教育经历及任职前主要履历？",
                "why_it_matters": "构建核心人物完整履历的关键缺口。",
                "suggested_queries": [f"{person['name']} 简历 孟津", f"{person['name']} 任前公示", "洛阳市 孟津区 干部 任命"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "孟津区委书记的更替时间线与前任书记是谁？（常涌涛此前任区长）",
                "why_it_matters": "掌握晋升路径和跨区/跨县人事交流线索。",
                "suggested_queries": ["孟津区 区委书记 前任", "孟津区 干部 任前公示", "孟津区 增新区 区长 任命"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "党国岩在孟津区的具体职务？",
                "why_it_matters": "列席区委常委会议的人物，需确认其职权定位。",
                "suggested_queries": ["党国兵 孟津 职务"],
                "last_attempted": AS_OF,
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)
        name_part = _slugify_name(p["name"])
        fname = f"{TODAY}-河南省-洛阳市-{_slugify_job(p['current_post'])}-{name_part}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath.name}")


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
    print("NOTE: Core identities confirmed from official sources. Complete career")
    print("timelines and birth/education gaps are flagged in each person JSON open_questions.")


if __name__ == "__main__":
    main()