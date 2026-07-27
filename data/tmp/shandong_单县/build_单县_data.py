#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 单县 (Shan County), 菏泽市, 山东省.

Level: 县
Province: 山东省
Parent city: 菏泽市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_单县

Research date: 2026-07-25
Official source: http://www.shanxian.gov.cn/ (单县人民政府) — site unreachable during research

Current status (as of 2026-07-25, based on available knowledge):
- 县委书记: 耿振华 (Geng Zhenhua, assumed office ~2021/2022, formerly 菏泽市委宣传部分管日常工作副部长等)
- 县长: 魏传永 (Wei Chuanyong, assumed office ~2021/2022, formerly 单县县委副书记)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader, government sites) were
  rate-limited, blocked, or timed out during research. Government site www.shanxian.gov.cn
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
import sys
from datetime import datetime
from pathlib import Path

# When running from scripts/build/, the file lives in scripts/build/
# When staging in data/tmp/, resolve accordingly
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "单县"

# If running from staging, DB_PATH/GEXF_PATH are in staging dir.
# If running from scripts/build/, DB goes to staging tmp for eventual promotion.
# Default: write alongside the script (staging or build dir)
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

    # 1. 耿振华 — 县委书记
    {
        "id": 1,
        "name": "耿振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共单县县委书记",
        "current_org": "中共单县委员会",
        "source": "综合知识（网络搜索受限，需进一步验证）",
    },
    # 2. 魏传永 — 县长
    {
        "id": 2,
        "name": "魏传永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "单县县委副书记、县长",
        "current_org": "单县人民政府",
        "source": "综合知识（网络搜索受限，需进一步验证）",
    },
    # 3. 县委副书记（专职副书记，姓名待查）
    {
        "id": 3,
        "name": "【待查】单县县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委副书记（专职，待查）",
        "current_org": "中共单县委员会",
        "source": "GAP — 专职副书记具体人选未确认",
    },
    # 4. 县委常委、常务副县长（姓名待查）
    {
        "id": 4,
        "name": "【待查】单县常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委常委、常务副县长（待查）",
        "current_org": "单县人民政府",
        "source": "GAP — 常务副县长具体人选未确认",
    },
    # 5. 县委常委、县纪委书记（姓名待查）
    {
        "id": 5,
        "name": "【待查】单县纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委常委、县纪委书记、县监委主任（待查）",
        "current_org": "中共单县纪律检查委员会",
        "source": "GAP — 纪委书记具体人选未确认",
    },
    # 6. 县委常委、组织部部长（姓名待查）
    {
        "id": 6,
        "name": "【待查】单县县委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委常委、组织部部长（待查）",
        "current_org": "中共单县委员会组织部",
        "source": "GAP — 组织部部长具体人选未确认",
    },
    # 7. 县委常委、宣传部部长（姓名待查）
    {
        "id": 7,
        "name": "【待查】单县县委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委常委、宣传部部长（待查）",
        "current_org": "中共单县委员会宣传部",
        "source": "GAP — 宣传部部长具体人选未确认",
    },
    # 8. 县委常委、政法委书记（姓名待查）
    {
        "id": 8,
        "name": "【待查】单县县委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委常委、政法委书记（待查）",
        "current_org": "中共单县委员会政法委员会",
        "source": "GAP — 政法委书记具体人选未确认",
    },
    # 9. 县委常委、统战部部长（姓名待查）
    {
        "id": 9,
        "name": "【待查】单县县委统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委常委、统战部部长（待查）",
        "current_org": "中共单县委员会统战部",
        "source": "GAP — 统战部部长具体人选未确认",
    },
    # 10. 县人武部部长（姓名待查）
    {
        "id": 10,
        "name": "【待查】单县人民武装部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "单县县委常委、人民武装部部长（待查）",
        "current_org": "单县人民武装部",
        "source": "GAP — 人武部部长具体人选未确认",
    },
    # 11. 前任县委书记 — 穆杰
    {
        "id": 11,
        "name": "穆杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "推测已任菏泽市领导职务（如副市长或市委常委）",
        "current_org": "推测为菏泽市",
        "source": "穆杰约2017-2021年任单县县委书记，后调任菏泽市。网络搜索受限，需验证。",
    },
    # 12. 前任县长 — 张庆国
    {
        "id": 12,
        "name": "张庆国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原单县县长（推测已调任他职）",
        "current_org": "原单县人民政府",
        "source": "张庆国约2017-2021年任单县县长，后由魏传永接任。网络搜索受限，需验证。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共单县委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市委", "location": "菏泽市单县"},
    {"id": 2, "name": "单县人民政府", "type": "政府", "level": "县处级", "parent": "菏泽市人民政府", "location": "菏泽市单县"},
    {"id": 3, "name": "中共单县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共单县委员会", "location": "菏泽市单县"},
    {"id": 4, "name": "中共单县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共单县委员会", "location": "菏泽市单县"},
    {"id": 5, "name": "中共单县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共单县委员会", "location": "菏泽市单县"},
    {"id": 6, "name": "中共单县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共单县委员会", "location": "菏泽市单县"},
    {"id": 7, "name": "中共单县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共单县委员会", "location": "菏泽市单县"},
    {"id": 8, "name": "单县人民武装部", "type": "党委", "level": "县处级", "parent": "菏泽军分区", "location": "菏泽市单县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 耿振华 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共单县县委书记", "start": "2021", "end": "present", "rank": "县处级", "note": "推测2021/2022年由菏泽市调任单县县委书记"},
    # 耿振华 — 曾任菏泽市委宣传部副部长/网信办主任（推测）
    {"person_id": 1, "org_id": 1, "title": "菏泽市委宣传部副部长/市委网信办主任（推测前任职务）", "start": "2018", "end": "2021", "rank": "县处级", "note": "推测担任菏泽市委网信办主任/宣传部副部长（分管日常工作）"},
    # 魏传永 — 县长
    {"person_id": 2, "org_id": 2, "title": "单县县委副书记、县长", "start": "2021", "end": "present", "rank": "县处级", "note": "推测2021/2022年上任，此前为单县县委副书记"},
    # 魏传永 — 曾任单县县委副书记
    {"person_id": 2, "org_id": 1, "title": "单县县委副书记（专职）", "start": "2019", "end": "2021", "rank": "县处级", "note": "推测2019年后任单县县委副书记，后升县长"},
    # 待查_县委副书记
    {"person_id": 3, "org_id": 1, "title": "单县县委副书记（专职）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_常务副县长
    {"person_id": 4, "org_id": 2, "title": "单县县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_纪委书记
    {"person_id": 5, "org_id": 3, "title": "单县县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_组织部部长
    {"person_id": 6, "org_id": 4, "title": "单县县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_宣传部部长
    {"person_id": 7, "org_id": 5, "title": "单县县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "单县县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部部长
    {"person_id": 9, "org_id": 6, "title": "单县县委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_人武部部长
    {"person_id": 10, "org_id": 8, "title": "单县县委常委、人民武装部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 穆杰 — 前任县委书记
    {"person_id": 11, "org_id": 1, "title": "单县县委书记（前任）", "start": "2017", "end": "2021", "rank": "县处级", "note": "推测去向为菏泽市级职务（如副市长/市委常委）"},
    # 张庆国 — 前任县长
    {"person_id": 12, "org_id": 2, "title": "单县县长（前任）", "start": "2017", "end": "2021", "rank": "县处级", "note": "推测2021年左右离任，去向待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 耿振华 ↔ 魏传永 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "耿振华任县委书记、魏传永任县长，党政搭档",
     "overlap_org": "单县", "overlap_period": "2021-至今", "confidence": "plausible"},
    # 耿振华 ⟷ 穆杰 (前任书记)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor",
     "context": "耿振华接替穆杰任单县县委书记",
     "overlap_org": "中共单县委员会", "overlap_period": "2021", "confidence": "plausible"},
    # 魏传永 ⟷ 张庆国 (前任县长)
    {"person_a": 2, "person_b": 12, "type": "predecessor_successor",
     "context": "魏传永接替张庆国任单县县长",
     "overlap_org": "单县人民政府", "overlap_period": "2021", "confidence": "plausible"},
    # 穆杰 ⟷ 张庆国 (前任党政搭档)
    {"person_a": 11, "person_b": 12, "type": "overlap",
     "context": "穆杰任县委书记期间，张庆国任单县县长",
     "overlap_org": "单县", "overlap_period": "2017-2021", "confidence": "plausible"},
    # 耿振华 ⟷ 张庆国 (可能重叠）
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "耿振华可能曾在菏泽市级层面与张庆国有工作交集",
     "overlap_org": "菏泽市", "overlap_period": "2018-2021", "confidence": "unverified"},
    # 魏传永与耿振华（上下级关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "魏传永从县委副书记升任县长，耿振华为县委书记",
     "overlap_org": "中共单县委员会", "overlap_period": "2019-2022", "confidence": "plausible"},
    # 穆杰 ⟷ 魏传永（前任上级与现任县长）
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "穆杰任县委书记期间，魏传永可能已在单县任职",
     "overlap_org": "中共单县委员会", "overlap_period": "2019-2021", "confidence": "unverified"},
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
                "person_id": f"shanxian_{other['name']}",
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
            "region": "单县",
            "job": person["current_post"],
            "task_id": "shandong_单县",
            "time_focus": "2016-2026",
        },
        "identity": {
            "person_id": f"shanxian_{person['name']}",
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
            {"id": "S001", "title": "综合知识（未验证）", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "low",
             "notes": "未查证原始来源，因网络搜索工具全部不可用（Exa限流、政府网站超时、百度403）"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有成员的完整履历均未查证；县委书记耿振华、县长魏传永的当前任职及完整履历需通过官方渠道确认。县委副书记、常务副县长、纪委书记、组织部长、宣传部长、政法委书记、统战部长、人武部长等班子成员具体人选全部待查。前任书记穆杰和前任县长张庆国的详细任职时间和去向待确认。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前县委书记耿振华的完整履历（含出生年月、教育背景、出生地、早期任职经历）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["耿振华 简历 菏泽", "耿振华 单县 任前公示", "耿振华 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前县长魏传永的完整履历及全名确认", "why_it_matters": "确定其晋升路径和与县委书记的关系", "suggested_queries": ["魏传永 单县 县长", "单县 县长 现任", "魏传永 简历"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "耿振华的当前任职是否仍为单县县委书记，魏传永是否确实为单县县长", "why_it_matters": "核心调查目标，需官方渠道确认", "suggested_queries": ["单县 领导分工 2024 2025", "单县县委书记 现任", "单县县长 现任", "site:shanxian.gov.cn 领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "单县县委领导班子完整名单（专职副书记、常务副县长、纪委书记、组织部长、宣传部长、政法委书记、统战部长、人武部长）", "why_it_matters": "完成领导班子全名单，识别关联节点", "suggested_queries": ["单县 县委常委会", "单县 领导班子 成员", "单县 县领导", "单县 领导分工"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任县委书记穆杰的完整去向和现任职务", "why_it_matters": "追踪菏泽干部交流模式", "suggested_queries": ["穆杰 菏泽 现任", "穆杰 单县 调任 职务"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任县长张庆国的去向和现任职务", "why_it_matters": "了解单县县长晋升路径", "suggested_queries": ["张庆国 单县 县长 调任", "张庆国 现任 职务"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "单县与菏泽其他县区的干部交流情况", "why_it_matters": "跨县区人事网络分析", "suggested_queries": ["单县 干部 交流 菏泽", "单县 调任 曹县 定陶"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "单县特色产业（羊肉汤、医药等）对当地领导政策方向的影响", "why_it_matters": "了解县域治理重点与领导分工关系", "suggested_queries": ["单县 羊肉汤 产业 书记 县长", "单县 经济 发展 特色"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        if "待查" in p["name"]:
            continue  # Skip placeholder entries
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        # Build job slug — remove common suffixes for cleaner filenames
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
    print(f"  单县 领导班子工作关系网络")
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

    print(f"\n✅ 单县数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
