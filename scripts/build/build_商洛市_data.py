#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 商洛市 (Shangluo City, Shaanxi) leadership network.

Scope: 地级市 level — 市委书记 & 市长
Web research was partially degraded; career timeline gaps are flagged.
"""
import sys
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/shaanxi_商洛市")
DB_PATH = os.path.join(TMP, "商洛市_network.db")
GEXF_PATH = os.path.join(TMP, "商洛市_network.gexf")

# Ensure TMP exists
os.makedirs(TMP, exist_ok=True)

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "赵璟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1966-01",
        "birthplace": "陕西省延安市",
        "education": "西安交通大学（硕士）",
        "party_join": "",
        "work_start": "",
        "current_post": "商洛市委书记",
        "current_org": "中共商洛市委",
        "source": "https://zh.wikipedia.org/wiki/赵璟",
    },
    {
        "id": 2,
        "name": "王青峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-07",
        "birthplace": "陕西省澄城县",
        "education": "陕西师范大学（研究生）",
        "party_join": "",
        "work_start": "",
        "current_post": "商洛市长",
        "current_org": "商洛市人民政府",
        "source": "https://zh.wikipedia.org/wiki/王青峰",
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "郑光照",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-09",
        "birthplace": "陕西省礼泉县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "内蒙古自治区副主席（原商洛市委书记）",
        "current_org": "内蒙古自治区人民政府",
        "source": "open_question — 历任商洛市委书记",
    },
    {
        "id": 4,
        "name": "张小平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原商洛市长",
        "current_org": "",
        "source": "open_question — 历任商洛市长",
    },
]

organizations = [
    {"id": 1, "name": "中共商洛市委", "type": "党委", "level": "地级市", "parent": "中共陕西省委", "location": "陕西省商洛市"},
    {"id": 2, "name": "商洛市人民政府", "type": "政府", "level": "地级市", "parent": "陕西省人民政府", "location": "陕西省商洛市"},
    {"id": 3, "name": "内蒙古自治区人民政府", "type": "政府", "level": "省级", "parent": "中华人民共和国中央人民政府", "location": "内蒙古自治区"},
]

positions = [
    # 赵璟 — 商洛市委书记
    {"person_id": 1, "org_id": 1, "title": "商洛市委书记", "start_date": "2022-08", "end_date": "", "rank": "正厅级", "note": "现任"},
    # 王青峰 — 商洛市长
    {"person_id": 2, "org_id": 2, "title": "商洛市长", "start_date": "2021-07", "end_date": "", "rank": "正厅级", "note": "现任"},
    # 郑光照 — 前商洛市委书记
    {"person_id": 3, "org_id": 1, "title": "商洛市委书记", "start_date": "2019-08", "end_date": "2022-08", "rank": "正厅级", "note": "前任"},
    {"person_id": 3, "org_id": 3, "title": "内蒙古自治区副主席", "start_date": "2022-08", "end_date": "", "rank": "副省级", "note": ""},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "搭档",
        "context": "赵璟任商洛市委书记后，王青峰任市长二人搭班子",
        "overlap_org": "中共商洛市委/商洛市人民政府",
        "overlap_period": "2022-08至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "接任",
        "context": "赵璟接替郑光照任商洛市委书记",
        "overlap_org": "中共商洛市委",
        "overlap_period": "2022-08",
    },
]


# ── BUILD ────────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p["current_post"]
    if "书记" in post and "市委" in post:
        return "255,50,50"
    elif "市长" in post and "市" in post:
        return "50,100,255"
    return "100,100,100"


def is_top_leader(p):
    return p["id"] in (1, 2)


def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    # Create tables
    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")

    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    # Insert data
    for p in persons:
        conn.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )
    for o in organizations:
        conn.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"[OK] Database: {DB_PATH}")
    print(f"      Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>商洛市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start_date" type="string"/>')
    lines.append('      <attribute id="3" title="end_date" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = "party_secretary" if "书记" in p["current_post"] else "mayor" if "市长" in p["current_post"] else "other"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        otype = o["type"]
        if otype == "党委":
            oc = "255,200,200"
        elif otype == "政府":
            oc = "200,200,255"
        else:
            oc = "200,200,200"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{pos["start_date"]}"/>')
        lines.append(f'          <attvalue for="3" value="{pos["end_date"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="关系" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["overlap_period"]}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("[DONE] 商洛市 build complete")
