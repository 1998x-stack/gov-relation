#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 淮安市 (Huai'an City) leadership network.

Covers: City-level leadership (市委书记, 市长),
7 sub-divisions: 淮安区, 淮阴区, 清江浦区, 洪泽区, 涟水县, 盱眙县, 金湖县.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/huaian_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/huaian_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委/市政府 ──
    # 1. 史志军 — 淮安市委书记 (1969-04, 江苏溧阳)
    {"id":1,"name":"史志军","gender":"男","ethnicity":"汉族","birth":"1969-04","birthplace":"江苏溧阳","education":"","party_join":"","work_start":"","current_post":"淮安市委书记","current_org":"中共淮安市委员会","source":"https://zh.wikipedia.org/wiki/%E5%8F%B2%E5%BF%97%E5%86%9B"},
    # 2. 顾坤 — 淮安市市长 (1976-01, 江苏海门)
    {"id":2,"name":"顾坤","gender":"男","ethnicity":"汉族","birth":"1976-01","birthplace":"江苏海门","education":"","party_join":"","work_start":"","current_post":"淮安市市长","current_org":"淮安市人民政府","source":"https://zh.wikipedia.org/wiki/%E9%A1%BE%E5%9D%A4"},

    # ── 3 Districts (区) ──
    # 3. 淮安区 — 书记待查
    {"id":3,"name":"淮安区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"淮安区委书记","current_org":"中共淮安区委员会","source":""},
    # 4. 淮安区 — 区长待查
    {"id":4,"name":"淮安区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"淮安区区长","current_org":"淮安区人民政府","source":""},

    # 5. 淮阴区 — 书记待查
    {"id":5,"name":"淮阴区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"淮阴区委书记","current_org":"中共淮阴区委员会","source":""},
    # 6. 淮阴区 — 区长待查
    {"id":6,"name":"淮阴区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"淮阴区区长","current_org":"淮阴区人民政府","source":""},

    # 7. 清江浦区 — 书记待查
    {"id":7,"name":"清江浦区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"清江浦区委书记","current_org":"中共清江浦区委员会","source":""},
    # 8. 清江浦区 — 区长待查
    {"id":8,"name":"清江浦区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"清江浦区区长","current_org":"清江浦区人民政府","source":""},

    # 9. 洪泽区 — 书记待查
    {"id":9,"name":"洪泽区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"洪泽区委书记","current_org":"中共洪泽区委员会","source":""},
    # 10. 洪泽区 — 区长待查
    {"id":10,"name":"洪泽区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"洪泽区区长","current_org":"洪泽区人民政府","source":""},

    # ── 2 Counties (县) ──
    # 11. 涟水县 — 书记待查
    {"id":11,"name":"涟水县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"涟水县委书记","current_org":"中共涟水县委员会","source":""},
    # 12. 涟水县 — 县长待查
    {"id":12,"name":"涟水县县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"涟水县县长","current_org":"涟水县人民政府","source":""},

    # 13. 孙志标 — 盱眙县委书记
    {"id":13,"name":"孙志标","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"盱眙县委书记","current_org":"中共盱眙县委员会","source":""},
    # 14. 盱眙县 — 县长待查
    {"id":14,"name":"盱眙县县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"盱眙县县长","current_org":"盱眙县人民政府","source":""},

    # 15. 贺宝祥 — 金湖县委书记
    {"id":15,"name":"贺宝祥","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"金湖县委书记","current_org":"中共金湖县委员会","source":""},
    # 16. 金湖县 — 县长待查
    {"id":16,"name":"金湖县县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"金湖县县长","current_org":"金湖县人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Huai'an city-level
    {"id":1,"name":"中共淮安市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省淮安市"},
    {"id":2,"name":"淮安市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省淮安市"},

    # ── 4 Districts — Party committees ──
    {"id":3,"name":"中共淮安区委员会","type":"党委","level":"县级","parent":"中共淮安市委员会","location":"江苏省淮安市淮安区"},
    {"id":4,"name":"中共淮阴区委员会","type":"党委","level":"县级","parent":"中共淮安市委员会","location":"江苏省淮安市淮阴区"},
    {"id":5,"name":"中共清江浦区委员会","type":"党委","level":"县级","parent":"中共淮安市委员会","location":"江苏省淮安市清江浦区"},
    {"id":6,"name":"中共洪泽区委员会","type":"党委","level":"县级","parent":"中共淮安市委员会","location":"江苏省淮安市洪泽区"},

    # ── 3 Counties — Party committees ──
    {"id":7,"name":"中共涟水县委员会","type":"党委","level":"县级","parent":"中共淮安市委员会","location":"江苏省淮安市涟水县"},
    {"id":8,"name":"中共盱眙县委员会","type":"党委","level":"县级","parent":"中共淮安市委员会","location":"江苏省淮安市盱眙县"},
    {"id":9,"name":"中共金湖县委员会","type":"党委","level":"县级","parent":"中共淮安市委员会","location":"江苏省淮安市金湖县"},

    # ── 4 Districts — Governments ──
    {"id":10,"name":"淮安区人民政府","type":"政府","level":"县级","parent":"淮安市人民政府","location":"江苏省淮安市淮安区"},
    {"id":11,"name":"淮阴区人民政府","type":"政府","level":"县级","parent":"淮安市人民政府","location":"江苏省淮安市淮阴区"},
    {"id":12,"name":"清江浦区人民政府","type":"政府","level":"县级","parent":"淮安市人民政府","location":"江苏省淮安市清江浦区"},
    {"id":13,"name":"洪泽区人民政府","type":"政府","level":"县级","parent":"淮安市人民政府","location":"江苏省淮安市洪泽区"},

    # ── 3 Counties — Governments ──
    {"id":14,"name":"涟水县人民政府","type":"政府","level":"县级","parent":"淮安市人民政府","location":"江苏省淮安市涟水县"},
    {"id":15,"name":"盱眙县人民政府","type":"政府","level":"县级","parent":"淮安市人民政府","location":"江苏省淮安市盱眙县"},
    {"id":16,"name":"金湖县人民政府","type":"政府","level":"县级","parent":"淮安市人民政府","location":"江苏省淮安市金湖县"},

    # External higher-level orgs
    {"id":17,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":18,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 史志军 (淮安市委书记) ──
    {"id":1,"person_id":1,"org_id":1,"title":"淮安市委书记","start":"","end":"","rank":"正厅级","note":"1969-04，江苏溧阳人"},
    # ── 顾坤 (淮安市市长) ──
    {"id":2,"person_id":2,"org_id":2,"title":"淮安市市长","start":"","end":"","rank":"正厅级","note":"1976-01，江苏海门人"},

    # ── Placeholder positions ──
    {"id":3,"person_id":3,"org_id":3,"title":"淮安区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":4,"person_id":4,"org_id":10,"title":"淮安区区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":5,"person_id":5,"org_id":4,"title":"淮阴区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":6,"person_id":6,"org_id":11,"title":"淮阴区区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":7,"person_id":7,"org_id":5,"title":"清江浦区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":8,"person_id":8,"org_id":12,"title":"清江浦区区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":9,"person_id":9,"org_id":6,"title":"洪泽区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":10,"person_id":10,"org_id":13,"title":"洪泽区区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":11,"person_id":11,"org_id":7,"title":"涟水县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":12,"person_id":12,"org_id":14,"title":"涟水县县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":13,"person_id":13,"org_id":8,"title":"盱眙县委书记","start":"","end":"","rank":"副厅级","note":"已确认姓名"},
    {"id":14,"person_id":14,"org_id":15,"title":"盱眙县县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":15,"person_id":15,"org_id":9,"title":"金湖县委书记","start":"","end":"","rank":"副厅级","note":"已确认姓名"},
    {"id":16,"person_id":16,"org_id":16,"title":"金湖县县长","start":"","end":"","rank":"正处级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政搭档 市级 ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"史志军（市委书记）与顾坤（市长）为淮安市党政一把手搭档","overlap_org":"淮安市","overlap_period":"至今"},

    # ── 上下级：市委书记 → 各区/县委书记 ──
    {"id":2,"person_a":1,"person_b":3,"type":"上下级","context":"市委书记领导淮安区委书记","overlap_org":"淮安市/淮安区","overlap_period":"至今"},
    {"id":3,"person_a":1,"person_b":5,"type":"上下级","context":"市委书记领导淮阴区委书记","overlap_org":"淮安市/淮阴区","overlap_period":"至今"},
    {"id":4,"person_a":1,"person_b":7,"type":"上下级","context":"市委书记领导清江浦区委书记","overlap_org":"淮安市/清江浦区","overlap_period":"至今"},
    {"id":5,"person_a":1,"person_b":9,"type":"上下级","context":"市委书记领导洪泽区委书记","overlap_org":"淮安市/洪泽区","overlap_period":"至今"},
    {"id":6,"person_a":1,"person_b":11,"type":"上下级","context":"市委书记领导涟水县委书记","overlap_org":"淮安市/涟水县","overlap_period":"至今"},
    {"id":7,"person_a":1,"person_b":13,"type":"上下级","context":"市委书记领导孙志标（盱眙县委书记）","overlap_org":"淮安市/盱眙县","overlap_period":"至今"},
    {"id":8,"person_a":1,"person_b":15,"type":"上下级","context":"市委书记领导贺宝祥（金湖县委书记）","overlap_org":"淮安市/金湖县","overlap_period":"至今"},

    # ── 上下级：市长 → 各区/县长 ──
    {"id":9,"person_a":2,"person_b":4,"type":"上下级","context":"市长领导淮安区区长","overlap_org":"淮安市/淮安区","overlap_period":"至今"},
    {"id":10,"person_a":2,"person_b":6,"type":"上下级","context":"市长领导淮阴区区长","overlap_org":"淮安市/淮阴区","overlap_period":"至今"},
    {"id":11,"person_a":2,"person_b":8,"type":"上下级","context":"市长领导清江浦区区长","overlap_org":"淮安市/清江浦区","overlap_period":"至今"},
    {"id":12,"person_a":2,"person_b":10,"type":"上下级","context":"市长领导洪泽区区长","overlap_org":"淮安市/洪泽区","overlap_period":"至今"},
    {"id":13,"person_a":2,"person_b":12,"type":"上下级","context":"市长领导涟水县县长","overlap_org":"淮安市/涟水县","overlap_period":"至今"},
    {"id":14,"person_a":2,"person_b":14,"type":"上下级","context":"市长领导盱眙县县长","overlap_org":"淮安市/盱眙县","overlap_period":"至今"},
    {"id":15,"person_a":2,"person_b":16,"type":"上下级","context":"市长领导金湖县县长","overlap_org":"淮安市/金湖县","overlap_period":"至今"},
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
    if "书记" in post and "市委" in post and "区委" not in post and "县委" not in post and "县委" not in post.replace("县委书记",""):
        return "200,30,30"
    if "市长" in post or "县长" in post:
        return "30,80,200"
    if "人大" in post:
        return "160,200,220"
    if "政协" in post:
        return "180,160,220"
    if "区委书记" in post or "县委书记" in post or "市委书记" in post:
        return "200,60,60"
    if "区长" in post or "县长" in post:
        return "60,120,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>淮安市（地级市）领导班子工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","current_post"),("3","entity_type"),("4","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = "16.0" if any(k in p.get("current_post","") for k in ["市委书记","市长"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("current_post","")),("3","person"),("4","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",""),("3","organization"),("4",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
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
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",r.get("overlap_period","")),("2",""),("3",r.get("context",""))]:
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
