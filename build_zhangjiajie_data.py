#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 张家界市 leadership network."""

import sqlite3
import os

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/zhangjiajie_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/zhangjiajie_network.gexf")

# ── DATA ──

persons = [
    # ── City-level leaders ──
    {"id": 1, "name": "贺辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-09", "birthplace": "湖南益阳", "education": "博士研究生（湘潭大学）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委书记", "current_org": "中共张家界市委员会",
     "source": "http://www.zjj.gov.cn/c13785/20260615/i1162786.html"},
    {"id": 2, "name": "陈澎", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-04", "birthplace": "湖南湘乡", "education": "在职研究生，法学博士（湘潭大学）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委副书记、代市长", "current_org": "张家界市人民政府",
     "source": "http://www.zjj.gov.cn/c13786/20260615/i1162787.html"},
    {"id": 3, "name": "田华玉", "gender": "女", "ethnicity": "土家族",
     "birth": "1973-05", "birthplace": "湖南慈利", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市人大常委会主任", "current_org": "张家界市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%AE%B6%E7%95%8C%E5%B8%82"},
    {"id": 4, "name": "杨广林", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-08", "birthplace": "湖南永州", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市政协主席", "current_org": "张家界市政协",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%AE%B6%E7%95%8C%E5%B8%82"},
    # ── City Party Standing Committee ──
    {"id": 5, "name": "王令波", "gender": "女", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "", "education": "湖南师范大学汉语言文学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、市纪委书记", "current_org": "中共张家界市纪律检查委员会",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162790.html"},
    {"id": 6, "name": "廖国豪", "gender": "男", "ethnicity": "",
     "birth": "1973-04", "birthplace": "", "education": "大学，法学学士，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、组织部部长", "current_org": "中共张家界市委组织部",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162791.html"},
    {"id": 7, "name": "贺建壬", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-06", "birthplace": "", "education": "在职研究生，管理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、市委秘书长", "current_org": "中共张家界市委办公室",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162792.html"},
    {"id": 8, "name": "吴文海", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-05", "birthplace": "", "education": "外交学院国际法专业，法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、宣传部部长", "current_org": "中共张家界市委宣传部",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162793.html"},
    {"id": 9, "name": "林宏生", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-09", "birthplace": "", "education": "研究生，军事学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、军分区司令员", "current_org": "张家界军分区",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162794.html"},
    {"id": 10, "name": "赵云海", "gender": "男", "ethnicity": "土家族",
     "birth": "1974-09", "birthplace": "湖南桑植（推测）", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、统战部部长", "current_org": "中共张家界市委统战部",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162795.html"},
    {"id": 11, "name": "崔晓", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-02", "birthplace": "", "education": "硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、常务副市长", "current_org": "张家界市人民政府",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162796.html"},
    {"id": 12, "name": "马碧", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-02", "birthplace": "", "education": "研究生，文学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家界市委常委、副市长", "current_org": "张家界市人民政府",
     "source": "http://www.zjj.gov.cn/c13787/20260615/i1162797.html"},
    # ── District/county leaders ──
    {"id": 13, "name": "张喜松", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永定区委书记", "current_org": "中共张家界市永定区委员会",
     "source": "http://www.zjjyd.gov.cn/c4861/20260629/i1165569.html"},
    {"id": 14, "name": "刘梦融", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永定区委副书记、代区长", "current_org": "永定区人民政府",
     "source": "http://www.zjjyd.gov.cn/c4861/20260629/i1165569.html"},
    {"id": 15, "name": "钟跃波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武陵源区委书记、张管局党委书记", "current_org": "中共张家界市武陵源区委员会",
     "source": "https://www.wlynews.cn/content/646041/98/16061144.html"},
    {"id": 16, "name": "代劲", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武陵源区委副书记、代理区长", "current_org": "武陵源区人民政府",
     "source": "https://www.wlynews.cn/content/646041/58/16082590.html"},
    {"id": 17, "name": "侯毅", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "慈利县委书记", "current_org": "中共慈利县委员会",
     "source": "http://www.cili.gov.cn/c3378/20260707/i1167132.html"},
    {"id": 18, "name": "姜华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "慈利县委副书记、代县长", "current_org": "慈利县人民政府",
     "source": "http://www.cili.gov.cn/c3378/20260714/i1168455.html"},
    {"id": 19, "name": "黄瑛", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桑植县委书记", "current_org": "中共桑植县委员会",
     "source": "http://www.sangzhi.gov.cn/c2370/20260701/i1166292.html"},
    {"id": 20, "name": "张冲", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桑植县委副书记、代县长", "current_org": "桑植县人民政府",
     "source": "http://www.sangzhi.gov.cn/c2370/20260713/i1168290.html"},
    # ── Predecessors ──
    {"id": 21, "name": "刘革安", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委统战部（原张家界市委书记）", "current_org": "湖南省委统战部",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%AE%B6%E7%95%8C%E5%B8%82"},
    {"id": 22, "name": "王洪斌", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "已卸任张家界市长（2025.09）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%AE%B6%E7%95%8C%E5%B8%82"},
    {"id": 23, "name": "虢正贵", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湘西土家族苗族自治州州委书记", "current_org": "中共湘西州委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%AE%B6%E7%95%8C%E5%B8%82"},
]

organizations = [
    {"id": 1, "name": "中共张家界市委员会", "type": "party_committee", "level": "prefecture", "parent": "中共湖南省委", "location": "张家界市"},
    {"id": 2, "name": "张家界市人民政府", "type": "government", "level": "prefecture", "parent": "湖南省人民政府", "location": "张家界市"},
    {"id": 3, "name": "张家界市人大常委会", "type": "npc", "level": "prefecture", "parent": "湖南省人大常委会", "location": "张家界市"},
    {"id": 4, "name": "张家界市政协", "type": "cppcc", "level": "prefecture", "parent": "湖南省政协", "location": "张家界市"},
    {"id": 5, "name": "中共张家界市纪律检查委员会", "type": "discipline", "level": "prefecture", "parent": "中共张家界市委员会", "location": "张家界市"},
    {"id": 6, "name": "中共张家界市委组织部", "type": "party_dept", "level": "prefecture", "parent": "中共张家界市委员会", "location": "张家界市"},
    {"id": 7, "name": "中共张家界市委宣传部", "type": "party_dept", "level": "prefecture", "parent": "中共张家界市委员会", "location": "张家界市"},
    {"id": 8, "name": "中共张家界市委统战部", "type": "party_dept", "level": "prefecture", "parent": "中共张家界市委员会", "location": "张家界市"},
    {"id": 9, "name": "中共张家界市委办公室", "type": "party_dept", "level": "prefecture", "parent": "中共张家界市委员会", "location": "张家界市"},
    {"id": 10, "name": "张家界军分区", "type": "military", "level": "prefecture", "parent": "", "location": "张家界市"},
    {"id": 11, "name": "中共张家界市永定区委员会", "type": "party_committee", "level": "district", "parent": "中共张家界市委员会", "location": "永定区"},
    {"id": 12, "name": "永定区人民政府", "type": "government", "level": "district", "parent": "张家界市人民政府", "location": "永定区"},
    {"id": 13, "name": "中共张家界市武陵源区委员会", "type": "party_committee", "level": "district", "parent": "中共张家界市委员会", "location": "武陵源区"},
    {"id": 14, "name": "武陵源区人民政府", "type": "government", "level": "district", "parent": "张家界市人民政府", "location": "武陵源区"},
    {"id": 15, "name": "中共慈利县委员会", "type": "party_committee", "level": "county", "parent": "中共张家界市委员会", "location": "慈利县"},
    {"id": 16, "name": "慈利县人民政府", "type": "government", "level": "county", "parent": "张家界市人民政府", "location": "慈利县"},
    {"id": 17, "name": "中共桑植县委员会", "type": "party_committee", "level": "county", "parent": "中共张家界市委员会", "location": "桑植县"},
    {"id": 18, "name": "桑植县人民政府", "type": "government", "level": "county", "parent": "张家界市人民政府", "location": "桑植县"},
    {"id": 19, "name": "湖南省委统战部", "type": "party_dept", "level": "province", "parent": "中共湖南省委", "location": "长沙市"},
    {"id": 20, "name": "中共湘西州委员会", "type": "party_committee", "level": "prefecture", "parent": "中共湖南省委", "location": "湘西州"},
]

positions = [
    # City-level party
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2026-06", "end": "", "rank": "正厅级", "note": ""},
    # City-level government
    {"person_id": 2, "org_id": 2, "title": "市委副书记、代市长、党组书记", "start": "2026-04", "end": "", "rank": "正厅级", "note": "代理市长，尚未转正"},
    # NPC & CPPCC
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "2022-01", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "2023-12", "end": "", "rank": "正厅级", "note": ""},
    # Standing Committee members
    {"person_id": 5, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start": "2021", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "市委常委、组织部部长", "start": "2021", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "市委常委、市委秘书长", "start": "2024-05", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "市委常委、宣传部部长", "start": "2022", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 10, "title": "市委常委、军分区司令员", "start": "2025-03", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "市委常委、统战部部长", "start": "2022-01", "end": "", "rank": "副厅级", "note": "土家族"},
    {"person_id": 11, "org_id": 2, "title": "市委常委、常务副市长", "start": "2026-06", "end": "", "rank": "副厅级", "note": "最年轻常委（1982年生）"},
    {"person_id": 12, "org_id": 2, "title": "市委常委、副市长", "start": "2026-03", "end": "", "rank": "副厅级", "note": ""},
    # District/county level
    {"person_id": 13, "org_id": 11, "title": "永定区委书记", "start": "2024", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 12, "title": "永定区委副书记、代区长", "start": "2026", "end": "", "rank": "正处级", "note": "代区长"},
    {"person_id": 15, "org_id": 13, "title": "武陵源区委书记、张管局党委书记", "start": "2026", "end": "", "rank": "正处级", "note": "原任区长升书记"},
    {"person_id": 16, "org_id": 14, "title": "武陵源区委副书记、代理区长", "start": "2026-07", "end": "", "rank": "正处级", "note": "新任代理区长"},
    {"person_id": 17, "org_id": 15, "title": "慈利县委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 16, "title": "慈利县委副书记、代县长", "start": "2026", "end": "", "rank": "正处级", "note": "代县长"},
    {"person_id": 19, "org_id": 17, "title": "桑植县委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 18, "title": "桑植县委副书记、代县长", "start": "2026", "end": "", "rank": "正处级", "note": "代县长"},
    # Predecessors
    {"person_id": 21, "org_id": 1, "title": "原市委书记（2021.03-2026.06）", "start": "2021-03", "end": "2026-06", "rank": "正厅级", "note": "调任湖南省委统战部"},
    {"person_id": 21, "org_id": 19, "title": "省委统战部（新职）", "start": "2026-06", "end": "", "rank": "正厅级", "note": "调任"},
    {"person_id": 22, "org_id": 2, "title": "原市长（2021.04-2025.09）", "start": "2021-04", "end": "2025-09", "rank": "正厅级", "note": "卸任，去向待核实"},
    {"person_id": 23, "org_id": 1, "title": "原市委书记（2016.12-2021.03）", "start": "2016-12", "end": "2021-03", "rank": "正厅级", "note": ""},
    {"person_id": 23, "org_id": 20, "title": "湘西州委书记", "start": "2021-03", "end": "", "rank": "正厅级", "note": "调任湘西州"},
]

relationships = [
    # Leadership pair
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "贺辉（书记）+ 陈澎（代市长），2026年4月起搭档", "overlap_org": "中共张家界市委员会/张家界市人民政府", "overlap_period": "2026-04至今"},
    # Predecessor-successor
    {"person_a": 21, "person_b": 1, "type": "前后任", "context": "刘革安是贺辉的前任市委书记", "overlap_org": "中共张家界市委员会", "overlap_period": "2026-06交接"},
    {"person_a": 22, "person_b": 2, "type": "前后任", "context": "王洪斌是陈澎的前任市长", "overlap_org": "张家界市人民政府", "overlap_period": "2025-09/2026-04交接"},
    {"person_a": 23, "person_b": 21, "type": "前后任", "context": "虢正贵是刘革安的前任市委书记", "overlap_org": "中共张家界市委员会", "overlap_period": "2021-03交接"},
    # Standing Committee colleagues (working together currently)
    {"person_a": 1, "person_b": 5, "type": "班子成员", "context": "书记与纪委书记，市委常委会同僚", "overlap_org": "中共张家界市委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 6, "type": "班子成员", "context": "书记与组织部长", "overlap_org": "中共张家界市委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 10, "type": "班子成员", "context": "书记与统战部长（赵云海系桑植出身）", "overlap_org": "中共张家界市委员会", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 11, "type": "班子成员", "context": "代市长与常务副市长（崔晓1982年生，最年轻）", "overlap_org": "张家界市人民政府", "overlap_period": "2026-06至今"},
    # County-level: 赵云海 was from 桑植县
    {"person_a": 10, "person_b": 19, "type": "桑植渊源", "context": "赵云海曾任桑植县长，黄瑛现任桑植县委书记", "overlap_org": "桑植县", "overlap_period": "推测"},
    {"person_a": 10, "person_b": 20, "type": "桑植渊源", "context": "赵云海曾任桑植县长，张冲现任桑植代县长", "overlap_org": "桑植县", "overlap_period": "推测"},
]


# ── BUILD DATABASE ──

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions
        (person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?)""",
        (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# ── BUILD GEXF ──

person_rows = cur.execute("SELECT id, name, current_post FROM persons").fetchall()
org_rows = cur.execute("SELECT id, name, type FROM organizations").fetchall()
pos_rows = cur.execute("SELECT person_id, org_id FROM positions").fetchall()
rel_rows = cur.execute("SELECT person_a, person_b, type, context FROM relationships").fetchall()

conn.close()

# Build GEXF using string formatting
parts = []
parts.append('<?xml version="1.0" encoding="UTF-8"?>')
parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
parts.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
parts.append('    <attributes class="node">')
parts.append('      <attribute id="role" title="Role" type="string"/>')
parts.append('      <attribute id="birth" title="Birth" type="string"/>')
parts.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
parts.append('      <attribute id="current_post" title="Current Post" type="string"/>')
parts.append('    </attributes>')
parts.append('    <attributes class="edge">')
parts.append('      <attribute id="type" title="Type" type="string"/>')
parts.append('      <attribute id="context" title="Context" type="string"/>')
parts.append('      <attribute id="start" title="Start" type="string"/>')
parts.append('      <attribute id="end" title="End" type="string"/>')
parts.append('    </attributes>')

# Nodes: persons
parts.append('    <nodes>')
for pid, name, post in person_rows:
    # Determine role & color
    if '书记' in (post or '') and '市委' in (post or ''):
        role = 'party_secretary'
        color = '#E03C31'
        size = 20.0
    elif '市长' in (post or '') or '区长' in (post or '') or '县长' in (post or ''):
        role = 'government'
        color = '#3B82F6'
        size = 20.0 if '代市长' in post or '市委副书记' in post else 16.0
    elif '纪委书记' in (post or '') or '纪检' in (post or ''):
        role = 'discipline'
        color = '#F59E0B'
        size = 14.0
    elif '人大' in (post or ''):
        role = 'npc'
        color = '#10B981'
        size = 14.0
    elif '政协' in (post or ''):
        role = 'cppcc'
        color = '#8B5CF6'
        size = 14.0
    else:
        role = 'other'
        color = '#6B7280'
        size = 14.0
    parts.append(f'      <node id="p{pid}" label="{name}">')
    parts.append(f'        <attvalues>')
    parts.append(f'          <attvalue for="role" value="{role}"/>')
    parts.append(f'          <attvalue for="birth" value=""/>')
    parts.append(f'          <attvalue for="birthplace" value=""/>')
    parts.append(f'          <attvalue for="current_post" value="{post}"/>')
    parts.append(f'        </attvalues>')
    parts.append(f'        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>')
    parts.append(f'        <viz:size value="{size}"/>')
    parts.append(f'        <viz:shape value="disc"/>')
    parts.append(f'      </node>')

# Nodes: organizations
org_color_map = {
    'party_committee': ('#DC2626', 8.0),
    'government': ('#2563EB', 8.0),
    'discipline': ('#D97706', 8.0),
    'party_dept': ('#9333EA', 8.0),
    'npc': ('#059669', 8.0),
    'cppcc': ('#7C3AED', 8.0),
    'military': ('#4B5563', 8.0),
}
for oid, oname, otype in org_rows:
    oc, osize = org_color_map.get(otype, ('#6B7280', 8.0))
    parts.append(f'      <node id="o{oid}" label="{oname}">')
    parts.append(f'        <viz:color r="{int(oc[1:3],16)}" g="{int(oc[3:5],16)}" b="{int(oc[5:7],16)}"/>')
    parts.append(f'        <viz:size value="{osize}"/>')
    parts.append(f'        <viz:shape value="square"/>')
    parts.append(f'      </node>')

parts.append('    </nodes>')

# Edges
edge_id = 0
parts.append('    <edges>')
# person→org edges
for ppid, ooid in pos_rows:
    edge_id += 1
    parts.append(f'      <edge id="e{edge_id}" source="p{ppid}" target="o{ooid}" type="directed">')
    parts.append(f'        <attvalues>')
    parts.append(f'          <attvalue for="type" value="worked_at"/>')
    parts.append(f'          <attvalue for="context" value="任职"/>')
    parts.append(f'          <attvalue for="start" value=""/>')
    parts.append(f'          <attvalue for="end" value=""/>')
    parts.append(f'        </attvalues>')
    parts.append(f'        <viz:color r="156" g="163" b="175"/>')
    parts.append(f'        <viz:thickness value="1.0"/>')
    parts.append(f'      </edge>')
# person↔person edges
for pa, pb, rtype, ctx in rel_rows:
    edge_id += 1
    parts.append(f'      <edge id="e{edge_id}" source="p{pa}" target="p{pb}" type="undirected">')
    parts.append(f'        <attvalues>')
    parts.append(f'          <attvalue for="type" value="{rtype}"/>')
    parts.append(f'          <attvalue for="context" value="{ctx}"/>')
    parts.append(f'          <attvalue for="start" value=""/>')
    parts.append(f'          <attvalue for="end" value=""/>')
    parts.append(f'        </attvalues>')
    thickness = '3.0' if '党政搭档' in rtype or '前后任' in rtype else '1.5'
    parts.append(f'        <viz:color r="212" g="169" b="74"/>')
    parts.append(f'        <viz:thickness value="{thickness}"/>')
    parts.append(f'      </edge>')

parts.append('    </edges>')
parts.append('  </graph>')
parts.append('</gexf>')

with open(GEXF_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(parts))

# ── SUMMARY ──
print(f"✅ Database: {DB_PATH}")
print(f"✅ GEXF graph: {GEXF_PATH}")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")
print(f"   Edges in GEXF: {edge_id}")
