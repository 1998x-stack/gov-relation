#!/usr/bin/env python3
"""
环县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Huan County leadership network.

Level: 县
Province: 甘肃省
Parent city: 庆阳市
Region: 环县
Targets: 县委书记 & 县长

Research Sources:
- www.huanxian.gov.cn (环县人民政府官网 领导之窗, accessed 2026-07-22)
- 环县新闻 (2026年7月)
- 庆阳市领导网络 (已有研究数据)

Confirmed officeholders (as of 2026-07-22, from www.huanxian.gov.cn):
- 县委书记: 曹育铮
- 县委副书记、县长: 杨添翼

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "环县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "环县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "曹育铮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "环县县委书记",
        "current_org": "中共环县委员会",
        "source": "www.huanxian.gov.cn (领导之窗); 环县新闻2026-07-14",
        "person_id": "huanxian_cao_yuzheng"
    },
    {
        "id": "p02",
        "name": "杨添翼",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "环县县委副书记、县政府党组书记、县长",
        "current_org": "环县人民政府",
        "source": "www.huanxian.gov.cn (领导之窗); 环县新闻2026-07-10",
        "person_id": "huanxian_yang_tianyi"
    },
    # ════════════════════════════════════════
    # Predecessors (identified from county news patterns)
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "曹育铮（前任待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（环县前任县委书记）",
        "current_org": "待查",
        "source": "待查 — 需后续搜索曹育铮前任信息",
        "person_id": "huanxian_predecessor_secretary"
    },
    {
        "id": "p04",
        "name": "杨添翼（前任待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（环县前任县长）",
        "current_org": "待查",
        "source": "待查 — 需后续搜索杨添翼前任信息",
        "person_id": "huanxian_predecessor_mayor"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共环县委员会", "type": "党委", "level": "县处级", "parent": "中共庆阳市委员会", "location": "甘肃省庆阳市环县环城镇"},
    {"id": "o02", "name": "环县人民政府", "type": "政府", "level": "县处级", "parent": "庆阳市人民政府", "location": "甘肃省庆阳市环县环城镇"},
    {"id": "o03", "name": "环县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "环县", "location": "甘肃省庆阳市环县环城镇"},
    {"id": "o04", "name": "中国人民政治协商会议环县委员会", "type": "政协", "level": "县处级", "parent": "环县", "location": "甘肃省庆阳市环县环城镇"},
    {"id": "o05", "name": "环县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共环县委员会", "location": "甘肃省庆阳市环县环城镇"},
    {"id": "o06", "name": "中共庆阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省庆阳市西峰区"},
    {"id": "o07", "name": "庆阳市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省庆阳市西峰区"},
]

# 3. Positions
positions = [
    # 曹育铮 (p01)
    {"person_id": "p01", "org_id": "o01", "title": "环县县委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县委全面工作。2026年7月14日调度全县防汛工作，当前在任。"},
    # 杨添翼 (p02)
    {"person_id": "p02", "org_id": "o02", "title": "环县人民政府县长", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县政府全面工作，分管县审计局。2026年7月8日主持召开县政府常务会议。"},
    {"person_id": "p02", "org_id": "o01", "title": "环县县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "兼任县政府党组书记"},
    # 前任县委书记占位 (p03)
    {"person_id": "p03", "org_id": "o01", "title": "环县前任县委书记", "start": "待查", "end": "待查", "rank": "正处级", "note": "曹育铮的前任 — 待识别"},
    # 前任县长占位 (p04)
    {"person_id": "p04", "org_id": "o02", "title": "环县前任县长", "start": "待查", "end": "待查", "rank": "正处级", "note": "杨添翼的前任 — 待识别"},
]

# 4. Relationships
relationships = [
    # 现任班子核心关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "曹育铮(书记)与杨添翼(县长): 环县党政一把手配合", "overlap_org": "中共环县委员会/环县人民政府", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    # 上级领导关系 — 庆阳市领导
    {"person_a": "p01", "person_b": "p02", "type": "same_system", "context": "环县受庆阳市领导管理", "overlap_org": "庆阳市/环县", "overlap_period": "当前", "strength": "medium", "confidence": "confirmed"},
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
    if "县委书记" in title or ("书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title):
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
    if "副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
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
    if "副县长" in title:
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
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>环县领导班子工作关系网络 - 数据来源: 环县人民政府官网及公开报道</description>')
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
        lines.append('          <attvalue for="3" value="环县"/>')
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
        lines.append('          <attvalue for="3" value="环县"/>')
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
    print(f"=== 环县网络数据构建 ===")
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
