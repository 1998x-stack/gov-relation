#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Honggu District (红古区), Lanzhou, Gansu."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_红古区")
DB_PATH = os.path.join(TMP, "红古区_network.db")
GEXF_PATH = os.path.join(TMP, "红古区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "薛蕾", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区委书记", "current_org": "中共红古区委",
     "source": "兰州市领导信息"},
    {"id": 2, "name": "肖正明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区区长", "current_org": "红古区人民政府",
     "source": "兰州市领导信息"},

    # ── Previous Leaders ──
    {"id": 3, "name": "李荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原红古区委书记（前任）", "current_org": "中共红古区委（原）",
     "source": "公开报道"},
    {"id": 4, "name": "张涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原红古区区长（前任）", "current_org": "红古区人民政府（原）",
     "source": "公开报道"},

    # ── Key Standing Committee Members ──
    {"id": 5, "name": "韩鹤峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区委常委、常务副区长", "current_org": "红古区人民政府",
     "source": "公开报道"},
    {"id": 6, "name": "邵建胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区委常委、纪委书记、监委主任", "current_org": "中共红古区纪律检查委员会",
     "source": "公开报道"},
    {"id": 7, "name": "杨恩奎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区委常委、组织部部长", "current_org": "中共红古区委组织部",
     "source": "公开报道"},
    {"id": 8, "name": "张惠勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区委常委、政法委书记", "current_org": "中共红古区委政法委员会",
     "source": "公开报道"},
    {"id": 9, "name": "秦敦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区委常委、区委办主任", "current_org": "中共红古区委",
     "source": "公开报道"},
    {"id": 10, "name": "刘军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区委常委、宣传部部长", "current_org": "中共红古区委宣传部",
     "source": "公开报道"},

    # ── Other Key Leaders ──
    {"id": 11, "name": "范永锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区人大常委会主任", "current_org": "红古区人民代表大会常务委员会",
     "source": "公开报道"},
    {"id": 12, "name": "张国胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区政协主席", "current_org": "中国人民政治协商会议红古区委员会",
     "source": "公开报道"},
    {"id": 13, "name": "马鹤林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区副区长", "current_org": "红古区人民政府",
     "source": "公开报道"},
    {"id": 14, "name": "杜生湖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红古区副区长", "current_org": "红古区人民政府",
     "source": "公开报道"},
]

organizations = [
    {"id": 1, "name": "中共红古区委", "type": "党委", "level": "县处级", "parent": "中共兰州市委员会",
     "location": "甘肃省兰州市红古区"},
    {"id": 2, "name": "红古区人民政府", "type": "政府", "level": "县处级", "parent": "兰州市人民政府",
     "location": "甘肃省兰州市红古区"},
    {"id": 3, "name": "红古区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "兰州市人大常委会",
     "location": "甘肃省兰州市红古区"},
    {"id": 4, "name": "中国人民政治协商会议红古区委员会", "type": "政协", "level": "县处级", "parent": "兰州市政协",
     "location": "甘肃省兰州市红古区"},
    {"id": 5, "name": "中共红古区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共兰州市纪律检查委员会",
     "location": "甘肃省兰州市红古区"},
    {"id": 6, "name": "中共红古区委组织部", "type": "党委", "level": "县处级", "parent": "中共红古区委",
     "location": "甘肃省兰州市红古区"},
    {"id": 7, "name": "中共红古区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共红古区委",
     "location": "甘肃省兰州市红古区"},
    {"id": 8, "name": "中共红古区委宣传部", "type": "党委", "level": "县处级", "parent": "中共红古区委",
     "location": "甘肃省兰州市红古区"},
]

positions = [
    # ── Xue Lei (薛蕾) ──
    {"person_id": 1, "org_id": 1, "title": "红古区委书记", "start": "", "end": "present", "rank": "正处级", "note": "红古区委书记"},

    # ── Xiao Zhengming (肖正明) ──
    {"person_id": 2, "org_id": 2, "title": "红古区区长", "start": "", "end": "present", "rank": "正处级", "note": "红古区区长"},

    # ── Li Rong (李荣) — Predecessor party secretary ──
    {"person_id": 3, "org_id": 1, "title": "红古区委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "薛蕾前任"},

    # ── Zhang Tao (张涛) — Predecessor mayor ──
    {"person_id": 4, "org_id": 2, "title": "红古区区长（前任）", "start": "", "end": "", "rank": "正处级", "note": "肖正明前任"},

    # ── Han Hefeng (韩鹤峰) ──
    {"person_id": 5, "org_id": 2, "title": "红古区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Shao Jiansheng (邵建胜) ──
    {"person_id": 6, "org_id": 5, "title": "红古区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Yang Enkui (杨恩奎) ──
    {"person_id": 7, "org_id": 6, "title": "红古区委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Zhang Huiyong (张惠勇) ──
    {"person_id": 8, "org_id": 7, "title": "红古区委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Qin Dun (秦敦) ──
    {"person_id": 9, "org_id": 1, "title": "红古区委常委、区委办主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Liu Jun (刘军) ──
    {"person_id": 10, "org_id": 8, "title": "红古区委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Fan Yongfeng (范永锋) ──
    {"person_id": 11, "org_id": 3, "title": "红古区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # ── Zhang Guosheng (张国胜) ──
    {"person_id": 12, "org_id": 4, "title": "红古区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # ── Ma Helin (马鹤林) ──
    {"person_id": 13, "org_id": 2, "title": "红古区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Du Shenghu (杜生湖) ──
    {"person_id": 14, "org_id": 2, "title": "红古区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾作为红古区委书记，肖正明作为区长，是党政一把手搭档关系",
     "overlap_org": "红古区", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "前后任", "strength": "strong",
     "context": "薛蕾接替李荣任红古区委书记",
     "overlap_org": "中共红古区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "前后任", "strength": "strong",
     "context": "肖正明接替张涛任红古区区长",
     "overlap_org": "红古区人民政府", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与韩鹤峰在红古区委共事，韩鹤峰任常务副区长",
     "overlap_org": "红古区", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与邵建胜在红古区委共事，邵建胜任纪委书记",
     "overlap_org": "中共红古区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与杨恩奎在红古区委共事，杨恩奎任组织部部长",
     "overlap_org": "中共红古区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与张惠勇在红古区委共事，张惠勇任政法委书记",
     "overlap_org": "中共红古区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与秦敦在红古区委共事，秦敦任区委办主任",
     "overlap_org": "中共红古区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与刘军在红古区委共事，刘军任宣传部部长",
     "overlap_org": "中共红古区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "党政同僚", "strength": "strong",
     "context": "肖正明与韩鹤峰在红古区政府共事，韩鹤峰任常务副区长辅佐区长",
     "overlap_org": "红古区人民政府", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与范永锋在红古区四大班子共事，范永锋任人大主任",
     "overlap_org": "红古区", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "党政同僚", "strength": "strong",
     "context": "薛蕾与张国胜在红古区四大班子共事，张国胜任政协主席",
     "overlap_org": "红古区", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "党政同僚", "strength": "strong",
     "context": "肖正明与范永锋在红古区共事",
     "overlap_org": "红古区", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "党政同僚", "strength": "strong",
     "context": "肖正明与张国胜在红古区共事",
     "overlap_org": "红古区", "overlap_period": "", "confidence": "confirmed"},
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
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" not in role)

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
    lines.append('    <description>红古区领导班子工作关系网络 - 甘肃省兰州市红古区</description>')
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
