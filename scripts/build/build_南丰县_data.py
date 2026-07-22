#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 南丰县, 抚州市, 江西省.

南丰县领导班子:
  - 县委书记: 叶峰 — 已知姓名，履历需补充细节
  - 县委副书记、县长: 张沥泉 — 已知姓名，履历需补充细节

南丰县为抚州市下辖县，位于江西省东部，与福建省接壤。
以蜜桔产业闻名，有"中国蜜桔之乡"之称。

Research date: 2026-07-15
"""

import sqlite3
import os
import sys
from datetime import datetime

# Paths
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "南丰县_network.db")
GEXF_PATH = os.path.join(STAGING, "南丰县_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# Research Data
# =========================================================================

persons = [
    # ── 南丰县委书记 叶峰 ──
    {
        "id": 1,
        "name": "叶峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南丰县委书记",
        "current_org": "中共南丰县委员会",
        "source": "Baike/Baidu; 南丰县政府官网",
        "notes": "叶峰任南丰县委书记，具体履历需进一步查证。曾可能任职于抚州市或江西省直部门。"
    },
    # ── 南丰县长 张沥泉 ──
    {
        "id": 2,
        "name": "张沥泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南丰县委副书记、县长",
        "current_org": "南丰县人民政府",
        "source": "Baike/Baidu; 南丰县政府官网",
        "notes": "张沥泉任南丰县长，具体履历需进一步查证。"
    },
    # ── 抚州市委书记 范小林（上级领导，用于跨级关系网络） ──
    {
        "id": 3,
        "name": "范小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "江西宜丰",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委书记",
        "current_org": "中共抚州市委员会",
        "source": "build_fuzhou_data.py; 澎湃新闻",
        "notes": "抚州市委书记，南丰县的上级领导。2024.10从省纪委常务副书记空降抚州。"
    },
    # ── 抚州市长 王宏安（上级领导，用于跨级关系网络） ──
    {
        "id": 4,
        "name": "王宏安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-08",
        "birthplace": "江西彭泽",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委副书记、市长",
        "current_org": "抚州市人民政府",
        "source": "build_fuzhou_data.py; district.ce.cn",
        "notes": "抚州市长，南丰县的上级领导。2025年1月确认。"
    },
]

orgs = [
    {
        "id": 1,
        "name": "中共南丰县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西抚州南丰"
    },
    {
        "id": 2,
        "name": "南丰县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西抚州南丰"
    },
    {
        "id": 3,
        "name": "中共抚州市委员会",
        "type": "党委",
        "level": "厅局级",
        "parent": "中共江西省委员会",
        "location": "江西抚州"
    },
    {
        "id": 4,
        "name": "抚州市人民政府",
        "type": "政府",
        "level": "厅局级",
        "parent": "江西省人民政府",
        "location": "江西抚州"
    },
]

positions = [
    # 叶峰 — 南丰县委书记
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "南丰县委书记",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "现任南丰县委书记，具体到任时间待查"
    },
    # 张沥泉 — 南丰县长
    {
        "id": 2,
        "person_id": 2,
        "org_id": 2,
        "title": "南丰县委副书记、县长",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "现任南丰县长，具体到任时间待查"
    },
    # 范小林 — 抚州市委书记
    {
        "id": 3,
        "person_id": 3,
        "org_id": 3,
        "title": "抚州市委书记",
        "start": "2024-10",
        "end": "",
        "rank": "正厅级",
        "note": "2024.10从省纪委常务副书记空降抚州"
    },
    # 王宏安 — 抚州市长
    {
        "id": 4,
        "person_id": 4,
        "org_id": 4,
        "title": "抚州市委副书记、市长",
        "start": "",
        "end": "",
        "rank": "正厅级",
        "note": "2025年1月确认在任"
    },
]

relationships = [
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政搭档",
        "context": "叶峰（县委书记）与张沥泉（县长）在南丰县党政班子搭档",
        "overlap_org": "南丰县",
        "overlap_period": "—至今"
    },
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "上下级关系",
        "context": "叶峰（南丰县委书记）受范小林（抚州市委书记）领导",
        "overlap_org": "抚州市",
        "overlap_period": "2024-10至今"
    },
    {
        "id": 3,
        "person_a_id": 2,
        "person_b_id": 4,
        "type": "上下级关系",
        "context": "张沥泉（南丰县长）受王宏安（抚州市长）领导",
        "overlap_org": "抚州市",
        "overlap_period": ""
    },
]


# =========================================================================
# Utility functions
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    """Return viz:color RGB string based on post title."""
    post = post or ""
    if "书记" in post and ("县委" in post or "区委" in post):
        return "255,50,50"  # red for party secretary
    if "县长" in post and "副" not in post:
        return "50,100,255"  # blue for government head
    if "副市长" in post or "副县长" in post:
        return "80,140,230"  # lighter blue for deputies
    if "市长" in post:
        return "50,100,255"
    return "120,120,120"  # grey


def ocolor_viz(otype):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(otype, "200,200,200")


# =========================================================================
# SQLite Build
# =========================================================================

def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
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
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY,
        person_a_id INTEGER NOT NULL,
        person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        c.execute(
            "INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    for o in orgs:
        c.execute(
            "INSERT INTO organizations VALUES(?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        c.execute(
            "INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
            (pos["id"], pos["person_id"], pos["org_id"],
             pos["title"], pos["start"], pos["end"],
             pos["rank"], pos["note"])
        )

    for r in relationships:
        c.execute(
            "INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
            (r["id"], r["person_a_id"], r["person_b_id"],
             r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    return counts


# =========================================================================
# GEXF Build
# =========================================================================

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>南丰县领导班子工作关系网络 - 2026-07-15</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = pcolor_viz(p["current_post"])
        sz = "20.0" if p["id"] <= 2 else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")),
                     ("2", p.get("birthplace", "")), ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in orgs:
        c = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""),
                     ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
            f'label="{esc(pos["title"])}" weight="1.0">'
        )
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start", "")),
                     ("2", pos.get("end", "")), ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" '
            f'label="{esc(r["type"])}" weight="2.0">'
        )
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(orgs)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# Main
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print(f"  南丰县领导班子工作关系网络 — 数据构建")
    print(f"  日期: {today}")
    print("=" * 60)

    # SQLite
    counts = build_sqlite()
    print(f"\n  ✓ SQLite: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    # GEXF
    tn, te = build_gexf()
    print(f"\n  ✓ GEXF: {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    # Verify
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"Database not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF not created: {GEXF_PATH}")

    if errors:
        print(f"\n  ✗ ERRORS:")
        for e in errors:
            print(f"    - {e}")
        sys.exit(1)
    else:
        print(f"\n  ✓ BUILD COMPLETE")
        print(f"    DB size: {os.path.getsize(DB_PATH)} bytes")
        print(f"    GEXF size: {os.path.getsize(GEXF_PATH)} bytes")
        print()
        print(f"  ⚠️  下一步工作：")
        print(f"    1. 通过南丰县政府官网或百度百科确认叶峰、张沥泉的完整履历")
        print(f"    2. 搜索'南丰县委书记 叶峰 简历'补充个人信息")
        print(f"    3. 搜索'南丰县长 张沥泉 简历'补充个人信息")
        print(f"    4. 确认2026年是否有人事调整（叶峰/张沥泉是否仍在任）")
        print(f"    5. 确认南丰县领导班子其他成员（副书记、常务副县长、纪委书记等）")
        print(f"    6. 更新 persons/positions/relationships 数据")
        print(f"    7. 重新运行本脚本 + 更新 person JSON + 报告")
