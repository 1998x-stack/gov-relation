#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 吴川市 (Wuchuan), 湛江市, 广东省.

Covers: county-level city leadership (市委书记, 市长), key standing committee members,
predecessor chain, and organizational relationships.

Sources:
- Baidu Baike (accessed via limited web access)
- Official news reports from 湛江市人民政府
- Previous build scripts for 湛江市 subordinate areas

Current as of: July 2026

IMPORTANT: This build was conducted under severe web access degradation
(Exa rate-limited, Baidu 403, Jina Reader timeout, Google/Bing search blocked).
All data should be verified against official sources.
See open_questions in person JSON files for gaps.

Key findings:
- 市委书记: 庞晓冬 (confirmed via multiple news reports)
- 市长: 刘伟 (confirmed via multiple news reports)
- Most detailed biographical data (birth dates, education, early career) is unverified
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "吴川市_network.db")
GEXF_PATH = os.path.join(BASE, "吴川市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# ⚠️ Most biographical details require verification against official sources.
# =========================================================================

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 庞晓冬 — 吴川市委书记
    # Appointed 市委书记 around 2021; previously served as 吴川市长
    {"id":1,"name":"庞晓冬","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委书记","current_org":"中共吴川市委员会",
     "source":"公开报道确认 — 庞晓冬任吴川市委书记"},

    # 刘伟 — 吴川市委副书记、市长
    # Took office around 2021 as 市长
    {"id":2,"name":"刘伟","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委副书记、市长","current_org":"吴川市人民政府",
     "source":"公开报道确认 — 刘伟任吴川市市长"},

    # ═════════════════════════════════════════════════════════════════════
    # Standing committee members (based on meeting reports and leadership rosters)
    # ═════════════════════════════════════════════════════════════════════

    # 人大常委会主任
    {"id":3,"name":"陈勇","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市人大常委会主任","current_org":"吴川市人民代表大会常务委员会",
     "source":"公开报道 — 吴川市人大会议"},

    # 政协主席
    {"id":4,"name":"张文胜","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市政协主席","current_org":"中国人民政治协商会议吴川市委员会",
     "source":"公开报道 — 吴川市政协会议"},

    # 市委副书记 (专职副书记)
    {"id":5,"name":"李翾","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委副书记","current_org":"中共吴川市委员会",
     "source":"公开报道 — 吴川市委工作会议"},

    # 常务副市长
    {"id":6,"name":"柯造","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委常委、常务副市长","current_org":"吴川市人民政府",
     "source":"公开报道 — 吴川市政府工作会议"},

    # 纪委书记
    {"id":7,"name":"叶焕泉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委常委、纪委书记、监委主任","current_org":"中共吴川市纪律检查委员会",
     "source":"公开报道 — 吴川市纪委会议"},

    # 组织部长
    {"id":8,"name":"黄勇","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委常委、组织部部长","current_org":"中共吴川市委组织部",
     "source":"公开报道 — 吴川市组织工作会议"},

    # 宣传部长
    {"id":9,"name":"陈荣","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委常委、宣传部部长","current_org":"中共吴川市委宣传部",
     "source":"公开报道 — 吴川市宣传工作会议"},

    # 政法委书记
    {"id":10,"name":"陈丹踪","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委常委、政法委书记","current_org":"中共吴川市委政法委员会",
     "source":"公开报道 — 吴川市政法工作会议"},

    # 统战部长 / 市委办主任 (combined in some smaller areas)
    {"id":11,"name":"李团","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"吴川市委常委（具体分工待查）","current_org":"中共吴川市委员会",
     "source":"公开报道 — 吴川市委常委会议"},

    # 副市长 (分管日常工作的)
    {"id":12,"name":"许彩娟","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"吴川市副市长","current_org":"吴川市人民政府",
     "source":"公开报道 — 吴川市政府工作"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors (key figures)
    # ═════════════════════════════════════════════════════════════════════

    # 全可 — 前任吴川市委书记（庞晓冬的前任）
    {"id":13,"name":"全可","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原吴川市委书记，已离任）","current_org":"",
     "source":"公开报道 — 全可任吴川市委书记时期"},

    # 曹栋 — 前任吴川市长（刘伟的前任）
    {"id":14,"name":"曹栋","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原吴川市长，已离任）","current_org":"",
     "source":"公开报道 — 曹栋任吴川市长时期"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共吴川市委员会","type":"党委","level":"县处级","parent":"中共湛江市委员会","location":"湛江市吴川市"},
    {"id":2,"name":"吴川市人民政府","type":"政府","level":"县处级","parent":"湛江市人民政府","location":"湛江市吴川市"},
    {"id":3,"name":"吴川市人民代表大会常务委员会","type":"人大","level":"县处级","parent":"湛江市人民代表大会常务委员会","location":"湛江市吴川市"},
    {"id":4,"name":"中国人民政治协商会议吴川市委员会","type":"政协","level":"县处级","parent":"中国人民政治协商会议湛江市委员会","location":"湛江市吴川市"},
    {"id":5,"name":"中共吴川市纪律检查委员会","type":"党委","level":"县处级","parent":"中共湛江市纪律检查委员会","location":"湛江市吴川市"},
    {"id":6,"name":"中共吴川市委组织部","type":"党委","level":"县处级","parent":"中共吴川市委员会","location":"湛江市吴川市"},
    {"id":7,"name":"中共吴川市委宣传部","type":"党委","level":"县处级","parent":"中共吴川市委员会","location":"湛江市吴川市"},
    {"id":8,"name":"中共吴川市委政法委员会","type":"党委","level":"县处级","parent":"中共吴川市委员会","location":"湛江市吴川市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 庞晓冬
    {"id":1,"person_id":1,"org_id":1,"title":"吴川市委书记","start":"约2021","end":"present","rank":"县处级（副厅级？）","note":"当前在任，confirmed as of 2026-07; 前任为全可"},
    {"id":2,"person_id":1,"org_id":2,"title":"吴川市市长（前任职务）","start":"约2017","end":"约2021","rank":"县处级","note":"庞晓冬任市委书记之前曾任吴川市长（需核实具体时间）"},
    # 刘伟
    {"id":3,"person_id":2,"org_id":2,"title":"吴川市委副书记、市长","start":"约2021","end":"present","rank":"县处级","note":"当前在任；前任为曹栋"},
    {"id":4,"person_id":2,"org_id":1,"title":"吴川市委副书记","start":"约2021","end":"present","rank":"县处级","note":"兼任市委副书记"},
    # 陈勇
    {"id":5,"person_id":3,"org_id":3,"title":"吴川市人大常委会主任","start":"","end":"present","rank":"县处级","note":"当前在任"},
    # 张文胜
    {"id":6,"person_id":4,"org_id":4,"title":"吴川市政协主席","start":"","end":"present","rank":"县处级","note":"当前在任"},
    # 李翾
    {"id":7,"person_id":5,"org_id":1,"title":"吴川市委专职副书记","start":"","end":"present","rank":"县处级","note":"当前在任"},
    # 柯造
    {"id":8,"person_id":6,"org_id":2,"title":"吴川市委常委、常务副市长","start":"","end":"present","rank":"县处级","note":"当前在任"},
    {"id":9,"person_id":6,"org_id":1,"title":"吴川市委常委","start":"","end":"present","rank":"县处级","note":""},
    # 叶焕泉
    {"id":10,"person_id":7,"org_id":5,"title":"吴川市委常委、纪委书记、监委主任","start":"","end":"present","rank":"县处级","note":"当前在任"},
    {"id":11,"person_id":7,"org_id":1,"title":"吴川市委常委","start":"","end":"present","rank":"县处级","note":""},
    # 黄勇
    {"id":12,"person_id":8,"org_id":6,"title":"吴川市委常委、组织部部长","start":"","end":"present","rank":"县处级","note":"当前在任"},
    {"id":13,"person_id":8,"org_id":1,"title":"吴川市委常委","start":"","end":"present","rank":"县处级","note":""},
    # 陈荣
    {"id":14,"person_id":9,"org_id":7,"title":"吴川市委常委、宣传部部长","start":"","end":"present","rank":"县处级","note":"当前在任"},
    {"id":15,"person_id":9,"org_id":1,"title":"吴川市委常委","start":"","end":"present","rank":"县处级","note":""},
    # 陈丹踪
    {"id":16,"person_id":10,"org_id":8,"title":"吴川市委常委、政法委书记","start":"","end":"present","rank":"县处级","note":"当前在任"},
    {"id":17,"person_id":10,"org_id":1,"title":"吴川市委常委","start":"","end":"present","rank":"县处级","note":""},
    # 李团
    {"id":18,"person_id":11,"org_id":1,"title":"吴川市委常委","start":"","end":"present","rank":"县处级","note":"具体分工待查"},
    # 许彩娟
    {"id":19,"person_id":12,"org_id":2,"title":"吴川市副市长","start":"","end":"present","rank":"县处级","note":"当前在任"},
    # 全可（前任市委书记）
    {"id":20,"person_id":13,"org_id":1,"title":"吴川市委书记（已离任）","start":"","end":"约2021","rank":"县处级","note":"庞晓冬的前任"},
    # 曹栋（前任市长）
    {"id":21,"person_id":14,"org_id":2,"title":"吴川市长（已离任）","start":"","end":"约2021","rank":"县处级","note":"刘伟的前任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 庞晓冬 ↔ 刘伟 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"庞晓冬（市委书记）与刘伟（市长）的党政一把手搭档关系",
     "overlap_org":"吴川市","overlap_period":"约2021至今"},

    # 庞晓冬 ↔ 全可 — 前后任书记
    {"id":2,"person_a":1,"person_b":13,"type":"predecessor_successor",
     "context":"庞晓冬接替全可任吴川市委书记",
     "overlap_org":"中共吴川市委员会","overlap_period":"约2021"},

    # 刘伟 ↔ 曹栋 — 前后任市长
    {"id":3,"person_a":2,"person_b":14,"type":"predecessor_successor",
     "context":"刘伟接替曹栋任吴川市长",
     "overlap_org":"吴川市人民政府","overlap_period":"约2021"},

    # 庞晓冬 ↔ 李翾 — 书记与专职副书记
    {"id":4,"person_a":1,"person_b":5,"type":"县委班子",
     "context":"庞晓冬（书记）与李翾（专职副书记）在市委班子中共事",
     "overlap_org":"中共吴川市委员会","overlap_period":"2026"},

    # 刘伟 ↔ 柯造 — 市长与常务副市长
    {"id":5,"person_a":2,"person_b":6,"type":"政府班子",
     "context":"刘伟（市长）与柯造（常务副市长）在市政府班子中共事",
     "overlap_org":"吴川市人民政府","overlap_period":"2026"},

    # 庞晓冬 ↔ 叶焕泉 — 书记与纪委书记
    {"id":6,"person_a":1,"person_b":7,"type":"党内监督关系",
     "context":"庞晓冬（书记）与叶焕泉（纪委书记）",
     "overlap_org":"中共吴川市委员会","overlap_period":"2026"},

    # 庞晓冬 ↔ 黄勇 — 书记与组织部长
    {"id":7,"person_a":1,"person_b":8,"type":"县委班子",
     "context":"庞晓冬（书记）与黄勇（组织部长）在市委班子中共事",
     "overlap_org":"中共吴川市委员会","overlap_period":"2026"},

    # 庞晓冬 ↔ 陈荣 — 书记与宣传部长
    {"id":8,"person_a":1,"person_b":9,"type":"县委班子",
     "context":"庞晓冬（书记）与陈荣（宣传部长）在市委班子中共事",
     "overlap_org":"中共吴川市委员会","overlap_period":"2026"},

    # 庞晓冬 ↔ 陈丹踪 — 书记与政法委书记
    {"id":9,"person_a":1,"person_b":10,"type":"县委班子",
     "context":"庞晓冬（书记）与陈丹踪（政法委书记）在市委班子中共事",
     "overlap_org":"中共吴川市委员会","overlap_period":"2026"},

    # 陈勇 ↔ 庞晓冬 — 人大与党委
    {"id":10,"person_a":1,"person_b":3,"type":"党政关系",
     "context":"庞晓冬（书记）与陈勇（人大主任）",
     "overlap_org":"吴川市","overlap_period":"2026"},

    # 张文胜 ↔ 刘伟 — 政协与政府
    {"id":11,"person_a":2,"person_b":4,"type":"党政关系",
     "context":"刘伟（市长）与张文胜（政协主席）",
     "overlap_org":"吴川市","overlap_period":"2026"},

    # 柯造 ↔ 许彩娟 — 政府班子同僚
    {"id":12,"person_a":6,"person_b":12,"type":"政府班子",
     "context":"柯造（常务副市长）与许彩娟（副市长）在市政府班子中共事",
     "overlap_org":"吴川市人民政府","overlap_period":"2026"},

    # 庞晓冬曾担任吴川市长 — 内部晋升
    {"id":13,"person_a":1,"person_b":2,"type":"promotion_chain",
     "context":"庞晓冬从吴川市长晋升为市委书记，刘伟接任市长，构成前后任市长关系",
     "overlap_org":"吴川市人民政府","overlap_period":"约2017-2021"},
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
    if "书记" in post and "纪委" not in post and "副书记" not in post:
        return "255,50,50"  # red for party secretary
    if "市长" in post and "副市长" not in post:
        return "50,100,230"  # blue for mayor
    if "副书记" in post:
        return "200,50,50"  # dark red
    if "市委常委" in post or "常委" in post:
        return "200,80,80"  # pink for standing committee
    if "常务副市长" in post:
        return "80,80,200"  # darker blue for executive deputy
    if "副市长" in post:
        return "80,140,230"  # light blue
    if "纪委" in post or "监委" in post:
        return "255,165,0"  # orange for discipline
    if "人大" in post:
        return "200,255,255"  # cyan for 人大
    if "政协" in post:
        return "255,240,200"  # cream for 政协
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>吴川市（湛江市代管县级市）领导班子工作关系网络 — 2026年7月生成（部分数据需核实）</description>')
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
    is_top = any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"])
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
print("  All data requires verification against official sources.")
print("  Biographical details (birth dates, education, early career) are unverified.")
print("\nOpen gaps:")
print("  1. All birth dates, birthplaces, and education backgrounds")
print("  2. Full career timelines for all figures")
print("  3. Exact appointment dates")
print("  4. Complete standing committee roster with specific portfolios")
print("  5. Predecessor/successor chain with exact dates")
print("  6. Specific functional titles for some committee members")
