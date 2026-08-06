#!/usr/bin/env python3
"""
Build script for 永顺县 (Yongshun County), 湘西土家族苗族自治州, 湖南省.
Current as of 2026-08.

Key findings (sources: local repo report `report/20260714-湘西土家族苗族自治州-领导班子.md`
citing zh.wikipedia.org/wiki/永顺县, plus Sogou first-result for 永顺县委换届):
- 县委书记: 向加茂 (苗族, 湖南永顺/湘西, ~1973-02生之间), took office ~2025-02.
    - Previously served as 永顺县县长 (from ~2021-10), promoted to 县委书记; currently
      serves 书记兼县长 (一肩挑) — second such arrangement in 湘西州 (also 花垣王京海).
- 县长: 向加茂（兼）— no separate 县长 appointed yet since his 2025-02 promotion.
- 前县委书记: 彭军 (was 书记 in 2022, before 向加茂; exact tenure/departure unverified — gap).
- 县委副书记: 周海强、龙海先; 县纪委书记: 曾有成.
- 新一届县委常委: 向加茂、周海强、龙海先、曾有成、聂仁海、杨湉、张永强、张海峰、谢深洪、陈济祧、彭忠华.
- 跨县永顺人网络: 彭武学(泸溪县委书记,永顺人), 毛家(凤凰县委书记,永顺人); 符家波曾任永顺县委副书记后转泸溪县长(plausible).
- 上级领导: 州委书记 刘涛(河南,2024-10 跨省调任), 州长(代理) 尚生龙(2026-06, 土家族).

DATA INTEGRITY NOTICE:
- Web access degraded this session (Baidu captcha, 永顺政府官网 ysx.gov.cn 412/空页, Google JS渲染,
  Exa MCP rate-limit, Wikipedia/Jina timeout).
  Core identities (向加茂书记/县长) are CONFIRMED from the local 湘西州 report + Sogou first-result.
  Full career resumes, education, party-join and work-start dates for 向加茂 / 彭军 are NOT confirmed
  and are encoded as gaps / confidence=plausible|unverified rather than fabricated.
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
        "id": 1, "name": "向加茂", "gender": "男", "ethnicity": "苗族",
        "birth": "1973-02", "birthplace": "湖南省永顺县",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "永顺县委书记（兼县长）", "current_org": "中共永顺县委员会",
        "source": "湘西州领导班子报告(2026-07) / zh.wikipedia.org/wiki/永顺县 / Sogou 永顺县委换届",
    },
    {
        # Predecessor 永顺县委书记 (before 向加茂)
        "id": 2, "name": "彭军", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "永顺县委原书记（任期/去向待查）", "current_org": "中共永顺县委员会（已卸任）",
        "source": "腾讯视频'总监·书记访谈'(2022-09)提及永顺县委书记彭军（任期未核实）",
    },
    {
        "id": 3, "name": "周海强", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "永顺县委副书记", "current_org": "中共永顺县委员会",
        "source": "Sogou 永顺县委换届新一届党委名单（周海强为县委副书记）",
    },
    {
        "id": 4, "name": "龙海先", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "永顺县委副书记", "current_org": "中共永顺县委员会",
        "source": "Sogou 永顺县委换届新一届党委名单（龙海先为县委副书记）",
    },
    {
        "id": 5, "name": "曾有成", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "永顺县纪委书记、县监委主任", "current_org": "中共永顺县纪律检查委员会",
        "source": "Sogou 永顺县纪委换届选举曾有成为县纪委书记",
    },
    {
        "id": 6, "name": "曾甲林", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "永顺县人大常委会主任（待核）", "current_org": "永顺县人大常委会",
        "source": "湘西州领导班子报告(2026-07)提及永顺人大主任疑为曾甲林（未经核实，gap）",
    },
    {
        "id": 7, "name": "彭武学", "gender": "男", "ethnicity": "土家族",
        "birth": "1971-05", "birthplace": "湖南省永顺县",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "泸溪县委书记", "current_org": "中共泸溪县委员会",
        "source": "湘西州领导班子报告(2026-07)；永顺人跨县主政泸溪",
    },
    {
        "id": 8, "name": "毛家", "gender": "男", "ethnicity": "土家族",
        "birth": "1973-10", "birthplace": "湖南省永顺县",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "凤凰县委书记", "current_org": "中共凤凰县委员会",
        "source": "湘西州领导班子报告(2026-07)；永顺籍干部跨县主政凤凰",
    },
    {
        "id": 9, "name": "刘涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-06", "birthplace": "河南省方城县",
        "education": "", "party_join": "1996-11", "work_start": "1997-07",
        "current_post": "湘西州州委书记", "current_org": "中共湘西土家族苗族自治州委员会",
        "source": "湘西州领导班子报告(2026-07) / 维基百科 刘涛(1971年)",
    },
    {
        "id": 10, "name": "尚生龙", "gender": "男", "ethnicity": "土家族",
        "birth": "1972-05", "birthplace": "湖南省桑植县",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "湘西州州长（代理）", "current_org": "湘西土家族苗族自治州人民政府",
        "source": "湘西州领导班子报告(2026-07)；2026-06 代理州长",
    },
    {
        "id": 11, "name": "符家波", "gender": "男", "ethnicity": "苗族",
        "birth": "1979-05", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "泸溪县县长", "current_org": "泸溪县人民政府",
        "source": "湘西州领导班子报告(2026-07)；Sogou 2022 年'永顺县委副书记符家波'（跨县迁转线索）",
    },
]

organizations = [
    {"id": 1, "name": "中共永顺县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "永顺县"},
    {"id": 2, "name": "永顺县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "永顺县"},
    {"id": 3, "name": "永顺县人大常委会", "type": "county_people_congress", "level": "county",
     "parent": "湖南省人民代表大会", "location": "永顺县"},
    {"id": 4, "name": "中共永顺县纪律检查委员会", "type": "county_discipline", "level": "county",
     "parent": "中共湘西土家族苗族自治州纪律检查委员会", "location": "永顺县"},
    {"id": 5, "name": "中共湘西土家族苗族自治州委员会", "type": "prefecture_party", "level": "prefecture",
     "parent": "中共湖南省委员会", "location": "吉首市"},
    {"id": 6, "name": "湘西土家族苗族自治州人民政府", "type": "prefecture_gov", "level": "prefecture",
     "parent": "湖南省人民政府", "location": "吉首市"},
    {"id": 7, "name": "中共泸溪县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "泸溪县"},
    {"id": 8, "name": "泸溪县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "泸溪县"},
    {"id": 9, "name": "中共凤凰县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "凤凰县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "永顺县委书记", "start_date": "2025-02", "end_date": "", "rank": "正处级",
     "note": "由永顺县长升任书记，兼县长（一肩挑）"},
    {"person_id": 1, "org_id": 2, "title": "永顺县县长", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": "2021-10 任县长；2025-02 升书记后仍兼县长（新县长未任命，gap）"},
    {"person_id": 2, "org_id": 1, "title": "永顺县委书记", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "向加茂之前任永顺县委书记(2022年在位)；任期与离任去向未核实(gap)"},
    {"person_id": 9, "org_id": 5, "title": "湘西州州委书记", "start_date": "2024-10", "end_date": "", "rank": "正厅级",
     "note": "跨省调任；接替虢正贵"},
    {"person_id": 10, "org_id": 6, "title": "湘西州州长（代理）", "start_date": "2026-06", "end_date": "", "rank": "正厅级",
     "note": "接替陈华"},
    {"person_id": 3, "org_id": 1, "title": "永顺县委副书记", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "新一届永顺县委副书记"},
    {"person_id": 4, "org_id": 1, "title": "永顺县委副书记", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "新一届永顺县委副书记"},
    {"person_id": 5, "org_id": 4, "title": "永顺县纪委书记", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "新一届永顺县纪委选举产生"},
    {"person_id": 7, "org_id": 7, "title": "泸溪县委书记", "start_date": "2021-06", "end_date": "", "rank": "正处级",
     "note": "永顺籍干部跨县主政泸溪"},
    {"person_id": 8, "org_id": 9, "title": "凤凰县委书记", "start_date": "2022-01", "end_date": "", "rank": "正处级",
     "note": "永顺籍干部跨县主政凤凰"},
    {"person_id": 11, "org_id": 8, "title": "泸溪县县长", "start_date": "2023-11", "end_date": "", "rank": "正处级",
     "note": "曾任永顺县委副书记（2022）后跨县任泸溪县长（plausible）"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "向加茂接替彭军任永顺县委书记（彭军2022年在任，向加茂2025-02升书记）",
     "overlap_org": "中共永顺县委员会", "overlap_period": "2025-02"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "向加茂受刘涛（湘西州委书记）领导",
     "overlap_org": "中共湘西土家族苗族自治州委员会", "overlap_period": "2024-10起"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "向加茂的县长身份隶属尚生龙(代理州长)所辖政府序列",
     "overlap_org": "湘西土家族苗族自治州人民政府", "overlap_period": "2026-06起"},
    {"person_a": 7, "person_b": 1, "type": "same_native_place",
     "context": "彭武学(泸溪县委书记)为永顺籍，与永顺县同乡网络",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 8, "person_b": 1, "type": "same_native_place",
     "context": "毛家(凤凰县委书记)为永顺籍，与永顺县同乡网络",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 11, "person_b": 1, "type": "cross_county_rotation",
     "context": "符家波曾任永顺县委副书记(2022)，后跨县任泸溪县长(2023-11)（plausible履历关联）",
     "overlap_org": "中共永顺县委员会", "overlap_period": "2022"},
]

DB_PATH = str(SCRIPT_DIR / "永顺县_network.db")
GEXF_PATH = str(SCRIPT_DIR / "永顺县_network.gexf")

if __name__ == "__main__":
    slug = "永顺县"
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