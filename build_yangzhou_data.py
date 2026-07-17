#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 扬州市 (Yangzhou City) leadership network.

Covers: City-level leadership (市委书记, 市长, 人大主任, 政协主席),
6 sub-divisions: 广陵区, 邗江区, 江都区, 宝应县, 仪征市, 高邮市.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yangzhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yangzhou_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership (扬州市本级) ──
    {"id":1,"name":"王进健","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"扬州市委书记","current_org":"中共扬州市委员会","source":"https://zh.wikipedia.org/wiki/%E6%89%AC%E5%B7%9E%E5%B8%82"},
    {"id":2,"name":"郑海涛","gender":"男","ethnicity":"汉族","birth":"1975","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"扬州市市长","current_org":"扬州市人民政府","source":"https://zh.wikipedia.org/wiki/%E6%89%AC%E5%B7%9E%E5%B8%82"},
    {"id":3,"name":"孔令俊","gender":"男","ethnicity":"汉族","birth":"1965","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"扬州市人大常委会主任","current_org":"扬州市人大常委会","source":"https://zh.wikipedia.org/wiki/%E6%89%AC%E5%B7%9E%E5%B8%82"},
    {"id":4,"name":"陈扬","gender":"男","ethnicity":"汉族","birth":"1963","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"扬州市政协主席","current_org":"政协扬州市委员会","source":"https://zh.wikipedia.org/wiki/%E6%89%AC%E5%B7%9E%E5%B8%82"},

    # ── 广陵区 ──
    {"id":5,"name":"张伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"广陵区委书记","current_org":"中共广陵区委员会","source":"https://zh.wikipedia.org/wiki/%E5%B9%BF%E9%99%B5%E5%8C%BA"},
    {"id":6,"name":"广陵区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"广陵区区长","current_org":"广陵区人民政府","source":""},

    # ── 邗江区 ──
    {"id":7,"name":"邗江区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"邗江区委书记","current_org":"中共邗江区委员会","source":""},
    {"id":8,"name":"邗江区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"邗江区区长","current_org":"邗江区人民政府","source":""},

    # ── 江都区 ──
    {"id":9,"name":"江都区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"江都区委书记","current_org":"中共江都区委员会","source":""},
    {"id":10,"name":"江都区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"江都区区长","current_org":"江都区人民政府","source":""},

    # ── 宝应县 ──
    {"id":11,"name":"宝应县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"宝应县委书记","current_org":"中共宝应县委员会","source":""},
    {"id":12,"name":"胡晓峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"宝应县县长","current_org":"宝应县人民政府","source":"https://zh.wikipedia.org/wiki/%E5%AE%9D%E5%BA%94%E5%8E%BF"},

    # ── 仪征市 ──
    {"id":13,"name":"王炳松","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"仪征市委书记","current_org":"中共仪征市委员会","source":"https://zh.wikipedia.org/wiki/%E4%BB%AA%E5%BE%81%E5%B8%82"},
    {"id":14,"name":"孙建年","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"仪征市代市长","current_org":"仪征市人民政府","source":"https://zh.wikipedia.org/wiki/%E4%BB%AA%E5%BE%81%E5%B8%82"},
    {"id":15,"name":"仲玲","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"仪征市人大常委会主任","current_org":"仪征市人大常委会","source":"https://zh.wikipedia.org/wiki/%E4%BB%AA%E5%BE%81%E5%B8%82"},

    # ── 高邮市 ──
    {"id":16,"name":"韦峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"高邮市委书记","current_org":"中共高邮市委员会","source":"https://zh.wikipedia.org/wiki/%E9%AB%98%E9%82%AE%E5%B8%82"},
    {"id":17,"name":"高邮市市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"高邮市市长","current_org":"高邮市人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Yangzhou city-level
    {"id":1,"name":"中共扬州市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省扬州市"},
    {"id":2,"name":"扬州市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省扬州市"},
    {"id":3,"name":"扬州市人大常委会","type":"人大","level":"地级","parent":"江苏省人大常委会","location":"江苏省扬州市"},
    {"id":4,"name":"政协扬州市委员会","type":"政协","level":"地级","parent":"政协江苏省委员会","location":"江苏省扬州市"},

    # Sub-divisions — 广陵区
    {"id":5,"name":"中共广陵区委员会","type":"党委","level":"县级","parent":"中共扬州市委员会","location":"江苏省扬州市广陵区"},
    {"id":6,"name":"广陵区人民政府","type":"政府","level":"县级","parent":"扬州市人民政府","location":"江苏省扬州市广陵区"},

    # 邗江区
    {"id":7,"name":"中共邗江区委员会","type":"党委","level":"县级","parent":"中共扬州市委员会","location":"江苏省扬州市邗江区"},
    {"id":8,"name":"邗江区人民政府","type":"政府","level":"县级","parent":"扬州市人民政府","location":"江苏省扬州市邗江区"},

    # 江都区
    {"id":9,"name":"中共江都区委员会","type":"党委","level":"县级","parent":"中共扬州市委员会","location":"江苏省扬州市江都区"},
    {"id":10,"name":"江都区人民政府","type":"政府","level":"县级","parent":"扬州市人民政府","location":"江苏省扬州市江都区"},

    # 宝应县
    {"id":11,"name":"中共宝应县委员会","type":"党委","level":"县级","parent":"中共扬州市委员会","location":"江苏省扬州市宝应县"},
    {"id":12,"name":"宝应县人民政府","type":"政府","level":"县级","parent":"扬州市人民政府","location":"江苏省扬州市宝应县"},

    # 仪征市
    {"id":13,"name":"中共仪征市委员会","type":"党委","level":"县级","parent":"中共扬州市委员会","location":"江苏省扬州市仪征市"},
    {"id":14,"name":"仪征市人民政府","type":"政府","level":"县级","parent":"扬州市人民政府","location":"江苏省扬州市仪征市"},
    {"id":15,"name":"仪征市人大常委会","type":"人大","level":"县级","parent":"扬州市人大常委会","location":"江苏省扬州市仪征市"},

    # 高邮市
    {"id":16,"name":"中共高邮市委员会","type":"党委","level":"县级","parent":"中共扬州市委员会","location":"江苏省扬州市高邮市"},
    {"id":17,"name":"高邮市人民政府","type":"政府","level":"县级","parent":"扬州市人民政府","location":"江苏省扬州市高邮市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 王进健 ──
    {"id":1,"person_id":1,"org_id":1,"title":"扬州市委书记","start":"","end":"","rank":"正厅级","note":"来自Wikipedia infobox"},
    # ── 郑海涛 ──
    {"id":2,"person_id":2,"org_id":2,"title":"扬州市市长","start":"","end":"","rank":"正厅级","note":"1975年生"},
    # ── 孔令俊 ──
    {"id":3,"person_id":3,"org_id":3,"title":"扬州市人大常委会主任","start":"","end":"","rank":"正厅级","note":"1965年生"},
    # ── 陈扬 ──
    {"id":4,"person_id":4,"org_id":4,"title":"扬州市政协主席","start":"","end":"","rank":"正厅级","note":"1963年生"},
    # ── 张伟（广陵区） ──
    {"id":5,"person_id":5,"org_id":5,"title":"广陵区委书记","start":"","end":"","rank":"副厅级","note":"来自Wikipedia infobox"},
    # ── 广陵区区长 ──
    {"id":6,"person_id":6,"org_id":6,"title":"广陵区区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    # ── 邗江区委书记 ──
    {"id":7,"person_id":7,"org_id":7,"title":"邗江区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    # ── 邗江区区长 ──
    {"id":8,"person_id":8,"org_id":8,"title":"邗江区区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    # ── 江都区委书记 ──
    {"id":9,"person_id":9,"org_id":9,"title":"江都区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    # ── 江都区区长 ──
    {"id":10,"person_id":10,"org_id":10,"title":"江都区区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    # ── 宝应县委书记 ──
    {"id":11,"person_id":11,"org_id":11,"title":"宝应县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    # ── 胡晓峰（宝应县） ──
    {"id":12,"person_id":12,"org_id":12,"title":"宝应县县长","start":"","end":"","rank":"正处级","note":"来自Wikipedia infobox"},
    # ── 王炳松（仪征市） ──
    {"id":13,"person_id":13,"org_id":13,"title":"仪征市委书记","start":"","end":"","rank":"副厅级","note":"来自Wikipedia infobox"},
    # ── 孙建年（仪征市） ──
    {"id":14,"person_id":14,"org_id":14,"title":"仪征市代市长","start":"","end":"","rank":"正处级","note":"来自Wikipedia infobox"},
    # ── 仲玲（仪征市） ──
    {"id":15,"person_id":15,"org_id":15,"title":"仪征市人大常委会主任","start":"","end":"","rank":"正处级","note":"来自Wikipedia infobox"},
    # ── 韦峰（高邮市） ──
    {"id":16,"person_id":16,"org_id":16,"title":"高邮市委书记","start":"","end":"","rank":"副厅级","note":"来自Wikipedia infobox"},
    # ── 高邮市市长 ──
    {"id":17,"person_id":17,"org_id":17,"title":"高邮市市长","start":"","end":"","rank":"正处级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政搭档 —— 市级 ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"王进健（市委书记）与郑海涛（市长）为扬州市党政一把手搭档","overlap_org":"扬州市","overlap_period":"至今"},

    # ── 市级与下属部委办局 ──
    {"id":2,"person_a":1,"person_b":3,"type":"党政搭档","context":"市委书记与人大常委会主任分工协作","overlap_org":"扬州市","overlap_period":"至今"},
    {"id":3,"person_a":2,"person_b":4,"type":"党政搭档","context":"市长与政协主席分工协作","overlap_org":"扬州市","overlap_period":"至今"},

    # ── 区县党政搭档 ──
    {"id":4,"person_a":5,"person_b":6,"type":"党政搭档","context":"张伟（广陵区委书记）与广陵区区长党政搭档","overlap_org":"广陵区","overlap_period":"至今"},
    {"id":5,"person_a":7,"person_b":8,"type":"党政搭档","context":"邗江区委书记与邗江区区长党政搭档","overlap_org":"邗江区","overlap_period":"至今"},
    {"id":6,"person_a":9,"person_b":10,"type":"党政搭档","context":"江都区委书记与江都区区长党政搭档","overlap_org":"江都区","overlap_period":"至今"},
    {"id":7,"person_a":11,"person_b":12,"type":"党政搭档","context":"宝应县委书记与胡晓峰（宝应县长）党政搭档","overlap_org":"宝应县","overlap_period":"至今"},
    {"id":8,"person_a":13,"person_b":14,"type":"党政搭档","context":"王炳松（仪征市委书记）与孙建年（仪征代市长）党政搭档","overlap_org":"仪征市","overlap_period":"至今"},
    {"id":9,"person_a":16,"person_b":17,"type":"党政搭档","context":"韦峰（高邮市委书记）与高邮市市长党政搭档","overlap_org":"高邮市","overlap_period":"至今"},

    # ── 上下级：市领导与下级区县领导 ──
    {"id":10,"person_a":1,"person_b":5,"type":"上下级","context":"市委书记领导广陵区委书记","overlap_org":"扬州市/广陵区","overlap_period":"至今"},
    {"id":11,"person_a":1,"person_b":7,"type":"上下级","context":"市委书记领导邗江区委书记","overlap_org":"扬州市/邗江区","overlap_period":"至今"},
    {"id":12,"person_a":1,"person_b":9,"type":"上下级","context":"市委书记领导江都区委书记","overlap_org":"扬州市/江都区","overlap_period":"至今"},
    {"id":13,"person_a":1,"person_b":11,"type":"上下级","context":"市委书记领导宝应县委书记","overlap_org":"扬州市/宝应县","overlap_period":"至今"},
    {"id":14,"person_a":1,"person_b":13,"type":"上下级","context":"市委书记领导仪征市委书记","overlap_org":"扬州市/仪征市","overlap_period":"至今"},
    {"id":15,"person_a":1,"person_b":16,"type":"上下级","context":"市委书记领导高邮市委书记","overlap_org":"扬州市/高邮市","overlap_period":"至今"},

    {"id":16,"person_a":2,"person_b":6,"type":"上下级","context":"市长领导广陵区区长","overlap_org":"扬州市/广陵区","overlap_period":"至今"},
    {"id":17,"person_a":2,"person_b":8,"type":"上下级","context":"市长领导邗江区区长","overlap_org":"扬州市/邗江区","overlap_period":"至今"},
    {"id":18,"person_a":2,"person_b":10,"type":"上下级","context":"市长领导江都区区长","overlap_org":"扬州市/江都区","overlap_period":"至今"},
    {"id":19,"person_a":2,"person_b":12,"type":"上下级","context":"市长领导宝应县县长","overlap_org":"扬州市/宝应县","overlap_period":"至今"},
    {"id":20,"person_a":2,"person_b":14,"type":"上下级","context":"市长领导仪征市代市长","overlap_org":"扬州市/仪征市","overlap_period":"至今"},
    {"id":21,"person_a":2,"person_b":17,"type":"上下级","context":"市长领导高邮市市长","overlap_org":"扬州市/高邮市","overlap_period":"至今"},
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
    if "书记" in post and "区委" not in post and "市委" in post:
        return "200,30,30"
    if "市长" in post or "县长" in post:
        return "30,80,200"
    if "人大" in post:
        return "160,200,220"
    if "政协" in post:
        return "180,160,220"
    if "区委书记" in post or "县委书记" in post or "市委书记" in post:
        return "200,60,60"
    if "代市长" in post:
        return "60,120,220"
    if "区长" in post:
        return "60,120,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>扬州市（地级市）领导班子工作关系网络 — 2026年7月14日生成</description>')
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
