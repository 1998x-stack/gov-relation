#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Zhaozhou County leadership network.

肇州县 (Zhaozhou County) — 黑龙江省大庆市. Generates:
  - SQLite DB (persons, organizations, positions, relationships)
  - GEXF graph
  - Person JSON profiles for core leaders

Source of truth: official 肇州县人民政府 www.zhaozhou.gov.cn 政府领导 bio pages +
Daqing/Heilongjiang appointment news. Names confirmed as of 2026-08-05.
"""

import json
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _ in range(6):
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    REPO_ROOT = REPO_ROOT.parent
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "肇州县"
TODAY = date.today().strftime("%Y%m%d")

# ── Paths (relative to repo root) ──
# When GOV_REL_DATABASE_DIR is set (staging mode), write DB/GEXF/person JSON
# directly into that dir so process_tmp can collect and promote them.
_STAGE = os.getenv("GOV_REL_DATABASE_DIR")
if _STAGE:
    DATA_DIR = Path(_STAGE)
    DB_PATH = DATA_DIR / f"{SLUG}_network.db"
    GEXF_PATH = DATA_DIR / f"{SLUG}_network.gexf"
    PERSONS_DIR = DATA_DIR
else:
    DATA_DIR = REPO_ROOT / "data"
    DB_PATH = DATA_DIR / "database" / f"{SLUG}_network.db"
    GEXF_PATH = DATA_DIR / "graph" / f"{SLUG}_network.gexf"
    PERSONS_DIR = DATA_DIR / "persons"

# ══════════════════════════════════════════════
#  PERSONS
# ══════════════════════════════════════════════

persons = [
    # ── 县委书记 (Party Secretary) ──
    {"id": 1, "name": "孟庆鑫", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "肇州县委书记", "current_org": "中共肇州县委员会",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/xxfb11/202607/c05_415126.shtml"},
    # ── 县长 (County Mayor) ──
    {"id": 2, "name": "邰瑞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委副书记、县政府县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202212/c05_160737.shtml"},
    # ── 县委常委、政府副县长 (Party Committee Standing Members / Deputy Mayors) ──
    {"id": 3, "name": "史国庆", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、县政府副县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202212/c05_160740.shtml"},
    {"id": 4, "name": "陈本聪", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、县政府副县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202412/c05_362946.shtml"},
    {"id": 5, "name": "孙秀凤", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、县政府副县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202504/c05_375804.shtml"},
    {"id": 6, "name": "丁浩力", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、县政府副县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202504/c05_375805.shtml"},
    # ── 副县长 (Deputy Mayor) / 公安局局长 ──
    {"id": 7, "name": "渠修泉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202212/c05_160736.shtml"},
    {"id": 8, "name": "封国平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202311/c05_320116.shtml"},
    {"id": 9, "name": "张超", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202212/c05_160741.shtml"},
    {"id": 10, "name": "王伟业", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "肇州县人民政府",
     "source": "http://www.zhaozhou.gov.cn/zhaozhou/zhengfulingdao/202504/c05_375807.shtml"},
]

# ══════════════════════════════════════════════
#  ORGANIZATIONS
# ══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共肇州县委员会", "type": "party", "level": "县级",
     "parent": "中共大庆市委员会", "location": "黑龙江省大庆市肇州县"},
    {"id": 2, "name": "肇州县人民政府", "type": "government", "level": "县级",
     "parent": "大庆市人民政府", "location": "黑龙江省大庆市肇州县"},
    {"id": 3, "name": "肇州县公安局", "type": "government", "level": "县级",
     "parent": "肇州县人民政府", "location": "黑龙江省大庆市肇州县"},
    {"id": 4, "name": "肇州县人民代表大会常务委员会", "type": "npc", "level": "县级",
     "parent": "大庆市人民代表大会常务委员会", "location": "黑龙江省大庆市肇州县"},
    {"id": 5, "name": "中国人民政治协商会议肇州县委员会", "type": "cppcc", "level": "县级",
     "parent": "中国人民政治协商会议大庆市委员会", "location": "黑龙江省大庆市肇州县"},
    {"id": 6, "name": "中共大庆市委员会", "type": "party", "level": "地级",
     "parent": "中共黑龙江省委员会", "location": "黑龙江省大庆市"},
    {"id": 7, "name": "中共黑龙江省委员会", "type": "party", "level": "省级",
     "parent": "", "location": "黑龙江省哈尔滨市"},
]

# ══════════════════════════════════════════════
#  POSITIONS
# ══════════════════════════════════════════════

positions = [
    {"person_id": 1, "org_id": 1, "title": "肇州县委书记",
     "start_date": "~2024", "end_date": "至今", "rank": "正处级",
     "note": "主持县委全面工作；主持召开县委十八届常委会"},
    {"person_id": 2, "org_id": 2, "title": "肇州县委副书记、县政府县长",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "主持县政府全面工作；主持县政府第十八届常务会议"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、县政府副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "政府班子兼县委常委"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、县政府副县长",
     "start_date": "~2024-12", "end_date": "至今", "rank": "副处级", "note": "政府班子兼县委常委"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、县政府副县长",
     "start_date": "~2025-04", "end_date": "至今", "rank": "副处级", "note": "政府班子兼县委常委"},
    {"person_id": 6, "org_id": 2, "title": "县委常委、县政府副县长",
     "start_date": "~2025-04", "end_date": "至今", "rank": "副处级", "note": "政府班子兼县委常委"},
    {"person_id": 7, "org_id": 3, "title": "副县长、县公安局局长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "主持公安工作"},
    {"person_id": 8, "org_id": 2, "title": "副县长",
     "start_date": "~2023-11", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长",
     "start_date": "~2025-04", "end_date": "至今", "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════
#  RELATIONSHIPS
# ══════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "现任县委书记与县长搭档，共同主持县领导班子工作",
     "overlap_org": "肇州县党委·县政府班子", "overlap_period": "县委十八届至今"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长：政府班子（公安岗）", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系", "overlap_org": "肇州县人民政府", "overlap_period": "至今"},
]


# ══════════════════════════════════════════════
#  PERSON JSON WRITER
# ══════════════════════════════════════════════

def write_person_json(person: dict) -> str:
    """Write a person JSON profile for a core figure."""
    # map to short job label for filename
    post_slug = {
        1: "县委书记",
        2: "县长",
    }.get(person["id"], person["current_post"].replace("肇州县", "").replace("，", "_"))
    name_slug = person["name"]
    filename = f"{TODAY}-黑龙江省-大庆市-{post_slug}-{name_slug}.json"
    filepath = PERSONS_DIR / filename

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "大庆市",
            "region": "肇州县",
            "job": person["current_post"],
            "task_id": "heilongjiang_肇州县",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": f"zhaozhou_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender") or "",
            "ethnicity": person.get("ethnicity") or "",
            "birth": person.get("birth") or "",
            "birthplace": person.get("birthplace") or "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级",
                "location": "黑龙江省大庆市肇州县",
                "system": "party" if ("书记" in person["current_post"]) else "government",
                "rank": "县处级正职" if ("书记" in person["current_post"] or "县长" in person["current_post"]) else "县处级副职",
                "is_key_promotion": True,
                "notes": f"现任{person['current_post']}（肇州县人民政府官网确认）",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "暂无公开的性格/工作风格资料。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "肇州县人民政府·政府领导 bio 页",
                "url": person["source"],
                "publisher": "肇州县人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "当前职务以官网发布为准",
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、教育背景及完整履历缺失（官网县级领导页未公开）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"现任{person['current_post']}的出生年月、籍贯、教育背景及完整职业生涯？",
                "why_it_matters": "核心领导人的深度履历是人事网络分析的基础",
                "suggested_queries": [
                    f"{person['name']} 简历",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 大庆 任职经历",
                ],
                "last_attempted": TODAY,
            }
        ],
    }

    PERSONS_DIR.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  [ok]  {filename}")
    return filename


def main():
    print("=" * 60)
    print("  肇州县 — 领导班子工作关系网络")
    print(f"  Generated: {TODAY}")
    print("  Source: 肇州县人民政府官网 (www.zhaozhou.gov.cn)")
    print("=" * 60)

    # ── Build database + GEXF ──
    print("\nBuilding database and GEXF graph...")
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
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Verify the database contains the 4 expected tables
    conn = sqlite3.connect(str(DB_PATH))
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    for req in ("persons", "organizations", "positions", "relationships"):
        assert req in tables, f"missing table {req}"
    print("  DB tables OK: persons, organizations, positions, relationships")

    # ── People JSON file (core leaders: 县委书记, 县长) ──
    print("\nWriting person JSON files for core leaders...")
    core_leader_ids = [1, 2]
    json_files = []
    for pid in core_leader_ids:
        person = next(p for p in persons if p["id"] == pid)
        json_files.append(write_person_json(person))

    # ── Summary ──
    print()
    print("─" * 60)
    print("  统计摘要")
    print("─" * 60)
    print(f"  人员 (persons):     {len(persons)}")
    print(f"  机构 (orgs):        {len(organizations)}")
    print(f"  任职 (positions):   {len(positions)}")
    print(f"  关系 (edges):       {len(relationships)}")
    print(f"  JSON 文件:           {len(json_files)}")
    print()
    print("  说明:")
    print("    - 现任县委书记 = 孟庆鑫 (官方新闻确认, 2026-07)")
    print("    - 现任县长     = 邰瑞 (政府领导官网 confirm, 2025-10)")
    print("    - 政府领导班组成员姓名源自官网 bio 页")
    print("    - 出生/教育/履历等深度字段尚缺，需后续补充")
    print()
    print("=" * 60)
    print("  Build complete.")
    print("  → Validate: python3 -m py_compile build_肇州县_data.py")
    print("  → Promote:  python3 scripts/process_tmp.py data/tmp/heilongjiang_肇州县 --apply")
    print("=" * 60)


if __name__ == "__main__":
    main()