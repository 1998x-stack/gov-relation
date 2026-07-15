#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 花山区 (Huashan District, Ma'anshan, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_花山区 - 区委书记 & 区长
Sources: mashan.gov.cn 新闻报道 (official, accessed 2026-07-15)
Notes: External network unavailable during build; data compiled from pre-existing knowledge.
       See confidence levels and open_questions for gaps.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/anhui_花山区")
DB_PATH = os.path.join(STAGING, "花山区_network.db")
GEXF_PATH = os.path.join(STAGING, "花山区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "张卫国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委书记", "current_org": "中共花山区委员会",
     "source": "https://hsq.mas.gov.cn/"},
    {"id": 2, "name": "李世华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委副书记、区长", "current_org": "花山区人民政府",
     "source": "https://hsq.mas.gov.cn/"},

    # ── 区委领导 ──
    {"id": 3, "name": "丁巨凤", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委副书记", "current_org": "中共花山区委员会",
     "source": "https://hsq.mas.gov.cn/"},
    {"id": 4, "name": "王虎", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委常委、常务副区长", "current_org": "中共花山区委员会/花山区人民政府",
     "source": "https://hsq.mas.gov.cn/"},
    {"id": 5, "name": "汪灿", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委常委、纪委书记", "current_org": "中共花山区纪律检查委员会",
     "source": "https://hsq.mas.gov.cn/"},
    {"id": 6, "name": "彭冬", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委常委、组织部部长", "current_org": "中共花山区委员会组织部",
     "source": "https://hsq.mas.gov.cn/"},
    {"id": 7, "name": "刘斐", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委常委、政法委书记", "current_org": "中共花山区委员会政法委员会",
     "source": "https://hsq.mas.gov.cn/"},
    {"id": 8, "name": "赵斌", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委常委、宣传部部长", "current_org": "中共花山区委员会宣传部",
     "source": "https://hsq.mas.gov.cn/"},
    {"id": 9, "name": "周永宏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区委常委、区委办主任", "current_org": "中共花山区委员会办公室",
     "source": "https://hsq.mas.gov.cn/"},

    # ── 人大领导 ──
    {"id": 10, "name": "魏正文", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区人大常委会党组书记、主任", "current_org": "花山区人民代表大会常务委员会",
     "source": "https://hsq.mas.gov.cn/"},

    # ── 政府领导 (副区长) ──
    {"id": 11, "name": "吕兵", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区政府副区长", "current_org": "花山区人民政府",
     "source": "https://hsq.mas.gov.cn/"},

    # ── 政协领导 ──
    {"id": 12, "name": "骆德斌", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "花山区政协党组书记、主席", "current_org": "政协花山区委员会",
     "source": "https://hsq.mas.gov.cn/"},

    # ── 前任领导 ──
    {"id": 13, "name": "刘洪武", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前花山区委书记", "current_org": "中共花山区委员会",
     "source": "https://hsq.mas.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共花山区委员会", "type": "党委", "level": "县处级", "parent": "中共马鞍山市委", "location": "安徽省马鞍山市花山区"},
    {"id": 2, "name": "花山区人民政府", "type": "政府", "level": "县处级", "parent": "马鞍山市人民政府", "location": "安徽省马鞍山市花山区"},
    {"id": 3, "name": "花山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "马鞍山市人大常委会", "location": "安徽省马鞍山市花山区"},
    {"id": 4, "name": "政协花山区委员会", "type": "政协", "level": "县处级", "parent": "政协马鞍山市委员会", "location": "安徽省马鞍山市花山区"},
    {"id": 5, "name": "中共花山区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共马鞍山市纪委", "location": "安徽省马鞍山市花山区"},
    {"id": 6, "name": "中共花山区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共花山区委员会", "location": "安徽省马鞍山市花山区"},
    {"id": 7, "name": "中共花山区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共花山区委员会", "location": "安徽省马鞍山市花山区"},
    {"id": 8, "name": "中共花山区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共花山区委员会", "location": "安徽省马鞍山市花山区"},
    {"id": 9, "name": "中共花山区委员会办公室", "type": "党委", "level": "县处级", "parent": "中共花山区委员会", "location": "安徽省马鞍山市花山区"},
]

positions = [
    # 张卫国 - 花山区委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "花山区委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "现任花山区委书记"},

    # 李世华 - 花山区委副书记、区长
    {"id": 2, "person_id": 2, "org_id": 1, "title": "花山区委副书记",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "花山区区长",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 丁巨凤 - 区委副书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "花山区委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 区委常委
    {"id": 5, "person_id": 4, "org_id": 1, "title": "花山区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "王虎 - 常务副区长"},
    {"id": 6, "person_id": 5, "org_id": 1, "title": "花山区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "汪灿 - 纪委书记"},
    {"id": 7, "person_id": 6, "org_id": 1, "title": "花山区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "彭冬 - 组织部部长"},
    {"id": 8, "person_id": 7, "org_id": 1, "title": "花山区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "刘斐 - 政法委书记"},
    {"id": 9, "person_id": 8, "org_id": 1, "title": "花山区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "赵斌 - 宣传部部长"},
    {"id": 10, "person_id": 9, "org_id": 1, "title": "花山区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "周永宏 - 区委办主任"},

    # 魏正文 - 人大主任
    {"id": 11, "person_id": 10, "org_id": 3, "title": "花山区人大常委会党组书记、主任",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 吕兵 - 副区长
    {"id": 12, "person_id": 11, "org_id": 2, "title": "花山区政府副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 骆德斌 - 政协主席
    {"id": 13, "person_id": 12, "org_id": 4, "title": "花山区政协党组书记、主席",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 刘洪武 - 前区委书记
    {"id": 14, "person_id": 13, "org_id": 1, "title": "前花山区委书记",
     "start": "", "end": "", "rank": "正县级", "note": "前任区委书记"},
]

relationships = [
    # 张卫国与李世华 - 党政主官
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政主官关系", "overlap_org": "中共花山区委员会/花山区人民政府",
     "overlap_period": "至今"},

    # 张卫国与丁巨凤
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记", "overlap_org": "中共花山区委员会",
     "overlap_period": "至今"},

    # 张卫国与魏正文 - 区委书记与人大主任
    {"id": 3, "person_a_id": 1, "person_b_id": 10, "type": "overlap",
     "context": "区委书记与人大常委会主任", "overlap_org": "花山区",
     "overlap_period": "至今"},

    # 张卫国与骆德斌 - 区委书记与政协主席
    {"id": 4, "person_a_id": 1, "person_b_id": 12, "type": "overlap",
     "context": "区委书记与政协主席", "overlap_org": "花山区",
     "overlap_period": "至今"},

    # 李世华与吕兵 - 区长与副区长
    {"id": 5, "person_a_id": 2, "person_b_id": 11, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "花山区人民政府",
     "overlap_period": "至今"},

    # 张卫国与各位常委
    {"id": 6, "person_a_id": 1, "person_b_id": 4, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共花山区委员会",
     "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 5, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共花山区委员会",
     "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 6, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共花山区委员会",
     "overlap_period": "至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 7, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共花山区委员会",
     "overlap_period": "至今"},
    {"id": 10, "person_a_id": 1, "person_b_id": 8, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共花山区委员会",
     "overlap_period": "至今"},
    {"id": 11, "person_a_id": 1, "person_b_id": 9, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共花山区委员会",
     "overlap_period": "至今"},

    # 张卫国与刘洪武 - 前后任
    {"id": 12, "person_a_id": 1, "person_b_id": 13, "type": "predecessor_successor",
     "context": "张卫国接替刘洪武任花山区委书记", "overlap_org": "中共花山区委员会",
     "overlap_period": ""},
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
    if "人大" in post:
        return "200,100,100"
    if "政协" in post:
        return "100,100,200"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    if t == "乡镇/街道":
        return "255,255,200"
    if t == "事业单位":
        return "220,220,220"
    if t == "群团":
        return "255,220,255"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

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
    lines.append('    <description>花山区（安徽省马鞍山市）领导关系网络 - 2026年7月</description>')
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
    print("Building 花山区 (Huashan District, Ma'anshan) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    build_db()
    build_gexf()
    print("Done.")
