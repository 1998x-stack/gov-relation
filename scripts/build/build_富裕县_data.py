#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 富裕县 leadership network.

富裕县隶属于黑龙江省齐齐哈尔市。

Current leadership as of 2025-11 (source: Baidu Baike county page):
- 县委书记: 董加成
- 县长: 代友谊
- 人大主任: 杨荣华
- 政协主席: 杨丽

NOTE: Due to severely degraded web access (Exa rate-limited, Baidu/Google/Bing
blocked or timing out, Jina Reader timed out), detailed biographical data
(birth, birthplace, education, full career timeline) for most figures could
not be obtained. The database and graph encode the confirmed leadership roster
with gaps explicitly marked.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "富裕县"

# Write to staging directory (this script lives in data/tmp/heilongjiang_富裕县/)
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "富裕县_network.db"
GEXF_PATH = STAGING_DIR / "富裕县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共富裕县委员会", "type": "党委", "level": "县处级", "parent": "中共齐齐哈尔市委", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 2, "name": "富裕县人民政府", "type": "政府", "level": "县处级", "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 3, "name": "富裕县人大常委会", "type": "人大", "level": "县处级", "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 4, "name": "富裕县政协", "type": "政协", "level": "县处级", "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 5, "name": "中共富裕县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共齐齐哈尔市纪委", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 6, "name": "中共富裕县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共富裕县委员会", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 7, "name": "中共富裕县委组织部", "type": "党委", "level": "县处级", "parent": "中共富裕县委员会", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 8, "name": "中共富裕县委宣传部", "type": "党委", "level": "县处级", "parent": "中共富裕县委员会", "location": "黑龙江省齐齐哈尔市富裕县"},
    {"id": 9, "name": "中共富裕县委统战部", "type": "党委", "level": "县处级", "parent": "中共富裕县委员会", "location": "黑龙江省齐齐哈尔市富裕县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ── 县委领导 ──
    {"id": 1, "name": "董加成", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共富裕县委书记", "current_org": "中共富裕县委员会",
     "source": "https://baike.baidu.com/item/%E5%AF%8C%E8%A3%95%E5%8E%BF"},
    # 代友谊 — 县长
    {"id": 2, "name": "代友谊", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富裕县委副书记、县政府县长", "current_org": "富裕县人民政府",
     "source": "https://baike.baidu.com/item/%E5%AF%8C%E8%A3%95%E5%8E%BF"},
    # 杨荣华 — 人大主任
    {"id": 3, "name": "杨荣华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富裕县人大常委会主任", "current_org": "富裕县人大常委会",
     "source": "https://baike.baidu.com/item/%E5%AF%8C%E8%A3%95%E5%8E%BF"},
    # 杨丽 — 政协主席
    {"id": 4, "name": "杨丽", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富裕县政协主席", "current_org": "富裕县政协",
     "source": "https://baike.baidu.com/item/%E5%AF%8C%E8%A3%95%E5%8E%BF"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 董加成
    {"person_id": 1, "org_id": 1, "title": "中共富裕县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 代友谊
    {"person_id": 2, "org_id": 1, "title": "富裕县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "富裕县政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 杨荣华
    {"person_id": 3, "org_id": 3, "title": "富裕县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 杨丽
    {"person_id": 4, "org_id": 4, "title": "富裕县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 董加成 — 代友谊（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "富裕县委班子党政正职搭档", "overlap_org": "中共富裕县委员会/富裕县人民政府", "overlap_period": ""},
    # 董加成 — 杨荣华（县委-人大）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委-人大班子搭档", "overlap_org": "中共富裕县委员会/富裕县人大常委会", "overlap_period": ""},
    # 代友谊 — 杨荣华（政府-人大）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "政府-人大班子搭档", "overlap_org": "富裕县人民政府/富裕县人大常委会", "overlap_period": ""},
    # 杨丽 — 董加成（政协-县委）
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "政协-县委班子搭档", "overlap_org": "富裕县政协/中共富裕县委员会", "overlap_period": ""},
]

# ── BUILD ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
