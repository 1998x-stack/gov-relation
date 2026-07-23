#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 威县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
STAGING = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(STAGING, "威县_network.db")
GEXF_PATH = os.path.join(STAGING, "威县_network.gexf")

persons = [
    {"id": 1, "name": "高凯英", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共威县委员会",
     "source": "https://www.weixian.gov.cn/single/258/78227.html"},
    {"id": 2, "name": "程科峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县长", "current_org": "威县人民政府",
     "source": "https://www.weixian.gov.cn/single/258/78274.html"},
]

organizations = [
    {"id": 1, "name": "中共威县委员会", "type": "党委", "level": "县级",
     "parent": "中共邢台市委员会", "location": "河北省邢台市威县"},
    {"id": 2, "name": "威县人民政府", "type": "政府", "level": "县级",
     "parent": "邢台市人民政府", "location": "河北省邢台市威县"},
    {"id": 3, "name": "中共威县纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "中共威县委员会", "location": "河北省邢台市威县"},
    {"id": 4, "name": "威县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "威县", "location": "河北省邢台市威县"},
    {"id": 5, "name": "中国人民政治协商会议威县委员会", "type": "政协", "level": "县级",
     "parent": "威县", "location": "河北省邢台市威县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "截至2026年7月在任，主持县委十二届十一次全会"},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "县委副书记、县政府党组书记、县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "兼任县委副书记"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "县委书记与县长党政搭档",
     "overlap_org": "威县县委县政府", "overlap_period": "2026年至今"},
]

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys=ON")

for tbl in ("relationships","positions","organizations","persons"):
    conn.execute(f"DROP TABLE IF EXISTS {tbl}")

conn.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
    ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
    education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
    current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
);
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
    level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
);
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
         p["education"],p["party_join"],p["work_start"],
         p["current_post"],p["current_org"],p["source"]))

for o in organizations:
    conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
        (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

for r in positions:
    conn.execute("INSERT INTO positions(person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
        (r["person_id"],r["org_id"],r["title"],r["start_date"],r["end_date"],r["rank"],r["note"]))

for r in relationships:
    conn.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
        (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

conn.commit()
conn.close()
print(f"DB ready: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

def person_color(post):
    if "书记" in post and "副" not in post: return "200,30,30"
    if "县长" in post or "区长" in post or "市长" in post: return "30,100,200"
    if "副" in post: return "100,150,220"
    if "常委" in post: return "180,100,180"
    return "180,180,180"

def org_color(t):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
            "政协":"255,240,200","纪委":"255,165,0"}.get(t,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>gov-relation research agent</creator>')
lines.append('    <description>威县领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="current_post" type="string"/>')
lines.append('      <attribute id="2" title="current_org" type="string"/>')
lines.append('      <attribute id="3" title="org_type" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p["current_post"])
    sz = "60.0" if "书记" in p["current_post"] and "副" not in p["current_post"] else "50.0" if "县长" in p["current_post"] else "35.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o["type"])
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="3" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="0.8"/>')
    lines.append('        <viz:size value="15.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')

lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF ready: {GEXF_PATH}")
print("Done.")
