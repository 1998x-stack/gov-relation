#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 晋安区 (Jin'an District), 福州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Sources:
- Jin'an District Government official website (fzja.gov.cn) — news and leadership mentions
- Fuzhou Daily / mainstream media reports
- Official government meeting/news pages

Current as of: July 2026

Key findings:
- 区委书记: 林涛 (also 福州市人大常委会副主任)
- 区长: 夏星 (left around May-June 2026, last seen May 28, 2026)
- 代区长: 吴思斌 (confirmed from July 15, 2026 news article)
- 夏星 succeeded his predecessor as 代区长 around late 2025

Note: Birth dates, education, and full career timelines for most officials
require on-site verification of the government leadership page.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "晋安区_network.db")
GEXF_PATH = os.path.join(BASE, "晋安区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 林涛 — 晋安区委书记、福州市人大常委会副主任 (confirmed from district news, April 2026)
    {"id":1,"name":"林涛","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市人大常委会副主任、晋安区委书记","current_org":"中共福州市晋安区委员会",
     "source":"https://www.fzja.gov.cn/xjwz/zwgk/zfhy/qtthy/202605/t20260506_5317500.htm"},

    # 夏星 — 原晋安区委副书记、区长 (last appeared May 28, 2026, left between May-Jun 2026)
    {"id":2,"name":"夏星","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原晋安区委副书记、区长（2026年5-6月离任）","current_org":"福州市晋安区人民政府",
     "source":"https://www.fzja.gov.cn/xjwz/zwgk/zfhy/cwhy/202606/t20260612_5333243.htm"},

    # 吴思斌 — 晋安区委副书记、代区长 (confirmed from July 2026 news)
    {"id":3,"name":"吴思斌","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"晋安区委副书记、代区长","current_org":"福州市晋安区人民政府",
     "source":"https://www.fzja.gov.cn/xjwz/zwgk/gzdt/jadt/202607/t20260715_5346988.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═════════════════════════════════════════════════════════════════════

    # 前任区委书记 — name not confirmed from available sources
    # 夏星的前任 (晋安区原区长，夏星2025年底以代区长身份接任)
    # 前任区长姓名 — not confirmed from available sources
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福州市晋安区委员会","type":"党委","level":"县处级","parent":"中共福州市委员会","location":"福州市晋安区"},
    {"id":2,"name":"福州市晋安区人民政府","type":"政府","level":"县处级","parent":"福州市人民政府","location":"福州市晋安区"},
    {"id":3,"name":"福州市人民代表大会常务委员会","type":"人大","level":"副厅级","parent":"福建省人民代表大会常务委员会","location":"福州市"},
    {"id":4,"name":"福兴经济开发区管委会","type":"开发区","level":"省级","parent":"福州市人民政府","location":"福州市晋安区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 林涛 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"晋安区委书记","start":"","end":"至今","rank":"县处级(兼副厅级)","note":"同时担任福州市人大常委会副主任"},
    {"id":2,"person_id":1,"org_id":3,"title":"福州市人大常委会副主任","start":"","end":"至今","rank":"副厅级","note":"兼任"},
    # 夏星 — 原区长
    {"id":3,"person_id":2,"org_id":2,"title":"晋安区委副书记、区长","start":"约2025-12","end":"2026-05","rank":"县处级","note":"2025年12月以代区长身份作政府工作报告；2026年5月后离任"},
    # 吴思斌 — 代区长
    {"id":4,"person_id":3,"org_id":2,"title":"晋安区委副书记、代区长","start":"2026-07","end":"至今","rank":"县处级","note":"2026年7月15日首次以代区长身份公开报道"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 林涛 vs 夏星 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"林涛（区委书记）与夏星（区长）在晋安区共事",
     "overlap_org":"晋安区","overlap_period":"约2025-12至2026-05"},

    # 林涛 vs 吴思斌 — 新任党政搭档
    {"id":2,"person_a":1,"person_b":3,"type":"党政搭档",
     "context":"林涛（区委书记）与吴思斌（代区长）在晋安区共事",
     "overlap_org":"晋安区","overlap_period":"2026-07至今"},

    # 夏星 → 吴思斌 — 前后任（区长）
    {"id":3,"person_a":2,"person_b":3,"type":"前后任",
     "context":"夏星（前任区长）→ 吴思斌（现任代区长）",
     "overlap_org":"福州市晋安区人民政府","overlap_period":"不重叠（前后任）"},
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
    if "书记" in post and "区委" in post:
        return "230,50,50"  # red for party secretary
    if "区长" in post:
        return "50,100,230"  # blue for district mayor
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    if "人大" in post:
        return "200,230,255"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255","开发区":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>晋安区（福州市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    is_top = any(k in p.get("current_post","") for k in ["区委书记","区长","代区长"])
    sz = "20.0" if is_top else "12.0"
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
print("  1. Verify 林涛's full name and birth/education details")
print("  2. Verify 吴思斌's full name and birth/education details")
print("  3. Find predecessor of 林涛 (previous party secretary)")
print("  4. Find predecessor of 夏星 (previous district mayor)")
print("  5. Complete career timelines for all officials")
print("  6. Add standing committee members (区纪委、组织部、宣传部、政法委等)")
