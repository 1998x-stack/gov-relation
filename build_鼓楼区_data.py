#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 鼓楼区 (Gulou District), 福州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Sources:
- Gulou District Government official website (gl.gov.cn) — news and leadership mentions
- CCTV/CNR news reports (search.cctv.com) — current leaders and activities
- Fujian Daily / Fuzhou Daily media reports

Current as of: July 2026
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "鼓楼区_network.db")
GEXF_PATH = os.path.join(BASE, "鼓楼区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 刘用全 — 鼓楼区委书记 (assumed office around April-May 2025)
    {"id":1,"name":"刘用全","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鼓楼区委书记","current_org":"中共福州市鼓楼区委员会",
     "source":"https://search.cctv.com/search.php?qtext=%E5%88%98%E7%94%A8%E5%85%A8+%E9%BC%93%E6%A5%BC%E5%8C%BA"},

    # 杨辉 — 鼓楼区委副书记、区长
    {"id":2,"name":"杨辉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鼓楼区委副书记、区长","current_org":"福州市鼓楼区人民政府",
     "source":"https://search.cctv.com/search.php?qtext=%E6%9D%A8%E8%BE%89+%E9%BC%93%E6%A5%BC%E5%8C%BA+%E5%8C%BA%E9%95%BF"},

    # ── Standing committee members ──
    # 高春 — 区委常委、常务副区长
    {"id":3,"name":"高春","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鼓楼区委常委、常务副区长","current_org":"福州市鼓楼区人民政府",
     "source":"https://search.cctv.com/search.php?qtext=%E9%AB%98%E6%98%A5+%E9%BC%93%E6%A5%BC%E5%8C%BA"},

    # 张玉佩 — 副区长、三级调研员
    {"id":4,"name":"张玉佩","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鼓楼区政府副区长、三级调研员","current_org":"福州市鼓楼区人民政府",
     "source":"https://search.cctv.com/search.php?qtext=%E5%BC%A0%E7%8E%89%E4%BD%A9+%E9%BC%93%E6%A5%BC%E5%8C%BA"},

    # 翁晖 — 副区长
    {"id":5,"name":"翁晖","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鼓楼区政府副区长","current_org":"福州市鼓楼区人民政府",
     "source":"https://search.cctv.com/search.php?qtext=%E7%BF%81%E6%99%96+%E9%BC%93%E6%A5%BC%E5%8C%BA"},

    # 林能响 — 副区长、福州市公安局鼓楼分局局长
    {"id":6,"name":"林能响","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鼓楼区副区长、福州市公安局鼓楼分局局长","current_org":"福州市公安局鼓楼分局",
     "source":"https://search.cctv.com/search.php?qtext=%E6%9E%97%E8%83%BD%E5%93%8D+%E9%BC%93%E6%A5%BC%E5%8C%BA"},

    # ── Predecessors ──
    # 黄建新 — 前任鼓楼区委书记（2021-2025），福州市人大常委会副主任
    {"id":7,"name":"黄建新","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市人大常委会副主任（原鼓楼区委书记）","current_org":"福州市人民代表大会常务委员会",
     "source":"https://search.cctv.com/search.php?qtext=%E9%BB%84%E5%BB%BA%E6%96%B0+%E9%BC%93%E6%A5%BC%E5%8C%BA+%E5%8C%BA%E5%A7%94%E4%B9%A6%E8%AE%B0"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福州市鼓楼区委员会","type":"党委","level":"县处级","parent":"中共福州市委员会","location":"福州市鼓楼区"},
    {"id":2,"name":"福州市鼓楼区人民政府","type":"政府","level":"县处级","parent":"福州市人民政府","location":"福州市鼓楼区"},
    {"id":3,"name":"福州市公安局鼓楼分局","type":"政府","level":"县处级","parent":"福州市公安局","location":"福州市鼓楼区"},
    {"id":4,"name":"福州市人民代表大会常务委员会","type":"人大","level":"地级市","parent":"福建省人民代表大会常务委员会","location":"福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 刘用全 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"鼓楼区委书记","start":"2025-04","end":"至今","rank":"正处级","note":"接替黄建新，约2025年4-5月到任"},
    # 杨辉 — 区长
    {"id":2,"person_id":2,"org_id":2,"title":"鼓楼区委副书记、区长","start":"2021-05","end":"至今","rank":"正处级","note":"2021年任区长，此前为区委副书记"},
    # 高春 — 常务副区长
    {"id":3,"person_id":3,"org_id":2,"title":"鼓楼区委常委、常务副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 张玉佩 — 副区长
    {"id":4,"person_id":4,"org_id":2,"title":"鼓楼区政府副区长、三级调研员","start":"","end":"至今","rank":"副处级","note":""},
    # 翁晖 — 副区长
    {"id":5,"person_id":5,"org_id":2,"title":"鼓楼区政府副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 林能响 — 副区长兼公安分局局长
    {"id":6,"person_id":6,"org_id":3,"title":"鼓楼区副区长、福州市公安局鼓楼分局局长","start":"","end":"至今","rank":"副处级","note":""},
    {"id":7,"person_id":6,"org_id":2,"title":"鼓楼区副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 黄建新 — 前任区委书记
    {"id":8,"person_id":7,"org_id":1,"title":"鼓楼区委书记","start":"2021","end":"2025-04","rank":"正处级","note":"同时任福州市人大常委会副主任（副厅级）；后由刘用全接任"},
    {"id":9,"person_id":7,"org_id":4,"title":"福州市人大常委会副主任","start":"2022","end":"至今","rank":"副厅级","note":"兼任鼓楼区委书记至2025年"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 刘用全 vs 杨辉 (current party-gov duo)
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"刘用全（区委书记）与杨辉（区长）在鼓楼区共事",
     "overlap_org":"福州市鼓楼区","overlap_period":"2025年至今"},

    # ── Party Secretary succession
    {"id":2,"person_a":7,"person_b":1,"type":"前后任",
     "context":"黄建新（2021-2025书记）→ 刘用全（2025接任）",
     "overlap_org":"中共福州市鼓楼区委员会","overlap_period":"不重叠（前后任）"},

    # ── 杨辉 vs 黄建新 — former party-gov duo
    {"id":3,"person_a":2,"person_b":7,"type":"党政搭档",
     "context":"杨辉（区长）与黄建新（书记）曾在鼓楼区共事（2021-2025）",
     "overlap_org":"福州市鼓楼区","overlap_period":"2021-2025"},

    # ── 高春（常务副区长）- 杨辉（区长）— 政府班子搭档
    {"id":4,"person_a":2,"person_b":3,"type":"上下级",
     "context":"杨辉（区长）与高春（常务副区长）在鼓楼区政府共事",
     "overlap_org":"福州市鼓楼区人民政府","overlap_period":"至今"},

    # ── 张玉佩 - 杨辉 — 政府班子搭档
    {"id":5,"person_a":2,"person_b":4,"type":"上下级",
     "context":"杨辉（区长）与张玉佩（副区长）在鼓楼区政府共事",
     "overlap_org":"福州市鼓楼区人民政府","overlap_period":"至今"},

    # ── 翁晖 - 杨辉 — 政府班子搭档
    {"id":6,"person_a":2,"person_b":5,"type":"上下级",
     "context":"杨辉（区长）与翁晖（副区长）在鼓楼区政府共事",
     "overlap_org":"福州市鼓楼区人民政府","overlap_period":"至今"},

    # ── 林能响 - 杨辉 — 政府班子搭档
    {"id":7,"person_a":2,"person_b":6,"type":"上下级",
     "context":"杨辉（区长）与林能响（副区长）在鼓楼区政府共事",
     "overlap_org":"福州市鼓楼区人民政府","overlap_period":"至今"},
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
    if "区委书记" in post:
        return "230,50,50"  # red for top party secretary
    if "区长" in post:
        return "50,100,230"  # blue for gov leaders
    if "常务副区长" in post:
        return "80,140,230"
    if "副区长" in post:
        return "100,160,230"
    if "人大" in post:
        return "180,200,255"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255",
            "纪委":"255,220,180"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>福州市鼓楼区（市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    c = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["区委书记","区长"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
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
print("\n⚠️ NOTE: This data requires verification. Key items:")
print("  1. Verify current party secretary and mayor against latest gl.gov.cn leadership page")
print("  2. Fill in biographical details (birth dates, education) for all officials")
print("  3. Identify additional standing committee members (organization dept, discipline, propaganda, united front)")
