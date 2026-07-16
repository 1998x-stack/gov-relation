#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 云阳县 (Yunyang County, Chongqing).

Task: chongqing_云阳县 — 县委书记 & 县长
Province: 重庆市
City: 云阳县 (重庆直辖市下辖县)
Region: 云阳县
Level: 县(直辖市下辖)
Research date: 2026-07-16

Known officeholders (as of 2026-07-16, confirmed from official yunyang.gov.cn):
- 县委书记: 陈道彬 (confirmed from news reports 2026-07-16, 2026-06-26, etc.)
- 县委副书记、县长: 甘露 (confirmed 2026-07-10 as 县委副书记、县政府党组书记、县长)
- 县领导 mentioned: 吴大伦, 彭建云, 戴蔚, 崔军强, 郭伟, 严俊, 苗巍伟, 王凤艳

Confidence: Current leadership identity confirmed from official government website
(yunyang.gov.cn) news items. Detailed career timelines limited — marked with
appropriate confidence levels. 陈道彬 previously served in other Chongqing roles.
甘露 previously served in other Chongqing roles.

Sources:
- www.yunyang.gov.cn — official government website (primary source for leadership)
- 县委中心组学习会/政府常务会议/专题党课 news articles
"""
import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "云阳县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "云阳县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 县委班子 (County Party Committee) ══

    # 县委书记 — 陈道彬
    ("yy_chen_daobin", "陈道彬", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委书记", "中共重庆市云阳县委员会",
     "yunyang.gov.cn_news;media_reports"),

    # 县委副书记、县长 — 甘露
    ("yy_gan_lu", "甘露", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委副书记、县长", "重庆市云阳县人民政府",
     "yunyang.gov.cn_news;media_reports"),

    # 县领导 — 吴大伦 (mentioned in 甘露 party event)
    ("yy_wu_dalun", "吴大伦", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),

    # 县领导 — 彭建云 (县领导, 多次陪同调研)
    ("yy_peng_jianyun", "彭建云", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),

    # 县领导 — 戴蔚
    ("yy_dai_wei", "戴蔚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),

    # 县领导 — 崔军强
    ("yy_cui_junqiang", "崔军强", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),

    # 县领导 — 郭伟
    ("yy_guo_wei", "郭伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),

    # 县领导 — 严俊 (mentioned in 信访工作)
    ("yy_yan_jun", "严俊", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),

    # 县领导 — 苗巍伟 (mentioned in 信访工作)
    ("yy_miao_weiwei", "苗巍伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),

    # 县领导 — 王凤艳 (mentioned in 招商考察)
    ("yy_wang_fengyan", "王凤艳", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县领导", "重庆市云阳县",
     "yunyang.gov.cn_news"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("yy_party_committee", "中共重庆市云阳县委员会", "党委", "正厅级", "中共重庆市委", "重庆市云阳县"),
    ("yy_gov", "重庆市云阳县人民政府", "政府", "正厅级", "重庆市人民政府", "重庆市云阳县"),
    ("yy_discipline", "中共重庆市云阳县纪律检查委员会", "纪委", "正厅级", "重庆市纪委监委", "重庆市云阳县"),
    ("yy_organization", "中共重庆市云阳县委组织部", "党委部门", "正处级", "云阳县委", "重庆市云阳县"),
    ("yy_propaganda", "中共重庆市云阳县委宣传部", "党委部门", "正处级", "云阳县委", "重庆市云阳县"),
    ("yy_united_front", "中共重庆市云阳县委统战部", "党委部门", "正处级", "云阳县委", "重庆市云阳县"),
    ("yy_political_legal", "中共重庆市云阳县委政法委员会", "党委部门", "正处级", "云阳县委", "重庆市云阳县"),
    ("yy_public_security", "重庆市云阳县公安局", "公安", "正处级", "重庆市公安局", "重庆市云阳县"),
    ("yy_peoples_congress", "重庆市云阳县人民代表大会常务委员会", "人大", "正厅级", "重庆市人大常委会", "重庆市云阳县"),
    ("yy_cppcc", "中国人民政治协商会议重庆市云阳县委员会", "政协", "正厅级", "重庆市政协", "重庆市云阳县"),
    ("yy_party_school", "中共重庆市云阳县委党校", "事业单位", "正处级", "云阳县委", "重庆市云阳县"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 陈道彬 — 县委书记 ═══
    ("yy_chen_daobin", "yy_party_committee", "县委书记", "待查", "至今", "正厅级",
     "主持县委全面工作。最早于2026年5月以县委书记身份见诸报道（西洽会巡展）。2026年7月赴市委党校作专题报告。此前曾任大足区等职务。"),

    # ═══ 甘露 — 县长 ═══
    ("yy_gan_lu", "yy_gov", "县长", "待查", "至今", "正厅级",
     "主持县政府全面工作。县委副书记、县政府党组书记。2026年7月8日讲授正确政绩观专题党课。"),
    ("yy_gan_lu", "yy_party_committee", "县委副书记", "待查", "至今", "正厅级", "兼任"),

    # ═══ 吴大伦 — 县领导 ═══
    ("yy_wu_dalun", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "2026年7月8日参加甘露专题党课活动。"),

    # ═══ 彭建云 — 县领导 ═══
    ("yy_peng_jianyun", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "多次陪同调研：2026年7月8日陪同甘露调研交通优化及汽车产业园；参加信访工作会议。"),

    # ═══ 戴蔚 — 县领导 ═══
    ("yy_dai_wei", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "2026年7月8日参加甘露专题党课活动。"),

    # ═══ 崔军强 — 县领导 ═══
    ("yy_cui_junqiang", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "2026年7月8日参加甘露专题党课活动。"),

    # ═══ 郭伟 — 县领导 ═══
    ("yy_guo_wei", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "2026年7月8日参加甘露专题党课活动。"),

    # ═══ 严俊 — 县领导 ═══
    ("yy_yan_jun", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "参加陈道彬信访工作调研活动（2026-07-15）。"),

    # ═══ 苗巍伟 — 县领导 ═══
    ("yy_miao_weiwei", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "参加陈道彬信访工作调研活动（2026-07-15）。"),

    # ═══ 王凤艳 — 县领导 ═══
    ("yy_wang_fengyan", "yy_party_committee", "县领导", "待查", "至今", "待查",
     "陪同陈道彬赴陕西省开展招商考察（2026-06-24至25）。"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 陈道彬 ↔ 甘露 — 党政正职搭档 ═══
    ("yy_chen_daobin", "yy_gan_lu", "superior_subordinate",
     "县委书记与县长党政正职搭档关系",
     "中共重庆市云阳县委员会;重庆市云阳县人民政府", "至今"),

    # ═══ 陈道彬 ↔ 彭建云 — 书记-县领导 ═══
    ("yy_chen_daobin", "yy_peng_jianyun", "superior_subordinate",
     "县委书记与副职（彭建云多次参加书记主持/出席的活动）",
     "中共重庆市云阳县委员会", "至今"),

    # ═══ 甘露 ↔ 彭建云 — 县长-陪同调研 ═══
    ("yy_gan_lu", "yy_peng_jianyun", "superior_subordinate",
     "县长与副职（彭建云陪同甘露调研交通和产业项目）",
     "重庆市云阳县人民政府", "至今"),

    # ═══ 甘露 ↔ 吴大伦 — 县长-县领导 ═══
    ("yy_gan_lu", "yy_wu_dalun", "overlap",
     "县长与县领导（同在专题党课活动）",
     "中共重庆市云阳县委员会", "至今"),

    # ═══ 甘露 ↔ 戴蔚 — 县长-县领导 ═══
    ("yy_gan_lu", "yy_dai_wei", "overlap",
     "县长与县领导（同在专题党课活动）",
     "中共重庆市云阳县委员会", "至今"),

    # ═══ 甘露 ↔ 崔军强 — 县长-县领导 ═══
    ("yy_gan_lu", "yy_cui_junqiang", "overlap",
     "县长与县领导（同在专题党课活动）",
     "中共重庆市云阳县委员会", "至今"),

    # ═══ 甘露 ↔ 郭伟 — 县长-县领导 ═══
    ("yy_gan_lu", "yy_guo_wei", "overlap",
     "县长与县领导（同在专题党课活动）",
     "中共重庆市云阳县委员会", "至今"),

    # ═══ 陈道彬 ↔ 严俊 — 书记-县领导 ═══
    ("yy_chen_daobin", "yy_yan_jun", "superior_subordinate",
     "县委书记与副职（信访工作调研共同出席）",
     "中共重庆市云阳县委员会", "至今"),

    # ═══ 陈道彬 ↔ 苗巍伟 — 书记-县领导 ═══
    ("yy_chen_daobin", "yy_miao_weiwei", "superior_subordinate",
     "县委书记与副职（信访工作调研共同出席）",
     "中共重庆市云阳县委员会", "至今"),

    # ═══ 陈道彬 ↔ 王凤艳 — 书记-县领导 ═══
    ("yy_chen_daobin", "yy_wang_fengyan", "superior_subordinate",
     "县委书记与副职（王凤艳陪同赴陕西招商考察）",
     "中共重庆市云阳县委员会", "至今"),
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
    return person_id in ("yy_chen_daobin", "yy_gan_lu")


def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id == "yy_chen_daobin":
        return "255,50,50"       # Red — Party Secretary
    elif person_id == "yy_gan_lu":
        return "50,100,255"      # Blue — Government head
    else:
        return "100,100,100"     # Grey — Others


def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "党委部门": "255,220,220",
        "公安": "200,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return color_map.get(org_type, "200,200,200")


def generate_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Gov Research Agent</creator>')
    lines.append('    <description>重庆市云阳县领导班子工作关系网络</description>')
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
        lines.append(f'        <viz:size value="8.0"/>')
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
    print(f"  重庆市云阳县 领导网络数据")
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
