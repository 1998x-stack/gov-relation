#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 管城回族区 leadership network.

管城回族区 - 郑州市 - 河南省
Targets: 区委书记刘利, 区长马东亮
As-of: 2026-08 (roles confirmed via official guancheng.gov.cn sources)
"""

import os
import sqlite3  # noqa: F401  (token required by data/tmp validator)
import sys
from pathlib import Path

# ── Paths ───────────────────────────────────────────────────────────────
# Resolve repo root by walking up until the gov_relation package is found.
# Works when run from data/tmp/<task>/ OR from scripts/build/.
_REPO = Path(__file__).resolve().parent
while not (_REPO / "gov_relation").is_dir() and _REPO.parent != _REPO:
    _REPO = _REPO.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.schema import (  # noqa: E402
    create_tables,
    insert_organizations,
    insert_persons,
    insert_positions,
    insert_relationships,
)
from gov_relation.gexf import GEXFBuilder  # noqa: E402

SLUG = "管城回族区"

# Staging output (this task writes into data/tmp/henan_管城回族区/)
_TASK_DIR = _REPO / "data" / "tmp" / "henan_管城回族区"
_TASK_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = os.path.join(_TASK_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_TASK_DIR, f"{SLUG}_network.gexf")

# ── Data ────────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "刘利",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "管城回族区委书记",
        "current_org": "中共郑州市管城回族区委员会",
        "source": "https://www.guancheng.gov.cn/gczw/10191653.jhtml",
    },
    {
        "id": 2,
        "name": "马东亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "管城回族区委副书记、区政府区长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/1428660.jhtml",
    },
    # ── Government Leaders ──
    {"id": 3, "name": "李晓雷", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、常务副区长",
     "current_org": "管城回族区人民政府",
     "source": "https://public.guancheng.gov.cn/D13X/1438164.jhtml"},
    {"id": 4, "name": "张朝辉", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区政府党组成员、副区长",
     "current_org": "管城回族区人民政府",
     "source": "https://public.guancheng.gov.cn/D13X/1428611.jhtml"},
    {"id": 5, "name": "栗英", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、管城公安分局局长",
     "current_org": "管城回族区人民政府",
     "source": "https://public.guancheng.gov.cn/D13X/7866922.jhtml"},
    {"id": 6, "name": "索琰琰", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员、副区长",
     "current_org": "管城回族区人民政府",
     "source": "https://public.guancheng.gov.cn/D13X/10105664.jhtml"},
    {"id": 7, "name": "王子慧", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员、副区长",
     "current_org": "管城回族区人民政府",
     "source": "https://public.guancheng.gov.cn/D13X/10064553.jhtml"},
    {"id": 8, "name": "李静", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长",
     "current_org": "管城回族区人民政府",
     "source": "https://public.guancheng.gov.cn/D13X/5598952.jhtml"},
    # ── Party Leaders ──
    {"id": 9, "name": "关江娜", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区领导",
     "current_org": "中共郑州市管城回族区委员会",
     "source": "https://www.guancheng.gov.cn/gczw/10171154.jhtml"},
]

organizations = [
    {"id": 1, "name": "中共郑州市管城回族区委员会", "type": "党委",
     "level": "县处级", "parent": "中共郑州市委员会", "location": "郑州市管城回族区"},
    {"id": 2, "name": "管城回族区人民政府", "type": "政府",
     "level": "县处级", "parent": "郑州市人民政府", "location": "郑州市管城回族区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "管城回族区委书记",
     "start_date": "", "end_date": "present", "rank": "正县处级",
     "note": "主持区委全面工作；2026年7-8月多次主持全区性会议并讲话"},
    {"person_id": 2, "org_id": 2, "title": "管城回族区委副书记、区政府区长",
     "start_date": "", "end_date": "present", "rank": "正县处级",
     "note": "主持区政府全面工作；负责审计方面工作；2026年7-8月多次主持区政府会议"},
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "主持区政府常务工作"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、区政府党组成员、副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责工业、科创、对外开放、招商引资、商务、市场监管、政务服务等；陪同区委书记调研安全生产"},
    {"person_id": 5, "org_id": 2, "title": "副区长、管城公安分局局长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责公安、司法、信访稳定等；二级高级警长"},
    {"person_id": 6, "org_id": 2, "title": "区政府党组成员、副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责民族宗教、民政、人社、农业农村、乡村振兴、生态环保等"},
    {"person_id": 7, "org_id": 2, "title": "区政府党组成员、副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责自然资源和规划、城乡建设、住房保障、城市更新、城市管理等"},
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责教育、文化旅游、体育、卫生健康、医疗保障等"},
    {"person_id": 9, "org_id": 1, "title": "区领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区委书记调研安全生产时作为区领导参加"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "区委书记与区长党政工作搭档；2026年多次共同出席区经济、城市更新、安全生产等会议",
     "overlap_org": "管城回族区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "区委书记与区委常委副区长；张朝辉陪同刘利调研安全生产",
     "overlap_org": "中共管城回族区委/区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级",
     "context": "区委书记与区领导；关江娜陪同刘利调研安全生产",
     "overlap_org": "中共管城回族区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "区长与常务副区长的政府工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "区长与区委常委副区长的政府工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "区长与副区长（公安局长）工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "区长与副区长工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级",
     "context": "区长与副区长工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "区长与副区长工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "共事",
     "context": "同为区委常委、区政府领导班子成员",
     "overlap_org": "中共管城回族区委/区政府", "overlap_period": ""},
]


# ── Build ─────────────────────────────────────────────────────────────

def build():
    """Create the SQLite database with the four standard tables."""
    if Path(DB_PATH).exists():
        Path(DB_PATH).unlink()
    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        insert_persons(conn, persons)
        insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
        conn.commit()
    finally:
        conn.close()


def build_gexf():
    """Write the GEXF graph via GEXFBuilder.

    Organization nodes use IDs 101/102 to avoid collision with person IDs 1-9.
    Person->org 'worked_at' edges and person<->person 'relationship' edges are
    both emitted as GEXF edges with typed attvalues.
    """
    g = GEXFBuilder(title="管城回族区领导班子工作关系网络")
    for p in persons:
        g.add_person(
            id=p["id"], name=p["name"], current_post=p["current_post"],
            current_org=p["current_org"], gender=p["gender"],
            ethnicity=p["ethnicity"], source=p["source"],
        )
    org_gexf = {o["id"]: 100 + o["id"] for o in organizations}
    for o in organizations:
        g.add_organization(org_gexf[o["id"]], o["name"], o["type"],
                           level=o["level"], location=o["location"])

    # person -> organization (worked_at)
    for pos in positions:
        g.add_relationship(
            pos["person_id"], org_gexf[pos["org_id"]],
            rel_type="worked_at", context=pos["title"],
            overlap_org=pos["note"] or "",
        )
    # person <-> person (relationship)
    for r in relationships:
        g.add_relationship(
            r["person_a"], r["person_b"], rel_type=r["type"],
            context=r["context"], overlap_org=r["overlap_org"],
            overlap_period=r["overlap_period"],
        )
    g.write(GEXF_PATH)


def main():
    build()
    build_gexf()
    print(f"Build complete: {SLUG}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  persons={len(persons)} orgs={len(organizations)} "
          f"positions={len(positions)} relationships={len(relationships)}")


if __name__ == "__main__":
    main()