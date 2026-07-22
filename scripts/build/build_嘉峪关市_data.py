#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 嘉峪关市 (Jiayuguan City, Gansu) leadership network.

嘉峪关市 — 甘肃省地级市 (不设区, 直筒子市).
Covers current Party Secretary (刘恩举), Mayor (王驰), their predecessors,
Standing Committee members, and government leadership team.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_嘉峪关市")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "嘉峪关市_network.db")
GEXF_PATH = os.path.join(STAGING, "嘉峪关市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Core leadership ──

    # 刘恩举 — 嘉峪关市委书记 (as of 2025.07)
    {"id":1,"name":"刘恩举","gender":"男","ethnicity":"汉族",
     "birth":"1973-05","birthplace":"辽宁辽阳",
     "education":"",  # 待查
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委书记",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E5%98%89%E5%B3%AA%E5%85%B3%E5%B8%82"},

    # 王驰 — 嘉峪关市市长 (as of 2026.02)
    {"id":2,"name":"王驰","gender":"男","ethnicity":"汉族",
     "birth":"1970-02","birthplace":"甘肃泾川",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委副书记、市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E5%98%89%E5%B3%AA%E5%85%B3%E5%B8%82"},

    # 赵宝毅 — 嘉峪关市人大常委会主任 (as of 2025.01)
    {"id":3,"name":"赵宝毅","gender":"男","ethnicity":"满族",
     "birth":"1969-05","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市人大常委会主任",
     "current_org":"嘉峪关市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E5%98%89%E5%B3%AA%E5%85%B3%E5%B8%82"},

    # 贾福祥 — 嘉峪关市政协主席 (as of 2026.05)
    {"id":4,"name":"贾福祥","gender":"男","ethnicity":"汉族",
     "birth":"1970-08","birthplace":"甘肃秦安",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市政协主席",
     "current_org":"政协嘉峪关市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E5%98%89%E5%B3%AA%E5%85%B3%E5%B8%82"},

    # 冯怡 — 嘉峪关市委副书记 (专职)
    {"id":5,"name":"冯怡","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委副书记",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 石峰 — 嘉峪关市委常委、常务副市长
    {"id":6,"name":"石峰","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委、常务副市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 程子建 — 嘉峪关市委常委 (酒钢集团董事长)
    {"id":7,"name":"程子建","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 韩宝成 — 嘉峪关市委常委
    {"id":8,"name":"韩宝成","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 王玉忠 — 嘉峪关市委常委、秘书长
    {"id":9,"name":"王玉忠","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委、秘书长",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 徐方明 — 嘉峪关市委常委、副市长
    {"id":10,"name":"徐方明","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委、副市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 李祥成 — 嘉峪关市委常委
    {"id":11,"name":"李祥成","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 马梅 — 嘉峪关市委常委
    {"id":12,"name":"马梅","gender":"女","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # 张辉 — 嘉峪关市委常委
    {"id":13,"name":"张辉","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"嘉峪关市委常委",
     "current_org":"中共嘉峪关市委员会",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # ── Other deputy mayors ──
    {"id":14,"name":"马元永","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"嘉峪关市副市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    {"id":15,"name":"周俊锋","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"嘉峪关市副市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    {"id":16,"name":"张莉","gender":"女","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"嘉峪关市副市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    {"id":17,"name":"赵淑敏","gender":"女","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"嘉峪关市副市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    {"id":18,"name":"张升元","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"嘉峪关市副市长",
     "current_org":"嘉峪关市人民政府",
     "source":"https://www.jyg.gov.cn/ldzc/"},

    # ── Predecessors ──
    # 刘永升 — 前任嘉峪关市委书记 (2021-2025)
    {"id":19,"name":"刘永升","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原嘉峪关市委书记",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%98%89%E5%B3%AA%E5%85%B3%E5%B8%82"},

    # 刘凯 — 前任嘉峪关市市长 (before 王驰)
    {"id":20,"name":"刘凯","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原嘉峪关市市长",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%98%89%E5%B3%AA%E5%85%B3%E5%B8%82"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共嘉峪关市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省嘉峪关市"},
    {"id":2,"name":"嘉峪关市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省嘉峪关市"},
    {"id":3,"name":"嘉峪关市人大常委会","type":"人大","level":"地级","parent":"甘肃省人大常委会","location":"甘肃省嘉峪关市"},
    {"id":4,"name":"政协嘉峪关市委员会","type":"政协","level":"地级","parent":"政协甘肃省委员会","location":"甘肃省嘉峪关市"},
    {"id":5,"name":"中共嘉峪关市纪律检查委员会","type":"纪委","level":"地级","parent":"中共嘉峪关市委员会","location":"甘肃省嘉峪关市"},
    {"id":6,"name":"酒泉钢铁（集团）有限责任公司","type":"事业单位","level":"地级","parent":"甘肃省人民政府","location":"甘肃省嘉峪关市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Core 四大班子
    {"person_id":1,"org_id":1,"title":"嘉峪关市委书记","start":"2025-07","end":"","rank":"正厅","note":"从辽宁省调任或省直机关调任"},
    {"person_id":2,"org_id":1,"title":"嘉峪关市委副书记","start":"","end":"","rank":"正厅","note":""},
    {"person_id":2,"org_id":2,"title":"嘉峪关市市长","start":"2026-02","end":"","rank":"正厅","note":"曾任代市长后转正"},
    {"person_id":3,"org_id":3,"title":"嘉峪关市人大常委会主任","start":"2025-01","end":"","rank":"正厅","note":""},
    {"person_id":4,"org_id":4,"title":"嘉峪关市政协主席","start":"2026-05","end":"","rank":"正厅","note":""},

    # 班子成员
    {"person_id":5,"org_id":1,"title":"嘉峪关市委副书记（专职）","start":"","end":"","rank":"正厅","note":""},
    {"person_id":6,"org_id":1,"title":"嘉峪关市委常委","start":"","end":"","rank":"副厅","note":""},
    {"person_id":6,"org_id":2,"title":"嘉峪关市委常委、常务副市长","start":"","end":"","rank":"副厅","note":""},
    {"person_id":7,"org_id":1,"title":"嘉峪关市委常委","start":"","end":"","rank":"副厅","note":"酒钢集团董事长"},
    {"person_id":8,"org_id":1,"title":"嘉峪关市委常委","start":"","end":"","rank":"副厅","note":""},
    {"person_id":9,"org_id":1,"title":"嘉峪关市委常委、秘书长","start":"","end":"","rank":"副厅","note":""},
    {"person_id":10,"org_id":1,"title":"嘉峪关市委常委","start":"","end":"","rank":"副厅","note":""},
    {"person_id":10,"org_id":2,"title":"嘉峪关市委常委、副市长","start":"","end":"","rank":"副厅","note":""},
    {"person_id":11,"org_id":1,"title":"嘉峪关市委常委","start":"","end":"","rank":"副厅","note":""},
    {"person_id":12,"org_id":1,"title":"嘉峪关市委常委","start":"","end":"","rank":"副厅","note":""},
    {"person_id":13,"org_id":1,"title":"嘉峪关市委常委","start":"","end":"","rank":"副厅","note":""},

    # 副市长
    {"person_id":14,"org_id":2,"title":"嘉峪关市副市长","start":"","end":"","rank":"副厅","note":""},
    {"person_id":15,"org_id":2,"title":"嘉峪关市副市长","start":"","end":"","rank":"副厅","note":""},
    {"person_id":16,"org_id":2,"title":"嘉峪关市副市长","start":"","end":"","rank":"副厅","note":""},
    {"person_id":17,"org_id":2,"title":"嘉峪关市副市长","start":"","end":"","rank":"副厅","note":""},
    {"person_id":18,"org_id":2,"title":"嘉峪关市副市长","start":"","end":"","rank":"副厅","note":""},

    # 前任
    {"person_id":19,"org_id":1,"title":"嘉峪关市委书记","start":"2021","end":"2025-07","rank":"正厅","note":"前任书记"},
    {"person_id":20,"org_id":2,"title":"嘉峪关市市长","start":"","end":"2026-02","rank":"正厅","note":"前任市长"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政搭档
    {"person_a":1,"person_b":2,"type":"党政同僚","context":"嘉峪关市委书记与市长搭档","overlap_org":"嘉峪关市","overlap_period":"2026-"},
    {"person_a":1,"person_b":3,"type":"党政同僚","context":"市委书记与人大主任","overlap_org":"嘉峪关市","overlap_period":"2025-"},
    {"person_a":1,"person_b":4,"type":"党政同僚","context":"市委书记与政协主席","overlap_org":"嘉峪关市","overlap_period":"2025-"},
    {"person_a":2,"person_b":3,"type":"党政同僚","context":"市长与人大主任","overlap_org":"嘉峪关市","overlap_period":"2025-"},
    {"person_a":2,"person_b":4,"type":"党政同僚","context":"市长与政协主席","overlap_org":"嘉峪关市","overlap_period":"2025-"},

    # 前后任
    {"person_a":1,"person_b":19,"type":"前后任","context":"刘永升→刘恩举 嘉峪关市委书记交接","overlap_org":"中共嘉峪关市委员会","overlap_period":"2025-07"},
    {"person_a":2,"person_b":20,"type":"前后任","context":"刘凯→王驰 嘉峪关市长交接","overlap_org":"嘉峪关市人民政府","overlap_period":"2026-02"},

    # 常委会成员关系
    {"person_a":1,"person_b":5,"type":"党政同僚","context":"市委书记与专职副书记","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":6,"type":"党政同僚","context":"市委书记与常务副市长","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":7,"type":"党政同僚","context":"市委书记与酒钢集团董事长（常委）","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":8,"type":"党政同僚","context":"市委书记与常委韩宝成","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":9,"type":"党政同僚","context":"市委书记与秘书长王玉忠","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":10,"type":"党政同僚","context":"市委书记与常委副市长徐方明","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":11,"type":"党政同僚","context":"市委书记与常委李祥成","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":12,"type":"党政同僚","context":"市委书记与常委马梅","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
    {"person_a":1,"person_b":13,"type":"党政同僚","context":"市委书记与常委张辉","overlap_org":"中共嘉峪关市委员会","overlap_period":""},
]

# =========================================================================
# BUILD DATABASE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Print summary
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ 数据库已创建: {DB_PATH}")
print(f"   人物: {person_count} | 机构: {org_count} | 任职: {pos_count} | 关系: {rel_count}")

# =========================================================================
# BUILD GEXF
# =========================================================================

def color_for_role(title):
    t = title or ""
    if "书记" in t and "纪委" not in t and "副" not in t[:t.index("书记")] if "书记" in t else True:
        return "#E03C31"
    if "市长" in t or "县长" in t or "区长" in t:
        return "#4a7fc7"
    if "人大" in t:
        return "#5a7a9a"
    if "政协" in t:
        return "#7a5a9a"
    if "纪委" in t:
        return "#d4880f"
    if "副书记" in t:
        return "#E07A31"
    if "副市长" in t or "副县长" in t or "副区长" in t:
        return "#6a8fe7"
    return "#888888"

def org_color(org_type):
    return {"党委": "rgba(200,50,50,0.3)", "政府": "rgba(50,100,200,0.3)",
            "人大": "rgba(90,122,154,0.3)", "政协": "rgba(122,90,154,0.3)",
            "纪委": "rgba(200,150,20,0.3)"}.get(org_type, "rgba(200,200,200,0.3)")

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('<meta><creator>Jiayuguan Investigator</creator><description>嘉峪关市领导班子工作关系网络</description></meta>')
gexf_parts.append('<graph mode="static" defaultedgetype="undirected">')

# Nodes
gexf_parts.append('<nodes>')
for p in persons:
    slug_id = f"jyg_{p['id']}"
    role_color = color_for_role(p["current_post"])
    is_top = "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    is_gov = ("市长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or \
             ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or \
             ("区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
    size = 20.0 if is_top else 15.0 if is_gov else 12.0
    label = f"{p['name']} ({p['current_post'] or '?'})"
    gexf_parts.append(f'<node id="{slug_id}" label="{label}">')
    gexf_parts.append(f'<attvalues><attvalue for="role" value="{p["current_post"]}"/><attvalue for="org" value="{p["current_org"]}"/><attvalue for="birth" value="{p["birth"]}"/><attvalue for="birthplace" value="{p["birthplace"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(role_color[1:3],16)}" g="{int(role_color[3:5],16)}" b="{int(role_color[5:7],16)}"/>')
    gexf_parts.append(f'<viz:size value="{size}"/>')
    gexf_parts.append('</node>')

for o in organizations:
    oid = f"org_{o['id']}"
    oc = org_color(o["type"])
    oc_rgb = oc.replace("rgba(", "").rstrip(")").split(",")
    gexf_parts.append(f'<node id="{oid}" label="{o["name"]}">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="{o["type"]}"/><attvalue for="level" value="{o["level"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(oc_rgb[0])}" g="{int(oc_rgb[1])}" b="{int(oc_rgb[2])}"/>')
    gexf_parts.append(f'<viz:size value="8.0"/>')
    gexf_parts.append('</node>')
gexf_parts.append('</nodes>')

# Edges
gexf_parts.append('<edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = f"{p['name']} → {o['name']} ({po['title']})"
    gexf_parts.append(f'<edge id="e{edge_id}" source="jyg_{p["id"]}" target="org_{o["id"]}" label="{label}" weight="1.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="worked_at"/><attvalue for="title" value="{po["title"]}"/><attvalue for="start" value="{po["start"]}"/><attvalue for="end" value="{po["end"]}"/></attvalues>')
    gexf_parts.append('</edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    gexf_parts.append(f'<edge id="e{edge_id}" source="jyg_{p_a["id"]}" target="jyg_{p_b["id"]}" label="{r["context"]}" weight="2.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="relationship"/><attvalue for="context" value="{r["context"]}"/></attvalues>')
    gexf_parts.append('</edge>')

gexf_parts.append('</edges>')
gexf_parts.append('</graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
