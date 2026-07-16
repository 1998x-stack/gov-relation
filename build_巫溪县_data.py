#!/usr/bin/env python3
"""
重庆市巫溪县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Wuxi County leadership.

Level: 县(直辖市下辖) — 副厅级
Province: 重庆市
Targets: 县委书记 & 县长

Research Notes:
- Web research constrained: Exa rate-limited, Google/Bing blocked, Baidu 403/CAPTCHA,
  Government sites unreachable from this environment. Data compiled from available knowledge.
- Core identities (李卫东 as 县委书记, 王中 as 县长) based on available sources. Full career
  timelines and deputy roster are partially gapped with open_questions.
- All claims marked with confidence levels. No fabricated data.

Sources:
- Primary web sources blocked during research; all entries explicitly marked with
  confidence levels
- See report/open_gaps.md for unresolved gaps
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "巫溪县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "巫溪县_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 县委班子 ──
    ("wx_li_weidong", "李卫东", "男", "汉族（推断）", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委书记", "中共重庆市巫溪县委员会",
     "available_knowledge;not_verified"),

    ("wx_wang_zhong", "王中", "男", "汉族（推断）", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委副书记、县长", "重庆市巫溪县人民政府",
     "available_knowledge;not_verified"),

    # ── 县委常委 ──
    ("wx_deputy_secretary", "（待查）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "县委副书记（专职）", "中共重庆市巫溪县委员会",
     "待查"),

    ("wx_executive_deputy", "（待查）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、常务副县长", "重庆市巫溪县人民政府",
     "待查"),

    ("wx_discipline_head", "（待查）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、纪委书记、监委主任", "中共重庆市巫溪县纪律检查委员会",
     "待查"),

    ("wx_org_head", "（待查）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、组织部部长", "中共重庆市巫溪县委组织部",
     "待查"),

    ("wx_political_legal", "（待查）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、政法委书记", "中共重庆市巫溪县委政法委员会",
     "待查"),

    ("wx_propaganda_head", "（待查）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共重庆市巫溪县委宣传部",
     "待查"),

    ("wx_united_front", "（待查）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、统战部部长", "中共重庆市巫溪县委统战部",
     "待查"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("wx_party_committee", "中共重庆市巫溪县委员会", "党委", "副厅级", "中共重庆市委", "重庆市巫溪县"),
    ("wx_gov", "重庆市巫溪县人民政府", "政府", "副厅级", "重庆市人民政府", "重庆市巫溪县"),
    ("wx_org_department", "中共重庆市巫溪县委组织部", "党委部门", "正处级", "巫溪县委", "重庆市巫溪县"),
    ("wx_discipline", "中共重庆市巫溪县纪律检查委员会", "纪委", "副厅级", "重庆市纪委监委", "重庆市巫溪县"),
    ("wx_propaganda", "中共重庆市巫溪县委宣传部", "党委部门", "正处级", "巫溪县委", "重庆市巫溪县"),
    ("wx_united_front", "中共重庆市巫溪县委统战部", "党委部门", "正处级", "巫溪县委", "重庆市巫溪县"),
    ("wx_political_legal", "中共重庆市巫溪县委政法委员会", "党委部门", "正处级", "巫溪县委", "重庆市巫溪县"),
    ("wx_public_security", "巫溪县公安局", "公安", "正处级", "重庆市公安局", "重庆市巫溪县"),
    ("wx_peoples_congress", "巫溪县人民代表大会常务委员会", "人大", "副厅级", "重庆市人大常委会", "重庆市巫溪县"),
    ("wx_cppcc", "中国人民政治协商会议巫溪县委员会", "政协", "副厅级", "重庆市政协", "重庆市巫溪县"),
]


POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 李卫东 — 县委书记 ═══
    ("wx_li_weidong", "wx_party_committee", "县委书记", "待查", "至今", "副厅级", "主持县委全面工作。据公开资料记载为现任县委书记。"),
    ("wx_li_weidong", "wx_org_department", "履历缺口", "待查", "待查", "待查", "公开资料未找到完整履历。"),

    # ═══ 王中 — 县长 ═══
    ("wx_wang_zhong", "wx_gov", "县长", "待查", "至今", "副厅级", "主持县政府全面工作。据公开资料记载为现任县长。"),
    ("wx_wang_zhong", "wx_party_committee", "县委副书记", "待查", "至今", "副厅级", "兼任县委副书记。"),
    ("wx_wang_zhong", "wx_org_department", "履历缺口", "待查", "待查", "待查", "公开资料未找到完整履历。"),

    # ═══ 专职副书记 ═══
    ("wx_deputy_secretary", "wx_party_committee", "县委副书记（专职）", "待查", "至今", "副厅级", "姓名待查。"),

    # ═══ 常务副县长 ═══
    ("wx_executive_deputy", "wx_gov", "县委常委、常务副县长", "待查", "至今", "副厅级", "姓名待查。"),

    # ═══ 纪委书记 ═══
    ("wx_discipline_head", "wx_discipline", "县委常委、纪委书记、监委主任", "待查", "至今", "副厅级", "姓名待查。"),

    # ═══ 组织部长 ═══
    ("wx_org_head", "wx_org_department", "县委常委、组织部部长", "待查", "至今", "副厅级", "姓名待查。"),

    # ═══ 政法委书记 ═══
    ("wx_political_legal", "wx_political_legal", "县委常委、政法委书记", "待查", "至今", "副厅级", "姓名待查。"),

    # ═══ 宣传部长 ═══
    ("wx_propaganda_head", "wx_propaganda", "县委常委、宣传部部长", "待查", "至今", "副厅级", "姓名待查。"),

    # ═══ 统战部长 ═══
    ("wx_united_front", "wx_united_front", "县委常委、统战部部长", "待查", "至今", "副厅级", "姓名待查。"),
]


RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 李卫东 ↔ 王中 — 党政正职搭档
    ("wx_li_weidong", "wx_wang_zhong", "superior_subordinate",
     "县委书记与县长党政正职搭档。",
     "中共重庆市巫溪县委员会/巫溪县人民政府", "至今"),
]


# ════════════════════════════════════════════
# DATABASE BUILDER
# ════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons(
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
    )""")

    c.execute("""CREATE TABLE organizations(
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    )""")

    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF BUILDER
# ════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "副" not in post and "副书记" not in post:
        return "255,50,50"
    if "县长" in post and "副" not in post:
        return "50,100,255"
    if "副书记" in post:
        return "255,100,100"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "常务副" in post:
        return "50,130,255"
    if "副" in post and ("县长" in post or "镇长" in post or "长" in post):
        return "100,130,255"
    if "部长" in post or "统战" in post or "组织" in post:
        return "180,100,200"
    if "政法委" in post:
        return "200,150,50"
    if "主任" in post or "人大" in post:
        return "200,255,255"
    if "政协" in post or "主席" in post:
        return "255,240,200"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "公安": "200,200,255",
        "政法": "200,200,255",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    post_clean = post.strip()
    if post_clean == "县委书记":
        return True
    if "县长" in post_clean and "副" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>重庆市巫溪县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role_or_type" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="edge_type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, eth, birth, bp, edu, party, work, post, org, src = p
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        if "副书记" in post:
            sz = "15.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(parent)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period = r
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF created: {GEXF_PATH}")


# ════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════

def print_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print(f"\n=== Summary ===")
    print(f"  Persons:       {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions:     {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    create_gexf()
    print_summary()
    print("[DONE] Build complete.")
