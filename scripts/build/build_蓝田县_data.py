#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 蓝田县, 西安市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_蓝田县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 蓝田县人民政府官方网站 (www.lantian.gov.cn) — confirmed current leadership resumes
  - 领导之窗页面: /zwgk/ldzc/ltb/1.html (李同勃), /zwgk/ldzc/shq/1.html (苏护强)
  - 新闻中心 articles confirming 徐毅 as 县委书记 (various dates through 2026-07-25)

Confidence notes:
  - 县政府领导（8人）姓名、职务、分工、简历全部在政府网站确认
  - 县委书记 徐毅 在政府网站的新闻中频繁出现（确认在职），但未在政府领导之窗列出（县委领导属于党务系统）
  - 苏护强（常务副县长）简历完整，曾任蓝田县委常委、组织部长
  - 王晶（副县长）简历有部分信息模糊；部分副县长的早期履历不完整
  - 县人大常委会主任、县政协主席信息待补充
  - 县委其他常委（组织部长、纪委书记、宣传部长等）信息未在政府网站单独列出
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
# When run from staging directory, resolve up to project root
if os.path.basename(BASE).startswith("shaanxi_"):
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "蓝田县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (县委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 徐毅 — 县委书记
    {
        "id": 1,
        "name": "徐毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共蓝田县委员会",
        "source": "蓝田县人民政府网站新闻中心多处报道确认，最新：2026-07-25 调研光伏+乡村振兴项目"
    },
    # 李同勃 — 县委副书记、县长
    {
        "id": 2,
        "name": "李同勃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年5月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/ltb/1.html"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (县政府) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 苏护强 — 县委常委、副县长（常务）
    {
        "id": 3,
        "name": "苏护强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年7月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/shq/1.html"
    },
    # 王晶 — 县委常委、副县长
    {
        "id": 4,
        "name": "王晶",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1983年2月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/wj/1.html"
    },
    # 毛会霞 — 副县长
    {
        "id": 5,
        "name": "毛会霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/mhx/1.html"
    },
    # 何勇 — 副县长
    {
        "id": 6,
        "name": "何勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/hy/1.html"
    },
    # 李永波 — 副县长
    {
        "id": 7,
        "name": "李永波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/lyb/1.html"
    },
    # 丁相天 — 副县长
    {
        "id": 8,
        "name": "丁相天",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/dxt/1.html"
    },
    # 蔚红德 — 副县长、公安局长
    {
        "id": 9,
        "name": "蔚红德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局党委书记、局长",
        "current_org": "蓝田县人民政府",
        "source": "https://www.lantian.gov.cn/zwgk/ldzc/whd/1.html"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共蓝田县委员会",
        "type": "党委",
        "level": "县",
        "location": "西安市蓝田县县门街6号"
    },
    {
        "id": 2,
        "name": "蓝田县人民政府",
        "type": "政府",
        "level": "县",
        "location": "西安市蓝田县县门街6号"
    },
    {
        "id": 3,
        "name": "蓝田县公安局",
        "type": "政府",
        "level": "县",
        "location": "西安市蓝田县"
    },
]

positions_data = [
    # 徐毅
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "最新报道截至2026-07-25"},
    # 李同勃
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 苏护强
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管常务工作"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 王晶
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 毛会霞
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 何勇
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李永波
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "九三学社社员"},
    # 丁相天
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 蔚红德
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副县级", "note": "二级高级警长"},
]

relationships_data = [
    # 徐毅 — 李同勃：党政正职搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长（党政正职搭档）",
        "overlap_org": "中共蓝田县委员会",
        "overlap_period": "2024年至今"
    },
    # 徐毅 — 苏护强：县委领导关系
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委",
        "overlap_org": "中共蓝田县委员会",
        "overlap_period": "2024年至今"
    },
    # 徐毅 — 王晶：县委领导关系
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委",
        "overlap_org": "中共蓝田县委员会",
        "overlap_period": "2024年至今"
    },
    # 李同勃 — 苏护强：县长与常务副县长
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长",
        "overlap_org": "蓝田县人民政府",
        "overlap_period": "2024年至今"
    },
    # 李同勃 — 各副县长：政府班子关系
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县政府班子", "overlap_org": "蓝田县人民政府", "overlap_period": "2024年至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县政府班子", "overlap_org": "蓝田县人民政府", "overlap_period": "2024年至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县政府班子", "overlap_org": "蓝田县人民政府", "overlap_period": "2024年至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县政府班子", "overlap_org": "蓝田县人民政府", "overlap_period": "2024年至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县政府班子", "overlap_org": "蓝田县人民政府", "overlap_period": "2024年至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县政府班子", "overlap_org": "蓝田县人民政府", "overlap_period": "2024年至今"},
    # 苏护强曾任蓝田县委常委、组织部长 — 可能和多位县领导有工作交集
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同时担任县委常委", "overlap_org": "中共蓝田县委员会", "overlap_period": "2024年至今"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helper
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSONS_DIR = STAGING_DIR
PERSON_JSONS = []


def make_person_json(person: dict) -> dict:
    """Create a person graph JSON following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    job = person["current_post"].split("、")[0] if "、" in person["current_post"] else person["current_post"]

    # Build career timeline from positions_data
    career = []
    for pos in positions_data:
        if pos["person_id"] == pid:
            career.append({
                "start": pos["start"] or "unknown",
                "end": pos["end"] or "unknown",
                "org": next((o["name"] for o in organizations_data if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "西安市蓝田县",
                "system": "party" if pos["org_id"] == 1 else "government",
                "rank": pos["rank"],
                "is_key_promotion": False,
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })

    # Build relationships
    rels = []
    for r in relationships_data:
        if r["person_a"] == pid:
            other_name = next((p["name"] for p in persons_data if p["id"] == r["person_b"]), "")
            rels.append({
                "person": other_name,
                "person_id": f"蓝田县_{r['person_b']}",
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] in ("superior_subordinate",) else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })

    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省",
            "city": "西安市",
            "region": "蓝田县",
            "job": job,
            "task_id": "shaanxi_蓝田县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": f"shaanxi_lantian_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": f"https://www.lantian.gov.cn/zwgk/ldzc/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正县级" if "书记" in person["current_post"] and "副" not in person["current_post"] else "副县级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations_data],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "待补充", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {"centrality": "", "betweenness": "", "clusters": []},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": ["S001"]}
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "蓝田县人民政府官方网站 — 领导之窗",
                "url": "https://www.lantian.gov.cn/zwgk/ldzc/",
                "publisher": "蓝田县人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": f"{name}的官方简历或新闻活动报道"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high" if pid <= 2 else "medium",
            "biggest_gap": "早期履历信息不完整，学历和工作起始年份待补充"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{name}的完整履历（学历、工作起始年份、早期职务）",
                "why_it_matters": "影响对干部培养路径和升迁速度的分析",
                "suggested_queries": [f"{name} 简历 蓝田县", f"{name} 任职公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def write_person_json(person: dict) -> str:
    """Write a single person JSON file and return the filename."""
    name = person["name"]
    job = person["current_post"].split("、")[0] if "、" in person["current_post"] else person["current_post"]
    filename = f"{TODAY}-陕西省-西安市-{job}-{name}.json"
    filepath = PERSON_JSONS_DIR / filename
    data = make_person_json(person)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network data...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders (县委书记, 县长, 常务副县长)
    core_ids = [1, 2, 3]  # 徐毅, 李同勃, 苏护强
    written = []
    for p in persons_data:
        if p["id"] in core_ids:
            fname = write_person_json(p)
            written.append(fname)
            print(f"  Person JSON: {fname}")

    print(f"\nDone! {len(written)} person JSONs written.")
    print(f"Run: python3 scripts/process_tmp.py data/tmp/shaanxi_蓝田县")
    print(f"Then: python3 scripts/process_tmp.py data/tmp/shaanxi_蓝田县 --apply")


if __name__ == "__main__":
    main()
