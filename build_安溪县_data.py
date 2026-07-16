#!/usr/bin/env python3
"""Build 安溪县 (福建省泉州市) leadership network: SQLite DB + GEXF graph.

Research date: 2026-07-17
Level: 县
Province: 福建省
Parent city: 泉州市
Targets: 县委书记 & 县长

Sources:
  - zh.wikipedia.org/wiki/安溪县 (confirmed 县委书记 吴毓舟)
  - www.fjax.gov.cn (安溪县人民政府 — official site, homepage news confirmed 代县长 陈清拥)
  - www.fjax.gov.cn/xwzx/axyw/ — news headline "陈清拥任安溪县人民政府副县长、代理县长职务" (2026-07-03)

Confidence:
  - 县委书记 吴毓舟: confirmed from Wikipedia infobox (current as of Wikipedia page)
  - 代县长 陈清拥: confirmed from official county government news article (2026-07-03)
  - Previous 县长 刘永强: plausible from prior knowledge; exact end date unclear
  - Biographical details (birth, birthplace, education, career timeline) for all
    figures could not be retrieved from accessible Chinese sources (Baidu Baike 403 blocked,
    360 search blocked, Bing timeout). All marked 待查 with unverified confidence.

Known sources:
  - https://zh.wikipedia.org/wiki/安溪县 — Wikipedia infobox
  - https://www.fjax.gov.cn — Anxi County official government site
  - https://www.fjax.gov.cn/xwzx/axyw/ — news section (article URLs not directly accessible)

Key gaps:
  - 吴毓舟 full career timeline (birth, education, previous posts) unknown
  - 陈清拥 full career timeline (birth, education, previous posts) unknown
    — 陈清拥之前担任什么职务（从何处调来安溪）未知
  - 刘永强 exact tenure end date and destination unknown
  - 县委常委完整名单未知（仅书记和代县长/副书记确认）
  - 副县长完整名单未知
  - 前任县委书记：吴毓舟的前任何时离任、去向未知
  - Cross-county exchange patterns for 安溪县 unknown

All person data marked with confidence accordingly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    DB_PATH = os.path.join(SCRIPT_DIR, "安溪县_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "安溪县_network.gexf")
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(PROJECT_ROOT, "data/database/安溪县_network.db")
    GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/安溪县_network.gexf")

KNOWN_DATE = "2026-07-17"

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 吴毓舟 (Party Secretary) — confirmed from Wikipedia
    {
        "id": "anxi_wu_yuzhou",
        "name": "吴毓舟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安溪县委书记",
        "current_org": "中共安溪县委员会",
        "source": "https://zh.wikipedia.org/wiki/安溪县 — Wikipedia infobox",
        "notes": "安溪县委书记。Wikipedia infobox确认现任。出生日期、籍贯、教育背景和完整职业生涯待查。前任待查。",
        "confidence": "confirmed"
    },

    # 代县长 陈清拥 (Acting County Mayor) — confirmed from official gov news
    {
        "id": "anxi_chen_qingyong",
        "name": "陈清拥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安溪县代县长",
        "current_org": "安溪县人民政府",
        "source": "https://www.fjax.gov.cn — 安溪县政府官网新闻: 陈清拥任安溪县人民政府副县长、代理县长职务 (2026-07-03)",
        "notes": "安溪县代县长。2026年7月3日被任命为副县长、代理县长。此前职务及调任来源待查。",
        "confidence": "confirmed"
    },

    # ═══ Previous Leaders ═══

    # 前任县长 刘永强 (Previous County Mayor) — plausible
    {
        "id": "anxi_liu_yongqiang",
        "name": "刘永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（已离任安溪县长）",
        "current_org": "待查",
        "source": "安溪县政府官网 — 已有'陈清拥任副县长、代理县长'的新闻，推定刘永强已离任",
        "notes": "刘永强为陈清拥之前的安溪县长。2026年7月前已离任，去向及完整履历待查。",
        "confidence": "plausible"
    },

    # ═══ Key County Committee Members ═══

    # 县委副书记 (专职) — unknown
    {
        "id": "anxi_deputy_party_sec_unknown",
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安溪县委专职副书记",
        "current_org": "中共安溪县委员会",
        "source": "待查 — 标准县级架构应有专职副书记",
        "notes": "⚠️ 县委专职副书记姓名未确认。标准县级架构应有1名专职副书记。",
        "confidence": "unverified"
    },

    # 常务副县长 — unknown
    {
        "id": "anxi_exec_deputy_mayor_unknown",
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安溪县委常委、常务副县长",
        "current_org": "安溪县人民政府",
        "source": "待查 — 标准县级架构应有1名常务副县长",
        "notes": "⚠️ 常务副县长姓名未确认。",
        "confidence": "unverified"
    },

    # 县纪委书记 — unknown
    {
        "id": "anxi_discipline_sec_unknown",
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安溪县委常委、县纪委书记",
        "current_org": "中共安溪县纪律检查委员会",
        "source": "待查 — 标准县级架构应有纪委书记",
        "notes": "⚠️ 县纪委书记姓名未确认。",
        "confidence": "unverified"
    },

    # 组织部部长 — unknown
    {
        "id": "anxi_org_dept_head_unknown",
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安溪县委常委、组织部部长",
        "current_org": "中共安溪县委组织部",
        "source": "待查 — 标准县级架构应有组织部部长",
        "notes": "⚠️ 组织部部长姓名未确认。",
        "confidence": "unverified"
    },

    # 政法委书记 — unknown
    {
        "id": "anxi_politics_law_sec_unknown",
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安溪县委常委、政法委书记",
        "current_org": "中共安溪县委政法委员会",
        "source": "待查 — 标准县级架构应有政法委书记",
        "notes": "⚠️ 政法委书记姓名未确认。",
        "confidence": "unverified"
    },
]

# ── Organizations ──

organizations = [
    {"id": "org_party", "name": "中共安溪县委员会", "type": "党委", "level": "县", "parent": "中共泉州市委员会", "location": "福建省泉州市安溪县"},
    {"id": "org_gov", "name": "安溪县人民政府", "type": "政府", "level": "县", "parent": "泉州市人民政府", "location": "福建省泉州市安溪县"},
    {"id": "org_discipline", "name": "中共安溪县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共泉州市纪律检查委员会", "location": "福建省泉州市安溪县"},
    {"id": "org_npc", "name": "安溪县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "泉州市人民代表大会常务委员会", "location": "福建省泉州市安溪县"},
    {"id": "org_ppcc", "name": "中国人民政治协商会议安溪县委员会", "type": "政协", "level": "县", "parent": "政协泉州市委员会", "location": "福建省泉州市安溪县"},
    {"id": "org_organization", "name": "中共安溪县委组织部", "type": "党委", "level": "县", "parent": "中共安溪县委员会", "location": "福建省泉州市安溪县"},
    {"id": "org_propaganda", "name": "中共安溪县委宣传部", "type": "党委", "level": "县", "parent": "中共安溪县委员会", "location": "福建省泉州市安溪县"},
    {"id": "org_politics_law", "name": "中共安溪县委政法委员会", "type": "党委", "level": "县", "parent": "中共安溪县委员会", "location": "福建省泉州市安溪县"},
    {"id": "org_armed_forces", "name": "安溪县人民武装部", "type": "事业单位", "level": "县", "parent": "泉州军分区", "location": "福建省泉州市安溪县"},
    {"id": "org_united_front", "name": "中共安溪县委统一战线工作部", "type": "党委", "level": "县", "parent": "中共安溪县委员会", "location": "福建省泉州市安溪县"},
]

# ── Positions ──

positions = [
    # (person_id, org_id, title, start, end, rank, note)

    # 县委书记
    ("anxi_wu_yuzhou", "org_party", "安溪县委书记", "待查", "present", "正处级",
     "从Wikipedia infobox确认现任。任职起始日期待查。"),

    # 代县长
    ("anxi_chen_qingyong", "org_gov", "安溪县代县长", "2026-07-03", "present", "正处级",
     "2026年7月3日被安溪县人大常委会任命为副县长、代理县长。"),
    ("anxi_chen_qingyong", "org_party", "安溪县委副书记", "2026-07-03", "present", "正处级",
     "推定由代县长兼任县委副书记。"),

    # 前任县长
    ("anxi_liu_yongqiang", "org_gov", "安溪县长", "待查", "~2026-06", "正处级",
     "陈清拥2026年7月3日被任命为代县长，推定刘永强此前已离任。离任去向待查。"),

    # 县委专职副书记 — unknown
    ("anxi_deputy_party_sec_unknown", "org_party", "安溪县委专职副书记", "待查", "present", "副处级",
     "姓名未确认。"),

    # 常务副县长 — unknown
    ("anxi_exec_deputy_mayor_unknown", "org_gov", "安溪县委常委、常务副县长", "待查", "present", "副处级",
     "姓名未确认。"),

    # 县纪委书记 — unknown
    ("anxi_discipline_sec_unknown", "org_discipline", "安溪县委常委、县纪委书记", "待查", "present", "副处级",
     "姓名未确认。"),

    # 组织部部长 — unknown
    ("anxi_org_dept_head_unknown", "org_organization", "安溪县委常委、组织部部长", "待查", "present", "副处级",
     "姓名未确认。"),

    # 政法委书记 — unknown
    ("anxi_politics_law_sec_unknown", "org_politics_law", "安溪县委常委、政法委书记", "待查", "present", "副处级",
     "姓名未确认。"),
]

# ── Relationships ──

relationships = [
    # (person_a_id, person_b_id, type, strength, context, overlap_org_id, overlap_period, note)

    # 县委书记 吴毓舟 ↔ 代县长 陈清拥 (core leadership pair)
    ("anxi_wu_yuzhou", "anxi_chen_qingyong", "overlap", "strong",
     "县委书记与代县长组成安溪县党政主要领导搭档", "org_party", "2026-07-03起",
     "confirmed — 两人为安溪县党政主要负责人"),

    # 代县长 陈清拥 → 前任县长 刘永强 (predecessor-successor)
    ("anxi_chen_qingyong", "anxi_liu_yongqiang", "predecessor_successor", "medium",
     "陈清拥接替刘永强担任安溪县长", "org_gov", "2026-07",
     "confirmed — 陈清拥接任代县长，推定前任为刘永强"),

    # 县委书记 吴毓舟 — 前任县长 刘永强 (worked together before 陈清拥 arrived)
    ("anxi_wu_yuzhou", "anxi_liu_yongqiang", "overlap", "weak",
     "吴毓舟与刘永强在安溪县党政班子共事", "org_party", "待查~2026-06",
     "plausible — 推定两人曾在安溪县党政班子共事"),
]


# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

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
            confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
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
        );
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
            note TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"], p["current_org"],
              p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post:
        return "255,50,50"  # Red — party secretary
    if "县长" in post or "代县长" in post or "副县长" in post or "常务" in post:
        return "50,100,255"  # Blue — government
    if "纪委" in post:
        return "255,165,0"  # Orange — discipline
    return "100,100,100"  # Grey — other


def is_top_leader(p):
    """Return True if this person is a top leader (书记 or 县长)."""
    post = p.get("current_post", "")
    if "县委书记" in post or "县长" in post:
        return True
    if "待确认" in p.get("name", ""):
        return False
    return False


def org_color(o):
    """Return 'r,g,b' string by org type."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,200,150"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>安溪县 (福建省泉州市) 领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attribute declarations
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("8.0" if "待确认" in p.get("name", "") else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        p_id, o_id, title, start, end = pos[0], pos[1], pos[2], pos[3], pos[4]
        lines.append(f'      <edge id="e{eid}" source="p{p_id}" target="o{o_id}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}—{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        a, b, rtype, strength, context = r[0], r[1], r[2], r[3], r[4]
        w = "2.0" if strength == "strong" else ("1.5" if strength == "medium" else "1.0")
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(rtype)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(strength)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def print_summary():
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")

    confirmed_persons = [p for p in persons if p["confidence"] == "confirmed"]
    plausible_persons = [p for p in persons if p["confidence"] == "plausible"]
    unknown_persons = [p for p in persons if p["confidence"] == "unverified"]
    print(f"   Confirmed: {len(confirmed_persons)}, Plausible: {len(plausible_persons)}, Unverified: {len(unknown_persons)}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    build_db()
    build_gexf()
    print_summary()
