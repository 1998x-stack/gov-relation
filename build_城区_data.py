#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汕尾市城区 leadership network.

城区 — 市辖区, 广东省汕尾市下辖, 汕尾市人民政府所在地.
Research date: 2026-07-22

Sources:
- 汕尾市人民政府门户网站 (www.shanwei.gov.cn) — news articles, interviews
- 新华网 (www.xinhuanet.com) — "对话山海·现在好时节" interview with 区长詹响锑
- 汕尾日报 — interview with 区委书记肖苏

Coverage:
- Current 区委书记 肖苏 — identity confirmed from 汕尾日报 interview (2026-06-11)
- Current 区长 詹响锑 — identity confirmed from 新华网 interview (2026-07-09)
- Deputy 副区长 李小燕 — mentioned in 政民互动 section (interview available)
- District leadership roster — partial (常委待补充)
- Predecessor chain — limited

Confidence notes:
- 肖苏 (Party Secretary): identity confirmed from official interview; detailed bio needs further research
- 詹响锑 (District Mayor): identity confirmed from official interview; detailed bio needs further research
- 李小燕 (Deputy Mayor): identity confirmed from interview listing; detailed bio needs further research
- Full leadership roster: needs government website access for 领导之窗
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/guangdong_城区")
DB_PATH = os.path.join(STAGING, "城区_network.db")
GEXF_PATH = os.path.join(STAGING, "城区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 肖苏 — 城区委书记 (as of 汕尾日报 interview, 2026-06-11)
    {"id":1,"name":"肖苏","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委书记",
     "current_org":"中共汕尾市城区委员会",
     "source":"http://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/qxxwa/content/post_1253862.html"},

    # 詹响锑 — 城区委副书记、区长 (as of 新华网 interview, 2026-07-09)
    {"id":2,"name":"詹响锑","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委副书记、区长",
     "current_org":"汕尾市城区人民政府",
     "source":"https://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/qxxwa/content/post_1260423.html"},

    # 李小燕 — 城区副区长 (mentioned in 政民互动)
    {"id":3,"name":"李小燕","gender":"女","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"城区人民政府副区长",
     "current_org":"汕尾市城区人民政府",
     "source":"https://www.shanwei.gov.cn — 政民互动·在线访谈栏目"},

    # ── 区委常委 (需进一步确认) ──
    # 区人大常委会主任
    {"id":4,"name":"（区人大常委会主任待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区人大常委会主任",
     "current_org":"汕尾市城区人民代表大会常务委员会",
     "source":"公开资料待查"},

    # 区政协主席
    {"id":5,"name":"（区政协主席待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区政协主席",
     "current_org":"中国人民政治协商会议汕尾市城区委员会",
     "source":"公开资料待查"},

    # 区纪委书记/监委主任
    {"id":6,"name":"（区纪委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区纪委书记、监委主任",
     "current_org":"中共汕尾市城区纪律检查委员会",
     "source":"公开资料待查"},

    # 常务副区长
    {"id":7,"name":"（常务副区长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委常委、常务副区长",
     "current_org":"汕尾市城区人民政府",
     "source":"公开资料待查"},

    # 组织部部长
    {"id":8,"name":"（组织部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委常委、组织部部长",
     "current_org":"中共汕尾市城区委员会",
     "source":"公开资料待查"},

    # 宣传部部长
    {"id":9,"name":"（宣传部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委常委、宣传部部长",
     "current_org":"中共汕尾市城区委员会",
     "source":"公开资料待查"},

    # 政法委书记
    {"id":10,"name":"（政法委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委常委、政法委书记",
     "current_org":"中共汕尾市城区委员会",
     "source":"公开资料待查"},

    # 统战部部长
    {"id":11,"name":"（统战部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委常委、统战部部长",
     "current_org":"中共汕尾市城区委员会",
     "source":"公开资料待查"},

    # 区委办公室主任/区委常委
    {"id":12,"name":"（区委办公室主任待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委常委、区委办公室主任",
     "current_org":"中共汕尾市城区委员会",
     "source":"公开资料待查"},

    # 人武部政委/部长
    {"id":13,"name":"（人武部主官待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"城区委常委、人武部主官",
     "current_org":"汕尾市城区人民武装部",
     "source":"公开资料待查"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共汕尾市城区委员会","type":"党委","level":"县处级","parent":"中共汕尾市委员会","location":"广东省汕尾市城区"},
    {"id":2,"name":"汕尾市城区人民政府","type":"政府","level":"县处级","parent":"汕尾市人民政府","location":"广东省汕尾市城区"},
    {"id":3,"name":"汕尾市城区人民代表大会常务委员会","type":"人大","level":"县处级","parent":"汕尾市人民代表大会常务委员会","location":"广东省汕尾市城区"},
    {"id":4,"name":"中国人民政治协商会议汕尾市城区委员会","type":"政协","level":"县处级","parent":"政协汕尾市委员会","location":"广东省汕尾市城区"},
    {"id":5,"name":"中共汕尾市城区纪律检查委员会","type":"纪委","level":"县处级","parent":"中共汕尾市纪律检查委员会","location":"广东省汕尾市城区"},
    {"id":6,"name":"中共汕尾市城区委员会组织部","type":"党委部门","level":"乡科级","parent":"中共汕尾市城区委员会","location":"广东省汕尾市城区"},
    {"id":7,"name":"中共汕尾市城区委员会宣传部","type":"党委部门","level":"乡科级","parent":"中共汕尾市城区委员会","location":"广东省汕尾市城区"},
    {"id":8,"name":"中共汕尾市城区委员会政法委员会","type":"党委部门","level":"乡科级","parent":"中共汕尾市城区委员会","location":"广东省汕尾市城区"},
    {"id":9,"name":"中共汕尾市城区委员会统一战线工作部","type":"党委部门","level":"乡科级","parent":"中共汕尾市城区委员会","location":"广东省汕尾市城区"},
    {"id":10,"name":"中共汕尾市城区委员会办公室","type":"党委部门","level":"乡科级","parent":"中共汕尾市城区委员会","location":"广东省汕尾市城区"},
    {"id":11,"name":"汕尾市城区人民武装部","type":"军队","level":"县处级","parent":"汕尾军分区","location":"广东省汕尾市城区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 肖苏
    {"person_id":1,"org_id":1,"title":"城区委书记","start_date":"","end_date":"","rank":"正处级","note":"2026年6月仍在任"},
    # 詹响锑
    {"person_id":2,"org_id":2,"title":"区长","start_date":"","end_date":"","rank":"正处级","note":"城区委副书记、区长, 2026年7月仍在任"},
    # 李小燕
    {"person_id":3,"org_id":2,"title":"副区长","start_date":"","end_date":"","rank":"副处级","note":""},
    # 其他待查
    {"person_id":4,"org_id":3,"title":"主任","start_date":"","end_date":"","rank":"正处级","note":"待确认"},
    {"person_id":5,"org_id":4,"title":"主席","start_date":"","end_date":"","rank":"正处级","note":"待确认"},
    {"person_id":6,"org_id":5,"title":"书记","start_date":"","end_date":"","rank":"副处级","note":"待确认"},
    {"person_id":7,"org_id":2,"title":"常务副区长","start_date":"","end_date":"","rank":"副处级","note":"待确认"},
    {"person_id":8,"org_id":6,"title":"部长","start_date":"","end_date":"","rank":"副处级","note":"待确认"},
    {"person_id":9,"org_id":7,"title":"部长","start_date":"","end_date":"","rank":"副处级","note":"待确认"},
    {"person_id":10,"org_id":8,"title":"书记","start_date":"","end_date":"","rank":"副处级","note":"待确认"},
    {"person_id":11,"org_id":9,"title":"部长","start_date":"","end_date":"","rank":"副处级","note":"待确认"},
    {"person_id":12,"org_id":10,"title":"主任","start_date":"","end_date":"","rank":"副处级","note":"待确认"},
    {"person_id":13,"org_id":11,"title":"主官","start_date":"","end_date":"","rank":"副师级/正团级","note":"待确认"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 肖苏 <-> 詹响锑: 区委书记—区长搭档
    {"person_a":1,"person_b":2,"type":"共事","context":"区委书记—区长搭档","overlap_org":"中共汕尾市城区委员会/汕尾市城区人民政府","overlap_period":"2026"},
    # 肖苏 <-> 李小燕: 上下级
    {"person_a":1,"person_b":3,"type":"上下级","context":"区委书记—副区长","overlap_org":"中共汕尾市城区委员会/汕尾市城区人民政府","overlap_period":"2026"},
    # 詹响锑 <-> 李小燕: 上下级
    {"person_a":2,"person_b":3,"type":"上下级","context":"区长—副区长","overlap_org":"汕尾市城区人民政府","overlap_period":"2026"},
]

# =========================================================================
# BUILD
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(current_post):
    """Return GEXF color for a person node based on their current post."""
    role = current_post
    if "书记" in role and "副" not in role and "纪委" not in role:
        return (200, 30, 30)  # 深红 — 一把手
    if "区长" in role:
        return (30, 100, 200)  # 深蓝 — 政府首长
    if "副区长" in role or "副" in role:
        return (100, 150, 220)  # 浅蓝 — 副职
    if "纪委" in role or "监委" in role:
        return (255, 165, 0)  # 橙色 — 纪委
    if "主任" in role:
        return (60, 180, 60)  # 绿色 — 人大/政协
    if "主席" in role:
        return (60, 180, 60)
    if "常委" in role:
        return (180, 100, 180)  # 紫色
    return (100, 100, 100)  # 灰色 — 其他

def is_top_leader(post):
    return "书记" in post and "副" not in post and "纪委" not in post

def org_color(org_type):
    colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "人大": (200, 255, 255),
        "政协": (255, 240, 200),
        "纪委": (255, 200, 150),
        "党委部门": (240, 220, 240),
        "军队": (200, 200, 200),
    }
    return colors.get(org_type, (200, 200, 200))

# ---- Build SQLite ----
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS relationships;
    DROP TABLE IF EXISTS positions;
    DROP TABLE IF EXISTS organizations;
    DROP TABLE IF EXISTS persons;

    CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    );

    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );

    CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT DEFAULT '',
        start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute(
        "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"])
    )

for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
        (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"])
    )

for pos in positions:
    cur.execute(
        "INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
        (pos["person_id"],pos["org_id"],pos["title"],pos["start_date"],pos["end_date"],pos["rank"],pos["note"])
    )

for r in relationships:
    cur.execute(
        "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
        (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"])
    )

conn.commit()
conn.close()
print(f"SQLite DB written: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

# ---- Build GEXF ----
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gov-Relation Research Agent</creator>')
lines.append('    <description>汕尾市城区领导班子关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="current_post" type="string"/>')
lines.append('      <attribute id="2" title="current_org" type="string"/>')
lines.append('      <attribute id="3" title="gender" type="string"/>')
lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
lines.append('      <attribute id="5" title="birth" type="string"/>')
lines.append('      <attribute id="6" title="source" type="string"/>')
lines.append('      <attribute id="7" title="org_type" type="string"/>')
lines.append('      <attribute id="8" title="level" type="string"/>')
lines.append('      <attribute id="9" title="location" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
lines.append('    </attributes>')

# -- Nodes --
lines.append('    <nodes>')

# Person nodes
for p in persons:
    c = person_color(p["current_post"])
    sz = "20.0" if is_top_leader(p["current_post"]) else "12.0"
    name = p["name"].replace("（", "(").replace("）", ")")
    lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="1.0"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    c = org_color(o["type"])
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="8" value="{esc(o["level"])}"/>')
    lines.append(f'          <attvalue for="9" value="{esc(o["location"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="0.8"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# -- Edges --
lines.append('    <edges>')

# Person -> Organization (worked_at)
eid = 1
for pos in positions:
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

# Person <-> Person (relationship)
for r in relationships:
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF graph written: {GEXF_PATH}")
print(f"  Total nodes: {len(persons) + len(organizations)}")
print(f"  Total edges: {len(positions) + len(relationships)}")
