#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 芗城区 (Xiangcheng District, Zhangzhou, Fujian) leadership network.

芗城区 — 市辖区, 福建省漳州市下辖, 漳州市人民政府所在地.
Research date: 2026-07-16

Sources:
- Wikipedia (zh.wikipedia.org/wiki/芗城区) — district info, current区委书记
- Government website (www.xc.gov.cn) — news references

Coverage:
- Current区委书记 黄庆辉 — identity confirmed from Wikipedia
- Current区长 — identity pending (not disclosed on Wikipedia infobox)
- District leadership roster — partial
- Predecessor chain — limited

Confidence notes:
- 黄庆辉 (Party Secretary): identity confirmed from Wikipedia infobox; detailed bio needs further research
- 区长: not yet identified from public sources — open gap
- Full leadership roster: needs government website access
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_芗城区")
DB_PATH = os.path.join(STAGING, "芗城区_network.db")
GEXF_PATH = os.path.join(STAGING, "芗城区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 黄庆辉 — 芗城区委书记 (as of Wikipedia infobox, 2026-07-16)
    {"id":1,"name":"黄庆辉","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区委书记",
     "current_org":"中共漳州市芗城区委员会",
     "source":"https://zh.wikipedia.org/wiki/%E8%8A%97%E5%9F%8E%E5%8C%BA"},

    # 区长 — 身份待查 (open gap)
    {"id":2,"name":"（区长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区区长",
     "current_org":"漳州市芗城区人民政府",
     "source":"公开资料未找到现任区长信息"},

    # ── 区委常委 (需进一步确认) ──
    # Based on typical district leadership structure
    # 区人大常委会主任
    {"id":3,"name":"（区人大常委会主任待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区人大常委会主任",
     "current_org":"漳州市芗城区人民代表大会常务委员会",
     "source":"公开资料待查"},

    # 区政协主席
    {"id":4,"name":"（区政协主席待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区政协主席",
     "current_org":"中国人民政治协商会议漳州市芗城区委员会",
     "source":"公开资料待查"},

    # 区纪委书记/监委主任
    {"id":5,"name":"（区纪委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区纪委书记、监委主任",
     "current_org":"中共漳州市芗城区纪律检查委员会",
     "source":"公开资料待查"},

    # 常务副区长
    {"id":6,"name":"（常务副区长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区委常委、常务副区长",
     "current_org":"漳州市芗城区人民政府",
     "source":"公开资料待查"},

    # 组织部部长
    {"id":7,"name":"（组织部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区委常委、组织部部长",
     "current_org":"中共漳州市芗城区委员会",
     "source":"公开资料待查"},

    # 宣传部部长
    {"id":8,"name":"（宣传部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区委常委、宣传部部长",
     "current_org":"中共漳州市芗城区委员会",
     "source":"公开资料待查"},

    # 政法委书记
    {"id":9,"name":"（政法委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区委常委、政法委书记",
     "current_org":"中共漳州市芗城区委员会",
     "source":"公开资料待查"},

    # 统战部部长
    {"id":10,"name":"（统战部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区委常委、统战部部长",
     "current_org":"中共漳州市芗城区委员会",
     "source":"公开资料待查"},

    # ── 政府副区长 ──
    {"id":11,"name":"（副区长待查1）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区副区长",
     "current_org":"漳州市芗城区人民政府",
     "source":"公开资料待查"},

    {"id":12,"name":"（副区长待查2）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区副区长",
     "current_org":"漳州市芗城区人民政府",
     "source":"公开资料待查"},

    {"id":13,"name":"（副区长/公安局长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"芗城区副区长、公安分局局长",
     "current_org":"漳州市公安局芗城分局",
     "source":"公开资料待查"},

    # ── Predecessors (需进一步确认) ──
    {"id":14,"name":"（前任区委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"（前任芗城区委书记）",
     "current_org":"",
     "source":"公开资料待查"},

    {"id":15,"name":"（前前任区委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"（前前任芗城区委书记）",
     "current_org":"",
     "source":"公开资料待查"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共漳州市芗城区委员会","type":"党委","level":"区级","parent":"中共漳州市委员会","location":"福建省漳州市芗城区"},
    {"id":2,"name":"漳州市芗城区人民政府","type":"政府","level":"区级","parent":"漳州市人民政府","location":"福建省漳州市芗城区"},
    {"id":3,"name":"中共漳州市芗城区纪律检查委员会","type":"党委","level":"区级","parent":"漳州市纪律检查委员会","location":"福建省漳州市芗城区"},
    {"id":4,"name":"漳州市公安局芗城分局","type":"政府","level":"区级","parent":"漳州市公安局","location":"福建省漳州市芗城区"},
    {"id":5,"name":"漳州市芗城区人民代表大会常务委员会","type":"人大","level":"区级","parent":"漳州市人大常委会","location":"福建省漳州市芗城区"},
    {"id":6,"name":"中国人民政治协商会议漳州市芗城区委员会","type":"政协","level":"区级","parent":"漳州市政协","location":"福建省漳州市芗城区"},
    {"id":7,"name":"中共漳州市委宣传部","type":"党委","level":"市级","parent":"中共漳州市委员会","location":"福建省漳州市"},
    {"id":8,"name":"中共漳州市委组织部","type":"党委","level":"市级","parent":"中共漳州市委员会","location":"福建省漳州市"},
    {"id":9,"name":"漳州市人民政府","type":"政府","level":"市级","parent":"福建省人民政府","location":"福建省漳州市"},
    {"id":10,"name":"中共漳州市委员会","type":"党委","level":"市级","parent":"中共福建省委员会","location":"福建省漳州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 黄庆辉 — 区委书记
    {"person_id":1,"org_id":1,"title":"芗城区委书记","start":"","end":"present","rank":"正处级","note":"Wikipedia infobox显示为现任区委书记"},
    # 区长待查
    {"person_id":2,"org_id":2,"title":"芗城区区长","start":"","end":"present","rank":"正处级","note":"身份待查"},
    # 人大常委会主任
    {"person_id":3,"org_id":5,"title":"芗城区人大常委会主任","start":"","end":"present","rank":"正处级","note":"身份待查"},
    # 政协主席
    {"person_id":4,"org_id":6,"title":"芗城区政协主席","start":"","end":"present","rank":"正处级","note":"身份待查"},
    # 纪委书记
    {"person_id":5,"org_id":3,"title":"芗城区纪委书记、监委主任","start":"","end":"present","rank":"副处级","note":"身份待查"},
    # 常务副区长
    {"person_id":6,"org_id":2,"title":"芗城区委常委、常务副区长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    # 组织部部长
    {"person_id":7,"org_id":1,"title":"芗城区委常委、组织部部长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    # 宣传部部长
    {"person_id":8,"org_id":1,"title":"芗城区委常委、宣传部部长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    # 政法委书记
    {"person_id":9,"org_id":1,"title":"芗城区委常委、政法委书记","start":"","end":"present","rank":"副处级","note":"身份待查"},
    # 统战部部长
    {"person_id":10,"org_id":1,"title":"芗城区委常委、统战部部长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    # 副区长
    {"person_id":11,"org_id":2,"title":"芗城区副区长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    {"person_id":12,"org_id":2,"title":"芗城区副区长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    {"person_id":13,"org_id":4,"title":"芗城区副区长、公安分局局长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    # 前任
    {"person_id":14,"org_id":1,"title":"前任芗城区委书记","start":"","end":"","rank":"正处级","note":"身份待查"},
    {"person_id":15,"org_id":1,"title":"前前任芗城区委书记","start":"","end":"","rank":"正处级","note":"身份待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 区委书记 — 区长 (党政一把手)
    {"person_a":1,"person_b":2,"type":"overlap","context":"区委书记与区长为党政搭档","overlap_org":"芗城区","overlap_period":"当前","confidence":"plausible","strength":"medium"},
    # 前任关系（待确认具体人名）
    {"person_a":1,"person_b":14,"type":"predecessor_successor","context":"区委书记接替关系","overlap_org":"芗城区委","overlap_period":"","confidence":"unverified","strength":"medium"},
    {"person_a":14,"person_b":15,"type":"predecessor_successor","context":"区委书记接替关系","overlap_org":"芗城区委","overlap_period":"","confidence":"unverified","strength":"medium"},
]

# =========================================================================
# BUILD SQLite DATABASE
# =========================================================================
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],
                   p["birth"],p["birthplace"],p["education"],
                   p["party_join"],p["work_start"],
                   p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()

    # Print summary
    cur = conn.execute("SELECT COUNT(*) FROM persons"); pc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM organizations"); oc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM positions"); poc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM relationships"); rc = cur.fetchone()[0]
    print(f"✅ SQLite: {pc} persons, {oc} organizations, {poc} positions, {rc} relationships")
    conn.close()

# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    if "区委书记" in p["current_post"]: return "255,50,50"
    if "区长" in p["current_post"]: return "50,100,255"
    if "纪委书记" in p["current_post"]: return "255,165,0"
    return "100,100,100"

def is_top_leader(p):
    return "区委书记" in p["current_post"] or "区长" in p["current_post"]

def org_color(o):
    colors = {
        "党委": "255,200,200", "政府": "200,200,255",
        "人大": "200,255,255", "政协": "255,240,200",
        "开发区": "200,255,200", "乡镇": "255,255,200",
        "事业单位": "220,220,220",
    }
    return colors.get(o["type"], "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>芗城区领导班子工作关系网络 - 漳州市芗城区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        # Check if person and org exist
        p_exists = any(p["id"] == pid for p in persons)
        o_exists = any(o["id"] == oid for o in organizations)
        if p_exists and o_exists:
            lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')
            eid += 1

    # Person <-> Person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF: {len(persons)} person nodes, {len(organizations)} organization nodes, {eid} edges")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("芗城区领导班子工作关系网络数据构建")
    print(f"构建时间: {datetime.now().isoformat()}")
    print("=" * 60)
    build_db()
    build_gexf()
    print(f"\n📁 数据库: {DB_PATH}")
    print(f"📁 GEXF图: {GEXF_PATH}")
    print("✅ 构建完成")
