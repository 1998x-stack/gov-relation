#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 株洲市 leadership network."""

import sqlite3
import os
from datetime import date

DB_DIR = "data/database"
GRAPH_DIR = "data/graph"
DB_PATH = os.path.join(DB_DIR, "zhuzhou_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "zhuzhou_network.gexf")
TODAY = "2026-07-14"

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────

persons = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    ("zhuzhou_wang_jianqiu", "王建球", "男", "汉族", "", "", "", "", "",
     "市委书记", "中共株洲市委",
     "http://district.ce.cn/newarea/sddy/202606/t20260610_3021728.shtml"),
    ("zhuzhou_he_enguang", "何恩广", "男", "汉族", "", "", "", "", "",
     "市委副书记、代市长", "株洲市人民政府",
     "https://www.zhuzhou.gov.cn/c15633/index.html"),
    ("zhuzhou_zhou_yanxi", "周艳希", "女", "汉族", "", "", "", "", "",
     "市委副书记、市委政法委书记", "中共株洲市委",
     "http://www.zhuzhou.gov.cn/c15124/20260626/i2508741.html"),
    ("zhuzhou_yang_wangping", "阳望平", "男", "汉族", "", "", "", "", "",
     "市委常委、市委组织部部长", "中共株洲市委",
     "http://www.zhuzhou.gov.cn/c15124/20260626/i2508741.html"),
    ("zhuzhou_yang_yingjie", "杨英杰", "男", "汉族", "", "", "", "", "",
     "市委常委、市委秘书长", "中共株洲市委",
     "http://www.zhuzhou.gov.cn/c15124/20260626/i2508741.html"),
    ("zhuzhou_jiang_xiaozhong", "江小忠", "女", "汉族", "", "", "", "", "",
     "市委常委（推测宣传部部长）", "中共株洲市委",
     "http://www.zhuzhou.gov.cn/c15124/20260626/i2508741.html"),
    ("zhuzhou_luo_shaoyun", "罗绍昀", "男", "汉族", "", "", "", "", "",
     "市委常委", "中共株洲市委",
     "http://www.zhuzhou.gov.cn/c15124/20260626/i2508741.html"),
    ("zhuzhou_liu_yaliang", "刘亚亮", "男", "汉族", "", "", "", "", "",
     "市委常委、常务副市长", "株洲市人民政府",
     "https://www.zhuzhou.gov.cn/c20413/index.html"),
    ("zhuzhou_luo_houqing", "罗厚清", "男", "汉族", "", "", "", "", "",
     "市委常委（推测市纪委书记）", "中共株洲市委",
     "http://www.zhuzhou.gov.cn/c15124/20260626/i2508741.html"),
    ("zhuzhou_he_huixin", "何慧新", "女", "汉族", "", "", "", "", "",
     "市委常委、副市长", "株洲市人民政府",
     "https://www.zhuzhou.gov.cn/c23748/index.html"),
    ("zhuzhou_hou_hongguang", "侯宏光", "男", "汉族", "", "", "", "", "",
     "市委常委（推测株洲军分区）", "株洲军分区",
     "http://www.zhuzhou.gov.cn/c15124/20260626/i2508741.html"),
    # Predecessors
    ("zhuzhou_cao_huiquan", "曹慧泉", "男", "汉族", "1966-03", "湖南益阳", "博士", "", "",
     "前任株洲市委书记（另有任用）", "中共湖南省委（待公布）",
     "https://zh.wikipedia.org/wiki/曹慧泉"),
    ("zhuzhou_mao_tengfei", "毛腾飞", "男", "汉族", "1962-10", "湖南武冈", "博士", "", "",
     "前株洲市委书记（已落马）", "湖南省政协（降为四级主任科员）",
     "https://zh.wikipedia.org/wiki/毛腾飞"),
]

organizations = [
    ("zhu_zhou_party", "中共株洲市委", "党委", "地市级", "", "湖南株洲"),
    ("zhu_zhou_gov", "株洲市人民政府", "政府", "地市级", "中共株洲市委", "湖南株洲"),
    ("zhu_zhou_politics_law", "中共株洲市委政法委员会", "党委部门", "地市级", "中共株洲市委", "湖南株洲"),
    ("zhu_zhou_organization", "中共株洲市委组织部", "党委部门", "地市级", "中共株洲市委", "湖南株洲"),
    ("zhu_zhou_propaganda", "中共株洲市委宣传部", "党委部门", "地市级", "中共株洲市委", "湖南株洲"),
    ("zhu_zhou_discipline", "中共株洲市纪律检查委员会", "纪委", "地市级", "中共株洲市委", "湖南株洲"),
    ("zhu_zhou_military", "株洲军分区", "军队", "地市级", "", "湖南株洲"),
    ("hunan_industry_it", "湖南省工业和信息化厅", "省政府部门", "厅级", "", "湖南长沙"),
    ("hunan_cppcc", "湖南省政协", "政协", "省级", "", "湖南长沙"),
]

positions = [
    (1, "zhuzhou_wang_jianqiu", "zhu_zhou_party", "市委书记", "2026-06", "", "正厅级", ""),
    (2, "zhuzhou_he_enguang", "zhu_zhou_party", "市委副书记", "2026-??", "", "副厅级", ""),
    (3, "zhuzhou_he_enguang", "zhu_zhou_gov", "代市长", "2026-??", "", "正厅级", "市人民政府党组书记"),
    (4, "zhuzhou_zhou_yanxi", "zhu_zhou_party", "市委副书记", "2025-??", "", "副厅级", ""),
    (5, "zhuzhou_zhou_yanxi", "zhu_zhou_politics_law", "市委政法委书记", "2025-??", "", "副厅级", ""),
    (6, "zhuzhou_yang_wangping", "zhu_zhou_organization", "市委组织部部长", "2025-??", "", "副厅级", "市委常委"),
    (7, "zhuzhou_yang_yingjie", "zhu_zhou_party", "市委秘书长", "2025-??", "", "副厅级", "市委常委"),
    (8, "zhuzhou_liu_yaliang", "zhu_zhou_gov", "常务副市长", "2024-??", "", "副厅级", "市委常委、党组副书记"),
    (9, "zhuzhou_he_huixin", "zhu_zhou_gov", "副市长", "2024-??", "", "副厅级", "市委常委"),
    # Predecessor positions
    (10, "zhuzhou_cao_huiquan", "zhu_zhou_party", "市委书记", "2021-04", "2026-06", "正厅级", "第19任株洲市委书记"),
    (11, "zhuzhou_cao_huiquan", "hunan_industry_it", "厅长", "2018-10", "2021-05", "正厅级", "省工信厅厅长"),
    (12, "zhuzhou_mao_tengfei", "zhu_zhou_party", "市委书记", "2016-03", "2021-04", "正厅级", "第18任株洲市委书记"),
    (13, "zhuzhou_mao_tengfei", "hunan_industry_it", "厅长", "2021-04", "2022-05", "正厅级", "与曹慧泉互换岗位"),
    (14, "zhuzhou_mao_tengfei", "hunan_cppcc", "副主任", "2022-05", "2022-11", "副厅级", "省政协经济科技委员会副主任"),
]

relationships = [
    (1, "zhuzhou_cao_huiquan", "zhuzhou_mao_tengfei", "岗位对调",
     "2021年4月两人互换：曹慧泉从省工信厅厅长→株洲市委书记，毛腾飞从株洲市委书记→省工信厅厅长",
     "湖南省工信厅/株洲市委", "2021-04"),
    (2, "zhuzhou_wang_jianqiu", "zhuzhou_cao_huiquan", "前后任交接",
     "2026年6月王建球接替曹慧泉任株洲市委书记",
     "中共株洲市委", "2026-06"),
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
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

nodes_xml = ""
edges_xml = ""

# Person nodes
for p in persons:
    pid = p[0]
    name = p[1]
    role = p[9]
    # Color by role
    if "书记" in role and "市委" in role:
        color = "#E03C31"  # 红色—党委一把手
        size = 20.0
    elif "市长" in role or "代市长" in role or "副市长" in role:
        color = "#2B7CE9"  # 蓝色—政府领导
        size = 16.0 if "市长" in role and "副" not in role else 12.0
    elif "纪委" in role:
        color = "#FF8C00"  # 橙色—纪检
        size = 12.0
    else:
        color = "#888888"  # 灰色—其他
        size = 12.0

    nodes_xml += f"""      <node id="{esc(pid)}" label="{esc(name)}">
        <attvalues>
          <attvalue for="type" value="person"/>
          <attvalue for="role" value="{esc(role)}"/>
        </attvalues>
        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>
        <viz:size value="{size}"/>
        <viz:position x="0" y="0" z="0"/>
      </node>\n"""

# Organization nodes
org_color_map = {
    "党委": "#8B0000", "党委部门": "#A52A2A", "政府": "#1E90FF",
    "省政府部门": "#4169E1", "政协": "#2E8B57", "纪委": "#FF8C00",
    "军队": "#556B2F",
}
for o in organizations:
    oid = o[0]
    oname = o[1]
    otype = o[2]
    color = org_color_map.get(otype, "#666666")
    nodes_xml += f"""      <node id="{esc(oid)}" label="{esc(oname)}">
        <attvalues>
          <attvalue for="type" value="organization"/>
          <attvalue for="org_type" value="{esc(otype)}"/>
        </attvalues>
        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>
        <viz:size value="8.0"/>
        <viz:position x="0" y="0" z="0"/>
      </node>\n"""

# Edges: person → organization (worked_at)
for po in positions:
    pid = po[1]
    oid = po[2]
    title = po[3]
    start = po[4] or ""
    end = po[5] or ""
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
    a, b, rtype, ctx, overlap_org, overlap_period = r[1], r[2], r[3], r[4], r[5], r[6]
    if rtype == "岗位对调" or rtype == "前后任交接":
        color_str = "#C9A94E"
        thickness = 3.0
    else:
        color_str = "#6495ED"
        thickness = 1.5
    r_, g_, b_ = int(color_str[1:3], 16), int(color_str[3:5], 16), int(color_str[5:7], 16)
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
    <description>株洲市领导工作关系网络 — built {TODAY}</description>
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
