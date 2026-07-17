#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Lushan City (庐山市) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/lushan_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/lushan_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (一把手) ──
    {"id": 1, "name": "邵九思", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "九江市委常委、庐山管理局党委书记、庐山市委书记",
     "current_org": "中共庐山市委",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    # ── Current Mayor (二把手) ──
    {"id": 2, "name": "熊杜明", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山管理局局长、庐山市人民政府市长",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    # ── Deputy Mayor / Executive Deputy (常务副市长) ──
    {"id": 3, "name": "邓剑", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政府副市长、党组副书记",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    # ── Deputy Mayors (副市长) ──
    {"id": 4, "name": "汪新锋", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政府副市长、党组成员",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    {"id": 5, "name": "温战强", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "", "work_start": "",
     "current_post": "庐山市政府副市长",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    {"id": 6, "name": "李爱华", "gender": "女", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "", "work_start": "",
     "current_post": "庐山市政府副市长",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    {"id": 7, "name": "张毅蕾", "gender": "女", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政府副市长、党组成员",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    {"id": 8, "name": "刘永安", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政府副市长、党组成员",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    {"id": 9, "name": "徐智", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政府副市长、党组成员",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    {"id": 10, "name": "束中阳", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政府副市长、党组成员",
     "current_org": "庐山市人民政府",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    # ── Government Office Director ──
    {"id": 11, "name": "李曲波", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政府办公室主任、党组成员",
     "current_org": "庐山市人民政府办公室",
     "source": "https://www.lushan.gov.cn/ (confirmed)"},

    # ── Predecessors (历任领导) ──
    # Previous Party Secretaries (历任市委书记)
    {"id": 12, "name": "李甫勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-09", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "已调离庐山市（履历待查去向）",
     "current_org": "",
     "source": "https://www.lushan.gov.cn/ (inferred from news)"},

    {"id": 13, "name": "孙金淼", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "已调离庐山市（履历待查去向）",
     "current_org": "",
     "source": "https://www.lushan.gov.cn/ (inferred from news)"},

    {"id": 14, "name": "杨健", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "已调离庐山市（履历待查去向）",
     "current_org": "",
     "source": "https://www.lushan.gov.cn/ (inferred from news)"},

    # ── Leader of People's Congress (人大主任) ──
    {"id": 15, "name": "刘英", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市人大常委会主任（推测）",
     "current_org": "庐山市人大常委会",
     "source": "https://www.lushan.gov.cn/ (inferred)"},

    # ── CPPCC Chairman (政协主席) ──
    {"id": 16, "name": "赵木林", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市政协主席（推测）",
     "current_org": "庐山市政协",
     "source": "https://www.lushan.gov.cn/ (inferred)"},

    # ── Discipline Inspection (纪委书记) ──
    {"id": 17, "name": "项飞", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市委常委、市纪委书记（推测）",
     "current_org": "中共庐山市纪律检查委员会",
     "source": "https://www.lushan.gov.cn/ (inferred)"},

    # ── Organization Department Minister (组织部部长) ──
    {"id": 18, "name": "易晓剑", "gender": "男", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市委常委、组织部部长（推测）",
     "current_org": "中共庐山市委组织部",
     "source": "https://www.lushan.gov.cn/ (inferred)"},

    # ── Propaganda Department Minister (宣传部部长) ──
    {"id": 19, "name": "邹菲", "gender": "女", "ethnicity": "汉族",
     "birth": "履历待查", "birthplace": "履历待查", "education": "履历待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山市委常委、宣传部部长（推测）",
     "current_org": "中共庐山市委宣传部",
     "source": "https://www.lushan.gov.cn/ (inferred)"},
]

organizations = [
    {"id": 1, "name": "中共庐山市委", "type": "党委", "level": "县处级", "parent": "中共九江市委", "location": "江西九江庐山"},
    {"id": 2, "name": "庐山市人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江庐山"},
    {"id": 3, "name": "庐山管理局", "type": "景区管理", "level": "正厅级", "parent": "江西省人民政府", "location": "江西九江庐山"},
    {"id": 4, "name": "中共庐山市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共九江市纪律检查委员会", "location": "江西九江庐山"},
    {"id": 5, "name": "中共庐山市委组织部", "type": "党委部门", "level": "县处级", "parent": "中共庐山市委", "location": "江西九江庐山"},
    {"id": 6, "name": "中共庐山市委宣传部", "type": "党委部门", "level": "县处级", "parent": "中共庐山市委", "location": "江西九江庐山"},
    {"id": 7, "name": "庐山市人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "江西九江庐山"},
    {"id": 8, "name": "庐山市政协", "type": "政协", "level": "县处级", "parent": "", "location": "江西九江庐山"},
    {"id": 9, "name": "庐山市人民政府办公室", "type": "政府", "level": "县处级", "parent": "庐山市人民政府", "location": "江西九江庐山"},
    {"id": 10, "name": "中共九江市委", "type": "党委", "level": "厅级", "parent": "中共江西省委", "location": "江西九江"},
    {"id": 11, "name": "九江市人民政府", "type": "政府", "level": "厅级", "parent": "江西省人民政府", "location": "江西九江"},
]

positions = [
    # ── Shao Jiusi (邵九思) ──
    {"id": 1, "person_id": 1, "org_id": 3, "title": "庐山管理局党委书记", "start": "2024?", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 1, "title": "庐山市委书记", "start": "2024?", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 3, "person_id": 1, "org_id": 10, "title": "九江市委常委", "start": "2024?", "end": "", "rank": "副厅级", "note": "现任，高配"},
    # Shao Jiusi previous positions
    {"id": 51, "person_id": 1, "org_id": 11, "title": "九江市政府副市长", "start": "", "end": "", "rank": "副厅级", "note": "前任职务（推测）"},
    {"id": 52, "person_id": 1, "org_id": 10, "title": "九江市委统战部部长", "start": "", "end": "", "rank": "副厅级", "note": "前任职务（推测）"},
    {"id": 53, "person_id": 1, "org_id": 11, "title": "九江市修水县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "前任职务（推测）"},

    # ── Xiong Duming (熊杜明) ──
    {"id": 6, "person_id": 2, "org_id": 2, "title": "庐山市人民政府市长、党组书记", "start": "2025?", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 7, "person_id": 2, "org_id": 3, "title": "庐山管理局局长", "start": "2025?", "end": "", "rank": "副厅级", "note": "现任"},
    # Xiong Duming previous positions
    {"id": 54, "person_id": 2, "org_id": 1, "title": "庐山市委副书记（原任）", "start": "", "end": "", "rank": "县处级副职", "note": "前任职务（推测）"},
    {"id": 55, "person_id": 2, "org_id": 2, "title": "庐山市人民政府常务副市长（原任）", "start": "", "end": "", "rank": "县处级副职", "note": "前任职务（推测）"},

    # ── Deng Jian (邓剑) ──
    {"id": 8, "person_id": 3, "org_id": 2, "title": "庐山市政府副市长、党组副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任，常务副市长"},

    # ── Deputy Mayors ──
    {"id": 9, "person_id": 4, "org_id": 2, "title": "庐山市政府副市长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 5, "org_id": 2, "title": "庐山市政府副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 6, "org_id": 2, "title": "庐山市政府副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 7, "org_id": 2, "title": "庐山市政府副市长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 13, "person_id": 8, "org_id": 2, "title": "庐山市政府副市长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 9, "org_id": 2, "title": "庐山市政府副市长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 15, "person_id": 10, "org_id": 2, "title": "庐山市政府副市长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Li Qubo (李曲波) ──
    {"id": 16, "person_id": 11, "org_id": 9, "title": "庐山市人民政府办公室主任、党组成员", "start": "", "end": "", "rank": "县处级", "note": "现任"},

    # ── Predecessors ──
    {"id": 17, "person_id": 12, "org_id": 1, "title": "庐山市委书记", "start": "2020?", "end": "2024?", "rank": "县处级正职", "note": "前任书记"},
    {"id": 18, "person_id": 13, "org_id": 1, "title": "庐山市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "前任书记"},
    {"id": 19, "person_id": 14, "org_id": 1, "title": "庐山市委书记（首任）", "start": "2016-05", "end": "2018?", "rank": "县处级正职", "note": "首任书记"},

    # ── Committee Members ──
    {"id": 20, "person_id": 15, "org_id": 7, "title": "庐山市人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任（推测）"},
    {"id": 21, "person_id": 16, "org_id": 8, "title": "庐山市政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任（推测）"},
    {"id": 22, "person_id": 17, "org_id": 4, "title": "庐山市委常委、市纪委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任（推测）"},
    {"id": 23, "person_id": 18, "org_id": 5, "title": "庐山市委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（推测）"},
    {"id": 24, "person_id": 19, "org_id": 6, "title": "庐山市委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（推测）"},
]

relationships = [
    # ── Predecessor-Successor (Party Secretaries) ──
    {"id": 1, "person_a_id": 14, "person_b_id": 13, "type": "交接", "context": "杨健→孙金淼 庐山市委书记交接", "overlap_org": "中共庐山市委", "overlap_period": ""},
    {"id": 2, "person_a_id": 13, "person_b_id": 12, "type": "交接", "context": "孙金淼→李甫勇 庐山市委书记交接", "overlap_org": "中共庐山市委", "overlap_period": ""},
    {"id": 3, "person_a_id": 12, "person_b_id": 1, "type": "交接", "context": "李甫勇→邵九思 庐山市委书记交接", "overlap_org": "中共庐山市委", "overlap_period": ""},

    # ── Party Secretary - Mayor (党政搭档) ──
    {"id": 4, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "邵九思任庐山市委书记时，熊杜明任市长", "overlap_org": "中共庐山市委/庐山市人民政府", "overlap_period": "当前"},

    # ─市局合一体制关联
    {"id": 5, "person_a_id": 1, "person_b_id": 2, "type": "管理局搭档", "context": "邵九思任管理局党委书记，熊杜明任管理局局长", "overlap_org": "庐山管理局", "overlap_period": "当前"},

    # ── Deputy Mayor coworkers ──
    {"id": 6, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "邓剑与汪新锋均为副市长", "overlap_org": "庐山市人民政府", "overlap_period": "当前"},
    {"id": 7, "person_a_id": 3, "person_b_id": 8, "type": "同僚", "context": "邓剑与刘永安均为副市长", "overlap_org": "庐山市人民政府", "overlap_period": "当前"},
    {"id": 8, "person_a_id": 4, "person_b_id": 7, "type": "同僚", "context": "汪新锋与张毅蕾互为AB岗", "overlap_org": "庐山市人民政府", "overlap_period": "当前"},
    {"id": 9, "person_a_id": 3, "person_b_id": 9, "type": "同僚", "context": "邓剑与徐智互为AB岗", "overlap_org": "庐山市人民政府", "overlap_period": "当前"},

    # ── Cross-system relationships ──
    {"id": 10, "person_a_id": 1, "person_b_id": 17, "type": "上下级", "context": "邵九思（书记）与项飞（纪委书记）为市委常委同僚", "overlap_org": "中共庐山市委", "overlap_period": "当前"},
    {"id": 11, "person_a_id": 1, "person_b_id": 18, "type": "上下级", "context": "邵九思（书记）与易晓剑（组织部长）为市委常委同僚", "overlap_org": "中共庐山市委", "overlap_period": "当前"},
    {"id": 12, "person_a_id": 1, "person_b_id": 19, "type": "上下级", "context": "邵九思（书记）与邹菲（宣传部长）为市委常委同僚", "overlap_org": "中共庐山市委", "overlap_period": "当前"},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
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

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>庐山市领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    # Color coding: 书记=red, 政府领导=blue, 人大政协=orange, 纪委=orange, 其他=gray
    if p["id"] in [1]:  # Party Secretary
        color = '#E03C31'
        size = 20.0
    elif p["id"] in [2]:  # Mayor
        color = '#2980B9'
        size = 18.0
    elif p["id"] in [3, 4, 5, 6, 7, 8, 9, 10]:  # Government leaders
        color = '#2980B9'
        size = 14.0
    elif p["id"] in [11]:  # Office Director
        color = '#2980B9'
        size = 12.0
    elif p["id"] in [12, 13, 14]:  # Predecessors (mix of party/gov)
        color = '#8E44AD'
        size = 14.0
    elif p["id"] in [15, 16]:  # 人大政协
        color = '#E67E22'
        size = 14.0
    elif p["id"] in [17]:  # 纪委
        color = '#E67E22'
        size = 14.0
    else:
        color = '#95A5A6'
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
