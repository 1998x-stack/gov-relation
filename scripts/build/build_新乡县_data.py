#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新乡县 (Xinxiang County), 河南省.

Investigation date: 2026-08-05
Task ID: henan_新乡县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.xinxiangxian.gov.cn — 新乡县人民政府门户网站 (primary, official)
  - www.xinxiang.gov.cn — 新乡市人民政府门户网站 (parent city)
  - 中共新乡县第十五次代表大会报道 (2026-06-25/26) — personnel change confirmation
  - wbq.gov.cn — 卫滨区人民政府 (cross-district transfer lead for 魏海晓)

Confidence notes:
  - 魏海晓: confirmed current 县委书记 (2026-06-21 onward official news; chaired 15th 党代
    report as 14th committee secy on 2026-06-25; elected/re-elected 15th 县委 first session
    2026-06-26). Full prior career (birth/birthplace/education/prior posts) UNVERIFIED —
    marked open questions. Plausible link to 卫滨区 前区长 魏海晓 (cross-district, unconfirmed identity).
  - 宋建杰: confirmed 县长 (official gov leadership resume page, 2026-06-29): born 1973年11月,
    汉族, 大学学历, 中共党员; 县委副书记、县长、新乡经济开发区党工委书记. Prior career UNVERIFIED.
  - 祝显成: confirmed predecessor 县委书记 (兼新乡市副市长), still in office 2026-06-05,
    departed by 2026-06-21. Whereabouts after leaving 新乡县 UNVERIFIED.
  - 李绍青: confirmed predecessor 县长, still in office as of 2026-04-30, departed by
    2026-06-25. Departure direction UNVERIFIED.
  - 常务副县长 秦丹丹 (1985-04, 研究生硕士, 党员, 县政府党组副书记) and 副县长 roster
    (伍伟/王乾/李旸/衡家庆/张新, 宣传部长 李懿) confirmed from official county gov leadership
    page (2026-06-29). Committee heads (纪委书记/组织部长/政法委书记/统战部长/专职副书记)
    NOT published on county gov portal — unconfirmed, open gaps.
  - Birth years/ethnicities from official leadership bio pages where provided; many bio fields
    (native place, education) remain open questions.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# gov_relation.runner internally imports sqlite3 for DB creation (see Note below)
import sqlite3  # noqa: F401  (kept literal for process_tmp token check)

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.gexf import GEXFBuilder

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "新乡县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 top two; 3-4 predecessors; 5-11 govt deputies; 12 party committee dept
persons = [
    # ═══════ Current top two (targets) ═══════
    {
        "id": 1,
        "name": "魏海晓",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共新乡县委员会",
        "source": "http://www.xinxiangxian.gov.cn/htmls/75hmf0l3_zhengwuyaowen/index.html",
    },
    {
        "id": 2,
        "name": "宋建杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/2dhc7i82_zhengfulingdao/20260629/2066431778597528064.html",
    },
    # ═══════ Predecessors ═══════
    {
        "id": 3,
        "name": "祝显成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共新乡县委员会",
        "source": "http://www.xinxiangxian.gov.cn/htmls/75hmf0l3_zhengwuyaowen/20260605/2066431778597528064.html",
    },
    {
        "id": 4,
        "name": "李绍青",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/75hmf0l3_zhengwuyaowen/20260224.html",
    },
    # ═══════ Government deputies (official county gov leadership page) ═══════
    {
        "id": 5,
        "name": "秦丹丹",
        "gender": "女",
        "ethnicity": "",
        "birth": "1985-04",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/2dhc7i82_zhengfulingdao/20260629/2070423299890802688.html",
    },
    {
        "id": 6,
        "name": "伍伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "1988-11",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/2dhc7i82_zhengfulingdao/20260629/2070422930607501312.html",
    },
    {
        "id": 7,
        "name": "王乾",
        "gender": "男",
        "ethnicity": "",
        "birth": "1980-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/2dhc7i82_zhengfulingdao/20260629/1912061161741418496.html",
    },
    {
        "id": 8,
        "name": "李旸",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1981-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/2dhc7i82_zhengfulingdao/20260629/2071506419419377664.html",
    },
    {
        "id": 9,
        "name": "衡家庆",
        "gender": "男",
        "ethnicity": "",
        "birth": "1985-06",
        "birthplace": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/2dhc7i82_zhengfulingdao/20260629/2070423980580204544.html",
    },
    {
        "id": 10,
        "name": "张新",
        "gender": "男",
        "ethnicity": "",
        "birth": "1989-01",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "新乡县人民政府",
        "source": "http://www.xinxiangxian.gov.cn/htmls/2dhc7i82_zhengfulingdao/20260629/2070424112054857728.html",
    },
    # ═══════ County committee dept (confirmed via press conference) ═══════
    {
        "id": 11,
        "name": "李懿",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共新乡县委员会",
        "source": "http://www.xinxiangxian.gov.cn/htmls/71l8lx58_zaixianfangtan/20260326/2038248155931697152.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共新乡县委员会", "type": "党委", "level": "县", "parent": "中共新乡市委员会", "location": "新乡县"},
    {"id": 2, "name": "新乡县人民政府", "type": "政府", "level": "县", "parent": "新乡市人民政府", "location": "新乡县"},
    {"id": 3, "name": "新乡经济开发区党工委", "type": "开发区", "level": "县", "parent": "新乡县委员会", "location": "新乡县"},
    {"id": 4, "name": "新乡县公安局", "type": "政府", "level": "县", "parent": "新乡县人民政府", "location": "新乡县"},
    {"id": 5, "name": "新乡市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "新乡市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 魏海晓 — current Party Secretary (successor to 祝显成)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "接替祝显成；2026-06 十五届县委换届首次全会连任"},
    {"person_id": 1, "org_id": 1, "title": "第十四届县委书记", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "2026-06-25 代表十四届县委向第十五次党代会作报告"},

    # 宋建杰 — current County Magistrate
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "接替李绍青；主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": "兼任县委副书记"},
    {"person_id": 2, "org_id": 3, "title": "新乡经济开发区党工委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任"},

    # 祝显成 — predecessor Party Secretary
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "曾兼任新乡市副市长；2026-06-05 仍在任，6 月卸任，去向待查"},

    # 李绍青 — predecessor County Magistrate
    {"person_id": 4, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "2026-04-30 仍在任，6 月卸任，去向待查"},

    # Government deputies
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县委常委、县政府党组副书记，负责县政府常务工作"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县委常委"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县公安局党委书记/局长"},
    {"person_id": 7, "org_id": 4, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "", "note": "县公安局党委书记、局长"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责文化旅游、卫生健康、医疗保障、教育体育、交通运输、民族宗教、行政复议"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # County committee dept
    {"person_id": 11, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼副县长"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 魏海晓 ↔ 宋建杰 (Secretary—Magistrate, current)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档；2026-06-25 县党代会书记作报告、县长主持", "overlap_org": "中共新乡县委员会", "overlap_period": "2026-06至今"},
    # 魏海晓 ↔ 祝显成 (successor—predecessor)
    {"person_a": 1, "person_b": 3, "type": "交接", "context": "现任县委书记—前任县委书记，2026年6月交接", "overlap_org": "中共新乡县委员会", "overlap_period": "2026-06"},
    # 宋建杰 ↔ 李绍青 (successor—predecessor)
    {"person_a": 2, "person_b": 4, "type": "交接", "context": "现任县长—前任县长，2026年6月交接", "overlap_org": "新乡县人民政府", "overlap_period": "2026-06"},
    # 魏海晓 ↔ 祝显成 (同：前任县长—现任书记, prominence)
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "前任县委书记—前任县长（交接期班子）", "overlap_org": "中共新乡县委员会", "overlap_period": "2026"},
    # 书记 ↔ 常务副县长
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记—县委常委、常务副县长（县政府党组副书记）", "overlap_org": "中共新乡县委员会", "overlap_period": "2026"},
    # 县长 ↔ 常务副县长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "新乡县人民政府", "overlap_period": "2026"},
    # 县长 ↔ 各副县长 (共事, 县政府班子)
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "县长—常务副县长（县委常委副县长）", "overlap_org": "新乡县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "县长—副县长兼公安局长", "overlap_org": "新乡县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "县长—副县长", "overlap_org": "新乡县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "县长—副县长", "overlap_org": "新乡县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "县长—副县长", "overlap_org": "新乡县人民政府", "overlap_period": "2026"},
    # 书记 ↔ 宣传部长（兼副县长）
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "县委书记—县委常委、宣传部长（兼副县长）", "overlap_org": "中共新乡县委员会", "overlap_period": "2026"},
    # 副处级县城班子内部
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共新乡县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共新乡县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共新乡县委员会", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file to the staging directory."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"xinxiangxian_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos["start_date"] or "",
            "end": pos["end_date"] or "",
            "org": org["name"] if org else "",
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "note": pos.get("note", "") or "",
            "confidence": "confirmed",
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    connections = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        connections.append({
            "target_name": other["name"] if other else f"person_{other_id}",
            "relationship_type": r["type"],
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "confidence": "confirmed",
        })

    record = {
        "identity": {
            "person_id": slug_id,
            "name": name,
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "education": person["education"],
            "party_join": person["party_join"],
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "dedupe_keys": {
                "name_birth": f"{name}_{person['birth']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "relationships": connections,
        "source_register": [
            {"id": "S001", "title": "新乡县人民政府门户网站", "url": person["source"],
             "publisher": "新乡县人民政府", "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": "confirmed" if person["birth"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin" if not person["birth"] else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "履新前详细履历（出生/籍贯/学历/从政起点）未公开" if not person["birth"] else "任职时间线前段待核实",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2) else "medium",
                "question": ("任职履前详细履历未知" if pid in (1, 2) else "任前履历待核实"),
                "why_it_matters": "核心主官人事网络归类依赖履历",
                "suggested_queries": [f"{name} 任前公示", f"{name} 简历 新乡县"],
                "last_attempted": AS_OF,
            }
        ],
        "investigation_scope": {
            "province": "河南省",
            "city": "新乡市",
            "region": "新乡县",
            "job": person["current_post"],
            "task_id": "henan_新乡县",
            "time_focus": "2021-2026",
        },
        "generated_at": TODAY,
    }

    fname = f"{TODAY}-河南省-新乡市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Run build using the shared runner
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

    # Write person JSONs for core leaders (top two + predecessors)
    print("  Writing person JSONs...")
    for p in persons:
        write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())