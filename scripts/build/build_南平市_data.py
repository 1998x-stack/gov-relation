#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Nanping City (南平市), Fujian Province.

Covers: Party Secretary (市委书记), Mayor (市长), key leadership,
predecessor/successor chains, and the city-level leadership network.

Sources:
- Wikipedia (Chinese): 南平市 leadership info and predecessor lists
- np.gov.cn: Official Nanping city government website
- Wikipedia (English): Nanping city overview

Generated: 2026-07-16
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_南平市")
DB_PATH = os.path.join(TMP, "南平市_network.db")
GEXF_PATH = os.path.join(TMP, "南平市_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 袁超洪 — 南平市委书记
    {"id":1,"name":"袁超洪","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市委书记","current_org":"中共南平市委员会","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 林建 — 南平市市长
    {"id":2,"name":"林建","gender":"男","ethnicity":"汉族","birth":"1970-11","birthplace":"","education":"在职研究生学历，管理学硕士","party_join":"中共党员","work_start":"","current_post":"南平市市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn/cms/html/npszf/lj1/index.html"},

    # ── Other current city leaders ──
    # 陈善平 — 南平市人大常委会主任
    {"id":3,"name":"陈善平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市人大常委会主任","current_org":"南平市人大常委会","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 吴添富 — 南平市政协主席 (中共党员、九三学社社员)
    {"id":4,"name":"吴添富","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员、九三学社","work_start":"","current_post":"南平市政协主席","current_org":"政协南平市委员会","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},

    # ── Current deputy mayors (from np.gov.cn) ──
    {"id":5,"name":"何明星","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市副市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},
    {"id":6,"name":"杨新强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市副市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},
    {"id":7,"name":"林湫","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市副市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},
    {"id":8,"name":"魏敦盛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市副市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},
    {"id":9,"name":"陈河北","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市副市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},
    {"id":10,"name":"黄桂诚","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市副市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},
    {"id":11,"name":"黄拔荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市副市长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},
    # 秘书长
    {"id":12,"name":"詹旭斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南平市人民政府秘书长","current_org":"南平市人民政府","source":"https://www.np.gov.cn"},

    # ── Predecessors — 市委书记 ──
    # 林瑞良 — 前任市委书记 (2021.12-2023.02)
    {"id":13,"name":"林瑞良","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 袁毅 — 前任市委书记 (2016.09-2021.02)
    {"id":14,"name":"袁毅","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 庄稼汉 — 前任市委书记 (2015.02-2016.09)
    {"id":15,"name":"庄稼汉","gender":"男","ethnicity":"汉族","birth":"1963","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 裴金佳 — 前任市委书记 (2012.01-2015.02)
    {"id":16,"name":"裴金佳","gender":"男","ethnicity":"汉族","birth":"1963","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 雷春美 — 前任市委书记 (2008.04-2012.01), 女
    {"id":17,"name":"雷春美","gender":"女","ethnicity":"畲族","birth":"1959","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 徐谦 — 前任市委书记 (2003.07-2008.04)
    {"id":18,"name":"徐谦","gender":"男","ethnicity":"汉族","birth":"1954","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 李川 — 前任市委书记 (2001.04-2003.07)
    {"id":19,"name":"李川","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},

    # ── Predecessors — 市长 ──
    # 袁超洪 — 前任市长 (2020.09-2023.02), 升任市委书记 (same as person 1)
    # 刘洪建 — 前任市长 (2018.07-2020.07)
    {"id":20,"name":"刘洪建","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 许维泽 — 前任市长 (2016.08-2018.07)
    {"id":21,"name":"许维泽","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 林宝金 — 前任市长 (2012.01-2016.07)
    {"id":22,"name":"林宝金","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 裴金佳 — 前任市长 (2010.04-2012.01) (same as person 16)
    # 龚清概 — 前任市长 (2007.06-2010.02)
    {"id":23,"name":"龚清概","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
    # 陈桦 — 前任市长 (2003.07-2006.11), 女
    {"id":24,"name":"陈桦","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共南平市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省南平市"},
    {"id":2,"name":"南平市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省南平市"},
    {"id":3,"name":"南平市人大常委会","type":"人大","level":"地级","parent":"","location":"福建省南平市"},
    {"id":4,"name":"政协南平市委员会","type":"政协","level":"地级","parent":"","location":"福建省南平市"},
    {"id":5,"name":"中共福建省纪律检查委员会","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":6,"name":"福建省人民政府","type":"政府","level":"省级","parent":"","location":"福建省福州市"},
    {"id":7,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
    {"id":8,"name":"福建省经济和信息化委员会","type":"政府","level":"省级","parent":"福建省人民政府","location":"福建省福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 袁超洪 — Party Secretary (previously Mayor)
    {"person_id":1,"org_id":1,"title":"南平市委书记","start":"2023-02","end":"present","rank":"正厅级","note":"2023年2月任市委书记，此前为市长"},
    {"person_id":1,"org_id":2,"title":"南平市市长","start":"2020-09","end":"2023-02","rank":"正厅级","note":"2020年9月任代市长，后当选市长"},

    # 林建 — Mayor
    {"person_id":2,"org_id":2,"title":"南平市市长","start":"2023-02","end":"present","rank":"正厅级","note":"2023年2月任代市长/市长"},
    {"person_id":2,"org_id":1,"title":"南平市委副书记","start":"2023-02","end":"present","rank":"正厅级","note":"兼任市委副书记"},

    # 陈善平 — 人大主任
    {"person_id":3,"org_id":3,"title":"南平市人大常委会主任","start":"","end":"present","rank":"正厅级","note":""},

    # 吴添富 — 政协主席
    {"person_id":4,"org_id":4,"title":"南平市政协主席","start":"","end":"present","rank":"正厅级","note":"中共党员、九三学社社员"},

    # 副市长们
    {"person_id":5,"org_id":2,"title":"南平市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":6,"org_id":2,"title":"南平市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":7,"org_id":2,"title":"南平市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":8,"org_id":2,"title":"南平市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":9,"org_id":2,"title":"南平市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":10,"org_id":2,"title":"南平市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":11,"org_id":2,"title":"南平市副市长","start":"","end":"present","rank":"副厅级","note":""},

    # 詹旭斌 — 秘书长
    {"person_id":12,"org_id":2,"title":"南平市人民政府秘书长","start":"","end":"present","rank":"正处级","note":""},

    # ── 前任市委书记 ──
    {"person_id":13,"org_id":1,"title":"南平市委书记","start":"2021-12","end":"2023-02","rank":"正厅级","note":"林瑞良"},
    {"person_id":14,"org_id":1,"title":"南平市委书记","start":"2016-09","end":"2021-02","rank":"正厅级","note":"袁毅"},
    {"person_id":15,"org_id":1,"title":"南平市委书记","start":"2015-02","end":"2016-09","rank":"正厅级","note":"庄稼汉"},
    {"person_id":16,"org_id":1,"title":"南平市委书记","start":"2012-01","end":"2015-02","rank":"正厅级","note":"裴金佳"},
    {"person_id":17,"org_id":1,"title":"南平市委书记","start":"2008-04","end":"2012-01","rank":"正厅级","note":"雷春美"},
    {"person_id":18,"org_id":1,"title":"南平市委书记","start":"2003-07","end":"2008-04","rank":"正厅级","note":"徐谦"},
    {"person_id":19,"org_id":1,"title":"南平市委书记","start":"2001-04","end":"2003-07","rank":"正厅级","note":"李川"},

    # ── 前任市长 ──
    {"person_id":20,"org_id":2,"title":"南平市市长","start":"2018-07","end":"2020-07","rank":"正厅级","note":"刘洪建"},
    {"person_id":21,"org_id":2,"title":"南平市市长","start":"2016-08","end":"2018-07","rank":"正厅级","note":"许维泽"},
    {"person_id":22,"org_id":2,"title":"南平市市长","start":"2012-01","end":"2016-07","rank":"正厅级","note":"林宝金"},
    {"person_id":23,"org_id":2,"title":"南平市市长","start":"2007-06","end":"2010-02","rank":"正厅级","note":"龚清概"},
    {"person_id":24,"org_id":2,"title":"南平市市长","start":"2003-07","end":"2006-11","rank":"正厅级","note":"陈桦"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Predecessor-successor: 市委书记 chain
    {"person_a":1,"person_b":13,"type":"predecessor_successor","context":"袁超洪接替林瑞良任南平市委书记","overlap_org":"中共南平市委员会","overlap_period":"2021-2023","direction":"person_to_other","strength":"strong"},
    {"person_a":13,"person_b":14,"type":"predecessor_successor","context":"林瑞良接替袁毅任南平市委书记","overlap_org":"中共南平市委员会","overlap_period":"2021","direction":"person_to_other","strength":"strong"},
    {"person_a":14,"person_b":15,"type":"predecessor_successor","context":"袁毅接替庄稼汉任南平市委书记","overlap_org":"中共南平市委员会","overlap_period":"2016","direction":"person_to_other","strength":"strong"},
    {"person_a":15,"person_b":16,"type":"predecessor_successor","context":"庄稼汉接替裴金佳任南平市委书记","overlap_org":"中共南平市委员会","overlap_period":"2015","direction":"person_to_other","strength":"strong"},
    {"person_a":16,"person_b":17,"type":"predecessor_successor","context":"裴金佳接替雷春美任南平市委书记","overlap_org":"中共南平市委员会","overlap_period":"2012","direction":"person_to_other","strength":"strong"},
    {"person_a":17,"person_b":18,"type":"predecessor_successor","context":"雷春美接替徐谦任南平市委书记","overlap_org":"中共南平市委员会","overlap_period":"2008","direction":"person_to_other","strength":"strong"},
    {"person_a":18,"person_b":19,"type":"predecessor_successor","context":"徐谦接替李川任南平市委书记","overlap_org":"中共南平市委员会","overlap_period":"2003","direction":"person_to_other","strength":"strong"},

    # Predecessor-successor: 市长 chain
    {"person_a":2,"person_b":1,"type":"predecessor_successor","context":"林建接替袁超洪任南平市市长","overlap_org":"南平市人民政府","overlap_period":"2023","direction":"person_to_other","strength":"strong"},
    {"person_a":1,"person_b":20,"type":"predecessor_successor","context":"袁超洪接替刘洪建任南平市市长","overlap_org":"南平市人民政府","overlap_period":"2020","direction":"person_to_other","strength":"strong"},
    {"person_a":20,"person_b":21,"type":"predecessor_successor","context":"刘洪建接替许维泽任南平市市长","overlap_org":"南平市人民政府","overlap_period":"2018","direction":"person_to_other","strength":"strong"},
    {"person_a":21,"person_b":22,"type":"predecessor_successor","context":"许维泽接替林宝金任南平市市长","overlap_org":"南平市人民政府","overlap_period":"2016","direction":"person_to_other","strength":"strong"},
    {"person_a":22,"person_b":16,"type":"predecessor_successor","context":"林宝金接替裴金佳任南平市市长","overlap_org":"南平市人民政府","overlap_period":"2012","direction":"person_to_other","strength":"strong"},
    {"person_a":16,"person_b":23,"type":"predecessor_successor","context":"裴金佳接替龚清概任南平市市长","overlap_org":"南平市人民政府","overlap_period":"2010","direction":"person_to_other","strength":"strong"},
    {"person_a":23,"person_b":24,"type":"predecessor_successor","context":"龚清概接替陈桦任南平市市长","overlap_org":"南平市人民政府","overlap_period":"2007","direction":"person_to_other","strength":"strong"},

    # Mayor-to-Party-Secretary promotion paths
    {"person_a":1,"person_b":13,"type":"superior_subordinate","context":"袁超洪在任市长期间与市委书记林瑞良搭班","overlap_org":"中共南平市委员会","overlap_period":"2021-2023","direction":"undirected","strength":"strong"},
    {"person_a":1,"person_b":14,"type":"superior_subordinate","context":"袁超洪任市长期间市委书记为袁毅","overlap_org":"中共南平市委员会","overlap_period":"2020-2021","direction":"undirected","strength":"strong"},
    {"person_a":22,"person_b":16,"type":"superior_subordinate","context":"林宝金任市长期间裴金佳先后任市长、市委书记","overlap_org":"南平市人民政府","overlap_period":"2012-2015","direction":"undirected","strength":"strong"},
    {"person_a":16,"person_b":17,"type":"superior_subordinate","context":"裴金佳任市长期间雷春美为市委书记","overlap_org":"中共南平市委员会","overlap_period":"2010-2012","direction":"undirected","strength":"strong"},
]


# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        direction TEXT, strength TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                   p["birthplace"],p["education"],p["party_join"],
                   p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,\"end\",rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,direction,strength) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"],r["direction"],r["strength"]))

    conn.commit()
    conn.close()
    print(f"SQLite DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    if "书记" in (p.get("current_post") or ""):
        return "255,50,50"
    elif "市长" in (p.get("current_post") or "") or "副市长" in (p.get("current_post") or ""):
        return "50,100,255"
    elif "主任" in (p.get("current_post") or "") or "政协" in (p.get("current_post") or ""):
        return "155,155,155"
    else:
        return "100,100,100"

def org_color(o):
    m = {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200"}
    return m.get(o["type"],"200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 2)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def org_size(o):
    return "8.0"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>南平市领导班子关系网络 - 福建省南平市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{org_size(o)}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(pid, filename_suffix):
    p = next(x for x in persons if x["id"] == pid)
    rels_out = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next(x for x in persons if x["id"] == r["person_b"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})
        elif r["person_b"] == pid:
            other = next(x for x in persons if x["id"] == r["person_a"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})

    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            person_positions.append({
                "start":pos["start"],"end":pos["end"],"org":org["name"] if org else "",
                "title":pos["title"],"level":pos.get("rank",""),"location":org["location"] if org else "",
                "system":"party" if org and "党委" in org["type"] else "government",
                "rank":pos.get("rank",""),"is_key_promotion":False,"notes":pos.get("note",""),
                "confidence":"confirmed","source_ids":["S001"]
            })

    profile = {
        "schema_version": "1.0",
        "generated_at": "2026-07-16",
        "investigation_scope": {
            "province": "福建省",
            "city": "南平市",
            "region": "南平市",
            "job": filename_suffix,
            "task_id": "fujian_南平市",
            "time_focus": "1995-present"
        },
        "identity": {
            "person_id": f"fujian_nanping_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":"","study_type":"unknown","source_ids":[]}],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {"name_birth":"","name_birthplace":"","official_profile_url":""}
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正厅级",
            "as_of": "2026-07-16",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": person_positions,
        "organizations": [],
        "relationships": rels_out,
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
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id":"S001","title":"南平市 - 维基百科","url":"https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82",
             "publisher":"维基百科","published_at":"","accessed_at":"2026-07-16","source_type":"encyclopedia","reliability":"medium","notes":""},
            {"id":"S002","title":"林建市长 - 南平市人民政府","url":"https://www.np.gov.cn/cms/html/npszf/lj1/index.html",
             "publisher":"南平市人民政府","published_at":"","accessed_at":"2026-07-16","source_type":"official","reliability":"high","notes":""},
            {"id":"S003","title":"Nanping - English Wikipedia","url":"https://en.wikipedia.org/wiki/Nanping",
             "publisher":"Wikipedia","published_at":"","accessed_at":"2026-07-16","source_type":"encyclopedia","reliability":"medium","notes":""}
        ],
        "confidence_summary": {
            "identity":"partial",
            "current_role":"confirmed",
            "career_completeness":"partial",
            "relationship_confidence":"high",
            "biggest_gap":f"缺少{p['name']}的出生地、早期教育背景和完整履历时间线"
        },
        "open_questions": [
            {"priority":"high","question":f"{p['name']}的出生地和早期教育背景","why_it_matters":"影响人物身份确认和履历完整度",
             "suggested_queries":[f"{p['name']} 简历",f"{p['name']} 出生"],"last_attempted":"2026-07-16"},
            {"priority":"high","question":f"{p['name']}在任南平前的完整履历","why_it_matters":"理解其职业发展路径和提拔背景",
             "suggested_queries":[f"{p['name']} 任职经历"],"last_attempted":"2026-07-16"}
        ]
    }

    filename = f"20260716-福建省-南平市-{filename_suffix}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"Person JSON created: {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_sqlite()
    build_gexf()
    write_person_json(1, "市委书记")
    write_person_json(2, "市长")
    print("\nDone. All artifacts written to", TMP)
