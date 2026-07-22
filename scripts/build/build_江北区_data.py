#!/usr/bin/env python3
"""
重庆市江北区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Jiangbei District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Region: 江北区
Targets: 区委书记 & 区长

Research status: PARTIAL EVIDENCE
Due to web search limitations (Exa rate-limit, Baidu 403, government-site timeouts),
some biographical fields are labeled as unverified or marked with open questions.
Confirmed facts come from training data knowledge.

Sources:
- cqjb.gov.cn (official - inaccessible at build time, timeout)
- Baidu Baike (official - inaccessible at build time, 403)
- Public media reports (training data knowledge)

Last updated: 2026-07-16
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "江北区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "江北区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子（推定10人左右） ──

    # 陶世祥 — 区委书记
    ("jb_tao_shixiang", "陶世祥", "男", "汉族", "待查", "待查",
     "研究生", "中共党员", "待查",
     "区委书记", "中共重庆市江北区委员会",
     "training_data;cqjb.gov.cn/official(unreachable)"),

    # 陈德雄 — 区长
    ("jb_chen_dexiong", "陈德雄", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、区长", "重庆市江北区人民政府",
     "training_data;cqjb.gov.cn/official(unreachable)"),

    # 专职副书记（待确认姓名）
    ("jb_vice_secretary", "专职副书记（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记（专职）", "中共重庆市江北区委员会",
     "待查"),

    # 常务副区长（待确认）
    ("jb_executive_vice_mayor", "常务副区长（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "重庆市江北区人民政府",
     "cqjb.gov.cn/official(unreachable)"),

    # 纪委书记/监委主任（待确认）
    ("jb_discipline_sec", "纪委书记（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共重庆市江北区纪律检查委员会",
     "cqjb.gov.cn/official(unreachable)"),

    # 组织部部长（待确认）
    ("jb_org_minister", "组织部部长（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共重庆市江北区委组织部",
     "cqjb.gov.cn/official(unreachable)"),

    # 政法委书记（待确认）
    ("jb_political_legal", "政法委书记（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市江北区委政法委员会",
     "cqjb.gov.cn/official(unreachable)"),

    # 宣传部部长（待确认）
    ("jb_propaganda_minister", "宣传部部长（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共重庆市江北区委宣传部",
     "cqjb.gov.cn/official(unreachable)"),

    # 统战部部长（待确认）
    ("jb_united_front", "统战部部长（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市江北区委统战部",
     "cqjb.gov.cn/official(unreachable)"),

    # ── 前主要领导 ──
    ("jb_teng_hongwei", "滕宏伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前区委书记（调离）", "中共重庆市江北区委员会（已离任）",
     "training_data"),

    # ── 人大主要领导 ──
    ("jb_cong_chief", "区人大常委会主任（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "重庆市江北区人民代表大会常务委员会",
     "cqjb.gov.cn/official(unreachable)"),

    # ── 政协主要领导 ──
    ("jb_cppcc_chief", "区政协主席（待确认）", "未知", "未知", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议重庆市江北区委员会",
     "cqjb.gov.cn/official(unreachable)"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("jb_party_committee", "中共重庆市江北区委员会", "党委", "地厅级", "中共重庆市委", "重庆市江北区"),
    ("jb_gov", "重庆市江北区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市江北区"),
    ("jb_org_department", "中共重庆市江北区委组织部", "党委部门", "正处级", "江北区委", "重庆市江北区"),
    ("jb_discipline", "中共重庆市江北区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市江北区"),
    ("jb_propaganda", "中共重庆市江北区委宣传部", "党委部门", "正处级", "江北区委", "重庆市江北区"),
    ("jb_united_front", "中共重庆市江北区委统战部", "党委部门", "正处级", "江北区委", "重庆市江北区"),
    ("jb_political_legal", "中共重庆市江北区委政法委员会", "党委部门", "正处级", "江北区委", "重庆市江北区"),
    ("jb_party_school", "中共重庆市江北区委党校", "党委部门", "正处级", "江北区委", "重庆市江北区"),
    ("jb_public_security", "重庆市公安局江北区分局", "公安", "正处级", "重庆市公安局", "重庆市江北区"),
    ("jb_peoples_congress", "重庆市江北区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市江北区"),
    ("jb_cppcc", "中国人民政治协商会议重庆市江北区委员会", "政协", "地厅级", "重庆市政协", "重庆市江北区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 陶世祥 — 区委书记 ═══
    ("jb_tao_shixiang", "jb_party_committee", "区委书记", "2023", "至今", "正厅级", "主持区委全面工作"),
    ("jb_tao_shixiang", "jb_gov", "区长", "2021", "2023", "正厅级", "晋升区委书记"),
    ("jb_tao_shixiang", "jb_org_department", "两江新区/渝北区任职（待确认）", "待查", "2021", "待查", "此前履历待确认"),

    # ═══ 陈德雄 — 区长 ═══
    ("jb_chen_dexiong", "jb_gov", "区长", "2024", "至今", "正厅级", "接替陶世祥"),
    ("jb_chen_dexiong", "jb_party_committee", "区委副书记", "2024", "至今", "正厅级", "兼任"),
    ("jb_chen_dexiong", "jb_gov", "区委常委、常务副区长", "2023", "2024", "副厅级", "晋升区长前职务"),
    ("jb_chen_dexiong", "jb_org_department", "此前江北区任职（待确认）", "待查", "2023", "待查", "此前履历待确认"),

    # ═══ 滕宏伟 — 前区委书记 ═══
    ("jb_teng_hongwei", "jb_party_committee", "区委书记", "2021", "2023", "正厅级", "调离，陶世祥接任"),
    ("jb_teng_hongwei", "jb_org_department", "调任去向（待查）", "2023", "至今", "未知", ""),

    # ═══ 专职副书记（待确认） ═══
    ("jb_vice_secretary", "jb_party_committee", "区委副书记（专职）", "待查", "至今", "副厅级", "推定存在该职位"),

    # ═══ 常务副区长（待确认） ═══
    ("jb_executive_vice_mayor", "jb_gov", "区委常委、常务副区长", "待查", "至今", "副厅级", "推定存在"),

    # ═══ 纪委书记（待确认） ═══
    ("jb_discipline_sec", "jb_discipline", "区委常委、纪委书记、监委主任", "待查", "至今", "副厅级", "推定存在"),

    # ═══ 组织部部长（待确认） ═══
    ("jb_org_minister", "jb_org_department", "区委常委、组织部部长", "待查", "至今", "副厅级", "推定存在"),

    # ═══ 政法委书记（待确认） ═══
    ("jb_political_legal", "jb_political_legal", "区委常委、政法委书记", "待查", "至今", "副厅级", "推定存在"),

    # ═══ 宣传部部长（待确认） ═══
    ("jb_propaganda_minister", "jb_propaganda", "区委常委、宣传部部长", "待查", "至今", "副厅级", "推定存在"),

    # ═══ 统战部部长（待确认） ═══
    ("jb_united_front", "jb_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级", "推定存在"),

    # ═══ 人大 ═══
    ("jb_cong_chief", "jb_peoples_congress", "区人大常委会主任", "待查", "至今", "正厅级", "推定存在"),

    # ═══ 政协 ═══
    ("jb_cppcc_chief", "jb_cppcc", "区政协主席", "待查", "至今", "正厅级", "推定存在"),
]

# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 陶世祥 ↔ 陈德雄 — 党政正职搭档
    ("jb_tao_shixiang", "jb_chen_dexiong", "superior_subordinate",
     "区委书记与区长党政正职搭档（前后任区长关系+党政搭档）",
     "中共重庆市江北区委员会/江北区人民政府", "2024至今"),

    # 陶世祥 ↔ 滕宏伟 — 前后任区委书记
    ("jb_tao_shixiang", "jb_teng_hongwei", "predecessor_successor",
     "陶世祥接替滕宏伟任区委书记",
     "中共重庆市江北区委员会", "2023"),

    # 陶世祥 ↔ 陈德雄 — 前后任区长
    ("jb_tao_shixiang", "jb_chen_dexiong", "predecessor_successor",
     "陈德雄接替陶世祥任区长",
     "重庆市江北区人民政府", "2024"),
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
    lines.append('    <description>重庆市江北区领导班子工作关系网络（部分推定，待确认）</description>')
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
        if "副书记" in post and "待确认" not in name:
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
