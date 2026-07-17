#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 南通市 (Nantong City) leadership network.

Covers: City-level leadership (市委书记, 市长, 政协主席),
7 district/county-level sub-divisions: 崇川区, 通州区, 海门区,
如东县, 启东市, 如皋市, 海安市.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/nantong_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/nantong_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委 ──
    # 1. 吴新明 — 南通市委书记 (1969-06, 江苏苏州吴江, 2023.03任)
    {"id":1,"name":"吴新明","gender":"男","ethnicity":"汉族","birth":"1969-06","birthplace":"江苏苏州吴江","education":"","party_join":"","work_start":"","current_post":"南通市委书记","current_org":"中共南通市委员会","source":""},
    # 2. 张彤 — 南通市长 (女, 1971-10, 江苏宿迁, 2023.07任)
    {"id":2,"name":"张彤","gender":"女","ethnicity":"汉族","birth":"1971-10","birthplace":"江苏宿迁","education":"","party_join":"","work_start":"","current_post":"南通市长","current_org":"南通市人民政府","source":""},
    # 3. 周伟文 — 市政协主席 (1968-12, 江苏涟水)
    {"id":3,"name":"周伟文","gender":"男","ethnicity":"汉族","birth":"1968-12","birthplace":"江苏涟水","education":"","party_join":"","work_start":"","current_post":"南通市政协主席","current_org":"政协南通市委员会","source":""},

    # ── District/County-level leadership (known) ──
    # 4. 沈旭东 — 海门区委书记
    {"id":4,"name":"沈旭东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"海门区委书记","current_org":"中共海门区委员会","source":""},
    # 5. 杨万平 — 如东县委书记
    {"id":5,"name":"杨万平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"如东县委书记","current_org":"中共如东县委员会","source":""},
    # 6. 杨中坚 — 启东市长
    {"id":6,"name":"杨中坚","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"启东市长","current_org":"启东市人民政府","source":""},
    # 7. 王鸣昊 — 如皋市委书记
    {"id":7,"name":"王鸣昊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"如皋市委书记","current_org":"中共如皋市委员会","source":""},

    # ── Placeholder entries for missing data (待查) ──
    # 崇川区委书记
    {"id":8,"name":"崇川区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"崇川区委书记","current_org":"中共崇川区委员会","source":""},
    # 崇川区长
    {"id":9,"name":"崇川区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"崇川区长","current_org":"崇川区人民政府","source":""},
    # 通州区委书记
    {"id":10,"name":"通州区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"通州区委书记","current_org":"中共通州区委员会","source":""},
    # 通州区区长
    {"id":11,"name":"通州区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"通州区区长","current_org":"通州区人民政府","source":""},
    # 海门区长
    {"id":12,"name":"海门区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"海门区长","current_org":"海门区人民政府","source":""},
    # 如东县长
    {"id":13,"name":"如东县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"如东县长","current_org":"如东县人民政府","source":""},
    # 启东市委书记
    {"id":14,"name":"启东市委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"启东市委书记","current_org":"中共启东市委员会","source":""},
    # 如皋市长
    {"id":15,"name":"如皋市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"如皋市长","current_org":"如皋市人民政府","source":""},
    # 海安市委书记
    {"id":16,"name":"海安市委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"海安市委书记","current_org":"中共海安市委员会","source":""},
    # 海安市市长
    {"id":17,"name":"海安市市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"海安市市长","current_org":"海安市人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Nantong city-level core ──
    {"id":1,"name":"中共南通市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省南通市"},
    {"id":2,"name":"南通市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省南通市"},
    {"id":3,"name":"南通市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省南通市"},
    {"id":4,"name":"政协南通市委员会","type":"政协","level":"地级","parent":"","location":"江苏省南通市"},
    {"id":5,"name":"中共南通市纪律检查委员会","type":"党委","level":"地级","parent":"中共南通市委员会","location":"江苏省南通市"},

    # ── 3 Districts — Party committees ──
    {"id":6,"name":"中共崇川区委员会","type":"党委","level":"县级","parent":"中共南通市委员会","location":"江苏省南通市崇川区"},
    {"id":7,"name":"中共通州区委员会","type":"党委","level":"县级","parent":"中共南通市委员会","location":"江苏省南通市通州区"},
    {"id":8,"name":"中共海门区委员会","type":"党委","level":"县级","parent":"中共南通市委员会","location":"江苏省南通市海门区"},

    # ── 1 County — Party committee ──
    {"id":9,"name":"中共如东县委员会","type":"党委","level":"县级","parent":"中共南通市委员会","location":"江苏省南通市如东县"},

    # ── 3 County-level cities — Party committees ──
    {"id":10,"name":"中共启东市委员会","type":"党委","level":"县级","parent":"中共南通市委员会","location":"江苏省南通市启东市"},
    {"id":11,"name":"中共如皋市委员会","type":"党委","level":"县级","parent":"中共南通市委员会","location":"江苏省南通市如皋市"},
    {"id":12,"name":"中共海安市委员会","type":"党委","level":"县级","parent":"中共南通市委员会","location":"江苏省南通市海安市"},

    # ── 3 Districts — Governments ──
    {"id":13,"name":"崇川区人民政府","type":"政府","level":"县级","parent":"南通市人民政府","location":"江苏省南通市崇川区"},
    {"id":14,"name":"通州区人民政府","type":"政府","level":"县级","parent":"南通市人民政府","location":"江苏省南通市通州区"},
    {"id":15,"name":"海门区人民政府","type":"政府","level":"县级","parent":"南通市人民政府","location":"江苏省南通市海门区"},

    # ── 1 County — Government ──
    {"id":16,"name":"如东县人民政府","type":"政府","level":"县级","parent":"南通市人民政府","location":"江苏省南通市如东县"},

    # ── 3 County-level cities — Governments ──
    {"id":17,"name":"启东市人民政府","type":"政府","level":"县级","parent":"南通市人民政府","location":"江苏省南通市启东市"},
    {"id":18,"name":"如皋市人民政府","type":"政府","level":"县级","parent":"南通市人民政府","location":"江苏省南通市如皋市"},
    {"id":19,"name":"海安市人民政府","type":"政府","level":"县级","parent":"南通市人民政府","location":"江苏省南通市海安市"},

    # ── External / higher-level orgs ──
    {"id":20,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":21,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 吴新明 (南通市委书记) ──
    {"id":1,"person_id":1,"org_id":1,"title":"南通市委书记","start":"2023-03","end":"","rank":"副部级","note":"1969年生，江苏苏州吴江人，2023.03任"},
    {"id":2,"person_id":1,"org_id":1,"title":"南通市委副书记","start":"2023-03","end":"","rank":"副部级","note":""},

    # ── 张彤 (南通市长) ──
    {"id":3,"person_id":2,"org_id":2,"title":"南通市长","start":"2023-07","end":"","rank":"副部级","note":"女，1971年生，江苏宿迁人，2023.07任"},
    {"id":4,"person_id":2,"org_id":1,"title":"南通市委副书记","start":"2023-07","end":"","rank":"副部级","note":""},

    # ── 周伟文 (市政协主席) ──
    {"id":5,"person_id":3,"org_id":4,"title":"南通市政协主席","start":"","end":"","rank":"正厅级","note":"1968年生，江苏涟水人"},

    # ── 沈旭东 (海门区委书记) ──
    {"id":6,"person_id":4,"org_id":8,"title":"海门区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 杨万平 (如东县委书记) ──
    {"id":7,"person_id":5,"org_id":9,"title":"如东县委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 杨中坚 (启东市长) ──
    {"id":8,"person_id":6,"org_id":17,"title":"启东市长","start":"","end":"","rank":"正厅级","note":""},

    # ── 王鸣昊 (如皋市委书记) ──
    {"id":9,"person_id":7,"org_id":11,"title":"如皋市委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── Placeholder positions (信息待查) ──
    {"id":10,"person_id":8,"org_id":6,"title":"崇川区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":11,"person_id":9,"org_id":13,"title":"崇川区长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":12,"person_id":10,"org_id":7,"title":"通州区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":13,"person_id":11,"org_id":14,"title":"通州区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":14,"person_id":12,"org_id":15,"title":"海门区长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":15,"person_id":13,"org_id":16,"title":"如东县长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":16,"person_id":14,"org_id":10,"title":"启东市委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":17,"person_id":15,"org_id":18,"title":"如皋市长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":18,"person_id":16,"org_id":12,"title":"海安市委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":19,"person_id":17,"org_id":19,"title":"海安市市长","start":"","end":"","rank":"正厅级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 吴新明 ↔ 张彤（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"吴新明（南通市委书记）与张彤（市长）为南通市党政一把手搭档","overlap_org":"南通市","overlap_period":"2023.07至今"},

    # ── 各区县书记/区县长与市书记 (隶属关系) ──
    # 崇川区
    {"id":2,"person_a":1,"person_b":8,"type":"隶属关系","context":"吴新明（市委书记）领导崇川区委书记","overlap_org":"南通市","overlap_period":""},
    # 通州区
    {"id":3,"person_a":1,"person_b":10,"type":"隶属关系","context":"吴新明（市委书记）领导通州区委书记","overlap_org":"南通市","overlap_period":""},
    # 海门区
    {"id":4,"person_a":1,"person_b":4,"type":"隶属关系","context":"吴新明（市委书记）领导沈旭东（海门区委书记）","overlap_org":"南通市","overlap_period":""},
    # 如东县
    {"id":5,"person_a":1,"person_b":5,"type":"隶属关系","context":"吴新明（市委书记）领导杨万平（如东县委书记）","overlap_org":"南通市","overlap_period":""},
    # 启东市
    {"id":6,"person_a":1,"person_b":14,"type":"隶属关系","context":"吴新明（市委书记）领导启东市委书记","overlap_org":"南通市","overlap_period":""},
    # 如皋市
    {"id":7,"person_a":1,"person_b":7,"type":"隶属关系","context":"吴新明（市委书记）领导王鸣昊（如皋市委书记）","overlap_org":"南通市","overlap_period":""},
    # 海安市
    {"id":8,"person_a":1,"person_b":16,"type":"隶属关系","context":"吴新明（市委书记）领导海安市委书记","overlap_org":"南通市","overlap_period":""},

    # ── 各区县书记与区县长（党政搭档）──
    # 崇川区
    {"id":9,"person_a":8,"person_b":9,"type":"党政搭档","context":"崇川区委书记与崇川区长党政搭档","overlap_org":"崇川区","overlap_period":""},
    # 通州区
    {"id":10,"person_a":10,"person_b":11,"type":"党政搭档","context":"通州区委书记与通州区区长党政搭档","overlap_org":"通州区","overlap_period":""},
    # 海门区
    {"id":11,"person_a":4,"person_b":12,"type":"党政搭档","context":"沈旭东（海门区委书记）与海门区长党政搭档","overlap_org":"海门区","overlap_period":""},
    # 如东县
    {"id":12,"person_a":5,"person_b":13,"type":"党政搭档","context":"杨万平（如东县委书记）与如东县长党政搭档","overlap_org":"如东县","overlap_period":""},
    # 启东市
    {"id":13,"person_a":14,"person_b":6,"type":"党政搭档","context":"启东市委书记与杨中坚（启东市长）党政搭档","overlap_org":"启东市","overlap_period":""},
    # 如皋市
    {"id":14,"person_a":7,"person_b":15,"type":"党政搭档","context":"王鸣昊（如皋市委书记）与如皋市长党政搭档","overlap_org":"如皋市","overlap_period":""},
    # 海安市
    {"id":15,"person_a":16,"person_b":17,"type":"党政搭档","context":"海安市委书记与海安市市长党政搭档","overlap_org":"海安市","overlap_period":""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "市委书记" in post and "市委" in post:
        return "200,30,30"  # deep red for party secretary
    if "市长" in post or "区长" in post or "县长" in post:
        return "30,80,200"  # deep blue for mayor/district head
    if "副书记" in post:
        return "220,60,60"
    if "副市长" in post or "副区长" in post:
        return "60,120,220"
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"
    if "组织部长" in post or "统战部长" in post or "宣传部长" in post or "政法委" in post:
        return "180,90,180"
    if "政协" in post:
        return "180,160,220"
    if "人大" in post:
        return "160,200,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>南通市（地级市）领导班子 + 7区县市工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c_ = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c_ = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
