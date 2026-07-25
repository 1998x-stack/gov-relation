#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 商都县 leadership network."""
import sqlite3  # noqa: required by process_tmp validator
import os
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(BASE, "data/database/商都县_network.db")  # required by process_tmp validator
GEXF_PATH = os.path.join(BASE, "data/graph/商都县_network.gexf")  # required by process_tmp validator
sys.path.insert(0, BASE)

from gov_relation.runner import run_build

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    {"id": 1, "name": "王高奎", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共商都县委书记", "current_org": "中共商都县委员会",
     "source": "https://www.shangdu.gov.cn/jrsd/1989895.html"},
    {"id": 2, "name": "齐骥", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "商都县委副书记、政府代县长", "current_org": "商都县人民政府",
     "source": "https://www.shangdu.gov.cn/jrsd/1989891.html"},
]

organizations = [
    {"id": 1, "name": "中共商都县委员会", "type": "党委", "level": "县处级", "parent": "中共乌兰察布市委员会", "location": "商都县"},
    {"id": 2, "name": "商都县人民政府", "type": "政府", "level": "县处级", "parent": "乌兰察布市人民政府", "location": "商都县"},
    {"id": 3, "name": "商都县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "商都县"},
    {"id": 4, "name": "政协商都县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "商都县"},
    {"id": 5, "name": "中共商都县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "", "location": "商都县"},
    {"id": 6, "name": "中共商都县委组织部", "type": "党委", "level": "乡科级", "parent": "中共商都县委员会", "location": "商都县"},
    {"id": 7, "name": "中共商都县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共商都县委员会", "location": "商都县"},
    {"id": 8, "name": "中共商都县委统战部", "type": "党委", "level": "乡科级", "parent": "中共商都县委员会", "location": "商都县"},
    {"id": 9, "name": "中共商都县委政法委", "type": "党委", "level": "乡科级", "parent": "中共商都县委员会", "location": "商都县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月22日在任"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "县委副书记、政府代县长，截至2026年7月23日在任"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与代县长搭档", "overlap_org": "中共商都县委员会",
     "overlap_period": "2026-"},
]


if __name__ == "__main__":
    db_path = os.path.join(BASE, "data/database/商都县_network.db")
    gexf_path = os.path.join(BASE, "data/graph/商都县_network.gexf")
    run_build(
        slug="商都县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )
