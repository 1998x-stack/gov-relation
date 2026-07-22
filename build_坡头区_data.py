#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 坡头区 (Potou District), 湛江市, 广东省.

Covers: district-level leaders (区委书记, 区长), key standing committee members,
predecessor chain, and organizational relationships.

Sources:
- 坡头区人民政府 official site: www.zjpotou.gov.cn (unreachable during build)
- 湛江市人民政府: www.zhanjiang.gov.cn
- Baidu Baike / web search (all sources unreachable due to access restrictions)

Current as of: July 2026

IMPORTANT: This build was conducted under severe web access degradation
(Exa rate-limited, Baidu 403, government site timed out, search engines blocked).
All data is based on pre-training knowledge and should be verified against
official sources. See open_questions in person JSON files for gaps.

Key findings:
- 区委书记: 不详 (Unable to confirm current区委书记 due to web access failure)
- 区长: 不详 (Unable to confirm current 区长 due to web access failure)

Note: The 坡头区 government website (www.zjpotou.gov.cn) was completely unreachable
from this environment. All search engines (Google, Bing, Baidu, DuckDuckGo) were
blocked or timed out. Exa search API was rate-limited. Jina Reader was unavailable.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "坡头区_network.db")
GEXF_PATH = os.path.join(BASE, "坡头区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# ⚠️ ALL PERSONS LISTED BELOW ARE BASED ON PRE-TRAINING KNOWLEDGE AND REQUIRE
# VERIFICATION AGAINST OFFICIAL SOURCES. WEB ACCESS WAS UNAVAILABLE DURING BUILD.
# =========================================================================

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 区委书记 — Could not confirm current officeholder
    # Based on historical knowledge, the区委书记 of坡头区 in recent years
    # has typically been a member of the 湛江市委 standing committee.
    # Earlier known区委书记 include 陈政 (served ~2016-2020) and 谢伍 (served ~2020-2023).
    # The current officeholder as of 2026 could not be confirmed.

    # 区长 — Similarly could not confirm current officeholder.
    # Known previous 区长 include 陈景泰 (served ~2016-2021) and 黄哲辉 (appointed ~2021).

    # Due to complete web access failure, we create entries for known recent leaders
    # with explicit caveats about currency.

    # 谢伍 — 坡头区委原书记 (served ~2020-2023 period)
    {"id":1,"name":"谢伍","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原坡头区委书记（2020-2023前后在任）","current_org":"中共湛江市坡头区委员会",
     "source":"Historical knowledge — requires verification"},

    # 黄哲辉 — 坡头区委副书记、原区长 (appointed ~2021)
    {"id":2,"name":"黄哲辉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"坡头区委副书记、原区长（2021前后任职）","current_org":"湛江市坡头区人民政府",
     "source":"Historical knowledge — requires verification"},

    # ═════════════════════════════════════════════════════════════════════
    # Key officials (from historical context)
    # ═════════════════════════════════════════════════════════════════════

    # 陈政 — 坡头区委原书记 (served ~2016-2020)
    {"id":3,"name":"陈政","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原坡头区委书记（2016-2020前后在任）","current_org":"中共湛江市坡头区委员会",
     "source":"Historical knowledge — requires verification"},

    # 陈景泰 — 坡头区委原副书记、原区长 (served ~2016-2021)
    {"id":4,"name":"陈景泰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原坡头区委副书记、区长（2016-2021前后在任）","current_org":"湛江市坡头区人民政府",
     "source":"Historical knowledge — requires verification"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共湛江市坡头区委员会","type":"党委","level":"县处级","parent":"中共湛江市委员会","location":"湛江市坡头区"},
    {"id":2,"name":"湛江市坡头区人民政府","type":"政府","level":"县处级","parent":"湛江市人民政府","location":"湛江市坡头区"},
    {"id":3,"name":"湛江市坡头区人民代表大会常务委员会","type":"人大","level":"县处级","parent":"湛江市人民代表大会常务委员会","location":"湛江市坡头区"},
    {"id":4,"name":"中国人民政治协商会议湛江市坡头区委员会","type":"政协","level":"县处级","parent":"中国人民政治协商会议湛江市委员会","location":"湛江市坡头区"},
    {"id":5,"name":"中共湛江市坡头区纪律检查委员会","type":"党委","level":"县处级","parent":"中共湛江市纪律检查委员会","location":"湛江市坡头区"},
    {"id":6,"name":"湛江高新技术产业开发区（坡头区合署）","type":"开发区","level":"省级","parent":"湛江市人民政府","location":"湛江市坡头区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 谢伍
    {"id":1,"person_id":1,"org_id":1,"title":"坡头区委书记","start":"2020","end":"2023","rank":"县处级","note":"约2020-2023年在任，具体任职时间需核实"},
    # 黄哲辉
    {"id":2,"person_id":2,"org_id":2,"title":"坡头区委副书记、区长","start":"2021","end":"","rank":"县处级","note":"约2021年任职，当前是否在任需核实"},
    # 陈政
    {"id":3,"person_id":3,"org_id":1,"title":"坡头区委书记","start":"2016","end":"2020","rank":"县处级","note":"约2016-2020年在任"},
    # 陈景泰
    {"id":4,"person_id":4,"org_id":2,"title":"坡头区委副书记、区长","start":"2016","end":"2021","rank":"县处级","note":"约2016-2021年在任，后调任其他职务"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 谢伍 vs 黄哲辉 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"谢伍（区委书记）与黄哲辉（区长）在坡头区共事",
     "overlap_org":"湛江市坡头区","overlap_period":"2021-2023"},

    # 陈政 vs 陈景泰 — 前任党政搭档
    {"id":2,"person_a":3,"person_b":4,"type":"党政搭档",
     "context":"陈政（原区委书记）与陈景泰（原区长）在坡头区共事",
     "overlap_org":"湛江市坡头区","overlap_period":"2016-2020"},

    # 谢伍 — 陈政 前后任
    {"id":3,"person_a":3,"person_b":1,"type":"前后任",
     "context":"陈政（2016-2020区委书记）与谢伍（2020-2023区委书记）前后任交接",
     "overlap_org":"中共湛江市坡头区委员会","overlap_period":"2020"},

    # 陈景泰 — 黄哲辉 前后任
    {"id":4,"person_a":4,"person_b":2,"type":"前后任",
     "context":"陈景泰（2016-2021区长）与黄哲辉（2021起区长）前后任交接",
     "overlap_org":"湛江市坡头区人民政府","overlap_period":"2021"},
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
    if "人大常委会" in post or "人大" in post:
        return "200,255,255"  # cyan for 人大
    if "政协" in post:
        return "255,240,200"  # cream for 政协
    if "纪委" in post:
        return "255,165,0"  # orange for discipline
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>坡头区（湛江市辖区）领导班子工作关系网络 — 2026年7月生成（部分数据需核实）</description>')
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
    is_top = any(k in p.get("current_post","") for k in ["区委书记","区长"])
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
print("\n⚠️ CRITICAL: This data is based on pre-training knowledge only.")
print("  Web access was completely unavailable during this build.")
print("  The current区委书记 and 区长 of 坡头区 could NOT be confirmed.")
print("  All data requires verification against official sources.")
print("\nOpen gaps:")
print("  1. Current区委书记 — unknown, needs official source verification")
print("  2. Current 区长 — unknown, needs official source verification")
print("  3. All birth dates, education backgrounds, and career timelines")
print("  4. Full standing committee roster")
print("  5. Complete predecessor/successor chain with exact dates")
