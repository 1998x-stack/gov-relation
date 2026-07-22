#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 永登县 (Yongdeng County, Lanzhou, Gansu) leadership network.

永登县 — 甘肃省兰州市下辖县.
Targets: 县委书记 (王彦群), 县长 (贾文涛).
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_永登县")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "永登县_network.db")
GEXF_PATH = os.path.join(STAGING, "永登县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. County top leadership ──

    # 王彦群 — 永登县委书记 (as of 兰州市数据 2026)
    {"id": 1, "name": "王彦群", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永登县委书记",
     "current_org": "中共永登县委",
     "source": "兰州市领导班子数据"},

    # 贾文涛 — 永登县县长 (as of 兰州市数据 2026)
    {"id": 2, "name": "贾文涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永登县人民政府县长",
     "current_org": "永登县人民政府",
     "source": "兰州市领导班子数据"},

    # ── B. Key deputies (县委常委会/县政府) ──

    # 县委副书记（通常兼任县长，或专职副书记）
    # 永登县委专职副书记 — 待查具体姓名
    {"id": 3, "name": "待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永登县委副书记（专职）",
     "current_org": "中共永登县委",
     "source": ""},

    # 常务副县长 — 待查
    {"id": 4, "name": "待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永登县委常委、常务副县长",
     "current_org": "永登县人民政府",
     "source": ""},

    # 纪委书记
    {"id": 5, "name": "待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永登县委常委、纪委书记、监委主任",
     "current_org": "中共永登县纪律检查委员会",
     "source": ""},

    # 组织部部长
    {"id": 6, "name": "待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永登县委常委、组织部部长",
     "current_org": "中共永登县委组织部",
     "source": ""},

    # 宣传部部长
    {"id": 7, "name": "待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永登县委常委、宣传部部长",
     "current_org": "中共永登县委宣传部",
     "source": ""},

    # 政法委书记
    {"id": 8, "name": "待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永登县委常委、政法委书记",
     "current_org": "中共永登县委政法委员会",
     "source": ""},

    # ── C. Predecessors ──

    # 前任县委书记 — 待查
    {"id": 9, "name": "待查（前任县委书记）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "已离任（原永登县委书记）",
     "current_org": "",
     "source": ""},

    # 前任县长 — 待查
    {"id": 10, "name": "待查（前任县长）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "已离任（原永登县县长）",
     "current_org": "",
     "source": ""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共永登县委", "type": "党委", "level": "县级",
     "parent": "中共兰州市委员会", "location": "甘肃省兰州市永登县"},
    {"id": 2, "name": "永登县人民政府", "type": "政府", "level": "县级",
     "parent": "兰州市人民政府", "location": "甘肃省兰州市永登县"},
    {"id": 3, "name": "永登县人大常委会", "type": "人大", "level": "县级",
     "parent": "", "location": "甘肃省兰州市永登县"},
    {"id": 4, "name": "永登县政协", "type": "政协", "level": "县级",
     "parent": "", "location": "甘肃省兰州市永登县"},
    {"id": 5, "name": "中共永登县纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "中共永登县委", "location": "甘肃省兰州市永登县"},
    {"id": 6, "name": "中共永登县委组织部", "type": "党委", "level": "县级",
     "parent": "中共永登县委", "location": "甘肃省兰州市永登县"},
    {"id": 7, "name": "中共永登县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共永登县委", "location": "甘肃省兰州市永登县"},
    {"id": 8, "name": "中共永登县委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共永登县委", "location": "甘肃省兰州市永登县"},
    {"id": 9, "name": "中共兰州市委员会", "type": "党委", "level": "副省级",
     "parent": "中共甘肃省委员会", "location": "甘肃省兰州市"},
    {"id": 10, "name": "兰州市人民政府", "type": "政府", "level": "副省级",
     "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
]

# =========================================================================
# POSITIONS (current)
# =========================================================================
positions = [
    # Top leaders
    {"person_id": 1, "org_id": 1, "title": "永登县委书记", "start": "", "end": "",
     "rank": "正处", "note": "现任县委书记"},
    {"person_id": 2, "org_id": 2, "title": "永登县人民政府县长", "start": "", "end": "",
     "rank": "正处", "note": "现任县长"},
    # Deputies
    {"person_id": 3, "org_id": 1, "title": "永登县委副书记", "start": "", "end": "",
     "rank": "副处", "note": "姓名待查"},
    {"person_id": 4, "org_id": 2, "title": "永登县委常委、常务副县长", "start": "", "end": "",
     "rank": "副处", "note": "姓名待查"},
    {"person_id": 5, "org_id": 5, "title": "永登县委常委、纪委书记、监委主任", "start": "", "end": "",
     "rank": "副处", "note": "姓名待查"},
    {"person_id": 6, "org_id": 6, "title": "永登县委常委、组织部部长", "start": "", "end": "",
     "rank": "副处", "note": "姓名待查"},
    {"person_id": 7, "org_id": 7, "title": "永登县委常委、宣传部部长", "start": "", "end": "",
     "rank": "副处", "note": "姓名待查"},
    {"person_id": 8, "org_id": 8, "title": "永登县委常委、政法委书记", "start": "", "end": "",
     "rank": "副处", "note": "姓名待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # County top leadership pair
    {"person_a": 1, "person_b": 2, "type": "党政同僚",
     "context": "永登县委书记与县长搭档",
     "overlap_org": "永登县", "overlap_period": "2023-"},
]

# =========================================================================
# BUILD DATABASE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

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

print(f"✅ 数据库已创建: {DB_PATH}")
print(f"   人物: {person_count} | 机构: {org_count} | 任职: {pos_count} | 关系: {rel_count}")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def color_for_role(title):
    t = title or ""
    if "书记" in t and "纪委" not in t and ("副" not in t[:t.index("书记")] if "书记" in t else True):
        return "#E03C31"
    if "县长" in t and "副" not in t:
        return "#4a7fc7"
    if "人大" in t:
        return "#5a7a9a"
    if "政协" in t:
        return "#7a5a9a"
    if "纪委" in t:
        return "#d4880f"
    if "副书记" in t:
        return "#E07A31"
    if "副县长" in t:
        return "#6a8fe7"
    return "#888888"


def org_color(org_type):
    colors = {"党委": "rgba(200,50,50,0.3)", "政府": "rgba(50,100,200,0.3)",
              "人大": "rgba(90,122,154,0.3)", "政协": "rgba(122,90,154,0.3)",
              "纪委": "rgba(200,150,20,0.3)"}
    return colors.get(org_type, "rgba(200,200,200,0.3)")


ged_lines = []
ged_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
ged_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
ged_lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
ged_lines.append('    <creator>China Gov Network Investigator</creator>')
ged_lines.append('    <description>永登县领导班子工作关系网络</description>')
ged_lines.append('  </meta>')
ged_lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
ged_lines.append('    <attributes class="node">')
ged_lines.append('      <attribute id="0" title="type" type="string"/>')
ged_lines.append('      <attribute id="1" title="role" type="string"/>')
ged_lines.append('      <attribute id="2" title="org" type="string"/>')
ged_lines.append('      <attribute id="3" title="birth" type="string"/>')
ged_lines.append('      <attribute id="4" title="birthplace" type="string"/>')
ged_lines.append('    </attributes>')

# Edge attributes
ged_lines.append('    <attributes class="edge">')
ged_lines.append('      <attribute id="0" title="type" type="string"/>')
ged_lines.append('      <attribute id="1" title="context" type="string"/>')
ged_lines.append('    </attributes>')

# Person nodes
ged_lines.append('    <nodes>')
for p in persons:
    slug_id = f"yongdeng_p{p['id']}"
    role_color = color_for_role(p["current_post"])
    r_val = int(role_color[1:3], 16)
    g_val = int(role_color[3:5], 16)
    b_val = int(role_color[5:7], 16)

    is_top = ("书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "")
              and "副" not in (p["current_post"] or ""))
    is_gov = ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
    size = 20.0 if is_top else 15.0 if is_gov else 12.0

    label = f"{p['name']} ({p['current_post'] or '?'})"
    ged_lines.append(f'      <node id="{slug_id}" label="{esc(label)}">')
    ged_lines.append('        <attvalues>')
    ged_lines.append(f'          <attvalue for="0" value="person"/>')
    ged_lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    ged_lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    ged_lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
    ged_lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
    ged_lines.append('        </attvalues>')
    ged_lines.append(f'        <viz:color r="{r_val}" g="{g_val}" b="{b_val}"/>')
    ged_lines.append(f'        <viz:size value="{size}"/>')
    ged_lines.append('      </node>')

# Organization nodes
for o in organizations:
    oid = f"yongdeng_org_{o['id']}"
    oc = org_color(o["type"])
    oc_rgb = oc.replace("rgba(", "").rstrip(")").split(",")
    ged_lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    ged_lines.append('        <attvalues>')
    ged_lines.append(f'          <attvalue for="0" value="organization"/>')
    ged_lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    ged_lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
    ged_lines.append('        </attvalues>')
    ged_lines.append(f'        <viz:color r="{int(oc_rgb[0])}" g="{int(oc_rgb[1])}" b="{int(oc_rgb[2])}"/>')
    ged_lines.append(f'        <viz:size value="8.0"/>')
    ged_lines.append('      </node>')

ged_lines.append('    </nodes>')

# Edges
ged_lines.append('    <edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = f"{p['name']} → {o['name']} ({po['title']})"
    ged_lines.append(
        f'      <edge id="e{edge_id}" source="yongdeng_p{p["id"]}" target="yongdeng_org{o["id"]}" '
        f'label="{esc(label)}" weight="1.0">')
    ged_lines.append('        <attvalues>')
    ged_lines.append(f'          <attvalue for="0" value="worked_at"/>')
    ged_lines.append(          f'          <attvalue for="1" value="{esc(po["title"] + " (" + po["start"] + " – " + po["end"] + ")")}"/>')
    ged_lines.append('        </attvalues>')
    ged_lines.append('      </edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    ged_lines.append(
        f'      <edge id="e{edge_id}" source="yongdeng_p{p_a["id"]}" target="yongdeng_p{p_b["id"]}" '
        f'label="{esc(r["context"])}" weight="2.0">')
    ged_lines.append('        <attvalues>')
    ged_lines.append(f'          <attvalue for="0" value="relationship"/>')
    ged_lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    ged_lines.append('        </attvalues>')
    ged_lines.append('      </edge>')

ged_lines.append('    </edges>')
ged_lines.append('  </graph>')
ged_lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(ged_lines))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
