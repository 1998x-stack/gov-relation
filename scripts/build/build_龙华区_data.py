#!/usr/bin/env python3
"""
龙华区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Longhua District leadership network.

Level: 市辖区
Province: 广东省
Parent City: 深圳市
Region: 龙华区
Targets: 区委书记 & 区长

Research Sources:
- 维基百科 — 龙华区 (深圳市)
- 深圳市龙华区政府在线 — 领导之窗
- 公开新闻报道

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "龙华区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "龙华区_network.gexf")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "王卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙华区委书记",
        "current_org": "中共深圳市龙华区委员会",
        "source": "维基百科: 龙华区(深圳市)",
        "person_id": "longhua_wang_wei"
    },
    {
        "id": "p02",
        "name": "雷卫华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙华区委副书记、区长",
        "current_org": "深圳市龙华区人民政府",
        "source": "公开新闻报道",
        "person_id": "longhua_lei_weihua"
    },
    # ════════════════════════════════════════
    # Key Deputies (区委常委 / 副区长)
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "皮勇华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙华区委副书记、政法委书记",
        "current_org": "中共深圳市龙华区委员会",
        "source": "公开报道",
        "person_id": "longhua_pi_yonghua"
    },
    {
        "id": "p04",
        "name": "徐志斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙华区委常委、常务副区长",
        "current_org": "深圳市龙华区人民政府",
        "source": "公开报道",
        "person_id": "longhua_xu_zhibin"
    },
    {
        "id": "p05",
        "name": "曾敬东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙华区委常委、区纪委书记、区监委主任",
        "current_org": "中共深圳市龙华区纪律检查委员会",
        "source": "公开报道",
        "person_id": "longhua_zeng_jingdong"
    },
    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════
    {
        "id": "p06",
        "name": "杜玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1965年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "深圳市人大常委会副主任（原龙华区委书记）",
        "current_org": "深圳市人民代表大会常务委员会",
        "source": "公开报道",
        "person_id": "longhua_du_ling"
    },
    {
        "id": "p07",
        "name": "余新国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "深圳市委常委、政法委书记（原龙华区委书记）",
        "current_org": "中共深圳市委政法委员会",
        "source": "公开报道",
        "person_id": "longhua_yu_xinguo"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共深圳市龙华区委员会", "type": "党委", "level": "市辖区", "parent": "中共深圳市委员会", "location": "深圳市龙华区观湖街道"},
    {"id": 2, "name": "深圳市龙华区人民政府", "type": "政府", "level": "市辖区", "parent": "深圳市人民政府", "location": "深圳市龙华区观湖街道"},
    {"id": 3, "name": "中共深圳市龙华区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共深圳市纪律检查委员会", "location": "深圳市龙华区观湖街道"},
    {"id": 4, "name": "深圳市龙华区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "深圳市人民代表大会常务委员会", "location": "深圳市龙华区"},
    {"id": 5, "name": "深圳市龙华区政协", "type": "政协", "level": "市辖区", "parent": "深圳市政协", "location": "深圳市龙华区"},
    {"id": 6, "name": "中共深圳市委员会", "type": "党委", "level": "副省级", "parent": "中共广东省委员会", "location": "深圳市福田区"},
    {"id": 7, "name": "深圳市人民政府", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "深圳市福田区"},
    {"id": 8, "name": "深圳市人民代表大会常务委员会", "type": "人大", "level": "副省级", "parent": "广东省人大常委会", "location": "深圳市福田区"},
    {"id": 9, "name": "中共深圳市委政法委员会", "type": "党委", "level": "副省级", "parent": "中共深圳市委员会", "location": "深圳市福田区"},
    {"id": 10, "name": "龙华新区党工委", "type": "党委", "level": "市辖区(功能区)", "parent": "中共深圳市委", "location": "深圳市龙华区"},
    {"id": 11, "name": "南山区人民政府", "type": "政府", "level": "市辖区", "parent": "深圳市人民政府", "location": "深圳市南山区"},
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 王卫 — 龙华区委书记
    ("p01", 1, "龙华区委书记", "2021", "至今", "副厅级", "现任龙华区委书记"),
    ("p01", 6, "深圳市委委员", "2021", "至今", "副厅级", ""),
    ("p01", 10, "龙华新区党工委副书记、管委会主任", "2015", "2017", "副厅级", "龙华新区时期"),
    ("p01", 7, "龙华区区长", "2017", "2021", "副厅级", "龙华设区后首任区长"),
    ("p01", 11, "南山区副区长", "2011", "2015", "正处级", ""),

    # 雷卫华 — 龙华区区长
    ("p02", 2, "龙华区委副书记、区长", "2021", "至今", "副厅级", "接替王卫任区长"),
    ("p02", 6, "深圳市委委员", "2021", "至今", "副厅级", ""),
    ("p02", 7, "深圳市政府副秘书长", "2019", "2021", "正局级", ""),
    ("p02", 6, "深圳市委办公厅副主任", "2016", "2019", "副局级", ""),
    ("p02", 7, "深圳市投资推广署副署长", "2014", "2016", "副局级", ""),

    # 皮勇华 — 区委副书记、政法委书记
    ("p03", 1, "龙华区委副书记、政法委书记", "2021", "至今", "副厅级", ""),
    ("p03", 7, "龙华区副区长", "2017", "2021", "副局级", ""),

    # 徐志斌 — 常务副区长
    ("p04", 2, "龙华区委常委、常务副区长", "2021", "至今", "副局级", ""),
    ("p04", 7, "龙华区发展和改革局局长", "2017", "2021", "正处级", ""),

    # 曾敬东 — 纪委书记
    ("p05", 3, "龙华区委常委、纪委书记、区监委主任", "2021", "至今", "副局级", ""),

    # 杜玲 — 原龙华区委书记
    ("p06", 1, "龙华区委书记", "2018", "2021", "副厅级", "接替余新国"),
    ("p06", 8, "深圳市人大常委会副主任", "2021", "至今", "副省级", ""),
    ("p06", 10, "龙华新区党工委书记", "2015", "2018", "副厅级", ""),

    # 余新国 — 原龙华区委书记
    ("p07", 1, "龙华区委书记", "2015", "2018", "副厅级", "首任龙华区委书记"),
    ("p07", 9, "深圳市委常委、政法委书记", "2018", "至今", "副省级", ""),
    ("p07", 11, "南山区区长", "2011", "2015", "正局级", ""),
]

# 4. Relationships
relationships = [
    # 王卫 ↔ 雷卫华: Current top leadership team
    ("p01", "p02", "共事", "区委书记—区长搭档", "中共深圳市龙华区委员会/龙华区人民政府", "2021至今"),

    # 王卫 ↔ 杜玲: Predecessor-successor as party secretary
    ("p01", "p06", "前后任", "杜玲卸任区委书记，王卫接任", "中共深圳市龙华区委员会", "2021"),

    # 杜玲 ↔ 余新国: Predecessor-successor as party secretary
    ("p06", "p07", "前后任", "余新国卸任龙华区委书记，杜玲接任", "中共深圳市龙华区委员会", "2018"),

    # 王卫 → 雷卫华: Predecessor-successor as district mayor
    ("p01", "p02", "前后任", "王卫卸任区长升任区委书记，雷卫华接任区长", "龙华区人民政府", "2021"),

    # 王卫 ↔ 余新国: 南山-龙华 connection
    ("p01", "p07", "跨区共事", "余新国任南山区区长时，王卫任南山区副区长", "南山区人民政府", "2011~2015"),

    # 皮勇华 ↔ 王卫: Leadership team
    ("p03", "p01", "上下级", "区委副书记—区委书记", "中共深圳市龙华区委员会", "2021至今"),

    # 皮勇华 ↔ 雷卫华: Leadership team
    ("p03", "p02", "上下级", "区委副书记—区长", "中共深圳市龙华区委员会/龙华区人民政府", "2021至今"),

    # 徐志斌 ↔ 雷卫华: Government leadership
    ("p04", "p02", "上下级", "常务副区长—区长", "深圳市龙华区人民政府", "2021至今"),

    # 曾敬东 → 王卫: Discipline inspection
    ("p05", "p01", "上下级", "区纪委书记—区委书记", "中共深圳市龙华区委员会", "2021至今"),
]

# ── Helper functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_top_leader(name):
    return name in ("王卫", "雷卫华", "杜玲", "余新国")

def person_color(name, post):
    if "书记" in post and "副书记" not in post:
        return (255, 50, 50)  # Red - Party Secretary
    if "区长" in post or "市长" in post:
        return (50, 100, 255)  # Blue - Government leader
    if "常委" in post and "副区长" in post:
        return (100, 150, 255)  # Light blue - Deputy
    if "纪委" in post:
        return (255, 165, 0)  # Orange - Discipline
    if "政法委" in post:
        return (200, 100, 100)  # Dark red - Politics/Law
    if "人大" in post:
        return (200, 255, 255)  # Cyan
    if "政协" in post:
        return (255, 240, 200)  # Cream
    return (100, 100, 100)  # Grey

def org_color(org_type):
    colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "人大": (200, 255, 255),
        "政协": (255, 240, 200),
        "事业单位": (220, 220, 220),
    }
    return colors.get(org_type, (200, 200, 200))

# ── Build SQLite database ──

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start_date TEXT, end_date TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    # Insert persons
    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (int(p["id"][1:]), p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        pid = int(pos[0][1:])
        oid = pos[1]
        title = pos[2]
        start_d = pos[3]
        end_d = pos[4]
        rank = pos[5]
        note = pos[6]
        c.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (pid, oid, title, start_d, end_d, rank, note))

    # Insert relationships
    for r in relationships:
        pa = int(r[0][1:])
        pb = int(r[1][1:])
        rtype = r[2]
        ctx = r[3]
        oorg = r[4]
        oper = r[5]
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (pa, pb, rtype, ctx, oorg, oper))

    conn.commit()
    conn.close()
    print(f"  Database created: {DB_PATH}")


# ── Build GEXF graph ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>深圳市龙华区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('      <attribute id="5" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = int(p["id"][1:])
        c = person_color(p["name"], p["current_post"])
        sz = "20.0" if is_top_leader(p["name"]) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — Organizations
    for o in organizations:
        oid = o["id"]
        c = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="5" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges — Person→Organization (worked_at)
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        pid = int(pos[0][1:])
        oid = pos[1]
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[2])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos[4] or "")}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos[3])}～{esc(pos[4] or "至今")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges — Person↔Person (relationship)
    for r in relationships:
        eid += 1
        pa = int(r[0][1:])
        pb = int(r[1][1:])
        rel = r[2]
        ctx = r[3]
        oorg = r[4]
        oper = r[5]
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rel)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oorg)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(oper)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF graph created: {GEXF_PATH}")


# ── Main ──

if __name__ == "__main__":
    print("Building 龙华区 network data...")
    build_db()
    build_gexf()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print("\nSummary:")
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  {table}: {count}")
    conn.close()
    print("\nDone.")
