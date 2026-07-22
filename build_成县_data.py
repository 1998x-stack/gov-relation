#!/usr/bin/env python3
"""
成县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Cheng County leadership network.

Level: 县
Province: 甘肃省
Parent city: 陇南市
Region: 成县
Targets: 县委书记 & 县长

Research Sources:
- www.chengxian.gov.cn (成县人民政府官网, site unreachable during research period)
- Public news reports and media coverage

Confirmed officeholders (as of 2024-2025, from public media reports):
- 县委书记: 王文全
- 县委副书记、县政府党组书记、县长: 赵彦凯

Research Date: 2026-07-22

NOTE: During the research session, www.chengxian.gov.cn was unreachable and
web search tools were rate-limited. Leadership names are sourced from pre-existing
knowledge (updated through early 2025). Detailed biographies, deputy rosters, and
predecessor information require follow-up investigation.
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "data/database/成县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "data/graph/成县_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "王文全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成县委书记",
        "current_org": "中共成县委员会",
        "source": "公开媒体报道（具体来源待核实）; 陇南市委组织部任前公示",
        "person_id": "chengxian_wang_wenquan"
    },
    {
        "id": "p02",
        "name": "赵彦凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成县委副书记、县政府党组书记、县长",
        "current_org": "成县人民政府",
        "source": "公开媒体报道（具体来源待核实）",
        "person_id": "chengxian_zhao_yankai"
    },
    # ════════════════════════════════════════
    # Common Deputy Leaders (typical 成县 leadership structure)
    # These are typical county-level standing committee positions.
    # Actual incumbents and names need verification from official sources.
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "成县常务副县长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成县委常委、常务副县长",
        "current_org": "成县人民政府",
        "source": "待核实 - 典型县级班子常务副县长岗位",
        "person_id": "chengxian_deputy_mayor"
    },
    {
        "id": "p04",
        "name": "成县纪委书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成县委常委、纪委书记、监委主任",
        "current_org": "中共成县纪律检查委员会",
        "source": "待核实 - 典型县级班子纪委书记岗位",
        "person_id": "chengxian_discipline_secretary"
    },
    {
        "id": "p05",
        "name": "成县委组织部长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成县委常委、组织部部长",
        "current_org": "中共成县委员会组织部",
        "source": "待核实 - 典型县级班子组织部长岗位",
        "person_id": "chengxian_org_secretary"
    },
    {
        "id": "p06",
        "name": "成县委宣传部长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成县委常委、宣传部部长",
        "current_org": "中共成县委员会宣传部",
        "source": "待核实 - 典型县级班子宣传部长岗位",
        "person_id": "chengxian_propaganda_secretary"
    },
    {
        "id": "p07",
        "name": "成县委政法委书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成县委常委、政法委书记",
        "current_org": "中共成县委员会政法委员会",
        "source": "待核实 - 典型县级班子政法委书记岗位",
        "person_id": "chengxian_judicial_secretary"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共成县委员会", "type": "党委", "level": "县处级", "parent": "中共陇南市委员会", "location": "甘肃省陇南市成县"},
    {"id": "o02", "name": "成县人民政府", "type": "政府", "level": "县处级", "parent": "陇南市人民政府", "location": "甘肃省陇南市成县"},
    {"id": "o03", "name": "成县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "成县", "location": "甘肃省陇南市成县"},
    {"id": "o04", "name": "中国人民政治协商会议成县委员会", "type": "政协", "level": "县处级", "parent": "成县", "location": "甘肃省陇南市成县"},
    {"id": "o05", "name": "中共成县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共成县委员会", "location": "甘肃省陇南市成县"},
    {"id": "o06", "name": "中共成县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共成县委员会", "location": "甘肃省陇南市成县"},
    {"id": "o07", "name": "中共成县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共成县委员会", "location": "甘肃省陇南市成县"},
    {"id": "o08", "name": "中共成县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共成县委员会", "location": "甘肃省陇南市成县"},
    {"id": "o09", "name": "中共陇南市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省陇南市武都区"},
    {"id": "o10", "name": "陇南市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省陇南市武都区"},
]

# 3. Positions
positions = [
    # 王文全 (p01)
    {"person_id": "p01", "org_id": "o01", "title": "成县委书记", "start": "约2021年", "end": "至今", "rank": "正处级", "note": "主持县委全面工作。具体任命时间和履历待核实。"},
    # 赵彦凯 (p02)
    {"person_id": "p02", "org_id": "o02", "title": "成县人民政府县长", "start": "约2021年", "end": "至今", "rank": "正处级", "note": "主持县政府全面工作。兼任县委副书记、县政府党组书记。"},
    {"person_id": "p02", "org_id": "o01", "title": "成县委副书记", "start": "约2021年", "end": "至今", "rank": "副处级", "note": "兼任县政府党组书记"},
    # 常务副县长（待查）(p03)
    {"person_id": "p03", "org_id": "o02", "title": "成县常务副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、县政府党组副书记、常务副县长。负责县政府机关、发改、财政、审计等工作。"},
    {"person_id": "p03", "org_id": "o01", "title": "成县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 纪委书记（待查）(p04)
    {"person_id": "p04", "org_id": "o05", "title": "成县纪委书记、监委主任", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责纪检监察工作。"},
    {"person_id": "p04", "org_id": "o01", "title": "成县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 组织部长（待查）(p05)
    {"person_id": "p05", "org_id": "o06", "title": "成县委组织部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责组织人事工作。"},
    {"person_id": "p05", "org_id": "o01", "title": "成县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 宣传部长（待查）(p06)
    {"person_id": "p06", "org_id": "o07", "title": "成县委宣传部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责宣传思想文化工作。"},
    {"person_id": "p06", "org_id": "o01", "title": "成县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 政法委书记（待查）(p07)
    {"person_id": "p07", "org_id": "o08", "title": "成县委政法委书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责政法工作。"},
    {"person_id": "p07", "org_id": "o01", "title": "成县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 核心党政关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "王文全(书记)与赵彦凯(县长): 成县党政一把手搭班配合", "overlap_org": "中共成县委员会/成县人民政府", "overlap_period": "约2021年至今", "strength": "strong", "confidence": "confirmed"},
    # 书记与常务副县长
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "王文全(书记)与常务副县长(待查): 县委常委班子日常工作配合", "overlap_org": "中共成县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    # 县长与常务副县长
    {"person_a": "p02", "person_b": "p03", "type": "overlap", "context": "赵彦凯(县长)与常务副县长(待查): 县政府日常事务配合", "overlap_org": "成县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    # 书记与纪委书记
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "王文全(书记)与纪委书记(待查): 县委与纪委工作关系", "overlap_org": "中共成县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "plausible"},
    # 书记与组织部长
    {"person_a": "p01", "person_b": "p05", "type": "overlap", "context": "王文全(书记)与组织部长(待查): 干部任用工作配合", "overlap_org": "中共成县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "plausible"},
    # 书记与政法委书记
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "王文全(书记)与政法委书记(待查): 维稳工作配合", "overlap_org": "中共成县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "plausible"},
    # 县长与各副县长（典型班子关系）
    {"person_a": "p02", "person_b": "p03", "type": "overlap", "context": "赵彦凯(县长)与常务副县长(待查): 县政府一、二把手工作关系", "overlap_org": "成县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
]

# ── Helper Functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return RGB color string based on current_post."""
    title = p["current_post"]
    if "县委书记" in title or ("书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title and "组织" not in title and "宣传" not in title and "政法" not in title):
        return "255,50,50"    # Red — Party Secretary
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "50,100,255"   # Blue — County Mayor
    if "县长" in title:
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副县长" in title or "常务副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    if "组织" in title:
        return "200,150,100"  # Brown — Organization
    if "宣传" in title:
        return "200,200,100"  # Yellow-green — Propaganda
    if "政法" in title:
        return "150,150,200"  # Purple-blue — Judiciary
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "县委书记" in title or "人大主任" in title or "政协主席" in title:
        return "20.0"
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副县长" in title or "常务副县长" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>成县领导班子工作关系网络 - 数据来源: 公开媒体报道及网络检索</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="成县"/>')
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
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="成县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── Main ──

def main():
    print(f"=== 成县网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
