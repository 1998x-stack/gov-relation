#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 潘集区 (Panji District, Huainan, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_潘集区 - 区委书记 & 区长
Sources: panji.gov.cn 新闻报道 (official, accessed 2026-07-15)
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/anhui_潘集区")
DB_PATH = os.path.join(STAGING, "潘集区_network.db")
GEXF_PATH = os.path.join(STAGING, "潘集区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "李国柱", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委书记", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 2, "name": "徐杉", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委副书记、区长", "current_org": "潘集区人民政府",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},

    # ── 区委领导 ──
    {"id": 3, "name": "盛星", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委副书记", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 4, "name": "段传策", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 5, "name": "杨磊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 6, "name": "苏传刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 7, "name": "宋永", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 8, "name": "李海兵", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 9, "name": "廖延延", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 10, "name": "胡伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},
    {"id": 11, "name": "陈超", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区委常委", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},

    # ── 人大领导 ──
    {"id": 12, "name": "曾健", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区人大常委会党组书记、主任", "current_org": "潘集区人民代表大会常务委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},

    # ── 政府领导 (副区长) ──
    {"id": 13, "name": "张伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区政府副区长", "current_org": "潘集区人民政府",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259067072.html"},

    # ── 政协领导 ──
    {"id": 14, "name": "董善积", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潘集区政协党组书记、主席", "current_org": "政协潘集区委员会",
     "source": "https://www.panji.gov.cn/pjzx/jrpj/11259066854.html"},

    # ── 前任领导 ──
    {"id": 15, "name": "宋立敏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前潘集区委书记", "current_org": "中共潘集区委员会",
     "source": "https://www.panji.gov.cn/zsyz/zsyz/11258987167.html"},
]

organizations = [
    {"id": 1, "name": "中共潘集区委员会", "type": "党委", "level": "县处级", "parent": "中共淮南市委", "location": "安徽省淮南市潘集区"},
    {"id": 2, "name": "潘集区人民政府", "type": "政府", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市潘集区"},
    {"id": 3, "name": "潘集区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "淮南市人大常委会", "location": "安徽省淮南市潘集区"},
    {"id": 4, "name": "政协潘集区委员会", "type": "政协", "level": "县处级", "parent": "政协淮南市委员会", "location": "安徽省淮南市潘集区"},
]

positions = [
    # 李国柱 - 潘集区委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "潘集区委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "现任，在2026年6月中共潘集区第十二次代表大会上连任区委书记"},

    # 徐杉 - 潘集区委副书记、区长
    {"id": 2, "person_id": 2, "org_id": 1, "title": "潘集区委副书记",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "潘集区区长",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 盛星 - 区委副书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "潘集区委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 区委常委
    {"id": 5, "person_id": 4, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "段传策"},
    {"id": 6, "person_id": 5, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "杨磊"},
    {"id": 7, "person_id": 6, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "苏传刚"},
    {"id": 8, "person_id": 7, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "宋永"},
    {"id": 9, "person_id": 8, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "李海兵"},
    {"id": 10, "person_id": 9, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "廖延延"},
    {"id": 11, "person_id": 10, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "胡伟"},
    {"id": 12, "person_id": 11, "org_id": 1, "title": "潘集区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "陈超"},

    # 曾健 - 人大主任
    {"id": 13, "person_id": 12, "org_id": 3, "title": "潘集区人大常委会党组书记、主任",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 张伟 - 副区长
    {"id": 14, "person_id": 13, "org_id": 2, "title": "潘集区政府副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 董善积 - 政协主席
    {"id": 15, "person_id": 14, "org_id": 4, "title": "潘集区政协党组书记、主席",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 宋立敏 - 前区委书记
    {"id": 16, "person_id": 15, "org_id": 1, "title": "前潘集区委书记",
     "start": "", "end": "", "rank": "正县级", "note": "前任区委书记，旧新闻报道曾召开项目推进会"},
]

relationships = [
    # 李国柱与徐杉 - 党政主官
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政主官关系", "overlap_org": "中共潘集区委员会/潘集区人民政府",
     "overlap_period": "至今"},

    # 李国柱与盛星
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},

    # 李国柱与曾健 - 区委书记与人大主任
    {"id": 3, "person_a_id": 1, "person_b_id": 12, "type": "overlap",
     "context": "区委书记与人大常委会主任", "overlap_org": "潘集区",
     "overlap_period": "至今"},

    # 李国柱与董善积 - 区委书记与政协主席
    {"id": 4, "person_a_id": 1, "person_b_id": 14, "type": "overlap",
     "context": "区委书记与政协主席", "overlap_org": "潘集区",
     "overlap_period": "至今"},

    # 徐杉与张伟 - 区长与副区长
    {"id": 5, "person_a_id": 2, "person_b_id": 13, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "潘集区人民政府",
     "overlap_period": "至今"},

    # 李国柱与各位常委 - 区委书记与区委常委班子成员
    {"id": 6, "person_a_id": 1, "person_b_id": 4, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 5, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 6, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 7, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},
    {"id": 10, "person_a_id": 1, "person_b_id": 8, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},
    {"id": 11, "person_a_id": 1, "person_b_id": 9, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},
    {"id": 12, "person_a_id": 1, "person_b_id": 10, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},
    {"id": 13, "person_a_id": 1, "person_b_id": 11, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共潘集区委员会",
     "overlap_period": "至今"},

    # 李国柱与宋立敏 - 前后任
    {"id": 14, "person_a_id": 1, "person_b_id": 15, "type": "predecessor_successor",
     "context": "李国柱接替宋立敏任潘集区委书记", "overlap_org": "中共潘集区委员会",
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
    lines.append('    <description>潘集区（安徽省淮南市）领导关系网络 - 2026年7月</description>')
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
    print("Building 潘集区 (Panji District, Huainan) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    build_db()
    build_gexf()
    print("Done.")
