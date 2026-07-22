#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 台江区 (Taijiang District), 福州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Sources:
- Taijiang District Government official website (taijiang.gov.cn) — news and leadership mentions
- Fuzhou Municipal Government official website (fuzhou.gov.cn) — city leadership page
- Media reports (CCTV, thepaper.cn)

Current as of: July 2026

⚠️ NOTE: The current 区委书记 (party secretary) name could not be confirmed
from open web sources. 梁栋 (former party secretary) was promoted to Fuzhou 副市长.
The successor's identity requires on-site verification of the government leadership page.
Marked with confidence="unverified" placeholder.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "台江区_network.db")
GEXF_PATH = os.path.join(BASE, "台江区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════
    # NOTE: 区委书记 — Current position holder could not be confirmed from
    # available open sources. Previous holder 梁栋 promoted to Fuzhou副市长.
    # The current secretary (name unknown) assumed office after 梁栋's promotion
    # (likely late 2024 or early 2025).
    {"id":1,"name":"（区委书记待确认）","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"台江区委书记","current_org":"中共福州市台江区委员会",
     "source":"待补充——需查阅taijiang.gov.cn领导之窗页面"},

    # 林发希 — 台江区委副书记、代区长 (confirmed from news articles)
    {"id":2,"name":"林发希","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"台江区委副书记、代区长","current_org":"福州市台江区人民政府",
     "source":"https://www.taijiang.gov.cn/xjwz/zwgk/gzdt/tjdt/202607/t20260709_5344541.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Standing committee members / district leaders mentioned in news
    # ═════════════════════════════════════════════════════════════════════

    # 华智敏 — 区领导 (mentioned in typhoon defense article, July 2026)
    {"id":3,"name":"华智敏","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"台江区领导","current_org":"中共福州市台江区委员会",
     "source":"https://www.taijiang.gov.cn/xjwz/zwgk/gzdt/tjdt/202607/t20260709_5344541.htm"},

    # 林辉 — 区领导 (mentioned in typhoon defense article, July 2026)
    {"id":4,"name":"林辉","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"台江区领导","current_org":"中共福州市台江区委员会",
     "source":"https://www.taijiang.gov.cn/xjwz/zwgk/gzdt/tjdt/202607/t20260709_5344541.htm"},

    # 余永俤 — 区人大常委会党组书记、主任 (confirmed from people's congress article)
    {"id":5,"name":"余永俤","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"台江区人大常委会党组书记、主任","current_org":"福州市台江区人民代表大会常务委员会",
     "source":"https://www.taijiang.gov.cn/xjwz/zwgk/gzdt/tjdt/202607/t20260715_5347061.htm"},

    # 郭美月 — 区人大常委会党组成员、副主任
    {"id":6,"name":"郭美月","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"台江区人大常委会党组成员、副主任","current_org":"福州市台江区人民代表大会常务委员会",
     "source":"https://www.taijiang.gov.cn/xjwz/zwgk/gzdt/tjdt/202607/t20260715_5347061.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═════════════════════════════════════════════════════════════════════

    # 梁栋 — 前任台江区委书记，现任福州市副市长
    {"id":7,"name":"梁栋","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市副市长（原台江区委书记）","current_org":"福州市人民政府",
     "source":"https://www.fuzhou.gov.cn/zwgk/ldzc/"},

    # 李凡 — 前前任台江区长/书记，后受处分
    {"id":8,"name":"李凡","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（曾任台江区区长、区委书记，2023年受处分）","current_org":"",
     "source":"https://search.cctv.com/search.php?qtext=%E6%9D%8E%E5%87%A1+%E5%8F%B0%E6%B1%9F%E5%8C%BA"},

    # 梁建勇 — 曾任台江区委副书记、区长、区委书记，后升任福建省副省长
    {"id":9,"name":"梁建勇","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（曾任台江区委书记，后任福建省副省长）","current_org":"",
     "source":"https://search.cctv.com/search.php?qtext=%E6%A2%81%E5%BB%BA%E5%8B%87+%E5%8F%B0%E6%B1%9F%E5%8C%BA"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福州市台江区委员会","type":"党委","level":"县处级","parent":"中共福州市委员会","location":"福州市台江区"},
    {"id":2,"name":"福州市台江区人民政府","type":"政府","level":"县处级","parent":"福州市人民政府","location":"福州市台江区"},
    {"id":3,"name":"福州市台江区人民代表大会常务委员会","type":"人大","level":"县处级","parent":"福州市人民代表大会常务委员会","location":"福州市台江区"},
    {"id":4,"name":"福州市人民政府","type":"政府","level":"地市级","parent":"福建省人民政府","location":"福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 区委书记（待确认）
    {"id":1,"person_id":1,"org_id":1,"title":"台江区委书记","start":"","end":"至今","rank":"正处级","note":"前任梁栋升任福州市副市长后接任，具体姓名待确认"},

    # 林发希 — 代区长
    {"id":2,"person_id":2,"org_id":2,"title":"台江区委副书记、代区长","start":"2026","end":"至今","rank":"正处级","note":"2026年任代区长，此前任职待查"},
    {"id":3,"person_id":2,"org_id":1,"title":"台江区委副书记","start":"2026","end":"至今","rank":"正处级","note":""},

    # 华智敏
    {"id":4,"person_id":3,"org_id":1,"title":"台江区领导","start":"","end":"至今","rank":"","note":""},

    # 林辉
    {"id":5,"person_id":4,"org_id":1,"title":"台江区领导","start":"","end":"至今","rank":"","note":""},

    # 余永俤 — 人大常委会主任
    {"id":6,"person_id":5,"org_id":3,"title":"台江区人大常委会党组书记、主任","start":"","end":"至今","rank":"正处级","note":""},

    # 郭美月 — 人大常委会副主任
    {"id":7,"person_id":6,"org_id":3,"title":"台江区人大常委会党组成员、副主任","start":"","end":"至今","rank":"副处级","note":""},

    # 梁栋 — 前区委书记
    {"id":8,"person_id":7,"org_id":1,"title":"台江区委书记","start":"2021","end":"2024","rank":"正处级","note":"后升任福州市副市长"},
    {"id":9,"person_id":7,"org_id":4,"title":"福州市副市长","start":"2024","end":"至今","rank":"副厅级","note":"原台江区委书记升任"},

    # 李凡 — 前台江区区长/书记
    {"id":10,"person_id":8,"org_id":2,"title":"台江区区长","start":"","end":"","rank":"正处级","note":"后任区委书记"},
    {"id":11,"person_id":8,"org_id":1,"title":"台江区委书记","start":"","end":"","rank":"正处级","note":"2023年因违反中央八项规定受处分"},

    # 梁建勇 — 前书记
    {"id":12,"person_id":9,"org_id":2,"title":"台江区委副书记、区长","start":"","end":"","rank":"正处级","note":""},
    {"id":13,"person_id":9,"org_id":1,"title":"台江区委书记","start":"","end":"","rank":"正处级","note":"后升任福建省副省长"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 林发希 vs （待确认书记）— 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"待确认的区委书记与代区长林发希在台江区共事",
     "overlap_org":"福州市台江区","overlap_period":"2026年至今"},

    # 梁栋 → 接任书记 — 前后任
    {"id":2,"person_a":7,"person_b":1,"type":"前后任",
     "context":"梁栋（前任书记，升副市长）→ 接任者（姓名待确认）",
     "overlap_org":"中共福州市台江区委员会","overlap_period":"不重叠（前后任）"},

    # 梁栋 — 林发希 — 可能的前后任党政搭档
    {"id":3,"person_a":7,"person_b":2,"type":"前后任",
     "context":"梁栋（原书记）与林发希（代区长）——梁栋任书记期间林发希可能尚未到任",
     "overlap_org":"福州市台江区","overlap_period":"不确定"},

    # 李凡 — 梁栋 — 前后任书记
    {"id":4,"person_a":8,"person_b":7,"type":"前后任",
     "context":"李凡（前书记，受处分）→ 梁栋接任",
     "overlap_org":"中共福州市台江区委员会","overlap_period":"不重叠（前后任）"},

    # 梁建勇 — 李凡 — 前后任书记
    {"id":5,"person_a":9,"person_b":8,"type":"前后任",
     "context":"梁建勇（前书记，升副省长）→ 李凡接任",
     "overlap_org":"中共福州市台江区委员会","overlap_period":"不重叠（前后任）"},

    # 余永俤 — 林发希 — 人大-政府关系
    {"id":6,"person_a":5,"person_b":2,"type":"党政军人大",
     "context":"人大主任余永俤与代区长林发希在台江区共事",
     "overlap_org":"福州市台江区","overlap_period":"2026年至今"},
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
    if "区长" in post or "代区长" in post:
        return "50,100,230"  # blue for gov leaders
    if "人大" in post:
        return "180,200,255"
    if "副市长" in post:
        return "80,100,200"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255",
            "纪委":"255,220,180"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>福州市台江区（市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["区委书记","区长","代区长"]) else "12.0"
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
print("  1. VERIFY current party secretary name against taijiang.gov.cn leadership page")
print("  2. Fill in biographical details (birth dates, education) for all officials")
print("  3. Identify additional standing committee members (organization dept, discipline, propaganda, united front)")
print("  4. Add deputy district mayors and their portfolios")
print("  5. Confirm 林发希's transition from acting to full district mayor")
