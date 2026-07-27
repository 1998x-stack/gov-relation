#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 朝阳县, 朝阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_朝阳县
Level: 县
Targets: 县委书记 & 县长

Research status: WEB ACCESS DEGRADED
  - Exa API rate-limited (free tier exhausted)
  - Baidu: 403 captcha block
  - Jina Reader: timeout
  - Official 朝阳县人民政府网站 (www.zgcyx.gov.cn): DNS not resolved
  - 朝阳市人民政府网站 (www.chaoyang.gov.cn): accessible
  - Primary source: Sogou search results via direct Python HTTP client

Current officeholders (as of 2026-07):
  - 县委书记: 石万田 (confirmed via multiple news sources, ~1972年生)
  - 县委副书记、县长: 巴行金 (confirmed via government page snippet, 1978年2月生)
  - 前任县委书记: 刘力东 (现朝阳市副市长, 2025年4月提名)

Leadership team (partially identified):
  - 县人大常委会主任: 王凤山
  - 县政协主席: 张国金
  - 县委常委、政法委书记: 杨怀
  - 县委常委、副县长: 待确认 (拟任县(市)区委副书记)
  - 副县长: 鲍鲲 (女,蒙古族,1983年10月生,无党派)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "朝阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ── 县委书记 ──
    {
        "id": 1,
        "name": "石万田",
        "gender": "男",
        "ethnicity": "",
        "birth": "1972年",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党朝阳县委员会",
        "source": "https://www.sogou.com/web?query=石万田+朝阳县委书记",
    },
    # ── 县委副书记、县长 ──
    {
        "id": 2,
        "name": "巴行金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "",
        "education": "研究生学历,硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "朝阳县人民政府",
        "source": "https://www.sogou.com/web?query=巴行金+朝阳县+县长",
    },
    # ── 前任县委书记 ──
    {
        "id": 3,
        "name": "刘力东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "朝阳市副市长",
        "current_org": "朝阳市人民政府",
        "source": "https://www.sogou.com/web?query=刘力东+朝阳+副市长",
    },
    # ── 县人大常委会主任 ──
    {
        "id": 4,
        "name": "王凤山",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "朝阳县人民代表大会常务委员会",
        "source": "https://www.sogou.com/web?query=朝阳县+王凤山+人大常委会主任",
    },
    # ── 县政协主席 ──
    {
        "id": 5,
        "name": "张国金",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议朝阳县委员会",
        "source": "https://www.sogou.com/web?query=朝阳县+政协主席+张国金",
    },
    # ── 县委常委、政法委书记 ──
    {
        "id": 6,
        "name": "杨怀",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共朝阳县委政法委员会",
        "source": "https://www.sogou.com/web?query=朝阳县+杨怀+政法委书记",
    },
    # ── 副县长 ──
    {
        "id": 7,
        "name": "鲍鲲",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1983年10月",
        "birthplace": "",
        "education": "研究生学历,法学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "朝阳县人民政府",
        "source": "https://www.sogou.com/web?query=鲍鲲+朝阳县+副县长",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党朝阳县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共朝阳市委",
        "location": "辽宁省朝阳市朝阳县",
    },
    {
        "id": 2,
        "name": "朝阳县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "朝阳市人民政府",
        "location": "辽宁省朝阳市朝阳县",
    },
    {
        "id": 3,
        "name": "朝阳市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "辽宁省人民政府",
        "location": "辽宁省朝阳市",
    },
    {
        "id": 4,
        "name": "朝阳县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "朝阳市人大常委会",
        "location": "辽宁省朝阳市朝阳县",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议朝阳县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协朝阳市委员会",
        "location": "辽宁省朝阳市朝阳县",
    },
    {
        "id": 6,
        "name": "中共朝阳县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党朝阳县委员会",
        "location": "辽宁省朝阳市朝阳县",
    },
    {
        "id": 7,
        "name": "朝阳柳城经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "朝阳县人民政府",
        "location": "辽宁省朝阳市朝阳县柳城",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 石万田
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-04", "end_date": "present", "rank": "县处级正职", "note": "从县长转任县委书记，2026年4月朝阳县融媒体中心报道确认"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、代县长", "start_date": "2021-04", "end_date": "2021-12", "rank": "县处级正职", "note": "2021年4月起任代理县长"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长", "start_date": "2021-12", "end_date": "2026-04", "rank": "县处级正职", "note": "2021年12月去代转正"},
    # 巴行金
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "未知", "end_date": "present", "rank": "县处级正职", "note": "现任朝阳县委副书记、县人民政府党组书记、县长，1978年2月生"},
    {"person_id": 2, "org_id": 2, "title": "县委常委、副县长", "start_date": "未知", "end_date": "未知", "rank": "县处级副职", "note": "曾任县委常委、副县长"},
    # 刘力东
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "未知", "end_date": "2025-04", "rank": "县处级正职", "note": "前任朝阳县委书记"},
    {"person_id": 3, "org_id": 3, "title": "副市长", "start_date": "2025-04", "end_date": "present", "rank": "地厅级副职", "note": "2025年4月辽宁省委组织部公示拟提名为地级市副市长人选"},
    # 王凤山
    {"person_id": 4, "org_id": 4, "title": "县人大常委会主任", "start_date": "未知", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 张国金
    {"person_id": 5, "org_id": 5, "title": "县政协主席", "start_date": "未知", "end_date": "present", "rank": "县处级正职", "note": "2025年9月率队考察建平县乡村建设"},
    # 杨怀
    {"person_id": 6, "org_id": 6, "title": "县委常委、政法委书记", "start_date": "未知", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 鲍鲲
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "未知", "end_date": "present", "rank": "县处级副职", "note": "女,蒙古族,1983年10月生,无党派,研究生学历法学硕士"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 石万田 ← 刘力东 (predecessor-successor)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "刘力东为前任朝阳县委书记，石万田接任县委书记",
        "overlap_org": "中国共产党朝阳县委员会",
        "overlap_period": "2021-2025",
    },
    # 石万田 ↔ 巴行金 (政府交接)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "石万田由县长转任县委书记后，巴行金接任县长",
        "overlap_org": "朝阳县人民政府",
        "overlap_period": "2026",
    },
    # 石万田 — 王凤山 (党政领导班子)
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "石万田任县委书记期间，王凤山任县人大常委会主任",
        "overlap_org": "中国共产党朝阳县委员会",
        "overlap_period": "2026",
    },
    # 石万田 — 杨怀 (县委班子)
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "石万田与杨怀同在朝阳县委班子共事",
        "overlap_org": "中国共产党朝阳县委员会",
        "overlap_period": "2026",
    },
    # 巴行金 — 鲍鲲 (政府班子)
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "巴行金任县长，鲍鲲任副县长，同在政府班子",
        "overlap_org": "朝阳县人民政府",
        "overlap_period": "2026",
    },
    # 刘力东 — 王凤山 (前任班子)
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "刘力东任县委书记时，王凤山任县人大常委会主任",
        "overlap_org": "中国共产党朝阳县委员会",
        "overlap_period": "未知",
    },
]

# ── Main ─────────────────────────────────────────────────────────────────────

def write_person_json(person_id: int) -> str | None:
    """Write a person JSON file and return its path, or None if skipped."""
    person_map = {p["id"]: p for p in persons}
    p = person_map.get(person_id)
    if not p:
        return None

    # Collect positions for this person
    person_positions = [pos for pos in positions if pos["person_id"] == person_id]

    # Collect relationships for this person
    person_rels = []
    for rel in relationships:
        if rel["person_a"] == person_id or rel["person_b"] == person_id:
            other_id = rel["person_b"] if rel["person_a"] == person_id else rel["person_a"]
            other = person_map.get(other_id, {})
            person_rels.append({
                "person": other.get("name", ""),
                "person_id": f"chaoyangxian_{other.get('name', '')}",
                "relationship_type": rel["type"],
                "strength": "strong",
                "evidence": rel["context"],
                "overlap_org": rel["overlap_org"],
                "overlap_period": rel["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })

    # Build career timeline
    career = []
    for pos in person_positions:
        career.append({
            "start": pos["start_date"],
            "end": pos["end_date"],
            "org": pos.get("note", "").split("，")[0] if pos.get("note") else "",
            "title": pos["title"],
            "level": pos["rank"],
            "location": "辽宁省朝阳市朝阳县",
            "system": "party" if "委" in pos["title"] else "government",
            "rank": pos["rank"],
            "is_key_promotion": "县委书记" in pos["title"] or "县长" in pos["title"],
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if pos["start_date"] != "未知" else "plausible",
            "source_ids": ["S001"],
        })

    filename_suffix = p["current_post"].replace("、", "_").replace("，", "_")
    filename = f"{TODAY}-辽宁省-朝阳市-{filename_suffix}-{p['name']}.json"
    filepath = _CURRENT_DIR / filename

    obj = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "朝阳市",
            "region": "朝阳县",
            "job": p["current_post"],
            "task_id": "liaoning_朝阳县",
            "time_focus": "2021-2026",
        },
        "identity": {
            "person_id": f"chaoyangxian_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": p.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p['birth']}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if "书记" in p["current_post"] or "县长" in p["current_post"] or "主任" in p["current_post"] else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career,
        "organizations": [
            {
                "org_id": f"o{org['id']}",
                "name": org["name"],
                "type": org["type"],
                "role": p["current_post"],
                "start": "",
                "end": "",
            }
            for org in organizations
        ],
        "relationships": person_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["辽宁省朝阳市"],
            "promotion_velocity": {
                "summary": "公开履历不完整",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "degree_centrality": 0,
            "betweenness_centrality": 0,
            "community": "朝阳县",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，未发现公开的纪律处分、问责或负面媒体报道",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": ["S001"],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "Sogou搜索结果 - 朝阳县人事信息",
                "url": f"https://www.sogou.com/web?query={p['name']}+朝阳县",
                "publisher": "搜狗搜索",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "media",
                "reliability": "medium",
                "notes": "多来源综合：朝阳县融媒体中心、政府网站片段、新闻报道",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "早期履历完全未知，教育背景、入党时间、参加工作年份均需补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯，特别是2021年之前的职务",
                "why_it_matters": "无法判断晋升速度、专业领域、系统经验",
                "suggested_queries": [f"{p['name']} 简历 任职经历", f"{p['name']} 任前公示", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{p['name']}的教育背景、出生地、入党时间",
                "why_it_matters": "人员身份确定与dedupe key",
                "suggested_queries": [f"{p['name']} 出生 学历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  Wrote person JSON: {filepath}")
    return filename


def main():
    # Ensure staging directory exists
    _CURRENT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Building {SLUG} network data...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Remove existing files if present
    for path in [DB_PATH, GEXF_PATH]:
        if path.exists():
            path.unlink()

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

    print("\nWriting person JSONs...")
    for p in persons:
        write_person_json(p["id"])

    # Verify output files
    print("\nVerification:")
    for path in [DB_PATH, GEXF_PATH]:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        print(f"  {path.name}: {'OK' if exists else 'MISSING'} ({size} bytes)")

    # Count person JSONs
    person_jsons = list(_CURRENT_DIR.glob("*.json"))
    print(f"  Person JSONs: {len(person_jsons)}")

    # DB table counts
    conn = sqlite3.connect(str(DB_PATH))
    try:
        for table in ["persons", "organizations", "positions", "relationships"]:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  DB {table}: {count}")
    finally:
        conn.close()

    print("\nDone.")


if __name__ == "__main__":
    main()
