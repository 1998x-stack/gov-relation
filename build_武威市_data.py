#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 武威市 (Wuwei City, Gansu) leadership network.

武威市 — 甘肃省地级市, 河西走廊门户.
Covers current Party Secretary (武和谦), Mayor (叶万彬), their predecessors,
key diyi leadership, and relationship network.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_武威市")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "武威市_network.db")
GEXF_PATH = os.path.join(STAGING, "武威市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. City-level top leadership (current) ──

    # 武和谦 — 武威市委书记 (as of 2026.06)
    {"id":1,"name":"武和谦","gender":"男","ethnicity":"汉族",
     "birth":"1971-01","birthplace":"甘肃白银",
     "education":"长安大学（原西安公路交通大学）研究生，工学硕士",
     "party_join":"中共党员","work_start":"1990-07",
     "current_post":"武威市委书记",
     "current_org":"中共武威市委员会",
     "source":"https://baike.baidu.com/item/%E6%AD%A6%E5%92%8C%E8%B0%A6/14902180"},

    # 叶万彬 — 武威市市长 (as of 2025.08)
    {"id":2,"name":"叶万彬","gender":"男","ethnicity":"藏族",
     "birth":"1977-05","birthplace":"青海乐都",
     "education":"青海省委党校研究生",
     "party_join":"2001-11","work_start":"1996-07",
     "current_post":"武威市人民政府市长",
     "current_org":"武威市人民政府",
     "source":"https://baike.baidu.com/item/%E5%8F%B6%E4%B8%87%E5%BD%AC"},

    # 曾国俊 — 武威市人大常委会主任 (as of 2024.01)
    {"id":3,"name":"曾国俊","gender":"男","ethnicity":"汉族",
     "birth":"1968-03","birthplace":"甘肃景泰",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"武威市人大常委会主任",
     "current_org":"武威市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E6%AD%A6%E5%A8%81%E5%B8%82"},

    # 李宏伟 — 武威市政协主席 (as of 2024.01)
    {"id":4,"name":"李宏伟","gender":"男","ethnicity":"汉族",
     "birth":"1966-10","birthplace":"甘肃张掖",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"武威市政协主席",
     "current_org":"武威市政协",
     "source":"https://zh.wikipedia.org/wiki/%E6%AD%A6%E5%A8%81%E5%B8%82"},

    # ── B. Predecessors — 市委书记 ──

    # 王国斌 — 前任市委书记 (2023.03-2026.06), 现任临夏州委书记
    {"id":5,"name":"王国斌","gender":"男","ethnicity":"汉族",
     "birth":"1972-07","birthplace":"甘肃清水",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"临夏州委书记（原武威市委书记）",
     "current_org":"中共临夏回族自治州委员会",
     "source":"https://baike.baidu.com/item/%E7%8E%8B%E5%9B%BD%E6%96%8C/63406778"},

    # 柳鹏 — 前任市委书记 (2017.04-2023.03), 现任甘肃省发改委主任
    {"id":6,"name":"柳鹏","gender":"男","ethnicity":"汉族",
     "birth":"1971-11","birthplace":"甘肃兰州",
     "education":"中央党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"甘肃省发改委主任（原武威市委书记）",
     "current_org":"甘肃省发展和改革委员会",
     "source":"https://zh.wikipedia.org/wiki/%E6%9F%B3%E9%B9%8F"},

    # 火荣贵 — 前任市委书记 (2010.01-2017.04), 落马
    {"id":7,"name":"火荣贵","gender":"男","ethnicity":"汉族",
     "birth":"1962-10","birthplace":"甘肃景泰",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原武威市委书记（2019年因严重违纪被双开，判刑18年）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E7%81%AB%E8%8D%A3%E8%B4%B5"},

    # 肖庆平 — 前任市委书记 (2008.05-2010.01)
    {"id":8,"name":"肖庆平","gender":"男","ethnicity":"汉族",
     "birth":"1956-03","birthplace":"甘肃文县",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"已退休（原甘肃省民政厅厅长）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E8%82%96%E5%BA%86%E5%B9%B3"},

    # ── C. Predecessors — 市长 ──

    # 马秀兰 — 前任市长 (2023.04-2025.07), 现任宁夏中卫市长
    {"id":9,"name":"马秀兰","gender":"女","ethnicity":"回族",
     "birth":"1974-03","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"宁夏中卫市委副书记、市长（原武威市长）",
     "current_org":"中卫市人民政府",
     "source":"https://baike.baidu.com/item/%E9%A9%AC%E7%A7%80%E5%85%B0/57748078"},

    # 周伟 — 前任市长 (2018.07-2021.08)
    {"id":10,"name":"周伟","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"甘肃岷县",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原武威市长",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E6%AD%A6%E5%A8%81%E5%B8%82"},

    # 郭承录 — 前任市长 (2008.05-2011.09), 后任甘肃省政协副主席
    {"id":11,"name":"郭承录","gender":"男","ethnicity":"汉族",
     "birth":"1962-08","birthplace":"甘肃永昌",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"已退休（原甘肃省政协副主席、平凉市委书记）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%83%AD%E6%89%BF%E5%BD%95"},

    # 李明生 — 前任市长 (2016.05-2018.07), 2023年退休
    {"id":12,"name":"李明生","gender":"男","ethnicity":"汉族",
     "birth":"1963-01","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"已退休（原甘肃省农业农村厅副厅长）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%98%8E%E7%94%9F_(1963%E5%B9%B4)"},

    # 张绪胜 — 首任市委书记 (2001.04-2008.05)
    {"id":13,"name":"张绪胜","gender":"男","ethnicity":"汉族",
     "birth":"1954-07","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"已退休（原甘肃省人大常委会秘书长）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E7%BB%AA%E8%83%9C"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 武威市级核心
    {"id":1,"name":"中共武威市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省武威市凉州区"},
    {"id":2,"name":"武威市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省武威市凉州区"},
    {"id":3,"name":"武威市人大常委会","type":"人大","level":"地级","parent":"甘肃省人大常委会","location":"甘肃省武威市凉州区"},
    {"id":4,"name":"武威市政协","type":"政协","level":"地级","parent":"政协甘肃省委员会","location":"甘肃省武威市凉州区"},
    {"id":5,"name":"中共武威市纪律检查委员会","type":"党委","level":"地级","parent":"中共武威市委员会","location":"甘肃省武威市凉州区"},

    # 上级
    {"id":6,"name":"中共甘肃省委员会","type":"党委","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":7,"name":"甘肃省人民政府","type":"政府","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":8,"name":"甘肃省人大常委会","type":"人大","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":9,"name":"政协甘肃省委员会","type":"政协","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":10,"name":"甘肃省发展和改革委员会","type":"政府","level":"省级","parent":"甘肃省人民政府","location":"甘肃省兰州市"},

    # 调任去向
    {"id":11,"name":"中共临夏回族自治州委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省临夏市"},
    {"id":12,"name":"中共白银市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省白银市"},
    {"id":13,"name":"中共平凉市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省平凉市"},
    {"id":14,"name":"中卫市人民政府","type":"政府","level":"地级","parent":"宁夏回族自治区人民政府","location":"宁夏中卫市"},
    {"id":15,"name":"甘肃省交通运输厅","type":"政府","level":"省级","parent":"甘肃省人民政府","location":"甘肃省兰州市"},
]

# =========================================================================
# POSITIONS (career timeline edges)
# =========================================================================
positions = [
    # 武和谦 — 书记
    {"id":1,"person_id":1,"org_id":1,"title":"武威市委书记","start":"2026-06","end":"present","rank":"正厅级","note":""},
    {"id":2,"person_id":1,"org_id":6,"title":"定西市委副书记、市长","start":"2023-04","end":"2026-06","rank":"正厅级","note":"调任武威市委书记"},
    {"id":3,"person_id":1,"org_id":7,"title":"张掖市委常委、常务副市长","start":"","end":"2023-04","rank":"副厅级","note":"此前在兰州市任职"},
    {"id":4,"person_id":1,"org_id":8,"title":"兰州市副市长","start":"","end":"","rank":"副厅级","note":""},
    {"id":5,"person_id":1,"org_id":9,"title":"兰州市城关区委书记","start":"","end":"","rank":"正县级","note":""},

    # 叶万彬 — 市长
    {"id":10,"person_id":2,"org_id":2,"title":"武威市人民政府市长","start":"2025-08","end":"present","rank":"正厅级","note":"跨省调任（青海→甘肃）"},
    {"id":11,"person_id":2,"org_id":10,"title":"果洛藏族自治州委副书记、州长","start":"2021-04","end":"2025-07","rank":"正厅级","note":"青海省"},
    {"id":12,"person_id":2,"org_id":11,"title":"海南藏族自治州委常委、副州长","start":"","end":"2021-03","rank":"副厅级","note":"青海省"},

    # 曾国俊 — 人大主任
    {"id":20,"person_id":3,"org_id":3,"title":"武威市人大常委会主任","start":"2024-01","end":"present","rank":"正厅级","note":""},

    # 李宏伟 — 政协主席
    {"id":30,"person_id":4,"org_id":4,"title":"武威市政协主席","start":"2024-01","end":"present","rank":"正厅级","note":""},

    # 王国斌 — 前任书记
    {"id":40,"person_id":5,"org_id":11,"title":"临夏州委书记","start":"2026-06","end":"present","rank":"正厅级","note":""},
    {"id":41,"person_id":5,"org_id":1,"title":"武威市委书记","start":"2023-03","end":"2026-06","rank":"正厅级","note":""},
    {"id":42,"person_id":5,"org_id":2,"title":"武威市人民政府市长","start":"2021-08","end":"2023-04","rank":"正厅级","note":"后任书记"},

    # 柳鹏 — 前任书记
    {"id":50,"person_id":6,"org_id":10,"title":"甘肃省发改委主任","start":"2026-03","end":"present","rank":"正厅级","note":""},
    {"id":51,"person_id":6,"org_id":15,"title":"甘肃省交通运输厅厅长","start":"2023-03","end":"2026-03","rank":"正厅级","note":""},
    {"id":52,"person_id":6,"org_id":1,"title":"武威市委书记","start":"2017-04","end":"2023-03","rank":"正厅级","note":""},
    {"id":53,"person_id":6,"org_id":13,"title":"嘉峪关市委书记","start":"2016-08","end":"2017-04","rank":"正厅级","note":""},

    # 火荣贵 — 前任书记（落马）
    {"id":60,"person_id":7,"org_id":1,"title":"武威市委书记","start":"2010-01","end":"2017-04","rank":"正厅级","note":"2019年因严重违纪被双开，判刑18年"},

    # 肖庆平 — 前任书记
    {"id":70,"person_id":8,"org_id":12,"title":"白银市委书记","start":"2010-01","end":"","rank":"正厅级","note":""},
    {"id":71,"person_id":8,"org_id":1,"title":"武威市委书记","start":"2008-05","end":"2010-01","rank":"正厅级","note":""},
    {"id":72,"person_id":8,"org_id":2,"title":"武威市人民政府市长","start":"2006-07","end":"2008-05","rank":"正厅级","note":"升任书记"},

    # 马秀兰 — 前任市长
    {"id":80,"person_id":9,"org_id":14,"title":"宁夏中卫市委副书记、市长","start":"2025-07","end":"present","rank":"正厅级","note":"跨省调任"},
    {"id":81,"person_id":9,"org_id":2,"title":"武威市人民政府市长","start":"2023-04","end":"2025-07","rank":"正厅级","note":""},

    # 郭承录 — 前任市长
    {"id":90,"person_id":11,"org_id":13,"title":"平凉市委书记","start":"2017","end":"2018","rank":"正厅级","note":""},
    {"id":91,"person_id":11,"org_id":2,"title":"武威市人民政府市长","start":"2008-05","end":"2011-09","rank":"正厅级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 武和谦 ← → 叶万彬: 党政一把手
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate",
     "context":"武和谦（书记）与叶万彬（市长）为党政一把手搭档",
     "overlap_org":"中共武威市委员会","overlap_period":"2026-06至今"},

    # 武和谦 ← → 王国斌: 书记交接
    {"id":2,"person_a":1,"person_b":5,"type":"predecessor_successor",
     "context":"王国斌→武和谦: 王国斌2026年6月转任临夏州委书记, 武和谦任武威市委书记",
     "overlap_org":"中共武威市委员会","overlap_period":"2026-06"},

    # 王国斌 ← → 柳鹏: 书记交接
    {"id":3,"person_a":5,"person_b":6,"type":"predecessor_successor",
     "context":"柳鹏→王国斌: 柳鹏2023年3月转任省交通厅长, 王国斌由市长接任书记",
     "overlap_org":"中共武威市委员会","overlap_period":"2023-03"},

    # 叶万彬 ← → 马秀兰: 市长交接
    {"id":4,"person_a":2,"person_b":9,"type":"predecessor_successor",
     "context":"马秀兰→叶万彬: 马秀兰2025年7月跨省调任宁夏中卫市长, 叶万彬跨省调任武威市长",
     "overlap_org":"武威市人民政府","overlap_period":"2025-07"},

    # 王国斌自任市长转书记
    {"id":5,"person_a":5,"person_b":9,"type":"predecessor_successor",
     "context":"王国斌任市长(2021.8-2023.4)后升书记, 马秀兰接任市长",
     "overlap_org":"武威市人民政府","overlap_period":"2023-04"},

    # 柳鹏 ← → 火荣贵: 书记交接（政治生态转折）
    {"id":6,"person_a":6,"person_b":7,"type":"predecessor_successor",
     "context":"火荣贵→柳鹏: 火荣贵2017年4月落马被查, 柳鹏接任书记进行政治生态修复",
     "overlap_org":"中共武威市委员会","overlap_period":"2017-04"},

    # 肖庆平 ← 火荣贵: 书记交接
    {"id":7,"person_a":8,"person_b":7,"type":"predecessor_successor",
     "context":"肖庆平→火荣贵: 火荣贵2010年1月接任书记",
     "overlap_org":"中共武威市委员会","overlap_period":"2010-01"},

    # 郭承录 ← 王国斌: 武威市长→平凉/临夏（跨市升迁模式）
    {"id":8,"person_a":11,"person_b":5,"type":"same_system",
     "context":"郭承录（武威市长→平凉书记）与王国斌（武威市长→临夏书记）均为武威市长升迁至其他地市一把手",
     "overlap_org":"武威市人民政府","overlap_period":"跨时期"},

    # 肖庆平自任市长转书记
    {"id":9,"person_a":8,"person_b":11,"type":"predecessor_successor",
     "context":"肖庆平由市长升书记, 郭承录接任市长",
     "overlap_org":"武威市人民政府","overlap_period":"2008-05"},
]

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return color based on role."""
    role = p["current_post"]
    if "书记" in role and "纪委" not in role:
        return "255,50,50"    # Red — Party Secretary
    elif "市长" in role or "区长" in role or "县长" in role or "州长" in role:
        return "50,100,255"   # Blue — Government leader
    elif "纪委书记" in role or "纪委" in role:
        return "255,165,0"    # Orange — Discipline
    elif "人大" in role:
        return "200,255,255"  # Cyan — People's Congress
    elif "政协" in role:
        return "255,240,200"  # Cream — CPPCC
    else:
        return "100,100,100"  # Grey — Others

def is_top_leader(p):
    """Top leaders get larger node size."""
    return p["id"] in [1, 2, 3, 4, 5, 6, 7]  # 书记,市长,人大主任,政协主席,主要前任

def org_color(o):
    """Return color for organization nodes."""
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    else:
        return "200,200,200"

# =========================================================================
# BUILD DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],
                   p["birth"],p["birthplace"],p["education"],
                   p["party_join"],p["work_start"],
                   p["current_post"],p["current_org"],p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                  (pos["id"],pos["person_id"],pos["org_id"],
                   pos["title"],pos["start"],pos["end"],
                   pos["rank"],pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                  (r["id"],r["person_a"],r["person_b"],
                   r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent / github.com/gov-relation</creator>')
    lines.append('    <description>武威市（甘肃省地级市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
        lines.append('        </attvalues>')
        cr = c.split(",")
        lines.append(f'        <viz:color r="{cr[0]}" g="{cr[1]}" b="{cr[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        cr = c.split(",")
        lines.append(f'        <viz:color r="{cr[0]}" g="{cr[1]}" b="{cr[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person<->Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()

    # Stats
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons","organizations","positions","relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()
    print("Done.")
