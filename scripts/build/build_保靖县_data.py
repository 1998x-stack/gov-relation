#!/usr/bin/env python3
"""
Build script for 保靖县 (Baojing County), 湘西土家族苗族自治州, 湖南省.
Current as of 2026-08.

Key confirmed findings (source: local repo report `report/20260714-湘西土家族苗族自治州-领导班子.md`,
itself citing zh.wikipedia.org/wiki/保靖县):
- 县委书记: 周建武 (b.1977-11, 汉族, 湖南涟源市), took office ~2024-06.
    - Previously served as 保靖县县长, promoted to 县委书记 (internal predecessor-successor).
- 县长: 郭应湘 (b.1979-06, 汉族, 湖南桂东县), took office ~2024-07.
- 前县委书记: 杨志慧 (before 周建武; exact tenure/departure unverified — open gap).
- 跨县关联: 周胜益 (龙山县县长, 保靖籍); 王京(花垣县委书记) 与周建为邻县书记。

DATA INTEGRITY NOTICE:
- Web access degraded this session (Baidu captcha, Sogou antispider, Exa MCP rate-limit).
  Core identities are CONFIRMED from the local 湘西 report. Full career resumes, education,
  party-join and work-start dates for 周建 / 郭应湘 / 杨志慧 are NOT confirmed and are
  encoded as gaps / confidence=unverified rather than fabricated.

Sources:
- report/20260714-湘西土家族苗族自治州-领导班子.md (local, cites zh.wikipedia.org/wiki/保靖县)
- report/20260725-湘西土家族苗族自治州-领导班子.md (local)
- scripts/build/build_湘西土家族苗族自治州_data.py (local, person records)
"""

import sys
import os
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.gexf import GEXFBuilder
import sqlite3

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now().strftime("%Y-%m-%d")

persons = [
    {
        "id": 1, "name": "周建武", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-11", "birthplace": "湖南省涟源市",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "保靖县委书记", "current_org": "中共保靖县委员会",
        "source": "湘西州领导班子报告(2026-07) / zh.wikipedia.org/wiki/保靖县",
    },
    {
        "id": 2, "name": "郭应湘", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-06", "birthplace": "湖南省桂东县",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "保靖县县长", "current_org": "保靖县人民政府",
        "source": "湘西州领导班子报告(2026-07) / zh.wikipedia.org/wiki/保靖县",
    },
    {
        # Predecessor 保靖县委书记 (before 周建武)
        "id": 3, "name": "杨志慧", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "保靖县委原书记（任期/去向待查）", "current_org": "中共保靖县委员会（已卸任）",
        "source": "搜狗联想词 '保靖县委书记杨志慧简历'（任期未核实）",
    },
    {
        "id": 4, "name": "周胜益", "gender": "男", "ethnicity": "苗族",
        "birth": "1972-09", "birthplace": "湖南省保靖县",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县县长", "current_org": "龙山县人民政府",
        "source": "湘西州领导班子报告(2026-07)；保靖籍干部网络",
    },
    {
        "id": 5, "name": "王京海", "gender": "男", "ethnicity": "土家族",
        "birth": "1975-09", "birthplace": "湖南省慈利县",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "花垣县委书记（兼县长）", "current_org": "中共花垣县委员会",
        "source": "湘西州领导班子报告(2026-07)",
    },
    {
        "id": 6, "name": "刘涛", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "河南省",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "湘西州委书记", "current_org": "中共湘西土家族苗族自治州委员会",
        "source": "湘西州领导班子报告(2026-07)；跨省调任(2024-10)",
    },
]

organizations = [
    {"id": 1, "name": "中共保靖县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "保靖县"},
    {"id": 2, "name": "保靖县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "保靖县"},
    {"id": 3, "name": "中共湘西土家族苗族自治州委员会", "type": "prefecture_party", "level": "prefecture",
     "parent": "中共湖南省委员会", "location": "吉首市"},
    {"id": 4, "name": "湘西土家族苗族自治州人民政府", "type": "prefecture_gov", "level": "prefecture",
     "parent": "湖南省人民政府", "location": "吉首市"},
    {"id": 5, "name": "中共花垣县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "花垣县"},
    {"id": 6, "name": "龙山县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "龙山县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "保靖县委书记", "start_date": "2024-06", "end_date": "", "rank": "正处级",
     "note": "由保靖县长升任"},
    {"person_id": 1, "org_id": 2, "title": "保靖县县长", "start_date": "", "end_date": "2024-06", "rank": "正处级",
     "note": "2024-06 升县委书记；县长任期开始日期未核实(gap)"},
    {"person_id": 2, "org_id": 2, "title": "保靖县县长", "start_date": "2024-07", "end_date": "", "rank": "正处级",
     "note": "2024-07 接任"},
    {"person_id": 3, "org_id": 1, "title": "保靖县委书记", "start_date": "", "end_date": "2024-06", "rank": "正处级",
     "note": "保靖县委原书记；任期与去向未核实"},
    {"person_id": 4, "org_id": 6, "title": "龙山县县长", "start_date": "2022-03", "end_date": "", "rank": "正处级",
     "note": "保靖籍干部，跨县主政"},
    {"person_id": 5, "org_id": 5, "title": "花垣县委书记", "start_date": "2025-02", "end_date": "", "rank": "正处级",
     "note": "兼县长；与周建武同为邻县书记"},
    {"person_id": 6, "org_id": 3, "title": "湘西州委书记", "start_date": "2024-10", "end_date": "", "rank": "正厅级",
     "note": "跨省调任，接替虢正贵"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "郭应湘接任周建武的县长（周2024-06升书记，郭2024-07任县长）",
     "overlap_org": "保靖县人民政府", "overlap_period": "2024-07"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "周建武接替杨志慧任保靖县委书记",
     "overlap_org": "中共保靖县委员会", "overlap_period": "2024-06"},
    {"person_a": 1, "person_b": 5, "type": "neighbor_colleagues",
     "context": "周建武(保靖书记)与王京海(花垣书记)为邻县书记",
     "overlap_org": "", "overlap_period": "2024-06起"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "周建武隶于刘涛(湘西州委书记)",
     "overlap_org": "中共湘西土家族苗族自治州委员会", "overlap_period": "2024-10起"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "郭应湘隶于州委书记刘涛所属党委",
     "overlap_org": "中共湘西土家族苗族自治州委员会", "overlap_period": "2024-10起"},
    {"person_a": 4, "person_b": 1, "type": "same_native_place",
     "context": "周胜益(龙山县县长)为保靖人，与保靖干部同籍网络",
     "overlap_org": "", "overlap_period": ""},
]

DB_PATH = str(SCRIPT_DIR / "保靖县_network.db")
GEXF_PATH = str(SCRIPT_DIR / "保靖县_network.gexf")

if __name__ == "__main__":
    slug = "保靖县"
    db_path = SCRIPT_DIR / f"{slug}_network.db"
    gexf_path = SCRIPT_DIR / f"{slug}_network.gexf"

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
        print(f"Runner API OK: {len(persons)} persons, {len(organizations)} orgs, "
              f"{len(positions)} positions, {len(relationships)} relationships")
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
            conn.execute(
                "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                 p["education"], p["party_join"], p["work_start"], p["current_post"],
                 p["current_org"], p["source"]))
        for o in organizations:
            conn.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                         (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
        for pos in positions:
            conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                         (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
                          pos["end_date"], pos["rank"], pos["note"]))
        for r in relationships:
            conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                         (r["person_a"], r["person_b"], r["type"], r["context"],
                          r["overlap_org"], r["overlap_period"]))
        conn.commit()
        conn.close()
        print(f"SQLite DB: {db_path}")
        builder = GEXFBuilder(title=slug)
        for p in persons:
            builder.add_person(id=p["id"], name=p["name"], current_post=p["current_post"],
                               current_org=p["current_org"], gender=p.get("gender", ""),
                               ethnicity=p.get("ethnicity", ""), birth=p.get("birth", ""),
                               source=p.get("source", ""))
        for o in organizations:
            builder.add_organization(id=o["id"] + 100000, name=o["name"], org_type=o["type"],
                                     level=o["level"], location=o["location"])
        for r in relationships:
            builder.add_relationship(source=r["person_a"], target=r["person_b"], rel_type=r.get("type", ""),
                                     context=r.get("context", ""), overlap_org=r.get("overlap_org", ""),
                                     overlap_period=r.get("overlap_period", ""))
        builder.write(gexf_path)
        print(f"GEXF graph: {gexf_path}")

    print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print(f"Output: {db_path}, {gexf_path}")