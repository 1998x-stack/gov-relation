#!/usr/bin/env python3
"""
会昌县 (Huichang County) - 赣州市, 江西省
领导班子工作关系网络生成脚本

Generated: 2026-07-15
Task: jiangxi_会昌县

Sources:
- 会昌县人民政府网 https://www.huichang.gov.cn
- 会昌县党务公开网 https://hcxf.gov.cn
- 百度百科
- 网易新闻 / 澎湃新闻 / 腾讯新闻

Includes:
- Current Party Secretary and County Mayor
- Full leadership roster
- Organization nodes
- Career and relationship edges
"""

import sqlite3
import os
import sys
import json
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(OUTPUT_DIR, "会昌县_network.db")
GEXF_PATH = os.path.join(OUTPUT_DIR, "会昌县_network.gexf")
TODAY = "2026-07-15"

# ── Data ───────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "李茂进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-12",
        "birthplace": "江西石城",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2006-08",
        "current_post": "会昌县委书记",
        "current_org": "中共会昌县委员会",
        "source": "https://www.huichang.gov.cn",
    },
    {
        "id": 2,
        "name": "吕浩泳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "江西兴国",
        "education": "大学学历",
        "party_join": "1998-03",
        "work_start": "1999-08",
        "current_post": "会昌县委副书记、县长提名人选",
        "current_org": "会昌县人民政府",
        "source": "https://www.huichang.gov.cn",
    },
    {
        "id": 3,
        "name": "潘金城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-12",
        "birthplace": "江西赣州",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江西省委督导组组长、组织部部务委员（原会昌县委书记）",
        "current_org": "中共江西省委",
        "source": "https://baike.baidu.com/item/%E6%BD%98%E9%87%91%E5%9F%8E",
    },
    {
        "id": 4,
        "name": "李德伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "江西南康",
        "education": "大学学历",
        "party_join": "1996-04",
        "work_start": "1996-09",
        "current_post": "原会昌县委副书记、县长",
        "current_org": "（已离任）",
        "source": "https://www.huichang.gov.cn",
    },
    {
        "id": 5,
        "name": "许建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "会昌县委常委、副县长",
        "current_org": "会昌县人民政府",
        "source": "https://www.huichang.gov.cn",
    },
    {
        "id": 6,
        "name": "彭亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "会昌县委副书记、副县长",
        "current_org": "会昌县人民政府",
        "source": "https://www.huichang.gov.cn",
    },
    {
        "id": 7,
        "name": "殷俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "会昌县委常委",
        "current_org": "中共会昌县委员会",
        "source": "https://www.huichang.gov.cn",
    },
]

# Predecessor/successor: Previous county leaders
previous_leaders = [
    {
        "id": 8,
        "name": "蔡小卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原会昌县委书记（2016-2021）",
        "current_org": "（已离任）",
        "source": "https://baike.baidu.com",
    },
]

all_persons = persons + previous_leaders

organizations = [
    {"id": 1, "name": "中共会昌县委员会", "type": "党委",
     "level": "县处级", "parent": "中共赣州市委员会",
     "location": "江西赣州会昌"},
    {"id": 2, "name": "会昌县人民政府", "type": "政府",
     "level": "县处级", "parent": "赣州市人民政府",
     "location": "江西赣州会昌"},
    {"id": 3, "name": "中共江西省委", "type": "党委",
     "level": "省部级", "parent": "",
     "location": "江西南昌"},
]

positions = [
    # Current roles
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "会昌县委书记",
     "start": "2026-07", "end": "", "rank": "县处级正职",
     "note": "2026年7月由县长转任县委书记"},
    {"id": 2, "person_id": 2, "org_id": 2,
     "title": "会昌县委副书记、县长提名人选",
     "start": "2026-07", "end": "", "rank": "县处级正职",
     "note": "2026年7月任职"},
    # Previous roles
    {"id": 3, "person_id": 3, "org_id": 1,
     "title": "会昌县委书记（前任）",
     "start": "2021-08", "end": "2026", "rank": "县处级正职",
     "note": "2021年8月至2026年任会昌县委书记，后调任江西省委"},
    {"id": 4, "person_id": 4, "org_id": 2,
     "title": "会昌县委副书记、县长（前任）",
     "start": "2021-09", "end": "2024-11", "rank": "县处级正职",
     "note": "2024年11月离任"},
    {"id": 5, "person_id": 1, "org_id": 2,
     "title": "会昌县委副书记、县长（前任职务）",
     "start": "2024-11", "end": "2026-07", "rank": "县处级正职",
     "note": "2024年11月任代县长，2025年1月当选，2026年7月转任县委书记"},
    {"id": 6, "person_id": 5, "org_id": 2,
     "title": "会昌县委常委、副县长",
     "start": "", "end": "", "rank": "副处级",
     "note": "现任"},
    {"id": 7, "person_id": 6, "org_id": 2,
     "title": "会昌县委副书记、副县长",
     "start": "", "end": "", "rank": "副处级",
     "note": "现任"},
    {"id": 8, "person_id": 7, "org_id": 1,
     "title": "会昌县委常委",
     "start": "2021-08", "end": "", "rank": "副处级",
     "note": "2021年8月当选县委常委"},
    {"id": 9, "person_id": 8, "org_id": 1,
     "title": "会昌县委书记（前任）",
     "start": "2016", "end": "2021-08", "rank": "县处级正职",
     "note": "2016-2021年任会昌县委书记"},
]

relationships = [
    {
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政搭档",
        "context": "李茂进（县委书记）与吕浩泳（县长提名人选）为现任党政正职搭档",
        "overlap_org": "会昌县",
        "overlap_period": "2026-07至今",
    },
    {
        "person_a_id": 3,
        "person_b_id": 4,
        "type": "党政搭档",
        "context": "潘金城（县委书记）与李德伟（县长）为2021-2024年党政正职搭档",
        "overlap_org": "会昌县",
        "overlap_period": "2021-2024",
    },
    {
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "predecessor_successor",
        "context": "李茂进（县长→县委书记）接替潘金城（县委书记→省委）的职务",
        "overlap_org": "会昌县",
        "overlap_period": "2024-2026",
    },
    {
        "person_a_id": 1,
        "person_b_id": 4,
        "type": "predecessor_successor",
        "context": "李茂进接替李德伟任会昌县长",
        "overlap_org": "会昌县人民政府",
        "overlap_period": "2024",
    },
    {
        "person_a_id": 3,
        "person_b_id": 8,
        "type": "predecessor_successor",
        "context": "潘金城接替蔡小卫任会昌县委书记",
        "overlap_org": "中共会昌县委员会",
        "overlap_period": "2021",
    },
]


# ── SQLite Generator ──────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY,
        person_a_id INTEGER, person_b_id INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")

    for p in all_persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"],
                   pos["title"], pos["start"], pos["end"],
                   pos["rank"], pos["note"]))
    for idx, r in enumerate(relationships, 1):
        c.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (idx, r["person_a_id"], r["person_b_id"],
                   r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


# ── GEXF Generator ────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Person node color by role."""
    post = p.get("current_post", "")
    if "县委书记" in post or "县委书记" in post:
        return "255,50,50"
    elif "县长" in post or "副县长" in post:
        return "50,100,255"
    else:
        return "100,100,100"


def org_color(o):
    """Organization node color by type."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    return "200,200,200"


def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or "县长" in post


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>会昌县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in all_persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birthplace",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("location",""))}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("start",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("end",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Created: {GEXF_PATH}")


# ── Main ───────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    build_db()
    build_gexf()
    print("\nDone. Artifacts in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
