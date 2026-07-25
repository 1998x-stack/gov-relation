#!/usr/bin/env python3
"""
烟台市莱山区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Laishan District leadership.

Research notes:
- Web access was heavily degraded during this investigation (Exa rate-limited,
  Baidu 403, government site JS-rendered).
- All data marked with ⚠️ "待确认" requires official source verification.
- Current officeholders need direct confirmation from:
  https://www.ytlaishan.gov.cn/col/col38579/ (区政府领导)
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in BASE_DIR:
    REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))
else:
    REPO_ROOT = BASE_DIR

STAGING_DIR = os.path.join(REPO_ROOT, "data/tmp/shandong_莱山区")
DB_PATH = os.path.join(STAGING_DIR, "莱山区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "莱山区_network.gexf")

# ── DATA ──
# ⚠️ All info needs source verification

PERSONS = [
    # dict format matching gov_relation.schema expected columns
    {"id": 1, "name": "罗建", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共烟台市莱山区委书记", "current_org": "中共烟台市莱山区委员会",
     "source": "https://www.ytlaishan.gov.cn/col/col38579/ 待确认"},
    {"id": 2, "name": "蒋海华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "烟台市莱山区人民政府区长", "current_org": "烟台市莱山区人民政府",
     "source": "https://www.ytlaishan.gov.cn/col/col38579/ 待确认"},
    {"id": 3, "name": "（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "莱山区委副书记", "current_org": "中共烟台市莱山区委员会",
     "source": ""},
    {"id": 4, "name": "（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "莱山区常务副区长", "current_org": "烟台市莱山区人民政府",
     "source": ""},
    {"id": 5, "name": "（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "莱山区纪委书记、监委主任", "current_org": "中共烟台市莱山区纪律检查委员会",
     "source": ""},
    {"id": 6, "name": "（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "莱山区委组织部部长", "current_org": "中共烟台市莱山区委员会组织部",
     "source": ""},
    {"id": 7, "name": "（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "莱山区委政法委书记", "current_org": "中共烟台市莱山区委员会政法委员会",
     "source": ""},
    {"id": 8, "name": "（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "莱山区委宣传部部长", "current_org": "中共烟台市莱山区委员会宣传部",
     "source": ""},
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共烟台市莱山区委员会", "type": "党委", "level": "正处级", "parent": "中共烟台市委员会", "location": "烟台市莱山区"},
    {"id": 2, "name": "烟台市莱山区人民政府", "type": "政府", "level": "正处级", "parent": "烟台市人民政府", "location": "烟台市莱山区"},
    {"id": 3, "name": "中共烟台市莱山区纪律检查委员会", "type": "纪委", "level": "正处级", "parent": "中共烟台市纪律检查委员会", "location": "烟台市莱山区"},
    {"id": 4, "name": "烟台市莱山区监察委员会", "type": "监察", "level": "正处级", "parent": "烟台市监察委员会", "location": "烟台市莱山区"},
    {"id": 5, "name": "中共烟台市莱山区委员会组织部", "type": "党委部门", "level": "正科级", "parent": "中共烟台市莱山区委员会", "location": "烟台市莱山区"},
    {"id": 6, "name": "中共烟台市莱山区委员会宣传部", "type": "党委部门", "level": "正科级", "parent": "中共烟台市莱山区委员会", "location": "烟台市莱山区"},
    {"id": 7, "name": "中共烟台市莱山区委员会政法委员会", "type": "党委部门", "level": "正科级", "parent": "中共烟台市莱山区委员会", "location": "烟台市莱山区"},
    {"id": 8, "name": "烟台市莱山区人大常委会", "type": "人大", "level": "正处级", "parent": "烟台市人大常委会", "location": "烟台市莱山区"},
    {"id": 9, "name": "中国人民政治协商会议烟台市莱山区委员会", "type": "政协", "level": "正处级", "parent": "烟台市政协", "location": "烟台市莱山区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "中共烟台市莱山区委书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": "需确认"},
    {"person_id": 2, "org_id": 2, "title": "烟台市莱山区人民政府区长",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": "需确认"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政主要领导搭档关系",
     "overlap_org": "中共烟台市莱山区委员会/烟台市莱山区人民政府",
     "overlap_period": ""},
]


# ── SQLite Build ────────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(pid):
    return {1: "255,50,50", 2: "50,100,255", 5: "255,165,0"}.get(pid, "100,100,100")


def org_color(org_type):
    return {"党委": "255,200,200", "政府": "200,200,255", "纪委": "255,200,200",
            "监察": "255,200,200", "党委部门": "255,200,200",
            "人大": "200,255,255", "政协": "255,240,200"}.get(org_type, "200,200,200")


def build():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL, type TEXT DEFAULT '', level TEXT DEFAULT '',
            parent TEXT DEFAULT '', location TEXT DEFAULT ''
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        cur.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"],
             p["current_org"], p["source"])
        )
    for o in ORGANIZATIONS:
        cur.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    for pos in POSITIONS:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )
    for rel in RELATIONSHIPS:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (rel["person_a"], rel["person_b"], rel["type"], rel["context"], rel["overlap_org"], rel["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

    # GEXF
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>烟台市莱山区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p["id"]).split(",")
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        c = org_color(o["type"]).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


if __name__ == "__main__":
    build()
