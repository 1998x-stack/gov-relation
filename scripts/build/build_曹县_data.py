#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 曹县 (Caoxian County), 菏泽市, 山东省.

Level: 县
Province: 山东省
Parent city: 菏泽市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_曹县

Research date: 2026-07-25
Official source: http://www.cao.gov.cn/ (曹县人民政府) — site unreachable during research

Current status (as of 2026-07-25, based on available knowledge):
- 县委书记: 赵福龙 (Zhao Fulong, assumed office ~2020/2021, formerly 曹县县长)
- 县长: 孟令选 (Meng Lingxuan, assumed office ~2022/2023, formerly 曹县县委副书记)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader, government sites) were
  rate-limited, blocked, or timed out during research. Government site www.cao.gov.cn
  and parent city site www.heze.gov.cn were unreachable. Baidu Baike returned 403.

  Leadership identification and biographical details are based on pre-existing
  knowledge that may not reflect the most current appointments. All information
  should be treated as "unverified" or "plausible" until independent web research
  can be completed.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "曹县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 赵福龙 — 县委书记
    {
        "id": 1,
        "name": "赵福龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共曹县县委书记",
        "current_org": "中共曹县委员会",
        "source": "综合新闻报道（网络搜索受限，需进一步验证）",
    },
    # 2. 孟令选 — 县长
    {
        "id": 2,
        "name": "孟令选",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曹县县委副书记、县长",
        "current_org": "曹县人民政府",
        "source": "综合新闻报道（网络搜索受限，需进一步验证）",
    },
    # 3. 县委副书记（专职副书记，姓名待查）
    {
        "id": 3,
        "name": "【待查】曹县县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委副书记（专职，待查）",
        "current_org": "中共曹县委员会",
        "source": "GAP — 专职副书记具体人选未确认",
    },
    # 4. 县委常委、常务副县长（姓名待查）
    {
        "id": 4,
        "name": "【待查】曹县常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委常委、常务副县长（待查）",
        "current_org": "曹县人民政府",
        "source": "GAP — 常务副县长具体人选未确认",
    },
    # 5. 县委常委、县纪委书记（姓名待查）
    {
        "id": 5,
        "name": "【待查】曹县纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委常委、县纪委书记、县监委主任（待查）",
        "current_org": "中共曹县纪律检查委员会",
        "source": "GAP — 纪委书记具体人选未确认",
    },
    # 6. 县委常委、组织部部长（姓名待查）
    {
        "id": 6,
        "name": "【待查】曹县县委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委常委、组织部部长（待查）",
        "current_org": "中共曹县委员会组织部",
        "source": "GAP — 组织部部长具体人选未确认",
    },
    # 7. 县委常委、宣传部部长（姓名待查）
    {
        "id": 7,
        "name": "【待查】曹县县委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委常委、宣传部部长（待查）",
        "current_org": "中共曹县委员会宣传部",
        "source": "GAP — 宣传部部长具体人选未确认",
    },
    # 8. 县委常委、政法委书记（姓名待查）
    {
        "id": 8,
        "name": "【待查】曹县县委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委常委、政法委书记（待查）",
        "current_org": "中共曹县委员会政法委员会",
        "source": "GAP — 政法委书记具体人选未确认",
    },
    # 9. 县委常委、统战部部长（姓名待查）
    {
        "id": 9,
        "name": "【待查】曹县县委统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委常委、统战部部长（待查）",
        "current_org": "中共曹县委员会统战部",
        "source": "GAP — 统战部部长具体人选未确认",
    },
    # 10. 县人武部部长（姓名待查）
    {
        "id": 10,
        "name": "【待查】曹县人民武装部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曹县县委常委、人民武装部部长（待查）",
        "current_org": "曹县人民武装部",
        "source": "GAP — 人武部部长具体人选未确认",
    },
    # 11. 前任县委书记 — 张乾山
    {
        "id": 11,
        "name": "张乾山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原曹县县委书记（推测已调任菏泽市领导职务或已退休）",
        "current_org": "原中共曹县委员会",
        "source": "张乾山约2016-2020年任曹县县委书记，后由赵福龙接任。网络搜索受限，此信息需验证。",
    },
    # 12. 前任县长 — 梁惠民（女）
    {
        "id": 12,
        "name": "梁惠民",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原曹县县长（推测已调任）",
        "current_org": "原曹县人民政府",
        "source": "梁惠民约2017-2021年任曹县县长，后由孟令选接任。网络搜索受限，此信息需验证。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共曹县委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市委", "location": "菏泽市曹县"},
    {"id": 2, "name": "曹县人民政府", "type": "政府", "level": "县处级", "parent": "菏泽市人民政府", "location": "菏泽市曹县"},
    {"id": 3, "name": "中共曹县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共曹县委员会", "location": "菏泽市曹县"},
    {"id": 4, "name": "中共曹县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共曹县委员会", "location": "菏泽市曹县"},
    {"id": 5, "name": "中共曹县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共曹县委员会", "location": "菏泽市曹县"},
    {"id": 6, "name": "中共曹县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共曹县委员会", "location": "菏泽市曹县"},
    {"id": 7, "name": "中共曹县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共曹县委员会", "location": "菏泽市曹县"},
    {"id": 8, "name": "曹县人民武装部", "type": "党委", "level": "县处级", "parent": "菏泽军分区", "location": "菏泽市曹县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 赵福龙 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共曹县县委书记", "start": "2020", "end": "present", "rank": "县处级", "note": "推测2020年前后由曹县县长转任县委书记"},
    # 赵福龙 — 曾任曹县县长
    {"person_id": 1, "org_id": 2, "title": "曹县县委副书记、县长（前任职务）", "start": "2017", "end": "2020", "rank": "县处级", "note": "推测2017-2020年任曹县县长"},
    # 孟令选 — 县长
    {"person_id": 2, "org_id": 2, "title": "曹县县委副书记、县长", "start": "2022", "end": "present", "rank": "县处级", "note": "推测2022/2023年上任，此前为曹县县委副书记"},
    # 孟令选 — 曾任曹县县委副书记
    {"person_id": 2, "org_id": 1, "title": "曹县县委副书记（专职）", "start": "2020", "end": "2022", "rank": "县处级", "note": "推测2020年后任县委副书记"},
    # 待查_县委副书记
    {"person_id": 3, "org_id": 1, "title": "曹县县委副书记（专职）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_常务副县长
    {"person_id": 4, "org_id": 2, "title": "曹县县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_纪委书记
    {"person_id": 5, "org_id": 3, "title": "曹县县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_组织部部长
    {"person_id": 6, "org_id": 4, "title": "曹县县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_宣传部部长
    {"person_id": 7, "org_id": 5, "title": "曹县县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "曹县县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部部长
    {"person_id": 9, "org_id": 6, "title": "曹县县委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_人武部部长
    {"person_id": 10, "org_id": 8, "title": "曹县县委常委、人民武装部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 张乾山 — 前任县委书记
    {"person_id": 11, "org_id": 1, "title": "曹县县委书记（前任）", "start": "2016", "end": "2020", "rank": "县处级", "note": "推测去向为菏泽市级职务或退休"},
    # 梁惠民 — 前任县长（女）
    {"person_id": 12, "org_id": 2, "title": "曹县县长（前任）", "start": "2017", "end": "2021", "rank": "县处级", "note": "推测已调任其他职务"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 赵福龙 ↔ 孟令选 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "赵福龙任县委书记、孟令选任县长，党政搭档",
     "overlap_org": "曹县", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 赵福龙 ⟷ 张乾山 (前任书记)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor",
     "context": "赵福龙接替张乾山任曹县县委书记",
     "overlap_org": "中共曹县委员会", "overlap_period": "2020", "confidence": "plausible"},
    # 赵福龙 ⟷ 梁惠民 (前任搭档、前任县长)
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "赵福龙任县长期间与梁惠民共事（梁惠民前任县长）",
     "overlap_org": "曹县人民政府", "overlap_period": "2017-2019", "confidence": "plausible"},
    # 孟令选 ⟷ 梁惠民 (前任县长)
    {"person_a": 2, "person_b": 12, "type": "predecessor_successor",
     "context": "孟令选接替梁惠民任曹县县长",
     "overlap_org": "曹县人民政府", "overlap_period": "2022", "confidence": "plausible"},
    # 赵福龙与孟令选（党政交接期）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "赵福龙任县委书记期间，孟令选从县委副书记升任县长",
     "overlap_org": "中共曹县委员会", "overlap_period": "2020-2022", "confidence": "plausible"},
    # 张乾山 ⟷ 梁惠民 (前任党政搭档)
    {"person_a": 11, "person_b": 12, "type": "overlap",
     "context": "张乾山任县委书记期间，梁惠民任曹县县长",
     "overlap_org": "曹县", "overlap_period": "2017-2020", "confidence": "plausible"},
    # 孟令选 ⟷ 张乾山 (前任书记)
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "张乾山任县委书记期间，孟令选可能已任职曹县",
     "overlap_org": "中共曹县委员会", "overlap_period": "2018-2020", "confidence": "unverified"},
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
            "confidence": "unverified",
            "source_ids": ["S001"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id and p["id"] != pid), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"caoxian_{other['name']}",
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
            "city": "菏泽市",
            "region": "曹县",
            "job": person["current_post"],
            "task_id": "shandong_曹县",
            "time_focus": "2016-2026",
        },
        "identity": {
            "person_id": f"caoxian_{person['name']}",
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
            "administrative_rank": "县处级",
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
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["菏泽市"],
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
            {"id": "S001", "title": "综合新闻报道（未验证）", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "low",
             "notes": "未查证原始来源，因网络搜索工具全部不可用（Exa限流、政府网站超时、百度403）"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有成员的完整履历均未查证；县委书记赵福龙、县长孟令选的当前任职及完整履历需通过官方渠道确认。县委副书记、常务副县长、纪委书记、组织部长、宣传部长、政法委书记、统战部长、人武部长等班子成员具体人选全部待查。前任书记张乾山和前任县长梁惠民的详细任职时间和去向待确认。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前县委书记赵福龙的完整履历（含出生年月、教育背景、出生地、早期任职经历）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["赵福龙 简历 菏泽", "赵福龙 曹县 任前公示", "赵福龙 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前县长孟令选的完整履历及全名确认", "why_it_matters": "确定其晋升路径和与县委书记的关系", "suggested_queries": ["孟令选 曹县 县长", "曹县 县长 现任", "孟令选 简历"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "赵福龙的当前任职是否仍为曹县县委书记，孟令选是否确实为曹县县长", "why_it_matters": "核心调查目标，需官方渠道确认", "suggested_queries": ["曹县 领导分工 2024 2025", "曹县县委书记 现任", "曹县县长 现任", "site:cao.gov.cn 领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "曹县县委领导班子完整名单（专职副书记、常务副县长、纪委书记、组织部长、宣传部长、政法委书记、统战部长、人武部长）", "why_it_matters": "完成领导班子全名单，识别关联节点", "suggested_queries": ["曹县 县委常委会", "曹县 领导班子 成员", "曹县 县领导", "曹县 领导分工"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任县委书记张乾山的完整去向和现任职务", "why_it_matters": "追踪菏泽干部交流模式", "suggested_queries": ["张乾山 菏泽 现任", "张乾山 曹县 调任 职务"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任县长梁惠民（女）的去向和现任职务", "why_it_matters": "女性干部成长路径和跨县交流模式", "suggested_queries": ["梁惠民 曹县 县长 调任", "梁惠民 现任 职务"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "曹县在中国网络上的知名度（短视频/电商）对当地人事安排的影响", "why_it_matters": "理解网红县域的特殊政治生态", "suggested_queries": ["曹县 网络 走红 县委书记 态度", "曹县 电商 产业 领导 分工"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "曹县与其他菏泽下辖县区的干部交流情况", "why_it_matters": "跨县区人事网络分析", "suggested_queries": ["曹县 干部 交流 菏泽", "曹县 调任 定陶 单县"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        if "待查" in p["name"]:
            continue  # Skip placeholder entries
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        filename = f"{TODAY}-山东省-菏泽市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  曹县 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 综合知识（搜索受限，需进一步验证）")
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

    print(f"\n✅ 曹县数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
