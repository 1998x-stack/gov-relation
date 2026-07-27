#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新乡市 (Xinxiang City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_新乡市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.xinxiang.gov.cn — 新乡市人民政府网站 (primary, current as of July 2026)
  - News articles confirm 魏建平 transitioned from mayor to Party Secretary between Apr-Jun 2026
  - News articles confirm 陈维忠 as current mayor

Confidence notes:
  - 魏建平: confirmed via multiple government news articles (July 2026) as Party Secretary;
    was mayor as of April 2026 (skills competition article)
  - 陈维忠: confirmed via government news (July 2026) as mayor
  - 李卫东: confirmed as previous Party Secretary (mentioned as recently as April 2026 skills competition)
  - Leadership roster: confirmed from party committee plenary session attendance list (June 2026)
  - Detailed career timelines (education, early career, birthplace) could not be fully verified
    due to web access limitations (Baidu Baike 403, Wikipedia timeout, Exa rate-limited)
  - Birth years and ethnicities are marked as open questions where unverified
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Uses gov_relation.runner which internally imports sqlite3 for DB creation
# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
# Also check common parent locations
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
SLUG = "新乡市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 core leaders, 10-19 standing committee, 20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "魏建平",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774822.html"
    },
    {
        "id": 2,
        "name": "陈维忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "新乡市人民政府",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774822.html"
    },
    {
        "id": 3,
        "name": "王笃波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774822.html"
    },
    {
        "id": 4,
        "name": "王新军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774822.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (市委常委)
    # Source: 市委十二届十次全会主席台就座名单 (2026-06-03)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "谢松民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    {
        "id": 6,
        "name": "祁文华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    {
        "id": 7,
        "name": "杨彦玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    {
        "id": 8,
        "name": "温伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    {
        "id": 9,
        "name": "陈红阳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "新乡市人民政府",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774833.html"
    },
    {
        "id": 10,
        "name": "李德龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    {
        "id": 11,
        "name": "崔红建",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    {
        "id": 12,
        "name": "徐光华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    {
        "id": 13,
        "name": "李军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774164.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "祝显成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新乡市人民政府",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774817.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "李卫东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共新乡市委员会",
        "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10773612.html"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共新乡市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "新乡市"},
    {"id": 2, "name": "新乡市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "新乡市"},
    {"id": 3, "name": "中国人民政治协商会议新乡市委员会", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "新乡市"},
    {"id": 4, "name": "新乡市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "新乡市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 魏建平 — current Party Secretary (promoted from mayor ~June 2026)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-06", "end_date": "", "rank": "正厅级", "note": "由市长转任市委书记"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "", "end_date": "2026-06", "rank": "正厅级", "note": "前任市长，后升任市委书记"},

    # 陈维忠 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2026-06", "end_date": "", "rank": "正厅级", "note": "新任市长"},

    # 王笃波
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # 王新军
    {"person_id": 4, "org_id": 3, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},

    # Standing committee members
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # Deputy mayor
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # Predecessor
    {"person_id": 15, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "2026-06", "rank": "正厅级", "note": "前任市委书记，去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 魏建平 ↔ 陈维忠 (mayor to successor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市长—市长交接", "overlap_org": "新乡市人民政府", "overlap_period": "2026"},
    # 魏建平 ↔ 陈红阳 (previously served as co-leaders in city government)
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "市长—常务副市长", "overlap_org": "新乡市人民政府", "overlap_period": ""},
    # 王笃波 ↔ 魏建平 (副书记—书记)
    {"person_a": 3, "person_b": 1, "type": "共事", "context": "副书记—书记", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    # 李卫东 (predecessor) ↔ 魏建平 (successor)
    {"person_a": 15, "person_b": 1, "type": "交接", "context": "前任书记—现任书记", "overlap_org": "中共新乡市委员会", "overlap_period": "2026"},
    # 李卫东 ↔ 陈维忠 (previous Party Secretary - new mayor)
    {"person_a": 15, "person_b": 2, "type": "共事", "context": "前任书记—新任市长", "overlap_org": "中共新乡市委员会", "overlap_period": "2026"},
    # Standing committee internal relationships (tight-knit)
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 12, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 13, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共新乡市委员会", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"xinxiang_{name}"

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
    core_ids = {1, 2, 3, 4, 15}  # Core leaders + predecessor
    for p in persons:
        write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
