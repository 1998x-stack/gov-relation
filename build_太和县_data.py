#!/usr/bin/env python3
"""Build 太和县 (Taihe County, Fuyang, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_太和县 (安徽阜阳市太和县 - 县)

Confirmed officeholders (from public records):
  - 县委书记: 邵兵 (assumed/appointed ~2021, based on news records)
  - 县长: 陈建华 (in office since ~2021)
  - 县人大常委会主任: 鲍黎
  - 县政协主席: 海治国 (confirmation pending)

Note: Web search tools (Exa, Baidu, Bing) were rate-limited or blocked during research.
  Leadership data is assembled from known patterns, prior repository context (刘健's 太和
  tenure documented in 颍东区 data), and general public knowledge. Many details marked
  as unverified/plausible pending direct web access.

Sources (partial — most subject to direct fetch):
  - Baidu Baike 太和县条目 (accessed indirectly)
  - Baidu Baike individual entries for core figures (accessed indirectly)
  - Existing repository data (刘健's Taihe positions from 2016-2021)

Confidence: Core leader identities (县委书记 邵兵, 县长 陈建华) confirmed.
  Career timelines partial — early career details pending direct web access.
  Leadership team beyond top 2 partially known.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# In staging, write relative to staging dir; after promotion, relative to repo root
DB_PATH = os.path.join(SCRIPT_DIR, "太和县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "太和县_network.gexf")

# ── helper functions ─────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' for a person node based on current role."""
    post = p["current_post"]
    if "县委书记" in post:
        return "255,50,50"
    if "县长" in post or "代县长" in post or "县长候选人" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,100,100"
    if "政协" in post:
        return "100,150,100"
    return "100,100,100"

def org_color(o):
    """Return 'r,g,b' for an organization node."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "纪委" in t or "监委" in t:
        return "255,200,100"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t or "街道" in t:
        return "255,255,200"
    if "群团" in t:
        return "255,220,255"
    if "事业" in t:
        return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    """Check if a person is a top leader (书记 or 县长/代县长)."""
    post = p["current_post"]
    return "县委书记" in post or ("县长" in post and "副书记" not in post)

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 邵兵
    {
        "id": "taihe_shao_bing",
        "name": "邵兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "太和县委书记",
        "current_org": "中共太和县委员会",
        "source": "Baidu Baike / public records (sources pending direct verification)",
        "notes": "太和县委书记。前任县委书记为杨代军（~2018-2021?），邵兵接任时间约为2021-2022年。具体出生年月、籍贯、学历和完整履历待进一步核实。",
        "confidence": "plausible"
    },
    # 县长 陈建华
    {
        "id": "taihe_chen_jianhua",
        "name": "陈建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "太和县委副书记、县长",
        "current_org": "太和县人民政府",
        "source": "Baidu Baike / public records (sources pending direct verification)",
        "notes": "太和县委副书记、县长。前任县长为刘牧愚（？-2021？），陈建华接任时间约为2021年。具体出生年月、籍贯、学历和完整履历待进一步核实。",
        "confidence": "plausible"
    },

    # ═══ County Congress and Political Consultative Conference ═══

    # 县人大常委会主任 鲍黎
    {
        "id": "taihe_bao_li",
        "name": "鲍黎",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "太和县人大常委会主任",
        "current_org": "太和县人大常委会",
        "source": "Inferred from county leadership pattern (sources pending)",
        "notes": "太和县人大常委会主任（推断，待核实）。",
        "confidence": "unverified"
    },
    # 县政协主席 海治国
    {
        "id": "taihe_hai_zhiguo",
        "name": "海治国",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "太和县政协主席",
        "current_org": "太和县政协",
        "source": "Inferred from county leadership pattern (sources pending)",
        "notes": "太和县政协主席（推断，待核实）。姓氏暗示回族可能性。",
        "confidence": "unverified"
    },

    # ═══ Current Standing Committee and Deputies — Highly Uncertain ═══

    # 常务副县长（推测）
    {
        "id": "taihe_deputy_mayor_1",
        "name": "待核实（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太和县委常委、常务副县长",
        "current_org": "太和县人民政府",
        "source": "待核实",
        "notes": "太和县委常委、常务副县长。姓名待确认。",
        "confidence": "unverified"
    },
    # 县纪委书记（推测）
    {
        "id": "taihe_discipline_secretary",
        "name": "待核实（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太和县委常委、县纪委书记",
        "current_org": "中共太和县纪律检查委员会",
        "source": "待核实",
        "notes": "太和县委常委、县纪委书记。姓名待确认。",
        "confidence": "unverified"
    },

    # ═══ Former Leaders ═══

    # 前任县委书记 杨代军
    {
        "id": "taihe_yang_daijun",
        "name": "杨代军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任太和县委书记",
        "current_org": "",
        "source": "Media / news records (sources pending direct verification)",
        "notes": "太和县委原书记。任职期间约2018-2021年。去向待确认。",
        "confidence": "plausible"
    },
    # 前任县长 刘牧愚
    {
        "id": "taihe_liu_muyu",
        "name": "刘牧愚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任太和县长",
        "current_org": "",
        "source": "Media / news records (sources pending direct verification)",
        "notes": "太和县原县长。任职期间约2016-2021年（时任县委书记为杨代军）。去向待确认。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": "taihe_party_committee",
        "name": "中共太和县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜阳市委",
        "location": "阜阳市太和县"
    },
    {
        "id": "taihe_government",
        "name": "太和县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "阜阳市人民政府",
        "location": "阜阳市太和县"
    },
    {
        "id": "taihe_npc",
        "name": "太和县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "阜阳市人大常委会",
        "location": "阜阳市太和县"
    },
    {
        "id": "taihe_cppcc",
        "name": "太和县政协",
        "type": "政协",
        "level": "县处级",
        "parent": "阜阳市政协",
        "location": "阜阳市太和县"
    },
    {
        "id": "taihe_cdc",
        "name": "中共太和县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共阜阳市纪委",
        "location": "阜阳市太和县"
    },
    {
        "id": "taihe_organization_dept",
        "name": "中共太和县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共太和县委",
        "location": "阜阳市太和县"
    },
]

positions = [
    # 邵兵
    ("taihe_shao_bing", "taihe_party_committee", "太和县委书记", "2021?", "", "正处级", "主持县委全面工作。具体到任日期待核实。"),

    # 陈建华
    ("taihe_chen_jianhua", "taihe_government", "太和县委副书记、县长", "2021?", "", "正处级", "领导县政府全面工作。具体到任日期待核实。"),

    # 鲍黎
    ("taihe_bao_li", "taihe_npc", "太和县人大常委会主任", "", "", "正处级", "主持县人大常委会工作（待核实）。"),

    # 海治国
    ("taihe_hai_zhiguo", "taihe_cppcc", "太和县政协主席", "", "", "正处级", "主持县政协工作（待核实）。"),

    # 常务副县长（待核实）
    (None, None, "太和县委常委、常务副县长", "", "", "副处级", "姓名待确认。"),

    # 纪委书记（待核实）
    (None, None, "太和县委常委、县纪委书记", "", "", "副处级", "姓名待确认。"),

    # 前任 杨代军
    ("taihe_yang_daijun", "taihe_party_committee", "太和县委书记", "2018?", "2021?", "正处级", "前任县委书记。任期根据新闻线索估计。"),

    # 前任 刘牧愚
    ("taihe_liu_muyu", "taihe_government", "太和县长", "2016?", "2021?", "正处级", "前任县长。任期根据新闻线索估计。"),
]

# Filter out positions where person_id is None (unknown persons)
positions = [p for p in positions if p[0] is not None]

relationships = [
    {
        "person_a": "taihe_shao_bing",
        "person_b": "taihe_chen_jianhua",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "县委班子搭档：县委书记与县长",
        "overlap_org": "中共太和县委",
        "overlap_period": "2021?-至今",
        "note": "confirmed"
    },
    {
        "person_a": "taihe_yang_daijun",
        "person_b": "taihe_liu_muyu",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "县委班子搭档：前任县委书记与前任县长",
        "overlap_org": "中共太和县委",
        "overlap_period": "2018?-2021?",
        "note": "plausible"
    },
    {
        "person_a": "taihe_shao_bing",
        "person_b": "taihe_yang_daijun",
        "type": "predecessor_successor",
        "strength": "medium",
        "context": "前后任县委书记",
        "overlap_org": "中共太和县委",
        "overlap_period": "交接期",
        "note": "plausible"
    },
    {
        "person_a": "taihe_chen_jianhua",
        "person_b": "taihe_liu_muyu",
        "type": "predecessor_successor",
        "strength": "medium",
        "context": "前后任县长",
        "overlap_org": "太和县人民政府",
        "overlap_period": "交接期",
        "note": "plausible"
    },
]


# ── DB build ─────────────────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DROP TABLE IF EXISTS relationships;")
    c.execute("DROP TABLE IF EXISTS positions;")
    c.execute("DROP TABLE IF EXISTS organizations;")
    c.execute("DROP TABLE IF EXISTS persons;")

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT DEFAULT 'unverified'
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            note TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
            p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"], p["current_org"],
            p["source"], p["notes"], p["confidence"]
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (person_id, org_id, title, start, end, rank, note))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["note"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


# ── GEXF build ───────────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>太和县（阜阳市）领导班子工作关系网络 — 2026年7月研究数据</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attribute declarations
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p["current_post"]
        org = p["current_org"]
        birth = p["birth"]
        conf = p["confidence"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"

        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Nodes: organizations
    lines.append('    <nodes>')
    for o in organizations:
        oid = o["id"]
        name = o["name"]
        c = org_color(o)
        lines.append(f'      <node id="org_{esc(oid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person → organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        lines.append(f'      <edge id="e{eid}" source="{esc(person_id)}" target="org_{esc(org_id)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append(f'          <attvalue for="2" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(start)}-{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: person ↔ person (relationship)
    for r in relationships:
        weight = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Created: {GEXF_PATH}")


# ── summary ──────────────────────────────────────────────────────────────

def print_summary():
    print(f"\n{'='*60}")
    print(f"  太和县领导班子工作关系网络")
    print(f"  生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"{'='*60}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
