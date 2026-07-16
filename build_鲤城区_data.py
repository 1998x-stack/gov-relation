#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 鲤城区 (Licheng District), 泉州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Task: fujian_鲤城区 — 区委书记 & 区长
Province: 福建省
Parent city: 泉州市 (prefecture-level)
Region: 鲤城区
Level: 市辖区
Research date: 2026-07-16

Confirmed officeholders (as of 2026-07-16):
- 区委书记: 李垂举 (born ?) — confirmed from qzlc.gov.cn news (July 14-15, 2026)
- 区委副书记、区政府党组书记: 林祖传 (born 1976.06, male, Han) — confirmed from qzlc.gov.cn leadership page

Deputy district leaders (confirmed from official leadership page):
- 副区长: 张剑辉, 余经伟, 王伟, 李超端, 高结山, 卓鸿杰, 沈伟鹏

Sources:
- quanzhou Licheng District Government official website (www.qzlc.gov.cn) — leadership page and news
- qzlc.gov.cn news articles (July 2026): confirmed 区委书记李垂举, 区政府党组书记林祖传

Confidence: Current leadership identity-level confirmed from official government sources.
Full career timelines require additional research. Deputy mayor portfolios partially confirmed.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "鲤城区_network.db")
GEXF_PATH = os.path.join(BASE, "鲤城区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──

    # 李垂举 — 鲤城区委书记 (confirmed from qzlc.gov.cn news, July 2026)
    {"id":1,"name":"李垂举","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区委书记","current_org":"中共泉州市鲤城区委员会",
     "source":"https://www.qzlc.gov.cn/xxgk/gzdt/lcxw/202607/t20260716_3309605.htm"},

    # 林祖传 — 鲤城区委副书记、区政府党组书记（区长）
    {"id":2,"name":"林祖传","gender":"男","ethnicity":"汉族",
     "birth":"1976年6月","birthplace":"",
     "education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区委副书记、区政府党组书记","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/qzfld/lzc/"},

    # ── Deputy district mayors (from official leadership page) ──

    # 张剑辉 — 副区长
    {"id":3,"name":"张剑辉","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区副区长","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/fqz/zjh/"},

    # 余经伟 — 副区长
    {"id":4,"name":"余经伟","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区副区长","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/fqz/yjw/"},

    # 王伟 — 副区长
    {"id":5,"name":"王伟","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区副区长","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/fqz/ww/"},

    # 李超端 — 副区长
    {"id":6,"name":"李超端","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区副区长","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/fqz/lcd/"},

    # 高结山 — 副区长
    {"id":7,"name":"高结山","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区副区长","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/fqz/gjs/"},

    # 卓鸿杰 — 副区长
    {"id":8,"name":"卓鸿杰","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区副区长","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/fqz/zhj/"},

    # 沈伟鹏 — 副区长
    {"id":9,"name":"沈伟鹏","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"鲤城区副区长","current_org":"泉州市鲤城区人民政府",
     "source":"https://www.qzlc.gov.cn/ldzc/qzfld/fqz/swp/"},

    # ── Predecessors ──

    # 王克思 — 前任鲤城区长/书记（据公开信息）
    {"id":10,"name":"王克思","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（曾任鲤城区区长、区委书记）","current_org":"",
     "source":"https://search.cctv.com/search.php?qtext=%E7%8E%8B%E5%85%8B%E6%80%9D+%E9%B2%A4%E5%9F%8E"},

    # 黄阳春 — 曾任鲤城区委书记
    {"id":11,"name":"黄阳春","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（曾任鲤城区委书记）","current_org":"",
     "source":"https://search.cctv.com/search.php?qtext=%E9%BB%84%E9%98%B3%E6%98%A5+%E9%B2%A4%E5%9F%8E"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共泉州市鲤城区委员会","type":"党委","level":"县处级","parent":"中共泉州市委员会","location":"泉州市鲤城区"},
    {"id":2,"name":"泉州市鲤城区人民政府","type":"政府","level":"县处级","parent":"泉州市人民政府","location":"泉州市鲤城区"},
    {"id":3,"name":"中共泉州市委员会","type":"党委","level":"地市级","parent":"中共福建省委员会","location":"泉州市"},
    {"id":4,"name":"泉州市人民政府","type":"政府","level":"地市级","parent":"福建省人民政府","location":"泉州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 李垂举 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"鲤城区委书记","start":"","end":"至今","rank":"正处级","note":"2026年7月即在任，确切到任时间待查"},

    # 林祖传 — 区委副书记、区政府党组书记
    {"id":2,"person_id":2,"org_id":1,"title":"鲤城区委副书记","start":"","end":"至今","rank":"正处级","note":""},
    {"id":3,"person_id":2,"org_id":2,"title":"区政府党组书记","start":"","end":"至今","rank":"正处级","note":"1976年6月出生，大学学历"},

    # 张剑辉 — 副区长
    {"id":4,"person_id":3,"org_id":2,"title":"鲤城区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 余经伟 — 副区长
    {"id":5,"person_id":4,"org_id":2,"title":"鲤城区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 王伟 — 副区长
    {"id":6,"person_id":5,"org_id":2,"title":"鲤城区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 李超端 — 副区长
    {"id":7,"person_id":6,"org_id":2,"title":"鲤城区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 高结山 — 副区长
    {"id":8,"person_id":7,"org_id":2,"title":"鲤城区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 卓鸿杰 — 副区长
    {"id":9,"person_id":8,"org_id":2,"title":"鲤城区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 沈伟鹏 — 副区长
    {"id":10,"person_id":9,"org_id":2,"title":"鲤城区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 王克思 — 前任书记/区长
    {"id":11,"person_id":10,"org_id":1,"title":"鲤城区委书记","start":"","end":"","rank":"正处级","note":"前任书记"},
    {"id":12,"person_id":10,"org_id":2,"title":"鲤城区区长","start":"","end":"","rank":"正处级","note":"曾任区长后任书记"},

    # 黄阳春 — 前任书记
    {"id":13,"person_id":11,"org_id":1,"title":"鲤城区委书记","start":"","end":"","rank":"正处级","note":"前任书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 李垂举 — 林祖传 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"李垂举（区委书记）与林祖传（区委副书记、区政府党组书记/区长）在鲤城区共事",
     "overlap_org":"泉州市鲤城区","overlap_period":"2026年至今（待确认）"},

    # 李垂举 — 王克思 — 前后任书记
    {"id":2,"person_a":10,"person_b":1,"type":"前后任",
     "context":"王克思（前任书记）→ 李垂举接任",
     "overlap_org":"中共泉州市鲤城区委员会","overlap_period":"不重叠（前后任）"},

    # 王克思 — 黄阳春 — 前后任书记
    {"id":3,"person_a":11,"person_b":10,"type":"前后任",
     "context":"黄阳春（前前任书记）→ 王克思接任",
     "overlap_org":"中共泉州市鲤城区委员会","overlap_period":"不重叠（前后任）"},

    # 林祖传 — 副区长们 — 正副级关系
    {"id":4,"person_a":2,"person_b":3,"type":"正副级关系",
     "context":"区政府党组书记林祖传与副区长张剑辉在鲤城区政府共事",
     "overlap_org":"泉州市鲤城区人民政府","overlap_period":"2026年至今"},
    {"id":5,"person_a":2,"person_b":4,"type":"正副级关系",
     "context":"区政府党组书记林祖传与副区长余经伟在鲤城区政府共事",
     "overlap_org":"泉州市鲤城区人民政府","overlap_period":"2026年至今"},
    {"id":6,"person_a":2,"person_b":5,"type":"正副级关系",
     "context":"区政府党组书记林祖传与副区长王伟在鲤城区政府共事",
     "overlap_org":"泉州市鲤城区人民政府","overlap_period":"2026年至今"},
    {"id":7,"person_a":2,"person_b":6,"type":"正副级关系",
     "context":"区政府党组书记林祖传与副区长李超端在鲤城区政府共事",
     "overlap_org":"泉州市鲤城区人民政府","overlap_period":"2026年至今"},
    {"id":8,"person_a":2,"person_b":7,"type":"正副级关系",
     "context":"区政府党组书记林祖传与副区长高结山在鲤城区政府共事",
     "overlap_org":"泉州市鲤城区人民政府","overlap_period":"2026年至今"},
    {"id":9,"person_a":2,"person_b":8,"type":"正副级关系",
     "context":"区政府党组书记林祖传与副区长卓鸿杰在鲤城区政府共事",
     "overlap_org":"泉州市鲤城区人民政府","overlap_period":"2026年至今"},
    {"id":10,"person_a":2,"person_b":9,"type":"正副级关系",
     "context":"区政府党组书记林祖传与副区长沈伟鹏在鲤城区政府共事",
     "overlap_org":"泉州市鲤城区人民政府","overlap_period":"2026年至今"},
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
    if "区委书记" in post or "书记" in post:
        return "230,50,50"  # red for party secretary
    if "区长" in post or "政府党组书记" in post:
        return "50,100,230"  # blue for gov leaders
    if "副区长" in post:
        return "80,130,230"  # lighter blue for deputies
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
lines.append('    <description>泉州市鲤城区（市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["区委书记","政府党组书记","副书记"]) else "12.0"
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
print("  1. Confirm 李垂举's full name correctness and prior roles")
print("  2. Fill in biographical details (birth dates, education) for all officials")
print("  3. Identify standing committee members (organization dept, discipline, propaganda, united front)")
print("  4. Confirm district mayor title (林祖传 listed as 区政府党组书记, may also be 代区长 or 区长)")
print("  5. Verify predecessor chain (王克思, 黄阳春) exact dates")
