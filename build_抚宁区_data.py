#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Funing District (抚宁区), Qinhuangdao, Hebei."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/hebei_抚宁区")
DB_PATH = os.path.join(TMP, "抚宁区_network.db")
GEXF_PATH = os.path.join(TMP, "抚宁区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "郭继东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦皇岛市抚宁区委书记", "current_org": "中共秦皇岛市抚宁区委员会",
     "source": "https://www.chinafuning.gov.cn"},
    {"id": 2, "name": "张子松", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-09", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "抚宁区委副书记、区长", "current_org": "抚宁区人民政府",
     "source": "https://www.chinafuning.gov.cn/zfld.thtml"},

    # ── Deputy Leaders (from leadership activity pages) ──
    {"id": 3, "name": "李海龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "抚宁区委常委、副区长", "current_org": "抚宁区人民政府",
     "source": "https://www.chinafuning.gov.cn"},
    {"id": 4, "name": "刘勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "抚宁区副区长", "current_org": "抚宁区人民政府",
     "source": "https://www.chinafuning.gov.cn"},
    {"id": 5, "name": "王志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "抚宁区副区长", "current_org": "抚宁区人民政府",
     "source": "https://www.chinafuning.gov.cn"},
    {"id": 6, "name": "李新宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "抚宁区副区长", "current_org": "抚宁区人民政府",
     "source": "https://www.chinafuning.gov.cn"},
    {"id": 7, "name": "陈立江", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "抚宁区副区长", "current_org": "抚宁区人民政府",
     "source": "https://www.chinafuning.gov.cn"},
    {"id": 8, "name": "张广麒", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "抚宁区副区长", "current_org": "抚宁区人民政府",
     "source": "https://www.chinafuning.gov.cn"},
]

organizations = [
    {"id": 1, "name": "中共秦皇岛市抚宁区委员会", "type": "党委", "level": "县处级", "parent": "中共秦皇岛市委员会",
     "location": "河北省秦皇岛市抚宁区"},
    {"id": 2, "name": "抚宁区人民政府", "type": "政府", "level": "县处级", "parent": "秦皇岛市人民政府",
     "location": "河北省秦皇岛市抚宁区"},
    {"id": 3, "name": "抚宁区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "秦皇岛市人大常委会",
     "location": "河北省秦皇岛市抚宁区"},
    {"id": 4, "name": "中国人民政治协商会议抚宁区委员会", "type": "政协", "level": "县处级", "parent": "秦皇岛市政协",
     "location": "河北省秦皇岛市抚宁区"},
]

positions = [
    # ── Guo Jidong Career (郭继东) ──
    {"person_id": 1, "org_id": 1, "title": "抚宁区委书记", "start": "约2024", "end": "present", "rank": "正县处级", "note": "主持区委全面工作；此前履历待查"},

    # ── Zhang Zisong Career (张子松) ──
    {"person_id": 2, "org_id": 2, "title": "抚宁区委副书记、区长", "start": "约2023", "end": "present", "rank": "正县处级", "note": "领导区政府全面工作；1979年9月出生，大学学历"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记", "start": "约2023", "end": "present", "rank": "正县处级", "note": ""},

    # ── Li Hailong (李海龙) ──
    {"person_id": 3, "org_id": 2, "title": "抚宁区委常委、副区长", "start": "", "end": "present", "rank": "副县处级", "note": "分管相关领域工作"},
    {"person_id": 3, "org_id": 5, "title": "区粮食和物资储备局局长、区商务局局长（原任）", "start": "", "end": "2025-02", "rank": "", "note": "2025年2月不再兼任"},

    # ── Liu Yong (刘勇) ──
    {"person_id": 4, "org_id": 2, "title": "抚宁区副区长", "start": "", "end": "present", "rank": "副县处级", "note": "负责安全生产、森林防灭火等工作"},

    # ── Wang Zhigang (王志刚) ──
    {"person_id": 5, "org_id": 2, "title": "抚宁区副区长", "start": "", "end": "present", "rank": "副县处级", "note": "负责食品安全、社保等工作"},

    # ── Li Xinyu (李新宇) ──
    {"person_id": 6, "org_id": 2, "title": "抚宁区副区长", "start": "", "end": "present", "rank": "副县处级", "note": "负责美丽河湖项目、安全生产等工作"},

    # ── Chen Lijiang (陈立江) ──
    {"person_id": 7, "org_id": 2, "title": "抚宁区副区长", "start": "", "end": "present", "rank": "副县处级", "note": "负责防贫监测、森林防火等工作"},

    # ── Zhang Guangqi (张广麒) ──
    {"person_id": 8, "org_id": 2, "title": "抚宁区副区长", "start": "", "end": "present", "rank": "副县处级", "note": "负责医保、卫生健康、文旅等工作"},
]

relationships = [
    # Party Secretary ↔ Mayor
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "郭继东作为区委书记，张子松作为区长，是党政一把手搭档关系",
     "overlap_org": "中共抚宁区委/抚宁区人民政府",
     "overlap_period": "约2024年至今", "confidence": "confirmed"},

    # Party Secretary ↔ Deputy Leaders
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "郭继东与李海龙在抚宁区委/区政府共事，李海龙任区委常委、副区长",
     "overlap_org": "中共抚宁区委/抚宁区人民政府",
     "overlap_period": "约2024年至今", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "郭继东与刘勇在抚宁区共事，刘勇任副区长",
     "overlap_org": "中共抚宁区委/抚宁区人民政府",
     "overlap_period": "约2024年至今", "confidence": "confirmed"},

    # Mayor ↔ Deputy Leaders
    {"person_a": 2, "person_b": 3, "type": "subordinate", "strength": "strong",
     "context": "张子松作为区长，李海龙作为常委副区长协助区长工作",
     "overlap_org": "抚宁区人民政府",
     "overlap_period": "约2023年至今", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 4, "type": "subordinate", "strength": "medium",
     "context": "张子松与刘勇在区政府共事，刘勇任副区长",
     "overlap_org": "抚宁区人民政府",
     "overlap_period": "约2023年至今", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 5, "type": "subordinate", "strength": "medium",
     "context": "张子松与王志刚在区政府共事，王志刚任副区长",
     "overlap_org": "抚宁区人民政府",
     "overlap_period": "约2023年至今", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 6, "type": "subordinate", "strength": "medium",
     "context": "张子松与李新宇在区政府共事，李新宇任副区长",
     "overlap_org": "抚宁区人民政府",
     "overlap_period": "约2023年至今", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 7, "type": "subordinate", "strength": "medium",
     "context": "张子松与陈立江在区政府共事，陈立江任副区长",
     "overlap_org": "抚宁区人民政府",
     "overlap_period": "约2023年至今", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 8, "type": "subordinate", "strength": "medium",
     "context": "张子松与张广麒在区政府共事，张广麒任副区长",
     "overlap_org": "抚宁区人民政府",
     "overlap_period": "约2023年至今", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "区长" in role:
        return "50,100,255"
    elif "副区长" in role or "常委" in role:
        return "100,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
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

# ── BUILD DB ─────────────────────────────────────────────────

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
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
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
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>抚宁区领导班子工作关系网络 - 河北省秦皇岛市抚宁区</description>')
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
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
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

# ── SUMMARY ──────────────────────────────────────────────────

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
