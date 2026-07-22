#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海沧区 (Haicang District, Xiamen, Fujian).

海沧区 — 厦门市下辖区，全国设立最早、面积最大的台商投资区。

Research date: 2026-07-16
Sources:
- 海沧区政府网站 (www.haicang.gov.cn) — 领导活动报道
- 网易/新浪/腾讯新闻 — 干部任免报道
- 百度百科 — 龚建阳履历
- 人民网 — 干部任免公示
- 厦门日报 — 新闻报道
- 厦门市纪委监委网站 — 纪委全会报道

Coverage: 区委/区政府/区人大/区政协主要领导，
前任书记去向，区委常委班子主要成员。

Confidence notes:
- 龚建阳、黄鹤麟、游文昌身份与履历：confirmed（多源交叉验证）
- 吴申宇、陈仲谋、邓英志、许永良、黄炳文身份：confirmed（官方活动报道）
- 各人教育经历、具体时间节点：部分已确认，部分为plausible
- 街道层面领导：未纳入本版本（scope为区级班子）
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_海沧区")
DB_PATH = os.path.join(STAGING, "海沧区_network.db")
GEXF_PATH = os.path.join(STAGING, "海沧区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 龚建阳 — 海沧区委书记 (as of 2024.07)
    {"id":1,"name":"龚建阳","gender":"男","ethnicity":"汉族",
     "birth":"1968-07","birthplace":"福建莆田","education":"在职研究生，经济学硕士",
     "party_join":"中共党员","work_start":"1992-07",
     "current_post":"海沧台商投资区党工委书记、海沧区委书记",
     "current_org":"中共海沧区委",
     "source":"网易/新浪/人民网 — 福建两位厅级干部履新(2024-07-30)"},
    # 黄鹤麟 — 海沧区区长 (as of 2024.07)
    {"id":2,"name":"黄鹤麟","gender":"男","ethnicity":"汉族",
     "birth":"1970-05","birthplace":"福建福州(出生地松溪)","education":"省委党校研究生，公共管理硕士",
     "party_join":"中共党员","work_start":"1991-08",
     "current_post":"海沧台商投资区管委会主任、海沧区区长",
     "current_org":"海沧区人民政府",
     "source":"新浪网/人民网 — 福建两位厅级干部履新(2024-07-30); 中国经济网(2021-07)"},
    # 许永良 — 海沧区人大常委会主任 (as of 2024.12)
    {"id":3,"name":"许永良","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧区人大常委会主任",
     "current_org":"海沧区人大常委会",
     "source":"海沧区政府网站 — 两会日程报道(2024-12); 厦门人大网"},
    # 黄炳文 — 海沧区政协主席 (as of 2026.02)
    {"id":4,"name":"黄炳文","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧区政协主席",
     "current_org":"政协海沧区委员会",
     "source":"厦门市纪委监委 — 海沧区纪委五届六次全会报道(2026-02-12)"},

    # ── 2. Predecessors — 区委书记 ──
    # 游文昌 — 原海沧区委书记 (2018-2024)，现厦门市委政法委书记
    {"id":5,"name":"游文昌","gender":"男","ethnicity":"汉族",
     "birth":"1968-02","birthplace":"福建龙岩","education":"在职研究生，经济学硕士",
     "party_join":"中共党员","work_start":"",
     "current_post":"厦门市委常委、政法委书记",
     "current_org":"中共厦门市委政法委",
     "source":"人民网/网易 — 游文昌任厦门市委政法委书记(2024-08)"},
    # 连维兴 — 原海沧区委副书记，现湖里区人大常委会主任
    {"id":6,"name":"连维兴","gender":"男","ethnicity":"汉族",
     "birth":"1972-06","birthplace":"","education":"中央党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"湖里区人大常委会主任",
     "current_org":"湖里区人大常委会",
     "source":"鲁中晨报/鲁网(2023-11-20); 网易(2023-12-30)"},

    # ── 3. Current deputy leaders (常委) ──
    # 吴申宇 — 海沧区委副书记、海沧台商投资区管委会副主任
    {"id":7,"name":"吴申宇","gender":"男","ethnicity":"汉族",
     "birth":"1977-07","birthplace":"福建厦门","education":"中央党校研究生",
     "party_join":"中共党员","work_start":"1996-08",
     "current_post":"海沧区委副书记、海沧台商投资区管委会副主任",
     "current_org":"中共海沧区委",
     "source":"腾讯网(2022-02-21); 人民网(2023-12-16); 海沧区政府网站"},
    # 陈仲谋 — 海沧区委常委、常务副区长
    {"id":8,"name":"陈仲谋","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧区委常委、区政府常务副区长",
     "current_org":"海沧区人民政府",
     "source":"海沧区政府网站; 腾讯新闻发布会报道(2025-12-18)"},
    # 邓英志 — 海沧区纪委书记、监委主任
    {"id":9,"name":"邓英志","gender":"","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧台商投资区纪工委书记、区纪委书记、区监委主任",
     "current_org":"中共海沧区纪委",
     "source":"厦门市纪委监委 — 海沧区纪委五届六次全会报道(2026-02-12)"},

    # ── 4. 区政府副区长（部分，从公开活动获取）──
    {"id":10,"name":"彭延敏","gender":"","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧区副区长",
     "current_org":"海沧区人民政府",
     "source":"中国日报网 — 海沧区发布会(2025-12-19)"},
    {"id":11,"name":"眭国瑜","gender":"","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧台商投资区管委会副主任",
     "current_org":"海沧台商投资区管委会",
     "source":"人民网(2023-12-16); 腾讯新闻(2025-12-18)"},
    {"id":12,"name":"黄书枚","gender":"","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧区副区长",
     "current_org":"海沧区人民政府",
     "source":"海沧区政府网站 — 领导活动报道(2024-12-31)"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共海沧区委","type":"党委","level":"县处级","parent":"中共厦门市委","location":"厦门市海沧区"},
    {"id":2,"name":"海沧区人民政府","type":"政府","level":"县处级","parent":"厦门市人民政府","location":"厦门市海沧区"},
    {"id":3,"name":"海沧区人大常委会","type":"人大","level":"县处级","parent":"厦门市人大常委会","location":"厦门市海沧区"},
    {"id":4,"name":"政协海沧区委员会","type":"政协","level":"县处级","parent":"政协厦门市委员会","location":"厦门市海沧区"},
    {"id":5,"name":"中共海沧区纪委","type":"党委","level":"县处级","parent":"中共厦门市纪委","location":"厦门市海沧区"},
    {"id":6,"name":"海沧台商投资区管委会","type":"开发区","level":"副厅级","parent":"厦门市人民政府","location":"厦门市海沧区"},
    {"id":7,"name":"中共厦门市委政法委","type":"党委","level":"副省级","parent":"中共厦门市委","location":"厦门市"},
    {"id":8,"name":"湖里区人大常委会","type":"人大","level":"县处级","parent":"厦门市人大常委会","location":"厦门市湖里区"},
    {"id":9,"name":"中共翔安区委","type":"党委","level":"县处级","parent":"中共厦门市委","location":"厦门市翔安区"},
    {"id":10,"name":"政协三明市委员会","type":"政协","level":"地厅级","parent":"政协福建省委员会","location":"三明市"},
    {"id":11,"name":"中共湖里区委","type":"党委","level":"县处级","parent":"中共厦门市委","location":"厦门市湖里区"},
    {"id":12,"name":"厦门市自然资源和规划局","type":"政府","level":"副厅级","parent":"厦门市人民政府","location":"厦门市"},
    {"id":13,"name":"厦门市市政园林局","type":"政府","level":"副厅级","parent":"厦门市人民政府","location":"厦门市"},
    {"id":14,"name":"厦门市交通运输局","type":"政府","level":"副厅级","parent":"厦门市人民政府","location":"厦门市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 龚建阳 ──
    {"person_id":1,"org_id":1,"title":"海沧台商投资区党工委书记、海沧区委书记","start":"2024-07","end":"present","rank":"正厅级","note":"厦门市委常委"},
    {"person_id":1,"org_id":2,"title":"海沧区区长","start":"2021","end":"2024-07","rank":"正厅级","note":"此前任海沧台商投资区管委会主任"},
    {"person_id":1,"org_id":11,"title":"湖里区委书记","start":"2020","end":"2021","rank":"副厅级","note":""},
    {"person_id":1,"org_id":12,"title":"厦门市自然资源和规划局党组书记、局长","start":"","end":"2020","rank":"副厅级","note":""},
    {"person_id":1,"org_id":13,"title":"厦门市市政园林局党组书记、局长","start":"","end":"","rank":"副厅级","note":""},
    {"person_id":1,"org_id":14,"title":"厦门市交通运输局副局长","start":"","end":"","rank":"副厅级","note":""},

    # ── 黄鹤麟 ──
    {"person_id":2,"org_id":2,"title":"海沧台商投资区管委会主任、海沧区区长","start":"2024-07","end":"present","rank":"正厅级","note":""},
    {"person_id":2,"org_id":9,"title":"翔安区委书记","start":"2021-07","end":"2024-07","rank":"正厅级","note":"正厅长级"},
    {"person_id":2,"org_id":10,"title":"三明市政协主席、党组书记","start":"2020-01","end":"2021-07","rank":"正厅级","note":""},
    {"person_id":2,"org_id":1,"title":"福建省第七批援疆工作队领队（挂职昌吉州党委副书记）","start":"2017-02","end":"2020-01","rank":"厅级","note":""},
    {"person_id":2,"org_id":1,"title":"厦门市委宣传部副部长、市委文明办主任","start":"2012","end":"2017-02","rank":"副厅级","note":"兼市红十字会副会长"},
    {"person_id":2,"org_id":1,"title":"共青团厦门市委书记","start":"","end":"2012","rank":"正处级","note":""},
    {"person_id":2,"org_id":1,"title":"共青团厦门市委副书记","start":"","end":"","rank":"副处级","note":""},

    # ── 许永良 ──
    {"person_id":3,"org_id":3,"title":"海沧区人大常委会主任","start":"2024-12","end":"present","rank":"正处级","note":"2024年12月区十三届人大六次会议当选"},
    {"person_id":3,"org_id":3,"title":"海沧区人大常委会党组书记","start":"","end":"present","rank":"正处级","note":""},

    # ── 黄炳文 ──
    {"person_id":4,"org_id":4,"title":"海沧区政协主席","start":"","end":"present","rank":"正处级","note":""},

    # ── 游文昌 ──
    {"person_id":5,"org_id":7,"title":"厦门市委常委、政法委书记","start":"2024-08","end":"present","rank":"副省级","note":""},
    {"person_id":5,"org_id":1,"title":"海沧台商投资区党工委书记、海沧区委书记","start":"2018","end":"2024-07","rank":"正厅级","note":"厦门市委常委"},
    {"person_id":5,"org_id":2,"title":"海沧区代区长","start":"2018","end":"","rank":"正厅级","note":""},
    {"person_id":5,"org_id":1,"title":"思明区委书记","start":"","end":"2018","rank":"副厅级","note":""},
    {"person_id":5,"org_id":1,"title":"翔安区委副书记、副区长","start":"","end":"","rank":"副厅级","note":""},
    {"person_id":5,"org_id":1,"title":"厦门火炬高技术产业开发区党工委书记、管委会常务副主任","start":"","end":"","rank":"副厅级","note":""},

    # ── 连维兴 ──
    {"person_id":6,"org_id":8,"title":"湖里区人大常委会主任","start":"2023-11","end":"present","rank":"正处级","note":""},
    {"person_id":6,"org_id":1,"title":"海沧区委副书记","start":"2021","end":"2023-11","rank":"副处级","note":""},
    {"person_id":6,"org_id":2,"title":"海沧区副区长","start":"2017","end":"2021","rank":"副处级","note":""},
    {"person_id":6,"org_id":1,"title":"厦门市教育局办公室主任","start":"","end":"2017","rank":"正科级","note":""},

    # ── 吴申宇 ──
    {"person_id":7,"org_id":1,"title":"海沧区委副书记、海沧台商投资区管委会副主任","start":"2023-10","end":"present","rank":"副厅级","note":""},
    {"person_id":7,"org_id":2,"title":"思明区委常委、政法委书记","start":"","end":"2023","rank":"副厅级","note":""},
    {"person_id":7,"org_id":2,"title":"思明区副区长","start":"","end":"","rank":"副厅级","note":""},
    {"person_id":7,"org_id":1,"title":"共青团厦门市委书记","start":"","end":"","rank":"正处级","note":""},
    {"person_id":7,"org_id":1,"title":"共青团厦门市委副书记","start":"","end":"","rank":"副处级","note":""},
    {"person_id":7,"org_id":1,"title":"厦门市同安区洪塘镇党委副书记、镇长","start":"","end":"","rank":"正科级","note":""},
    {"person_id":7,"org_id":1,"title":"共青团厦门市同安区委书记","start":"","end":"","rank":"正科级","note":""},
    {"person_id":7,"org_id":1,"title":"共青团厦门市同安区委副书记","start":"","end":"","rank":"副科级","note":""},

    # ── 陈仲谋 ──
    {"person_id":8,"org_id":2,"title":"海沧区委常委、区政府常务副区长","start":"2021","end":"present","rank":"副厅级","note":""},
    {"person_id":8,"org_id":11,"title":"湖里区副区长","start":"","end":"2021","rank":"副厅级","note":""},

    # ── 邓英志 ──
    {"person_id":9,"org_id":5,"title":"海沧台商投资区纪工委书记、区纪委书记、区监委主任","start":"","end":"present","rank":"副厅级","note":""},

    # ── 副区长 ──
    {"person_id":10,"org_id":2,"title":"海沧区副区长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":11,"org_id":6,"title":"海沧台商投资区管委会副主任","start":"2023-10","end":"present","rank":"副厅级","note":"试用期一年(2023)"},
    {"person_id":12,"org_id":2,"title":"海沧区副区长","start":"","end":"present","rank":"副处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 龚建阳 ← 游文昌 (predecessor-successor, 区委书记)
    {"person_a":5,"person_b":1,"type":"predecessor_successor","context":"游文昌2018-2024年任海沧区委书记，龚建阳2024年7月接任","overlap_org":"中共海沧区委","overlap_period":"2024-07交接"},
    # 龚建阳 ← 黄鹤麟 (predecessor-successor, 区长)
    {"person_a":1,"person_b":2,"type":"predecessor_successor","context":"龚建阳2021-2024年任海沧区区长，黄鹤麟2024年7月接任","overlap_org":"海沧区人民政府","overlap_period":"2024-07交接"},
    # 龚建阳 → 连维兴 (搭档)
    {"person_a":1,"person_b":6,"type":"overlap","context":"龚建阳担任海沧区长期间，连维兴任海沧区委副书记(2021-2023年)","overlap_org":"中共海沧区委/海沧区人民政府","overlap_period":"2021-2023"},
    # 游文昌 → 龚建阳 (上下级，游文昌为书记，龚建阳为区长)
    {"person_a":5,"person_b":1,"type":"superior_subordinate","context":"游文昌任海沧区委书记期间，龚建阳任海沧区区长","overlap_org":"中共海沧区委/海沧区人民政府","overlap_period":"2021-2024"},
    # 陈仲谋 → 龚建阳 (上下级，曾在湖里区先后工作)
    {"person_a":8,"person_b":1,"type":"superior_subordinate","context":"龚建阳2020-2021年任湖里区委书记，陈仲谋此前曾任湖里区副区长","overlap_org":"中共湖里区委/湖里区人民政府","overlap_period":"2020-2021"},
    # 吴申宇 → 龚建阳、黄鹤麟 (当前班子)
    {"person_a":7,"person_b":1,"type":"overlap","context":"吴申宇任海沧区委副书记，龚建阳任区委书记，为当前班子搭档","overlap_org":"中共海沧区委","overlap_period":"2023-至今"},
    {"person_a":7,"person_b":2,"type":"overlap","context":"吴申宇任海沧区委副书记并兼管台港澳事务，黄鹤麟任区长","overlap_org":"中共海沧区委/海沧区人民政府","overlap_period":"2024-至今"},
    # 黄鹤麟 — 游文昌（无直接重叠，但关联翔安、海沧两区）
    # 陈仲谋 — 连维兴（湖里-海沧两区跨区任职）
]

# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")


# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_role_color(name, current_post):
    """Determine color based on person's role."""
    if "书记" in current_post and "纪委" not in current_post and "副书记" not in current_post:
        return "255,50,50"   # Red — Party Secretary
    if "区长" in current_post or "市长" in current_post or "县长" in current_post:
        return "50,100,255"  # Blue — Government head
    if "主任" in current_post and "管委会" not in current_post:
        return "200,255,255" # Cyan —人大
    if "主席" in current_post and "政协" in current_post:
        return "255,240,200" # Cream —政协
    if "纪委书记" in current_post or "纪工委" in current_post:
        return "255,165,0"   # Orange — Discipline
    if "副书记" in current_post:
        return "180,80,80"   # Dark red — Deputy Secretary
    if "常务副" in current_post or "副区长" in current_post or "副主任" in current_post:
        return "100,100,200" # Blue-grey — Deputies
    return "100,100,100"     # Grey — Others

def is_top_leader(name, current_post):
    if "书记" in current_post and "纪委" not in current_post and "副书记" not in current_post:
        return True
    if "区长" in current_post and "副" not in current_post:
        return True
    return False

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,220,200",
    }
    return colors.get(org_type, "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>OpenCode Research Agent (gov-relation project)</creator>')
    lines.append('    <description>海沧区领导班子工作关系网络 — 厦门市海沧区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_role_color(p["name"], p["current_post"])
        sz = "20.0" if is_top_leader(p["name"], p["current_post"]) else "12.0"
        role = p["current_post"]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        start = pos["start"] if pos["start"] else "unknown"
        end = pos["end"] if pos["end"] else "unknown"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"Building 海沧区 leadership network data...")
    print(f"Research as of: {AS_OF}")
    print()
    build_database()
    print()
    build_gexf()
    print()
    print("Done. Summary:")
    print(f"  - {len(persons)} persons")
    print(f"  - {len(organizations)} organizations")
    print(f"  - {len(positions)} positions")
    print(f"  - {len(relationships)} relationships (person↔person)")
