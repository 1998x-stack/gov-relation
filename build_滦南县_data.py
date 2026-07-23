#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 滦南县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGE = os.path.join(BASE, "data/tmp/hebei_滦南县")
DB_PATH = os.path.join(STAGE, "滦南县_network.db")
GEXF_PATH = os.path.join(STAGE, "滦南县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current and Recent 滦南 County Party Secretaries ──
    {"id": 1, "name": "吕素青", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共滦南县委书记", "current_org": "中共滦南县委员会",
     "source": "https://www.luannan.gov.cn/"},
    {"id": 2, "name": "艾文志", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "河北滦南", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
    {"id": 3, "name": "许晓娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    # ── Current and Recent 滦南 County Government Leaders ──
    {"id": 4, "name": "侯新宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县人民政府县长", "current_org": "滦南县人民政府",
     "source": "https://www.luannan.gov.cn/"},
    {"id": 5, "name": "张福增", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    # ── Key Deputies (县委常委, 副县长) ──
    {"id": 6, "name": "孔凡玉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县委常委、常务副县长", "current_org": "滦南县人民政府",
     "source": ""},
    {"id": 7, "name": "杨洪伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县委常委、组织部部长", "current_org": "中共滦南县委员会",
     "source": ""},
    {"id": 8, "name": "马文斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县委常委、政法委书记", "current_org": "中共滦南县委员会",
     "source": ""},
    {"id": 9, "name": "李凤祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县委常委、纪委书记、监委主任", "current_org": "中共滦南县纪律检查委员会",
     "source": ""},
    {"id": 10, "name": "刘晓明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县委常委、宣传部部长", "current_org": "中共滦南县委员会",
     "source": ""},
    {"id": 11, "name": "王立新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县委常委、县委办公室主任", "current_org": "中共滦南县委员会",
     "source": ""},
    {"id": 12, "name": "董焕德", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦南县委常委、统战部部长", "current_org": "中共滦南县委员会",
     "source": ""},

    # ── Predecessors (earlier) ──
    {"id": 13, "name": "蔡洪魁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
    {"id": 14, "name": "李春兴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共滦南县委员会", "type": "党委", "level": "县处级", "parent": "中共唐山市委", "location": "滦南县"},
    {"id": 2, "name": "滦南县人民政府", "type": "政府", "level": "县处级", "parent": "唐山市人民政府", "location": "滦南县"},
    {"id": 3, "name": "中共滦南县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共滦南县委员会", "location": "滦南县"},
    {"id": 4, "name": "中共滦南县委组织部", "type": "党委", "level": "县处级", "parent": "中共滦南县委员会", "location": "滦南县"},
    {"id": 5, "name": "中共滦南县委宣传部", "type": "党委", "level": "县处级", "parent": "中共滦南县委员会", "location": "滦南县"},
    {"id": 6, "name": "中共滦南县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共滦南县委员会", "location": "滦南县"},
    {"id": 7, "name": "中共滦南县委统战部", "type": "党委", "level": "县处级", "parent": "中共滦南县委员会", "location": "滦南县"},
    {"id": 8, "name": "中共滦南县委办公室", "type": "党委", "level": "县处级", "parent": "中共滦南县委员会", "location": "滦南县"},
    {"id": 9, "name": "滦南县人大常委会", "type": "人大", "level": "县处级", "parent": "唐山市人大常委会", "location": "滦南县"},
    {"id": 10, "name": "滦南县政协", "type": "政协", "level": "县处级", "parent": "唐山市政协", "location": "滦南县"},
]

positions = [
    # ── Party Secretaries ──
    {"person_id": 1, "org_id": 1, "title": "中共滦南县委书记",
     "start_date": "2021-10", "end_date": "present", "rank": "县处级正职",
     "note": "曾任滦南县县长，后接任县委书记"},
    {"person_id": 2, "org_id": 1, "title": "中共滦南县委书记",
     "start_date": "2016-12", "end_date": "2021-10", "rank": "县处级正职",
     "note": "前任县委书记"},
    {"person_id": 3, "org_id": 1, "title": "中共滦南县委书记",
     "start_date": "", "end_date": "2016-12", "rank": "县处级正职",
     "note": "前任县委书记"},
    {"person_id": 13, "org_id": 1, "title": "中共滦南县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "更早时期县委书记"},
    {"person_id": 14, "org_id": 1, "title": "中共滦南县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "更早时期县委书记"},

    # ── County Mayors ──
    {"person_id": 4, "org_id": 2, "title": "滦南县人民政府县长",
     "start_date": "2021-10", "end_date": "present", "rank": "县处级正职",
     "note": "现任县长，曾任滦南县委副书记"},
    {"person_id": 1, "org_id": 2, "title": "滦南县人民政府县长",
     "start_date": "2017", "end_date": "2021-10", "rank": "县处级正职",
     "note": "吕素青在任县委书记前担任县长"},
    {"person_id": 5, "org_id": 2, "title": "滦南县人民政府县长",
     "start_date": "2015", "end_date": "2017", "rank": "县处级正职",
     "note": "前任县长"},

    # ── Deputies ──
    {"person_id": 6, "org_id": 2, "title": "滦南县委常委、常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 4, "title": "滦南县委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 6, "title": "滦南县委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 9, "org_id": 3, "title": "滦南县委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 10, "org_id": 5, "title": "滦南县委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 11, "org_id": 8, "title": "滦南县委常委、县委办公室主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 12, "org_id": 7, "title": "滦南县委常委、统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
]

relationships = [
    # Predecessor-successor (Party Secretary chain)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "吕素青接替艾文志任县委书记",
     "overlap_org": "中共滦南县委员会",
     "overlap_period": "2021-10"},
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "context": "艾文志接替许晓娟任县委书记",
     "overlap_org": "中共滦南县委员会",
     "overlap_period": "2016-12"},

    # Predecessor-successor (County Mayor chain)
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor",
     "context": "侯新宏接替吕素青任县长（吕素青升任县委书记）",
     "overlap_org": "滦南县人民政府",
     "overlap_period": "2021-10"},
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor",
     "context": "吕素青接替张福增任县长",
     "overlap_org": "滦南县人民政府",
     "overlap_period": "2017"},

    # Party Secretary-Mayo- collaboration
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "吕素青（书记）与侯新宏（县长）搭班子",
     "overlap_org": "滦南县人民政府",
     "overlap_period": "2021-10至今"},
]

# ── HELPER: XML escape ──
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── PERSON COLOR ──
def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "纪委" not in role:
        return "255,50,50"   # Red — Party Secretary
    if "县长" in role or "副县长" in role:
        return "50,100,255"  # Blue — Government
    if "纪委" in role:
        return "255,165,0"   # Orange — Discipline
    return "100,100,100"     # Grey — Others


# ── ORG COLOR ──
def org_color(t):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


# ── BUILD DB ──
def build_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # Drop & recreate
    for tbl in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {tbl}")

    conn.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    cols = ["id","name","gender","ethnicity","birth","birthplace","education",
             "party_join","work_start","current_post","current_org","source"]
    ph = ",".join("?" for _ in cols)
    for p in persons:
        conn.execute(f"INSERT INTO persons ({','.join(cols)}) VALUES ({ph})",
                     [p.get(c, "") for c in cols])

    cols2 = ["id","name","type","level","parent","location"]
    ph2 = ",".join("?" for _ in cols2)
    for o in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(cols2)}) VALUES ({ph2})",
                     [o.get(c, "") for c in cols2])

    cols3 = ["person_id","org_id","title","start_date","end_date","rank","note"]
    ph3 = ",".join("?" for _ in cols3)
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(cols3)}) VALUES ({ph3})",
                     [pos.get(c, "") for c in cols3])

    cols4 = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    ph4 = ",".join("?" for _ in cols4)
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(cols4)}) VALUES ({ph4})",
                     [r.get(c, "") for c in cols4])

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rel:     {len(relationships)}")


# ── BUILD GEXF ──
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>滦南县党政领导关系网络</description>')
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
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if any(kw in p.get("current_post", "") for kw in ["县委书记", "县长"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Org nodes
    for o in organizations:
        c = org_color(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Position edges: person -> org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges: person <-> person
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── MAIN ──
if __name__ == "__main__":
    os.makedirs(STAGE, exist_ok=True)
    build_db()
    build_gexf()
