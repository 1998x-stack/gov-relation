#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 毕节市 leadership network.

Targets: 市委书记 (郭锡文) & 市长 (姚轶)
Data as of: 2026-07-23
Sources: www.bijie.gov.cn (official government website)
"""

import os
import sqlite3
from datetime import datetime

# Staging directory
TMP_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__))
)
BASE = os.path.join(TMP_DIR, "..", "..", "..")
DB_PATH = os.path.join(TMP_DIR, "毕节市_network.db")
GEXF_PATH = os.path.join(TMP_DIR, "毕节市_network.gexf")
PERSONS_DIR = os.path.join(TMP_DIR, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────

persons = [
    # === Current Top Leaders ===
    {
        "id": 1, "name": "郭锡文", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市委书记",
        "current_org": "中共毕节市委员会",
        "source": "https://www.bijie.gov.cn/",
    },
    {
        "id": 2, "name": "姚轶", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年12月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "毕节市委副书记、市人民政府市长",
        "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/ldzc/",
    },
    # === Other leadership team members ===
    {
        "id": 3, "name": "罗术灿", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 4, "name": "陈李军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 5, "name": "张超", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 6, "name": "游劲松", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 7, "name": "沈建黔", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 8, "name": "胡东亮", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 9, "name": "郑荣", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 10, "name": "邓志东", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
    {
        "id": 11, "name": "杨志成", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "毕节市领导", "current_org": "毕节市人民政府",
        "source": "https://www.bijie.gov.cn/zwgk/",
    },
]

organizations = [
    {"id": 1, "name": "中共毕节市委员会", "type": "党委",
     "level": "地级市", "parent": "中共贵州省委员会", "location": "贵州省毕节市"},
    {"id": 2, "name": "毕节市人民政府", "type": "政府",
     "level": "地级市", "parent": "贵州省人民政府", "location": "贵州省毕节市"},
    {"id": 3, "name": "毕节市人大常委会", "type": "人大",
     "level": "地级市", "parent": "贵州省人大常委会", "location": "贵州省毕节市"},
    {"id": 4, "name": "政协毕节市委员会", "type": "政协",
     "level": "地级市", "parent": "政协贵州省委员会", "location": "贵州省毕节市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "毕节市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "毕节市人民政府市长", "start": "", "end": "present", "rank": "正厅级", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "毕节市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任"},
    {"person_id": 3, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 4, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 5, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 6, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 7, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 8, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 9, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 10, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 11, "org_id": 2, "title": "毕节市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
]

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "郭锡文为毕节市委书记，姚轶为毕节市委副书记、市长，两人为党政一把手搭档关系",
        "overlap_org": "中共毕节市委员会",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
]

# ═══════════════════════════════════════════════════════
#  Build SQLite DB
# ═══════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    strength TEXT, confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

cur.executemany(
    "INSERT OR REPLACE INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)",
    persons,
)
cur.executemany(
    "INSERT OR REPLACE INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)",
    organizations,
)
cur.executemany(
    "INSERT INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)",
    positions,
)
cur.executemany(
    "INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period,:strength,:confidence)",
    relationships,
)

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
ps = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc = cur.fetchone()[0]
conn.close()

print(f"Database: {DB_PATH}")
print(f"  Persons: {pc}, Organizations: {oc}, Positions: {ps}, Relationships: {rc}")

# ═══════════════════════════════════════════════════════
#  Build GEXF Graph
# ═══════════════════════════════════════════════════════


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    title = p.get("current_post", "")
    if "书记" in title and "副" not in title:
        return "255,50,50"
    if "市长" in title or "区长" in title or "县长" in title:
        if "副" not in title:
            return "50,100,255"
        return "100,100,255"
    if "纪委" in title:
        return "255,165,0"
    return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    title = p.get("current_post", "")
    return "市委书记" in title or ("市长" in title and "副" not in title)


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append("    <creator>Gov Relation Research Agent</creator>")
lines.append(f"    <description>毕节市领导班子关系网络 — 数据截至 {datetime.now().strftime('%Y-%m-%d')}</description>")
lines.append("  </meta>")
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="education" type="string"/>')
lines.append("    </attributes>")

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="confidence" type="string"/>')
lines.append("    </attributes>")

# Nodes
lines.append("    <nodes>")
for p in persons:
    pid = p["id"]
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p.get("education",""))}"/>')
    lines.append("        </attvalues>")
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append("      </node>")

for o in organizations:
    oid = o["id"]
    c = org_color(o)
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
    lines.append("        </attvalues>")
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append("      </node>")

lines.append("    </nodes>")

# Edges
lines.append("    <edges>")
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
    lines.append('          <attvalue for="2" value="confirmed"/>')
    lines.append("        </attvalues>")
    lines.append("      </edge>")

for r in relationships:
    eid += 1
    w = "2.0" if r.get("strength") == "strong" else "1.0"
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type",""))}" weight="{w}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence",""))}"/>')
    lines.append("        </attvalues>")
    lines.append("      </edge>")

lines.append("    </edges>")
lines.append("  </graph>")
lines.append("</gexf>")

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"GEXF: {GEXF_PATH}")
print(f"  Total edges: {eid}")

print("\nDone.")
