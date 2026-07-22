#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 宁都县 (Ningdu County), 赣州市, 江西省.
县域领导班子工作关系网络

Current as of: 2026-07-15

Known officeholders:
- 县委书记: 傅小新 (male, since ~2023)
- 县长: 陈珉 (current as of 2025-2026, succeeded 何国杰)
- 县委专职副书记: unknown (待查)
- 常务副县长: unknown (待查)
- 纪委书记: unknown (待查)
- 组织部长: unknown (待查)
- 宣传部长: unknown (待查)
- 统战部长: unknown (待查)
- 政法委书记: unknown (待查)

Note: The 县政府 leadership page was not accessible via web fetch.
Standing committee composition is partially inferred from news reports.
Specific career histories are partially researched — gaps marked explicitly.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE, "宁都县_network.db")
GEXF_PATH = os.path.join(BASE, "宁都县_network.gexf")
today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ---- Core Leaders ----
    {
        "id": 1,
        "name": "傅小新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "江西赣州",
        "native_place": "江西赣州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁都县委书记",
        "current_org": "中共宁都县委员会",
        "source": "https://www.ningdu.gov.cn",
        "career_notes": "1973年10月出生。长期在赣州市工作。曾任赣州市政府副秘书长、市信访局局长等职。2023年任宁都县委书记。详细早期履历待进一步查证。"
    },
    {
        "id": 2,
        "name": "陈珉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "江西赣州",
        "native_place": "江西赣州",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁都县委副书记、县长",
        "current_org": "宁都县人民政府",
        "source": "https://www.ningdu.gov.cn",
        "career_notes": "2025-2026年任宁都县委副书记、县长。此前曾任宁都县委副书记（专职）或赣州市直部门职务。具体履历待查。2026年7月兼任宁都县人武部党委第一书记。"
    },
    # ---- Predecessors ----
    {
        "id": 3,
        "name": "何国杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "江西赣州",
        "native_place": "江西赣州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原宁都县委副书记、县长）",
        "current_org": "",
        "source": "公开报道/现有数据",
        "career_notes": "1975年11月出生。2021-2025年任宁都县委副书记、县长。前任县长。去向待查。"
    },
]

# County standing committee key departments (members unknown — placeholder nodes)
# We still create org nodes for the standard county-level orgs
organizations = [
    {"id": 1, "name": "中共宁都县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州宁都"},
    {"id": 2, "name": "宁都县人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州宁都"},
    {"id": 3, "name": "中共宁都县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市纪律检查委员会", "location": "江西赣州宁都"},
    {"id": 4, "name": "宁都县监察委员会", "type": "政府", "level": "县处级", "parent": "赣州市监察委员会", "location": "江西赣州宁都"},
    {"id": 5, "name": "中共宁都县委组织部", "type": "党委", "level": "县处级", "parent": "中共宁都县委员会", "location": "江西赣州宁都"},
    {"id": 6, "name": "中共宁都县委宣传部", "type": "党委", "level": "县处级", "parent": "中共宁都县委员会", "location": "江西赣州宁都"},
    {"id": 7, "name": "中共宁都县委统战部", "type": "党委", "level": "县处级", "parent": "中共宁都县委员会", "location": "江西赣州宁都"},
    {"id": 8, "name": "中共宁都县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共宁都县委员会", "location": "江西赣州宁都"},
    {"id": 9, "name": "宁都县人民武装部", "type": "党委", "level": "县处级", "parent": "赣州军分区", "location": "江西赣州宁都"},
    {"id": 10, "name": "宁都县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "赣州市人民代表大会常务委员会", "location": "江西赣州宁都"},
    {"id": 11, "name": "中国人民政治协商会议宁都县委员会", "type": "政协", "level": "县处级", "parent": "政协赣州市委员会", "location": "江西赣州宁都"},
]

positions = [
    # ---- Current leaders ----
    {"id": 1, "person_id": 1, "org_id": 1, "title": "宁都县委书记", "start": "2023", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "宁都县委副书记、县长", "start": "2025", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "宁都县委副书记", "start": "2025", "end": "", "rank": "县处级副职", "note": "兼任县长"},
    {"id": 4, "person_id": 2, "org_id": 9, "title": "宁都县人武部党委第一书记", "start": "2026-07", "end": "", "rank": "", "note": "兼任"},
    # ---- Predecessors ----
    {"id": 5, "person_id": 3, "org_id": 2, "title": "宁都县委副书记、县长（前任）", "start": "2021", "end": "2025", "rank": "县处级正职", "note": "前任县长"},
    {"id": 6, "person_id": 3, "org_id": 1, "title": "宁都县委副书记（前任）", "start": "2021", "end": "2025", "rank": "县处级副职", "note": "兼任"},
]

relationships = [
    # ---- 县委书记 ↔ 县长 ----
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "傅小新（县委书记）与陈珉（县长）为目前宁都县党政正职搭档",
     "overlap_org": "宁都县", "overlap_period": "2025至今",
     "confidence": "confirmed"},
    # ---- 前任 → 现任（县长） ----
    {"id": 2, "person_a_id": 3, "person_b_id": 2, "type": "前任继任",
     "context": "何国杰为宁都县长前任，陈珉为现任",
     "overlap_org": "宁都县人民政府", "overlap_period": "",
     "confidence": "confirmed"},
]

# =========================================================================
# BUILD SQLite Database
# =========================================================================

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
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
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)",
            (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"])
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (id, person_a_id, person_b_id, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?,?)",
            (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  ✓ SQLite: {DB_PATH}")


# =========================================================================
# BUILD GEXF Graph
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role."""
    title = p["current_post"]
    if "书记" in title and "县委" in title and "纪委" not in title:
        return "255,50,50"
    elif "县长" in title or "副县长" in title or "区长" in title:
        return "50,100,255"
    elif "纪委" in title or "监委" in title:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(p):
    ids_with_roles = {1, 2, 3}  # 书记+县长+主要前任
    return p["id"] in ids_with_roles

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>宁都县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["current_post"])}"/>')
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
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"]
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================

def main():
    print("宁都县领导班子工作关系网络数据生成")
    print(f"生成日期: {today}")
    print(f"人员: {len(persons)} 人")
    print(f"机构: {len(organizations)} 个")
    print(f"任职: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")
    print()

    print("构建 SQLite 数据库...")
    build_db()

    print("构建 GEXF 图文件...")
    build_gexf()

    print()
    print("数据生成完成!")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Summary stats
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"  {table}: {count} 条")
    conn.close()


if __name__ == "__main__":
    main()
