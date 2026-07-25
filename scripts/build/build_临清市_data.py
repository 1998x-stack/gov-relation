#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 临清市 (Linqing City), 聊城市, 山东省.

Level: 县级市
Province: 山东省
Parent city: 聊城市
Targets: 市委书记 (Party Secretary), 市长 (Mayor)
Task ID: shandong_临清市

Research date: 2026-07-25
Official source: http://www.linqing.gov.cn/ (临清市人民政府)

Current status (as of 2026-07-25, confirmed via government website news):
- 市委书记: 张志刚 (Zhang Zhigang) — confirmed active Jul 2026
- 市长: 周超 (Zhou Chao) — confirmed active Jul 2026

Confidence notes:
  Leadership identification confirmed via linqing.gov.cn homepage news items.
  Full biographies (birth, education, early career) could not be independently
  verified due to web search degradation (Exa rate-limited, Baidu blocked).
  Government leadership page (ldzc) was not directly accessible.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
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

SLUG = "临清市"

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

    # 1. 张志刚 — 市委书记
    {
        "id": 1,
        "name": "张志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共临清市委书记",
        "current_org": "中共临清市委员会",
        "source": "临清市人民政府官网要闻动态确认（2026年7月活动报道）",
    },
    # 2. 周超 — 市长
    {
        "id": 2,
        "name": "周超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临清市委副书记、市长",
        "current_org": "临清市人民政府",
        "source": "临清市人民政府官网要闻动态确认（2026年7月活动报道）",
    },
    # 3. 市委专职副书记（姓名待查）
    {
        "id": 3,
        "name": "【待查】临清市委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临清市委副书记（专职，待查）",
        "current_org": "中共临清市委员会",
        "source": "GAP — 专职副书记具体人选未确认",
    },
    # 4. 市委常委、常务副市长（姓名待查）
    {
        "id": 4,
        "name": "【待查】临清市常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临清市委常委、常务副市长（待查）",
        "current_org": "临清市人民政府",
        "source": "GAP — 常务副市长具体人选未确认",
    },
    # 5. 市委常委、市纪委书记（姓名待查）
    {
        "id": 5,
        "name": "【待查】临清市纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临清市委常委、市纪委书记、市监委主任（待查）",
        "current_org": "中共临清市纪律检查委员会",
        "source": "GAP — 纪委书记具体人选未确认",
    },
    # 6. 市委常委、组织部部长（姓名待查）
    {
        "id": 6,
        "name": "【待查】临清市委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临清市委常委、组织部部长（待查）",
        "current_org": "中共临清市委员会组织部",
        "source": "GAP — 组织部部长具体人选未确认",
    },
    # 7. 市委常委、宣传部部长（姓名待查）
    {
        "id": 7,
        "name": "【待查】临清市委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临清市委常委、宣传部部长（待查）",
        "current_org": "中共临清市委员会宣传部",
        "source": "GAP — 宣传部部长具体人选未确认",
    },
    # 8. 市委常委、政法委书记（姓名待查）
    {
        "id": 8,
        "name": "【待查】临清市委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临清市委常委、政法委书记（待查）",
        "current_org": "中共临清市委员会政法委员会",
        "source": "GAP — 政法委书记具体人选未确认",
    },
    # 9. 市委常委、统战部部长（姓名待查）
    {
        "id": 9,
        "name": "【待查】临清市委统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临清市委常委、统战部部长（待查）",
        "current_org": "中共临清市委员会统一战线工作部",
        "source": "GAP — 统战部部长具体人选未确认",
    },
    # 10. 前任市委书记（姓名待查）
    {
        "id": 10,
        "name": "【待查】临清市前任市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原临清市委书记（待查）",
        "current_org": "原中共临清市委员会",
        "source": "GAP — 前任市委书记信息待查",
    },
    # 11. 前任市长（姓名待查）
    {
        "id": 11,
        "name": "【待查】临清市前任市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原临清市长（待查）",
        "current_org": "原临清市人民政府",
        "source": "GAP — 前任市长信息待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共临清市委员会", "type": "党委", "level": "县处级", "parent": "中共聊城市委", "location": "聊城市临清市"},
    {"id": 2, "name": "临清市人民政府", "type": "政府", "level": "县处级", "parent": "聊城市人民政府", "location": "聊城市临清市"},
    {"id": 3, "name": "中共临清市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共临清市委员会", "location": "聊城市临清市"},
    {"id": 4, "name": "中共临清市委员会组织部", "type": "党委", "level": "县处级", "parent": "中共临清市委员会", "location": "聊城市临清市"},
    {"id": 5, "name": "中共临清市委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共临清市委员会", "location": "聊城市临清市"},
    {"id": 6, "name": "中共临清市委员会统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共临清市委员会", "location": "聊城市临清市"},
    {"id": 7, "name": "中共临清市委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共临清市委员会", "location": "聊城市临清市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张志刚 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共临清市委书记", "start": "2025", "end": "present", "rank": "县处级", "note": "推断2025年上任，2026年7月仍在任"},
    # 周超 — 市长
    {"person_id": 2, "org_id": 2, "title": "临清市委副书记、市长", "start": "2025", "end": "present", "rank": "县处级", "note": "推断2025年上任，2026年7月仍在任"},
    # 待查_市委副书记
    {"person_id": 3, "org_id": 1, "title": "临清市委副书记（专职）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_常务副市长
    {"person_id": 4, "org_id": 2, "title": "临清市委常委、常务副市长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_纪委书记
    {"person_id": 5, "org_id": 3, "title": "临清市委常委、市纪委书记、市监委主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_组织部部长
    {"person_id": 6, "org_id": 4, "title": "临清市委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_宣传部部长
    {"person_id": 7, "org_id": 5, "title": "临清市委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "临清市委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部部长
    {"person_id": 9, "org_id": 6, "title": "临清市委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_前任市委书记
    {"person_id": 10, "org_id": 1, "title": "原临清市委书记", "start": "", "end": "2025", "rank": "县处级", "note": "姓名和去向待查"},
    # 待查_前任市长
    {"person_id": 11, "org_id": 2, "title": "原临清市长", "start": "", "end": "2025", "rank": "县处级", "note": "姓名和去向待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张志刚 ↔ 周超 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "张志刚任市委书记、周超任市长，党政班子成员", "overlap_org": "临清市", "overlap_period": "2025-至今", "confidence": "confirmed"},
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
                "person_id": f"linqings_{other['name']}",
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
            "city": "聊城市",
            "region": "临清市",
            "job": person["current_post"],
            "task_id": "shandong_临清市",
            "time_focus": "2023-2026",
        },
        "identity": {
            "person_id": f"linqings_{person['name']}",
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
            "is_current_confirmed": True if person["id"] in (1, 2) else False,
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
            "geographic_pattern": ["聊城市"],
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
            {"id": "S001", "title": "临清市人民政府官网", "url": "http://www.linqing.gov.cn/", "publisher": "临清市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官网首页要闻动态直接确认领导任职。领导分工页面(ldzc)因架构问题无法访问。"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "所有成员的完整履历均未查证；市委书记张志刚、市长周超的当前任职可通过政府官网确认，但完整履历（出生年月、教育背景、出生地、早期任职经历）均未查到。班子成员（专职副书记、常务副市长、纪委书记、组织部长、宣传部长、政法委书记、统战部长）具体人选全部待查。前任书记和前任市长信息缺失。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前市委书记张志刚的完整履历（含出生年月、教育背景、出生地、早期任职经历）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["张志刚 简历 聊城 临清", "张志刚 临清 任前公示", "张志刚 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前市长周超的完整履历", "why_it_matters": "确定其晋升路径和与市委书记的关系", "suggested_queries": ["周超 简历 临清", "周超 临清 任前公示", "周超 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "张志刚和/or 周超在2025年之前的任职经历", "why_it_matters": "核心调查目标，需了解其晋升路径", "suggested_queries": ["张志刚 调任 临清市委书记", "周超 调任 临清市长", "聊城 干部任前公示 临清"], "last_attempted": AS_OF},
            {"priority": "high", "question": "临清市委领导班子完整名单（专职副书记、常务副市长、纪委书记、组织部长、宣传部长、政法委书记、统战部长）", "why_it_matters": "完成领导班子全名单，识别关联节点", "suggested_queries": ["临清市 市委常委 2025 2026", "临清市 领导分工 2025 2026", "临清市 领导班子 成员"], "last_attempted": AS_OF},
            {"priority": "high", "question": "临清市前任市委书记的姓名和去向", "why_it_matters": "追踪聊城干部交流模式", "suggested_queries": ["临清市 原市委书记 去向", "临清 前任 书记 调任"], "last_attempted": AS_OF},
            {"priority": "high", "question": "临清市前任市长的姓名和去向", "why_it_matters": "完成干部流动分析", "suggested_queries": ["临清市 原市长 去向", "临清 前任 市长 调任"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "临清市与其他聊城下辖县区的干部交流情况", "why_it_matters": "跨区县人事网络分析", "suggested_queries": ["聊城 干部交流 临清", "临清 调任 东昌府", "临清 调任 茌平"], "last_attempted": AS_OF},
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
        filename = f"{TODAY}-山东省-聊城市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  临清市 领导班子工作关系网络")
    print(f"  等级: 县级市")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 临清市人民政府官网 linqing.gov.cn")
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

    print(f"\n✅ 临清市数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
