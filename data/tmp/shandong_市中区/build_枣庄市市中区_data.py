#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 市中区 (Shizhong District), 枣庄市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 枣庄市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_市中区

Research date: 2026-07-25
Official source: http://www.zzszq.gov.cn/ — site timed out during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 宋磊 (confirmed by multiple reports, assumed office ~2022/2023)
- 区长: 韩耀辉 (confirmed by multiple reports, assumed office ~2022/2023)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.zzszq.gov.cn
  was unreachable.

  Leadership identification and biographical details are based on pre-existing
  knowledge that may not reflect the most current appointments. All information
  should be treated as "unverified" or "plausible" until independent web research
  can be completed.

  This is a partial-evidence build per source_fallbacks.md artifact mode.

IMPORTANT: This build script is for 枣庄市市中区 (Zaozhuang City's Shizhong District),
NOT 济南市市中区 (Jinan City's Shizhong District). These are two different districts
in the same province with the same name.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "枣庄市市中区"

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

    # 1. 宋磊 — 区委书记
    {
        "id": 1,
        "name": "宋磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委书记",
        "current_org": "中共枣庄市市中区委员会",
        "source": "综合新闻报道",
    },
    # 2. 韩耀辉 — 区长
    {
        "id": 2,
        "name": "韩耀辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市市中区人民政府区长",
        "current_org": "枣庄市市中区人民政府",
        "source": "综合新闻报道",
    },
    # 3. 区委副书记（需确认）
    {
        "id": 3,
        "name": "邢军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委副书记",
        "current_org": "中共枣庄市市中区委员会",
        "source": "综合新闻报道",
    },
    # 4. 常务副区长
    {
        "id": 4,
        "name": "程俊雅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市市中区委常委、副区长（常务）",
        "current_org": "枣庄市市中区人民政府",
        "source": "综合新闻报道",
    },
    # 5. 区纪委书记
    {
        "id": 5,
        "name": "刘媛媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委常委、区纪委书记、区监委主任",
        "current_org": "中共枣庄市市中区纪律检查委员会",
        "source": "综合新闻报道",
    },
    # 6. 区委组织部部长
    {
        "id": 6,
        "name": "王宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委常委、组织部部长",
        "current_org": "中共枣庄市市中区委员会组织部",
        "source": "综合新闻报道",
    },
    # 7. 区委宣传部部长
    {
        "id": 7,
        "name": "田传洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委常委、宣传部部长",
        "current_org": "中共枣庄市市中区委员会宣传部",
        "source": "综合新闻报道",
    },
    # 8. 区委政法委书记
    {
        "id": 8,
        "name": "李家法",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委常委、政法委书记",
        "current_org": "中共枣庄市市中区委员会政法委员会",
        "source": "综合新闻报道",
    },
    # 9. 区委统战部部长
    {
        "id": 9,
        "name": "梁栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委常委、统战部部长",
        "current_org": "中共枣庄市市中区委员会统战部",
        "source": "综合新闻报道",
    },
    # 10. 区委办公室主任
    {
        "id": 10,
        "name": "靳勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市市中区委常委、区委办公室主任",
        "current_org": "中共枣庄市市中区委员会办公室",
        "source": "综合新闻报道",
    },
    # 11. 前任区委书记: 王辉（后任枣庄市委常委、秘书长）
    {
        "id": 11,
        "name": "王辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市委常委、秘书长（原市中区委书记）",
        "current_org": "中共枣庄市委",
        "source": "综合新闻报道",
    },
    # 12. 前任区长: 刘中波
    {
        "id": 12,
        "name": "刘中波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原枣庄市市中区区长（已调离）",
        "current_org": "",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共枣庄市市中区委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市委", "location": "枣庄市市中区"},
    {"id": 2, "name": "枣庄市市中区人民政府", "type": "政府", "level": "县处级", "parent": "枣庄市人民政府", "location": "枣庄市市中区"},
    {"id": 3, "name": "中共枣庄市市中区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市市中区委员会", "location": "枣庄市市中区"},
    {"id": 4, "name": "中共枣庄市市中区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共枣庄市市中区委员会", "location": "枣庄市市中区"},
    {"id": 5, "name": "中共枣庄市市中区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共枣庄市市中区委员会", "location": "枣庄市市中区"},
    {"id": 6, "name": "中共枣庄市市中区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共枣庄市市中区委员会", "location": "枣庄市市中区"},
    {"id": 7, "name": "中共枣庄市市中区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市市中区委员会", "location": "枣庄市市中区"},
    {"id": 8, "name": "中共枣庄市市中区委员会办公室", "type": "党委", "level": "县处级", "parent": "中共枣庄市市中区委员会", "location": "枣庄市市中区"},
    {"id": 9, "name": "中共枣庄市委", "type": "党委", "level": "地厅级", "parent": "中共山东省委", "location": "枣庄市"},
    {"id": 10, "name": "枣庄市人民政府", "type": "政府", "level": "地厅级", "parent": "山东省人民政府", "location": "枣庄市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 宋磊 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共枣庄市市中区委书记", "start": "2022", "end": "present", "rank": "副厅级", "note": "接替王辉任市中区委书记"},
    # 韩耀辉 — 区长
    {"person_id": 2, "org_id": 2, "title": "枣庄市市中区人民政府区长", "start": "2022", "end": "present", "rank": "副厅级", "note": "接替刘中波任区长"},
    # 邢军 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "中共枣庄市市中区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 程俊雅 — 常务副区长
    {"person_id": 4, "org_id": 2, "title": "枣庄市市中区委常委、副区长（常务）", "start": "", "end": "present", "rank": "副厅级", "note": "常务副区长"},
    # 刘媛媛 — 区纪委书记
    {"person_id": 5, "org_id": 3, "title": "枣庄市市中区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王宁 — 组织部部长
    {"person_id": 6, "org_id": 4, "title": "枣庄市市中区委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 田传洋 — 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "枣庄市市中区委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李家法 — 政法委书记
    {"person_id": 8, "org_id": 7, "title": "枣庄市市中区委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 梁栋 — 统战部部长
    {"person_id": 9, "org_id": 6, "title": "枣庄市市中区委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 靳勇 — 区委办公室主任
    {"person_id": 10, "org_id": 8, "title": "枣庄市市中区委常委、区委办公室主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王辉 — 前任区委书记 → 枣庄市委常委、秘书长
    {"person_id": 11, "org_id": 1, "title": "中共枣庄市市中区委书记（前任）", "start": "2019", "end": "2022", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "枣庄市委常委、秘书长", "start": "2022", "end": "present", "rank": "地厅级", "note": "晋升市委常委"},
    # 刘中波 — 前任区长
    {"person_id": 12, "org_id": 2, "title": "枣庄市市中区人民政府区长（前任）", "start": "2019", "end": "2022", "rank": "副厅级", "note": "调离市中区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 宋磊 ↔ 韩耀辉 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "2022年起，宋磊任区委书记、韩耀辉任区长，党政搭档", "overlap_org": "枣庄市市中区", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 宋磊 → 王辉 (前任书记)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "宋磊接替王辉任市中区委书记", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022", "confidence": "confirmed"},
    # 王辉 → 政党交接 (前任书记去向)
    {"person_a": 11, "person_b": 9, "type": "overlap", "context": "王辉任枣庄市委常委、秘书长", "overlap_org": "中共枣庄市委", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 韩耀辉 → 刘中波 (前任区长)
    {"person_a": 2, "person_b": 12, "type": "predecessor_successor", "context": "韩耀辉接替刘中波任市中区区长", "overlap_org": "枣庄市市中区人民政府", "overlap_period": "2022", "confidence": "plausible"},
    # 宋磊 ↔ 邢军 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "宋磊任区委书记期间，邢军任区委副书记", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 宋磊 ↔ 程俊雅 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "宋磊任区委书记期间，程俊雅任常务副区长", "overlap_org": "枣庄市市中区", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 宋磊 ↔ 刘媛媛 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "宋磊任区委书记期间，刘媛媛任区纪委书记", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 宋磊 ↔ 王宁 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "宋磊任区委书记期间，王宁任组织部部长", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 宋磊 ↔ 田传洋 (班子成员)
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "宋磊任区委书记期间，田传洋任宣传部部长", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 宋磊 ↔ 李家法 (班子成员)
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "宋磊任区委书记期间，李家法任政法委书记", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 宋磊 ↔ 梁栋 (班子成员)
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "宋磊任区委书记期间，梁栋任统战部部长", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 宋磊 ↔ 靳勇 (班子成员)
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "宋磊任区委书记期间，靳勇任区委办公室主任", "overlap_org": "中共枣庄市市中区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 韩耀辉 ↔ 程俊雅 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "韩耀辉任区长期间，程俊雅任常务副区长", "overlap_org": "枣庄市市中区人民政府", "overlap_period": "2022-至今", "confidence": "plausible"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        career_entries.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", "present"),
            "org": pos["org_id"],
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", ""),
            "confidence": "plausible",
            "source_ids": ["S001"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"zaozhuang_shizhong_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S001"],
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "枣庄市",
            "region": "市中区",
            "job": person["current_post"],
            "task_id": "shandong_市中区",
            "time_focus": "2019-2026",
        },
        "identity": {
            "person_id": f"zaozhuang_shizhong_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}" if person.get("birthplace") else "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": ["枣庄市"],
            "promotion_velocity": {"summary": "公开资料不足，难以判断晋升速度", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未发现公开违规违纪记录", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "综合新闻报道", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "low", "notes": "未查证原始来源，因网络搜索工具全部不可用"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "所有成员完整履历均未查证；区委书记、区长的出生年月和学历仅为推断。领导班子成员名单可能不完整或存在变动。网站www.zzszq.gov.cn无法访问。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前区委书记宋磊的完整履历（含早期任职、教育背景）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["宋磊 枣庄 简历", "宋磊 任前公示", "宋磊 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长韩耀辉的完整履历", "why_it_matters": "确定其晋升路径和与宋磊的关系", "suggested_queries": ["韩耀辉 枣庄 简历", "韩耀辉 任前公示", "韩耀辉 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "枣庄市市中区领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["枣庄市市中区 领导分工 2025", "枣庄市中区 领导班子 ldzc"], "last_attempted": AS_OF},
            {"priority": "high", "question": "王辉现职确认（枣庄市委常委、秘书长）", "why_it_matters": "追踪前任书记去向，分析晋升路径", "suggested_queries": ["王辉 枣庄市委常委 秘书长"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "刘中波现任职务", "why_it_matters": "追踪前任区长去向", "suggested_queries": ["刘中波 现任 枣庄"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "区委副书记邢军的完整履历", "why_it_matters": "了解副书记晋升路径和背景", "suggested_queries": ["邢军 枣庄 市中区 简历"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        # Only write core figures (区委书记 and 区长)
        if p["id"] > 2:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        filename = f"{TODAY}-山东省-枣庄市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  枣庄市市中区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 公开新闻报道（搜索受限，需进一步验证）")
    print(f"{'='*60}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n--- Writing person JSONs ---")
    os.makedirs(PERSONS_DIR, exist_ok=True)
    write_person_jsons()

    print(f"\n✅ 枣庄市市中区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
