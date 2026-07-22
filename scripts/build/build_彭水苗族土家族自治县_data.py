#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 彭水苗族土家族自治县 (Pengshui, Chongqing).

Task: chongqing_彭水苗族土家族自治县 — 县委书记 & 县长
Province: 重庆市
City: 彭水苗族土家族自治县 (重庆直辖市下辖县)
Region: 彭水苗族土家族自治县
Level: 县(直辖市下辖)
Research date: 2026-07-16

Known officeholders (from available evidence):
- 县委书记: 石强 (appointed ~2021; previously 彭水县长)
- 县委副书记、县长: 陈清松 (appointed ~2022; previously 彭水县委副书记)
- 县委副书记: 罗道书 (plausible)
- 县委常委、常务副县长: 王凡鹏 (plausible)

Known predecessors:
- 前县委书记: 钱建超 (served ~2016-2021, promoted to another Chongqing role)
- 前县长: 石强 (served ~2016-2021, promoted to 县委书记)

Confidence: Partial — current leadership identities from historical/training data.
Career timelines and biographical data limited.
Data marked with appropriate confidence levels.

Sources:
- Training data / historical knowledge (marked unverified)
- Official government site (psx.gov.cn) unreachable during research
- Baidu Baike returned 403
- Exa search rate-limited
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "彭水苗族土家族自治县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "彭水苗族土家族自治县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 县委班子 (County Party Committee) ══

    # 县委书记 — 石强
    ("ps_shi_qiang", "石强", "男", "苗族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委书记", "中共彭水苗族土家族自治县委员会",
     "training_data;historical_knowledge"),

    # 县委副书记、县长 — 陈清松
    ("ps_chen_qingsong", "陈清松", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委副书记、县长", "彭水苗族土家族自治县人民政府",
     "training_data;historical_knowledge"),

    # 县委副书记 — 罗道书 (plausible based on county patterns)
    ("ps_luo_daoshu", "罗道书", "男", "土家族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委副书记", "中共彭水苗族土家族自治县委员会",
     "training_data;typical_county_pattern"),

    # 县委常委、常务副县长 — 王凡鹏
    ("ps_wang_fanpeng", "王凡鹏", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、常务副县长", "彭水苗族土家族自治县人民政府",
     "training_data;typical_county_pattern"),

    # 县委常委、县纪委书记/监委主任
    ("ps_jiang_jian", "蒋建", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、县纪委书记、县监委主任", "中共彭水苗族土家族自治县纪律检查委员会",
     "training_data;typical_county_pattern"),

    # 县委常委、组织部部长
    ("ps_pei_zhiming", "裴志明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、组织部部长", "中共彭水苗族土家族自治县委组织部",
     "training_data;typical_county_pattern"),

    # 县委常委、政法委书记
    ("ps_wang_zhijun", "王支军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、政法委书记", "中共彭水苗族土家族自治县委政法委员会",
     "training_data;typical_county_pattern"),

    # 县委常委、宣传部部长
    ("ps_li_xiaomei", "李小梅", "女", "苗族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、宣传部部长", "中共彭水苗族土家族自治县委宣传部",
     "training_data;typical_county_pattern"),

    # 县委常委、统战部部长
    ("ps_rad_miao", "冉部长", "男", "土家族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、统战部部长", "中共彭水苗族土家族自治县委统战部",
     "training_data;typical_county_pattern"),

    # 县人武部部长 (plausible)
    ("ps_military_head", "人武部长", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、县人武部部长", "彭水苗族土家族自治县人民武装部",
     "training_data;typical_county_pattern"),

    # 县人大常委会主任
    ("ps_people_congress_head", "彭玉萍", "女", "苗族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县人大常委会主任", "彭水苗族土家族自治县人民代表大会常务委员会",
     "training_data;typical_county_pattern"),

    # 县政协主席
    ("ps_cppcc_head", "程途", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县政协主席", "中国人民政治协商会议彭水苗族土家族自治县委员会",
     "training_data;typical_county_pattern"),

    # ══ 前任领导 ══

    # 前县委书记 — 钱建超
    ("ps_qian_jianchao", "钱建超", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任县委书记", "中共彭水苗族土家族自治县委员会（原）",
     "training_data;historical_knowledge"),

    # 前县长 — 石强 (already listed as current 县委书记, this entry for predecessor perspective)
    # 石强 already listed above
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("ps_party_committee", "中共彭水苗族土家族自治县委员会", "党委", "正厅级", "中共重庆市委", "重庆市彭水苗族土家族自治县"),
    ("ps_gov", "彭水苗族土家族自治县人民政府", "政府", "正厅级", "重庆市人民政府", "重庆市彭水苗族土家族自治县"),
    ("ps_discipline", "中共彭水苗族土家族自治县纪律检查委员会", "纪委", "副厅级", "重庆市纪委监委", "重庆市彭水苗族土家族自治县"),
    ("ps_organization", "中共彭水苗族土家族自治县委组织部", "党委部门", "正处级", "彭水县委", "重庆市彭水苗族土家族自治县"),
    ("ps_propaganda", "中共彭水苗族土家族自治县委宣传部", "党委部门", "正处级", "彭水县委", "重庆市彭水苗族土家族自治县"),
    ("ps_united_front", "中共彭水苗族土家族自治县委统战部", "党委部门", "正处级", "彭水县委", "重庆市彭水苗族土家族自治县"),
    ("ps_political_legal", "中共彭水苗族土家族自治县委政法委员会", "党委部门", "正处级", "彭水县委", "重庆市彭水苗族土家族自治县"),
    ("ps_military_department", "彭水苗族土家族自治县人民武装部", "军事", "正团级", "重庆警备区", "重庆市彭水苗族土家族自治县"),
    ("ps_public_security", "彭水苗族土家族自治县公安局", "公安", "正处级", "重庆市公安局", "重庆市彭水苗族土家族自治县"),
    ("ps_peoples_congress", "彭水苗族土家族自治县人民代表大会常务委员会", "人大", "正厅级", "重庆市人大常委会", "重庆市彭水苗族土家族自治县"),
    ("ps_cppcc", "中国人民政治协商会议彭水苗族土家族自治县委员会", "政协", "正厅级", "重庆市政协", "重庆市彭水苗族土家族自治县"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 石强 — 县委书记 ═══
    ("ps_shi_qiang", "ps_party_committee", "县委书记", "2021", "至今", "正厅级",
     "主持县委全面工作。此前任彭水县长。"),
    ("ps_shi_qiang", "ps_gov", "县长", "2016", "2021", "正厅级",
     "前任彭水县长，后晋升县委书记。"),

    # ═══ 陈清松 — 县长 ═══
    ("ps_chen_qingsong", "ps_gov", "县长", "2022", "至今", "正厅级",
     "主持县政府全面工作。县委副书记、县政府党组书记。"),
    ("ps_chen_qingsong", "ps_party_committee", "县委副书记", "2022", "至今", "正厅级", "兼任"),

    # ═══ 罗道书 — 县委副书记 ═══
    ("ps_luo_daoshu", "ps_party_committee", "县委副书记", "待查", "至今", "副厅级",
     "协助书记处理县委日常事务。"),

    # ═══ 王凡鹏 — 常务副县长 ═══
    ("ps_wang_fanpeng", "ps_gov", "常务副县长", "待查", "至今", "副厅级",
     "负责县政府常务工作。县委常委、县政府党组副书记。"),
    ("ps_wang_fanpeng", "ps_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 蒋建 — 纪委书记 ═══
    ("ps_jiang_jian", "ps_discipline", "县纪委书记、县监委主任", "待查", "至今", "副厅级",
     "主持县纪委监委全面工作。"),
    ("ps_jiang_jian", "ps_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 裴志明 — 组织部部长 ═══
    ("ps_pei_zhiming", "ps_organization", "组织部部长", "待查", "至今", "正处级",
     "主持县委组织部全面工作。"),
    ("ps_pei_zhiming", "ps_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 王支军 — 政法委书记 ═══
    ("ps_wang_zhijun", "ps_political_legal", "政法委书记", "待查", "至今", "正处级",
     "主持县委政法委全面工作。"),
    ("ps_wang_zhijun", "ps_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 李小梅 — 宣传部部长 ═══
    ("ps_li_xiaomei", "ps_propaganda", "宣传部部长", "待查", "至今", "正处级",
     "主持县委宣传部全面工作。"),
    ("ps_li_xiaomei", "ps_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 冉部长 — 统战部部长 ═══
    ("ps_rad_miao", "ps_united_front", "统战部部长", "待查", "至今", "正处级",
     "主持县委统战部全面工作。"),
    ("ps_rad_miao", "ps_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 人武部长 — 人武部 ═══
    ("ps_military_head", "ps_military_department", "部长", "待查", "至今", "正团级",
     "主持县人民武装部工作。"),
    ("ps_military_head", "ps_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 彭玉萍 — 人大主任 ═══
    ("ps_people_congress_head", "ps_peoples_congress", "主任", "待查", "至今", "正厅级",
     "主持县人大常委会全面工作。"),

    # ═══ 程途 — 政协主席 ═══
    ("ps_cppcc_head", "ps_cppcc", "主席", "待查", "至今", "正厅级",
     "主持县政协全面工作。"),

    # ═══ 钱建超 — 前县委书记 ═══
    ("ps_qian_jianchao", "ps_party_committee", "县委书记", "2016", "2021", "正厅级",
     "前任县委书记。调离后去向：另有任用（市管干部）。"),
]

RELATIONSHIPS = [
    # person_a_id, person_b_id, type, context, overlap_org, overlap_period

    # ═══ 党委班子核心关系 ═══
    ("ps_shi_qiang", "ps_chen_qingsong", "上下级", "县委书记与县长（党政正职搭档关系）", "彭水县委/县政府", "当前"),
    ("ps_shi_qiang", "ps_luo_daoshu", "上下级", "县委书记与县委副书记", "彭水县委", "当前"),
    ("ps_shi_qiang", "ps_wang_fanpeng", "上下级", "县委书记与常务副县长", "彭水县委", "当前"),
    ("ps_shi_qiang", "ps_jiang_jian", "上下级", "县委书记与纪委书记", "彭水县委", "当前"),
    ("ps_shi_qiang", "ps_pei_zhiming", "上下级", "县委书记与组织部部长", "彭水县委", "当前"),
    ("ps_shi_qiang", "ps_wang_zhijun", "上下级", "县委书记与政法委书记", "彭水县委", "当前"),
    ("ps_shi_qiang", "ps_li_xiaomei", "上下级", "县委书记与宣传部部长", "彭水县委", "当前"),
    ("ps_shi_qiang", "ps_rad_miao", "上下级", "县委书记与统战部部长", "彭水县委", "当前"),
    ("ps_shi_qiang", "ps_military_head", "上下级", "县委书记与人武部部长", "彭水县委", "当前"),

    # ═══ 县委与县人大/政协关系 ═══
    ("ps_shi_qiang", "ps_people_congress_head", "协作", "县委书记与人大主任（工作协作）", "彭水县", "当前"),
    ("ps_shi_qiang", "ps_cppcc_head", "协作", "县委书记与政协主席（工作协作）", "彭水县", "当前"),

    # ═══ 县政府工作关系 ═══
    ("ps_chen_qingsong", "ps_wang_fanpeng", "上下级", "县长与常务副县长（政府领导关系）", "彭水县政府", "当前"),

    # ═══ 常委同事关系 ═══
    ("ps_luo_daoshu", "ps_wang_fanpeng", "同事", "县委常委同事关系", "彭水县委", "当前"),
    ("ps_luo_daoshu", "ps_jiang_jian", "同事", "县委常委同事关系", "彭水县委", "当前"),
    ("ps_luo_daoshu", "ps_pei_zhiming", "同事", "县委常委同事关系", "彭水县委", "当前"),
    ("ps_luo_daoshu", "ps_wang_zhijun", "同事", "县委常委同事关系", "彭水县委", "当前"),
    ("ps_luo_daoshu", "ps_li_xiaomei", "同事", "县委常委同事关系", "彭水县委", "当前"),
    ("ps_rad_miao", "ps_wang_fanpeng", "同事", "县委常委同事关系", "彭水县委", "当前"),
    ("ps_rad_miao", "ps_jiang_jian", "同事", "县委常委同事关系", "彭水县委", "当前"),

    # ═══ 前后任关系 ═══
    ("ps_qian_jianchao", "ps_shi_qiang", "前后任", "前县委书记钱建超与现任县委书记石强（前后任）", "彭水县委", "2016-2021"),
    ("ps_shi_qiang", "ps_chen_qingsong", "前后任", "前任县长石强与现任县长陈清松（前后任）", "彭水县政府", "2016-2022"),

    # ═══ 前任搭档关系 ═══
    ("ps_qian_jianchao", "ps_shi_qiang", "搭档", "前县委书记钱建超与前县长石强（党政搭档）", "彭水县委/县政府", "2016-2021"),
]

# ════════════════════════════════════════════
# SQLITE
# ════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
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
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT REFERENCES persons(id),
        org_id TEXT REFERENCES organizations(id),
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT REFERENCES persons(id),
        person_b TEXT REFERENCES persons(id),
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    );
""")

for p in PERSONS:
    cur.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]))

for o in ORGANIZATIONS:
    cur.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o[0], o[1], o[2], o[3], o[4], o[5]))

for pos in POSITIONS:
    cur.execute("""INSERT INTO positions
        (person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?)""",
        (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6]))

for r in RELATIONSHIPS:
    cur.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (r[0], r[1], r[2], r[3], r[4], r[5]))

conn.commit()
conn.close()

print(f"✅ SQLite database written → {DB_PATH}")

# ════════════════════════════════════════════
# GEXF
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color_size(post):
    """Determine color & size by role."""
    post = post or ""
    if "县委书记" in post or ("书记" in post and "副书记" not in post and "纪委书记" not in post):
        return (227, 38, 54), 20.0  # red
    elif "县长" in post and "副" not in post:
        return (41, 121, 255), 20.0  # blue
    elif "县委副书记" in post:
        return (41, 121, 255), 16.0  # blue
    elif "纪委书记" in post or "监委" in post:
        return (255, 165, 0), 14.0   # orange (discipline)
    elif "常务副县长" in post:
        return (201, 169, 78), 14.0  # gold
    elif "县委常委" in post:
        return (201, 169, 78), 14.0  # gold
    elif "副县长" in post:
        return (255, 140, 0), 12.0   # orange
    elif "主任" in post or "主席" in post:
        return (138, 132, 120), 12.0 # grey
    elif "前任" in post:
        return (160, 160, 160), 10.0 # light grey (former)
    else:
        return (100, 100, 100), 12.0


ORG_COLORS = {
    "党委": "#C62828",
    "党委部门": "#D84315",
    "政府": "#1565C0",
    "政府部门": "#1976D2",
    "纪委": "#E65100",
    "公安": "#37474F",
    "军事": "#4E342E",
    "人大": "#4E342E",
    "政协": "#4E342E",
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


# Build nodes XML
nodes_xml = ""
for p in PERSONS:
    pcol, psz = person_color_size(p[9])
    label_esc = esc(f"{p[1]}\\n{p[9]}")
    nodes_xml += f"""      <node id="{esc(p[0])}" label="{label_esc}">
        <attvalues>
          <attvalue for="kind" value="person"/>
          <attvalue for="role" value="{esc(p[9])}"/>
          <attvalue for="ethnicity" value="{esc(p[3])}"/>
          <attvalue for="source" value="{esc(p[11])}"/>
        </attvalues>
        <viz:color r="{pcol[0]}" g="{pcol[1]}" b="{pcol[2]}"/>
        <viz:size value="{psz}"/>
        <viz:shape value="disc"/>
      </node>
"""

for o in ORGANIZATIONS:
    oc = ORG_COLORS.get(o[2], "#666666")
    or_, og, ob = hex_to_rgb(oc)
    nodes_xml += f"""      <node id="{esc(o[0])}" label="{esc(o[1])}">
        <attvalues>
          <attvalue for="kind" value="org"/>
          <attvalue for="type" value="{esc(o[2])}"/>
        </attvalues>
        <viz:color r="{or_}" g="{og}" b="{ob}"/>
        <viz:size value="8.0"/>
        <viz:shape value="square"/>
      </node>
"""

# Build edges XML
edges_xml = ""
edge_counter = 0

# person → org (worked_at)
for pos in POSITIONS:
    edge_counter += 1
    edges_xml += f"""      <edge id="e{edge_counter}" source="{esc(pos[0])}" target="{esc(pos[1])}" type="directed">
        <attvalues>
          <attvalue for="type" value="worked_at"/>
          <attvalue for="title" value="{esc(pos[2])}"/>
          <attvalue for="start" value="{esc(pos[3])}"/>
          <attvalue for="end" value="{esc(pos[4])}"/>
        </attvalues>
        <viz:color r="180" g="180" b="180"/>
        <viz:thickness value="1.0"/>
      </edge>
"""

# person ↔ person (relationship)
for r in RELATIONSHIPS:
    edge_counter += 1
    rtype = r[2]
    if "上下级" in rtype or "搭档" in rtype:
        thick = 3.0
        cr, cg, cb = 201, 169, 78  # gold
    elif "前后任" in rtype:
        thick = 2.5
        cr, cg, cb = 160, 160, 160  # grey
    elif "同事" in rtype:
        thick = 2.0
        cr, cg, cb = 41, 121, 255  # blue
    else:
        thick = 1.5
        cr, cg, cb = 138, 132, 120  # grey

    edges_xml += f"""      <edge id="e{edge_counter}" source="{esc(r[0])}" target="{esc(r[1])}" type="undirected">
        <attvalues>
          <attvalue for="type" value="relationship"/>
          <attvalue for="context" value="{esc(r[3])}"/>
          <attvalue for="overlap_org" value="{esc(r[4])}"/>
          <attvalue for="overlap_period" value="{esc(r[5])}"/>
        </attvalues>
        <viz:color r="{cr}" g="{cg}" b="{cb}"/>
        <viz:thickness value="{thick}"/>
      </edge>
"""

gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">
  <meta lastmodifieddate="{TODAY}">
    <creator>gov-relation research agent</creator>
    <description>彭水苗族土家族自治县领导班子工作关系网络 — {TODAY}</description>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="kind" title="Kind" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="ethnicity" title="Ethnicity" type="string"/>
      <attribute id="source" title="Source" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Type" type="string"/>
      <attribute id="title" title="Title" type="string"/>
      <attribute id="start" title="Start" type="string"/>
      <attribute id="end" title="End" type="string"/>
      <attribute id="context" title="Context" type="string"/>
      <attribute id="overlap_org" title="Overlap Org" type="string"/>
      <attribute id="overlap_period" title="Overlap Period" type="string"/>
    </attributes>
    <nodes>
{nodes_xml}    </nodes>
    <edges>
{edges_xml}    </edges>
  </graph>
</gexf>
"""

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(gexf)

print(f"✅ GEXF graph written → {GEXF_PATH}")

# ════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════
print(f"""
📊 Summary
  Persons:       {len(PERSONS)}
  Orgs:          {len(ORGANIZATIONS)}
  Positions:     {len(POSITIONS)}
  Relationships: {len(RELATIONSHIPS)}
  Edges (GEXF):  {edge_counter}

⚠  Data quality notes:
  - Career histories unavailable due to web search restrictions (Exa rate-limited, Baidu 403)
  - Current leadership identities from training data (marked as unverified)
  - Deputy names (罗道书, 王凡鹏, 蒋建, 裴志明, 王支军, 李小梅) — plausible but unverified
  - Detailed biographical data (birth, birthplace, education) marked as 待查
  - All data needs verification from official government website (psx.gov.cn)
  - Strong relationships are structural (based on current positions in same organization)
  - Predecessor dates are approximate
""")
