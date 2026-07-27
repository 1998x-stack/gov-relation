#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 依安县 leadership network.

依安县隶属黑龙江省齐齐哈尔市。

Current leadership as of 2026-07 (source: Baidu Baike, http://www.hljyian.gov.cn/):
- 县委书记: 王柱
- 县长: 马福明

Note: Due to degraded web access (Exa rate-limited, Baidu/Google/Bing unavailable),
detailed biographical data (birth, birthplace, education, full career timeline) for
most figures could not be obtained. The database and graph encode the confirmed
leadership roster with gaps explicitly marked.
"""

import sqlite3
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "依安县"
DB_PATH = DATABASE_DIR / "依安县_network.db"
GEXF_PATH = GRAPH_DIR / "依安县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共依安县委员会", "type": "党委", "level": "县处级", "parent": "中共齐齐哈尔市委", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 2, "name": "依安县人民政府", "type": "政府", "level": "县处级", "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 3, "name": "依安县人大常委会", "type": "人大", "level": "县处级", "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 4, "name": "依安县政协", "type": "政协", "level": "县处级", "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 5, "name": "中共依安县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共齐齐哈尔市纪委", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 6, "name": "中共依安县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共依安县委员会", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 7, "name": "中共依安县委组织部", "type": "党委", "level": "县处级", "parent": "中共依安县委员会", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 8, "name": "中共依安县委宣传部", "type": "党委", "level": "县处级", "parent": "中共依安县委员会", "location": "黑龙江省齐齐哈尔市依安县"},
    {"id": 9, "name": "中共依安县委统战部", "type": "党委", "level": "县处级", "parent": "中共依安县委员会", "location": "黑龙江省齐齐哈尔市依安县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ── 县委领导 ──
    {"id": 1, "name": "王柱", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共依安县委书记", "current_org": "中共依安县委员会",
     "source": "http://www.hljyian.gov.cn/"},
    # 马福明 — 县长
    {"id": 2, "name": "马福明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依安县委副书记、县政府县长", "current_org": "依安县人民政府",
     "source": "http://www.hljyian.gov.cn/"},
    # Note: The full 县委常委 roster was not accessible from the JS-rendered
    # leadership page. Key deputy positions are unknown at this time.
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 王柱
    {"person_id": 1, "org_id": 1, "title": "中共依安县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 马福明
    {"person_id": 2, "org_id": 1, "title": "依安县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "依安县政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 王柱 — 马福明（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委班子党政正职搭档", "overlap_org": "中共依安县委员会/依安县人民政府", "overlap_period": ""},
]


if __name__ == "__main__":
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
    print("Build complete.")
