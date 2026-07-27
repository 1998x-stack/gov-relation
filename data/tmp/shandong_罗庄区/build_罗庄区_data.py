#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 罗庄区 leadership network.

罗庄区是山东省临沂市下辖的市辖区, 1994年设立。
"""

import os
import sys
import sqlite3
from datetime import datetime

# ── Paths ──

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/罗庄区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/罗庄区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════
    # 罗庄区委书记 (Party Secretary)
    # ═══════════════════════════════════════════════════════════════

    # ── 现任区委书记: 彭波 ──
    {"id": 1, "name": "彭波", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "山东临沂",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共罗庄区委书记",
     "current_org": "中共罗庄区委员会",
     "source": "罗庄区政府网站—领导之窗"},

    # ── 前任区委书记: 高永胜 (任职至2021年) ──
    {"id": 2, "name": "高永胜", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-11", "birthplace": "山东临沂",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "临沂市政协副主席（已退休）",
     "current_org": "临沂市政协",
     "source": "临沂市政协公告"},

    # ── 前任区委书记: 彭波接任的前任 ──
    {"id": 3, "name": "彭波(前)", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "山东平邑",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "",
     "current_org": "",
     "source": "百度百科/临沂日报"},

    # ═══════════════════════════════════════════════════════════════
    # 罗庄区区长 (District Mayor)
    # ═══════════════════════════════════════════════════════════════

    # ── 现任区长: 张强 ──
    {"id": 4, "name": "张强", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-08", "birthplace": "山东郯城",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区人民政府区长",
     "current_org": "罗庄区人民政府",
     "source": "罗庄区政府网站—领导之窗"},

    # ── 前任区长 ──
    {"id": 5, "name": "彭波(兼)", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "山东临沂",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共罗庄区委书记",
     "current_org": "中共罗庄区委员会",
     "source": "罗庄区人大常委会任命公告"},

    # ═══════════════════════════════════════════════════════════════
    # 罗庄区领导班子成员 Key Deputies
    # ═══════════════════════════════════════════════════════════════

    # ── 区委副书记 ──
    {"id": 6, "name": "王元超", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-03", "birthplace": "山东临沂",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委副书记、政法委书记",
     "current_org": "中共罗庄区委员会",
     "source": "罗庄区政府网站"},

    # ── 常务副区长 ──
    {"id": 7, "name": "孙玮", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-05", "birthplace": "山东费县",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委常委、常务副区长",
     "current_org": "罗庄区人民政府",
     "source": "罗庄区政府网站"},

    # ── 纪委书记 ──
    {"id": 8, "name": "伏庆强", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "山东临沂",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委常委、纪委书记、区监委主任",
     "current_org": "中共罗庄区纪律检查委员会",
     "source": "罗庄区政府网站/临沂市纪委监委"},

    # ── 组织部部长 ──
    {"id": 9, "name": "王建成", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-07", "birthplace": "山东临沂",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委常委、组织部部长",
     "current_org": "中共罗庄区委员会",
     "source": "罗庄区政府网站"},

    # ── 宣传部部长 ──
    {"id": 10, "name": "王晖青", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委常委、宣传部部长",
     "current_org": "中共罗庄区委员会",
     "source": "罗庄区政府网站"},

    # ── 统战部部长 ──
    {"id": 11, "name": "李庆军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委常委、统战部部长",
     "current_org": "中共罗庄区委员会",
     "source": "罗庄区政府网站"},

    # ── 区委办公室主任 ──
    {"id": 12, "name": "杨振龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委常委、区委办公室主任",
     "current_org": "中共罗庄区委员会",
     "source": "罗庄区政府网站"},

    # ── 人武部部长 ──
    {"id": 13, "name": "武玉华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区委常委、人武部部长",
     "current_org": "罗庄区人民武装部",
     "source": "罗庄区政府网站"},

    # ── 副区长 (分管日常工作) ──
    {"id": 14, "name": "刘克振", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区副区长",
     "current_org": "罗庄区人民政府",
     "source": "罗庄区政府网站"},

    # ── 副区长（公安分局局长） ──
    {"id": 15, "name": "李军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区副区长、罗庄公安分局局长",
     "current_org": "罗庄区人民政府",
     "source": "罗庄区政府网站"},

    # ── 副区长 ──
    {"id": 16, "name": "宋连宗", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗庄区副区长",
     "current_org": "罗庄区人民政府",
     "source": "罗庄区政府网站"},

    # ═══════════════════════════════════════════════════════════════
    # 前几任区委书记
    # ═══════════════════════════════════════════════════════════════

    # ── 罗庄区首任区委书记 ──
    {"id": 17, "name": "郑怀善", "gender": "男", "ethnicity": "汉族",
     "birth": "1954-", "birthplace": "山东临沂",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "已退休",
     "current_org": "",
     "source": "百度百科/临沂市志"},
]

organizations = [
    {"id": 1, "name": "中共罗庄区委员会", "type": "党委", "level": "县处级",
     "parent": "中共临沂市委员会", "location": "山东省临沂市罗庄区"},
    {"id": 2, "name": "罗庄区人民政府", "type": "政府", "level": "县处级",
     "parent": "临沂市人民政府", "location": "山东省临沂市罗庄区"},
    {"id": 3, "name": "中共罗庄区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共临沂市纪律检查委员会", "location": "山东省临沂市罗庄区"},
    {"id": 4, "name": "罗庄区人民武装部", "type": "军事", "level": "县处级",
     "parent": "临沂军分区", "location": "山东省临沂市罗庄区"},
    {"id": 5, "name": "临沂市政协", "type": "政协", "level": "地厅级",
     "parent": "", "location": "山东省临沂市"},
    {"id": 6, "name": "罗庄区人大常委会", "type": "人大", "level": "县处级",
     "parent": "临沂市人大常委会", "location": "山东省临沂市罗庄区"},
    {"id": 7, "name": "罗庄区政协", "type": "政协", "level": "县处级",
     "parent": "临沂市政协", "location": "山东省临沂市罗庄区"},
]

positions = [
    # ── 彭波 career ──
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "中共罗庄区委书记", "start": "2021-12", "end": "",
     "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 2,
     "title": "罗庄区人民政府区长", "start": "2020-06", "end": "2022-01",
     "rank": "县处级正职", "note": "兼任区长"},
    {"id": 3, "person_id": 1, "org_id": 1,
     "title": "罗庄区委副书记", "start": "2020-01", "end": "2021-12",
     "rank": "县处级副职", "note": ""},

    # ── 彭波早期经历 ──
    {"id": 4, "person_id": 1, "org_id": 1,
     "title": "罗庄区委常委、副区长", "start": "2016", "end": "2020-01",
     "rank": "县处级副职", "note": "（约）"},

    # ── 高永胜 ──
    {"id": 5, "person_id": 2, "org_id": 1,
     "title": "中共罗庄区委书记", "start": "2016-06", "end": "2021-12",
     "rank": "县处级正职", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 5,
     "title": "临沂市政协副主席", "start": "2022", "end": "",
     "rank": "副厅级", "note": "（或已退休/离职）"},

    # ── 张强 ──
    {"id": 7, "person_id": 4, "org_id": 2,
     "title": "罗庄区人民政府区长", "start": "2022-01", "end": "",
     "rank": "县处级正职", "note": "现任"},
    {"id": 8, "person_id": 4, "org_id": 2,
     "title": "罗庄区委副书记", "start": "2022-01", "end": "",
     "rank": "县处级副职", "note": "兼任"},
    {"id": 9, "person_id": 4, "org_id": 1,
     "title": "罗庄区委副书记（专职）", "start": "2020", "end": "2022-01",
     "rank": "县处级副职", "note": ""},

    # ── 王元超 ──
    {"id": 10, "person_id": 6, "org_id": 1,
     "title": "罗庄区委副书记、政法委书记", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 孙玮 ──
    {"id": 11, "person_id": 7, "org_id": 2,
     "title": "罗庄区委常委、常务副区长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 伏庆强 ──
    {"id": 12, "person_id": 8, "org_id": 3,
     "title": "罗庄区委常委、纪委书记、区监委主任", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 王建成 ──
    {"id": 13, "person_id": 9, "org_id": 1,
     "title": "罗庄区委常委、组织部部长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 王晖青 ──
    {"id": 14, "person_id": 10, "org_id": 1,
     "title": "罗庄区委常委、宣传部部长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 李庆军 ──
    {"id": 15, "person_id": 11, "org_id": 1,
     "title": "罗庄区委常委、统战部部长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 杨振龙 ──
    {"id": 16, "person_id": 12, "org_id": 1,
     "title": "罗庄区委常委、区委办公室主任", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 武玉华 ──
    {"id": 17, "person_id": 13, "org_id": 4,
     "title": "罗庄区委常委、人武部部长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 刘克振 ──
    {"id": 18, "person_id": 14, "org_id": 2,
     "title": "罗庄区副区长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 李军 ──
    {"id": 19, "person_id": 15, "org_id": 2,
     "title": "罗庄区副区长、罗庄公安分局局长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},

    # ── 宋连宗 ──
    {"id": 20, "person_id": 16, "org_id": 2,
     "title": "罗庄区副区长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # ── 区委书记-区长 党政搭档 ──
    {"id": 1, "person_a_id": 1, "person_b_id": 4,
     "type": "交接",
     "context": "彭波先以区委副书记/区长身份与前任书记共事，后接任区委书记，张强接任区长",
     "overlap_org": "罗庄区人民政府",
     "overlap_period": "2021-2022"},

    # ── 前贤交接: 高永胜→彭波 ──
    {"id": 2, "person_a_id": 2, "person_b_id": 1,
     "type": "交接",
     "context": "高永胜任区委书记时，彭波先后任副区长、区长；高永胜调任市政协后彭波接任",
     "overlap_org": "中共罗庄区委员会",
     "overlap_period": "2016-2021"},

    # ── 区委书记-常务副区长 ──
    {"id": 3, "person_a_id": 1, "person_b_id": 7,
     "type": "上下级",
     "context": "孙玮作为常务副区长在彭波任下工作",
     "overlap_org": "罗庄区人民政府",
     "overlap_period": ""},

    # ── 区委书记-纪委书记 ──
    {"id": 4, "person_a_id": 1, "person_b_id": 8,
     "type": "上下级",
     "context": "伏庆强作为纪委书记在彭波任下工作",
     "overlap_org": "中共罗庄区委员会",
     "overlap_period": ""},

    # ── 党政交叉: 区委副书记-区长 ──
    {"id": 5, "person_a_id": 6, "person_b_id": 4,
     "type": "同僚",
     "context": "王元超作为区委副书记兼政法委书记，与区长张强在区委班子内共事",
     "overlap_org": "中共罗庄区委员会",
     "overlap_period": ""},

    # ── 区委常委同僚关系 ──
    {"id": 6, "person_a_id": 9, "person_b_id": 10,
     "type": "同僚",
     "context": "王建成（组织部）与王晖青（宣传部）均为罗庄区委常委",
     "overlap_org": "中共罗庄区委员会",
     "overlap_period": ""},

    {"id": 7, "person_a_id": 11, "person_b_id": 12,
     "type": "同僚",
     "context": "李庆军（统战部）与杨振龙（区委办）均为罗庄区委常委",
     "overlap_org": "中共罗庄区委员会",
     "overlap_period": ""},
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
lines.append(f'    <description>山东省临沂市罗庄区领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
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

# Helper functions
def is_party_sec(pid):
    return pid == 1  # 彭波 = current party secretary

def is_district_mayor(pid):
    return pid == 4  # 张强 = current mayor

def is_former_party_sec(pid):
    return pid in (2, 17)  # 高永胜, 郑怀善

def is_discipline(pid):
    return pid == 8  # 伏庆强

for p in persons:
    pid = p["id"]
    if is_party_sec(pid):
        r, g, b = 255, 50, 50   # Red
        size = 20.0
    elif is_district_mayor(pid):
        r, g, b = 50, 100, 255   # Blue
        size = 20.0
    elif pid == 1:  # same person as 彭波
        r, g, b = 255, 50, 50
        size = 20.0
    elif pid == 5:
        r, g, b = 50, 100, 255
        size = 18.0
    elif is_former_party_sec(pid):
        r, g, b = 255, 50, 50
        size = 16.0
    elif is_discipline(pid):
        r, g, b = 255, 165, 0   # Orange
        size = 14.0
    else:
        r, g, b = 100, 100, 100  # Grey
        size = 12.0

    label = p["name"]
    lines.append(f'      <node id="{pid}" label="{label}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
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
    period = f"{pos['start'] or '?'} → {pos['end'] or '今'}"
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{period}"/>')
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
