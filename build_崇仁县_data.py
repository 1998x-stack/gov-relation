#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 崇仁县, 抚州市, 江西省.

崇仁县领导班子:
  - 县委书记: [待核实] — 姓名和履历均需查证
  - 县长: [待核实] — 姓名和履历均需查证

崇仁县为抚州市下辖县，位于江西省中部。
本脚本使用占位数据构建结构框架，所有个人信息均标记为"待核实"。

Research constraints: 2026-07-15 — external web access (Baidu Baike, gov sites, search engines)
all blocked by network firewall. Person names, career timelines, and roster data are placeholder
scaffolding that must be filled when web access is restored.

Research date: 2026-07-15
"""

import sqlite3
import os
import sys
from datetime import datetime

# Paths
STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(STAGING, "..", ".."))
DB_PATH = os.path.join(STAGING, "崇仁县_network.db")
GEXF_PATH = os.path.join(STAGING, "崇仁县_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# Research Data
# =========================================================================
# ⚠️ ALL PERSONS DATA IS PLACEHOLDER / NEEDS VERIFICATION
# External web search was unavailable at build time.

persons = [
    {
        "id": 1,
        "name": "[待核实·崇仁县委书记]",
        "gender": "[待核实]",
        "ethnicity": "汉族",
        "birth": "[待核实]",
        "birthplace": "[待核实]",
        "education": "[待核实]",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崇仁县委书记",
        "current_org": "中共崇仁县委员会",
        "source": "需查阅崇仁县政府官网或江西省委组织部任前公示",
        "notes": "公开资料未能获取当前县委书记姓名及履历。请访问 www.chongren.gov.cn 或搜索'崇仁县委书记 任前公示'补充。"
    },
    {
        "id": 2,
        "name": "[待核实·崇仁县长]",
        "gender": "[待核实]",
        "ethnicity": "汉族",
        "birth": "[待核实]",
        "birthplace": "[待核实]",
        "education": "[待核实]",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崇仁县委副书记、县长",
        "current_org": "崇仁县人民政府",
        "source": "需查阅崇仁县政府官网或江西省委组织部任前公示",
        "notes": "公开资料未能获取当前县长姓名及履历。请访问 www.chongren.gov.cn 或搜索'崇仁县 县长'补充。"
    },
    # Known figures with 崇仁县 connections (for cross-network edges)
    {
        "id": 3,
        "name": "包峰亭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1990",
        "current_post": "萍乡市人大常委会副主任（兼石城县委书记）",
        "current_org": "萍乡市人大常委会",
        "source": "build_pingxiang_data.py",
        "notes": "曾于2005-2006年任崇仁县人民政府副县长（副县级），现已调离崇仁县。用于跨县工作关系网络。"
    },
    {
        "id": 4,
        "name": "颜赣辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-02",
        "birthplace": "江西崇仁",
        "education": "江西财经学院计划统计系工业统计专业",
        "party_join": "（2021年2月开除党籍）",
        "work_start": "1982-08",
        "current_post": "（2021年被判刑11年）",
        "current_org": "（原宜春市委书记）",
        "source": "build_jingdezhen_mayor_data.py; 人民网",
        "notes": "崇仁籍高官，曾任宜春市委书记，2021年因受贿被判刑11年。用于展示崇仁县籍贯人士在省内的影响力网络。"
    },
]

orgs = [
    {
        "id": 1,
        "name": "中共崇仁县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西抚州崇仁"
    },
    {
        "id": 2,
        "name": "崇仁县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西抚州崇仁"
    },
    {
        "id": 3,
        "name": "萍乡市人大常委会",
        "type": "人大",
        "level": "厅局级",
        "parent": "",
        "location": "江西萍乡"
    },
    {
        "id": 4,
        "name": "原宜春市委",
        "type": "党委",
        "level": "厅局级",
        "parent": "",
        "location": "江西宜春"
    },
]

positions = [
    # 崇仁县领导 — placeholder positions
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "崇仁县委书记",
        "start": "[待核实]",
        "end": "",
        "rank": "县处级正职",
        "note": "现任（姓名待核实）"
    },
    {
        "id": 2,
        "person_id": 2,
        "org_id": 2,
        "title": "崇仁县委副书记、县长",
        "start": "[待核实]",
        "end": "",
        "rank": "县处级正职",
        "note": "现任（姓名待核实）"
    },
    # 包峰亭 — 曾任职崇仁
    {
        "id": 3,
        "person_id": 3,
        "org_id": 2,
        "title": "崇仁县人民政府副县长",
        "start": "2005",
        "end": "2006",
        "rank": "副县级",
        "note": "调离崇仁后历任乐安、石城等县"
    },
    {
        "id": 4,
        "person_id": 3,
        "org_id": 3,
        "title": "萍乡市人大常委会副主任（兼石城县委书记）",
        "start": "2020",
        "end": "",
        "rank": "副厅级",
        "note": "获评全国脱贫攻坚先进个人"
    },
    # 颜赣辉 — 崇仁籍
    {
        "id": 5,
        "person_id": 4,
        "org_id": 4,
        "title": "宜春市委书记",
        "start": "",
        "end": "2021",
        "rank": "正厅级",
        "note": "2021年被查判刑"
    },
]

relationships = [
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政搭档",
        "context": "[待核实]县委书记与[待核实]县长在崇仁县党政班子搭档",
        "overlap_org": "崇仁县",
        "overlap_period": "[待核实]-至今"
    },
    {
        "id": 2,
        "person_a_id": 3,
        "person_b_id": 4,
        "type": "同籍贯",
        "context": "包峰亭（曾在崇仁任职）和颜赣辉（崇仁籍）均与崇仁县有不同程度关联",
        "overlap_org": "崇仁县",
        "overlap_period": "—"
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
    if "副县长" in post:
        return "80,140,230"  # lighter blue for deputies
    return "120,120,120"  # grey


def ocolor_viz(otype):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
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
    lines.append('    <description>崇仁县领导班子工作关系网络 - 2026-07-15 (⚠️ 数据为占位框架，需核实)</description>')
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
    print(f"  崇仁县领导班子工作关系网络 — 数据构建")
    print(f"  日期: {today}")
    print(f"  ⚠️  注意：当前数据为结构框架，人员姓名和履历均为占位符。")
    print(f"       外网访问受限，无法获取实际领导信息。")
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
        print(f"\n  ✓ BUILD COMPLETE (占位框架数据)")
        print(f"    DB size: {os.path.getsize(DB_PATH)} bytes")
        print(f"    GEXF size: {os.path.getsize(GEXF_PATH)} bytes")
        print()
        print(f"  ⚠️  下一步工作：")
        print(f"    1. 外网恢复后，访问 www.chongren.gov.cn 获取崇仁县领导名单")
        print(f"    2. 搜索'崇仁县委书记 任前公示'获取姓名")
        print(f"    3. 搜索'崇仁县长'获取县长姓名")
        print(f"    4. 逐个搜索领导人简历信息")
        print(f"    5. 更新 persons/positions/relationships 数据")
        print(f"    6. 重新运行本脚本 + 更新 person JSON + 报告")
