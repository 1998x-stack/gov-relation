#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 广灵县 (Guangling County), 大同市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_广灵县
Level: 县
Targets: 县委书记 & 县长

Research context:
  - Web search tools (Exa, Google, Baidu) were unavailable during this run.
  - Government site www.guangling.gov.cn timed out.
  - All information is from training data knowledge, NOT from current web verification.
  - Each claim is labeled with confidence: "confirmed", "plausible", or "unverified".
  - This artifact is generated under partial-evidence mode as specified in source_fallbacks.md.

Confidence notes:
  - Most career timeline entries are "unverified" — they reflect training data that may not
    reflect current (2026) officeholders.
  - Names and positions for core leaders (县委书记, 县长) should be verified against
    current official sources when web access becomes available.
  - Predecessor/successor chains are particularly uncertain.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "广灵县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_广灵县"
if _CURRENT_DIR.name == "shanxi_广灵县":
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
# IDs: 1-2 core leadership, 3-9 standing committee + deputy mayors, 10+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current, from training data - UNVERIFIED)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "董雄伟",  # 广灵县委书记 (last known from training data)
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县委书记",
        "current_org": "中共广灵县委员会",
        "source": "训练数据知识（需通过官方页面验证）",
        "notes": "董雄伟曾以广灵县委书记身份出现在公开报道中。完整履历、当前任职状态需通过广灵县政府网站或大同市委组织部确认。",
        "confidence": "unverified"
    },
    {
        "id": 2,
        "name": "梁军",  # 广灵县长 (last known from training data)
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县长",
        "current_org": "广灵县人民政府",
        "source": "训练数据知识（需通过官方页面验证）",
        "notes": "梁军曾以广灵县长身份出现在公开报道中。当前任职状态需通过官方来源确认。",
        "confidence": "unverified"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Deputy County Heads (largely unknown)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "广灵县人民政府",
        "source": "需通过官方网站查询",
        "notes": "信息缺口：广灵县领导班子成员（包括常务副县长、县委副书记、纪委书记、组织部长等）均需通过政府网站ldzc页面或大同市委组织部任前公示确认。",
        "confidence": "unverified"
    },
    {
        "id": 4,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共广灵县委员会",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共广灵县纪律检查委员会",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共广灵县委组织部",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共广灵县委宣传部",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共广灵县委政法委员会",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (all unverified from training data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "待查_前任县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任",
        "current_org": "中共广灵县委员会",
        "source": "需通过百度百科或新闻报道确认",
        "notes": "广灵县前任县委书记的姓名、去向均需通过搜索确认。董雄伟之前的前任书记可能是王丽萍或其他。",
        "confidence": "unverified"
    },
    {
        "id": 10,
        "name": "待查_前任县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任",
        "current_org": "广灵县人民政府",
        "source": "需通过百度百科或新闻报道确认",
        "notes": "广灵县前任县长的姓名、去向均需通过搜索确认。",
        "confidence": "unverified"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共广灵县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 2,
        "name": "广灵县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 3,
        "name": "中共广灵县纪律检查委员会",
        "type": "纪律检查",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 4,
        "name": "广灵县监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 5,
        "name": "中共广灵县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "广灵县",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 6,
        "name": "中共广灵县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "广灵县",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 7,
        "name": "中共广灵县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "广灵县",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 8,
        "name": "广灵县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议广灵县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市广灵县"
    },
    {
        "id": 10,
        "name": "中共大同市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "山西省",
        "location": "山西省大同市"
    },
    {
        "id": 11,
        "name": "大同市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "山西省",
        "location": "山西省大同市"
    },
    {
        "id": 12,
        "name": "中共大同市委组织部",
        "type": "党委",
        "level": "地市级",
        "parent": "大同市",
        "location": "山西省大同市"
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # Current leaders (unverified)
    {"person_id": 1, "org_id": 1, "title": "广灵县委书记", "start_date": "未知", "end_date": "现任", "rank": "正处级", "note": "当前任职日期需确认"},
    {"person_id": 2, "org_id": 2, "title": "广灵县长", "start_date": "未知", "end_date": "现任", "rank": "正处级", "note": "当前任职日期需确认"},
    # Standing committee members (placeholders)
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 5, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 6, "org_id": 5, "title": "县委常委、组织部部长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 7, "org_id": 6, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 8, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "姓名待查"},
    # Predecessors (placeholders)
    {"person_id": 9, "org_id": 1, "title": "广灵县委书记（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名和去向待查"},
    {"person_id": 10, "org_id": 2, "title": "广灵县长（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名和去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Very limited — can only define structural relationships based on organization hierarchy

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长为党政主要领导搭档关系",
        "overlap_org": "广灵县",
        "overlap_period": "当前任职期（待确认）"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长为上下级关系",
        "overlap_org": "广灵县",
        "overlap_period": "当前任职期"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长为正副手关系",
        "overlap_org": "广灵县人民政府",
        "overlap_period": "当前任职期"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记为领导与被监督关系",
        "overlap_org": "中共广灵县委员会",
        "overlap_period": "当前任职期"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与县委副书记（通常兼任县长或专职副书记）",
        "overlap_org": "广灵县",
        "overlap_period": "当前任职期"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "predecessor_successor",
        "context": "现任县委书记与前任县委书记的接替关系",
        "overlap_org": "中共广灵县委员会",
        "overlap_period": "职务交接期"
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "predecessor_successor",
        "context": "现任县长与前任县长的接替关系",
        "overlap_org": "广灵县人民政府",
        "overlap_period": "职务交接期"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

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

    # Write person JSON files for core leaders
    write_person_json(1, persons[0])
    write_person_json(2, persons[1])

    print(f"\n═══ Done — {SLUG} ═══")
    print(f"  Persons: {len(persons)} ({sum(1 for p in persons if '待查' not in p['name'])} named)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n  ⚠ NOTE: Most claims are unverified due to web access limitations.")
    print(f"  Run with verified data when web search is available.")
    print(f"  Confidence for core leader names: unverified (from training data).")
    print(f"  See open_gaps.md for priority research gaps.")


def write_person_json(pid: int, pdata: dict) -> None:
    """Write a person JSON file following the person_graph_json.md schema."""
    from datetime import date

    name = pdata["name"]
    job = pdata.get("current_post", "").replace("/", "_")
    fname = f"{TODAY}-山西省-大同市-{job}-{name}.json"
    fpath = PJSON_DIR / fname

    # Determine confidence string for current_role
    current_conf = "unverified" if "待查" in name or not name else "unverified"

    person_record = {
        "schema_version": "1.0",
        "generated_at": str(date.today()),
        "investigation_scope": {
            "province": "山西省",
            "city": "大同市",
            "region": "广灵县",
            "job": pdata.get("current_post", ""),
            "task_id": "shanxi_广灵县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"guangling_{name}",
            "name": name,
            "aliases": [],
            "gender": pdata.get("gender", ""),
            "ethnicity": pdata.get("ethnicity", ""),
            "birth": pdata.get("birth", ""),
            "birthplace": pdata.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": pdata.get("party_join", ""),
            "work_start": pdata.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_" if not pdata.get("birth") else f"{name}_{pdata['birth']}",
                "name_birthplace": f"{name}_" if not pdata.get("birthplace") else f"{name}_{pdata['birthplace']}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": pdata.get("current_post", ""),
            "current_org": pdata.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "履历信息不可用 - 需通过Web搜索补充",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断需要基于公开报道、讲话记录和治理行动，当前无可用信息来源。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开纪律处分或负面报道（搜索受限，无法全面检索）",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": current_conf,
            "current_role": current_conf,
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有身份信息和履历数据均需通过Web搜索验证。广灵县政府网站无法访问。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的当前任职状态。{job}是否仍由{name}担任？",
                "why_it_matters": "这是本次调研的核心人物，需要确认2026年最新的任职信息",
                "suggested_queries": [
                    f"广灵{job[:2]} {name}",
                    f"www.guangling.gov.cn 领导之窗",
                    f"大同市 广灵县 最新人事任免"
                ],
                "last_attempted": str(date.today())
            },
            {
                "priority": "critical",
                "question": f"{name}的完整履历（出生、教育、历任职务、晋升时间）",
                "why_it_matters": "没有履历就无法进行关系网络分析和跨县流动追踪",
                "suggested_queries": [
                    f"{name} 简历 任职经历",
                    f"{name} 百度百科",
                    f"{name} 任前公示"
                ],
                "last_attempted": str(date.today())
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


if __name__ == "__main__":
    main()
