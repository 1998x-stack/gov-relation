#!/usr/bin/env python3
"""安定区 (定西市, 甘肃省) 领导班子工作关系网络数据构建脚本"""

import os
import sqlite3
from datetime import datetime

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "安定区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "安定区_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    {
        "id": "anding_jia_wenju",
        "name": "贾文举",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定西市副市长、安定区委书记",
        "current_org": "中共定西市安定区委员会",
        "source": "https://www.anding.gov.cn/art/2026/4/22/art_524_1891607.html",
    },
    {
        "id": "anding_yang_kang",
        "name": "杨康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安定区委副书记、区长",
        "current_org": "安定区人民政府",
        "source": "https://www.anding.gov.cn/art/2026/7/12/art_521_1902944.html",
    },
]

# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共定西市安定区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定西市委员会",
        "location": "甘肃省定西市安定区",
    },
    {
        "id": 2,
        "name": "安定区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "定西市人民政府",
        "location": "甘肃省定西市安定区",
    },
    {
        "id": 3,
        "name": "定西市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "甘肃省人民政府",
        "location": "甘肃省定西市",
    },
    {
        "id": 4,
        "name": "中共定西市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省定西市",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    {
        "person_id": "anding_jia_wenju",
        "org_id": 1,
        "title": "安定区委书记",
        "start": "",
        "end": "present",
        "rank": "副厅级",
        "note": "同时担任定西市副市长",
    },
    {
        "person_id": "anding_jia_wenju",
        "org_id": 3,
        "title": "定西市副市长",
        "start": "",
        "end": "present",
        "rank": "副厅级",
        "note": "同时担任安定区委书记",
    },
    {
        "person_id": "anding_yang_kang",
        "org_id": 2,
        "title": "安定区区长",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "区委副书记",
    },
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    {
        "person_a": "anding_jia_wenju",
        "person_b": "anding_yang_kang",
        "type": "superior_subordinate",
        "context": "区委书记-区长搭班工作关系",
        "overlap_org": "中共定西市安定区委员会/安定区人民政府",
        "overlap_period": "2025-2026",
        "confidence": "confirmed",
    },
]

# ═══════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        return "255,50,50"    # Red — Party Secretary
    if "市长" in title or "区长" in title or ("副" not in title and "书记" not in title):
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title or "监察" in title or "纪委书记" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副" in title and ("区" in title or "市" in title or "县" in title):
        return "100,100,200"  # Light blue — Deputy
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other


def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title:
        return "20.0"
    if "市长" in title or "区长" in title and "副" not in title:
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副" in title:
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

    c.execute("DROP TABLE IF EXISTS persons")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS relationships")

    c.execute("""CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id INTEGER, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["education"],
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
            pos["start"], pos["end"], pos["rank"], pos.get("note", "")
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
    lines.append('    <description>安定区领导班子工作关系网络 - 数据来源: 安定区人民政府官网及公开报道</description>')
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
        lines.append('          <attvalue for="3" value="定西市"/>')
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
        lines.append('          <attvalue for="3" value="定西市"/>')
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
    print(f"=== 安定区网络数据构建 ===")
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
