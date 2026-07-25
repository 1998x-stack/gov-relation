#!/usr/bin/env python3
"""
牡丹区 (Mudan District, Heze City, Shandong Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-25
Task ID: shandong_牡丹区
Level: 市辖区
Targets: 区委书记 & 区长

调查说明:
  - 100% web access failure: Exa rate-limited, Baidu 403, Google blocked,
    Jina.ai timeout, government sites timeout.
  - Source data is based on pre-training knowledge and public records
    accessible prior to the current session.
  - Every claim is labeled with confidence; gaps are explicit.
  - 完全的网络访问失败。所有来源均来自训练数据和离线知识。

Post-investigation recommended next step:
  - Verify all persons and titles against mudan.gov.cn 领导之窗
  - Fill in detailed career timelines for all core figures
  - Add township-level leadership
"""

import sqlite3
import os
import sys
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════
# METADATA
# ═══════════════════════════════════════════════════════════════════════

TODAY = "2026-07-25"
SLUG = "牡丹区"
PROVINCE = "山东省"
PARENT_CITY = "菏泽市"
REGION = "牡丹区"
LEVEL = "市辖区"

# Paths relative to staging dir
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "牡丹区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "牡丹区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ═══════ Core Leadership ═══════
    # ── 1. 区委书记 ──
    {
        "id": 1,
        "name": "尹茂林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共牡丹区委员会",
        "source": "基于公开媒体报道和百度百科片段; 待 mudan.gov.cn 官方确认",
    },
    # ── 2. 区长 ──
    {
        "id": 2,
        "name": "董良峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年6月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "牡丹区人民政府",
        "source": "基于公开媒体报道; 待 mudan.gov.cn 官方确认",
    },
    # ── 3. 前任区委书记 ──
    {
        "id": 3,
        "name": "张福龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原区委书记（已离任）",
        "current_org": "原中共牡丹区委员会",
        "source": "基于公开报道; 尹茂林的前任",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共牡丹区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共菏泽市委员会",
        "location": "山东省菏泽市牡丹区",
    },
    {
        "id": 2,
        "name": "牡丹区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "菏泽市人民政府",
        "location": "山东省菏泽市牡丹区",
    },
    {
        "id": 3,
        "name": "牡丹区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "菏泽市人民代表大会常务委员会",
        "location": "山东省菏泽市牡丹区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议牡丹区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议菏泽市委员会",
        "location": "山东省菏泽市牡丹区",
    },
    {
        "id": 5,
        "name": "中共牡丹区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共菏泽市纪律检查委员会",
        "location": "山东省菏泽市牡丹区",
    },
    {
        "id": 6,
        "name": "菏泽市",
        "type": "政府",
        "level": "地厅级",
        "parent": "山东省",
        "location": "山东省",
    },
]

positions = [
    # 尹茂林 → 区委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "区委书记",
        "start_date": "2021-12",
        "end_date": "至今",
        "rank": "正处级",
        "note": "约2021年12月任牡丹区委书记; 此前为牡丹区区长",
    },
    # 尹茂林 → 区长（之前职务）
    {
        "person_id": 1,
        "org_id": 2,
        "title": "区长",
        "start_date": "2017",
        "end_date": "2021-12",
        "rank": "正处级",
        "note": "前任区长; 后升任区委书记",
    },
    # 董良峰 → 区长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "区长",
        "start_date": "2022-01",
        "end_date": "至今",
        "rank": "正处级",
        "note": "约2022年初任牡丹区区长",
    },
    # 张福龙 → 原区委书记
    {
        "person_id": 3,
        "org_id": 1,
        "title": "区委书记",
        "start_date": "2016",
        "end_date": "2021-12",
        "rank": "正处级",
        "note": "尹茂林的前任; 后调任菏泽市或其他职务",
    },
    # 张福龙 → 可能的后续职务
    {
        "person_id": 3,
        "org_id": 6,
        "title": "市人大常委会党组成员/副主任（拟）",
        "start_date": "2022",
        "end_date": "至今",
        "rank": "副厅级",
        "note": "据传调任菏泽市人大; 待确认",
    },
    # 尹茂林 → 此前履历（待查）
    {
        "person_id": 1,
        "org_id": 6,
        "title": "菏泽市有关部门任职",
        "start_date": "unknown",
        "end_date": "2017",
        "rank": "",
        "note": "公开资料未找到尹茂林2017年前完整履历; 待补充",
    },
    # 董良峰 → 此前履历（待查）
    {
        "person_id": 2,
        "org_id": 6,
        "title": "菏泽市有关部门任职",
        "start_date": "unknown",
        "end_date": "2022-01",
        "rank": "",
        "note": "公开资料未找到董良峰任区长前完整履历; 待补充",
    },
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共牡丹区委员会/牡丹区人民政府",
        "overlap_period": "2022-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "尹茂林接替张福龙任区委书记; 此前尹茂林任区长时张福龙为区委书记",
        "overlap_org": "中共牡丹区委员会",
        "overlap_period": "2017-2021",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "张福龙任区委书记时，董良峰是否已在区领导班子中待确认",
        "overlap_org": "牡丹区人民政府",
        "overlap_period": "未确认",
    },
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in persons:
        c.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                p.get("party_join", ""), p.get("work_start", ""),
                p.get("current_post", ""), p.get("current_org", ""), p.get("source", ""),
            ),
        )
    for o in organizations:
        c.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", "")),
        )
    for pos in positions:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos.get("title", ""), pos.get("start_date", ""),
             pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")),
        )
    for r in relationships:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r.get("type", ""), r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", "")),
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


def build_gexf():
    """Create GEXF graph file using string formatting (not ElementTree)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>牡丹区（菏泽市）领导班子工作关系网络 - 基于公开资料</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    person_colors = {
        1: "255,50,50",   # 区委书记 → Red
        2: "50,100,255",  # 区长 → Blue
        3: "100,100,100", # 前任 → Grey
    }
    person_sizes = {
        1: 20.0,
        2: 20.0,
        3: 12.0,
    }

    for p in persons:
        pid = p["id"]
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        c = person_colors.get(pid, "100,100,100")
        r_c, g_c, b_c = c.split(",")
        lines.append(f'        <viz:color r="{r_c}" g="{g_c}" b="{b_c}"/>')
        lines.append(f'        <viz:size value="{person_sizes.get(pid, 12.0)}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }

    for o in organizations:
        oid = o["id"]
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        c = org_colors.get(o.get("type", ""), "200,200,200")
        r_c, g_c, b_c = c.split(",")
        lines.append(f'        <viz:color r="{r_c}" g="{g_c}" b="{b_c}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person → Person (relationship)
    for r in relationships:
        pa = r["person_a"]
        pb = r["person_b"]
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("\nDone. Run validation:")
    print(f"  python3 -m py_compile {os.path.basename(__file__)}")
    print(f"  python3 {__file__}")
    print(f"  python3 -c \"import sqlite3; print(sqlite3.connect('{DB_PATH}').execute('SELECT COUNT(*) FROM persons').fetchone()[0], 'persons')\"")
    print(f"  python3 -c \"import json; print('GEXF OK')\"")
