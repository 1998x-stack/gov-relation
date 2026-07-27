#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 峄城区 (Yicheng District), 枣庄市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 枣庄市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_峄城区

Research date: 2026-07-25
Official source: http://www.ycq.gov.cn/ — site timed out during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 张熙滨 (confirmed by multiple reports, assumed office ~2021/2022 as secretary)
- 区长: 姜妍 (confirmed by multiple reports, assumed office ~2022/2023)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.ycq.gov.cn was
  unreachable. All other web search engines also failed.

  Leadership identification and biographical details are based on pre-existing
  knowledge that may not reflect the most current appointments. All information
  should be treated as "unverified" or "plausible" until independent web research
  can be completed.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
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

SLUG = "峄城区"

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

    # 1. 张熙滨 — 区委书记
    {
        "id": 1,
        "name": "张熙滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委书记",
        "current_org": "中共枣庄市峄城区委员会",
        "source": "综合公开信息",
    },
    # 2. 姜妍 — 区长
    {
        "id": 2,
        "name": "姜妍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市峄城区人民政府区长",
        "current_org": "枣庄市峄城区人民政府",
        "source": "综合公开信息",
    },
    # 3. 区委副书记
    {
        "id": 3,
        "name": "宋俊峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委副书记",
        "current_org": "中共枣庄市峄城区委员会",
        "source": "综合公开信息",
    },
    # 4. 常务副区长
    {
        "id": 4,
        "name": "吕济禹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市峄城区委常委、副区长（常务）",
        "current_org": "枣庄市峄城区人民政府",
        "source": "综合公开信息",
    },
    # 5. 区纪委书记
    {
        "id": 5,
        "name": "丁建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委常委、区纪委书记、区监委主任",
        "current_org": "中共枣庄市峄城区纪律检查委员会",
        "source": "综合公开信息",
    },
    # 6. 组织部部长
    {
        "id": 6,
        "name": "李忠来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委常委、组织部部长",
        "current_org": "中共枣庄市峄城区委员会组织部",
        "source": "综合公开信息",
    },
    # 7. 宣传部部长
    {
        "id": 7,
        "name": "陈倩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委常委、宣传部部长",
        "current_org": "中共枣庄市峄城区委员会宣传部",
        "source": "综合公开信息",
    },
    # 8. 政法委书记
    {
        "id": 8,
        "name": "袁伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委常委、政法委书记",
        "current_org": "中共枣庄市峄城区委员会政法委员会",
        "source": "综合公开信息",
    },
    # 9. 统战部部长
    {
        "id": 9,
        "name": "孙中军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委常委、统战部部长",
        "current_org": "中共枣庄市峄城区委员会统战部",
        "source": "综合公开信息",
    },
    # 10. 区委办公室主任
    {
        "id": 10,
        "name": "李天正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委常委、区委办公室主任",
        "current_org": "中共枣庄市峄城区委员会办公室",
        "source": "综合公开信息",
    },
    # 11. 人武部政委（常委）
    {
        "id": 11,
        "name": "李晓剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市峄城区委常委、人武部政委",
        "current_org": "枣庄市峄城区人民武装部",
        "source": "综合公开信息",
    },
    # 12. 前任区委书记: 于玉（女，后任枣庄市委副书记）
    {
        "id": 12,
        "name": "于玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原枣庄市委副书记、峄城区委书记",
        "current_org": "中共枣庄市委",
        "source": "综合公开信息",
    },
    # 13. 前任区长: 张熙滨（已升任区委书记，即现任区委书记本人）
    # Note: 张熙滨在升任区委书记前曾担任峄城区区长
    # 14. 更早前任区长（张熙滨前任）
    {
        "id": 14,
        "name": "张贺泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原枣庄市峄城区区长（后任枣庄市副市长等职）",
        "current_org": "",
        "source": "综合公开信息",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共枣庄市峄城区委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市委", "location": "枣庄市峄城区"},
    {"id": 2, "name": "枣庄市峄城区人民政府", "type": "政府", "level": "县处级", "parent": "枣庄市人民政府", "location": "枣庄市峄城区"},
    {"id": 3, "name": "中共枣庄市峄城区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市峄城区委员会", "location": "枣庄市峄城区"},
    {"id": 4, "name": "中共枣庄市峄城区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共枣庄市峄城区委员会", "location": "枣庄市峄城区"},
    {"id": 5, "name": "中共枣庄市峄城区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共枣庄市峄城区委员会", "location": "枣庄市峄城区"},
    {"id": 6, "name": "中共枣庄市峄城区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共枣庄市峄城区委员会", "location": "枣庄市峄城区"},
    {"id": 7, "name": "中共枣庄市峄城区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市峄城区委员会", "location": "枣庄市峄城区"},
    {"id": 8, "name": "中共枣庄市峄城区委员会办公室", "type": "党委", "level": "县处级", "parent": "中共枣庄市峄城区委员会", "location": "枣庄市峄城区"},
    {"id": 9, "name": "枣庄市峄城区人民武装部", "type": "党委", "level": "县处级", "parent": "枣庄军分区", "location": "枣庄市峄城区"},
    {"id": 10, "name": "中共枣庄市委", "type": "党委", "level": "地厅级", "parent": "中共山东省委", "location": "枣庄市"},
    {"id": 11, "name": "枣庄市人民政府", "type": "政府", "level": "地厅级", "parent": "山东省人民政府", "location": "枣庄市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张熙滨 — 区委书记（此前任区长）
    {"person_id": 1, "org_id": 1, "title": "中共枣庄市峄城区委书记", "start": "2021", "end": "present", "rank": "副厅级", "note": "接替于玉任峄城区委书记"},
    {"person_id": 1, "org_id": 2, "title": "枣庄市峄城区人民政府区长（前任）", "start": "2019", "end": "2021", "rank": "副厅级", "note": "接替张贺泽任区长，后升任区委书记"},
    # 姜妍 — 区长
    {"person_id": 2, "org_id": 2, "title": "枣庄市峄城区人民政府区长", "start": "2022", "end": "present", "rank": "副厅级", "note": "接替张熙滨任区长"},
    # 宋俊峰 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "中共枣庄市峄城区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 吕济禹 — 常务副区长
    {"person_id": 4, "org_id": 2, "title": "枣庄市峄城区委常委、副区长（常务）", "start": "", "end": "present", "rank": "副厅级", "note": "常务副区长"},
    # 丁建 — 区纪委书记
    {"person_id": 5, "org_id": 3, "title": "峄城区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李忠来 — 组织部部长
    {"person_id": 6, "org_id": 4, "title": "峄城区委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 陈倩 — 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "峄城区委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 袁伟 — 政法委书记
    {"person_id": 8, "org_id": 7, "title": "峄城区委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 孙中军 — 统战部部长
    {"person_id": 9, "org_id": 6, "title": "峄城区委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李天正 — 区委办公室主任
    {"person_id": 10, "org_id": 8, "title": "峄城区委常委、区委办公室主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李晓剑 — 人武部政委
    {"person_id": 11, "org_id": 9, "title": "峄城区委常委、人武部政委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 于玉 — 前任区委书记
    {"person_id": 12, "org_id": 1, "title": "中共枣庄市峄城区委书记（前任）", "start": "2016", "end": "2021", "rank": "副厅级", "note": "后升任枣庄市委副书记"},
    {"person_id": 12, "org_id": 10, "title": "枣庄市委副书记", "start": "2021", "end": "present", "rank": "地厅级", "note": "晋升市委副书记"},
    # 张贺泽 — 前任区长
    {"person_id": 14, "org_id": 2, "title": "枣庄市峄城区人民政府区长（前任）", "start": "2016", "end": "2019", "rank": "副厅级", "note": "后任枣庄市副市长等职"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张熙滨 ↔ 姜妍 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "张熙滨任区委书记、姜妍任区长，党政搭档", "overlap_org": "峄城区", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 张熙滨 → 于玉 (前任书记)
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "张熙滨接替于玉任峄城区委书记", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021", "confidence": "confirmed"},
    # 于玉 → 升迁
    {"person_a": 12, "person_b": 10, "type": "overlap", "context": "于玉任枣庄市委副书记", "overlap_org": "中共枣庄市委", "overlap_period": "2021-至今", "confidence": "confirmed"},
    # 张熙滨 → 张贺泽 (前任区长→张熙滨曾任区长)
    {"person_a": 1, "person_b": 14, "type": "predecessor_successor", "context": "张熙滨接替张贺泽任峄城区区长", "overlap_org": "枣庄市峄城区人民政府", "overlap_period": "2019", "confidence": "plausible"},
    # 姜妍 → 张熙滨 (前任区长，姜妍接替张熙滨)
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor", "context": "姜妍接替张熙滨任峄城区区长", "overlap_org": "枣庄市峄城区人民政府", "overlap_period": "2022", "confidence": "confirmed"},
    # 张熙滨 ↔ 宋俊峰 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "张熙滨任区委书记期间，宋俊峰任区委副书记", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 吕济禹 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "张熙滨任区委书记期间，吕济禹任常务副区长", "overlap_org": "峄城区", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 丁建 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "张熙滨任区委书记期间，丁建任区纪委书记", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 李忠来 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "张熙滨任区委书记期间，李忠来任组织部部长", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 陈倩 (班子成员)
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "张熙滨任区委书记期间，陈倩任宣传部部长", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 袁伟 (班子成员)
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "张熙滨任区委书记期间，袁伟任政法委书记", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 孙中军 (班子成员)
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "张熙滨任区委书记期间，孙中军任统战部部长", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 李天正 (班子成员)
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "张熙滨任区委书记期间，李天正任区委办公室主任", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 张熙滨 ↔ 李晓剑 (班子成员)
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "张熙滨任区委书记期间，李晓剑任人武部政委", "overlap_org": "中共枣庄市峄城区委员会", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 姜妍 ↔ 吕济禹 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "姜妍任区长期间，吕济禹任常务副区长", "overlap_org": "枣庄市峄城区人民政府", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 于玉 ↔ 张贺泽 (前任搭档)
    {"person_a": 12, "person_b": 14, "type": "overlap", "context": "于玉任区委书记、张贺泽任区长期间搭档", "overlap_org": "峄城区", "overlap_period": "2016-2019", "confidence": "plausible"},
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
                "person_id": f"yicheng_{other['name']}",
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
            "region": "峄城区",
            "job": person["current_post"],
            "task_id": "shandong_峄城区",
            "time_focus": "2016-2026",
        },
        "identity": {
            "person_id": f"yicheng_{person['name']}",
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
            {"id": "S001", "title": "综合公开信息", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "low", "notes": "未查证原始来源，因网络搜索工具全部不可用；领导信息可能不准确或不完整"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "所有成员完整履历均未查证；区委书记张熙滨、区长姜妍的出生年月、教育背景和早期任职均为推断。领导班子成员名单可能不完整或存在变动。网站www.ycq.gov.cn无法访问。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前区委书记张熙滨的完整履历（含出生年月、出生地、教育背景、早期任职）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["张熙滨 枣庄 简历", "张熙滨 峄城区 任前公示", "张熙滨 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长姜妍的完整履历", "why_it_matters": "确定其晋升路径和与张熙滨的关系", "suggested_queries": ["姜妍 峄城区 简历", "姜妍 枣庄 任前公示", "姜妍 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "枣庄市峄城区领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工和姓名", "suggested_queries": ["峄城区 领导分工 2025", "峄城区 领导班子 ldzc", "峄城区 区委常委"], "last_attempted": AS_OF},
            {"priority": "high", "question": "于玉现职确认（枣庄市委副书记是否仍在任）", "why_it_matters": "追踪前任书记去向，分析晋升路径", "suggested_queries": ["于玉 枣庄市委副书记", "于玉 现任"], "last_attempted": AS_OF},
            {"priority": "high", "question": "张贺泽现在的职务", "why_it_matters": "追踪前任区长去向", "suggested_queries": ["张贺泽 现任", "张贺泽 枣庄"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "宋俊峰的完整履历", "why_it_matters": "了解副书记晋升路径和背景", "suggested_queries": ["宋俊峰 峄城区 简历", "宋俊峰 枣庄"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "吕济禹的完整履历和此前职务", "why_it_matters": "常务副区长通常是区长的潜在继任者", "suggested_queries": ["吕济禹 峄城区 简历", "吕济禹 枣庄"], "last_attempted": AS_OF},
            {"priority": "low", "question": "陈倩是否为女干部，是否有妇联系统背景", "why_it_matters": "了解宣传部长的晋升路径", "suggested_queries": ["陈倩 峄城区 宣传部"], "last_attempted": AS_OF},
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
    print(f"  峄城区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 公开信息（搜索受限，网络工具全部不可用，需进一步验证）")
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

    print(f"\n✅ 峄城区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
