#!/usr/bin/env python3
"""
Build script for 花垣县 (Huayuan County), 湘西土家族苗族自治州, 湖南省.
Current as of 2026-08.

Key findings:
- 王京海 concurrently serves as 县委书记 and 县长 (since 2025-02 for secretary, 2022-03 for mayor)
- 花垣县 natives hold leadership posts in 龙山县 (时荣芬) and 凤凰县 (樊忠清)
- Strong cross-county cadre exchange within 湘西州

Sources:
- https://zh.wikipedia.org/wiki/花垣县
- https://zh.wikipedia.org/wiki/湘西土家族苗族自治州
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──────────────────────────────
# Works from both staging (data/tmp/...) and canonical (scripts/build/) locations
_REPO_ROOT = Path(__file__).resolve()
while not (_REPO_ROOT / "gov_relation" / "runner.py").exists() or _REPO_ROOT.name == "scripts":
    _REPO_ROOT = _REPO_ROOT.parent
    if _REPO_ROOT == _REPO_ROOT.parent:
        raise RuntimeError("Could not find repo root (gov_relation/runner.py)")
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.gexf import GEXFBuilder
import sqlite3

# ── Detect staging vs canonical ────────────────────────────────────
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ───────────────────────────────────────────────────────────

persons = [
    # ── Current top leader: 县委书记兼县长 ──
    {
        "id": 1,
        "name": "王京海",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1975-09",
        "birthplace": "湖南省慈利县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花垣县委书记兼县长",
        "current_org": "中共花垣县委员会",
        "source": "https://zh.wikipedia.org/wiki/花垣县",
    },
    # ── Predecessor: 原县委书记 ──
    {
        "id": 2,
        "name": "廖良辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花垣县委原书记",
        "current_org": "中共花垣县委员会",
        "source": "https://zh.wikipedia.org/wiki/花垣县",
    },
    # ── 县人大常委会主任 ──
    {
        "id": 3,
        "name": "龙仕英",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花垣县人大常委会主任",
        "current_org": "花垣县人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/花垣县",
    },
    # ── 县政协主席 ──
    {
        "id": 4,
        "name": "滕树红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花垣县政协主席",
        "current_org": "政协花垣县委员会",
        "source": "https://zh.wikipedia.org/wiki/花垣县",
    },
    # ── 花垣-native leaders in adjacent counties ──
    {
        "id": 5,
        "name": "时荣芬",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1976-12",
        "birthplace": "湖南省花垣县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙山县县委书记",
        "current_org": "中共龙山县委员会",
        "source": "https://zh.wikipedia.org/wiki/龙山县",
    },
    {
        "id": 6,
        "name": "樊忠清",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1975-10",
        "birthplace": "湖南省花垣县",
        "education": "中央党校函授学院本科班法律专业",
        "party_join": "1997-12",
        "work_start": "1996-09",
        "current_post": "凤凰县县长",
        "current_org": "凤凰县人民政府",
        "source": "https://baike.baidu.com/item/樊忠清",
    },
    # ── Prefecture leaders ──
    {
        "id": 7,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "河南省方城县",
        "education": "研究生（河南大学中国现代文学硕士）",
        "party_join": "1996-11",
        "work_start": "1997-07",
        "current_post": "湘西州委书记",
        "current_org": "中共湘西土家族苗族自治州委员会",
        "source": "https://zh.wikipedia.org/wiki/刘涛_(1971年)",
    },
    {
        "id": 8,
        "name": "尚生龙",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1972-05",
        "birthplace": "湖南省桑植县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "湘西州州长（代理）",
        "current_org": "湘西土家族苗族自治州人民政府",
        "source": "https://zh.wikipedia.org/wiki/湘西土家族苗族自治州",
    },
    # ── Neighboring county leaders (for relationship edges) ──
    {
        "id": 9,
        "name": "毛家",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1973-10",
        "birthplace": "湖南省永顺县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委书记",
        "current_org": "中共凤凰县委员会",
        "source": "https://zh.wikipedia.org/wiki/凤凰县",
    },
    {
        "id": 10,
        "name": "周建武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "湖南省涟源市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保靖县委书记",
        "current_org": "中共保靖县委员会",
        "source": "https://zh.wikipedia.org/wiki/保靖县",
    },
    {
        "id": 11,
        "name": "郭应湘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "湖南省桂东县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保靖县县长",
        "current_org": "保靖县人民政府",
        "source": "https://zh.wikipedia.org/wiki/保靖县",
    },
    {
        "id": 12,
        "name": "向加茂",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1973-02",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永顺县委书记兼县长",
        "current_org": "中共永顺县委员会",
        "source": "https://zh.wikipedia.org/wiki/永顺县",
    },
]

organizations = [
    {"id": 1, "name": "中共花垣县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "花垣县"},
    {"id": 2, "name": "花垣县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "花垣县"},
    {"id": 3, "name": "花垣县人民代表大会常务委员会", "type": "npc", "level": "county",
     "parent": "湘西土家族苗族自治州人大常委会", "location": "花垣县"},
    {"id": 4, "name": "政协花垣县委员会", "type": "cppcc", "level": "county",
     "parent": "政协湘西土家族苗族自治州委员会", "location": "花垣县"},
    {"id": 5, "name": "中共湘西土家族苗族自治州委员会", "type": "prefecture_party", "level": "prefecture",
     "parent": "中共湖南省委员会", "location": "吉首市"},
    {"id": 6, "name": "湘西土家族苗族自治州人民政府", "type": "prefecture_gov", "level": "prefecture",
     "parent": "湖南省人民政府", "location": "吉首市"},
    {"id": 7, "name": "中共凤凰县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "凤凰县"},
    {"id": 8, "name": "凤凰县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "凤凰县"},
    {"id": 9, "name": "中共龙山县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "龙山县"},
    {"id": 10, "name": "中共保靖县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "保靖县"},
    {"id": 11, "name": "保靖县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "保靖县"},
    {"id": 12, "name": "中共永顺县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "永顺县"},
    {"id": 13, "name": "永顺县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "永顺县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "花垣县委书记", "start_date": "2025-02", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "花垣县长", "start_date": "2022-03", "end_date": "", "rank": "正处级", "note": "书记兼县长"},
    {"person_id": 2, "org_id": 1, "title": "花垣县委原书记", "start_date": "", "end_date": "2025-02", "rank": "正处级", "note": "廖良辉卸任后王京海接任"},
    {"person_id": 3, "org_id": 3, "title": "花垣县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "花垣县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 9, "title": "龙山县县委书记", "start_date": "2022-01", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "凤凰县县长", "start_date": "2022-03", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "湘西州委书记", "start_date": "2024-10", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "湘西州州长（代理）", "start_date": "2026-06", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "凤凰县委书记", "start_date": "2022-01", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "保靖县委书记", "start_date": "2024-06", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 11, "title": "保靖县县长", "start_date": "2024-07", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 12, "title": "永顺县委书记", "start_date": "2025-02", "end_date": "", "rank": "正处级", "note": "书记兼县长"},
    {"person_id": 12, "org_id": 13, "title": "永顺县长", "start_date": "2021-10", "end_date": "", "rank": "正处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 5, "type": "same_county_system",
     "context": "王京海（花垣书记）与时荣芬（龙山书记）同属湘西州县书记网络",
     "overlap_org": "中共湘西土家族苗族自治州委员会", "overlap_period": "2025-02起"},
    {"person_a": 1, "person_b": 6, "type": "same_origin_network",
     "context": "王京海(花垣书记)与樊忠清(凤凰县长)同系花垣县干部网络",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor",
     "context": "廖良辉卸任花垣县委书记后王京海于2025年2月接任",
     "overlap_org": "中共花垣县委员会", "overlap_period": "2025-02"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "王京海（花垣书记）直属刘涛（湘西州委书记）领导",
     "overlap_org": "中共湘西土家族苗族自治州委员会", "overlap_period": "2025-02起"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "王京海（花垣县长→书记）受尚生龙（湘西州代州长）",
     "overlap_org": "湘西土家族苗族自治州人民政府", "overlap_period": "2025-02起"},
    {"person_a": 1, "person_b": 10, "type": "neighboring_county_colleagues",
     "context": "王京海（花垣书记）与周建武（保靖书记）为邻县书记",
     "overlap_org": "", "overlap_period": "2024-06起"},
    {"person_a": 1, "person_b": 12, "type": "neighboring_county_colleagues",
     "context": "王京海（花垣书记）与向加茂（永顺书记）为邻县书记",
     "overlap_org": "", "overlap_period": "2025-02起"},
]

# ══════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════

# ── process_tmp.py token markers ──────────────────────────────────
DB_PATH = str(SCRIPT_DIR / "花垣县_network.db")
GEXF_PATH = str(SCRIPT_DIR / "花垣县_network.gexf")

if __name__ == "__main__":
    slug = "花垣县"
    # Route output: staging → local dir, canonical → data/database/ and data/graph/
    STAGING = "/data/tmp/" in str(SCRIPT_DIR)
    if STAGING:
        db_path = SCRIPT_DIR / f"{slug}_network.db"
        gexf_path = SCRIPT_DIR / f"{slug}_network.gexf"
    else:
        db_path = _REPO_ROOT / "data" / "database" / f"{slug}_network.db"
        gexf_path = _REPO_ROOT / "data" / "graph" / f"{slug}_network.gexf"

    try:
        run_build(
            slug=slug,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=str(db_path),
            gexf_path=str(gexf_path),
            overwrite=True,
        )
        print(f"Runner API OK: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    except Exception as e:
        print(f"runner API failed: {e}")
        print("Falling back to direct build...")

        os.makedirs(SCRIPT_DIR, exist_ok=True)
        conn = sqlite3.connect(str(db_path))
        conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '');
        CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '', level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '');
        CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '');
        CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '');
        """)
        for p in persons:
            conn.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                         (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                          p["education"], p["party_join"], p["work_start"],
                          p["current_post"], p["current_org"], p["source"]))
        for o in organizations:
            conn.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                         (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
        for pos in positions:
            conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                         (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
        for r in relationships:
            conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                         (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
        conn.commit()
        conn.close()
        print(f"SQLite DB: {db_path}")

        # GEXF
        builder = GEXFBuilder(title=slug)
        for p in persons:
            builder.add_person(id=p["id"], name=p["name"], current_post=p["current_post"],
                              current_org=p["current_org"], gender=p.get("gender",""),
                              ethnicity=p.get("ethnicity",""), birth=p.get("birth",""), source=p.get("source",""))
        for o in organizations:
            builder.add_organization(id=o["id"] + 100000, name=o["name"], org_type=o["type"],
                                     level=o["level"], location=o["location"])
        for r in relationships:
            builder.add_relationship(source=r["person_a"], target=r["person_b"], rel_type=r.get("type",""),
                                     context=r.get("context",""), overlap_org=r.get("overlap_org",""),
                                     overlap_period=r.get("overlap_period",""))
        builder.write(gexf_path)
        print(f"GEXF graph: {gexf_path}")

    print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    print(f"Output: {db_path}, {gexf_path}")