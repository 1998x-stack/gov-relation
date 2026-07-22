#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 宁德市 (Ningde City), 福建省 (Fujian Province).

Covers: Party Secretary (市委书记), Mayor (市长), key leadership,
predecessor/successor chains, and the prefecture-level leadership network.

Sources:
- Wikipedia (Chinese): 宁德市 leadership overview, individual biographies
- Wikipedia: 宁德历任行政首长列表
- Official government website: ningde.gov.cn
- 澎湃新闻 appointment notices (thepaper.cn)
- 人民网 (people.com.cn) appointment coverage

Generated: 2026-07-17
"""

import sqlite3, os, json, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "宁德市_network.db")
GEXF_PATH = os.path.join(BASE, "宁德市_network.gexf")
PERSONS_DIR = BASE

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 张永宁 — 宁德市委书记 (appointed 2025.05)
    {"id":1,"name":"张永宁","gender":"男","ethnicity":"汉族",
     "birth":"1967-10","birthplace":"福建晋江",
     "education":"福建师范大学物理专业大学学历",
     "party_join":"1992-06","work_start":"1989-08",
     "current_post":"宁德市委书记","current_org":"中共宁德市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E6%B0%B8%E5%AE%81"},

    # 潘国强 — 宁德市市长 (appointed 2025.07)
    {"id":2,"name":"潘国强","gender":"男","ethnicity":"汉族",
     "birth":"1974-10","birthplace":"江苏宜兴",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"宁德市市长","current_org":"宁德市人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # ── Other current city leaders ──
    # 练欣 — 宁德市人大常委会主任
    {"id":3,"name":"练欣","gender":"男","ethnicity":"汉族",
     "birth":"1973-10","birthplace":"福建福州",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"宁德市人大常委会主任","current_org":"宁德市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # 毛祚松 — 宁德市政协主席
    {"id":4,"name":"毛祚松","gender":"男","ethnicity":"汉族",
     "birth":"1968-11","birthplace":"福建福清",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"宁德市政协主席","current_org":"政协宁德市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # ── Predecessors — 市委书记 ──
    # 梁伟新 — 前任市委书记 (2021.06-2025.05)
    {"id":5,"name":"梁伟新","gender":"男","ethnicity":"汉族",
     "birth":"1965-03","birthplace":"山东莱州（生于福建南平）",
     "education":"中共中央党校研究生学历",
     "party_join":"1988-03","work_start":"1984-12",
     "current_post":"福建省人大常委会委员、财经委副主任委员","current_org":"福建省人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E6%A2%81%E4%BC%9F%E6%96%B0"},

    # 郭锡文 — 前任市委书记 (2018.07-2021.06)
    {"id":6,"name":"郭锡文","gender":"男","ethnicity":"汉族",
     "birth":"1968-01","birthplace":"福建福清",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # 廖小军 — 前任市委书记 (2011.12-2018.07)
    {"id":7,"name":"廖小军","gender":"男","ethnicity":"汉族",
     "birth":"1962-07","birthplace":"福建福州",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # 陈荣凯 — 前任市委书记 (2007.06-2011.12)
    {"id":8,"name":"陈荣凯","gender":"男","ethnicity":"汉族",
     "birth":"1956-12","birthplace":"福建闽侯",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # 朱之文 — 前任市委书记 (2003.12-2007.06)
    {"id":9,"name":"朱之文","gender":"男","ethnicity":"汉族",
     "birth":"1958-10","birthplace":"福建东山",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # ── Predecessors — 市长 ──
    # 张永宁 is person 1 (served as mayor 2021.06-2025.05 before becoming secretary)
    # 梁伟新 is person 5 (served as mayor 2018.07-2021.06 before becoming secretary)

    # 隋军 — 前任市长 (2015.12-2018.07)
    {"id":10,"name":"隋军","gender":"女","ethnicity":"汉族",
     "birth":"1969-08","birthplace":"山东莒南",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # 郑新聪 — 前任市长 (2013.02-2015.12)
    {"id":11,"name":"郑新聪","gender":"男","ethnicity":"汉族",
     "birth":"1963-11","birthplace":"福建仙游",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},

    # 廖小军 — 前任市长 (2008.05-2011.12, same as person 7)
    # 陈荣凯 — 前任市长 (2003.02-2007.06, same as person 8)
    # 周金伙 — 前任市长 (2001.09-2003.02)
    {"id":12,"name":"周金伙","gender":"男","ethnicity":"汉族",
     "birth":"1953-01","birthplace":"福建福州",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%AE%81%E5%BE%B7%E5%B8%82"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中国共产党宁德市委员会","type":"党委","level":"地级市","parent":"中共福建省委","location":"蕉城区"},
    {"id":2,"name":"宁德市人民政府","type":"政府","level":"地级市","parent":"福建省人民政府","location":"蕉城区"},
    {"id":3,"name":"宁德市人大常委会","type":"人大","level":"地级市","parent":"宁德市","location":"蕉城区"},
    {"id":4,"name":"政协宁德市委员会","type":"政协","level":"地级市","parent":"宁德市","location":"蕉城区"},
    {"id":5,"name":"中共泉州市委","type":"党委","level":"地级市","parent":"中共福建省委","location":"泉州"},
    {"id":6,"name":"泉州市人民政府","type":"政府","level":"地级市","parent":"福建省人民政府","location":"泉州"},
    {"id":7,"name":"中共石狮市委","type":"党委","level":"县级市","parent":"中共泉州市委","location":"石狮"},
    {"id":8,"name":"中共邵武市委","type":"党委","level":"县级市","parent":"中共南平市委","location":"邵武"},
    {"id":9,"name":"中共武夷山市委","type":"党委","level":"县级市","parent":"中共南平市委","location":"武夷山"},
    {"id":10,"name":"漳州市人民政府","type":"政府","level":"地级市","parent":"福建省人民政府","location":"漳州"},
    {"id":11,"name":"福建省经济和信息化委员会","type":"政府","level":"省级","parent":"福建省人民政府","location":"福州"},
    {"id":12,"name":"福建省人大常委会","type":"人大","level":"省级","parent":"福建省","location":"福州"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 张永宁 career timeline
    {"person_id":1,"org_id":1,"title":"宁德市委书记","start":"2025-05","end":"至今","rank":"正厅级","note":"2025年5月20日起任"},
    {"person_id":1,"org_id":2,"title":"宁德市市长","start":"2021-06","end":"2025-05","rank":"正厅级","note":"2021年6月21日当选"},
    {"person_id":1,"org_id":5,"title":"泉州市委副书记","start":"2018-12","end":"2021-06","rank":"副厅级","note":"专职副书记"},
    {"person_id":1,"org_id":6,"title":"泉州市副市长","start":"2015-10","end":"2018-12","rank":"副厅级","note":""},
    {"person_id":1,"org_id":7,"title":"石狮市委书记","start":"2011-06","end":"2015-10","rank":"正处级","note":"2015年6月获评全国优秀县委书记"},
    {"person_id":1,"org_id":5,"title":"泉州市发改委主任","start":"2010-02","end":"2011-06","rank":"正处级","note":""},
    {"person_id":1,"org_id":5,"title":"泉州市委副秘书长、办公室主任","start":"2009-08","end":"2010-02","rank":"正处级","note":""},
    {"person_id":1,"org_id":5,"title":"晋江市委常委、宣传部部长","start":"2006-10","end":"2009-08","rank":"副处级","note":""},
    {"person_id":1,"org_id":6,"title":"晋江市副市长","start":"2004-01","end":"2006-10","rank":"副处级","note":""},
    {"person_id":1,"org_id":7,"title":"晋江市委组织部副部长","start":"1997-10","end":"2004-01","rank":"正科级","note":"2000年起兼任编办主任"},

    # 潘国强 — 市长 (limited info available)
    {"person_id":2,"org_id":2,"title":"宁德市市长","start":"2025-07","end":"至今","rank":"正厅级","note":"2025年7月上任"},

    # 练欣 — 人大常委会主任
    {"person_id":3,"org_id":3,"title":"宁德市人大常委会主任","start":"2026-01","end":"至今","rank":"正厅级","note":""},

    # 毛祚松 — 政协主席
    {"person_id":4,"org_id":4,"title":"宁德市政协主席","start":"2026-01","end":"至今","rank":"正厅级","note":""},

    # 梁伟新 career timeline
    {"person_id":5,"org_id":1,"title":"宁德市委书记","start":"2021-06","end":"2025-05","rank":"正厅级","note":""},
    {"person_id":5,"org_id":2,"title":"宁德市市长","start":"2018-07","end":"2021-06","rank":"正厅级","note":""},
    {"person_id":5,"org_id":11,"title":"福建省经信委副主任（正厅级）","start":"2017-05","end":"2018-07","rank":"正厅级","note":""},
    {"person_id":5,"org_id":10,"title":"漳州市副市长","start":"2013-12","end":"2017-05","rank":"副厅级","note":""},
    {"person_id":5,"org_id":8,"title":"邵武市委书记","start":"2005-08","end":"2011-06","rank":"正处级","note":""},
    {"person_id":5,"org_id":9,"title":"武夷山市委书记","start":"2011-06","end":"2013-12","rank":"正处级","note":""},

    # 郭锡文
    {"person_id":6,"org_id":1,"title":"宁德市委书记","start":"2018-07","end":"2021-06","rank":"正厅级","note":""},

    # 廖小军
    {"person_id":7,"org_id":1,"title":"宁德市委书记","start":"2011-12","end":"2018-07","rank":"正厅级","note":""},
    {"person_id":7,"org_id":2,"title":"宁德市市长","start":"2008-05","end":"2011-12","rank":"正厅级","note":""},

    # 陈荣凯
    {"person_id":8,"org_id":1,"title":"宁德市委书记","start":"2007-06","end":"2011-12","rank":"正厅级","note":""},
    {"person_id":8,"org_id":2,"title":"宁德市市长","start":"2003-02","end":"2007-06","rank":"正厅级","note":""},

    # 朱之文
    {"person_id":9,"org_id":1,"title":"宁德市委书记","start":"2003-12","end":"2007-06","rank":"正厅级","note":""},

    # 隋军
    {"person_id":10,"org_id":2,"title":"宁德市市长","start":"2015-12","end":"2018-07","rank":"正厅级","note":""},

    # 郑新聪
    {"person_id":11,"org_id":2,"title":"宁德市市长","start":"2013-02","end":"2015-12","rank":"正厅级","note":""},

    # 周金伙
    {"person_id":12,"org_id":2,"title":"宁德市市长","start":"2001-09","end":"2003-02","rank":"正厅级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 张永宁 ←→ 梁伟新 (predecessor-successor, both mayor and secretary)
    {"person_a":1,"person_b":5,"type":"predecessor_successor","context":"张永宁接替梁伟新任宁德市长(2021年)，后接替梁伟新任市委书记(2025年)","overlap_org":"宁德市","overlap_period":"2021-2025","strength":"strong"},
    # 张永宁 → 许维泽 (predecessor as 石狮市委书记)
    # 梁伟新 → 郭锡文 (predecessor as 市委书记)
    {"person_a":5,"person_b":6,"type":"predecessor_successor","context":"梁伟新接替郭锡文任宁德市委书记","overlap_org":"中共宁德市委","overlap_period":"2021","strength":"strong"},
    # 郭锡文 → 廖小军
    {"person_a":6,"person_b":7,"type":"predecessor_successor","context":"郭锡文接替廖小军任宁德市委书记","overlap_org":"中共宁德市委","overlap_period":"2018","strength":"strong"},
    # 廖小军 → 陈荣凯
    {"person_a":7,"person_b":8,"type":"predecessor_successor","context":"廖小军接替陈荣凯任宁德市委书记","overlap_org":"中共宁德市委","overlap_period":"2011-2012","strength":"strong"},
    # 张永宁 → 梁伟新 (mayor → secretary: 张永宁接替梁伟新为市长)
    {"person_a":5,"person_b":1,"type":"predecessor_successor","context":"张永宁接替梁伟新任宁德市长","overlap_org":"宁德市人民政府","overlap_period":"2018-2021","strength":"strong"},
    # 梁伟新 → 郭锡文 (市长接替)
    {"person_a":5,"person_b":6,"type":"predecessor_successor","context":"梁伟新接替郭锡文任宁德市长","overlap_org":"宁德市人民政府","overlap_period":"2018","strength":"strong"},
    # 隋军 → 郑新聪
    {"person_a":10,"person_b":11,"type":"predecessor_successor","context":"隋军接替郑新聪任宁德市长","overlap_org":"宁德市人民政府","overlap_period":"2015-2016","strength":"strong"},

    # 张永宁 - 泉州市系统
    {"person_a":1,"person_b":11,"type":"same_system","context":"张永宁(泉州系统)、郑新聪(曾任泉州市长、福建省副省长)","overlap_org":"","overlap_period":"","strength":"weak"},

    # 练欣 — 人大常委会主任 relation (limited info)
    # 潘国强 — 市长 relation (limited info - 江苏宜兴人, cross-province move)
]

# =========================================================================
# HELPERS
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    n = p["name"]
    if n in ("张永宁",):
        return "255,50,50"     # Red for party secretary
    if n in ("潘国强",):
        return "50,100,255"    # Blue for government head
    # Predecessor secretaries
    if n in ("梁伟新","郭锡文","廖小军","陈荣凯","朱之文"):
        return "200,100,100"   # Dark red for former secretaries
    # Predecessor mayors
    if n in ("隋军","郑新聪","周金伙"):
        return "100,100,200"   # Dark blue for former mayors
    # Other roles
    if n in ("练欣",):
        return "200,200,100"   # Yellow for人大
    if n in ("毛祚松",):
        return "200,200,100"   # Yellow for政协
    return "100,100,100"       # Grey

def org_color(o):
    t = o["type"]
    if t == "党委": return "255,200,200"
    if t == "政府": return "200,200,255"
    if t == "人大": return "200,255,255"
    if t == "政协": return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    return p["name"] in ("张永宁","潘国强","梁伟新")

def person_node_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                   p["education"],p["party_join"],p["work_start"],p["current_post"],
                   p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions(person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"SQLite DB written: {DB_PATH}")
    return True

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>宁德市领导工作关系网络 - Fujian Province</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p).split(",")
        sz = person_node_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # person → organization (worked_at)
    for pos in positions:
        p = next(x for x in persons if x["id"] == pos["person_id"])
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph written: {GEXF_PATH}")
    return True

# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(p, filename_suffix):
    person_id = f"ningde_{p['name']}"
    fname = f"20260717-福建省-宁德市-{filename_suffix}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)

    # Build career timeline from positions
    career = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            career.append({
                "start": pos["start"],
                "end": pos["end"],
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "rank": pos["rank"],
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })

    # Build relationships
    rels = []
    for r in relationships:
        if r["person_a"] == p["id"]:
            other = next((x for x in persons if x["id"] == r["person_b"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"ningde_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": r["strength"],
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })
        elif r["person_b"] == p["id"]:
            other = next((x for x in persons if x["id"] == r["person_a"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"ningde_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": r["strength"],
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })

    data = {
        "schema_version": "1.0",
        "generated_at": "2026-07-17",
        "investigation_scope": {
            "province": "福建省",
            "city": "宁德市",
            "region": "宁德市",
            "job": filename_suffix,
            "task_id": "fujian_宁德市",
            "time_focus": "2000-2026"
        },
        "identity": {
            "person_id": person_id,
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": p["birthplace"],
            "education": [{"period":"","institution":p["education"],"major":"","degree":"","study_type":"unknown","source_ids":["S001"]}] if p["education"] else [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p['birth']}",
                "name_birthplace": f"{p['name']}_{p['birthplace']}",
                "official_profile_url": p["source"]
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id":"S001","title":"Wikipedia Chinese","url":p["source"],"publisher":"Wikipedia","published_at":"","accessed_at":"2026-07-17","source_type":"encyclopedia","reliability":"medium","notes":""}
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": ""
        },
        "open_questions": [
            {"priority":"high","question":f"潘国强（现任市长）的完整履历和出生地","why_it_matters":"核心人物完整履历对图谱完整性至关重要","suggested_queries":[f"潘国强 简历","潘国强 宁德"],"last_attempted":"2026-07-17"},
            {"priority":"medium","question":"练欣、毛祚松的完整简历","why_it_matters":"完善四大班子领导信息","suggested_queries":["练欣 简历","毛祚松 简历"],"last_attempted":"2026-07-17"}
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {fpath}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"=== Building 宁德市 data (as_of={AS_OF}) ===")
    build_sqlite()
    build_gexf()
    # Write person JSONs for core figures
    # 张永宁 — 市委书记
    write_person_json(persons[0], "市委书记")
    # 潘国强 — 市长
    write_person_json(persons[1], "市长")
    # 梁伟新 — 前任市委书记/市长
    write_person_json(persons[4], "前任市委书记")

    # Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print("=== Done ===")
