#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 莎车县 (Shache County) leadership network."""

import sys
import os
from datetime import datetime

# Ensure the staging directory is writable
STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(STAGING, "..", ".."))
DB_PATH = os.path.join(STAGING, "莎车县_network.db")
GEXF_PATH = os.path.join(STAGING, "莎车县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── County Government Leaders (confirmed from official site) ──
    {"id": 1, "name": "艾山·吾买尔", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "1974-06", "birthplace": "新疆吐鲁番", "education": "大学学历",
     "party_join": "中共党员", "work_start": "1997-12",
     "current_post": "莎车县委副书记、人民政府党组书记、县长", "current_org": "莎车县人民政府",
     "source": "https://www.shache.gov.cn/scx/c108008/202110/8febc897cbd84c4a8a00e68b623d3409.shtml"},
    {"id": 2, "name": "包文泉", "gender": "男", "ethnicity": "回族",
     "birth": "1983-12", "birthplace": "新疆乌鲁木齐", "education": "大学学历",
     "party_join": "中共党员", "work_start": "2006-09",
     "current_post": "莎车县委副书记、人民政府党组副书记、常务副县长", "current_org": "莎车县人民政府",
     "source": "https://www.shache.gov.cn/scx/c108008/202110/7c4826e5e8824c9a9434166f445ddeda.shtml"},
    {"id": 3, "name": "林晓明", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-07", "birthplace": "甘肃通渭", "education": "大学学历",
     "party_join": "中共党员", "work_start": "1999-11",
     "current_post": "莎车县人民政府党组成员、副县长、政法委副书记、公安局局长", "current_org": "莎车县人民政府",
     "source": "https://www.shache.gov.cn/scx/c108008/202110/8e4d1ebb39114fea9ff786b54197c1bb.shtml"},
    {"id": 4, "name": "吴磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "新疆巴楚", "education": "大学学历",
     "party_join": "中共党员", "work_start": "2003-09",
     "current_post": "莎车县人民政府副县长", "current_org": "莎车县人民政府",
     "source": "https://www.shache.gov.cn/scx/c108008/202403/1be25b735c004ba4bd92695ef539f323.shtml"},
    {"id": 5, "name": "高悦明", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-01", "birthplace": "甘肃华池", "education": "大学学历",
     "party_join": "中共党员", "work_start": "2010-03",
     "current_post": "莎车县人民政府党组成员、副县长", "current_org": "莎车县人民政府",
     "source": "https://www.shache.gov.cn/scx/c108008/202212/c75cb8f432b747ba83f8cddaeb98beae.shtml"},
    {"id": 6, "name": "慕九涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-12", "birthplace": "甘肃庆阳", "education": "大学学历",
     "party_join": "中共党员", "work_start": "1994-12",
     "current_post": "莎车县人民政府党组成员、副县长", "current_org": "莎车县人民政府",
     "source": "https://www.shache.gov.cn/scx/c108008/202110/62e98880de004814b7c2e22276ee676e.shtml"},
    # ── Party Committee Secretary (unconfirmed — placeholder) ──
    # 县委书记: UNKNOWN from web research (government site only lists government team)
    # This entry is a placeholder — actual name needs to be found from party committee page
    # or other sources. Marked as unverified.
]

organizations = [
    {"id": 1, "name": "中共莎车县委员会", "type": "党委", "level": "县处级",
     "parent": "中共喀什地区委员会", "location": "新疆喀什莎车"},
    {"id": 2, "name": "莎车县人民政府", "type": "政府", "level": "县处级",
     "parent": "喀什地区行政公署", "location": "新疆喀什莎车"},
    {"id": 3, "name": "莎车县公安局", "type": "政府", "level": "正科级",
     "parent": "莎车县人民政府", "location": "新疆喀什莎车"},
]

positions = [
    # 艾山·吾买尔 — current roles
    {"person_id": 1, "org_id": 1, "title": "莎车县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "莎车县人民政府党组书记、县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县人民政府全盘工作"},
    # 包文泉
    {"person_id": 2, "org_id": 1, "title": "莎车县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "莎车县人民政府党组副书记、常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责常务工作，分管发改、财政、审计等"},
    # 林晓明
    {"person_id": 3, "org_id": 2, "title": "莎车县人民政府党组成员、副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "主持公安局全面工作"},
    {"person_id": 3, "org_id": 3, "title": "莎车县公安局局长、党委书记、督察长",
     "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 吴磊
    {"person_id": 4, "org_id": 2, "title": "莎车县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管农业农村、水利、乡村振兴、交通运输等"},
    # 高悦明
    {"person_id": 5, "org_id": 2, "title": "莎车县人民政府党组成员、副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管卫生健康、医疗保障、工业经济等"},
    # 慕九涛
    {"person_id": 6, "org_id": 2, "title": "莎车县人民政府党组成员、副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管商贸流通、市场监督管理、招商引资等"},
]

relationships = [
    # 县长 艾山·吾买尔 与 常务副县长 包文泉 — same organization overlapping
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "县长—常务副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    # 县长 与 林晓明 — 上下级工作关系
    {"person_a": 1, "person_b": 3, "type": "共事",
     "context": "县长—副县长（公安）工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    # 县长 与 吴磊 — 上下级工作关系
    {"person_a": 1, "person_b": 4, "type": "共事",
     "context": "县长—副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    # 县长 与 高悦明 — 上下级工作关系
    {"person_a": 1, "person_b": 5, "type": "共事",
     "context": "县长—副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    # 县长 与 慕九涛 — 上下级工作关系
    {"person_a": 1, "person_b": 6, "type": "共事",
     "context": "县长—副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    # 常务副县长 包文泉 与 其他副县长 — same team
    {"person_a": 2, "person_b": 3, "type": "共事",
     "context": "常务副县长—副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "共事",
     "context": "常务副县长—副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "共事",
     "context": "常务副县长—副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 6, "type": "共事",
     "context": "常务副县长—副县长工作关系", "overlap_org": "莎车县人民政府", "overlap_period": "当前"},
]

# ── BUILD ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
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

    # Insert data
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
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
             pos["end_date"], pos["rank"], pos["note"])
        )
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"DB created: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>莎车县领导班子关系网络图</description>')
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
    lines.append('      <attribute id="8" title="level" type="string"/>')
    lines.append('      <attribute id="9" title="location" type="string"/>')
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
    for p in persons:
        # Determine color by role
        post = p["current_post"]
        if "县长" in post and "副" not in post.replace("副书记", ""):
            r, g, b = "30", "100", "200"  # Blue — government head
        elif "副书记" in post:
            r, g, b = "220", "80", "80"   # Light red — deputy secretary
        elif "副县长" in post or "副" in post:
            r, g, b = "100", "150", "220" # Light blue — deputy
        else:
            r, g, b = "180", "180", "180" # Grey

        size = "20.0" if "县长" in post and "副" not in post.replace("副书记", "") else "12.0"

        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for attr_id, key in [("0", "type"), ("1", "current_post"), ("2", "current_org"),
                             ("3", "gender"), ("4", "ethnicity"), ("5", "birth"),
                             ("6", "source")]:
            val = p.get(key, "")
            if val:
                lines.append(f'          <attvalue for="{attr_id}" value="{esc(val)}"/>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('        <viz:shape value="circle"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        # Organization colors by type
        ot = o.get("type", "")
        if "党委" in ot:
            org_r, org_g, org_b = "255", "200", "200"
        elif "政府" in ot:
            org_r, org_g, org_b = "200", "200", "255"
        else:
            org_r, org_g, org_b = "220", "220", "220"
        lines.append(f'        <viz:color r="{org_r}" g="{org_g}" b="{org_b}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Position edges (person → organization)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        if pos.get("note"):
            lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person ↔ person)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {len(persons)} person nodes, {len(organizations)} org nodes, {eid} edges")


if __name__ == "__main__":
    print("Building 莎车县 network data...")
    build_db()
    build_gexf()
    print("Done.")