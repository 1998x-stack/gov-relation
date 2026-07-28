#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乌什县 (Wushi County) leadership network.
   Data from official government website www.ws.gov.cn (as of July 2026).
   Research date: 2026-07-28."""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "乌什县_network.db")
GEXF_PATH = os.path.join(BASE, "乌什县_network.gexf")

persons = [
    {"id": 1, "name": "吴新疆", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共乌什县委书记", "current_org": "中共乌什县委员会",
     "source": "http://www.ws.gov.cn/"},
    {"id": 2, "name": "格帕尔·阿布都卡德尔", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "乌什县委副书记、县长", "current_org": "乌什县人民政府",
     "source": "http://www.ws.gov.cn/"},
    {"id": 3, "name": "颜画", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任乌什县委书记", "current_org": "中共乌什县委员会",
     "source": ""},
    {"id": 4, "name": "马建军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "乌什县委常委、政法委书记", "current_org": "中共乌什县委员会",
     "source": ""},
    {"id": 5, "name": "周象征", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "乌什县委常委、组织部部长", "current_org": "中共乌什县委员会",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共乌什县委员会", "type": "党委", "level": "县处级",
     "parent": "中共阿克苏地区委员会", "location": "新疆阿克苏地区乌什县"},
    {"id": 2, "name": "乌什县人民政府", "type": "政府", "level": "县处级",
     "parent": "阿克苏地区行政公署", "location": "新疆阿克苏地区乌什县"},
    {"id": 3, "name": "中共乌什县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共阿克苏地区纪律检查委员会", "location": "新疆阿克苏地区乌什县"},
    {"id": 4, "name": "乌什县人大常委会", "type": "人大", "level": "县处级",
     "parent": "阿克苏地区人大工委", "location": "新疆阿克苏地区乌什县"},
    {"id": 5, "name": "政协乌什县委员会", "type": "政协", "level": "县处级",
     "parent": "政协阿克苏地区工委", "location": "新疆阿克苏地区乌什县"},
]

positions = [
    {"pid": 1, "oid": 1, "title": "中共乌什县委书记", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},
    {"pid": 2, "oid": 2, "title": "乌什县委副书记、县长", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},
    {"pid": 3, "oid": 1, "title": "前任乌什县委书记", "start": "", "end": "",
     "rank": "县处级正职", "note": ""},
    {"pid": 4, "oid": 1, "title": "乌什县委常委、政法委书记", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"pid": 5, "oid": 1, "title": "乌什县委常委、组织部部长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
]

relationships = [
    {"a": 1, "b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政搭档",
     "overlap_org": "乌什县", "overlap_period": "current"},
    {"a": 3, "b": 1, "type": "predecessor_successor",
     "context": "颜画前任，吴新疆接任",
     "overlap_org": "中共乌什县委", "overlap_period": ""},
]


def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def color(p):
    if p["id"]==1: return "255,50,50"
    if p["id"]==2: return "50,100,255"
    if "纪委" in p.get("current_post",""): return "255,165,0"
    return "100,100,100"

def oc(typ):
    m={"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200"}
    return m.get(typ,"200,200,200")

def create_db():
    if os.path.exists(DB_PATH): os.remove(DB_PATH)
    conn=sqlite3.connect(DB_PATH); cur=conn.cursor()
    cur.executescript("""CREATE TABLE persons(id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE organizations(id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE positions(id INTEGER PRIMARY KEY AUTOINCREMENT,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,end TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id)REFERENCES persons(id),FOREIGN KEY(org_id)REFERENCES organizations(id));
CREATE TABLE relationships(id INTEGER PRIMARY KEY AUTOINCREMENT,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a)REFERENCES persons(id),FOREIGN KEY(person_b)REFERENCES persons(id));
""")
    for p in persons:
        cur.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for po in positions:
        cur.execute("INSERT INTO positions(person_id,org_id,title,start,end,rank,note)VALUES(?,?,?,?,?,?,?)",
                    (po["pid"],po["oid"],po["title"],po["start"],po["end"],po["rank"],po["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period)VALUES(?,?,?,?,?,?)",
                    (r["a"],r["b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    conn.commit(); conn.close()
    print(f"  [OK] DB: {DB_PATH}")

def create_gexf():
    lines=["""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">
  <meta lastmodifieddate=\""""+datetime.now().strftime("%Y-%m-%d")+"""">
    <creator>gov-relation Agent</creator>
    <description>乌什县领导班子工作关系网络</description>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="0" title="type" type="string"/>
      <attribute id="1" title="post" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="0" title="type" type="string"/>
      <attribute id="1" title="context" type="string"/>
    </attributes>
    <nodes>"""]
    for p in persons:
        c=color(p); sz="20.0" if p["id"] in(1,2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c=oc(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues><attvalue for="0" value="organization"/><attvalue for="1" value=""/></attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid=0
    for po in positions:
        eid+=1
        lines.append(f'      <edge id="e{eid}" source="p{po["pid"]}" target="o{po["oid"]}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues><attvalue for="0" value="worked_at"/><attvalue for="1" value=""/></attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid+=1
        lines.append(f'      <edge id="e{eid}" source="p{r["a"]}" target="p{r["b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues><attvalue for="0" value="relationship"/><attvalue for="1" value=""/></attvalues>')
        lines.append('      </edge>')
    lines.append("""    </edges>
  </graph>
</gexf>""")
    with open(GEXF_PATH,"w",encoding="utf-8") as f: f.write("\n".join(lines))
    print(f"  [OK] GEXF: {GEXF_PATH}")

if __name__=="__main__":
    print("乌什县 —— 领导班子工作关系网络"); print("="*40)
    create_db(); create_gexf()
    print(f"\n摘要: 人员={sum(1 for p in persons if p['name'])}, 机构={len(organizations)}, 任职={len(positions)}, 关系={len(relationships)}")