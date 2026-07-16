#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 云霄县 (Yunxiao County, Fujian) leadership network.

云霄县 — 县, 福建省漳州市下辖, 位于福建省南部沿海.
Research date: 2026-07-16

Sources:
- yunxiao.gov.cn official news articles (July 2026)
- 云霄融媒 reports on county leadership activities

Coverage:
- Current top 2 leaders: 县委书记 杨志滨, 代县长 孙可
- 县人大常委会, 县政协 leaders
- Predecessors: 蓝良木 (前县委书记), 杨志滨 (前县长)
- Key county-level officials observed in 2026 news coverage
- 常山开发区 leadership (云霄县委书记/县长 concurrently serve)

Confidence notes:
- 杨志滨: confirmed current 县委书记 and former 县长
- 孙可: confirmed 代县长 (as of July 2026)
- 蓝良木: confirmed former 县委书记 (as of June 2026)
- Other county leaders: roles confirmed from news; detailed bios are partial
- Early careers of most leaders need further research
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_云霄县")
DB_PATH = os.path.join(STAGING, "云霄县_network.db")
GEXF_PATH = os.path.join(STAGING, "云霄县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 杨志滨 — 云霄县委书记、常山开发区党工委书记 (promoted from 县长 ~2026 Q2)
    {"id":1,"name":"杨志滨","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县委书记、常山开发区党工委书记",
     "current_org":"中共云霄县委员会",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-13/312576464.html"},
    # 孙可 — 云霄县委副书记、代县长、常山开发区管委会主任 (as of ~2026 Q2)
    {"id":2,"name":"孙可","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县委副书记、代县长、常山开发区管委会主任",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-13/312576464.html"},

    # ── 2. 县人大/政协 leaders ──
    # 黄文疆 — 县人大常委会主任
    {"id":3,"name":"黄文疆","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县人大常委会主任",
     "current_org":"云霄县人大常委会",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-15/1271913070.html"},
    # 林意纯 — 县政协主席
    {"id":4,"name":"林意纯","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县政协主席",
     "current_org":"政协云霄县委员会",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-15/1271913070.html"},
    # 方响宏 — 县政协党组书记
    {"id":5,"name":"方响宏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县政协党组书记",
     "current_org":"政协云霄县委员会",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-15/1271913070.html"},

    # ── 3. Known county-level officials (from 2026 news) ──
    # 林贵达 — 县领导 (observed in safety inspection)
    {"id":6,"name":"林贵达","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-13/312576464.html"},
    # 郑雯雯 — 县领导 (observed in 政法/宣传调研)
    {"id":7,"name":"郑雯雯","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-09/2123347012.html"},
    # 沈生辉 — 县领导
    {"id":8,"name":"沈生辉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-09/2123347012.html"},
    # 洪逸峰 — 县领导 (frequent appearances)
    {"id":9,"name":"洪逸峰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-09/2123347012.html"},
    # 陈国海 — 县领导
    {"id":10,"name":"陈国海","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-09/2123347012.html"},
    # 汤永坚 — 副县长 (presides over maritime safety meeting)
    {"id":11,"name":"汤永坚","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县副县长",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-06-12/882734293.html"},
    # 蔡猛添 — 县领导 (finance/agriculture)
    {"id":12,"name":"蔡猛添","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-08/709245207.html"},
    # 何少栋 — 县领导 (常山调研)
    {"id":13,"name":"何少栋","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-07/2095273521.html"},
    # 董勇贵 — 县领导 (云陵调研)
    {"id":14,"name":"董勇贵","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-08/421087085.html"},
    # 方成江 — 县领导
    {"id":15,"name":"方成江","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-08/421087085.html"},
    # 王荷明 — 县领导 (莆美/云陵调研)
    {"id":16,"name":"王荷明","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县领导",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-08/709245207.html"},
    # 吴兰波 — 副县长 (commerce/agriculture)
    {"id":17,"name":"吴兰波","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"云霄县副县长",
     "current_org":"云霄县人民政府",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-08/709245207.html"},

    # ── 4. 常山开发区 leadership ──
    # 陈顺国 — 常山开发区管委会常务副主任
    {"id":18,"name":"陈顺国","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"常山开发区管委会常务副主任",
     "current_org":"常山开发区管委会",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-07-15/1271913070.html"},
    # 林靖 — 常山开发区管委会副主任
    {"id":19,"name":"林靖","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"常山开发区管委会副主任",
     "current_org":"常山开发区管委会",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-06-10/1436694849.html"},

    # ── 5. Predecessors ──
    # 蓝良木 — 前云霄县委书记、常山开发区党工委书记 (as of June 2026)
    {"id":20,"name":"蓝良木","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"（原云霄县委书记、常山开发区党工委书记）",
     "current_org":"",
     "source":"http://www.yunxiao.gov.cn/cms/html/yxxrmzf/2026-06-12/882734293.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共云霄县委员会","type":"党委","level":"县级","parent":"中共漳州市委员会","location":"福建省漳州市云霄县"},
    {"id":2,"name":"云霄县人民政府","type":"政府","level":"县级","parent":"漳州市人民政府","location":"福建省漳州市云霄县"},
    {"id":3,"name":"云霄县人大常委会","type":"人大","level":"县级","parent":"","location":"福建省漳州市云霄县"},
    {"id":4,"name":"政协云霄县委员会","type":"政协","level":"县级","parent":"","location":"福建省漳州市云霄县"},
    {"id":5,"name":"常山开发区管委会","type":"开发区","level":"县级","parent":"漳州市人民政府","location":"福建省漳州市云霄县常山"},
    {"id":6,"name":"中共云霄县纪律检查委员会","type":"党委","level":"县级","parent":"中共云霄县委员会","location":"福建省漳州市云霄县"},
    {"id":7,"name":"中共云霄县委政法委员会","type":"党委","level":"县级","parent":"中共云霄县委员会","location":"福建省漳州市云霄县"},
    {"id":8,"name":"中共云霄县委宣传部","type":"党委","level":"县级","parent":"中共云霄县委员会","location":"福建省漳州市云霄县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 杨志滨 career timeline (partial) ──
    {"id":1,"person_id":1,"org_id":2,"title":"云霄县县长、常山开发区管委会主任","start":"~2022","end":"~2026-06","rank":"正处","note":"前职, 具体起始时间待核实"},
    {"id":2,"person_id":1,"org_id":1,"title":"云霄县委书记、常山开发区党工委书记","start":"~2026-06","end":"present","rank":"正处","note":"现任; 由县长转任书记"},
    {"id":3,"person_id":1,"org_id":5,"title":"常山开发区管委会主任（兼任）","start":"~2022","end":"~2026-06","rank":"正处","note":"县长兼管委会主任"},
    {"id":4,"person_id":1,"org_id":5,"title":"常山开发区党工委书记（兼任）","start":"~2026-06","end":"present","rank":"正处","note":"现任; 书记兼党工委书记"},

    # ── 孙可 career timeline (partial) ──
    {"id":5,"person_id":2,"org_id":2,"title":"云霄县委副书记、代县长、常山开发区管委会主任","start":"~2026-06","end":"present","rank":"正处","note":"现任代县长"},

    # ── 黄文疆 ──
    {"id":6,"person_id":3,"org_id":3,"title":"云霄县人大常委会主任","start":"~2025","end":"present","rank":"正处","note":"现任"},

    # ── 林意纯 ──
    {"id":7,"person_id":4,"org_id":4,"title":"云霄县政协主席","start":"~2025","end":"present","rank":"正处","note":"现任"},

    # ── 方响宏 ──
    {"id":8,"person_id":5,"org_id":4,"title":"云霄县政协党组书记","start":"~2026","end":"present","rank":"正处","note":"现任"},

    # ── 林贵达 ──
    {"id":9,"person_id":6,"org_id":2,"title":"云霄县领导（副县长/常委）","start":"~2026","end":"present","rank":"副处","note":"具体职务待核实"},

    # ── 郑雯雯 ──
    {"id":10,"person_id":7,"org_id":1,"title":"云霄县领导（常委/政法委/宣传）","start":"~2026","end":"present","rank":"副处","note":"参与政法官传调研"},

    # ── 沈生辉 ──
    {"id":11,"person_id":8,"org_id":1,"title":"云霄县领导（常委/政法委）","start":"~2026","end":"present","rank":"副处","note":"参与政法调研"},

    # ── 洪逸峰 ──
    {"id":12,"person_id":9,"org_id":1,"title":"云霄县领导（常委/县委办）","start":"~2026","end":"present","rank":"副处","note":"频繁出现在各类调研中"},

    # ── 陈国海 ──
    {"id":13,"person_id":10,"org_id":7,"title":"云霄县领导（政法委）","start":"~2026","end":"present","rank":"副处","note":"参与政法调研"},

    # ── 汤永坚 ──
    {"id":14,"person_id":11,"org_id":2,"title":"云霄县副县长","start":"~2024","end":"present","rank":"副处","note":"现任; 分管安全生产/海上安全"},

    # ── 蔡猛添 ──
    {"id":15,"person_id":12,"org_id":2,"title":"云霄县领导（副县长）","start":"~2025","end":"present","rank":"副处","note":"参与金融/城建调研"},

    # ── 何少栋 ──
    {"id":16,"person_id":13,"org_id":2,"title":"云霄县领导（常山/社会事务）","start":"~2026","end":"present","rank":"副处","note":"参与常山调研"},

    # ── 董勇贵 ──
    {"id":17,"person_id":14,"org_id":2,"title":"云霄县领导","start":"~2026","end":"present","rank":"副处","note":"参与云陵调研"},

    # ── 方成江 ──
    {"id":18,"person_id":15,"org_id":2,"title":"云霄县领导","start":"~2026","end":"present","rank":"副处","note":"参与云陵调研"},

    # ── 王荷明 ──
    {"id":19,"person_id":16,"org_id":2,"title":"云霄县领导","start":"~2026","end":"present","rank":"副处","note":"参与莆美/云陵调研"},

    # ── 吴兰波 ──
    {"id":20,"person_id":17,"org_id":2,"title":"云霄县副县长","start":"~2025","end":"present","rank":"副处","note":"现任; 分管商贸/电商"},

    # ── 陈顺国 ──
    {"id":21,"person_id":18,"org_id":5,"title":"常山开发区管委会常务副主任","start":"~2025","end":"present","rank":"正处","note":"现任"},

    # ── 林靖 ──
    {"id":22,"person_id":19,"org_id":5,"title":"常山开发区管委会副主任","start":"~2024","end":"present","rank":"副处","note":"现任"},

    # ── 蓝良木 (predecessor) ──
    {"id":23,"person_id":20,"org_id":1,"title":"云霄县委书记、常山开发区党工委书记","start":"~2022","end":"~2026-06","rank":"正处","note":"前职; 具体任期待核实"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 杨志滨 ←→ 孙可 (党政搭档, 2026-至今)
    {"id":1,"person_a":1,"person_b":2,"type":"overlap","context":"云霄县委书记-代县长党政搭档","overlap_org":"中共云霄县委员会/云霄县人民政府","overlap_period":"2026-至今"},
    # 蓝良木 → 杨志滨 (县委书记交接)
    {"id":2,"person_a":20,"person_b":1,"type":"predecessor_successor","context":"蓝良木→杨志滨 云霄县委书记交接","overlap_org":"中共云霄县委员会","overlap_period":"~2026-06"},
    # 杨志滨 → 孙可 (县长/代县长交接)
    {"id":3,"person_a":1,"person_b":2,"type":"predecessor_successor","context":"杨志滨升书记后、孙可接任代县长","overlap_org":"云霄县人民政府","overlap_period":"~2026-06"},
    # 杨志滨兼任常山开发区 (书记/主任/党工委书记)
    {"id":4,"person_a":1,"person_b":18,"type":"overlap","context":"杨志滨与陈顺国 常山开发区党工委/管委会搭档","overlap_org":"常山开发区管委会","overlap_period":"2026-至今"},
    # 汤永坚 与 吴兰波 (政府班子同僚)
    {"id":5,"person_a":11,"person_b":17,"type":"overlap","context":"云霄县政府班子同僚","overlap_org":"云霄县人民政府","overlap_period":"2025-至今"},
    # 洪逸峰频繁陪同调研 (县委办)
    {"id":6,"person_a":9,"person_b":1,"type":"overlap","context":"洪逸峰频繁陪同县委书记调研","overlap_org":"中共云霄县委员会","overlap_period":"2026-至今"},
    # 林贵达陪同安全生产督导
    {"id":7,"person_a":6,"person_b":1,"type":"overlap","context":"林贵达陪同县委书记安全生产督导","overlap_org":"云霄县人民政府","overlap_period":"2026"},
    # 黄文疆 与 林意纯 (人大政协)
    {"id":8,"person_a":3,"person_b":4,"type":"overlap","context":"县人大主任-县政协主席同届","overlap_org":"云霄县","overlap_period":"~2025-至今"},
    # 郑雯雯 与 沈生辉 (政法/宣传)
    {"id":9,"person_a":7,"person_b":8,"type":"overlap","context":"共同参与政法委宣传部调研","overlap_org":"中共云霄县委员会","overlap_period":"2026"},
]

# =========================================================================
# SQLITE DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT,
        source TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                      p["education"],p["party_join"],p["work_start"],p["current_post"],
                      p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for ps in positions:
        cur.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                     (ps["id"],ps["person_id"],ps["org_id"],ps["title"],ps["start"],ps["end"],ps["rank"],ps["note"]))
    for r in relationships:
        cur.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                     (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")

# =========================================================================
# GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return 'r,g,b' string based on person's role."""
    post = p.get("current_post","")
    if "书记" in post and "纪委" not in post and "人大" not in post and "政协" not in post:
        return "255,50,50"     # Red: Party Secretary
    if "县长" in post or "代县长" in post:
        return "50,100,255"    # Blue: Government head
    if "纪委" in post or "监委" in post:
        return "255,165,0"     # Orange: Discipline
    if "人大" in post:
        return "200,255,255"   # Cyan: People's Congress
    if "政协" in post:
        return "255,240,200"   # Cream: Political Consultative
    if "副县长" in post:
        return "50,100,255"    # Blue: Deputy mayor
    return "100,100,100"       # Grey: Others

def is_top_leader(p):
    return p["id"] in [1, 2]  # 杨志滨 and 孙可

def org_color(o):
    t = o.get("type","")
    m = {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200",
         "乡镇/街道":"255,255,200","事业单位":"220,220,220","群团":"255,220,255",
         "人大":"200,255,255","政协":"255,240,200"}
    return m.get(t,"200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>云霄县领导工作关系网络 - Yunxiao County Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="subtype" type="string"/>')
    lines.append('      <attribute id="2" title="job_title" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="birth" type="string"/>')
    lines.append('      <attribute id="5" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"][:20])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="3" value="县级"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birthplace"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person → Organization edges (worked_at)
    for ps in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{ps["person_id"]}" target="o{ps["org_id"]}" label="{esc(ps["title"][:30])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ps["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(ps["start"])}-{esc(ps["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring("\n".join(lines))
        print("    XML well-formed: OK")
    except Exception as e:
        print(f"    XML validation: {e}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("Building 云霄县 leadership network...")
    build_db()
    build_gexf()
    print("Done.")
