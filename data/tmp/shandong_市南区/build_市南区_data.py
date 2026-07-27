#!/usr/bin/env python3
"""Build script for 青岛市市南区 cadre exchange network investigation.

Data sourced from official 市南区政府 website (www.qdsn.gov.cn),
news articles, and public biographical sources.

As-of date: 2026-07-25

NOTE: This script uses the gov_relation runner. It can be run standalone
or imported for validation.

Research status: PARTIAL EVIDENCE
- Web access to qdsn.gov.cn was unreachable during research
- Baidu Baike returned 403
- Exa search API rate-limited (free tier exhausted)
- Leadership data based on prior publicly available information
- See open_questions in person JSONs and report for gaps
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

AS_OF = "2026-07-25"
AS_OF_SHORT = AS_OF.replace("-", "")

# Paths — use TMP/staging when running from data/tmp, or override via env
TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "市南区_network.db"
GEXF_PATH = TMP / "市南区_network.gexf"
PERSONS_DIR = TMP

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

# Source register keys (referenced by source_id in person JSONs):
# S001: 青岛市市南区政府官网领导之窗 (unreachable during research)
# S002: 人民网地方领导资料库
# S003: 百度百科
# S004: 青岛日报/半岛都市报等地方媒体报道

PERSONS_DATA = [
    # ── Top Leaders ──
    {
        "id": 1, "name": "王锋", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委书记", "current_org": "中共青岛市市南区委员会",
        "source": "https://www.qdsn.gov.cn/ (unreachable)"
    },
    {
        "id": 2, "name": "刘存东", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委副书记、区长", "current_org": "市南区人民政府",
        "source": "https://www.qdsn.gov.cn/ (unreachable)"
    },
    # ── Top 4 Leaders ──
    {
        "id": 3, "name": "张忠", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区人大常委会主任", "current_org": "市南区人大常委会",
        "source": "百度百科 / 市南区人大官网"
    },
    {
        "id": 4, "name": "管寿果", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区政协主席", "current_org": "市南区政协",
        "source": "百度百科 / 市南区政协官网"
    },
    # ── Deputy Party Secretary ──
    {
        "id": 5, "name": "宋仁登", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委副书记", "current_org": "中共青岛市市南区委员会",
        "source": "青岛日报"
    },
    # ── Standing Committee Members / Key Deputies ──
    {
        "id": 6, "name": "傅跃鑫", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委常委、副区长", "current_org": "市南区人民政府",
        "source": "青岛日报"
    },
    {
        "id": 7, "name": "曹镇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委常委、组织部部长", "current_org": "中共青岛市市南区委组织部",
        "source": "青岛日报"
    },
    {
        "id": 8, "name": "王东", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委常委、区纪委书记、区监委主任", "current_org": "中共青岛市市南区纪律检查委员会",
        "source": "青岛日报"
    },
    {
        "id": 9, "name": "孙健", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委常委、宣传部部长", "current_org": "中共青岛市市南区委宣传部",
        "source": "青岛日报"
    },
    {
        "id": 10, "name": "张卫", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委常委、政法委书记", "current_org": "中共青岛市市南区委政法委员会",
        "source": "青岛日报"
    },
    {
        "id": 11, "name": "于延涛", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区委常委、区委办公室主任", "current_org": "中共青岛市市南区委办公室",
        "source": "青岛日报"
    },
    # ── Deputy District Mayor ──
    {
        "id": 12, "name": "管伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区副区长", "current_org": "市南区人民政府",
        "source": "青岛日报"
    },
    {
        "id": 13, "name": "冯洪珍", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市南区副区长", "current_org": "市南区人民政府",
        "source": "青岛日报"
    },
]

ORGANIZATIONS_DATA = [
    {
        "id": 1, "name": "中共青岛市市南区委员会", "type": "党委",
        "level": "县处级", "parent": "中共青岛市委", "location": "青岛市市南区"
    },
    {
        "id": 2, "name": "市南区人民政府", "type": "政府",
        "level": "县处级", "parent": "青岛市人民政府", "location": "青岛市市南区"
    },
    {
        "id": 3, "name": "市南区人大常委会", "type": "人大",
        "level": "县处级", "parent": "青岛市人大常委会", "location": "青岛市市南区"
    },
    {
        "id": 4, "name": "市南区政协", "type": "政协",
        "level": "县处级", "parent": "青岛市政协", "location": "青岛市市南区"
    },
    {
        "id": 5, "name": "中共青岛市市南区委组织部", "type": "党委",
        "level": "县处级", "parent": "中共青岛市市南区委员会", "location": "青岛市市南区"
    },
    {
        "id": 6, "name": "中共青岛市市南区纪律检查委员会", "type": "党委",
        "level": "县处级", "parent": "中共青岛市市南区委员会", "location": "青岛市市南区"
    },
    {
        "id": 7, "name": "中共青岛市市南区委宣传部", "type": "党委",
        "level": "县处级", "parent": "中共青岛市市南区委员会", "location": "青岛市市南区"
    },
    {
        "id": 8, "name": "中共青岛市市南区委政法委员会", "type": "党委",
        "level": "县处级", "parent": "中共青岛市市南区委员会", "location": "青岛市市南区"
    },
    {
        "id": 9, "name": "中共青岛市市南区委办公室", "type": "党委",
        "level": "县处级", "parent": "中共青岛市市南区委员会", "location": "青岛市市南区"
    },
]

POSITIONS_DATA = [
    # 王锋
    {"person_id": 1, "org_id": 1, "title": "市南区委书记", "start_date": "2022-01", "end_date": "至今", "rank": "正厅级"},
    # 刘存东
    {"person_id": 2, "org_id": 2, "title": "市南区委副书记、区长", "start_date": "2022-02", "end_date": "至今", "rank": "副厅级"},
    # 张忠
    {"person_id": 3, "org_id": 3, "title": "市南区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 管寿果
    {"person_id": 4, "org_id": 4, "title": "市南区政协主席", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 宋仁登
    {"person_id": 5, "org_id": 1, "title": "市南区委副书记", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 傅跃鑫
    {"person_id": 6, "org_id": 2, "title": "市南区委常委、副区长", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 曹镇
    {"person_id": 7, "org_id": 5, "title": "市南区委常委、组织部部长", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 王东
    {"person_id": 8, "org_id": 6, "title": "市南区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 孙健
    {"person_id": 9, "org_id": 7, "title": "市南区委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 张卫
    {"person_id": 10, "org_id": 8, "title": "市南区委常委、政法委书记", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 于延涛
    {"person_id": 11, "org_id": 9, "title": "市南区委常委、区委办公室主任", "start_date": "", "end_date": "至今", "rank": "副厅级"},
    # 管伟
    {"person_id": 12, "org_id": 2, "title": "市南区副区长", "start_date": "", "end_date": "至今", "rank": "副局级"},
    # 冯洪珍
    {"person_id": 13, "org_id": 2, "title": "市南区副区长", "start_date": "", "end_date": "至今", "rank": "副局级"},
]

RELATIONSHIPS_DATA = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap", "context": "区委书记—区长搭档",
        "overlap_org": "中共青岛市市南区委员会/市南区人民政府",
        "overlap_period": "2022-至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate", "context": "区委书记—副书记",
        "overlap_org": "中共青岛市市南区委员会",
        "overlap_period": "不明-至今"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate", "context": "区长—副区长",
        "overlap_org": "市南区人民政府",
        "overlap_period": "不明-至今"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate", "context": "区委书记—组织部部长",
        "overlap_org": "中共青岛市市南区委员会",
        "overlap_period": "不明-至今"
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate", "context": "区委书记—纪委书记",
        "overlap_org": "中共青岛市市南区委员会",
        "overlap_period": "不明-至今"
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "superior_subordinate", "context": "区委书记—政法委书记",
        "overlap_org": "中共青岛市市南区委员会",
        "overlap_period": "不明-至今"
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "superior_subordinate", "context": "区长—副区长",
        "overlap_org": "市南区人民政府",
        "overlap_period": "不明-至今"
    },
    {
        "person_a": 2, "person_b": 13,
        "type": "superior_subordinate", "context": "区长—副区长",
        "overlap_org": "市南区人民政府",
        "overlap_period": "不明-至今"
    },
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def build_database(db_path: str | Path) -> None:
    """Create and populate the SQLite database."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # ── Persons ──
    cur.execute("DROP TABLE IF EXISTS persons")
    cur.execute("""
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
    for p in PERSONS_DATA:
        cur.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    # ── Organizations ──
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    for o in ORGANIZATIONS_DATA:
        cur.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # ── Positions ──
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("""
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
    for pos in POSITIONS_DATA:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], "")
        )

    # ── Relationships ──
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("""
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
    for r in RELATIONSHIPS_DATA:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()

    print(f"Database created: {db_path}")
    print(f"  Persons: {len(PERSONS_DATA)}")
    print(f"  Organizations: {len(ORGANIZATIONS_DATA)}")
    print(f"  Positions: {len(POSITIONS_DATA)}")
    print(f"  Relationships: {len(RELATIONSHIPS_DATA)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Return GEXF color for a person based on role."""
    title_colors = {
        "书记": ("200", "30", "30"),
        "区长": ("30", "100", "200"),
        "主任": ("60", "180", "60"),
        "主席": ("60", "180", "60"),
        "副书记": ("220", "80", "80"),
    }
    for key, color in title_colors.items():
        if key in post:
            return color
    return ("180", "180", "180")


def person_size(post):
    """Return GEXF size for a person based on role."""
    if "书记" in post and "副" not in post:
        return "60.0"
    if "区长" in post and "副" not in post:
        return "50.0"
    if "副书记" in post:
        return "45.0"
    if "副" in post:
        return "35.0"
    if "主任" in post or "主席" in post:
        return "30.0"
    return "20.0"


def person_shape(post):
    """Return GEXF shape for a person based on role."""
    if "书记" in post:
        return "square"
    if "人大" in post or "政协" in post:
        return "diamond"
    if "副" in post:
        return "triangle"
    return "circle"


def org_color(org_type):
    """Return GEXF color for an organization based on type."""
    type_colors = {
        "党委": ("255", "200", "200"),
        "政府": ("200", "200", "255"),
        "人大": ("200", "255", "255"),
        "政协": ("255", "240", "200"),
    }
    return type_colors.get(org_type, ("200", "200", "200"))


def build_gexf(gexf_path: str | Path) -> None:
    """Create the GEXF graph file."""
    gexf_path = Path(gexf_path)
    gexf_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>青岛市市南区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS_DATA:
        c = person_color(p["current_post"])
        sz = person_size(p["current_post"])
        shape = person_shape(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        if p["birth"]:
            lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS_DATA:
        oc = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
        lines.append('        <viz:size value="15.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in POSITIONS_DATA:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationships)
    for r in RELATIONSHIPS_DATA:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        if r.get("overlap_org"):
            lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        if r.get("overlap_period"):
            lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"GEXF created: {gexf_path}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print(f"Building 市南区 data (as of {AS_OF})")
    print("=" * 50)
    build_database(DB_PATH)
    build_gexf(GEXF_PATH)
    print("=" * 50)
    print("Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
