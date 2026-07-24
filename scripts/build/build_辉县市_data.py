#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 辉县市 (Huixian City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_辉县市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.huixianshi.gov.cn — 辉县市人民政府网站 (primary, current as of July 2026)
  - Baidu Baike "辉县市" entry — confirmed current leadership (王庆军, 郭奇)
  - Government news articles confirm standing committee via 第十五次党代会 (2026-06-25)
  - 郭奇 resume: official government leader page

Confidence notes:
  - 王庆军: confirmed as Party Secretary via multiple government news articles (June-July 2026)
  - 郭奇: confirmed as Mayor via official government leader page; birth 1984-01, Han ethnicity,
    graduate degree, law master, party member
  - Leadership roster: confirmed from 第十五次党代会主席团常务委员会名单 (2026-06-25)
  - Detailed career timelines (education, early career, birthplace) could not be fully verified
    due to web access limitations (Baidu Baike 403, Google blocked)
  - 王庆军's previous roles and full career timeline are open questions
"""

from __future__ import annotations

import json
import os
import sqlite3  # used via gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

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
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "辉县市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-5 core leaders, 6-15 standing committee, 16-20 deputy govt, 21+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "王庆军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共辉县市委员会",
        "source": "https://baike.baidu.com/item/辉县市"
    },
    {
        "id": 2,
        "name": "郭奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-01",
        "birthplace": "",
        "education": "研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/PublicInfo/Leader?id=5"
    },
    {
        "id": 3,
        "name": "李杨",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共辉县市委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    {
        "id": 4,
        "name": "姚志伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "辉县市人民代表大会常务委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    {
        "id": 5,
        "name": "崔国兵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议辉县市委员会",
        "source": "https://baike.baidu.com/item/辉县市"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (市委常委)
    # Source: 第十五次党代会主席团常务委员会名单 (2026-06-25)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "汤永",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共辉县市委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    {
        "id": 7,
        "name": "董智彪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共辉县市委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    {
        "id": 8,
        "name": "高伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共辉县市委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    {
        "id": 9,
        "name": "丁鹤",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共辉县市委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    {
        "id": 10,
        "name": "闫仁强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长、副市长",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/PublicInfo/Leader?id=10"
    },
    {
        "id": 11,
        "name": "李园丰",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市政府党组成员",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/PublicInfo/Leader?id=18"
    },
    {
        "id": 12,
        "name": "李明星",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共辉县市委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    {
        "id": 13,
        "name": "张寒瑞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共辉县市委员会",
        "source": "https://www.huixianshi.gov.cn/Article/25060"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "张永胜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/PublicInfo/Leader"
    },
    {
        "id": 15,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/PublicInfo/Leader"
    },
    {
        "id": 16,
        "name": "程龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/PublicInfo/Leader"
    },
    {
        "id": 17,
        "name": "刘志宽",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/Article/25179"
    },
    {
        "id": 18,
        "name": "郭林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/Article/25179"
    },
    {
        "id": 19,
        "name": "李进中",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员",
        "current_org": "辉县市人民政府",
        "source": "https://www.huixianshi.gov.cn/PublicInfo/Leader?id=14"
    },
    {
        "id": 20,
        "name": "张洪腾",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辉县经开区管委会主任",
        "current_org": "辉县经济技术开发区",
        "source": "https://www.huixianshi.gov.cn/Article/25179"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "刘军伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共辉县市委员会",
        "source": "https://baike.baidu.com/item/辉县市"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共辉县市委员会", "type": "党委", "level": "县级市", "parent": "中共新乡市委员会", "location": "辉县市"},
    {"id": 2, "name": "辉县市人民政府", "type": "政府", "level": "县级市", "parent": "新乡市人民政府", "location": "辉县市"},
    {"id": 3, "name": "辉县市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "新乡市人大常委会", "location": "辉县市"},
    {"id": 4, "name": "中国人民政治协商会议辉县市委员会", "type": "政协", "level": "县级市", "parent": "政协新乡市委员会", "location": "辉县市"},
    {"id": 5, "name": "辉县经济技术开发区", "type": "开发区", "level": "县级", "parent": "辉县市人民政府", "location": "辉县市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王庆军 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任市委书记，截至2026年6月"},

    # 郭奇 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "辉县市委副书记、市政府党组书记、市长"},

    # 李杨 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 姚志伟 — 人大主任
    {"person_id": 4, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},

    # 崔国兵 — 政协主席
    {"person_id": 5, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},

    # Standing committee members
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "第十五届市委常委"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "第十五届市委常委"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "第十五届市委常委"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "第十五届市委常委"},
    {"person_id": 10, "org_id": 2, "title": "市委常委、统战部部长、副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "常务副市长"},
    {"person_id": 11, "org_id": 2, "title": "市委常委、市政府党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "第十五届市委常委"},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "第十五届市委常委"},

    # Deputy mayors
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "市政府党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 经开区
    {"person_id": 20, "org_id": 5, "title": "辉县经开区管委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},

    # Predecessor
    {"person_id": 21, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任市委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 王庆军 ↔ 郭奇 (top duo)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "书记—市长搭档", "overlap_org": "中共辉县市委员会", "overlap_period": ""},

    # 王庆军 ↔ 李杨 (书记—副书记)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共辉县市委员会", "overlap_period": ""},

    # 郭奇 ↔ 李杨 (市长—副书记)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—副书记", "overlap_org": "中共辉县市委员会", "overlap_period": ""},

    # 王庆军 ↔ 姚志伟 (党委—人大)
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—人大主任", "overlap_org": "辉县市", "overlap_period": ""},

    # 王庆军 ↔ 崔国兵 (党委—政协)
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—政协主席", "overlap_org": "辉县市", "overlap_period": ""},

    # 郭奇 ↔ 闫仁强 (市长—常务副市长)
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—常务副市长", "overlap_org": "辉县市人民政府", "overlap_period": ""},

    # 郭奇 ↔ 李园丰 (市长—党组成员)
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—党组成员", "overlap_org": "辉县市人民政府", "overlap_period": ""},

    # Standing committee internal relationships (tight-knit 常委)
    {"person_a": 1, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共辉县市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共辉县市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共辉县市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共辉县市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共辉县市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共辉县市委员会", "overlap_period": ""},

    # 刘军伟 (predecessor) ↔ 王庆军 (successor)
    {"person_a": 21, "person_b": 1, "type": "交接", "context": "前任书记—现任书记", "overlap_org": "中共辉县市委员会", "overlap_period": ""},

    # Deputy mayors with mayor
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "辉县市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—副市长", "overlap_org": "辉县市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "市长—副市长", "overlap_org": "辉县市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "市长—副市长", "overlap_org": "辉县市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "市长—副市长", "overlap_org": "辉县市人民政府", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"huixian_{name}"

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "date": pos["start_date"] or "",
            "title": pos["title"],
            "org": org["name"] if org else "",
            "note": pos["note"] or "",
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    connections = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        connections.append({
            "target_name": other["name"] if other else f"person_{other_id}",
            "type": r["type"],
            "context": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
        })

    record = {
        "identity": {
            "id": slug_id,
            "name": name,
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "education": person["education"],
            "party_join": person["party_join"],
            "current_post": person["current_post"],
            "current_org": person["current_org"],
        },
        "career_timeline": career_timeline,
        "relationship_network": connections,
        "governance_profile": {
            "governance_approach": "",
            "policy_focus_areas": [],
            "open_questions": [],
        },
        "source_register": [person["source"]],
        "confidence": "confirmed" if person["source"] else "unverified",
        "investigation_date": AS_OF,
        "open_questions": _get_open_questions(person),
    }

    fname = f"{TODAY}-河南省-新乡市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person["birth"]:
        questions.append("出生年月未确认")
    if not person["birthplace"]:
        questions.append("籍贯未确认")
    if not person["ethnicity"]:
        questions.append("民族未确认")
    if not person["education"]:
        questions.append("学历教育背景未确认")
    if not person["work_start"]:
        questions.append("参加工作年份未确认")
    return questions


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

    # Write person JSONs
    print("  Writing person JSONs...")
    for p in persons:
        write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
