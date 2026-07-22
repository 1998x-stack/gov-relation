#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 金昌市 (Jinchang City, Gansu) leadership network.

金昌市 — 甘肃省地级市, 镍都.
Covers current Party Secretary (王方太), Mayor (王琳玺), their predecessors,
key Standing Committee members, and county/district-level leaders.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_金昌市")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "金昌市_network.db")
GEXF_PATH = os.path.join(STAGING, "金昌市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. City-level top leadership (current) ──

    # 王方太 — 金昌市委书记 (as of 2024.07)
    {"id":1,"name":"王方太","gender":"男","ethnicity":"汉族",
     "birth":"1973-02","birthplace":"甘肃天水",
     "education":"",  # 待查
     "party_join":"中共党员","work_start":"",
     "current_post":"金昌市委书记",
     "current_org":"中共金昌市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # 王琳玺 — 金昌市市长 (as of 2024.07)
    {"id":2,"name":"王琳玺","gender":"男","ethnicity":"汉族",
     "birth":"1971-12","birthplace":"甘肃会宁",
     "education":"",  # 待查
     "party_join":"中共党员","work_start":"",
     "current_post":"金昌市人民政府市长",
     "current_org":"金昌市人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # 王富民 — 金昌市人大常委会主任 (as of 2021.12)
    {"id":3,"name":"王富民","gender":"男","ethnicity":"汉族",
     "birth":"1965-05","birthplace":"陕西富平",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"金昌市人大常委会主任",
     "current_org":"金昌市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # 陈华(女) — 金昌市政协主席 (as of 2021.12)
    {"id":4,"name":"陈华","gender":"女","ethnicity":"汉族",
     "birth":"1966-12","birthplace":"甘肃张掖",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"金昌市政协主席",
     "current_org":"金昌市政协",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # ── B. Predecessors — 市委书记 ──

    # 王钧 — 前任市委书记 (2021.07-2024.07), 现任甘肃省副省长
    {"id":5,"name":"王钧","gender":"男","ethnicity":"汉族",
     "birth":"1971-02","birthplace":"甘肃陇南",
     "education":"西北师范大学",
     "party_join":"1992-06","work_start":"",
     "current_post":"甘肃省副省长（原金昌市委书记）",
     "current_org":"甘肃省人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E9%92%A7_(1971%E5%B9%B4)"},

    # 张永霞(女) — 前任市委书记 (2019.12-2021.07), 现任甘肃省委常委、宣传部部长
    {"id":6,"name":"张永霞","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"甘肃省委常委、宣传部部长（原金昌市委书记）",
     "current_org":"中共甘肃省委员会",
     "source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E6%B0%B8%E9%9C%9E"},

    # 王建太 — 前任市委书记 (2018.02-2019.12)
    {"id":7,"name":"王建太","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原金昌市委书记",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # 吴明明(女) — 前任市委书记 (2013.11-2018.01)
    {"id":8,"name":"吴明明","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原金昌市委书记",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # 张令平 — 前任市委书记 (2011.09-2013.11)
    {"id":9,"name":"张令平","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原金昌市委书记",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # ── C. Predecessors — 市长 ──

    # 王方太 — 前任市长 (2021.07-2024.07), 现任市委书记
    # (same as id=1, but track prior role)

    # 王钧 — 前任市长 (2020.09-2021.07), 后任书记
    # (same as id=5)

    # 杨建武 — 前任市长 (2016.09-2020.09)
    {"id":10,"name":"杨建武","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原金昌市市长",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # 张应华 — 前任市长 (2011.09-2016.09)
    {"id":11,"name":"张应华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原金昌市市长",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # ── D. Key deputies — 市委常委 ──

    # 常守远 — 原市委副书记 (已任别的职务), 人大副主任等需确认
    {"id":12,"name":"常守远","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"金昌市委常委（待确认具体职务）",
     "current_org":"中共金昌市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # ── E. 金川区 (下辖区) ──
    # 金川区委书记 — 待补充
    {"id":13,"name":"李生虎","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"金川区委书记",
     "current_org":"中共金川区委员会",
     "source":""},

    # ── F. 永昌县 (下辖县) ──
    # 永昌县委书记 — 待补充
    {"id":14,"name":"张健","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"永昌县委书记",
     "current_org":"中共永昌县委员会",
     "source":""},

    # ── G. 金川集团（重要地方企业）──
    {"id":15,"name":"阮英","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"金川集团党委书记、董事长",
     "current_org":"金川集团股份有限公司",
     "source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 金昌市级核心
    {"id":1,"name":"中共金昌市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省金昌市金川区"},
    {"id":2,"name":"金昌市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省金昌市金川区"},
    {"id":3,"name":"金昌市人大常委会","type":"人大","level":"地级","parent":"甘肃省人大常委会","location":"甘肃省金昌市金川区"},
    {"id":4,"name":"金昌市政协","type":"政协","level":"地级","parent":"政协甘肃省委员会","location":"甘肃省金昌市金川区"},
    {"id":5,"name":"中共金昌市纪律检查委员会","type":"党委","level":"地级","parent":"中共金昌市委员会","location":"甘肃省金昌市金川区"},

    # 上级
    {"id":6,"name":"中共甘肃省委员会","type":"党委","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":7,"name":"甘肃省人民政府","type":"政府","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":8,"name":"甘肃省人大常委会","type":"人大","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":9,"name":"政协甘肃省委员会","type":"政协","level":"省级","parent":"","location":"甘肃省兰州市"},

    # 下辖区县
    {"id":10,"name":"中共金川区委员会","type":"党委","level":"县级","parent":"中共金昌市委员会","location":"甘肃省金昌市金川区"},
    {"id":11,"name":"金川区人民政府","type":"政府","level":"县级","parent":"金昌市人民政府","location":"甘肃省金昌市金川区"},
    {"id":12,"name":"中共永昌县委员会","type":"党委","level":"县级","parent":"中共金昌市委员会","location":"甘肃省金昌市永昌县"},
    {"id":13,"name":"永昌县人民政府","type":"政府","level":"县级","parent":"金昌市人民政府","location":"甘肃省金昌市永昌县"},

    # 重要企业
    {"id":14,"name":"金川集团股份有限公司","type":"事业单位","level":"地级","parent":"甘肃省人民政府","location":"甘肃省金昌市金川区"},

    # 省级部门
    {"id":15,"name":"中共甘肃省委宣传部","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
]

# =========================================================================
# POSITIONS (career timeline edges)
# =========================================================================
positions = [
    # 王方太 — 书记 (and previously 市长)
    {"id":1,"person_id":1,"org_id":1,"title":"金昌市委书记","start":"2024-07","end":"present","rank":"正厅级","note":""},
    {"id":2,"person_id":1,"org_id":2,"title":"金昌市人民政府市长","start":"2021-07","end":"2024-07","rank":"正厅级","note":"后任市委书记"},
    {"id":3,"person_id":1,"org_id":6,"title":"原甘肃省任职（具体部门待查）","start":"","end":"2021-07","rank":"","note":"任市长前在省直机关工作"},

    # 王琳玺 — 市长
    {"id":4,"person_id":2,"org_id":2,"title":"金昌市人民政府市长（代市长/市长）","start":"2024-07","end":"present","rank":"正厅级","note":""},
    {"id":5,"person_id":2,"org_id":6,"title":"原甘肃省任职（具体部门待查）","start":"","end":"2024-07","rank":"","note":"任市长前在省直机关工作"},

    # 王富民 — 人大主任
    {"id":6,"person_id":3,"org_id":3,"title":"金昌市人大常委会主任","start":"2021-12","end":"present","rank":"正厅级","note":""},

    # 陈华 — 政协主席
    {"id":7,"person_id":4,"org_id":4,"title":"金昌市政协主席","start":"2021-12","end":"present","rank":"正厅级","note":""},

    # 王钧 — 前任书记/市长，现任副省长
    {"id":8,"person_id":5,"org_id":7,"title":"甘肃省副省长","start":"2024-07","end":"present","rank":"副省级","note":""},
    {"id":9,"person_id":5,"org_id":1,"title":"金昌市委书记","start":"2021-07","end":"2024-07","rank":"正厅级","note":""},
    {"id":10,"person_id":5,"org_id":2,"title":"金昌市人民政府市长","start":"2020-09","end":"2021-07","rank":"正厅级","note":"后任书记"},

    # 张永霞 — 前任书记
    {"id":11,"person_id":6,"org_id":15,"title":"甘肃省委常委、宣传部部长","start":"","end":"present","rank":"副省级","note":""},
    {"id":12,"person_id":6,"org_id":1,"title":"金昌市委书记","start":"2019-12","end":"2021-07","rank":"正厅级","note":""},

    # 王建太 — 前任书记
    {"id":13,"person_id":7,"org_id":1,"title":"金昌市委书记","start":"2018-02","end":"2019-12","rank":"正厅级","note":""},

    # 吴明明 — 前任书记
    {"id":14,"person_id":8,"org_id":1,"title":"金昌市委书记","start":"2013-11","end":"2018-01","rank":"正厅级","note":""},

    # 张令平 — 前任书记
    {"id":15,"person_id":9,"org_id":1,"title":"金昌市委书记","start":"2011-09","end":"2013-11","rank":"正厅级","note":""},

    # 杨建武 — 前任市长
    {"id":16,"person_id":10,"org_id":2,"title":"金昌市人民政府市长","start":"2016-09","end":"2020-09","rank":"正厅级","note":""},

    # 张应华 — 前任市长
    {"id":17,"person_id":11,"org_id":2,"title":"金昌市人民政府市长","start":"2011-09","end":"2016-09","rank":"正厅级","note":""},

    # 常守远 — 市委
    {"id":18,"person_id":12,"org_id":1,"title":"金昌市委常委","start":"","end":"","rank":"副厅级","note":"待确认具体职务"},

    # 金川区
    {"id":19,"person_id":13,"org_id":10,"title":"金川区委书记","start":"","end":"","rank":"正县级","note":""},

    # 永昌县
    {"id":20,"person_id":14,"org_id":12,"title":"永昌县委书记","start":"","end":"","rank":"正县级","note":""},

    # 金川集团
    {"id":21,"person_id":15,"org_id":14,"title":"金川集团党委书记、董事长","start":"","end":"","rank":"正厅级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王方太 ← → 王钧: 书记/市长 继任关联
    {"id":1,"person_a":1,"person_b":5,"type":"predecessor_successor",
     "context":"王钧→王方太: 王钧2024年7月升任副省长, 王方太由市长接任书记",
     "overlap_org":"中共金昌市委员会","overlap_period":"2024-07"},

    # 王方太 ← → 王琳玺: 市长交接
    {"id":2,"person_a":1,"person_b":2,"type":"predecessor_successor",
     "context":"王方太→王琳玺: 王方太由市长升任书记后, 王琳玺接任市长",
     "overlap_org":"金昌市人民政府","overlap_period":"2024-07"},

    # 王钧 ← → 张永霞: 书记继承
    {"id":3,"person_a":5,"person_b":6,"type":"predecessor_successor",
     "context":"张永霞→王钧: 张永霞2021年7月调离, 王钧由市长接任书记",
     "overlap_org":"中共金昌市委员会","overlap_period":"2021-07"},

    # 王钧自任市长转书记
    {"id":4,"person_a":5,"person_b":10,"type":"predecessor_successor",
     "context":"杨建武→王钧: 王钧2020年9月接任市长, 杨建武调离",
     "overlap_org":"金昌市人民政府","overlap_period":"2020-09"},

    # 张永霞←王建太
    {"id":5,"person_a":6,"person_b":7,"type":"predecessor_successor",
     "context":"王建太→张永霞: 张永霞2019年12月接任书记",
     "overlap_org":"中共金昌市委员会","overlap_period":"2019-12"},
]

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    name = p["name"]
    current = p.get("current_post", "")
    is_party_sec = "书记" in current and "副" not in current.split("书记")[0]
    is_gov_head = "市长" in current and "副" not in current
    is_gov_head = is_gov_head or ("省长" in current and "副" not in current)
    is_discipline = "纪委书记" in current or "监委" in current
    if is_party_sec:
        return "255,50,50"
    elif is_gov_head:
        return "50,100,255"
    elif is_discipline:
        return "255,165,0"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(p):
    current = p.get("current_post", "")
    return ("书记" in current and "副" not in current.split("书记")[0]) or \
           ("市长" in current and "副" not in current) or \
           ("省长" in current and "副" not in current)

# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
                   p.get("birth",""), p.get("birthplace",""), p.get("education",""),
                   p.get("party_join",""), p.get("work_start",""),
                   p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o.get("type",""), o.get("level",""),
                   o.get("parent",""), o.get("location","")))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start",""), pos.get("end",""), pos.get("rank",""),
                   pos.get("note","")))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    from datetime import datetime

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>金昌市领导关系网络 - Jinchang City Leadership Network (Gansu)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship), weight="2.0"
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
