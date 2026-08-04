#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 昌都市 (Qamdo) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/changdu_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/changdu_network.gexf")

# ── DATA ──
persons = [
    {"id": 1, "name": "庄劲松", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-03", "birthplace": "", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "昌都市委书记", "current_org": "中共昌都市委员会",
     "source": "https://baike.baidu.com/item/%E5%BA%84%E5%8A%B2%E6%9D%BE/58702246"},
    {"id": 2, "name": "龚会才", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "四川宣汉", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1990-07",
     "current_post": "西藏自治区党委常委、秘书长", "current_org": "中共西藏自治区委员会",
     "source": "https://baike.baidu.com/item/%E9%BE%9A%E4%BC%9A%E6%89%8D"},
    {"id": 3, "name": "普布顿珠", "gender": "男", "ethnicity": "藏族",
     "birth": "1972-11", "birthplace": "西藏江孜", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1996-07",
     "current_post": "四川省委常委、统战部部长", "current_org": "中共四川省委统战部",
     "source": "https://baike.baidu.com/item/%E6%99%AE%E5%B8%83%E9%A1%BF%E7%8F%A0"},
    {"id": 4, "name": "罗布顿珠", "gender": "男", "ethnicity": "藏族",
     "birth": "1960-12", "birthplace": "西藏琼结", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "1978-08",
     "current_post": "援助西藏发展基金会副理事长兼秘书长", "current_org": "援助西藏发展基金会",
     "source": "https://baike.baidu.com/item/%E7%BD%97%E5%B8%83%E9%A1%BF%E7%8F%A0/10538998"},
    {"id": 5, "name": "罗庆伍", "gender": "男", "ethnicity": "藏族",
     "birth": "1971-05", "birthplace": "西藏那曲", "education": "自治区党委党校大专",
     "party_join": "中共党员", "work_start": "1992-07",
     "current_post": "昌都市委副书记、市长", "current_org": "昌都市人民政府",
     "source": "https://baike.baidu.com/item/%E7%BD%97%E5%BA%86%E4%BC%8D"},
    {"id": 6, "name": "洛桑江村", "gender": "男", "ethnicity": "藏族",
     "birth": "1957-07", "birthplace": "西藏察雅（昌都）", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "1976-02",
     "current_post": "全国人大常委会副委员长", "current_org": "全国人大常委会",
     "source": "https://baike.baidu.com/item/%E6%B4%9B%E6%A1%91%E6%B1%9F%E6%9D%91"},
    {"id": 7, "name": "白玛赤林", "gender": "男", "ethnicity": "藏族",
     "birth": "1951-10", "birthplace": "西藏丁青（昌都）", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "1969-12",
     "current_post": "原全国人大常委会副委员长", "current_org": "全国人大常委会",
     "source": "https://baike.baidu.com/item/%E7%99%BD%E7%8E%9B%E8%B5%A4%E6%9E%97"},
    {"id": 8, "name": "向巴平措", "gender": "男", "ethnicity": "藏族",
     "birth": "1947-05", "birthplace": "西藏昌都", "education": "重庆大学",
     "party_join": "中共党员", "work_start": "1970-10",
     "current_post": "原全国人大常委会副委员长（退休）", "current_org": "全国人大常委会",
     "source": "https://baike.baidu.com/item/%E5%90%91%E5%B7%B4%E5%B9%B3%E6%8E%AA"},
]

organizations = [
    {"id": 1, "name": "中共昌都市委员会", "type": "党委", "level": "地级",
     "parent": "中共西藏自治区委员会", "location": "西藏自治区昌都市"},
    {"id": 2, "name": "昌都市人民政府", "type": "政府", "level": "地级",
     "parent": "西藏自治区人民政府", "location": "西藏自治区昌都市"},
    {"id": 3, "name": "中共西藏自治区委员会", "type": "党委", "level": "省级",
     "parent": "", "location": "西藏自治区拉萨市"},
    {"id": 4, "name": "西藏自治区人民政府", "type": "政府", "level": "省级",
     "parent": "", "location": "西藏自治区拉萨市"},
    {"id": 5, "name": "全国人大常委会", "type": "人大", "level": "国家级",
     "parent": "", "location": "北京市"},
    {"id": 6, "name": "中共四川省委统战部", "type": "党委", "level": "省级",
     "parent": "中共四川省委员会", "location": "四川省成都市"},
    {"id": 7, "name": "援助西藏发展基金会", "type": "其他", "level": "省级",
     "parent": "", "location": "西藏自治区拉萨市"},
    {"id": 8, "name": "中共那曲市委员会", "type": "党委", "level": "地级",
     "parent": "中共西藏自治区委员会", "location": "西藏自治区那曲市"},
]

positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "昌都市委书记",
     "start": "2024-09", "end": "", "rank": "正厅级",
     "note": "2024年9月13日任昌都市委书记"},
    {"id": 2, "person_id": 1, "org_id": 8, "title": "那曲市委书记",
     "start": "2021-09", "end": "2024-09", "rank": "正厅级", "note": ""},
    {"id": 3, "person_id": 1, "org_id": 4, "title": "自治区驻成都办事处党组书记、副主任",
     "start": "2020-06", "end": "2021-09", "rank": "正厅级", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 4, "title": "自治区驻成都办事处党委书记、副主任",
     "start": "2018-09", "end": "2020-06", "rank": "正厅级", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 4, "title": "自治区驻成都办事处党委副书记、主任",
     "start": "2012-12", "end": "2018-09", "rank": "正厅级", "note": ""},
    {"id": 6, "person_id": 1, "org_id": 3, "title": "西藏自治区党委宣传部副部长",
     "start": "2007-09", "end": "2012-12", "rank": "副厅级", "note": ""},
    {"id": 7, "person_id": 1, "org_id": 3, "title": "自治区党委宣传部新闻出版处处长",
     "start": "2003-06", "end": "2007-09", "rank": "正处级", "note": ""},
    {"id": 8, "person_id": 2, "org_id": 3, "title": "西藏自治区党委常委、秘书长",
     "start": "2024-07", "end": "", "rank": "副省级", "note": ""},
    {"id": 9, "person_id": 2, "org_id": 4, "title": "西藏自治区人民政府副主席",
     "start": "2023-01", "end": "2024-07", "rank": "副省级",
     "note": "兼任昌都市委书记"},
    {"id": 10, "person_id": 2, "org_id": 1, "title": "昌都市委书记",
     "start": "2022-04", "end": "2024-07", "rank": "正厅级", "note": ""},
    {"id": 11, "person_id": 2, "org_id": 3, "title": "西藏自治区纪委副书记、监委副主任",
     "start": "2018-01", "end": "2022-04", "rank": "正厅级", "note": "纪委出身"},
    {"id": 12, "person_id": 3, "org_id": 6, "title": "四川省委常委、统战部部长",
     "start": "2025-01", "end": "", "rank": "副省级", "note": "跨省交流至四川"},
    {"id": 13, "person_id": 3, "org_id": 1, "title": "昌都市委书记",
     "start": "2020-12", "end": "2022-04", "rank": "正厅级",
     "note": "同时兼任自治区政府副主席、后升自治区党委常委"},
    {"id": 14, "person_id": 4, "org_id": 7, "title": "援助西藏发展基金会副理事长兼秘书长",
     "start": "2023-10", "end": "", "rank": "正厅级", "note": "半退休状态"},
    {"id": 15, "person_id": 4, "org_id": 1, "title": "昌都市委书记（含地委书记时期）",
     "start": "2011-11", "end": "2017-04", "rank": "正厅级",
     "note": "2014年经历昌都地区改市"},
    {"id": 16, "person_id": 5, "org_id": 2, "title": "昌都市委副书记、市长",
     "start": "2022-11", "end": "", "rank": "正厅级", "note": ""},
    {"id": 17, "person_id": 6, "org_id": 5, "title": "全国人大常委会副委员长",
     "start": "2023-03", "end": "", "rank": "副国级", "note": "昌都察雅人，现任"},
    {"id": 18, "person_id": 7, "org_id": 5, "title": "全国人大常委会副委员长",
     "start": "2013-03", "end": "2023-03", "rank": "副国级", "note": "昌都丁青人，已退休"},
    {"id": 19, "person_id": 8, "org_id": 5, "title": "全国人大常委会副委员长",
     "start": "2008-03", "end": "2013-03", "rank": "副国级", "note": "昌都人，已退休"},
]

relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "succession",
     "context": "庄劲松接替龚会才任昌都市委书记", "overlap_org": "昌都市委",
     "overlap_period": "2024-09"},
    {"id": 2, "person_a": 2, "person_b": 3, "type": "succession",
     "context": "龚会才接替普布顿珠任昌都市委书记", "overlap_org": "昌都市委",
     "overlap_period": "2022-04"},
    {"id": 3, "person_a": 6, "person_b": 7, "type": "hometown",
     "context": "同为昌都籍全国人大常委会副委员长", "overlap_org": "全国人大常委会",
     "overlap_period": ""},
    {"id": 4, "person_a": 7, "person_b": 8, "type": "hometown",
     "context": "同为昌都籍全国人大常委会副委员长", "overlap_org": "全国人大常委会",
     "overlap_period": ""},
]

# ── BUILD ──
def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)
    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"],
                   o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"],
                   pos["title"], pos["start"], pos["end"],
                   pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"],
                   r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"Created database: {DB_PATH}")

def create_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    person_node_id = {p["id"]: f"changdu_{p['name']}" for p in persons}

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # nodes
    lines.append('    <nodes>')
    for p in persons:
        nid = person_node_id[p["id"]]
        label = f"{p['name']}\n{p['current_post']}"
        # color by role
        if "书记" in p["current_post"]:
            r, g, b = 220, 50, 50
        elif "市长" in p["current_post"]:
            r, g, b = 50, 100, 220
        elif "副委员长" in p["current_post"]:
            r, g, b = 200, 150, 30
        else:
            r, g, b = 150, 150, 150
        lines.append(f'      <node id="{nid}" label="{label}">')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="20.0"/>')
        lines.append(f'      </node>')

    for o in organizations:
        nid = f"org_{o['id']}"
        label = o["name"]
        if "党委" in o["type"] or "委员会" in o["name"]:
            r, g, b = 180, 50, 50
        elif "政府" in o["type"]:
            r, g, b = 50, 80, 180
        elif "人大" in o["type"]:
            r, g, b = 180, 180, 50
        else:
            r, g, b = 150, 150, 150
        lines.append(f'      <node id="{nid}" label="{label}">')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="10.0"/>')
        lines.append(f'      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        src = person_node_id[pos["person_id"]]
        tgt = f"org_{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{pos["title"]}"/>')
    for r in relationships:
        eid += 1
        src = person_node_id[r["person_a"]]
        tgt = person_node_id[r["person_b"]]
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="r["type"]"/>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Created GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    create_database()
    create_gexf()
    print(f"Done. {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
