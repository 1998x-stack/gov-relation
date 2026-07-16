#!/usr/bin/env python3
"""
北京市门头沟区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Mentougou District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjmtg.gov.cn (official leadership pages)
- Official news articles (2026-07-15 confirmed current officeholders)
- 百度百科 (partially accessible)

As-of date: 2026-07-16
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "门头沟区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "门头沟区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子 ──
    ("mtg_yu_huafeng", "喻华锋", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委书记", "中共北京市门头沟区委员会",
     "bjmtg.gov.cn/official"),

    ("mtg_lv_ming", "吕鸣", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、区长", "北京市门头沟区人民政府",
     "bjmtg.gov.cn/official"),

    # ── 其他常见区委常委（待确认名单） ──
    ("mtg_additional_1", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区委副书记（待确认）", "中共北京市门头沟区委员会",
     "待补充"),

    ("mtg_additional_2", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区委常委、常务副区长（待确认）", "北京市门头沟区人民政府",
     "待补充"),

    ("mtg_additional_3", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区委常委、纪委书记、监委主任（待确认）", "中共北京市门头沟区纪律检查委员会",
     "待补充"),

    ("mtg_additional_4", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区委常委、组织部部长（待确认）", "中共北京市门头沟区委组织部",
     "待补充"),

    ("mtg_additional_5", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区委常委、宣传部部长（待确认）", "中共北京市门头沟区委宣传部",
     "待补充"),

    ("mtg_additional_6", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区委常委、统战部部长（待确认）", "中共北京市门头沟区委统战部",
     "待补充"),

    ("mtg_additional_7", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区委常委、政法委书记（待确认）", "中共北京市门头沟区委政法委员会",
     "待补充"),

    # ── 前主要领导 ──
    ("mtg_predecessor_secretary", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "前任区委书记（待确认）", "已离任",
     "待补充"),

    ("mtg_predecessor_mayor", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "前任区长（待确认）", "已离任",
     "待补充"),

    # ── 人大主要领导 ──
    ("mtg_people_congress", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会主任（待确认）", "北京市门头沟区人民代表大会常务委员会",
     "待补充"),

    # ── 政协主要领导 ──
    ("mtg_cppcc", "待查", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区政协主席（待确认）", "中国人民政治协商会议北京市门头沟区委员会",
     "待补充"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("mtg_party_committee", "中共北京市门头沟区委员会", "党委", "地厅级", "中共北京市委", "北京市门头沟区"),
    ("mtg_gov", "北京市门头沟区人民政府", "政府", "地厅级", "北京市人民政府", "北京市门头沟区"),
    ("mtg_org_department", "中共北京市门头沟区委组织部", "党委部门", "正处级", "门头沟区委", "北京市门头沟区"),
    ("mtg_discipline", "中共北京市门头沟区纪律检查委员会", "纪委", "地厅级", "北京市纪委监委", "北京市门头沟区"),
    ("mtg_propaganda", "中共北京市门头沟区委宣传部", "党委部门", "正处级", "门头沟区委", "北京市门头沟区"),
    ("mtg_united_front", "中共北京市门头沟区委统战部", "党委部门", "正处级", "门头沟区委", "北京市门头沟区"),
    ("mtg_political_legal", "中共北京市门头沟区委政法委员会", "党委部门", "正处级", "门头沟区委", "北京市门头沟区"),
    ("mtg_party_school", "中共北京市门头沟区委党校", "党委部门", "正处级", "门头沟区委", "北京市门头沟区"),
    ("mtg_public_security", "北京市公安局门头沟分局", "公安", "正处级", "北京市公安局", "北京市门头沟区"),
    ("mtg_peoples_congress", "北京市门头沟区人民代表大会常务委员会", "人大", "地厅级", "北京市人大常委会", "北京市门头沟区"),
    ("mtg_cppcc", "中国人民政治协商会议北京市门头沟区委员会", "政协", "地厅级", "北京市政协", "北京市门头沟区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 喻华锋 — 区委书记 ═══
    ("mtg_yu_huafeng", "mtg_party_committee", "区委书记", "待查", "至今", "正厅级", "主持区委全面工作；2026年7月仍在任（bjmtg.gov.cn新闻确认）"),
    # 履历缺口
    ("mtg_yu_huafeng", "mtg_org_department", "履历缺口", "待查", "待查", "未知", "公开资料未找到完整履历"),

    # ═══ 吕鸣 — 区长 ═══
    ("mtg_lv_ming", "mtg_gov", "区长", "待查", "至今", "正厅级", "主持区政府全面工作；2026年7月仍在任（bjmtg.gov.cn新闻确认）"),
    ("mtg_lv_ming", "mtg_party_committee", "区委副书记", "待查", "至今", "正厅级", "兼任"),
    ("mtg_lv_ming", "mtg_org_department", "履历缺口", "待查", "待查", "未知", "公开资料未找到完整履历"),
]

# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 喻华锋 ↔ 吕鸣 — 党政正职搭档
    ("mtg_yu_huafeng", "mtg_lv_ming", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共北京市门头沟区委员会/门头沟区人民政府", "（2026年7月仍在任）"),
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
    if "区长" in post and "副" not in post:
        return "50,100,255"
    if "副书记" in post:
        return "255,100,100"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "常务副" in post:
        return "50,130,255"
    if "副区长" in post:
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
    if post_clean == "区委书记":
        return True
    if "区长" in post_clean and "副" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>北京市门头沟区领导班子工作关系网络</description>')
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
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    create_gexf()
    print("[DONE] Build complete.")
