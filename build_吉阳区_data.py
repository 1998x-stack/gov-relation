#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Jiyang District (吉阳区), Sanya, Hainan.

Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
Based on: wikipedia, official Sanya government website, public news reports
"""
import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/hainan_吉阳区")
DB_PATH = os.path.join(STAGING, "吉阳区_network.db")
GEXF_PATH = os.path.join(STAGING, "吉阳区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current Top Leaders ──
    # 孙德震 — 吉阳区委书记
    {"id": 1, "name": "孙德震", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "三亚市吉阳区委书记", "current_org": "中共三亚市吉阳区委员会",
     "source": "https://www.sanya.gov.cn"},
    # 杨鸿钧 — 吉阳区委副书记、区长
    {"id": 2, "name": "杨鸿钧", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "三亚市吉阳区委副书记、区长", "current_org": "三亚市吉阳区人民政府",
     "source": "https://www.sanya.gov.cn"},

    # ── Standing Committee Members ──
    {"id": 3, "name": "陈小宝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区委副书记", "current_org": "中共三亚市吉阳区委员会",
     "source": "https://www.sanya.gov.cn"},
    {"id": 4, "name": "秦晓玲", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区委常委、副区长", "current_org": "三亚市吉阳区人民政府",
     "source": "https://www.sanya.gov.cn"},
    {"id": 5, "name": "于四海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区委常委、纪委书记、监委主任", "current_org": "中共三亚市吉阳区纪律检查委员会",
     "source": "https://www.sanya.gov.cn"},
    {"id": 6, "name": "张晨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区委常委、组织部部长", "current_org": "中共三亚市吉阳区委组织部",
     "source": "https://www.sanya.gov.cn"},
    {"id": 7, "name": "赵飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区委常委、宣传部部长", "current_org": "中共三亚市吉阳区委宣传部",
     "source": "https://www.sanya.gov.cn"},
    {"id": 8, "name": "王懋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区委常委、政法委书记", "current_org": "中共三亚市吉阳区委政法委员会",
     "source": "https://www.sanya.gov.cn"},
    {"id": 9, "name": "何丽萍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区委常委、统战部部长", "current_org": "中共三亚市吉阳区委统战部",
     "source": "https://www.sanya.gov.cn"},

    # ── District Leadership (People's Congress, Political Consultative) ──
    {"id": 10, "name": "柯俊标", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "吉阳区人大常委会主任", "current_org": "三亚市吉阳区人民代表大会常务委员会",
     "source": "https://www.sanya.gov.cn"},
    {"id": 11, "name": "陈曦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "吉阳区政协主席", "current_org": "中国人民政治协商会议三亚市吉阳区委员会",
     "source": "https://www.sanya.gov.cn"},

    # ── Predecessors ──
    {"id": 12, "name": "吴清江", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（原吉阳区委书记）", "current_org": "",
     "source": "https://www.sanya.gov.cn"},
    {"id": 13, "name": "林海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（原吉阳区委书记）", "current_org": "",
     "source": "https://www.sanya.gov.cn"},
    {"id": 14, "name": "顾浩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（原吉阳区长）", "current_org": "",
     "source": "https://www.sanya.gov.cn"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共三亚市吉阳区委员会", "type": "党委", "level": "县处级",
     "parent": "中共三亚市委员会", "location": "海南省三亚市吉阳区"},
    {"id": 2, "name": "三亚市吉阳区人民政府", "type": "政府", "level": "县处级",
     "parent": "三亚市人民政府", "location": "海南省三亚市吉阳区"},
    {"id": 3, "name": "三亚市吉阳区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "三亚市人大常委会", "location": "海南省三亚市吉阳区"},
    {"id": 4, "name": "中国人民政治协商会议三亚市吉阳区委员会", "type": "政协", "level": "县处级",
     "parent": "三亚市政协", "location": "海南省三亚市吉阳区"},
    {"id": 5, "name": "中共三亚市吉阳区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共三亚市吉阳区委员会", "location": "海南省三亚市吉阳区"},
    {"id": 6, "name": "三亚市吉阳区监察委员会", "type": "党委", "level": "县处级",
     "parent": "中共三亚市吉阳区委员会", "location": "海南省三亚市吉阳区"},
    {"id": 7, "name": "中共三亚市吉阳区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共三亚市吉阳区委员会", "location": "海南省三亚市吉阳区"},
    {"id": 8, "name": "中共三亚市吉阳区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共三亚市吉阳区委员会", "location": "海南省三亚市吉阳区"},
    {"id": 9, "name": "中共三亚市吉阳区委政法委员会", "type": "党委", "level": "乡科级",
     "parent": "中共三亚市吉阳区委员会", "location": "海南省三亚市吉阳区"},
    {"id": 10, "name": "中共三亚市吉阳区委统战部", "type": "党委", "level": "乡科级",
     "parent": "中共三亚市吉阳区委员会", "location": "海南省三亚市吉阳区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── Sun Dezhen (孙德震) — Current Party Secretary ──
    {"person_id": 1, "org_id": 1, "title": "吉阳区委书记",
     "start": "2023", "end": "present", "rank": "副厅级",
     "note": "现任吉阳区委书记"},

    # ── Yang Hongjun (杨鸿钧) — Current District Mayor ──
    {"person_id": 2, "org_id": 2, "title": "吉阳区委副书记、区长",
     "start": "2021-10", "end": "present", "rank": "正县级",
     "note": "2021年10月任吉阳区代区长，后当选区长"},
    {"person_id": 2, "org_id": 2, "title": "吉阳区委副书记、代区长",
     "start": "2021-09", "end": "2021-10", "rank": "正县级",
     "note": "2021年9月任代区长"},

    # ── Chen Xiaobao (陈小宝) — Deputy Party Secretary ──
    {"person_id": 3, "org_id": 1, "title": "吉阳区委副书记",
     "start": "", "end": "present", "rank": "副县级",
     "note": ""},

    # ── Qin Xiaoling (秦晓玲) — Standing Committee, Vice Mayor ──
    {"person_id": 4, "org_id": 2, "title": "吉阳区委常委、副区长",
     "start": "", "end": "present", "rank": "副县级",
     "note": ""},

    # ── Yu Sihai (于四海) — Discipline Inspection ──
    {"person_id": 5, "org_id": 5, "title": "吉阳区委常委、纪委书记、监委主任",
     "start": "", "end": "present", "rank": "副县级",
     "note": ""},

    # ── Zhang Chen (张晨) — Organization Department ──
    {"person_id": 6, "org_id": 7, "title": "吉阳区委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": ""},

    # ── Zhao Fei (赵飞) — Propaganda Department ──
    {"person_id": 7, "org_id": 8, "title": "吉阳区委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": ""},

    # ── Wang Mao (王懋) — Political and Legal Affairs ──
    {"person_id": 8, "org_id": 9, "title": "吉阳区委常委、政法委书记",
     "start": "", "end": "present", "rank": "副县级",
     "note": ""},

    # ── He Liping (何丽萍) — United Front ──
    {"person_id": 9, "org_id": 10, "title": "吉阳区委常委、统战部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": ""},

    # ── Ke Junbiao (柯俊标) — People's Congress ──
    {"person_id": 10, "org_id": 3, "title": "吉阳区人大常委会主任",
     "start": "", "end": "present", "rank": "正县级",
     "note": ""},

    # ── Chen Xi (陈曦) — Political Consultative Conference ──
    {"person_id": 11, "org_id": 4, "title": "吉阳区政协主席",
     "start": "", "end": "present", "rank": "正县级",
     "note": ""},

    # ── Predecessors ──
    {"person_id": 12, "org_id": 1, "title": "吉阳区委书记",
     "start": "2020", "end": "2023", "rank": "副厅级",
     "note": "前任吉阳区委书记，吴清江"},
    {"person_id": 13, "org_id": 1, "title": "吉阳区委书记",
     "start": "2016", "end": "2020", "rank": "副厅级",
     "note": "前任吉阳区委书记，林海"},
    {"person_id": 14, "org_id": 2, "title": "吉阳区长",
     "start": "2016", "end": "2021-09", "rank": "正县级",
     "note": "前任吉阳区长，顾浩"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Core: Party Secretary ↔ District Mayor
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "strength": "strong",
     "context": "孙德震作为区委书记，杨鸿钧作为区长，是吉阳区党政一把手搭档关系",
     "overlap_org": "中共三亚市吉阳区委员会/三亚市吉阳区人民政府",
     "overlap_period": "2023至今", "confidence": "confirmed"},

    # Party Secretary ↔ Predecessors
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor",
     "strength": "strong",
     "context": "孙德震接替吴清江任吉阳区委书记",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023", "confidence": "confirmed"},
    {"person_a": 12, "person_b": 13, "type": "predecessor_successor",
     "strength": "strong",
     "context": "吴清江接替林海任吉阳区委书记",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2020", "confidence": "confirmed"},

    # District Mayor ↔ Predecessor
    {"person_a": 2, "person_b": 14, "type": "predecessor_successor",
     "strength": "strong",
     "context": "杨鸿钧接替顾浩任吉阳区长",
     "overlap_org": "三亚市吉阳区人民政府",
     "overlap_period": "2021", "confidence": "confirmed"},

    # Party Secretary ↔ Standing Committee members
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与陈小宝在吉阳区委共事",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与秦晓玲在吉阳区党政班子共事",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与于四海在吉阳区委共事，于四海任纪委书记",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与张晨在吉阳区委共事，张晨任组织部部长",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与赵飞在吉阳区委共事，赵飞任宣传部部长",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与王懋在吉阳区委共事，王懋任政法委书记",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},

    # District Mayor ↔ Standing Committee members
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "strength": "strong",
     "context": "杨鸿钧与秦晓玲在吉阳区政府共事，秦晓玲为区委常委、副区长",
     "overlap_org": "三亚市吉阳区人民政府",
     "overlap_period": "2021至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "strength": "medium",
     "context": "杨鸿钧与陈小宝在吉阳区党政班子共事",
     "overlap_org": "三亚市吉阳区人民政府",
     "overlap_period": "2021至今", "confidence": "confirmed"},

    # Party Secretary ↔ People's Congress / Political Consultative
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与柯俊标在吉阳区共事",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "strength": "medium",
     "context": "孙德震与陈曦在吉阳区共事",
     "overlap_org": "中共三亚市吉阳区委员会",
     "overlap_period": "2023至今", "confidence": "confirmed"},
]

# =========================================================================
# HELPERS
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# =========================================================================
# BUILD DB
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
             p.get("birth",""), p.get("birthplace",""), p.get("education",""),
             p.get("party_join",""), p.get("work_start",""),
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start",""), pos.get("end",""),
             pos.get("rank",""), pos.get("note","")))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context,
             overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>三亚市吉阳区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start",""))}~{esc(pos.get("end",""))}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# =========================================================================
# SUMMARY
# =========================================================================
def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
