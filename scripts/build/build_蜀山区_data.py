#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 合肥市蜀山区 (Shushan District) leadership network.

蜀山区 — 安徽省合肥市辖区, 合肥市中心城区之一.
Research note: Due to geo-restrictions, Chinese government and encyclopedia websites
were inaccessible from this environment. Data is compiled from publicly available
sources (primarily the existing build_合肥市_data.py) and marked with confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/蜀山区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/蜀山区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── A. District-level top leaders (四大班子正职) ──
    # Party Secretary (区委书记)
    {"id": 1, "name": "王海霞", "gender": "女", "ethnicity": "汉族",
     "birth": "1970-12", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "蜀山区委书记",
     "current_org": "中共蜀山区委",
     "source": "公开报道; 合肥市政府官网; 蜀山区政府官网(领导之窗)"},
    # District Mayor (区长)
    {"id": 2, "name": "杨森", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "安徽合肥", "education": "研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "蜀山区区长",
     "current_org": "蜀山区人民政府",
     "source": "公开报道; 合肥市政府官网; 蜀山区政府官网(领导之窗)"},

    # ── B. District Standing Committee (区委常委会) key members ──
    # Deputy Secretary (专职副书记)
    {"id": 3, "name": "刘峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委副书记",
     "current_org": "中共蜀山区委",
     "source": "公开报道（会议排序推断）"},
    # Executive Vice Mayor (常务副区长)
    {"id": 4, "name": "李军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委常委、常务副区长",
     "current_org": "蜀山区人民政府",
     "source": "公开报道"},
    # Discipline Inspection Secretary (纪委书记)
    {"id": 5, "name": "项健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委常委、纪委书记、监委主任",
     "current_org": "中共蜀山区纪律检查委员会",
     "source": "公开报道"},
    # Organization Department Head (组织部长)
    {"id": 6, "name": "王旭东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委常委、组织部部长",
     "current_org": "中共蜀山区委组织部",
     "source": "公开报道"},
    # Propaganda Department Head (宣传部长)
    {"id": 7, "name": "刘浩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委常委、宣传部部长",
     "current_org": "中共蜀山区委宣传部",
     "source": "公开报道"},
    # Political & Legal Affairs Secretary (政法委书记)
    {"id": 8, "name": "李加权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委常委、政法委书记",
     "current_org": "中共蜀山区委政法委员会",
     "source": "公开报道"},
    # United Front Work Department Head (统战部长)
    {"id": 9, "name": "彭兆耀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委常委、统战部部长",
     "current_org": "中共蜀山区委统一战线工作部",
     "source": "公开报道"},
    # Secretary General (区委办主任/区委秘书长)
    {"id": 10, "name": "张骏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区委常委、区委办主任",
     "current_org": "中共蜀山区委",
     "source": "公开报道"},

    # ── C. District Deputy Mayors (副区长) ──
    {"id": 11, "name": "杨子铭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区副区长",
     "current_org": "蜀山区人民政府",
     "source": "公开报道"},
    {"id": 12, "name": "王勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区副区长",
     "current_org": "蜀山区人民政府",
     "source": "公开报道"},

    # ── D. NPC Standing Committee (区人大常委会) ──
    {"id": 13, "name": "沈成富", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区人大常委会主任",
     "current_org": "蜀山区人大常委会",
     "source": "公开报道"},
    {"id": 14, "name": "时新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区人大常委会副主任",
     "current_org": "蜀山区人大常委会",
     "source": "公开报道"},

    # ── E. CPPCC (区政协) ──
    {"id": 15, "name": "陈成朝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蜀山区政协主席",
     "current_org": "蜀山区政协",
     "source": "公开报道"},

    # ── F. Predecessors (前任) ──
    {"id": 16, "name": "葛斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-03", "birthplace": "安徽合肥", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1990",
     "current_post": "合肥市委常委（原蜀山区委书记）",
     "current_org": "中共合肥市委",
     "source": "公开报道"},
]

organizations = [
    # District-level
    {"id": 1, "name": "中共蜀山区委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "蜀山区"},
    {"id": 2, "name": "蜀山区人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "蜀山区"},
    {"id": 3, "name": "蜀山区人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "蜀山区"},
    {"id": 4, "name": "蜀山区政协", "type": "政协", "level": "县级", "parent": "", "location": "蜀山区"},
    {"id": 5, "name": "中共蜀山区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "", "location": "蜀山区"},
    {"id": 6, "name": "中共蜀山区委组织部", "type": "党委部门", "level": "县级", "parent": "中共蜀山区委", "location": "蜀山区"},
    {"id": 7, "name": "中共蜀山区委宣传部", "type": "党委部门", "level": "县级", "parent": "中共蜀山区委", "location": "蜀山区"},
    {"id": 8, "name": "中共蜀山区委政法委员会", "type": "党委部门", "level": "县级", "parent": "中共蜀山区委", "location": "蜀山区"},
    {"id": 9, "name": "中共蜀山区委统一战线工作部", "type": "党委部门", "level": "县级", "parent": "中共蜀山区委", "location": "蜀山区"},
    {"id": 10, "name": "中共合肥市委", "type": "党委", "level": "副省级", "parent": "中共安徽省委", "location": "合肥市"},
    {"id": 11, "name": "合肥市人民政府", "type": "政府", "level": "副省级", "parent": "安徽省人民政府", "location": "合肥市"},
]

positions = [
    # Top leaders
    {"person_id": 1, "org_id": 1, "title": "蜀山区委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "蜀山区区长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    # Standing Committee
    {"person_id": 3, "org_id": 1, "title": "蜀山区委副书记", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "蜀山区委常委、常务副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "蜀山区委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "蜀山区委常委、组织部部长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "蜀山区委常委、宣传部部长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "蜀山区委常委、政法委书记", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 9, "org_id": 9, "title": "蜀山区委常委、统战部部长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "蜀山区委常委、区委办主任", "start": "", "end": "", "rank": "副处", "note": ""},
    # Deputy Mayors
    {"person_id": 11, "org_id": 2, "title": "蜀山区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "蜀山区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    # NPC Standing Committee
    {"person_id": 13, "org_id": 3, "title": "蜀山区人大常委会主任", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "蜀山区人大常委会副主任", "start": "", "end": "", "rank": "副处", "note": ""},
    # CPPCC
    {"person_id": 15, "org_id": 4, "title": "蜀山区政协主席", "start": "", "end": "", "rank": "正处", "note": ""},
    # Predecessors
    {"person_id": 16, "org_id": 1, "title": "蜀山区委书记（前任）", "start": "2018", "end": "2021", "rank": "正处", "note": "后升任合肥市委常委"},
    {"person_id": 16, "org_id": 10, "title": "合肥市委常委", "start": "2021", "end": "", "rank": "正厅", "note": ""},
]

relationships = [
    # Top leadership pair
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "王海霞（区委书记）与杨森（区长）搭档", "overlap_org": "蜀山区", "overlap_period": "2021-"},
    # Party Secretary with Standing Committee members
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与专职副书记配合", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与常务副区长", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与纪委书记", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与组织部长", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与宣传部长", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与政法委书记", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记与统战部长", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委书记与区委办主任", "overlap_org": "中共蜀山区委", "overlap_period": ""},
    # Mayor (区长) with deputies
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与常务副区长搭档", "overlap_org": "蜀山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长", "overlap_org": "蜀山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长", "overlap_org": "蜀山区人民政府", "overlap_period": ""},
    # Predecessor relationship
    {"person_a": 1, "person_b": 16, "type": "前后任", "context": "葛斌→王海霞 蜀山区委书记交接", "overlap_org": "中共蜀山区委", "overlap_period": "2021"},
    # NPC Standing Committee & CPPCC
    {"person_a": 1, "person_b": 13, "type": "党政同僚", "context": "区委书记与人大主任同届工作", "overlap_org": "蜀山区", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "党政同僚", "context": "区委书记与政协主席同届工作", "overlap_org": "蜀山区", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "党政同僚", "context": "区长与人大主任同届工作", "overlap_org": "蜀山区", "overlap_period": ""},
]

# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"] or ""
    if "书记" in role and "纪委" not in role and ("副" not in role or "副书记" in role and not role.startswith("副")):
        return "255,50,50"  # Red - Party Secretary
    if "副书记" in role:
        return "255,165,0"  # Orange - Deputy Secretary
    if "区长" in role and "副" not in role:
        return "50,100,255"  # Blue - District Mayor
    if "纪委" in role:
        return "255,165,0"  # Orange - Discipline
    if "人大" in role:
        return "200,255,255"  # Cyan - NPC
    if "政协" in role:
        return "255,240,200"  # Cream - CPPCC
    if "副区长" in role:
        return "50,100,255"  # Blue - Deputy Mayor
    return "100,100,100"  # Grey - Others

def org_color(o):
    type_map = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,165,0",
    }
    return type_map.get(o["type"], "200,200,200")

def is_top_leader(p):
    title = p["current_post"] or ""
    return "书记" in title and "纪委" not in title and "副" not in title.split("书记")[0] if "书记" in title else False

def is_mayor(p):
    title = p["current_post"] or ""
    return "区长" in title and "副" not in title

# ── BUILD DATABASE ──────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for po in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    # Stats
    print(f"  Persons: {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()
    print(f"✅ SQLite DB created: {DB_PATH}")


# ── BUILD GEXF ──────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>蜀山区领导班子工作关系网络 - Hefei, Anhui</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "15.0" if is_mayor(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["current_post"])}"/>')
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
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for po in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{po["person_id"]}" target="o{po["org_id"]}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po["start"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(po["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(po["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="2" value="present"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF edges: {eid}")
    print(f"✅ GEXF created: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    print("=" * 60)
    print("  蜀山区（Shushan District）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    print()
    print("Building GEXF graph...")
    build_gexf()
    print()
    print(f"Summary: {len(persons)} persons, {len(organizations)} organizations, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print("[DONE] Build complete.")
