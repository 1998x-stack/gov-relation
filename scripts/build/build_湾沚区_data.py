#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 芜湖市湾沚区 (Wanzhi District, Wuhu City, Anhui) leadership network.

湾沚区 — 安徽省芜湖市下辖区, 原芜湖县, 2020年撤县设区.
Data current as of July 2026. Sources: wanzhi.gov.cn (official), public reports.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/湾沚区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/湾沚区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── A. District-level top leadership ──
    # Party Secretary
    {"id": 1, "name": "李炜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区委书记",
     "current_org": "中共湾沚区委",
     "source": "芜湖市湾沚区人民政府网站 wanzhi.gov.cn 公开报道(2026年7月)"},
    # District Mayor
    {"id": 2, "name": "马荣", "gender": "男", "ethnicity": "回族",
     "birth": "1978-04", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区委副书记、区长",
     "current_org": "湾沚区人民政府",
     "source": "芜湖市湾沚区人民政府网站 wanzhi.gov.cn 领导之窗"},

    # ── B. District-level other key leaders ──
    # Deputy Party Secretary
    {"id": 3, "name": "张涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区委副书记、湾沚镇党委书记",
     "current_org": "中共湾沚区委",
     "source": "芜湖市湾沚区人民政府网站 公开报道(2026年7月)"},
    # NPC Standing Committee Chair
    {"id": 4, "name": "陶庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区人大常委会主任",
     "current_org": "湾沚区人大常委会",
     "source": "芜湖市湾沚区人民政府网站 公开报道(2026年7月)"},
    # CPPCC Chair
    {"id": 5, "name": "单增劲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区政协党组书记、主席候选人",
     "current_org": "湾沚区政协",
     "source": "芜湖市湾沚区人民政府网站 公开报道(2026年7月)"},

    # ── C. District government deputy leaders ──
    # Executive Deputy Mayor
    {"id": 6, "name": "徐江宝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区委常委、常务副区长",
     "current_org": "湾沚区人民政府",
     "source": "芜湖市湾沚区人民政府网站 领导之窗"},
    # Deputy Mayor
    {"id": 7, "name": "蔡传林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区委常委、副区长",
     "current_org": "湾沚区人民政府",
     "source": "芜湖市湾沚区人民政府网站 领导之窗"},
    # Deputy Mayor
    {"id": 8, "name": "后向前", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区副区长",
     "current_org": "湾沚区人民政府",
     "source": "芜湖市湾沚区人民政府网站 领导之窗"},
    # Deputy Mayor
    {"id": 9, "name": "吴毅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区副区长",
     "current_org": "湾沚区人民政府",
     "source": "芜湖市湾沚区人民政府网站 领导之窗"},
    # Deputy Mayor
    {"id": 10, "name": "缪青", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区副区长",
     "current_org": "湾沚区人民政府",
     "source": "芜湖市湾沚区人民政府网站 领导之窗"},
    # Deputy Mayor candidate
    {"id": 11, "name": "熊文哲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区副区长人选",
     "current_org": "湾沚区人民政府",
     "source": "芜湖市湾沚区人民政府网站 领导之窗"},

    # ── D. Predecessors (historical) ──
    # Former Party Secretary
    {"id": 12, "name": "殷琼", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市政协副主席（原湾沚区委书记2022-2025）",
     "current_org": "芜湖市政协",
     "source": "公开报道; 原芜湖市领导班子数据"},
]

organizations = [
    # District-level
    {"id": 1, "name": "中共湾沚区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "湾沚区"},
    {"id": 2, "name": "湾沚区人民政府", "type": "政府", "level": "县级", "parent": "芜湖市人民政府", "location": "湾沚区"},
    {"id": 3, "name": "湾沚区人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "湾沚区"},
    {"id": 4, "name": "湾沚区政协", "type": "政协", "level": "县级", "parent": "", "location": "湾沚区"},
    {"id": 5, "name": "芜湖市政协", "type": "政协", "level": "地厅级", "parent": "", "location": "芜湖市"},
    # Towns
    {"id": 6, "name": "中共湾沚镇委员会", "type": "党委", "level": "乡级", "parent": "中共湾沚区委", "location": "湾沚镇"},
    {"id": 7, "name": "芜湖市人民政府", "type": "政府", "level": "地厅级", "parent": "", "location": "芜湖市"},
]

positions = [
    # District top leaders
    {"person_id": 1, "org_id": 1, "title": "湾沚区委书记", "start": "2025?", "end": "", "rank": "正处", "note": "前任为殷琼"},
    {"person_id": 2, "org_id": 2, "title": "湾沚区区长", "start": "2025?", "end": "", "rank": "正处", "note": "区委副书记、区政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "湾沚区委副书记", "start": "2025?", "end": "", "rank": "正处", "note": ""},
    # Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "湾沚区委副书记", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "湾沚镇党委书记", "start": "", "end": "", "rank": "正科", "note": ""},
    # NPC / CPPCC
    {"person_id": 4, "org_id": 3, "title": "湾沚区人大常委会主任", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "湾沚区政协党组书记、主席候选人", "start": "2026?", "end": "", "rank": "正处", "note": ""},
    # Deputy Mayors
    {"person_id": 6, "org_id": 1, "title": "湾沚区委常委", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "湾沚区常务副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "湾沚区委常委", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "湾沚区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "湾沚区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "湾沚区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "湾沚区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "湾沚区副区长人选", "start": "2026?", "end": "", "rank": "副处", "note": ""},
    # Predecessors
    {"person_id": 12, "org_id": 1, "title": "湾沚区委书记", "start": "2022", "end": "2025?", "rank": "正处", "note": "前任区委书记"},
    {"person_id": 12, "org_id": 5, "title": "芜湖市政协副主席", "start": "2022", "end": "", "rank": "副厅", "note": "兼湾沚区委书记（前期）"},
]

relationships = [
    # Top leadership pair
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "湾沚区委书记与区长搭档", "overlap_org": "湾沚区", "overlap_period": "2025?-"},
    # Party Secretary ↔ other leaders
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委副书记（兼湾沚镇党委书记）", "overlap_org": "中共湾沚区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与区人大主任", "overlap_org": "湾沚区", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与区政协主席候选人", "overlap_org": "湾沚区", "overlap_period": ""},
    # Mayor ↔ Deputy Mayors
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与常务副区长搭档", "overlap_org": "湾沚区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长与区委常委副区长", "overlap_org": "湾沚区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长", "overlap_org": "湾沚区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与副区长", "overlap_org": "湾沚区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长", "overlap_org": "湾沚区人民政府", "overlap_period": ""},
    # Predecessor-successor
    {"person_a": 12, "person_b": 1, "type": "前后任", "context": "殷琼→李炜 湾沚区委书记交接", "overlap_org": "中共湾沚区委", "overlap_period": "2025?"},
    # Standing Committee overlaps
    {"person_a": 1, "person_b": 6, "type": "党政同僚", "context": "区委书记与常务副区委常委", "overlap_org": "中共湾沚区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "党政同僚", "context": "区委书记与区委常委副区长", "overlap_org": "中共湾沚区委", "overlap_period": ""},
    # Same-system
    {"person_a": 12, "person_b": 1, "type": "前后任", "context": "殷琼→李炜", "overlap_org": "中共湾沚区委", "overlap_period": "2025?"},
]

# ── BUILD DATABASE ──────────────────────────────────────────────────

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

# ── Print summary ──
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

# ── BUILD GEXF ──────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def color_for_role(title):
    t = title or ""
    if "书记" in t and "纪委" not in t and ("副" not in t[:t.index("书记")+2] if "书记" in t else True):
        return "#FF3232"
    if ("区长" in t and "副" not in t) or ("县长" in t and "副" not in t):
        return "#3264FF"
    if "人大" in t:
        return "#3A7A9A"
    if "政协" in t:
        return "#7A5A9A"
    if "纪委" in t:
        return "#FFA500"
    if "副书记" in t:
        return "#E07A31"
    if "副区长" in t:
        return "#6A8FE7"
    return "#888888"

def org_color(org_type):
    return {"党委": "rgba(255,200,200,0.3)", "政府": "rgba(200,200,255,0.3)",
            "人大": "rgba(200,255,255,0.3)", "政协": "rgba(255,240,200,0.3)",
            "纪委": "rgba(255,165,0,0.3)", "开发区": "rgba(200,255,200,0.3)",
            "乡镇/街道": "rgba(255,255,200,0.3)"}.get(org_type, "rgba(200,200,200,0.3)")

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
gexf_parts.append('    <creator>Claude Code Research Agent</creator>')
gexf_parts.append('    <description>芜湖市湾沚区领导班子工作关系网络</description>')
gexf_parts.append('  </meta>')
gexf_parts.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
gexf_parts.append('    <attributes class="node">')
gexf_parts.append('      <attribute id="0" title="type" type="string"/>')
gexf_parts.append('      <attribute id="1" title="role" type="string"/>')
gexf_parts.append('      <attribute id="2" title="org" type="string"/>')
gexf_parts.append('    </attributes>')
gexf_parts.append('    <attributes class="edge">')
gexf_parts.append('      <attribute id="0" title="type" type="string"/>')
gexf_parts.append('      <attribute id="1" title="title" type="string"/>')
gexf_parts.append('      <attribute id="2" title="context" type="string"/>')
gexf_parts.append('    </attributes>')

# Nodes
gexf_parts.append('    <nodes>')
for p in persons:
    slug_id = f"p{p['id']}"
    c = color_for_role(p["current_post"])
    # Determine if top leader
    is_top = False
    if "书记" in (p["current_post"] or ""):
        if "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or ""):
            is_top = True
    is_mayor = ("区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or \
               ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
    sz = "20.0" if is_top else "15.0" if is_mayor else "12.0"
    label = f"{p['name']} ({p['current_post'] or '?'})"
    gexf_parts.append(f'      <node id="{slug_id}" label="{esc(label)}">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="0" value="person"/>')
    gexf_parts.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    gexf_parts.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    gexf_parts.append(f'        </attvalues>')
    r, g, b = c[1:3], c[3:5], c[5:7]
    gexf_parts.append(f'        <viz:color r="{int(r,16)}" g="{int(g,16)}" b="{int(b,16)}"/>')
    gexf_parts.append(f'        <viz:size value="{sz}"/>')
    gexf_parts.append(f'      </node>')

for o in organizations:
    oid = f"o{o['id']}"
    oc = org_color(o["type"])
    oc_rgb = oc.replace("rgba(", "").rstrip(")").split(",")
    gexf_parts.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="0" value="org"/>')
    gexf_parts.append(f'          <attvalue for="1" value=""/>')
    gexf_parts.append(f'          <attvalue for="2" value=""/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'        <viz:color r="{int(oc_rgb[0])}" g="{int(oc_rgb[1])}" b="{int(oc_rgb[2])}"/>')
    gexf_parts.append(f'        <viz:size value="8.0"/>')
    gexf_parts.append(f'      </node>')
gexf_parts.append('    </nodes>')

# Edges
gexf_parts.append('    <edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = f"{p['name']} → {o['name']} ({po['title']})"
    gexf_parts.append(f'      <edge id="e{edge_id}" source="p{p["id"]}" target="o{o["id"]}" label="{esc(label)}" weight="1.0">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="0" value="worked_at"/>')
    gexf_parts.append(f'          <attvalue for="1" value="{esc(po["title"])}"/>')
    gexf_parts.append(f'          <attvalue for="2" value=""/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'      </edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    gexf_parts.append(f'      <edge id="e{edge_id}" source="p{p_a["id"]}" target="p{p_b["id"]}" label="{esc(r["context"])}" weight="2.0">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="0" value="relationship"/>')
    gexf_parts.append(f'          <attvalue for="1" value=""/>')
    gexf_parts.append(f'          <attvalue for="2" value="{esc(r["context"])}"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'      </edge>')

gexf_parts.append('    </edges>')
gexf_parts.append('  </graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
