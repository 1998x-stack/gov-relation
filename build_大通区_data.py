#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大通区 (Datong District, Huainan, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_大通区 - 区委书记 & 区长
Sources: hndt.gov.cn 领导之窗 (official, accessed 2026-07-15)
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/anhui_大通区")
DB_PATH = os.path.join(STAGING, "大通区_network.db")
GEXF_PATH = os.path.join(STAGING, "大通区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "荣耀", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-09", "birthplace": "安徽六安", "education": "大学学历，经济学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委书记", "current_org": "中共大通区委员会",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=233"},
    {"id": 2, "name": "李雪梅", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-12", "birthplace": "", "education": "大学学历，管理学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委副书记、区长、区政府党组书记", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=216"},

    # ──区委副书记 ──
    {"id": 3, "name": "王道红", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-07", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委副书记", "current_org": "中共大通区委员会",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},

    # ── 区委常委 ──
    {"id": 4, "name": "胡玉强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委、人武部政委", "current_org": "大通区人民武装部",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
    {"id": 5, "name": "刘福岩", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委、副区长", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
    {"id": 6, "name": "黄新", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "", "education": "研究生，文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委、常务副区长、区政府党组副书记", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=228"},
    {"id": 7, "name": "茆永生", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-08", "birthplace": "", "education": "研究生，农学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委、组织部部长", "current_org": "中共大通区委员会组织部",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=205"},
    {"id": 8, "name": "刘磊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委", "current_org": "中共大通区委员会",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
    {"id": 9, "name": "赵坤", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-11", "birthplace": "安徽淮南", "education": "省委党校研究生，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委、纪委书记、区监委副主任、代理主任", "current_org": "中共大通区纪律检查委员会",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=236"},
    {"id": 10, "name": "胡传兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-01", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委、政法委书记", "current_org": "中共大通区委员会政法委员会",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=218"},
    {"id": 11, "name": "王慧", "gender": "女", "ethnicity": "汉族",
     "birth": "1984-06", "birthplace": "", "education": "大学，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区委常委、宣传部部长、统战部部长", "current_org": "中共大通区委员会宣传部",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=229"},

    # ── 副区长 ──
    {"id": 12, "name": "田振兴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区副区长", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
    {"id": 13, "name": "张倩茹", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区副区长", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
    {"id": 14, "name": "李祥全", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区副区长", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
    {"id": 15, "name": "栾正军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区副区长", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
    {"id": 16, "name": "杨布政", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大通区副区长", "current_org": "大通区人民政府",
     "source": "https://www.hndt.gov.cn/content/column/6787587?liId=232"},
]

organizations = [
    {"id": 1, "name": "中共大通区委员会", "type": "党委", "level": "县处级", "parent": "中共淮南市委", "location": "安徽省淮南市大通区"},
    {"id": 2, "name": "大通区人民政府", "type": "政府", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市大通区"},
    {"id": 3, "name": "大通区人民武装部", "type": "政府", "level": "县处级", "parent": "淮南军分区", "location": "安徽省淮南市大通区"},
    {"id": 4, "name": "中共大通区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共大通区委员会", "location": "安徽省淮南市大通区"},
    {"id": 5, "name": "中共大通区委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共大通区委员会", "location": "安徽省淮南市大通区"},
    {"id": 6, "name": "中共大通区委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共大通区委员会", "location": "安徽省淮南市大通区"},
    {"id": 7, "name": "中共大通区委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共大通区委员会", "location": "安徽省淮南市大通区"},
    {"id": 8, "name": "中共大通区委员会统战部", "type": "党委", "level": "乡科级", "parent": "中共大通区委员会", "location": "安徽省淮南市大通区"},
]

positions = [
    # 荣耀
    {"id": 1, "person_id": 1, "org_id": 1, "title": "大通区委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "第十二届区委连任"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "田家庵区委副书记、区长",
     "start": "", "end": "", "rank": "正县级", "note": "前职，调任大通区委书记"},
    {"id": 3, "person_id": 1, "org_id": 2, "title": "田家庵区委副书记、党校校长",
     "start": "", "end": "", "rank": "副县级", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 1, "title": "田家庵区委常委、组织部部长、统战部部长",
     "start": "", "end": "", "rank": "副县级", "note": ""},

    # 李雪梅
    {"id": 5, "person_id": 2, "org_id": 2, "title": "大通区委副书记、区长、区政府党组书记",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 2, "title": "市级群团组织书记",
     "start": "", "end": "", "rank": "正县级", "note": "前职"},

    # 王道红
    {"id": 7, "person_id": 3, "org_id": 1, "title": "大通区委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 胡玉强
    {"id": 8, "person_id": 4, "org_id": 3, "title": "大通区委常委、人武部政委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 刘福岩
    {"id": 9, "person_id": 5, "org_id": 2, "title": "大通区委常委、副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 黄新
    {"id": 10, "person_id": 6, "org_id": 2, "title": "大通区委常委、常务副区长、区政府党组副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 茆永生
    {"id": 11, "person_id": 7, "org_id": 5, "title": "大通区委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 刘磊
    {"id": 12, "person_id": 8, "org_id": 1, "title": "大通区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 赵坤
    {"id": 13, "person_id": 9, "org_id": 4, "title": "大通区委常委、纪委书记、区监委副主任、代理主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 胡传兵
    {"id": 14, "person_id": 10, "org_id": 6, "title": "大通区委常委、政法委书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 王慧
    {"id": 15, "person_id": 11, "org_id": 7, "title": "大通区委常委、宣传部部长、统战部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 副区长们
    {"id": 16, "person_id": 12, "org_id": 2, "title": "大通区副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 17, "person_id": 13, "org_id": 2, "title": "大通区副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 18, "person_id": 14, "org_id": 2, "title": "大通区副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 19, "person_id": 15, "org_id": 2, "title": "大通区副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 20, "person_id": 16, "org_id": 2, "title": "大通区副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
]

relationships = [
    # 荣耀与李雪梅 - 党政主官工作关系
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政主官关系", "overlap_org": "中共大通区委员会/大通区人民政府",
     "overlap_period": "2026-至今"},

    # 荣耀与王道红 - 正副书记
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记", "overlap_org": "中共大通区委员会",
     "overlap_period": "2026-至今"},

    # 荣耀与赵坤 - 书记与纪委书记
    {"id": 3, "person_a_id": 1, "person_b_id": 9, "type": "superior_subordinate",
     "context": "区委书记与纪委书记", "overlap_org": "中共大通区委员会",
     "overlap_period": "2026-至今"},

    # 荣耀与茆永生 - 书记与组织部长
    {"id": 4, "person_a_id": 1, "person_b_id": 7, "type": "superior_subordinate",
     "context": "区委书记与组织部部长", "overlap_org": "中共大通区委员会",
     "overlap_period": "2026-至今"},

    # 李雪梅与黄新 - 区长与常务副区长
    {"id": 5, "person_a_id": 2, "person_b_id": 6, "type": "superior_subordinate",
     "context": "区长与常务副区长", "overlap_org": "大通区人民政府",
     "overlap_period": "2026-至今"},

    # 李雪梅与刘福岩 - 区长与副区长
    {"id": 6, "person_a_id": 2, "person_b_id": 5, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "大通区人民政府",
     "overlap_period": "2026-至今"},

    # 黄新与茆永生 - 相近出生年份，同期任职
    {"id": 7, "person_a_id": 6, "person_b_id": 7, "type": "overlap",
     "context": "两人分别1981和1983年出生，同为区委常委", "overlap_org": "中共大通区委员会",
     "overlap_period": "2026-至今"},

    # 王慧与茆永生 - 同为常委（组织+宣传")
    {"id": 8, "person_a_id": 11, "person_b_id": 7, "type": "overlap",
     "context": "区委常委中的宣传部部长与组织部部长", "overlap_org": "中共大通区委员会",
     "overlap_period": "2026-至今"},
]

# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "区委书记" in post:
        return "255,50,50"
    if "区长" in post:
        return "50,100,255"
    if "纪委书记" in post:
        return "255,165,0"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

def is_org_node(pid):
    return pid > 100

person_ids = {p["id"] for p in persons}
org_ids = {o["id"] for o in organizations}

# ── BUILD DB ─────────────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
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
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (id, person_a_id, person_b_id, type, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


# ── BUILD GEXF ───────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>大通区（安徽省淮南市）领导关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="gender" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="县处级"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        c = org_color(o)
        oid = o["id"] + 100
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        oid = pos["org_id"] + 100
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person relationships
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {len(persons)} persons, {len(organizations)} orgs, {eid} edges")


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    print("Building 大通区 (Datong District, Huainan) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    build_db()
    build_gexf()
    print("Done.")
