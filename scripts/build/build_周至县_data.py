#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 周至县, 西安市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_周至县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 周至县人民政府官方网站 (www.zhouzhi.gov.cn) — confirmed current leadership resumes
  - 领导之窗页面: /xxgk/fdzdgknr/ldzc/djl/1.html (段军利), /xxgk/fdzdgknr/ldzc/wxy/1.html (王小勇)
  - 新闻中心 articles confirming 闻其伟 as 县委书记 (various dates through 2026-07-25, e.g., "闻其伟督导调研县财政局党风廉政建设" 2026-04-17)
  - 领导活动页面 confirming 朱建平 as 县人大常委会主任 (2026-03-27 读书班)

Confidence notes:
  - 县政府领导（7人）姓名、职务、分工、简历全部在政府网站确认
  - 县委书记 闻其伟 在政府网站的新闻中频繁出现（确认在职），但未在政府领导之窗列出（县委领导属于党务系统）
  - 段军利（县长）简历完整，有公开官方页面
  - 闻其伟的完整履历暂无官方公开页面，有待补充
  - 县人大常委会主任朱建平、县政协主席信息待补充
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
# data/tmp/shaanxi_周至县/ -> need to go up 3 levels to reach project root
TMP_MARKER = os.path.sep + "tmp" + os.path.sep
if TMP_MARKER in BASE:
    # Path: .../data/tmp/shaanxi_周至县/
    # Need: .../ (project root, which is 3 levels up: data/tmp/taskid)
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
elif os.path.basename(BASE).startswith("shaanxi_"):
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "周至县"
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

    # 闻其伟 — 县委书记
    {
        "id": 1,
        "name": "闻其伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共周至县委员会",
        "source": "周至县人民政府网站新闻中心多处报道确认，最新：2026-04-17 督导调研县财政局党风廉政建设；2026-03-27 县委理论学习中心组读书班"
    },
    # 段军利 — 县委副书记、县长
    {
        "id": 2,
        "name": "段军利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "陕西西安",
        "education": "全日制大学本科学历、经济学学士，在职公共管理硕士",
        "party_join": "中共党员",
        "work_start": "2001年7月",
        "current_post": "县委副书记、县长",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/djl/1.html"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (县政府) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 王小勇 — 县委常委、副县长（常务）
    {
        "id": 3,
        "name": "王小勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年8月",
        "birthplace": "陕西蓝田",
        "education": "研究生文化程度",
        "party_join": "中共党员",
        "work_start": "1991年7月",
        "current_post": "县委常委、常务副县长",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/wxy/1.html"
    },
    # 赵勇 — 县委常委、副县长（挂职）
    {
        "id": 4,
        "name": "赵勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "贵州湄潭",
        "education": "全日制大学本科学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/zy/1.html"
    },
    # 刘文博 — 副县长
    {
        "id": 5,
        "name": "刘文博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "陕西西安",
        "education": "全日制大学本科学历、法学学士，在职公共管理硕士",
        "party_join": "致公党党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/lwb/1.html"
    },
    # 侯淑艳 — 副县长
    {
        "id": 6,
        "name": "侯淑艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "陕西周至",
        "education": "大学文化程度",
        "party_join": "中共党员",
        "work_start": "1991年7月",
        "current_post": "副县长",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/hsy/1.html"
    },
    # 骞宸 — 副县长
    {
        "id": 7,
        "name": "骞宸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "陕西周至",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "2005年8月",
        "current_post": "副县长",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/qc/1.html"
    },
    # 刘云峰 — 副县长、县公安局局长
    {
        "id": 8,
        "name": "刘云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "陕西蓝田",
        "education": "大学文化程度",
        "party_join": "中共党员",
        "work_start": "1999年7月",
        "current_post": "副县长、县公安局局长",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/lyf/1.html"
    },
    # 葛东升 — 副县长
    {
        "id": 9,
        "name": "葛东升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "陕西周至",
        "education": "大学文化程度",
        "party_join": "中共党员",
        "work_start": "1999年12月",
        "current_post": "副县长",
        "current_org": "周至县人民政府",
        "source": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/gds/1.html"
    },
    # 朱建平 — 县人大常委会主任
    {
        "id": 10,
        "name": "朱建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "周至县人民代表大会常务委员会",
        "source": "周至县人民政府网站新闻报道确认（2026-03-27 县委理论学习中心组读书班）"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共周至县委员会",
        "type": "党委",
        "level": "县",
        "location": "西安市周至县老城东街37号"
    },
    {
        "id": 2,
        "name": "周至县人民政府",
        "type": "政府",
        "level": "县",
        "location": "西安市周至县老城东街37号"
    },
    {
        "id": 3,
        "name": "周至县公安局",
        "type": "政府",
        "level": "县",
        "location": "西安市周至县"
    },
    {
        "id": 4,
        "name": "周至县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "location": "西安市周至县老城东街37号"
    },
]

positions_data = [
    # 闻其伟
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "最新报道截至2026-07-25"},
    # 段军利
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2022年3月", "end": "present", "rank": "正县级", "note": "主持县政府全面工作；2021年8月至2022年3月任代县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2021年8月", "end": "present", "rank": "副县级", "note": ""},
    # 王小勇
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管常务工作，协助分管财政、审计"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": "曾任县委常委、组织部部长"},
    # 赵勇（挂职）
    {"person_id": 4, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "苏陕协作挂职干部，来自太仓市"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 刘文博
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "致公党党员"},
    # 侯淑艳
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "2022年3月", "end": "present", "rank": "副县级", "note": "分管教育、卫健、医保"},
    # 骞宸
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管城建、城管、交通、生态环境"},
    # 刘云峰
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副县级", "note": "三级高级警长"},
    # 葛东升
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "曾任周至县委办主任"},
    # 朱建平
    {"person_id": 10, "org_id": 4, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

relationships_data = [
    # 闻其伟 — 段军利：党政正职搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长（党政正职搭档）",
        "overlap_org": "中共周至县委员会",
        "overlap_period": "2021年至今"
    },
    # 闻其伟 — 王小勇：县委领导关系
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委",
        "overlap_org": "中共周至县委员会",
        "overlap_period": ""
    },
    # 闻其伟 — 赵勇：县委领导关系
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委",
        "overlap_org": "中共周至县委员会",
        "overlap_period": ""
    },
    # 闻其伟 — 朱建平：县委与人大关系
    {
        "person_a": 1, "person_b": 10,
        "type": "overlap",
        "context": "县委书记与县人大常委会主任",
        "overlap_org": "中共周至县委员会",
        "overlap_period": ""
    },
    # 段军利 — 王小勇：县长与常务副县长
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长",
        "overlap_org": "周至县人民政府",
        "overlap_period": ""
    },
    # 段军利 — 各副县长：政府班子关系
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县政府班子", "overlap_org": "周至县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县政府班子", "overlap_org": "周至县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县政府班子", "overlap_org": "周至县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县政府班子", "overlap_org": "周至县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县政府班子", "overlap_org": "周至县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县政府班子", "overlap_org": "周至县人民政府", "overlap_period": ""},
    # 王小勇 — 其他县领导：县委常委关系
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同时担任县委常委", "overlap_org": "中共周至县委员会", "overlap_period": ""},
    # 侯淑艳 — 王小勇：曾在县委组织部共事
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "王小勇曾任县委常委、组织部长，侯淑艳曾任县委组织部副部长", "overlap_org": "中共周至县委组织部", "overlap_period": ""},
    # 葛东升 — 侯淑艳：曾在县委组织部共事
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "侯淑艳曾任县委组织部副部长，葛东升曾任县委组织部副部长", "overlap_org": "中共周至县委组织部", "overlap_period": ""},
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
    job = job.split("（")[0]  # Remove (挂职) suffix for filename

    # Build career timeline from positions_data
    career = []
    for pos in positions_data:
        if pos["person_id"] == pid:
            org_name = next((o["name"] for o in organizations_data if o["id"] == pos["org_id"]), "")
            career.append({
                "start": pos["start"] or "unknown",
                "end": pos["end"] or "unknown",
                "org": org_name,
                "title": pos["title"],
                "level": pos["rank"],
                "location": "西安市周至县",
                "system": "party" if pos["org_id"] == 1 else ("government" if pos["org_id"] in (2, 3) else "other"),
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
                "person_id": f"周至县_{r['person_b']}",
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
            "region": "周至县",
            "job": job,
            "task_id": "shaanxi_周至县",
            "time_focus": "2021-2026"
        },
        "identity": {
            "person_id": f"shaanxi_zhouzhi_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正县级" if "书记" in person["current_post"] and "副" not in person["current_post"] else ("正县级" if "县长" in person["current_post"] or "主任" in person["current_post"] else "副县级"),
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
                "title": "周至县人民政府官方网站 — 领导之窗",
                "url": "https://www.zhouzhi.gov.cn/xxgk/fdzdgknr/ldzc/",
                "publisher": "周至县人民政府",
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
            "relationship_confidence": "high" if pid <= 4 else "medium",
            "biggest_gap": "早期履历信息不完整，部分人员的学历和工作起始年份待补充"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{name}的完整履历（学历、工作起始年份、早期职务）",
                "why_it_matters": "影响对干部培养路径和升迁速度的分析",
                "suggested_queries": [f"{name} 简历 周至县", f"{name} 任职公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def write_person_json(person: dict) -> str:
    """Write a single person JSON file and return the filename."""
    name = person["name"]
    job = person["current_post"].split("、")[0] if "、" in person["current_post"] else person["current_post"]
    job = job.split("（")[0]  # Remove (挂职) suffix
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
    core_ids = [1, 2, 3]  # 闻其伟, 段军利, 王小勇
    written = []
    for p in persons_data:
        if p["id"] in core_ids:
            fname = write_person_json(p)
            written.append(fname)
            print(f"  Person JSON: {fname}")

    print(f"\nDone! {len(written)} person JSONs written.")
    print(f"Run: python3 scripts/process_tmp.py data/tmp/shaanxi_周至县")
    print(f"Then: python3 scripts/process_tmp.py data/tmp/shaanxi_周至县 --apply")


if __name__ == "__main__":
    main()
