#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 铜鼓县 (Tonggu County) leadership network.

Research date: 2026-07-15
Sources: http://www.tonggu.gov.cn (government website, news articles)
"""

import sqlite3, os, json, textwrap
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/tonggu_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/tonggu_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current Party Secretary ──
    {"id":1,"name":"熊小亮","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委书记","current_org":"中共铜鼓县委员会","source":"http://www.tonggu.gov.cn/tgxrmzf/tgyw/pc/list.html; 十五届县委常委会第141-143次会议"},

    # ── Current Mayor (candidate) ──
    {"id":2,"name":"袁常青","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委副书记、县长候选人","current_org":"铜鼓县人民政府","source":"http://www.tonggu.gov.cn/tgxrmzf/tgyw/pc/list.html; 第143次常委会"},

    # ── Deputy Party Secretary ──
    {"id":3,"name":"巫晓怡","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委副书记","current_org":"中共铜鼓县委员会","source":"http://www.tonggu.gov.cn; 常委会出席名单"},

    # ── Party Committee Standing Members ──
    {"id":4,"name":"傅鹏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委常委","current_org":"中共铜鼓县委员会","source":"http://www.tonggu.gov.cn; 常委会出席名单"},

    {"id":5,"name":"卢柏意","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委常委、统战部部长","current_org":"中共铜鼓县委员会统战部","source":"http://www.tonggu.gov.cn; 统战工作会议"},

    {"id":6,"name":"帅江","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委常委、副县长","current_org":"铜鼓县人民政府","source":"http://www.tonggu.gov.cn; 领导接听公告第37期"},

    {"id":7,"name":"熊涛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委常委","current_org":"中共铜鼓县委员会","source":"http://www.tonggu.gov.cn; 常委会出席名单"},

    {"id":8,"name":"谭光琅","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委常委","current_org":"中共铜鼓县委员会","source":"http://www.tonggu.gov.cn; 常委会出席名单"},

    {"id":9,"name":"黄万荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县委常委","current_org":"中共铜鼓县委员会","source":"http://www.tonggu.gov.cn; 第143次常委会新增出席"},

    # ── Deputy County Heads ──
    {"id":10,"name":"刘长检","gender":"男","ethnicity":"汉族","birth":"1983-05","birthplace":"","education":"省委党校研究生","party_join":"中共党员","work_start":"","current_post":"铜鼓县人民政府副县长、党组成员","current_org":"铜鼓县人民政府","source":"http://www.tonggu.gov.cn/tgxrmzf/fxz/pc/list.html"},

    {"id":11,"name":"潘小燕","gender":"女","ethnicity":"汉族","birth":"1982-07","birthplace":"","education":"本科","party_join":"无党派","work_start":"","current_post":"铜鼓县人民政府副县长（福州新区挂职）","current_org":"铜鼓县人民政府","source":"http://www.tonggu.gov.cn/tgxrmzf/fxz/pc/list.html"},

    {"id":12,"name":"彭浩屹","gender":"男","ethnicity":"汉族","birth":"1987-05","birthplace":"","education":"研究生","party_join":"中共党员","work_start":"","current_post":"铜鼓县人民政府副县长、党组成员、县公安局局长","current_org":"铜鼓县人民政府／县公安局","source":"http://www.tonggu.gov.cn/tgxrmzf/fxz/pc/list.html"},

    {"id":13,"name":"孙红星","gender":"男","ethnicity":"汉族","birth":"1976-01","birthplace":"","education":"大学","party_join":"中共党员","work_start":"","current_post":"铜鼓县人民政府副县长、党组成员","current_org":"铜鼓县人民政府","source":"http://www.tonggu.gov.cn/tgxrmzf/fxz/pc/list.html"},

    {"id":14,"name":"周升","gender":"女","ethnicity":"汉族","birth":"1986-04","birthplace":"","education":"研究生","party_join":"中共党员","work_start":"","current_post":"铜鼓县人民政府副县长、党组成员","current_org":"铜鼓县人民政府","source":"http://www.tonggu.gov.cn/tgxrmzf/fxz/pc/list.html"},

    # ── Legislature & Consultative ──
    {"id":15,"name":"余伟彬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县人大常委会主任","current_org":"铜鼓县人大常委会","source":"http://www.tonggu.gov.cn; 常委会会议列席名单"},

    {"id":16,"name":"罗咏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"铜鼓县政协主席","current_org":"政协铜鼓县委员会","source":"http://www.tonggu.gov.cn; 常委会会议列席名单"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":101,"name":"中共铜鼓县委员会","type":"党委","level":"县级","parent":"中共宜春市委员会","location":"江西省宜春市铜鼓县"},
    {"id":102,"name":"中共铜鼓县委员会统战部","type":"党委部门","level":"县级","parent":"中共铜鼓县委员会","location":"江西省宜春市铜鼓县"},
    {"id":103,"name":"铜鼓县人民政府","type":"政府","level":"县级","parent":"宜春市人民政府","location":"江西省宜春市铜鼓县"},
    {"id":104,"name":"铜鼓县公安局","type":"政府部门","level":"县级","parent":"铜鼓县人民政府","location":"江西省宜春市铜鼓县"},
    {"id":105,"name":"铜鼓县人大常委会","type":"人大","level":"县级","parent":"铜鼓县","location":"江西省宜春市铜鼓县"},
    {"id":106,"name":"政协铜鼓县委员会","type":"政协","level":"县级","parent":"铜鼓县","location":"江西省宜春市铜鼓县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Person 1: 熊小亮
    {"id":201,"person_id":1,"org_id":101,"title":"县委书记","start":"","end":"","rank":1,"note":"第十五届县委"},
    # Person 2: 袁常青
    {"id":202,"person_id":2,"org_id":103,"title":"县长候选人","start":"2026-07","end":"","rank":2,"note":"县委副书记、县长候选人（待人大选举）"},
    {"id":203,"person_id":2,"org_id":101,"title":"县委副书记","start":"2026-07","end":"","rank":2,"note":"兼职"},
    # Person 3: 巫晓怡
    {"id":204,"person_id":3,"org_id":101,"title":"县委副书记","start":"","end":"","rank":3,"note":"专职副书记"},
    # Person 4-9: 常委
    {"id":205,"person_id":4,"org_id":101,"title":"县委常委","start":"","end":"","rank":5,"note":""},
    {"id":206,"person_id":5,"org_id":101,"title":"县委常委","start":"","end":"","rank":5,"note":""},
    {"id":207,"person_id":5,"org_id":102,"title":"统战部部长","start":"","end":"","rank":1,"note":"兼职"},
    {"id":208,"person_id":6,"org_id":101,"title":"县委常委","start":"","end":"","rank":5,"note":""},
    {"id":209,"person_id":6,"org_id":103,"title":"副县长","start":"","end":"","rank":5,"note":"常务副县长"},
    {"id":210,"person_id":7,"org_id":101,"title":"县委常委","start":"","end":"","rank":5,"note":""},
    {"id":211,"person_id":8,"org_id":101,"title":"县委常委","start":"","end":"","rank":5,"note":""},
    {"id":212,"person_id":9,"org_id":101,"title":"县委常委","start":"2026-07","end":"","rank":5,"note":"新晋常委"},
    # Person 10-14: 副县长
    {"id":213,"person_id":10,"org_id":103,"title":"副县长","start":"","end":"","rank":6,"note":"党组成员"},
    {"id":214,"person_id":11,"org_id":103,"title":"副县长","start":"","end":"","rank":6,"note":"在福州新区挂职"},
    {"id":215,"person_id":12,"org_id":103,"title":"副县长","start":"","end":"","rank":6,"note":"党组成员"},
    {"id":216,"person_id":12,"org_id":104,"title":"局长","start":"","end":"","rank":1,"note":"县公安局局长"},
    {"id":217,"person_id":13,"org_id":103,"title":"副县长","start":"","end":"","rank":6,"note":"党组成员"},
    {"id":218,"person_id":14,"org_id":103,"title":"副县长","start":"","end":"","rank":6,"note":"党组成员"},
    # Person 15-16: 人大/政协
    {"id":219,"person_id":15,"org_id":105,"title":"主任","start":"","end":"","rank":1,"note":"县人大常委会主任"},
    {"id":220,"person_id":16,"org_id":106,"title":"主席","start":"","end":"","rank":1,"note":"县政协主席"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党委班子内关系
    {"id":301,"person_a":1,"person_b":2,"type":"上级—副手","context":"县委书记与县长候选人","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},
    {"id":302,"person_a":1,"person_b":3,"type":"上级—副手","context":"县委书记与专职副书记","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},
    {"id":303,"person_a":1,"person_b":4,"type":"上下级","context":"县委书记与县委常委","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},
    {"id":304,"person_a":1,"person_b":5,"type":"上下级","context":"县委书记与县委常委/统战部长","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},
    {"id":305,"person_a":1,"person_b":6,"type":"上下级","context":"县委书记与县委常委/副县长","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},
    {"id":306,"person_a":1,"person_b":7,"type":"上下级","context":"县委书记与县委常委","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},
    {"id":307,"person_a":1,"person_b":8,"type":"上下级","context":"县委书记与县委常委","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},
    {"id":308,"person_a":1,"person_b":9,"type":"上下级","context":"县委书记与新晋常委","overlap_org":"中共铜鼓县委员会","overlap_period":"当前"},

    # 县政府内关系
    {"id":309,"person_a":6,"person_b":10,"type":"同事","context":"常务副县长与副县长","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},
    {"id":310,"person_a":6,"person_b":12,"type":"同事","context":"常务副县长与副县长/公安局长","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},
    {"id":311,"person_a":6,"person_b":13,"type":"同事","context":"常务副县长与副县长","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},
    {"id":312,"person_a":10,"person_b":13,"type":"同事","context":"副县长同事关系","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},
    {"id":313,"person_a":10,"person_b":14,"type":"同事","context":"副县长同事关系","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},
    {"id":314,"person_a":12,"person_b":10,"type":"同事","context":"副县长同事关系","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},
    {"id":315,"person_a":12,"person_b":13,"type":"同事","context":"副县长同事关系","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},
    {"id":316,"person_a":13,"person_b":14,"type":"同事","context":"副县长同事关系","overlap_org":"铜鼓县人民政府","overlap_period":"当前"},

    # 人大/政协与党委
    {"id":317,"person_a":1,"person_b":15,"type":"协作","context":"县委书记与人大主任（工作协作）","overlap_org":"铜鼓县","overlap_period":"当前"},
    {"id":318,"person_a":1,"person_b":16,"type":"协作","context":"县委书记与政协主席（工作协作）","overlap_org":"铜鼓县","overlap_period":"当前"},
]

# =========================================================================
# SQLite
# =========================================================================
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        ethnicity TEXT,
        birth TEXT,
        birthplace TEXT,
        education TEXT,
        party_join TEXT,
        work_start TEXT,
        current_post TEXT,
        current_org TEXT,
        source TEXT
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER REFERENCES persons(id),
        org_id INTEGER REFERENCES organizations(id),
        title TEXT,
        start TEXT,
        end TEXT,
        rank INTEGER,
        note TEXT
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER REFERENCES persons(id),
        person_b INTEGER REFERENCES persons(id),
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    );
""")

for p in persons:
    cur.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT OR REPLACE INTO positions
        (id, person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?,?)""",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT OR REPLACE INTO relationships
        (id, person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?,?)""",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"✅ SQLite database written → {DB_PATH}")

# =========================================================================
# GEXF
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# Determine node color & size by role
def node_viz(person):
    name = person["name"]
    post = person["current_post"]
    birth = person["birth"]
    if "县委书记" in post or "书记" in post:
        color = "#E03C31"  # red
        size = 20.0
    elif "县长" in post:
        color = "#2979FF"  # blue
        size = 20.0
    elif "副书记" in post:
        color = "#2979FF"
        size = 16.0
    elif "常委" in post and "副县长" in post:
        color = "#C9A94E"  # gold
        size = 14.0
    elif "常委" in post:
        color = "#C9A94E"
        size = 14.0
    elif "副县长" in post:
        color = "#FF8C00"  # orange
        size = 12.0
    elif "主任" in post or "主席" in post:
        color = "#8A8478"  # grey
        size = 12.0
    else:
        color = "#8A8478"
        size = 12.0

    label = f"{name}"
    if birth:
        label += f" ({birth})"
    label += f"\\n{post}"

    return color, size, label

org_colors = {"党委":"#C62828","党委部门":"#D84315","政府":"#1565C0","政府部门":"#1976D2","人大":"#4E342E","政协":"#4E342E"}

# Build nodes XML
nodes_xml = ""
for p in persons:
    color, size, label = node_viz(p)
    nodes_xml += f"""      <node id="p{p['id']}" label="{esc(label)}">
        <attvalues>
          <attvalue for="kind" value="person"/>
          <attvalue for="role" value="{esc(p['current_post'])}"/>
        </attvalues>
        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>
        <viz:size value="{size}"/>
        <viz:shape value="disc"/>
      </node>
"""

for o in organizations:
    color = org_colors.get(o["type"], "#666666")
    nodes_xml += f"""      <node id="o{o['id']}" label="{esc(o['name'])}">
        <attvalues>
          <attvalue for="kind" value="org"/>
          <attvalue for="type" value="{esc(o['type'])}"/>
        </attvalues>
        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>
        <viz:size value="8.0"/>
        <viz:shape value="square"/>
      </node>
"""

# Build edges XML
edges_xml = ""
# person → org (worked_at)
from collections import defaultdict
edge_counter = 0

# person → org edges
for pos in positions:
    edge_counter += 1
    edges_xml += f"""      <edge id="e{edge_counter}" source="p{pos['person_id']}" target="o{pos['org_id']}" type="directed">
        <attvalues>
          <attvalue for="type" value="worked_at"/>
          <attvalue for="title" value="{esc(pos['title'])}"/>
        </attvalues>
        <viz:color r="180" g="180" b="180"/>
        <viz:thickness value="1.0"/>
      </edge>
"""

# person ↔ person (relationship)
for r in relationships:
    edge_counter += 1
    rtype = r["type"]
    if "上级" in rtype or "上下级" in rtype:
        thick = 3.0
        color_r, color_g, color_b = 201, 169, 78  # gold
    elif "同事" in rtype:
        thick = 2.0
        color_r, color_g, color_b = 41, 121, 255  # blue
    else:
        thick = 1.5
        color_r, color_g, color_b = 138, 132, 120  # grey
    
    edges_xml += f"""      <edge id="e{edge_counter}" source="p{r['person_a']}" target="p{r['person_b']}" type="undirected">
        <attvalues>
          <attvalue for="type" value="relationship"/>
          <attvalue for="context" value="{esc(r['context'])}"/>
          <attvalue for="overlap_org" value="{esc(r['overlap_org'])}"/>
        </attvalues>
        <viz:color r="{color_r}" g="{color_g}" b="{color_b}"/>
        <viz:thickness value="{thick}"/>
      </edge>
"""

gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">
  <meta lastmodifieddate="{datetime.now().strftime('%Y-%m-%d')}">
    <creator>gov-relation research agent</creator>
    <description>铜鼓县领导班子工作关系网络 — 2026-07-15</description>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="kind" title="Kind" type="string"/>
      <attribute id="role" title="Role" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Type" type="string"/>
      <attribute id="title" title="Title" type="string"/>
      <attribute id="context" title="Context" type="string"/>
      <attribute id="overlap_org" title="Overlap Org" type="string"/>
    </attributes>
    <nodes>
{nodes_xml}    </nodes>
    <edges>
{edges_xml}    </edges>
  </graph>
</gexf>
"""

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(gexf)

print(f"✅ GEXF graph written → {GEXF_PATH}")

# =========================================================================
# Summary
# =========================================================================
print(f"""
📊 Summary
  Persons:       {len(persons)}
  Orgs:          {len(organizations)}
  Positions:     {len(positions)}
  Relationships: {len(relationships)}
  Edges (GEXF):  {edge_counter}

⚠  Data quality notes:
  - Career histories for most officials are incomplete (no Baidu Baike/Wikipedia access)
  - 熊小亮 (party secretary): only name & role confirmed
  - 袁常青 (mayor candidate): only name & role confirmed
  - 袁常青 is listed as "县长候选人" suggesting the mayor election process is underway
  - Deputy county heads (5 persons): basic info available (name, birth year, education)
  - Sources: Government news articles & leadership page listings
  - All career timeline data needs further research
""")
