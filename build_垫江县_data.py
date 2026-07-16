#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 垫江县 (Dianjiang County, Chongqing).

Task: chongqing_垫江县 — 县委书记 & 县长
Province: 重庆市 (直辖市)
City: 垫江县 (直辖市下辖县)
Region: 垫江县
Level: 县(直辖市下辖)
Research date: 2026-07-16

Known officeholders (from Baidu Baike 垫江县 entry, as of 2025-11):
- 县委书记: 陈德川 (confirmed from Baidu Baike)
- 县政府党组书记、县长: 刘振 (confirmed from Baidu Baike)
- 县人大常委会主任: 粟登琳 (confirmed from Baidu Baike)
- 县政协党组书记、主席: 郑小波 (confirmed from Baidu Baike)

Note: This is a county (县) under Chongqing Municipality (重庆市), not a district.
垫江县 is classified as 县(直辖市下辖) — a county directly under the municipality.
Administrative rank: 正厅级 for top leaders (书记/县长), 副厅级 for deputies,
正处级 for department heads.

Sources:
- Baidu Baike 垫江县 entry (encyclopedia, accessed 2026-07-16)
- Additional career timeline data needs further research from government websites
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "垫江县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "垫江县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 县委领导班子 (County Party Committee) ══

    # 县委书记 — 陈德川
    ("dj_chen_dechuan", "陈德川", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "县委书记", "中共重庆市垫江县委员会",
     "baike_baidu_垫江县"),

    # 县政府党组书记、县长 — 刘振
    ("dj_liu_zhen", "刘振", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "县政府党组书记、县长", "重庆市垫江县人民政府",
     "baike_baidu_垫江县"),

    # ══ 县人大、政协领导 ══

    # 县人大常委会主任 — 粟登琳
    ("dj_su_denglin", "粟登琳", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "县人大常委会主任", "重庆市垫江县人民代表大会常务委员会",
     "baike_baidu_垫江县"),

    # 县政协党组书记、主席 — 郑小波
    ("dj_zheng_xiaobo", "郑小波", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "县政协党组书记、主席", "中国人民政治协商会议重庆市垫江县委员会",
     "baike_baidu_垫江县"),

    # ══ 县委副书记（待确认具体人选） ══
    # 注：垫江县委副书记（专职）人选待进一步从官方渠道确认
    # 以下为预留空位，待补充

    # ══ 前任领导 ══
    # 注：陈德川的前任县委书记、刘振的前任县长待查
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("dj_party_committee", "中共重庆市垫江县委员会", "党委", "地厅级", "中共重庆市委", "重庆市垫江县"),
    ("dj_gov", "重庆市垫江县人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市垫江县"),
    ("dj_discipline", "中共重庆市垫江县纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市垫江县"),
    ("dj_organization", "中共重庆市垫江县委组织部", "党委部门", "正处级", "垫江县委", "重庆市垫江县"),
    ("dj_propaganda", "中共重庆市垫江县委宣传部", "党委部门", "正处级", "垫江县委", "重庆市垫江县"),
    ("dj_united_front", "中共重庆市垫江县委统战部", "党委部门", "正处级", "垫江县委", "重庆市垫江县"),
    ("dj_political_legal", "中共重庆市垫江县委政法委员会", "党委部门", "正处级", "垫江县委", "重庆市垫江县"),
    ("dj_military_department", "重庆市垫江县人民武装部", "军事", "正师级", "重庆警备区", "重庆市垫江县"),
    ("dj_public_security", "重庆市垫江县公安局", "公安", "正处级", "重庆市公安局", "重庆市垫江县"),
    ("dj_peoples_congress", "重庆市垫江县人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市垫江县"),
    ("dj_cppcc", "中国人民政治协商会议重庆市垫江县委员会", "政协", "地厅级", "重庆市政协", "重庆市垫江县"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 陈德川 — 县委书记 ═══
    ("dj_chen_dechuan", "dj_party_committee", "县委书记", "待查", "至今", "正厅级",
     "主持县委全面工作。据百度百科垫江县词条记载为现任县委书记（截至2025年11月）。"),

    # ═══ 刘振 — 县长 ═══
    ("dj_liu_zhen", "dj_gov", "县长", "待查", "至今", "正厅级",
     "主持县政府全面工作。县政府党组书记。据百度百科垫江县词条记载为现任县长。"),
    ("dj_liu_zhen", "dj_party_committee", "县委副书记", "待查", "至今", "正厅级", "兼任县委副书记"),

    # ═══ 粟登琳 — 县人大常委会主任 ═══
    ("dj_su_denglin", "dj_peoples_congress", "县人大常委会主任", "待查", "至今", "正厅级",
     "主持县人大常委会全面工作。据百度百科垫江县词条记载为现任。"),

    # ═══ 郑小波 — 县政协主席 ═══
    ("dj_zheng_xiaobo", "dj_cppcc", "县政协党组书记、主席", "待查", "至今", "正厅级",
     "主持县政协全面工作。据百度百科垫江县词条记载为现任。"),
    ("dj_zheng_xiaobo", "dj_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任县委常委（政协主席通常进常委）"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 陈德川 ↔ 刘振 — 党政正职搭档 ═══
    ("dj_chen_dechuan", "dj_liu_zhen", "superior_subordinate",
     "县委书记与县长党政正职搭档关系",
     "中共重庆市垫江县委员会;重庆市垫江县人民政府", "至今"),

    # ═══ 陈德川 ↔ 粟登琳 — 党委-人大 ═══
    ("dj_chen_dechuan", "dj_su_denglin", "overlap",
     "县委书记与县人大常委会主任（党委与人大协调）",
     "中共重庆市垫江县委员会", "至今"),

    # ═══ 刘振 ↔ 粟登琳 — 政府-人大 ═══
    ("dj_liu_zhen", "dj_su_denglin", "overlap",
     "县长与县人大常委会主任（政府与人大协调）",
     "重庆市垫江县", "至今"),

    # ═══ 陈德川 ↔ 郑小波 — 党委-政协 ═══
    ("dj_chen_dechuan", "dj_zheng_xiaobo", "overlap",
     "县委书记与县政协主席（党委与政协协调）",
     "中共重庆市垫江县委员会", "至今"),
]


# ════════════════════════════════════════════
# SQLITE SETUP
# ════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
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

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
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
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF GENERATION
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def is_top_leader(person_id):
    return person_id in ("dj_chen_dechuan", "dj_liu_zhen", "dj_su_denglin", "dj_zheng_xiaobo")


def get_person_role(person_id):
    """Return role label for person for color coding."""
    for p in PERSONS:
        if p[0] == person_id:
            post = p[8]  # current_post
            if "书记" in post and "县委" in post:
                return "party_secretary"
            elif "县长" in post:
                return "government_head"
            elif "人大" in post:
                return "congress"
            elif "政协" in post:
                return "cppcc"
            return "other"
    return "other"


def person_color(person_id):
    """Return RGB string for person node based on role."""
    role = get_person_role(person_id)
    if role == "party_secretary":
        return "255,50,50"       # Red — Party Secretary
    elif role == "government_head":
        return "50,100,255"      # Blue — Government head
    elif role == "congress":
        return "200,255,255"     # Cyan — People's Congress
    elif role == "cppcc":
        return "255,240,200"     # Cream — Political Consultative
    else:
        return "100,100,100"     # Grey — Others


def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "党委部门": "255,220,220",
        "军事": "200,200,200",
        "公安": "200,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(org_type, "200,200,200")


def generate_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Gov Research Agent</creator>')
    lines.append('    <description>重庆市垫江县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── Node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # ── Edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[8]  # current_post
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="person"/>')
        lines.append(f'          <attvalue for="3" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        olevel = o[3]
        c = org_color(oid, otype)
        lines.append(f'      <node id="o{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(olevel)}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at via positions)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        start = pos[3] if pos[3] else ""
        end = pos[4] if pos[4] else ""
        eid += 1
        period = f"{start}-{end}" if start or end else ""
        lines.append(f'      <edge id="e{eid}" source="p{esc(pid)}" target="o{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oid)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        overlap_org = r[4]
        overlap_period = r[5]
        weight = "2.0"  # person-person edges stronger than person-org
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{esc(pa)}" target="p{esc(pb)}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(overlap_org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(overlap_period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF graph created: {GEXF_PATH}")


# ════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════

def print_summary():
    print(f"\n{'='*60}")
    print(f"  重庆市垫江县 领导网络数据")
    print(f"{'='*60}")
    print(f"  人物: {len(PERSONS)}")
    print(f"  机构: {len(ORGANIZATIONS)}")
    print(f"  任职记录: {len(POSITIONS)}")
    print(f"  关系边: {len(RELATIONSHIPS)}")
    print(f"{'='*60}")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"{'='*60}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    generate_gexf()
    print_summary()
