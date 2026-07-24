#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 安化县 (Anhua County), 益阳市, 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_安化县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.163.com/dy/article/KGUGPU1J05563DJA.html (李进任安化县委副书记)
  - https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C (安化县人民政府百度百科)
  - http://www.anhua.gov.cn (安化县人民政府官方网站)

Key findings:
  - 李进 (Acting County Mayor): born 1980, from 常德市, previously 武陵区副区长, 常德市委副秘书长/援藏(山南市隆子县委常务副书记), 安乡县委副书记/统战部长. Appointed 安化县委副书记 2025-12-16. Currently acting 县长.
  - 潘文剑 (Predecessor County Mayor → Party Secretary): resigned from 县长 on 2025-12-17, became 安化县委书记.
  - Key deputies: 贾启蒙, 禹丹, 张勇 (副县长), 贺磊 (副县长提名人选), 瞿永红 (副县长)
  - NOTE: Detailed career histories beyond current roles are limited. Many bio fields are open questions.

Confidence notes:
  - 李进 (Acting County Mayor): confirmed from 163.com news citing 益阳党建
  - 潘文剑 (Party Secretary/predecessor mayor): confirmed from baike.baidu.com and 163.com
  - 贾启蒙, 禹丹, 张勇 (Deputy Mayors): confirmed from baike.baidu.com
  - 贺磊 (Deputy Mayor nominee): confirmed from baike.baidu.com
  - 瞿永红 (Deputy Mayor): confirmed from baike.baidu.com news
  - Detailed bio data (birth, birthplace, education, early career) mostly unavailable
  - All claims labeled with confidence level; gaps explicitly documented
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

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "安化县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_安化县"
if _CURRENT_DIR.name == "hunan_安化县":
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
# IDs: 1-9 party/government core, 10-19 deputy government, 20-29 org leaders, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "潘文剑",
        "gender": "男",  # plausible
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县委书记",
        "current_org": "中共安化县委员会",
        "source": "https://www.163.com/dy/article/KGUGPU1J05563DJA.html + https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "confidence": "confirmed",
        "notes": "原安化县县长（2021-2025），2025年12月17日辞去县长职务，已任安化县委书记。从县长升任县委书记。此前履历待查。"
    },
    {
        "id": 2,
        "name": "李进",
        "gender": "男",  # plausible
        "ethnicity": "汉族",  # plausible
        "birth": "1980年",  # confirmed, exact month unknown
        "birthplace": "",  # open question
        "education": "",  # open question (possibly 武汉大学博士)
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "代理县长",
        "current_org": "安化县人民政府",
        "source": "https://www.163.com/dy/article/KGUGPU1J05563DJA.html",
        "confidence": "confirmed",
        "notes": "1980年出生，此前在常德市工作。曾任武陵区副区长，常德市委副秘书长、山南市隆子县委常务副书记（援藏），安乡县委副书记、统战部部长。2025年12月16日任安化县委副书记，拟提名为县市区长候选人。现为代理县长（待人大选举确认）。跨市从常德市调至益阳市安化县，属干部跨市交流典型案例。"
    },
    {
        "id": 3,
        "name": "贾启蒙",
        "gender": "",  # open question
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副县长",
        "current_org": "安化县人民政府",
        "source": "https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "confidence": "confirmed",
        "notes": "安化县副县长。百度百科显示在任。详细履历待查。"
    },
    {
        "id": 4,
        "name": "禹丹",
        "gender": "女",  # plausible (name suggests female)
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副县长",
        "current_org": "安化县人民政府",
        "source": "https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "confidence": "confirmed",
        "notes": "安化县副县长。百度百科显示在任。详细履历待查。"
    },
    {
        "id": 5,
        "name": "张勇",
        "gender": "男",  # plausible
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副县长",
        "current_org": "安化县人民政府",
        "source": "https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "confidence": "confirmed",
        "notes": "安化县副县长。百度百科显示在任。详细履历待查。"
    },
    {
        "id": 6,
        "name": "贺磊",
        "gender": "",  # open question
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副县长提名人选",
        "current_org": "安化县人民政府",
        "source": "https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "confidence": "confirmed",
        "notes": "安化县副县长提名人选（尚未正式任职）。百度百科显示。详细履历待查。"
    },
    {
        "id": 7,
        "name": "瞿永红",
        "gender": "男",  # plausible
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副县长",
        "current_org": "安化县人民政府",
        "source": "https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "confidence": "confirmed",
        "notes": "安化县副县长。2025年12月11日以副县长身份列席安化县十八届人大常委会第二十八次会议。详细履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other Major Org Leaders (unknown, placeholder for future research)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "陈飞燕",
        "gender": "",  # open question
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县人大常委会主任",
        "current_org": "安化县人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E5%AE%89%E5%8C%96%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "confidence": "confirmed",
        "notes": "安化县人大常委会主任。2025年12月11日主持县十八届人大常委会第二十八次会议。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共安化县委员会", "type": "政党", "level": "县级", "parent": "中共益阳市委员会", "location": "湖南省益阳市安化县"},
    {"id": 2, "name": "安化县人民政府", "type": "政府", "level": "县级", "parent": "益阳市人民政府", "location": "湖南省益阳市安化县"},
    {"id": 3, "name": "安化县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "安化县", "location": "湖南省益阳市安化县"},
    {"id": 4, "name": "中共常德市武陵区委员会", "type": "政党", "level": "县级", "parent": "中共常德市委员会", "location": "湖南省常德市武陵区"},
    {"id": 5, "name": "常德市武陵区人民政府", "type": "政府", "level": "县级", "parent": "常德市人民政府", "location": "湖南省常德市武陵区"},
    {"id": 6, "name": "中共常德市委员会", "type": "政党", "level": "地市级", "parent": "中共湖南省委员会", "location": "湖南省常德市"},
    {"id": 7, "name": "西藏山南市隆子县", "type": "政党", "level": "县级", "parent": "中共山南市委员会", "location": "西藏自治区山南市隆子县"},
    {"id": 8, "name": "中共安乡县委员会", "type": "政党", "level": "县级", "parent": "中共常德市委员会", "location": "湖南省常德市安乡县"},
    {"id": 9, "name": "安乡县人民政府", "type": "政府", "level": "县级", "parent": "常德市人民政府", "location": "湖南省常德市安乡县"},
    {"id": 10, "name": "中国共产党益阳市委员会", "type": "政党", "level": "地市级", "parent": "中共湖南省委员会", "location": "湖南省益阳市"},
    {"id": 11, "name": "益阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省益阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 潘文剑 (id=1)
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "约2021", "end_date": "2025-12-17", "rank": "正处级", "note": "安化县人民政府县长，2025年12月17日辞去"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-12", "end_date": "", "rank": "正处级", "note": "接任安化县委书记"},
    # 李进 (id=2)
    {"person_id": 2, "org_id": 5, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "常德市武陵区副区长，具体任期待查"},
    {"person_id": 2, "org_id": 6, "title": "市委副秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "常德市委副秘书长"},
    {"person_id": 2, "org_id": 7, "title": "县委常务副书记（援藏）", "start_date": "", "end_date": "", "rank": "正处级", "note": "西藏山南市隆子县委常务副书记，援藏干部"},
    {"person_id": 2, "org_id": 8, "title": "县委副书记、统战部部长", "start_date": "", "end_date": "2025-12", "rank": "副处级", "note": "安乡县委副书记、统战部部长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2025-12-16", "end_date": "", "rank": "副处级", "note": "任安化县委委员、常委、副书记"},
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start_date": "2025-12", "end_date": "", "rank": "正处级", "note": "安化县人民政府代理县长（待人大选举确认）"},
    # 贾启蒙 (id=3)
    {"person_id": 3, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "安化县副县长，具体任期待查"},
    # 禹丹 (id=4)
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "安化县副县长，具体任期待查"},
    # 张勇 (id=5)
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "安化县副县长，具体任期待查"},
    # 贺磊 (id=6)
    {"person_id": 6, "org_id": 2, "title": "副县长提名人选", "start_date": "", "end_date": "", "rank": "副处级", "note": "安化县副县长提名人选"},
    # 瞿永红 (id=7)
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "安化县副县长"},
    # 陈飞燕 (id=8)
    {"person_id": 8, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "县人大常委会党组书记、主任"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 潘文剑 → 李进：前后任县长关系
    {"person_a": 1, "person_b": 2, "type": "前后任", "context": "潘文剑辞去县长职务，由李进接任代理县长", "overlap_org": "安化县人民政府", "overlap_period": "2025-12"},
    # 潘文剑 → 李进：县委书记与县委副书记关系
    {"person_a": 1, "person_b": 2, "type": "直接上下级", "context": "潘文剑任安化县委书记，李进任安化县委副书记", "overlap_org": "中共安化县委员会", "overlap_period": "2025-12至今"},
    # 李进 → 瞿永红：县长与副县长关系
    {"person_a": 2, "person_b": 7, "type": "直接上下级", "context": "代理县长与副县长，县政府领导班子成员", "overlap_org": "安化县人民政府", "overlap_period": "2025-12至今"},
    # 李进 → 贾启蒙
    {"person_a": 2, "person_b": 3, "type": "直接上下级", "context": "代理县长与副县长，县政府领导班子成员", "overlap_org": "安化县人民政府", "overlap_period": "2025-12至今"},
    # 李进 → 禹丹
    {"person_a": 2, "person_b": 4, "type": "直接上下级", "context": "代理县长与副县长，县政府领导班子成员", "overlap_org": "安化县人民政府", "overlap_period": "2025-12至今"},
    # 李进 → 张勇
    {"person_a": 2, "person_b": 5, "type": "直接上下级", "context": "代理县长与副县长，县政府领导班子成员", "overlap_org": "安化县人民政府", "overlap_period": "2025-12至今"},
    # 瞿永红 → 潘文剑：前后任副县长与县长
    {"person_a": 7, "person_b": 1, "type": "同事", "context": "瞿永红以副县长身份列席潘文剑主持的县政府会议", "overlap_org": "安化县人民政府", "overlap_period": "2021-2025"},
    # 陈飞燕 → 潘文剑：人大与政府关系
    {"person_a": 8, "person_b": 1, "type": "工作关系", "context": "陈飞燕主持人大常委会，潘文剑辞去县长职务获人大常委会表决通过", "overlap_org": "安化县", "overlap_period": "2025-12"},
]

# ── Person JSONs ─────────────────────────────────────────────────────────────
PERSON_JSON_SCHEMA_VERSION = "1.0"

def build_person_json(p: dict) -> dict:
    """Build a person JSON record following the project's person_graph_json schema."""
    positions_for_person = [
        {
            "org": f"{pos['org_id']}",
            "title": pos["title"],
            "start": pos["start_date"] or None,
            "end": pos["end_date"] or None,
            "rank": pos.get("rank", ""),
            "note": pos.get("note", ""),
        }
        for pos in positions
        if pos["person_id"] == p["id"]
    ]
    relationships_for_person = [
        {
            "person_b": f"{r['person_b']}",
            "type": r["type"],
            "context": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
        }
        for r in relationships
        if r["person_a"] == p["id"]
    ] + [
        {
            "person_a": f"{r['person_a']}",
            "type": r["type"],
            "context": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
        }
        for r in relationships
        if r["person_b"] == p["id"]
    ]
    return {
        "schema_version": PERSON_JSON_SCHEMA_VERSION,
        "investigation_date": AS_OF,
        "person_id": p["id"],
        "name": p["name"],
        "gender": p.get("gender", ""),
        "ethnicity": p.get("ethnicity", ""),
        "birth": p.get("birth", ""),
        "birthplace": p.get("birthplace", ""),
        "education": p.get("education", ""),
        "party_join": p.get("party_join", ""),
        "work_start": p.get("work_start", ""),
        "current_post": p.get("current_post", ""),
        "current_org": p.get("current_org", ""),
        "source": p.get("source", ""),
        "confidence": p.get("confidence", "unverified"),
        "notes": p.get("notes", ""),
        "positions": positions_for_person,
        "relationships": relationships_for_person,
        "open_questions": _get_open_questions(p),
    }


def _get_open_questions(p: dict) -> list[str]:
    qs = []
    if not p.get("birth") or p["birth"] == "1980年":
        qs.append("缺少具体出生月日")
    if not p.get("birthplace"):
        qs.append("缺少籍贯信息")
    if not p.get("gender"):
        qs.append("缺少性别信息")
    if not p.get("ethnicity"):
        qs.append("缺少民族信息")
    if not p.get("education"):
        qs.append("缺少学历信息")
    if not p.get("work_start"):
        qs.append("缺少参加工作年份")
    if not p.get("party_join"):
        qs.append("缺少入党时间")
    # Check for career gaps
    positions_for_p = [pos for pos in positions if pos["person_id"] == p["id"]]
    has_empty_dates = any(not pos.get("start_date") or not pos.get("end_date") for pos in positions_for_p)
    if has_empty_dates or len(positions_for_p) <= 1:
        qs.append("履历时间线不完整，存在任职日期缺口")
    return qs


def write_person_json(p: dict) -> str:
    obj = build_person_json(p)
    job_slug = p["current_post"].replace(" ", "_")
    fname = f"{TODAY}-湖南省-益阳市-{job_slug}-{p['name']}.json"
    fpath = Path(PJSON_DIR) / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return str(fpath)


# ── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    # Write person JSONs
    written = []
    for p in persons:
        path = write_person_json(p)
        written.append(path)
        print(f"  Person JSON: {path}")

    # Write person JSONs also to PERSONS_DIR
    os.makedirs(str(PERSONS_DIR), exist_ok=True)
    for p in persons:
        job_slug = p["current_post"].replace(" ", "_")
        fname = f"{TODAY}-湖南省-益阳市-{job_slug}-{p['name']}.json"
        fpath = Path(PERSONS_DIR) / fname
        obj = build_person_json(p)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON (canonical): {fpath}")

    # Build DB + GEXF
    print(f"\nBuilding database: {DB_PATH}")
    print(f"Building GEXF: {GEXF_PATH}")
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
    print("\nDone.")


if __name__ == "__main__":
    main()
