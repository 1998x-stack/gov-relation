#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 思明区 (Siming District, Xiamen) leadership network.

思明区 — 厦门市核心城区，副省级城市辖区（正厅级建制），
厦门市委、市政府所在地。

Research date: 2026-07-16
Confidence notes:
- Core leadership (区委书记, 区长, 人大主任, 纪委书记) identity: confirmed from multiple media sources
- Career timeline details for top figures: based on media reports, partial
- Deputy leaders: partial (identified 常务副区长, some confirmed names only)
"""

import sqlite3
import os
from datetime import datetime
import json

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_思明区")
DB_PATH = os.path.join(STAGING, "思明区_network.db")
GEXF_PATH = os.path.join(STAGING, "思明区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 陈通汕 — 思明区委书记 (2025.05-), 前任区长 (2021-2025)
    {"id":1,"name":"陈通汕","gender":"男","ethnicity":"汉族",
     "birth":"1969-11","birthplace":"广东大埔","education":"在职研究生，管理学硕士",
     "party_join":"中共党员","work_start":"1992-08",
     "current_post":"思明区委书记",
     "current_org":"中共思明区委",
     "source":"人民网/厦门思明区政府"},
    # 苏国辉 — 思明区委副书记、区长 (2025.08-)
    {"id":2,"name":"苏国辉","gender":"男","ethnicity":"汉族",
     "birth":"1977-01","birthplace":"福建龙岩","education":"在职研究生，工学博士",
     "party_join":"中共党员","work_start":"unknown",
     "current_post":"思明区委副书记、区长",
     "current_org":"思明区人民政府",
     "source":"厦门思明区政府官方页面"},
    # 吕永辉 — 思明区人大常委会主任 (2021-)
    {"id":3,"name":"吕永辉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"思明区人大常委会主任",
     "current_org":"思明区人大常委会",
     "source":"思明区政府/厦门人大网"},

    # ── 2. Key deputies ──
    # 占兆文 — 思明区委常委、常务副区长
    {"id":4,"name":"占兆文","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"思明区委常委、常务副区长",
     "current_org":"思明区人民政府",
     "source":"思明区政府常务会议记录"},
    # 吴鲤鹏 — 思明区委常委、纪委书记、监委主任
    {"id":5,"name":"吴鲤鹏","gender":"女","ethnicity":"汉族",
     "birth":"1978-10","birthplace":"福建安溪","education":"大学，文学学士",
     "party_join":"中共党员","work_start":"1999-08",
     "current_post":"思明区委常委、区纪委书记、区监委主任",
     "current_org":"中共思明区纪律检查委员会",
     "source":"人民网/福建纪检监察网"},

    # ── 3. Predecessors ──
    # 林重阳 — 前任思明区委书记 (2022.04-2025.01)，现任厦门市政协副主席
    {"id":6,"name":"林重阳","gender":"男","ethnicity":"汉族",
     "birth":"1967-03","birthplace":"","education":"中央党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"厦门市政协副主席（原思明区委书记）",
     "current_org":"政协厦门市委员会",
     "source":"网易/白鹭洲知政"},
    # 陈通汕 also served as 区长 predecessor to 苏国辉 (already person 1)

    # ── 4. Other confirmed officials ──
    # 王意达 — 思明区副区长
    {"id":7,"name":"王意达","gender":"男","ethnicity":"汉族",
     "birth":"1974-01","birthplace":"","education":"党校在职大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"思明区副区长",
     "current_org":"思明区人民政府",
     "source":"思明区政府"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共思明区委","type":"党委","level":"正厅级","parent":"中共厦门市委","location":"厦门市思明区"},
    {"id":2,"name":"思明区人民政府","type":"政府","level":"正厅级","parent":"厦门市人民政府","location":"厦门市思明区"},
    {"id":3,"name":"思明区人大常委会","type":"人大","level":"正厅级","parent":"","location":"厦门市思明区"},
    {"id":4,"name":"政协厦门市委员会","type":"政协","level":"副省级","parent":"","location":"厦门市思明区"},
    {"id":5,"name":"中共思明区纪律检查委员会","type":"纪委","level":"正处级","parent":"中共思明区委","location":"厦门市思明区"},
    {"id":6,"name":"思明区监察委员会","type":"纪委","level":"正处级","parent":"","location":"厦门市思明区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current top leaders
    {"person_id":1,"org_id":1,"title":"思明区委书记","start":"2025-05","end":"","rank":"正厅级","note":"现任，2025年5月由区长升任"},
    {"person_id":1,"org_id":2,"title":"思明区区长","start":"2021-09","end":"2025-05","rank":"正厅级","note":"前任区长，升任区委书记"},
    {"person_id":2,"org_id":2,"title":"思明区委副书记、区长","start":"2025-08","end":"","rank":"正厅级","note":"现任，2025年8月正式当选"},
    {"person_id":2,"org_id":2,"title":"思明区副区长、代理区长","start":"2025-07","end":"2025-08","rank":"正厅级","note":"代理区长"},
    {"person_id":3,"org_id":3,"title":"思明区人大常委会主任","start":"2021","end":"","rank":"正厅级","note":"现任"},

    # Deputies
    {"person_id":4,"org_id":2,"title":"思明区委常委、常务副区长","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":5,"org_id":5,"title":"思明区委常委、纪委书记、监委主任","start":"2023","end":"","rank":"副厅级","note":"现任"},
    {"person_id":7,"org_id":2,"title":"思明区副区长","start":"","end":"","rank":"副厅级","note":"现任"},

    # Predecessor — Party Secretary
    {"person_id":6,"org_id":1,"title":"思明区委书记","start":"2022-04","end":"2025-01","rank":"正厅级","note":"前任区委书记，升任厦门市政协副主席"},
    {"person_id":6,"org_id":4,"title":"厦门市政协副主席","start":"2025-01","end":"","rank":"副省级","note":"现任"},

    # Predecessor — 陈通汕's pre-思明 roles
    {"person_id":1,"org_id":1,"title":"厦门市委组织部干部三处处长","start":"","end":"","rank":"正处级","note":"组织系统经历"},
    {"person_id":1,"org_id":2,"title":"厦门市政府副秘书长、办公厅主任","start":"","end":"2021-09","rank":"副厅级","note":"调任思明区前职务"},

    # 苏国辉's pre-思明 roles
    {"person_id":2,"org_id":2,"title":"厦门市政府办公厅经济社会二处处长","start":"","end":"","rank":"正处级","note":"早期职务"},
    {"person_id":2,"org_id":2,"title":"厦门市政府副秘书长","start":"","end":"2022","rank":"副厅级","note":"前期职务"},
    {"person_id":2,"org_id":1,"title":"厦门市集美区委副书记","start":"2022","end":"2025-07","rank":"副厅级","note":"调任思明区前职务"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Core working relationships
    {"person_a":1,"person_b":2,"type":"党政同僚","context":"陈通汕（区委书记）与苏国辉（区长）党政搭档","overlap_org":"思明区","overlap_period":"2025.08-"},
    {"person_a":1,"person_b":3,"type":"党政同僚","context":"区委书记与人大主任搭档","overlap_org":"思明区","overlap_period":"2021-"},

    # Predecessor-successor — Party Secretary
    {"person_a":6,"person_b":1,"type":"前后任","context":"林重阳→陈通汕 思明区委书记交接(2025.05)","overlap_org":"中共思明区委","overlap_period":"2025-05"},
    {"person_a":1,"person_b":2,"type":"前后任","context":"陈通汕→苏国辉 思明区长交接(2025.07)","overlap_org":"思明区人民政府","overlap_period":"2025-07"},

    # Leadership pairs
    {"person_a":1,"person_b":4,"type":"上下级","context":"区委书记与常务副区长","overlap_org":"思明区","overlap_period":"2025-"},
    {"person_a":1,"person_b":5,"type":"上下级","context":"区委书记与纪委书记","overlap_org":"思明区","overlap_period":"2023-"},
    {"person_a":2,"person_b":4,"type":"上下级","context":"区长与常务副区长","overlap_org":"思明区人民政府","overlap_period":"2025-"},
    {"person_a":2,"person_b":5,"type":"党政同僚","context":"区长与纪委书记","overlap_org":"思明区","overlap_period":"2025-"},
    {"person_a":3,"person_b":2,"type":"党政同僚","context":"人大主任与区长","overlap_org":"思明区","overlap_period":"2025-"},
]

# =========================================================================
# BUILD DATABASE
# =========================================================================
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Print summary
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ Database created: {DB_PATH}")
print(f"   Persons: {person_count} | Orgs: {org_count} | Positions: {pos_count} | Relationships: {rel_count}")

# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def color_for_role(title):
    t = title or ""
    if "书记" in t and "副" not in t and "纪委" not in t:
        return (255,50,50)   # Red for Party Secretary
    if "区长" in t and "副" not in t:
        return (50,100,255)  # Blue for District Mayor
    if "人大" in t:
        return (200,100,100) # Darker for People's Congress
    if "政协" in t:
        return (100,100,200) # Purple for CPPCC
    if "纪委" in t or "纪检" in t:
        return (255,165,0)   # Orange for discipline
    if "副" in t:
        return (100,150,255) # Lighter blue for deputies
    return (100,100,100)

def person_size(p):
    t = p.get("current_post","") or ""
    if ("书记" in t and "副" not in t and "纪委" not in t) or ("区长" in t and "副" not in t):
        return "20.0"
    if "副" in t:
        return "15.0"
    return "12.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>思明区领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attribute declarations
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="birthplace" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    pid = f"sm_{p['id']}"
    c = color_for_role(p.get("current_post",""))
    sz = person_size(p)
    label = esc(f"{p['name']} ({p.get('current_post','?')})")
    lines.append(f'      <node id="{pid}" label="{label}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p.get("birthplace",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# Organization nodes
org_colors = {
    "党委": (255,200,200), "政府": (200,200,255),
    "人大": (200,255,255), "政协": (255,240,200),
    "纪委": (255,220,180), "default": (200,200,200)
}
for o in organizations:
    oid = f"sm_org_{o['id']}"
    oc = org_colors.get(o["type"], org_colors["default"])
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# Edges: person→organization (worked_at)
lines.append('    <edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = esc(f"{p['name']} → {o['name']} ({po['title']})")
    lines.append(f'      <edge id="e{edge_id}" source="sm_{p["id"]}" target="sm_org_{o["id"]}" label="{label}" weight="1.0">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(po.get("title",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

# Edges: person↔person (relationship)
for r in relationships:
    if r["person_a"] == r["person_b"]:
        continue
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    context = esc(r.get("context",""))
    lines.append(f'      <edge id="e{edge_id}" source="sm_{p_a["id"]}" target="sm_{p_b["id"]}" label="{context}" weight="2.0">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{context}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF created: {GEXF_PATH}")
print(f"   Nodes: {len(persons) + len(organizations)} | Edges: {edge_id}")

conn.close()
print("✅ Done!")
