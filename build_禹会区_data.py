#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 蚌埠市禹会区 leadership network."""

import sqlite3
import os
from datetime import date

DB_DIR = "data/database"
GRAPH_DIR = "data/graph"
DB_PATH = os.path.join(DB_DIR, "禹会区_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "禹会区_network.gexf")
TODAY = "2026-07-15"

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────
# Research date: 2026-07-15
# Source: yuhui.gov.cn official website news articles
# Confirmed current: 区委书记张斌 (elected at 五届区委第一次全体会议 2026-06-25)

persons = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    ("yuhui_zhang_bin", "张斌", "男", "汉族", "", "", "", "", "",
     "区委书记", "中共蚌埠市禹会区委",
     "https://www.yuhui.gov.cn/zfyw/5094378.html"),
    ("yuhui_quzhang_unknown", "（待核实）", "", "", "", "", "", "", "",
     "区长（待核实）", "禹会区人民政府",
     "待确认来自官方来源"),
    # Predecessors — 张斌的前任
    ("yuhui_predecessor_unknown", "（前任区委书记待核实）", "", "", "", "", "", "", "",
     "前任区委书记", "中共蚌埠市禹会区委（已离任）",
     "待核实"),
]

organizations = [
    ("yuhui_party", "中共蚌埠市禹会区委员会", "党委", "县处级", "中共蚌埠市委", "安徽蚌埠"),
    ("yuhui_gov", "禹会区人民政府", "政府", "县处级", "中共蚌埠市禹会区委", "安徽蚌埠"),
    ("yuhui_discipline", "中共蚌埠市禹会区纪律检查委员会", "纪委", "县处级", "中共蚌埠市禹会区委", "安徽蚌埠"),
    ("yuhui_party_office", "中共蚌埠市禹会区委办公室", "党委部门", "正科级", "中共蚌埠市禹会区委", "安徽蚌埠"),
    ("yuhui_gov_office", "禹会区人民政府办公室", "政府部门", "正科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_org_dept", "中共蚌埠市禹会区委组织部", "党委部门", "正科级", "中共蚌埠市禹会区委", "安徽蚌埠"),
    ("yuhui_propaganda", "中共蚌埠市禹会区委宣传部", "党委部门", "正科级", "中共蚌埠市禹会区委", "安徽蚌埠"),
    ("yuhui_united_front", "中共蚌埠市禹会区委统战部", "党委部门", "正科级", "中共蚌埠市禹会区委", "安徽蚌埠"),
    ("yuhui_politics_law", "中共蚌埠市禹会区委政法委员会", "党委部门", "正科级", "中共蚌埠市禹会区委", "安徽蚌埠"),
    ("yuhui_people_congress", "蚌埠市禹会区人民代表大会常务委员会", "人大", "县处级", "", "安徽蚌埠"),
    ("yuhui_cppcc", "中国人民政治协商会议蚌埠市禹会区委员会", "政协", "县处级", "", "安徽蚌埠"),
    # Sub-district/town organizations
    ("yuhui_chao_yang", "禹会区朝阳街道", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_wei_si", "禹会区纬四街道", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_da_qing", "禹会区大庆街道", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_zhang_gong_shan", "禹会区张公山街道", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_diao_yu_tai", "禹会区钓鱼台街道", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_qin_ji", "禹会区秦集镇（蚌埠高新区托管）", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_ma_cheng", "禹会区马城镇", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
    ("yuhui_chang_qing", "禹会区长青乡", "乡镇/街道", "乡科级", "禹会区人民政府", "安徽蚌埠"),
]

positions = [
    # 张斌 - 区委书记
    (1, "yuhui_zhang_bin", "yuhui_party", "区委书记", "2026-06", "", "正处级",
     "2026年6月24日中共蚌埠市禹会区第五次代表大会闭幕；6月24日五届区委第一次全体会议选举为区委书记"),
    (2, "yuhui_zhang_bin", "yuhui_people_congress", "区人大常委会主任（可能兼任）", "未知", "", "正处级",
     "待核实是否兼任区人大常委会主任"),
    # 区长待核实
    (3, "yuhui_quzhang_unknown", "yuhui_gov", "区长", "未知", "", "正处级",
     "现任区长姓名待从官方来源核实"),
]

relationships = [
]

# ── Build SQLite ──────────────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    );
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)
for po in positions:
    cur.execute("INSERT OR REPLACE INTO positions (id, person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?,?)", po)
for r in relationships:
    cur.execute("INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r[1:])

conn.commit()
conn.close()
print(f"✅ SQLite: {DB_PATH}")

# ── Build GEXF ────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def hex_color_to_rgb(hex_str):
    """Convert #RRGGBB to (r,g,b) ints."""
    h = hex_str.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

nodes_xml = ""
edges_xml = ""

# Person nodes
for p in persons:
    pid = p[0]
    name = p[1]
    role = p[9] if p[9] else "未知"
    # Color by role
    if "书记" in role and "区委" in role:
        color = "#E03C31"  # Red — party secretary
        size = 20.0
    elif "区长" in role and "副" not in role:
        color = "#2B7CE9"  # Blue — government head
        size = 20.0
    elif "副区长" in role or "副市长" in role:
        color = "#2B7CE9"
        size = 12.0
    elif "纪委" in role:
        color = "#FF8C00"  # Orange — discipline
        size = 12.0
    else:
        color = "#888888"  # Grey — other
        size = 12.0

    r_, g_, b_ = hex_color_to_rgb(color)
    nodes_xml += f"""      <node id="{esc(pid)}" label="{esc(name)}">
        <attvalues>
          <attvalue for="type" value="person"/>
          <attvalue for="role" value="{esc(role)}"/>
        </attvalues>
        <viz:color r="{r_}" g="{g_}" b="{b_}"/>
        <viz:size value="{size}"/>
        <viz:position x="0" y="0" z="0"/>
      </node>\n"""

# Organization nodes
org_color_map = {
    "党委": "#8B0000",
    "党委部门": "#A52A2A",
    "政府": "#1E90FF",
    "政府部门": "#4169E1",
    "纪委": "#FF8C00",
    "人大": "#2E8B57",
    "政协": "#2E8B57",
    "乡镇/街道": "#DAA520",
}
for o in organizations:
    oid = o[0]
    oname = o[1]
    otype = o[2]
    color = org_color_map.get(otype, "#666666")
    r_, g_, b_ = hex_color_to_rgb(color)
    nodes_xml += f"""      <node id="{esc(oid)}" label="{esc(oname)}">
        <attvalues>
          <attvalue for="type" value="organization"/>
          <attvalue for="org_type" value="{esc(otype)}"/>
        </attvalues>
        <viz:color r="{r_}" g="{g_}" b="{b_}"/>
        <viz:size value="8.0"/>
        <viz:position x="0" y="0" z="0"/>
      </node>\n"""

# Edges: person → organization (worked_at)
for po in positions:
    pid = po[1]
    oid = po[2]
    title = po[3] if po[3] else ""
    start = po[4] if po[4] else ""
    end = po[5] if po[5] else ""
    edges_xml += f"""      <edge id="e_w_{po[0]}" source="{esc(pid)}" target="{esc(oid)}" type="directed" label="{esc(title)}">
        <attvalues>
          <attvalue for="edge_type" value="worked_at"/>
          <attvalue for="title" value="{esc(title)}"/>
          <attvalue for="start" value="{esc(start)}"/>
          <attvalue for="end" value="{esc(end)}"/>
        </attvalues>
      </edge>\n"""

# Edges: person ↔ person (relationship)
eid = 1000
for r in relationships:
    a, b, rtype, ctx, overlap_org, overlap_period = r[1], r[2], r[3], r[4] if len(r) > 4 else "", r[5] if len(r) > 5 else "", r[6] if len(r) > 6 else ""
    color_str = "#C9A94E"
    thickness = 2.0
    r_, g_, b_ = hex_color_to_rgb(color_str)
    edges_xml += f"""      <edge id="e_r_{eid}" source="{esc(a)}" target="{esc(b)}" type="undirected" label="{esc(rtype)}">
        <attvalues>
          <attvalue for="edge_type" value="relationship"/>
          <attvalue for="relationship_type" value="{esc(rtype)}"/>
          <attvalue for="context" value="{esc(ctx)}"/>
          <attvalue for="overlap_org" value="{esc(overlap_org)}"/>
          <attvalue for="overlap_period" value="{esc(overlap_period)}"/>
        </attvalues>
        <viz:color r="{r_}" g="{g_}" b="{b_}"/>
        <viz:thickness value="{thickness}"/>
      </edge>\n"""
    eid += 1

gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">
  <meta>
    <creator>Gov Relation Investigator</creator>
    <description>蚌埠市禹会区领导工作关系网络 — built {TODAY}</description>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="type" title="Type" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="org_type" title="Org Type" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="edge_type" title="Edge Type" type="string"/>
      <attribute id="title" title="Title" type="string"/>
      <attribute id="start" title="Start" type="string"/>
      <attribute id="end" title="End" type="string"/>
      <attribute id="relationship_type" title="Relationship Type" type="string"/>
      <attribute id="context" title="Context" type="string"/>
      <attribute id="overlap_org" title="Overlap Org" type="string"/>
      <attribute id="overlap_period" title="Overlap Period" type="string"/>
    </attributes>
    <nodes>
{nodes_xml}    </nodes>
    <edges>
{edges_xml}    </edges>
  </graph>
</gexf>"""

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(gexf)
print(f"✅ GEXF: {GEXF_PATH}")

# ── Summary ───────────────────────────────────────────────────────────

print(f"\n📊 Summary:")
print(f"   Persons:      {len(persons)}")
print(f"   Orgs:         {len(organizations)}")
print(f"   Positions:    {len(positions)}")
print(f"   Relationships: {len(relationships)}")
print(f"\n⚠️  Note: 区长姓名尚未确认（待后续调查补充）。")
