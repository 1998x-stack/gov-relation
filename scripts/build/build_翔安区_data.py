#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 翔安区 (Xiang'an District, Xiamen, Fujian).

翔安区 — 厦门市下辖区，2003年从同安区析出设立，辖7街道2镇。

Research date: 2026-07-16
Sources:
- 翔安区政府网站 (www.xiangan.gov.cn) — 领导信息页面
- 百度百科/维基百科 — 区情概况、区委书记简历
- 公开报道 — 任命信息、活动报道

Coverage: 区委书记、区长、副区长、区委常委，
前任书记/区长去向。

Confidence notes:
- 沈晓文（区长）：confirmed（官方领导信息页面）
- 李毅（区委书记）：confirmed（维基百科）
- 副区长信息：confirmed（官方领导信息页面）
- 区委常委：部分待确认
- 各人教育经历、具体时间节点：部分已确认，部分为plausible
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_翔安区")
DB_PATH = os.path.join(STAGING, "翔安区_network.db")
GEXF_PATH = os.path.join(STAGING, "翔安区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 李毅 — 翔安区委书记 (as of 2026.07)
    {"id":1,"name":"李毅","gender":"男","ethnicity":"汉族",
     "birth":"1974","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区委书记",
     "current_org":"中共翔安区委",
     "source":"维基百科 — 翔安区词条 (2025-12-23版)"},
    # 沈晓文 — 翔安区区长 (as of 2026.07)
    {"id":2,"name":"沈晓文","gender":"男","ethnicity":"汉族",
     "birth":"1983-10","birthplace":"","education":"研究生学历，理学博士",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区委副书记、区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息/区长/沈晓文"},

    # ── 2. 前任区委书记 ──
    # 黄鹤麟 — 原翔安区委书记 (2021.07-2024.07), 现海沧区区长
    {"id":3,"name":"黄鹤麟","gender":"男","ethnicity":"汉族",
     "birth":"1970-05","birthplace":"福建福州(出生地松溪)","education":"省委党校研究生，公共管理硕士",
     "party_join":"中共党员","work_start":"1991-08",
     "current_post":"海沧台商投资区管委会主任、海沧区区长",
     "current_org":"海沧区人民政府",
     "source":"海沧区数据 — 黄鹤麟履历"},

    # 游文昌 — 原翔安区委副书记、副区长（更早期），后任海沧区委书记、厦门市委常委、政法委书记
    {"id":4,"name":"游文昌","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"厦门市委常委、政法委书记",
     "current_org":"中共厦门市委政法委员会",
     "source":"海沧区数据"},

    # ── 3. 副区长（来源：翔安区政府网站领导信息）──
    {"id":5,"name":"邓小达","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区委常委、副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
    {"id":6,"name":"王永欣","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
    {"id":7,"name":"徐得志","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
    {"id":8,"name":"洪求瑛","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
    {"id":9,"name":"吕培勤","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
    {"id":10,"name":"张小博","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
    {"id":11,"name":"洪胜蓝","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
    {"id":12,"name":"叶捷频","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"翔安区副区长",
     "current_org":"翔安区人民政府",
     "source":"翔安区政府网站 — 领导信息"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共翔安区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"厦门市翔安区"},
    {"id":2,"name":"翔安区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"厦门市翔安区"},
    {"id":3,"name":"中共厦门市委","type":"党委","level":"副省级","parent":"中共福建省委","location":"厦门市思明区"},
    {"id":4,"name":"海沧区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"厦门市海沧区"},
    {"id":5,"name":"中共海沧区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"厦门市海沧区"},
    {"id":6,"name":"中共厦门市委政法委员会","type":"党委","level":"副省级","parent":"中共厦门市委","location":"厦门市思明区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 李毅 ──
    {"person_id":1,"org_id":1,"title":"翔安区委书记","start":"","end":"present","rank":"正处级","note":f"现任，截至{AS_OF}"},

    # ── 沈晓文 ──
    {"person_id":2,"org_id":1,"title":"翔安区委副书记","start":"","end":"present","rank":"正处级","note":f"现任，截至{AS_OF}"},
    {"person_id":2,"org_id":2,"title":"翔安区区长","start":"","end":"present","rank":"正处级","note":f"现任，截至{AS_OF}；主持区政府全面工作"},

    # ── 黄鹤麟（前任书记）──
    {"person_id":3,"org_id":1,"title":"翔安区委书记","start":"2021-07","end":"2024-07","rank":"正厅级","note":"正厅长级，后调任海沧区区长"},
    {"person_id":3,"org_id":4,"title":"海沧台商投资区管委会主任、海沧区区长","start":"2024-07","end":"present","rank":"正厅级","note":"现任"},

    # ── 游文昌 ──
    {"person_id":4,"org_id":1,"title":"翔安区委副书记、副区长","start":"","end":"","rank":"副厅级","note":""},
    {"person_id":4,"org_id":5,"title":"海沧区委书记","start":"2018","end":"2024-07","rank":"正厅级","note":"厦门市委常委"},
    {"person_id":4,"org_id":6,"title":"厦门市委常委、政法委书记","start":"2024-08","end":"present","rank":"副省级","note":"现任"},

    # ── 副区长 ──
    {"person_id":5,"org_id":2,"title":"翔安区委常委、副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
    {"person_id":6,"org_id":2,"title":"翔安区副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
    {"person_id":7,"org_id":2,"title":"翔安区副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
    {"person_id":8,"org_id":2,"title":"翔安区副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
    {"person_id":9,"org_id":2,"title":"翔安区副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
    {"person_id":10,"org_id":2,"title":"翔安区副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
    {"person_id":11,"org_id":2,"title":"翔安区副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
    {"person_id":12,"org_id":2,"title":"翔安区副区长","start":"","end":"present","rank":"副处级","note":f"现任，截至{AS_OF}"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政同僚
    {"person_a":1,"person_b":2,"type":"党政同僚","context":"翔安区委书记与区长搭档","overlap_org":"中共翔安区委/翔安区人民政府","overlap_period":f"{AS_OF}-"},
    # 前后任（区委书记）
    {"person_a":3,"person_b":1,"type":"前后任","context":"黄鹤麟→李毅 翔安区委书记交接","overlap_org":"中共翔安区委","overlap_period":"2024-07前后"},
    # 跨区关联
    {"person_a":3,"person_b":4,"type":"前后任","context":"游文昌→黄鹤麟 翔安区委书记前后任（游文昌早期曾任翔安区委副书记）","overlap_org":"中共翔安区委","overlap_period":"2021前后"},
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
        return (255,50,50)  # Red for Party Secretary
    if "区长" in t and "副" not in t:
        return (50,100,255)  # Blue for District Mayor
    if "副" in t and "区长" in t:
        return (100,150,255) # Lighter blue for deputies
    if "常委" in t:
        return (150,150,255)
    return (100,100,100)

def is_top_leader(p):
    t = p.get("current_post","") or ""
    return ("书记" in t and "副" not in t and "纪委" not in t)

def is_district_mayor(p):
    t = p.get("current_post","") or ""
    return ("区长" in t and "副" not in t) or ("县长" in t and "副" not in t)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>翔安区领导班子工作关系网络</description>')
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
    pid = f"xa_{p['id']}"
    c = color_for_role(p.get("current_post",""))
    sz = "20.0" if is_top_leader(p) else "15.0" if is_district_mayor(p) else "12.0"
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
    "default": (200,200,200)
}
for o in organizations:
    oid = f"xa_org_{o['id']}"
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
    lines.append(f'      <edge id="e{edge_id}" source="xa_{p["id"]}" target="xa_org_{o["id"]}" label="{label}" weight="1.0">')
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
    lines.append(f'      <edge id="e{edge_id}" source="xa_{p_a["id"]}" target="xa_{p_b["id"]}" label="{context}" weight="2.0">')
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
