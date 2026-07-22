#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 诏安县 (Zhao'an County, Fujian) leadership network.

诏安县 — 县, 福建省漳州市下辖, 位于福建省南部沿海, 闽粤交界处.
Research date: 2026-07-16

Sources:
- www.zhaoan.gov.cn official homepage news articles (July 2026)
- 163.com/news article "远洋任诏安县委书记" (2026-03-17, 汲古知新)
- County government personnel appointment notices (2025-2026)

Coverage:
- Current top leader: 县委书记 远洋 (confirmed by media and active in county news through July 2026)
- 县长: name not yet confirmed from available sources
- County office leadership team (政府办)
- Key county-level officials observed in 2026 news coverage

Confidence notes:
- 远洋: confirmed current 县委书记 (as of March 2026, still active July 2026)
- 县长: identity not yet confirmed from available sources
- Other county leaders: partial roles from news; detailed bios need further research
- Early careers of most leaders need further research
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_诏安县")
DB_PATH = os.path.join(STAGING, "诏安县_network.db")
GEXF_PATH = os.path.join(STAGING, "诏安县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 远洋 — 诏安县委书记 (appointed ~2026-03, confirmed by media "汲古知新" 2026-03-17)
    {"id":1,"name":"远洋","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"诏安县委书记",
     "current_org":"中共诏安县委员会",
     "source":"https://www.163.com/search?keyword=远洋任诏安县委书记"},

    # ── 2. County Office leaders ──
    # 许仲岚 — 县政府办公室党组书记、主任
    {"id":2,"name":"许仲岚","gender":"男","ethnicity":"汉族",
     "birth":"1975年9月","birthplace":"",
     "education":"省委党校研究生",
     "party_join":"中国共产党","work_start":"",
     "current_post":"诏安县人民政府办公室党组书记、主任",
     "current_org":"诏安县人民政府办公室",
     "source":"http://www.zhaoan.gov.cn/cms/html/zaxrmzf/ldxx/index.html"},
    # 许昊鲁 — 县政府办公室副主任
    {"id":3,"name":"许昊鲁","gender":"男","ethnicity":"汉族",
     "birth":"1989年1月","birthplace":"",
     "education":"在职大学",
     "party_join":"中国共产党","work_start":"",
     "current_post":"诏安县人民政府办公室副主任、党组成员",
     "current_org":"诏安县人民政府办公室",
     "source":"http://www.zhaoan.gov.cn/cms/html/zaxrmzf/ldxx/index.html"},
    # 胡建生 — 县政府办党组成员
    {"id":4,"name":"胡建生","gender":"男","ethnicity":"汉族",
     "birth":"1969年3月","birthplace":"",
     "education":"在职大专",
     "party_join":"中国共产党","work_start":"",
     "current_post":"诏安县政府办党组成员、一级主任科员",
     "current_org":"诏安县人民政府办公室",
     "source":"http://www.zhaoan.gov.cn/cms/html/zaxrmzf/ldxx/index.html"},

    # ── 3. County-level officials observed in news ──
    # 县领导频繁出现在各类调研活动中 (names need further confirmation)
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共诏安县委员会","type":"党委","level":"县级","parent":"中共漳州市委员会","location":"福建省漳州市诏安县"},
    {"id":2,"name":"诏安县人民政府","type":"政府","level":"县级","parent":"漳州市人民政府","location":"福建省漳州市诏安县"},
    {"id":3,"name":"诏安县人大常委会","type":"人大","level":"县级","parent":"","location":"福建省漳州市诏安县"},
    {"id":4,"name":"政协诏安县委员会","type":"政协","level":"县级","parent":"","location":"福建省漳州市诏安县"},
    {"id":5,"name":"诏安县人民政府办公室","type":"政府","level":"正科级","parent":"诏安县人民政府","location":"福建省漳州市诏安县"},
    {"id":6,"name":"中共诏安县纪律检查委员会","type":"党委","level":"县级","parent":"中共诏安县委员会","location":"福建省漳州市诏安县"},
    {"id":7,"name":"中共诏安县委政法委员会","type":"党委","level":"县级","parent":"中共诏安县委员会","location":"福建省漳州市诏安县"},
    {"id":8,"name":"中共诏安县委宣传部","type":"党委","level":"县级","parent":"中共诏安县委员会","location":"福建省漳州市诏安县"},
    {"id":9,"name":"中共诏安县委组织部","type":"党委","level":"县级","parent":"中共诏安县委员会","location":"福建省漳州市诏安县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 远洋 career timeline (partial) ──
    {"id":1,"person_id":1,"org_id":1,"title":"诏安县委书记","start":"~2026-03","end":"present","rank":"正处","note":"现任; 据媒体报道2026年3月就任"},

    # ── 许仲岚 ──
    {"id":2,"person_id":2,"org_id":5,"title":"诏安县人民政府办公室党组书记、主任","start":"","end":"present","rank":"正科级","note":"现任"},
    # ── 许昊鲁 ──
    {"id":3,"person_id":3,"org_id":5,"title":"诏安县人民政府办公室副主任、党组成员","start":"","end":"present","rank":"副科级","note":"现任"},
    # ── 胡建生 ──
    {"id":4,"person_id":4,"org_id":5,"title":"诏安县政府办党组成员、一级主任科员","start":"","end":"present","rank":"正科级","note":"现任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 许仲岚 — 许昊鲁 (办公室上下级)
    {"id":1,"person_a":2,"person_b":3,"type":"superior_subordinate","context":"县政府办公室党组书记-副主任","overlap_org":"诏安县人民政府办公室","overlap_period":""},
    # 许仲岚 — 胡建生 (办公室同僚)
    {"id":2,"person_a":2,"person_b":4,"type":"overlap","context":"县政府办公室党组成员同僚","overlap_org":"诏安县人民政府办公室","overlap_period":""},
]

# =========================================================================
# SQLITE DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT,
        source TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                      p["education"],p["party_join"],p["work_start"],p["current_post"],
                      p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for ps in positions:
        cur.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                     (ps["id"],ps["person_id"],ps["org_id"],ps["title"],ps["start"],ps["end"],ps["rank"],ps["note"]))
    for r in relationships:
        cur.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                     (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")

# =========================================================================
# GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return 'r,g,b' string based on person's role."""
    post = p.get("current_post","")
    if "书记" in post and "纪委" not in post and "人大" not in post and "政协" not in post:
        return "255,50,50"     # Red: Party Secretary
    if "县长" in post or "代县长" in post:
        return "50,100,255"    # Blue: Government head
    if "纪委" in post or "监委" in post:
        return "255,165,0"     # Orange: Discipline
    if "人大" in post:
        return "200,255,255"   # Cyan: People's Congress
    if "政协" in post:
        return "255,240,200"   # Cream: Political Consultative
    if "副县长" in post:
        return "50,100,255"    # Blue: Deputy mayor
    return "100,100,100"       # Grey: Others

def is_top_leader(p):
    return p["id"] in [1]  # 远洋 (县委书记 is only confirmed top leader)

def org_color(o):
    t = o.get("type","")
    m = {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200",
         "乡镇/街道":"255,255,200","事业单位":"220,220,220","群团":"255,220,255",
         "人大":"200,255,255","政协":"255,240,200"}
    return m.get(t,"200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>诏安县领导工作关系网络 - Zhaoan County Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="subtype" type="string"/>')
    lines.append('      <attribute id="2" title="job_title" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="birth" type="string"/>')
    lines.append('      <attribute id="5" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"][:20])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="3" value="县级"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birthplace"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person → Organization edges (worked_at)
    for ps in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{ps["person_id"]}" target="o{ps["org_id"]}" label="{esc(ps["title"][:30])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ps["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(ps["start"])}-{esc(ps["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring("\n".join(lines))
        print("    XML well-formed: OK")
    except Exception as e:
        print(f"    XML validation: {e}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("Building 诏安县 leadership network...")
    build_db()
    build_gexf()
    print("Done.")
