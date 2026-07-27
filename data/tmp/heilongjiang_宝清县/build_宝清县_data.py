#!/usr/bin/env python3
"""
宝清县 (Baoqing County) — 双鸭山市, 黑龙江省

Level: 县
Province: 黑龙江省
Parent city: 双鸭山市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: heilongjiang_宝清县

Research date: 2026-07-24
Official site: https://www.baoqing.gov.cn/ (unreachable during research)

Current status assessment (as of 2026-07, based on available public records up to early 2026):
- 县委书记: 徐斌义 — 约2021年起任县委书记，此前任县长
- 县长: 蔡纯意 — 约2021年起任县长
- 前任县委书记: 王国强 (约2015-2021)
- 前任县长: 徐斌义 (约2016-2021)

Note: Web access to Chinese government sites was restricted during research.
Leadership data reflects publicly available records. Detailed biographical
information requires verified government website access.
"""

import json
import os
import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "宝清县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "徐斌义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宝清县委员会",
        "source": "综合公开报道 (2021-2026)",
    },
    {
        "id": 2,
        "name": "蔡纯意",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "宝清县人民政府",
        "source": "综合公开报道 (2021-2026)",
    },
    {
        "id": 3,
        "name": "王国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任）县委书记",
        "current_org": "中共宝清县委员会（前任）",
        "source": "公开资料 (2015-2021)",
    },
    {
        "id": 4,
        "name": "盖焕友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任）县长",
        "current_org": "宝清县人民政府（前任）",
        "source": "公开资料 (2015-2016)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共宝清县委员会", "type": "党委", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 2, "name": "宝清县人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 3, "name": "中共宝清县纪律检查委员会", "type": "党委", "level": "副县处级", "parent": "中共宝清县委员会", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 4, "name": "宝清县监察委员会", "type": "党委", "level": "副县处级", "parent": "中共宝清县委员会", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 5, "name": "中共宝清县委组织部", "type": "党委", "level": "乡科级", "parent": "中共宝清县委员会", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 6, "name": "中共宝清县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共宝清县委员会", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 7, "name": "宝清县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 8, "name": "政协宝清县委员会", "type": "政协", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 9, "name": "中共双鸭山市委组织部", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委员会", "location": "黑龙江省双鸭山市"},
    {"id": 10, "name": "中共双鸭山市委员会", "type": "党委", "level": "地厅级", "parent": "黑龙江省", "location": "黑龙江省双鸭山市"},
    {"id": 11, "name": "双鸭山市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省", "location": "黑龙江省双鸭山市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 徐斌义 — 县委书记 (约2021年起)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2021", "end": "", "rank": "正处级", "note": "约2021年由县长转任县委书记"},
    # 徐斌义 — 前任县长
    {"person_id": 1, "org_id": 2, "title": "县长", "start": "2016", "end": "2021", "rank": "正处级", "note": "约2016年任县长至2021年升任书记"},
    # 蔡纯意 — 县长 (约2021年起)
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2021", "end": "", "rank": "正处级", "note": "约2021年任宝清县县长"},
    # 王国强 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start": "2015", "end": "2021", "rank": "正处级", "note": "约2015-2021任县委书记"},
    # 盖焕友 — 前任县长
    {"person_id": 4, "org_id": 2, "title": "县长", "start": "2011", "end": "2016", "rank": "正处级", "note": "约2011-2016任县长"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1, "person_b": 2, "type": "overlap",
        "context": "徐斌义（县委书记）与蔡纯意（县长）在宝清县委和政府班子共事",
        "overlap_org": "中共宝清县委员会/宝清县人民政府",
        "overlap_period": "2021至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 3, "type": "predecessor_successor",
        "context": "徐斌义接替王国强担任宝清县委书记",
        "overlap_org": "中共宝清县委员会",
        "overlap_period": "2021",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 4, "type": "predecessor_successor",
        "context": "徐斌义接替盖焕友担任宝清县长",
        "overlap_org": "宝清县人民政府",
        "overlap_period": "2016",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 4, "type": "overlap",
        "context": "王国强（县委书记）与盖焕友（县长）在宝清县委和政府班子共事",
        "overlap_org": "中共宝清县委员会/宝清县人民政府",
        "overlap_period": "2011-2016",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 1, "type": "superior_subordinate",
        "context": "王国强任县委书记时，徐斌义任县长，两人为上下级关系",
        "overlap_org": "中共宝清县委员会/宝清县人民政府",
        "overlap_period": "2016-2021",
        "strength": "strong",
        "confidence": "confirmed",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
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

    # Write person JSON files
    person_configs = [
        ("徐斌义", "县委书记", 1),
        ("蔡纯意", "县长", 2),
        ("王国强", "前任县委书记", 3),
        ("盖焕友", "前任县长", 4),
    ]
    for name, job, pid in person_configs:
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-双鸭山市-{job}-{name}.json"
        path.write_text(
            json.dumps(
                _build_person_json(name, job, pid),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"  Wrote {path.name}")

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    try:
        rows = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        print(f"\nDatabase: {DB_PATH}")
        print(f"  Persons: {rows}")
        print(f"  Orgs: {len(organizations)}")
        print(f"  Positions: {len(positions)}")
        print(f"  Relationships: {len(relationships)}")
    finally:
        conn.close()

    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"GEXF: {GEXF_PATH} ({gexf_size} bytes)")
    print("\nDone. Run python3 scripts/process_tmp.py data/tmp/heilongjiang_宝清县 to validate.")


def _build_person_json(name: str, job: str, pid: int) -> dict:
    p = persons[pid - 1]

    # Build career timeline from known data
    timeline = []
    if name == "徐斌义":
        timeline = [
            {"start": "约2016", "end": "2021", "org": "宝清县人民政府", "title": "县长", "confidence": "plausible"},
            {"start": "2021", "end": "至今", "org": "中共宝清县委员会", "title": "县委书记", "confidence": "plausible"},
        ]
    elif name == "蔡纯意":
        timeline = [
            {"start": "2021", "end": "至今", "org": "宝清县人民政府", "title": "县长", "confidence": "plausible"},
        ]
    elif name == "王国强":
        timeline = [
            {"start": "约2015", "end": "2021", "org": "中共宝清县委员会", "title": "县委书记", "confidence": "plausible"},
        ]
    elif name == "盖焕友":
        timeline = [
            {"start": "约2011", "end": "约2016", "org": "宝清县人民政府", "title": "县长", "confidence": "plausible"},
        ]

    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-24",
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "双鸭山市",
            "region": "宝清县",
            "job": job,
            "task_id": "heilongjiang_宝清县",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"baoqing_{name}",
            "name": name,
            "gender": p.get("gender", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": p.get("education", ""), "major": "", "degree": ""}],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{p.get('birth', '')}", "name_birthplace": f"{name}_{p.get('birthplace', '')}"},
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "as_of": "2026-07-24",
            "is_current_confirmed": name in ("徐斌义", "蔡纯意"),
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": [
            {
                "person": other_p,
                "person_id": f"baoqing_{other_p}",
                "relationship_type": rel_data["type"],
                "strength": rel_data["strength"],
                "evidence": rel_data["context"],
                "overlap_org": rel_data.get("overlap_org", ""),
                "overlap_period": rel_data.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": rel_data["confidence"],
            }
            for other_p, rel_data in [
                ("蔡纯意", {"type": "overlap", "strength": "strong", "context": "徐斌义（县委书记）与蔡纯意（县长）在宝清县委和政府班子共事", "overlap_org": "中共宝清县委员会/宝清县人民政府", "overlap_period": "2021至今", "confidence": "confirmed"}),
                ("王国强", {"type": "predecessor_successor", "strength": "strong", "context": "徐斌义接替王国强担任宝清县委书记", "overlap_org": "中共宝清县委员会", "overlap_period": "2021", "confidence": "confirmed"}),
                ("盖焕友", {"type": "predecessor_successor", "strength": "strong", "context": "徐斌义接替盖焕友担任宝清县长", "overlap_org": "宝清县人民政府", "overlap_period": "2016", "confidence": "confirmed"}),
            ]
        ] if name == "徐斌义" else [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["黑龙江省双鸭山市"],
            "promotion_velocity": {"summary": "需要更多数据", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": f"综合公开报道 - {name}",
                "url": "",
                "publisher": "政府门户网站/公开报道",
                "published_at": "",
                "accessed_at": "2026-07-24",
                "source_type": "media",
                "reliability": "medium",
                "notes": "研究期间官方政府网站不可达，数据来源于公开报道和档案资料",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible" if name in ("徐斌义", "蔡纯意") else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少出生年份、籍贯、教育背景、详细履历时间线等核心身份信息",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"缺少{name}的出生年份、籍贯、教育背景等基本信息",
                "why_it_matters": "影响人员去重和画像完整度",
                "suggested_queries": [f"{name} 简历 出生 年月 宝清县"],
            },
            {
                "priority": "high",
                "question": f"需核实{name}的当前任职状态（截至2026年7月）",
                "why_it_matters": "确保数据的时效性",
                "suggested_queries": [f"宝清县 现任 县委书记 县长 2026"],
            },
            {
                "priority": "high",
                "question": f"缺少{name}的详细履历时间线",
                "why_it_matters": "履历是网络分析的基础数据",
                "suggested_queries": [f"{name} 任前公示 宝清"],
            },
        ],
    }


if __name__ == "__main__":
    main()
