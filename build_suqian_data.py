#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 宿迁市 (Suqian City) leadership network.

Covers: City-level leadership (市委书记, 市长),
5 district/county-level sub-divisions: 宿城区, 宿豫区,
沭阳县, 泗阳县, 泗洪县.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/suqian_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/suqian_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership ──
    # 1. 盛蕾 — 宿迁市委书记 (女, 1972-11, 江苏苏州, 2024.12任)
    {"id":1,"name":"盛蕾","gender":"女","ethnicity":"汉族","birth":"1972-11","birthplace":"江苏苏州","education":"","party_join":"","work_start":"","current_post":"宿迁市委书记","current_org":"中共宿迁市委员会","source":""},
    # 2. 刘浩 — 宿迁市长 (1973-05, 江苏邳州, 2023.05任)
    {"id":2,"name":"刘浩","gender":"男","ethnicity":"汉族","birth":"1973-05","birthplace":"江苏邳州","education":"","party_join":"","work_start":"","current_post":"宿迁市市长","current_org":"宿迁市人民政府","source":""},

    # ── Known subs ──
    # 3. 王瑞 — 沭阳县长
    {"id":3,"name":"王瑞","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"沭阳县长","current_org":"沭阳县人民政府","source":""},
    # 4. 马伟 — 泗阳县委书记
    {"id":4,"name":"马伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"泗阳县委书记","current_org":"中共泗阳县委员会","source":""},
    # 5. 杨云峰 — 泗洪县委书记
    {"id":5,"name":"杨云峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"泗洪县委书记","current_org":"中共泗洪县委员会","source":""},

    # ── Placeholder entries for missing data (待查) ──
    # 宿城区委书记
    {"id":6,"name":"宿城区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"宿城区委书记","current_org":"中共宿城区委员会","source":""},
    # 宿城区长
    {"id":7,"name":"宿城区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"宿城区长","current_org":"宿城区人民政府","source":""},
    # 宿豫区委书记
    {"id":8,"name":"宿豫区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"宿豫区委书记","current_org":"中共宿豫区委员会","source":""},
    # 宿豫区长
    {"id":9,"name":"宿豫区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"宿豫区长","current_org":"宿豫区人民政府","source":""},
    # 沭阳县委书记
    {"id":10,"name":"沭阳县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"沭阳县委书记","current_org":"中共沭阳县委员会","source":""},
    # 泗阳县长
    {"id":11,"name":"泗阳县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"泗阳县长","current_org":"泗阳县人民政府","source":""},
    # 泗洪县长
    {"id":12,"name":"泗洪县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"泗洪县长","current_org":"泗洪县人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Suqian city-level core ──
    {"id":1,"name":"中共宿迁市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省宿迁市"},
    {"id":2,"name":"宿迁市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省宿迁市"},
    {"id":3,"name":"宿迁市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省宿迁市"},
    {"id":4,"name":"政协宿迁市委员会","type":"政协","level":"地级","parent":"","location":"江苏省宿迁市"},
    {"id":5,"name":"中共宿迁市纪律检查委员会","type":"党委","level":"地级","parent":"中共宿迁市委员会","location":"江苏省宿迁市"},

    # ── 2 Districts — Party committees ──
    {"id":6,"name":"中共宿城区委员会","type":"党委","level":"县级","parent":"中共宿迁市委员会","location":"江苏省宿迁市宿城区"},
    {"id":7,"name":"中共宿豫区委员会","type":"党委","level":"县级","parent":"中共宿迁市委员会","location":"江苏省宿迁市宿豫区"},

    # ── 3 Counties — Party committees ──
    {"id":8,"name":"中共沭阳县委员会","type":"党委","level":"县级","parent":"中共宿迁市委员会","location":"江苏省宿迁市沭阳县"},
    {"id":9,"name":"中共泗阳县委员会","type":"党委","level":"县级","parent":"中共宿迁市委员会","location":"江苏省宿迁市泗阳县"},
    {"id":10,"name":"中共泗洪县委员会","type":"党委","level":"县级","parent":"中共宿迁市委员会","location":"江苏省宿迁市泗洪县"},

    # ── 2 Districts — Governments ──
    {"id":11,"name":"宿城区人民政府","type":"政府","level":"县级","parent":"宿迁市人民政府","location":"江苏省宿迁市宿城区"},
    {"id":12,"name":"宿豫区人民政府","type":"政府","level":"县级","parent":"宿迁市人民政府","location":"江苏省宿迁市宿豫区"},

    # ── 3 Counties — Governments ──
    {"id":13,"name":"沭阳县人民政府","type":"政府","level":"县级","parent":"宿迁市人民政府","location":"江苏省宿迁市沭阳县"},
    {"id":14,"name":"泗阳县人民政府","type":"政府","level":"县级","parent":"宿迁市人民政府","location":"江苏省宿迁市泗阳县"},
    {"id":15,"name":"泗洪县人民政府","type":"政府","level":"县级","parent":"宿迁市人民政府","location":"江苏省宿迁市泗洪县"},

    # ── External / higher-level orgs ──
    {"id":16,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":17,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 盛蕾 (宿迁市委书记, 女) ──
    {"id":1,"person_id":1,"org_id":1,"title":"宿迁市委书记","start":"2024-12","end":"","rank":"副部级","note":"1972年生，女，江苏苏州人，2024.12任"},
    {"id":2,"person_id":1,"org_id":1,"title":"宿迁市委副书记","start":"2024-12","end":"","rank":"副部级","note":""},

    # ── 刘浩 (宿迁市市长) ──
    {"id":3,"person_id":2,"org_id":2,"title":"宿迁市市长","start":"2023-05","end":"","rank":"副部级","note":"1973-05，江苏邳州人，2023.05任"},
    {"id":4,"person_id":2,"org_id":1,"title":"宿迁市委副书记","start":"2023-05","end":"","rank":"副部级","note":""},

    # ── 王瑞 (沭阳县长) ──
    {"id":5,"person_id":3,"org_id":13,"title":"沭阳县长","start":"","end":"","rank":"正处级","note":""},

    # ── 马伟 (泗阳县委书记) ──
    {"id":6,"person_id":4,"org_id":9,"title":"泗阳县委书记","start":"","end":"","rank":"副厅级","note":""},

    # ── 杨云峰 (泗洪县委书记) ──
    {"id":7,"person_id":5,"org_id":10,"title":"泗洪县委书记","start":"","end":"","rank":"副厅级","note":""},

    # ── Placeholder positions ──
    {"id":8,"person_id":6,"org_id":6,"title":"宿城区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":9,"person_id":7,"org_id":11,"title":"宿城区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":10,"person_id":8,"org_id":7,"title":"宿豫区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":11,"person_id":9,"org_id":12,"title":"宿豫区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":12,"person_id":10,"org_id":8,"title":"沭阳县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":13,"person_id":11,"org_id":14,"title":"泗阳县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":14,"person_id":12,"org_id":15,"title":"泗洪县长","start":"","end":"","rank":"正处级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 盛蕾 ↔ 刘浩（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"盛蕾（宿迁市委书记）与刘浩（市长）为宿迁市党政一把手搭档","overlap_org":"宿迁市","overlap_period":"2024-12至今"},

    # ── 各区委/县委书记与区长/县长（党政搭档）──
    # 宿城区
    {"id":2,"person_a":6,"person_b":7,"type":"党政搭档","context":"宿城区委书记与宿城区长党政搭档","overlap_org":"宿城区","overlap_period":""},
    # 宿豫区
    {"id":3,"person_a":8,"person_b":9,"type":"党政搭档","context":"宿豫区委书记与宿豫区长党政搭档","overlap_org":"宿豫区","overlap_period":""},
    # 沭阳县
    {"id":4,"person_a":10,"person_b":3,"type":"党政搭档","context":"沭阳县委书记与王瑞（沭阳县长）党政搭档","overlap_org":"沭阳县","overlap_period":""},
    # 泗阳县
    {"id":5,"person_a":4,"person_b":11,"type":"党政搭档","context":"马伟（泗阳县委书记）与泗阳县长党政搭档","overlap_org":"泗阳县","overlap_period":""},
    # 泗洪县
    {"id":6,"person_a":5,"person_b":12,"type":"党政搭档","context":"杨云峰（泗洪县委书记）与泗洪县长党政搭档","overlap_org":"泗洪县","overlap_period":""},

    # ── 市区联系：各区委/县委书记向市委书记汇报 ──
    {"id":7,"person_a":1,"person_b":6,"type":"隶属关系","context":"盛蕾（市委书记）领导宿城区委书记","overlap_org":"宿迁市","overlap_period":""},
    {"id":8,"person_a":1,"person_b":8,"type":"隶属关系","context":"盛蕾（市委书记）领导宿豫区委书记","overlap_org":"宿迁市","overlap_period":""},
    {"id":9,"person_a":1,"person_b":10,"type":"隶属关系","context":"盛蕾（市委书记）领导沭阳县委书记","overlap_org":"宿迁市","overlap_period":""},
    {"id":10,"person_a":1,"person_b":4,"type":"隶属关系","context":"盛蕾（市委书记）领导马伟（泗阳县委书记）","overlap_org":"宿迁市","overlap_period":""},
    {"id":11,"person_a":1,"person_b":5,"type":"隶属关系","context":"盛蕾（市委书记）领导杨云峰（泗洪县委书记）","overlap_org":"宿迁市","overlap_period":""},
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
        return "200,30,30"
    if "市长" in post or "区长" in post or "县长" in post:
        return "30,80,200"
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
lines.append('    <description>宿迁市（地级市）领导班子 + 5区县工作关系网络 — 2026年7月14日生成</description>')
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
