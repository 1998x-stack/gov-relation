#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Zhenhai District (镇海区), Ningbo, Zhejiang."""

import sqlite3, os, sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/zhejiang_镇海区")
DB_PATH = os.path.join(TMP, "镇海区_network.db")
GEXF_PATH = os.path.join(TMP, "镇海区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "童华强", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-03", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁波市镇海区委书记、区长", "current_org": "中共宁波市镇海区委员会",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},

    # ── Deputy Leaders (区政府领导) ──
    {"id": 2, "name": "高翔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区委常委、常务副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},
    {"id": 3, "name": "林辉宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},
    {"id": 4, "name": "贺建良", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},
    {"id": 5, "name": "杨承志", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},
    {"id": 6, "name": "吴沂雁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},
    {"id": 7, "name": "彭鲲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},
    {"id": 8, "name": "杨才表", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},
    {"id": 9, "name": "陆水锦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇海区副区长", "current_org": "宁波市镇海区人民政府",
     "source": "https://www.zh.gov.cn/col/col1229626797/index.html"},

    # ── Previous Leaders ──
    {"id": 10, "name": "林雅莲", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原镇海区委书记（2016-2025/2026）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E9%95%87%E6%B5%B7%E5%8C%BA_(%E5%AE%81%E6%B3%A2%E5%B8%82)"},
]

organizations = [
    {"id": 1, "name": "中共宁波市镇海区委员会", "type": "党委", "level": "县处级", "parent": "中共宁波市委员会",
     "location": "浙江省宁波市镇海区"},
    {"id": 2, "name": "宁波市镇海区人民政府", "type": "政府", "level": "县处级", "parent": "宁波市人民政府",
     "location": "浙江省宁波市镇海区"},
    {"id": 3, "name": "镇海区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宁波市人大常委会",
     "location": "浙江省宁波市镇海区"},
    {"id": 4, "name": "中国人民政治协商会议镇海区委员会", "type": "政协", "level": "县处级", "parent": "宁波市政协",
     "location": "浙江省宁波市镇海区"},
    {"id": 5, "name": "中共宁波市镇海区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共宁波市纪委",
     "location": "浙江省宁波市镇海区"},
    {"id": 6, "name": "宁波石化经济技术开发区", "type": "开发区", "level": "国家级", "parent": "宁波市人民政府",
     "location": "浙江省宁波市镇海区"},
]

positions = [
    # 童华强
    {"person_id": 1, "org_id": 1, "title": "宁波市镇海区委书记",
     "start": "2026", "end": "present", "rank": "县处级正职", "note": "confirmed via official news 2026-07-30"},
    {"person_id": 1, "org_id": 2, "title": "宁波市镇海区区长、党组书记",
     "start": "", "end": "", "rank": "县处级正职", "note": "listed on government 领导之窗 page"},

    # 高翔
    {"person_id": 2, "org_id": 2, "title": "镇海区委常委、常务副区长",
     "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 副区长
    {"person_id": 3, "org_id": 2, "title": "镇海区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "镇海区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "镇海区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "镇海区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "镇海区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "镇海区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "镇海区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 林雅莲
    {"person_id": 10, "org_id": 1, "title": "原镇海区委书记",
     "start": "2016", "end": "2026", "rank": "县处级正职", "note": "succeeded by 童华强 in 2026"},
]

relationships = [
    # 童华强 ↔ 高翔 (上下级)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与常务副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    # 童华强 ↔ 各副区长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "宁波市镇海区人民政府", "overlap_period": "2026-"},
    # 林雅莲 → 童华强 — 前后任
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor",
     "context": "林雅莲卸任镇海区委书记，童华强接任", "overlap_org": "中共宁波市镇海区委员会", "overlap_period": "2016-2026"},
]

# ── BUILD FUNCTIONS ────────────────────────────────────────────────────

def esc(s):
    if s is None: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pname, title):
    """Return r,g,b string based on role."""
    if "区委书记" in title or "书记" in title:
        return "255,50,50"
    elif "区长" in title or "常务副" in title:
        return "50,100,255"
    else:
        return "100,100,100"

def org_color(otype):
    cmap = {"党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
            "乡镇": "255,255,200", "人大": "200,255,255", "政协": "255,240,200"}
    return cmap.get(otype, "200,200,200")

def person_size(pname, title):
    if "区委书记" in title or "区长" in title:
        return "20.0"
    return "12.0"

# ── SQLITE ────────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)
    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions(person_id, org_id, title, start, \"end\", rank, note) VALUES(?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period) VALUES(?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")

# ── GEXF ──────────────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>镇海区 government personnel network - 宁波市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    pid_map = {p["id"]: p for p in persons}
    oid_map = {o["id"]: o for o in organizations}

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"], p["current_post"])
        sz = person_size(p["name"], p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        w = "2.0" if pos["person_id"] == 1 else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")

# ── MAIN ──────────────────────────────────────────────────────────────

def main():
    build_db()
    build_gexf()
    print("Done. Built DB + GEXF for 镇海s区.")

if __name__ == "__main__":
    main()