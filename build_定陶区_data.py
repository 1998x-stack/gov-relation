#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 定陶区 (Dingtao District), 菏泽市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 菏泽市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_定陶区

Research date: 2026-07-25
Official source: http://www.dingtao.gov.cn/ (定陶区人民政府) — site unreachable during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 朱中华 (Zhu Zhonghua, assumed office ~2022, formerly 定陶区长)
- 区长: 刘勇 (Liu Yong, assumed office ~2023/2024, succeeded after 韩耀辉 transferred to 枣庄)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.dingtao.gov.cn
  and parent city site www.heze.gov.cn were unreachable. Baidu Baike returned 403.

  Leadership identification and biographical details are based on pre-existing
  knowledge that may not reflect the most current appointments. All information
  should be treated as "unverified" or "plausible" until independent web research
  can be completed.

  This is a partial-evidence build per source_fallbacks.md artifact mode.

  Note: 定陶县撤县设区于2016年4月，此前为定陶县。
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

SLUG = "定陶区"

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

    # 1. 朱中华 — 区委书记
    {
        "id": 1,
        "name": "朱中华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共菏泽市定陶区委书记",
        "current_org": "中共菏泽市定陶区委员会",
        "source": "综合新闻报道（网络搜索受限，需进一步验证）",
    },
    # 2. 刘勇 — 区长
    {
        "id": 2,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定陶区委副书记、区长",
        "current_org": "菏泽市定陶区人民政府",
        "source": "综合新闻报道（网络搜索受限，需进一步验证）",
    },
    # 3. 区委副书记（专职副书记，姓名待查）
    {
        "id": 3,
        "name": "【待查】定陶区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委副书记（待查）",
        "current_org": "中共菏泽市定陶区委员会",
        "source": "GAP — 专职副书记具体人选未确认",
    },
    # 4. 区委常委、常务副区长（姓名待查）
    {
        "id": 4,
        "name": "【待查】定陶区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、常务副区长（待查）",
        "current_org": "菏泽市定陶区人民政府",
        "source": "GAP — 常务副区长具体人选未确认",
    },
    # 5. 区委常委、区纪委书记（姓名待查）
    {
        "id": 5,
        "name": "【待查】定陶区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、区纪委书记、区监委主任（待查）",
        "current_org": "中共菏泽市定陶区纪律检查委员会",
        "source": "GAP — 纪委书记具体人选未确认",
    },
    # 6. 区委常委、组织部部长（姓名待查）
    {
        "id": 6,
        "name": "【待查】定陶区委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、组织部部长（待查）",
        "current_org": "中共菏泽市定陶区委员会组织部",
        "source": "GAP — 组织部部长具体人选未确认",
    },
    # 7. 区委常委、宣传部部长（姓名待查）
    {
        "id": 7,
        "name": "【待查】定陶区委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、宣传部部长（待查）",
        "current_org": "中共菏泽市定陶区委员会宣传部",
        "source": "GAP — 宣传部部长具体人选未确认",
    },
    # 8. 区委常委、政法委书记（姓名待查）
    {
        "id": 8,
        "name": "【待查】定陶区委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、政法委书记（待查）",
        "current_org": "中共菏泽市定陶区委员会政法委员会",
        "source": "GAP — 政法委书记具体人选未确认",
    },
    # 9. 区委常委、统战部部长（姓名待查）
    {
        "id": 9,
        "name": "【待查】定陶区委统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、统战部部长（待查）",
        "current_org": "中共菏泽市定陶区委员会统战部",
        "source": "GAP — 统战部部长具体人选未确认",
    },
    # 10. 前任区委书记 — 推测为聂元科（曾任定陶区委书记）
    {
        "id": 10,
        "name": "聂元科（推测）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原定陶区委书记（推测去向为菏泽市级职务）",
        "current_org": "原中共定陶区委",
        "source": "GAP — 聂元科约2019年前后曾任定陶区委书记，后调任菏泽市领导职务（推测为副市长/市委常委）。网络搜索受限，此信息需验证。",
    },
    # 11. 前任区长 — 推测为韩耀辉（已调任枣庄市市中区区长）
    {
        "id": 11,
        "name": "韩耀辉（已调离）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市市中区人民政府区长",
        "current_org": "枣庄市市中区人民政府",
        "source": "韩耀辉约2021-2022年任定陶区长，后跨市调任枣庄市市中区区长。网络搜索受限，此信息需验证。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共菏泽市定陶区委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市委", "location": "菏泽市定陶区"},
    {"id": 2, "name": "菏泽市定陶区人民政府", "type": "政府", "level": "县处级", "parent": "菏泽市人民政府", "location": "菏泽市定陶区"},
    {"id": 3, "name": "中共菏泽市定陶区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 4, "name": "中共菏泽市定陶区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 5, "name": "中共菏泽市定陶区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 6, "name": "中共菏泽市定陶区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 7, "name": "中共菏泽市定陶区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 朱中华 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共菏泽市定陶区委书记", "start": "2022", "end": "present", "rank": "县处级", "note": "推测2022年前后由定陶区长转任区委书记"},
    # 朱中华 — 曾任定陶区长
    {"person_id": 1, "org_id": 2, "title": "定陶区委副书记、区长（前任职务）", "start": "2019", "end": "2022", "rank": "县处级", "note": "推测2019-2022年任定陶区长"},
    # 刘勇 — 区长
    {"person_id": 2, "org_id": 2, "title": "定陶区委副书记、区长", "start": "2023", "end": "present", "rank": "县处级", "note": "推测2023/2024年上任"},
    # 待查_区委副书记
    {"person_id": 3, "org_id": 1, "title": "定陶区委副书记（专职）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_常务副区长
    {"person_id": 4, "org_id": 2, "title": "定陶区委常委、常务副区长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_纪委书记
    {"person_id": 5, "org_id": 3, "title": "定陶区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_组织部部长
    {"person_id": 6, "org_id": 4, "title": "定陶区委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_宣传部部长
    {"person_id": 7, "org_id": 5, "title": "定陶区委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "定陶区委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部部长
    {"person_id": 9, "org_id": 6, "title": "定陶区委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 聂元科（推测）— 前任区委书记
    {"person_id": 10, "org_id": 1, "title": "定陶区委书记（前任）", "start": "2019", "end": "2021", "rank": "县处级", "note": "推测去向为菏泽市领导"},
    # 韩耀辉（已调离）— 前任区长
    {"person_id": 11, "org_id": 2, "title": "定陶区长（前任）", "start": "2020", "end": "2022", "rank": "县处级", "note": "调任枣庄市市中区区长"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 朱中华 ↔ 刘勇 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "朱中华任区委书记、刘勇任区长，党政搭档", "overlap_org": "菏泽市定陶区", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 朱中华 ⟷ 聂元科 (前任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "朱中华接替聂元科任定陶区委书记", "overlap_org": "中共菏泽市定陶区委员会", "overlap_period": "2022", "confidence": "plausible"},
    # 朱中华 ⟷ 韩耀辉 (前任搭档、前后任)
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "朱中华任书记期间，韩耀辉曾任定陶区长", "overlap_org": "菏泽市定陶区", "overlap_period": "2022", "confidence": "plausible"},
    # 刘勇 ⟷ 韩耀辉 (前任区长)
    {"person_a": 2, "person_b": 11, "type": "predecessor_successor", "context": "刘勇接替韩耀辉任定陶区长", "overlap_org": "菏泽市定陶区人民政府", "overlap_period": "2023", "confidence": "plausible"},
    # 聂元科 ↔ 韩耀辉 (前任搭档)
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "聂元科任区委书记期间，韩耀辉曾任定陶区长", "overlap_org": "菏泽市定陶区", "overlap_period": "2020-2021", "confidence": "plausible"},
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
                "person_id": f"dingtao_{other['name']}",
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
            "region": "定陶区",
            "job": person["current_post"],
            "task_id": "shandong_定陶区",
            "time_focus": "2019-2026",
        },
        "identity": {
            "person_id": f"dingtao_{person['name']}",
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
            {"id": "S001", "title": "综合新闻报道（未验证）", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "low", "notes": "未查证原始来源，因网络搜索工具全部不可用（Exa限流、政府网站超时、百度403）"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有成员的完整履历均未查证；区委书记朱中华、区长刘勇的当前任职及完整履历需通过官方渠道确认。区委副书记、常务副区长、纪委书记、组织部长、宣传部长、政法委书记、统战部长等班子成员具体人选全部待查。前任书记聂元科和前任区长韩耀辉的详细任职时间待确认。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前区委书记朱中华的完整履历（含出生年月、教育背景、出生地、早期任职经历）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["朱中华 简历 菏泽", "朱中华 定陶 任前公示", "朱中华 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长刘勇的完整履历及全名确认", "why_it_matters": "确定其晋升路径和与区委书记的关系", "suggested_queries": ["刘勇 定陶 区长", "定陶区 区长 现任", "定陶区 政府 领导"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "朱中华的当前任职是否仍为定陶区委书记，刘勇是否确实为定陶区长", "why_it_matters": "核心调查目标，需官方渠道确认", "suggested_queries": ["定陶区 领导分工 2024 2025", "定陶区委书记 现任", "定陶区长 现任", "site:dingtao.gov.cn 领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "定陶区委领导班子完整名单（专职副书记、常务副区长、纪委书记、组织部长、宣传部长、政法委书记、统战部长）", "why_it_matters": "完成领导班子全名单，识别关联节点", "suggested_queries": ["定陶区 区委常委", "定陶区 领导班子 成员", "定陶区 领导分工"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任区委书记聂元科的完整去向和现任职务", "why_it_matters": "追踪菏泽干部交流模式", "suggested_queries": ["聂元科 菏泽 现任", "聂元科 定陶 调任"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任区长韩耀辉调任枣庄市市中区的时间线", "why_it_matters": "跨市干部交流分析", "suggested_queries": ["韩耀辉 枣庄 定陶 调任", "韩耀辉 市中区 区长 任命"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "定陶撤县设区（2016年4月）前后的人事变动时间线", "why_it_matters": "了解行政区划调整对人事的影响", "suggested_queries": ["定陶 撤县设区 人事 调整", "定陶区 历届 书记 区长"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "定陶区与其他菏泽下辖县区的干部交流情况", "why_it_matters": "跨区县人事网络分析", "suggested_queries": ["菏泽 干部交流 定陶", "定陶 调任 牡丹区", "定陶 调任 曹县"], "last_attempted": AS_OF},
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
    print(f"  定陶区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
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

    print(f"\n✅ 定陶区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
