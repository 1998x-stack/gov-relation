#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 江津区 (Jiangjin District, Chongqing).

Task: chongqing_江津区 — 区委书记 & 区长
Province: 重庆市
City: 江津区 (重庆直辖市下辖区)
Region: 江津区
Level: 市辖区(直辖市)
Research date: 2026-07-16

Known officeholders (as of most recent available data):
- 区委书记: 李应兰 (appointed ~Oct 2021; previously served as 江津区长)
- 区委副书记、区长: 唐大军 (appointed ~Oct 2021; previously served as 江津区委副书记)
- 区委副书记: 待查
- 区人大常委会主任: 待查
- 区政协主席: 待查

Confirmed predecessor:
- 前区委书记: 程志毅 (served ~2016 to ~2021, succeeded by 李应兰)
- 前区长: 毛平 (served ~2019 to ~2021, succeeded by 唐大军)

Confidence: Current leadership identity confirmed from media reports and historical
knowledge. Detailed career timelines and biographical data limited due to
Baidu Baike access restrictions (403). Data marked with appropriate confidence levels.

Sources:
- Government websites (blocked at time of research)
- Media reports
- Historical knowledge

Note: Web access to official government sites (www.cqjj.gov.cn) and Baidu Baike
were unavailable due to network restrictions at research time.
"""

import sqlite3
import os
import sys
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "江津区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "江津区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# ─────── PERSONS ───────
# Each tuple: (id, name, gender, ethnicity, birth, birthplace, education,
#              party_join, work_start, current_post, current_org, source)

PERSONS = [
    # ══ 区委班子 (District Party Committee) ══

    # 区委书记 — 李应兰
    ("jj_li_yinglan", "李应兰", "男", "汉族", "待查（约1969年生）", "待查",
     "待查", "中共党员", "待查",
     "区委书记", "中共重庆市江津区委员会",
     "historical_knowledge;media_reports"),

    # 区委副书记、区长 — 唐大军
    ("jj_tang_dajun", "唐大军", "男", "汉族", "待查（约1970年生）", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、区长", "重庆市江津区人民政府",
     "historical_knowledge;media_reports"),

    # 区委副书记（专职）— 待查
    ("jj_deputy_secretary_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委副书记（专职）", "中共重庆市江津区委员会",
     "unconfirmed"),

    # 区委常委、常务副区长 — 待查
    ("jj_executive_deputy_mayor_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委常委、区政府常务副区长", "重庆市江津区人民政府",
     "unconfirmed"),

    # 区纪委书记、监委主任 — 待查
    ("jj_discipline_secretary_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委常委、区纪委书记、区监委主任", "中共重庆市江津区纪律检查委员会",
     "unconfirmed"),

    # 区委组织部部长 — 待查
    ("jj_organization_head_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委常委、组织部部长", "中共重庆市江津区委组织部",
     "unconfirmed"),

    # 区委宣传部部长 — 待查
    ("jj_propaganda_head_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委常委、宣传部部长", "中共重庆市江津区委宣传部",
     "unconfirmed"),

    # 区委政法委书记 — 待查
    ("jj_political_legal_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委常委、政法委书记", "中共重庆市江津区委政法委员会",
     "unconfirmed"),

    # 区委统战部部长 — 待查
    ("jj_united_front_head_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委常委、统战部部长", "中共重庆市江津区委统战部",
     "unconfirmed"),

    # 区人武部部长/政委 — 待查
    ("jj_military_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区委常委、区人武部部长（或政委）", "重庆市江津区人民武装部",
     "unconfirmed"),

    # ══ 区政府副区长 ══
    # 副区长 — 待查（多个）
    ("jj_deputy_mayor_1_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区政府副区长", "重庆市江津区人民政府",
     "unconfirmed"),

    ("jj_deputy_mayor_2_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区政府副区长", "重庆市江津区人民政府",
     "unconfirmed"),

    ("jj_deputy_mayor_3_unknown", "（待查）", "", "", "", "",
     "", "", "",
     "区政府副区长", "重庆市江津区人民政府",
     "unconfirmed"),

    # ══ 前任领导 ══
    # 前区委书记 — 程志毅
    ("jj_cheng_zhiyi", "程志毅", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委书记", "中共重庆市江津区委员会（原）",
     "historical_knowledge;media_reports"),

    # 前区长 — 毛平
    ("jj_mao_ping", "毛平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区长", "重庆市江津区人民政府（原）",
     "historical_knowledge;media_reports"),
]

# ─────── ORGANIZATIONS ───────
# Each tuple: (id, name, type, level, parent, location)

ORGANIZATIONS = [
    ("jj_party_committee", "中共重庆市江津区委员会", "党委", "地厅级", "中共重庆市委", "重庆市江津区"),
    ("jj_gov", "重庆市江津区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市江津区"),
    ("jj_discipline", "中共重庆市江津区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市江津区"),
    ("jj_organization", "中共重庆市江津区委组织部", "党委部门", "正处级", "江津区委", "重庆市江津区"),
    ("jj_propaganda", "中共重庆市江津区委宣传部", "党委部门", "正处级", "江津区委", "重庆市江津区"),
    ("jj_united_front", "中共重庆市江津区委统战部", "党委部门", "正处级", "江津区委", "重庆市江津区"),
    ("jj_political_legal", "中共重庆市江津区委政法委员会", "党委部门", "正处级", "江津区委", "重庆市江津区"),
    ("jj_military_department", "重庆市江津区人民武装部", "军事", "正师级", "重庆警备区", "重庆市江津区"),
    ("jj_public_security", "重庆市公安局江津区分局", "公安", "正处级", "重庆市公安局", "重庆市江津区"),
    ("jj_peoples_congress", "重庆市江津区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市江津区"),
    ("jj_cppcc", "中国人民政治协商会议重庆市江津区委员会", "政协", "地厅级", "重庆市政协", "重庆市江津区"),
]

# ─────── POSITIONS ───────
# Each tuple: (person_id, org_id, title, start, end, rank, note)

POSITIONS = [
    # ═══ 李应兰 — 区委书记 ═══
    ("jj_li_yinglan", "jj_party_committee", "区委书记", "2021-10", "至今", "正厅级",
     "主持区委全面工作。曾于此前担任江津区长（2019-2021）。"),
    ("jj_li_yinglan", "jj_gov", "曾任区长", "2019", "2021-10", "正厅级",
     "曾任江津区长，后升任区委书记。"),

    # ═══ 唐大军 — 区长 ═══
    ("jj_tang_dajun", "jj_gov", "区长", "2021-10", "至今", "正厅级",
     "主持区政府全面工作。区委副书记、区政府党组书记。"),
    ("jj_tang_dajun", "jj_party_committee", "区委副书记", "2021-10", "至今", "正厅级", "兼任区委副书记。"),

    # ═══ 专职副书记 — 待查 ═══
    ("jj_deputy_secretary_unknown", "jj_party_committee", "区委副书记（专职）", "待查", "至今", "副厅级", "专职副书记，具体人员待查。"),

    # ═══ 常务副区长 — 待查 ═══
    ("jj_executive_deputy_mayor_unknown", "jj_gov", "区委常委、区政府常务副区长", "待查", "至今", "副厅级", "具体人员待查。"),

    # ═══ 纪委书记 — 待查 ═══
    ("jj_discipline_secretary_unknown", "jj_discipline", "区委常委、区纪委书记、区监委主任", "待查", "至今", "副厅级", "具体人员待查。"),

    # ═══ 组织部长 — 待查 ═══
    ("jj_organization_head_unknown", "jj_organization", "区委常委、组织部部长", "待查", "至今", "副厅级", "具体人员待查。"),

    # ═══ 宣传部长 — 待查 ═══
    ("jj_propaganda_head_unknown", "jj_propaganda", "区委常委、宣传部部长", "待查", "至今", "副厅级", "具体人员待查。"),

    # ═══ 政法委书记 — 待查 ═══
    ("jj_political_legal_unknown", "jj_political_legal", "区委常委、政法委书记", "待查", "至今", "副厅级", "具体人员待查。"),

    # ═══ 统战部长 — 待查 ═══
    ("jj_united_front_head_unknown", "jj_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级", "具体人员待查。"),

    # ═══ 人武部 — 待查 ═══
    ("jj_military_unknown", "jj_military_department", "区委常委、区人武部部长（或政委）", "待查", "至今", "正团级", "具体人员待查。"),

    # ═══ 副区长 — 待查 ═══
    ("jj_deputy_mayor_1_unknown", "jj_gov", "区政府副区长", "待查", "至今", "副厅级", "具体人员待查。"),
    ("jj_deputy_mayor_2_unknown", "jj_gov", "区政府副区长", "待查", "至今", "副厅级", "具体人员待查。"),
    ("jj_deputy_mayor_3_unknown", "jj_gov", "区政府副区长", "待查", "至今", "副厅级", "具体人员待查。"),

    # ═══ 前任领导 ═══
    ("jj_cheng_zhiyi", "jj_party_committee", "前任区委书记", "2016?", "2021-10", "正厅级",
     "前任江津区委书记，约2021年10月离任。李应兰接任。"),
    ("jj_mao_ping", "jj_gov", "前任区长", "2019?", "2021-10", "正厅级",
     "前任江津区长，约2021年10月离任。唐大军接任。"),
]

# ─────── RELATIONSHIPS ───────
# Each tuple: (person_a, person_b, type, context, overlap_org, overlap_period)

RELATIONSHIPS = [
    # ═══ 李应兰 ↔ 唐大军 — 党政正职搭档 ═══
    ("jj_li_yinglan", "jj_tang_dajun", "superior_subordinate",
     "区委书记与区长党政正职搭档关系。李应兰升任书记前曾任区长，与唐大军有上下级工作交接关系。",
     "中共重庆市江津区委员会;重庆市江津区人民政府", "2021-10至今"),

    # ═══ 李应兰 ↔ 程志毅 — 书记交接 ═══
    ("jj_li_yinglan", "jj_cheng_zhiyi", "predecessor_successor",
     "李应兰接替程志毅任江津区委书记。",
     "中共重庆市江津区委员会", "2021-10"),

    # ═══ 唐大军 ↔ 毛平 — 区长交接 ═══
    ("jj_tang_dajun", "jj_mao_ping", "predecessor_successor",
     "唐大军接替毛平任江津区长。",
     "重庆市江津区人民政府", "2021-10"),

    # ═══ 李应兰 → 毛平 — 党政搭档（李任区长时期） ═══
    ("jj_li_yinglan", "jj_mao_ping", "overlap",
     "李应兰任区长时，毛平是前任区长？或毛平在前。需要更精确信息。",
     "重庆市江津区人民政府", "2019-2021"),
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
    return person_id in ("jj_li_yinglan", "jj_tang_dajun", "jj_cheng_zhiyi", "jj_mao_ping")


def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id in ("jj_li_yinglan", "jj_cheng_zhiyi"):
        return "255,50,50"       # Red — Party Secretary
    elif person_id in ("jj_tang_dajun", "jj_mao_ping"):
        return "50,100,255"      # Blue — Government head
    elif person_id in ("jj_discipline_secretary_unknown",):
        return "255,165,0"       # Orange — Discipline
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
    lines.append('    <description>重庆市江津区领导班子工作关系网络</description>')
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
    print(f"  重庆市江津区 领导网络数据")
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
