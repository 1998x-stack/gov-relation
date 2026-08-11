#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 荆州市 (Jingzhou City), 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_荆州市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.jingzhou.gov.cn (荆州市人民政府门户网站) — homepage news feed confirming the
    current 市委书记 (汪元程) and 市委副书记、市长 (李迎伟), accessed 2026-08-06.

Confidence notes:
  - 汪元程 (市委书记): current role CONFIRMED via official jingzhou.gov.cn headline
    "汪元程率队赴四川成都开展招商考察" (2026-08-03至05).
  - 李迎伟 (市委副书记、市长): current role CONFIRMED via multiple official
    jingzhou.gov.cn headlines dated 2026-08-05/08-06.
  - Web access to external biography sources (Wikipedia, Baidu Baike, Jina, Exa,
    Bing, Xinhua, Hubei provincial sites) was blocked or rate-limited during this
    session. Full biographies (birth/birthplace/education/party join/work start/
    prior postings) could NOT be verified. Those fields are therefore left empty
    and recorded as open questions — NO biographical dates are fabricated.

Person/org/position data below is the structurally-valid core confirmed as of
2026-08-06 from the official portal.
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Allow importing gov_relation regardless of where this script lives
# (staging dir data/tmp/... or canonical scripts/build/...).
for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "荆州市"
AS_OF = "2026-08-06"
TODAY = datetime.now().strftime("%Y%m%d")

# Artifacts are written next to this script (staging dir while investigating).
# process_tmp.py copies them to canonical destinations on promotion.
HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed current roles) ────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "汪元程",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共荆州市委员会",
        "source": "https://www.jingzhou.gov.cn/",
    },
    {
        "id": 2,
        "name": "李迎伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "荆州市人民政府",
        "source": "https://www.jingzhou.gov.cn/",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共荆州市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共湖北省委",
        "location": "湖北省荆州市",
    },
    {
        "id": 2,
        "name": "荆州市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "湖北省人民政府",
        "location": "湖北省荆州市",
    },
]

# ── Positions (current, as-of 2026-08-06, official-confirmed) ────────────
positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "市委书记",
        "start_date": "2026-",
        "end_date": "",
        "rank": "正厅级",
        "note": "在任（截至2026-08-06官网新闻确认）",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "市长",
        "start_date": "2026-",
        "end_date": "",
        "rank": "正厅级",
        "note": "在任，市委副书记、市长（截至2026-08-06官网新闻确认）",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "市委副书记",
        "start_date": "2026-",
        "end_date": "",
        "rank": "副厅级",
        "note": "在任，市委副书记、市长（截至2026-08-06官网新闻确认）",
    },
]

# ── Relationships (confirmed co-office overlap) ───────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "市委书记—市长（市委领导班子成员）",
        "overlap_org": "中共荆州市委员会",
        "overlap_period": "2026至今",
    },
]

# ── Person JSONs (deep per-figure profiles) ───────────────────────────────
def build_person_json(person: dict, current_post: str, current_org: str,
                      job: str, admin_rank: str) -> dict:
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "荆州市",
            "region": "荆州市",
            "job": job,
            "task_id": "hubei_荆州市",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"jingzhou_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": "https://www.jingzhou.gov.cn/",
            },
        },
        "current_status": {
            "current_post": current_post,
            "current_org": current_org,
            "administrative_rank": admin_rank,
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "2026-",
                "end": "present",
                "org": current_org,
                "title": current_post,
                "level": "地级市",
                "location": "湖北省荆州市",
                "system": "party" if current_post == "市委书记" else "government",
                "rank": admin_rank,
                "is_key_promotion": True,
                "notes": "在任，官方（荆州市人民政府门户网站）2026-08-06 确认",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料在本次调研中无法访问，早期履历（出生、籍贯、学历、入党、工作起点、晋升时间线）未获取",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {
                "org": "中共荆州市委员会",
                "type": "党委",
                "level": "地级市",
                "location": "湖北省荆州市",
            },
            {
                "org": "荆州市人民政府",
                "type": "政府",
                "level": "地级市",
                "location": "湖北省荆州市",
            },
        ],
        "relationships": [
            {
                "person": "汪元程" if name != "汪元程" else "李迎伟",
                "person_id": "jingzhou_汪元程" if name != "汪元程" else "jingzhou_李迎伟",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "市委会市一书记—市长 同市领导班子成员（2026 年）",
                "overlap_org": "中共荆州市委员会",
                "overlap_period": "2026至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "governance_record": [
            {
                "period": "2026",
                "domain": "public_security" if name == "李迎伟" else "economic_development",
                "achievement_or_event": "市委书记率队赴四川成都开展招商考察" if name == "汪元程" else "市长专题调度'群腐'集中整治整改、赴松滋督办磷石膏综合治理、调研督导洪湖流域综合治理",
                "role_in_event": "带队招商" if name == "汪元程" else "专题调度/督办/调研",
                "measurable_outcome": "",
                "location": "荆州市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "本次调研（官方新闻范围）未发现负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "荆州市人民政府门户网站 首页要闻",
                "url": "https://www.jingzhou.gov.cn/",
                "publisher": "荆州市人民政府",
                "published_at": "2026-08-06",
                "accessed_at": "2026-08-06",
                "source_type": "official",
                "reliability": "high",
                "notes": "官网首页新闻确认市委书记（汪元程）、市委副书记、市长（李迎伟）在任",
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整履历（出生/籍贯/学历/入党/工作起点/此前任职）未访问到；网络访问受限",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name} 的完整履历（出生年月/籍贯/学历/入党时间/工作起始/晋升时间线）",
                "why_it_matters": "仅有当前职务确认，缺关键身份与履历，无法深入分析与关系网络构建",
                "suggested_queries": [
                    f"荆州市 市委书记 汪元程 简历",
                    f"荆州市 市长 李迎伟 简历",
                    "荆州市 领导之窗",
                    "湖北省 荆州市 组织部 任前公示",
                ],
                "last_attempted": "2026-08-06",
            }
        ],
    }


def main() -> None:
    # Build the canonical DB + GEXF.
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
    print(f"Built artifacts: {DB_PATH}, {GEXF_PATH}")

    # Person JSONs (written to staging dir; process_tmp promotes them).
    jobs = [
        ("市委书记", "中共荆州市委员会", "正厅级"),
        ("市长", "荆州市人民政府", "正厅级"),
    ]
    for person, (job, org, rank) in zip([persons[0], persons[1]], jobs):
        data = build_person_json(person, person["current_post"], person["current_org"], job, rank)
        out = HERE / f"{TODAY}-湖北省-荆州市-{job}-{person['name']}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Wrote person json: {out}")

    # Summary — verify the built DB by reading it back.
    conn = sqlite3.connect(str(DB_PATH))
    try:
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ("persons", "organizations", "positions", "relationships")}
    finally:
        conn.close()
    print("=" * 50)
    print(f"SLUG: {SLUG}")
    for table, n in counts.items():
        print(f"{table}: {n}")
    print("=" * 50)


if __name__ == "__main__":
    main()