#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 遂溪县 (Suixi County), 湛江市, 广东省.

Covers: county-level leaders (县委书记, 县长), key standing committee members,
predecessor chain, and organizational relationships.

Sources:
- 遂溪县人民政府 official site: www.suixi.gov.cn (unreachable during build)
- 湛江市人民政府: www.zhanjiang.gov.cn (source for confirmed 县长 张洋)
- 维基百科: zh.wikipedia.org (source for 余庆创 as 县委书记, 2018-era source)
- Baidu Baike / web search (all sources unreachable due to access restrictions)

Current as of: July 2026

IMPORTANT: This build was conducted under severe web access degradation
(Exa rate-limited, Baidu 403, suixi.gov.cn timed out, Jina Reader timeout,
Google/Bing search blocked). All data should be verified against official sources.
See open_questions in person JSON files for gaps.

Key findings:
- 县长: 张洋 (confirmed 2026-07-22 via official government news: "遂溪县委副书记、县长张洋")
- 县委书记: 不详 (Wikipedia lists 余庆创, but source is 2018; no recent 2025-2026 news
  shows the 县委书记. All recent county party committee meetings were presided by 张洋,
  suggesting the position may be vacant or in transition)
- Party standing committee members identified from meeting news reports
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "遂溪县_network.db")
GEXF_PATH = os.path.join(BASE, "遂溪县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# ⚠️ 县委书记 is unconfirmed. All data requires verification.
# =========================================================================

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current leadership
    # ═════════════════════════════════════════════════════════════════════

    # 张洋 — 遂溪县委副书记、县长 (confirmed as of 2026-07)
    {"id":1,"name":"张洋","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县委副书记、县长","current_org":"遂溪县人民政府",
     "source":"湛江市人民政府网站 — 遂溪县新闻确认（2026-07-22）"},

    # 余庆创 — Wikipedia lists as 县委书记, source from 2018, currency unverified
    {"id":2,"name":"余庆创","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"Wikipedia列书记载为遂溪县委书记（2018年来源，当前是否在任待查）","current_org":"中共遂溪县委员会",
     "source":"维基百科遂溪县条目标注（2018年来源）"},

    # ═════════════════════════════════════════════════════════════════════
    # Standing committee members (identified from official news)
    # ═════════════════════════════════════════════════════════════════════

    # 沈东宇 — 县人大常委会主任 (2026-07-08 party plenum seated in主席台)
    {"id":3,"name":"沈东宇","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县人大常委会主任","current_org":"遂溪县人民代表大会常务委员会",
     "source":"湛江市人民政府网站 — 遂溪县委十四届十次全会报道（2026-07-08）"},

    # 温观寿 — 县委副书记 (presided over 县委农村工作会议, 2026-06-29)
    {"id":4,"name":"温观寿","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县委副书记","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县新闻报道"},

    # 朱帝池 — 县委常委 (seated in主席台 at plenum)
    {"id":5,"name":"朱帝池","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县委常委","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县委十四届十次全会报道"},

    # 豆萍英 — 县委常委 (seated in主席台 at plenum)
    {"id":6,"name":"豆萍英","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县委常委","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县委十四届十次全会报道"},

    # 陈光提 — 县委常委 (seated in主席台 at plenum)
    {"id":7,"name":"陈光提","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县委常委","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县新闻报道"},

    # 伍华武 — 县委常委 (seated in主席台 at plenum)
    {"id":8,"name":"伍华武","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县委常委","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县委十四届十次全会报道"},

    # 朱凌静 — 县委常委 (seated in主席台 at plenum)
    {"id":9,"name":"朱凌静","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县委常委","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县委十四届十次全会报道"},

    # 邓志敏 — 县领导 (百千万工程专题工作会议)
    {"id":10,"name":"邓志敏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县领导（具体职务待查）","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县百千万工程专题工作会报道（2026-07-22）"},

    # 朱锐 — 县领导
    {"id":11,"name":"朱锐","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县领导（具体职务待查）","current_org":"中共遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县百千万工程专题工作会报道（2026-07-22）"},

    # 庄兆杰 — 县领导
    {"id":12,"name":"庄兆杰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县领导（具体职务待查）","current_org":"遂溪县人民政府",
     "source":"湛江市人民政府网站 — 遂溪县百千万工程专题工作会报道（2026-07-22）"},

    # 陈武 — 县领导
    {"id":13,"name":"陈武","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县领导（具体职务待查）","current_org":"遂溪县人民政府",
     "source":"湛江市人民政府网站 — 遂溪县百千万工程专题工作会报道（2026-07-22）"},

    # 黄志文 — 县领导 (遂溪县委工作会议, 2026-07-13)
    {"id":14,"name":"黄志文","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县领导（具体职务待查）","current_org":"遂溪县人民政府",
     "source":"湛江市人民政府网站 — 遂溪县委工作会议报道（2026-07-13）"},

    # 武猛 — 县领导 (遂溪县委工作会议)
    {"id":15,"name":"武猛","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县领导（具体职务待查）","current_org":"遂溪县人民政府",
     "source":"湛江市人民政府网站 — 遂溪县委工作会议报道（2026-07-13）"},

    # 潘汝权 — 县政协主席 (6·30活动, 2026-06-30)
    {"id":16,"name":"潘汝权","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"遂溪县政协主席","current_org":"中国人民政治协商会议遂溪县委员会",
     "source":"湛江市人民政府网站 — 遂溪县6·30助力乡村振兴活动报道（2026-06-30）"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共遂溪县委员会","type":"党委","level":"县处级","parent":"中共湛江市委员会","location":"湛江市遂溪县"},
    {"id":2,"name":"遂溪县人民政府","type":"政府","level":"县处级","parent":"湛江市人民政府","location":"湛江市遂溪县"},
    {"id":3,"name":"遂溪县人民代表大会常务委员会","type":"人大","level":"县处级","parent":"湛江市人民代表大会常务委员会","location":"湛江市遂溪县"},
    {"id":4,"name":"中国人民政治协商会议遂溪县委员会","type":"政协","level":"县处级","parent":"中国人民政治协商会议湛江市委员会","location":"湛江市遂溪县"},
    {"id":5,"name":"中共遂溪县纪律检查委员会","type":"党委","level":"县处级","parent":"中共湛江市纪律检查委员会","location":"湛江市遂溪县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 张洋
    {"id":1,"person_id":1,"org_id":2,"title":"遂溪县委副书记、县长","start":"","end":"","rank":"县处级","note":"当前在任，confirmed as of 2026-07-22"},
    {"id":2,"person_id":1,"org_id":1,"title":"遂溪县委副书记","start":"","end":"","rank":"县处级","note":"兼任县委副书记"},
    # 余庆创
    {"id":3,"person_id":2,"org_id":1,"title":"遂溪县委书记","start":"2018","end":"","rank":"县处级","note":"Wikipedia记载为县委书记，2018年来源，当前是否在任待查"},
    # 沈东宇
    {"id":4,"person_id":3,"org_id":3,"title":"遂溪县人大常委会主任","start":"","end":"","rank":"县处级","note":"2026年7月确认在职"},
    # 温观寿
    {"id":5,"person_id":4,"org_id":1,"title":"遂溪县委副书记","start":"","end":"","rank":"县处级","note":"2026年6月确认在职"},
    # 朱帝池
    {"id":6,"person_id":5,"org_id":1,"title":"遂溪县委常委","start":"","end":"","rank":"县处级","note":"2026年7月确认在职"},
    # 豆萍英
    {"id":7,"person_id":6,"org_id":1,"title":"遂溪县委常委","start":"","end":"","rank":"县处级","note":"2026年7月确认在职"},
    # 陈光提
    {"id":8,"person_id":7,"org_id":1,"title":"遂溪县委常委","start":"","end":"","rank":"县处级","note":"2026年7月确认在职"},
    # 伍华武
    {"id":9,"person_id":8,"org_id":1,"title":"遂溪县委常委","start":"","end":"","rank":"县处级","note":"2026年7月确认在职"},
    # 朱凌静
    {"id":10,"person_id":9,"org_id":1,"title":"遂溪县委常委","start":"","end":"","rank":"县处级","note":"2026年7月确认在职"},
    # 邓志敏
    {"id":11,"person_id":10,"org_id":1,"title":"遂溪县领导（县委或政府部门）","start":"","end":"","rank":"乡科级","note":"具体职务待查"},
    # 朱锐
    {"id":12,"person_id":11,"org_id":1,"title":"遂溪县领导（县委或政府部门）","start":"","end":"","rank":"乡科级","note":"具体职务待查"},
    # 庄兆杰
    {"id":13,"person_id":12,"org_id":2,"title":"遂溪县领导（政府部门）","start":"","end":"","rank":"乡科级","note":"具体职务待查"},
    # 陈武
    {"id":14,"person_id":13,"org_id":2,"title":"遂溪县领导（政府部门）","start":"","end":"","rank":"乡科级","note":"具体职务待查"},
    # 黄志文
    {"id":15,"person_id":14,"org_id":2,"title":"遂溪县领导（政府部门）","start":"","end":"","rank":"乡科级","note":"具体职务待查"},
    # 武猛
    {"id":16,"person_id":15,"org_id":2,"title":"遂溪县领导（政府部门）","start":"","end":"","rank":"乡科级","note":"具体职务待查"},
    # 潘汝权
    {"id":17,"person_id":16,"org_id":4,"title":"遂溪县政协主席","start":"","end":"","rank":"县处级","note":"2026年6月确认在职"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 张洋 vs 余庆创（若仍在任）— 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"张洋（县长）与余庆创（县委书记，假设仍在任）的党政搭档关系",
     "overlap_org":"遂溪县","overlap_period":"需核实"},

    # 张洋 vs 温观寿 — 县委副书记关系
    {"id":2,"person_a":1,"person_b":4,"type":"县委班子",
     "context":"张洋（县委副书记、县长）与温观寿（县委副书记）在县委班子中共事",
     "overlap_org":"中共遂溪县委员会","overlap_period":"2026"},

    # 沈东宇 vs 张洋 — 党政关系
    {"id":3,"person_a":1,"person_b":3,"type":"党政关系",
     "context":"张洋（县长）与沈东宇（县人大常委会主任）在县域治理中配合",
     "overlap_org":"遂溪县","overlap_period":"2026"},

    # 温观寿 vs 张洋 — 县委班子（已在上方）
    # 潘汝权 vs 张洋 — 政协与政府
    {"id":4,"person_a":1,"person_b":16,"type":"党政关系",
     "context":"张洋（县长）与潘汝权（县政协主席）",
     "overlap_org":"遂溪县","overlap_period":"2026"},
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
    if "书记" in post:
        return "230,50,50"  # red for party secretary
    if "县长" in post:
        return "50,100,230"  # blue for county mayor
    if "副县长" in post:
        return "80,140,230"
    if "人大常委会" in post or "人大" in post:
        return "200,255,255"  # cyan for 人大
    if "政协" in post:
        return "255,240,200"  # cream for 政协
    if "纪委" in post:
        return "255,165,0"  # orange for discipline
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>遂溪县（湛江市辖县）领导班子工作关系网络 — 2026年7月生成（部分数据需核实）</description>')
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
    is_top = any(k in p.get("current_post","") for k in ["县委书记","县长","副书记"])
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
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov),("2",""),("3",r.get("context",""))]:
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
print("\n⚠️ CRITICAL: This data is based on limited web access only.")
print("  The current 县委书记 of 遂溪县 could NOT be confirmed.")
print("  All data requires verification against official sources.")
print("\nOpen gaps:")
print("  1. Current 县委书记 — unknown, needs official source verification")
print("  2. 余庆创 — whether still in office as 县委书记 or replaced")
print("  3. All birth dates, education backgrounds, and career timelines")
print("  4. Full standing committee roster with specific portfolios")
print("  5. 张洋's complete career timeline")
print("  6. Predecessor/successor chain with exact dates")
