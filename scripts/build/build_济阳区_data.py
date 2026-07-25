#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 济阳区 leadership network.

济阳区是山东省济南市下辖的一个市辖区，位于济南市北部。

Research notes:
- 王友进: Appears on jiyang.gov.cn inspecting key projects (as of 2026-07)
  Likely current 区委书记; research incomplete due to web access limitations
- 区长: Currently unidentified from available sources
- Previous 区委书记: 秦蕾 (served until ~2024)
- Web search tools (Exa, Baidu, Google) were rate-limited or blocked during research
- Data should be considered preliminary; see open_gaps.md for details
"""

import sqlite3
import os
import sys
from datetime import datetime

# Ensure we can import gov_relation
BASE = "/workspace/data/xieming/other-codes/gov-relation"

TMP_DIR = os.path.join(BASE, "data/tmp/shandong_济阳区")
DB_PATH = os.path.join(TMP_DIR, "济阳区_network.db")
GEXF_PATH = os.path.join(TMP_DIR, "济阳区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "王友进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市济阳区委书记",
        "current_org": "中共济南市济阳区委员会",
        "source": "https://www.jiyang.gov.cn/ (homepage: '王友进察看重点项目')",
    },
    {
        "id": 2,
        "name": "待查（区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济阳区人民政府区长",
        "current_org": "济阳区人民政府",
        "source": "未找到可靠来源 — 见 open_gaps.md",
    },
    # ── Previous Leaders ──
    {
        "id": 3,
        "name": "秦蕾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原）中共济南市济阳区委书记",
        "current_org": "（原）中共济南市济阳区委员会",
        "source": "公开报道 — 秦蕾曾任济阳区委书记至2024年前后",
    },
    {
        "id": 4,
        "name": "黄晓广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原）济阳区人民政府区长",
        "current_org": "（原）济阳区人民政府",
        "source": "公开报道 — 黄晓广曾任济阳区长",
    },
    # ── Standing Committee Members ──
    {
        "id": 5,
        "name": "待查（常务副区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济阳区委常委、常务副区长",
        "current_org": "济阳区人民政府",
        "source": "未找到可靠来源 — 见 open_gaps.md",
    },
    {
        "id": 6,
        "name": "待查（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济阳区委常委、组织部部长",
        "current_org": "中共济南市济阳区委员会",
        "source": "未找到可靠来源 — 见 open_gaps.md",
    },
    {
        "id": 7,
        "name": "待查（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济阳区委常委、纪委书记、监委主任",
        "current_org": "中共济南市济阳区纪律检查委员会",
        "source": "未找到可靠来源 — 见 open_gaps.md",
    },
    {
        "id": 8,
        "name": "待查（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济阳区委常委、宣传部部长",
        "current_org": "中共济南市济阳区委员会",
        "source": "未找到可靠来源 — 见 open_gaps.md",
    },
    {
        "id": 9,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济阳区委常委、政法委书记",
        "current_org": "中共济南市济阳区委员会",
        "source": "未找到可靠来源 — 见 open_gaps.md",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共济南市济阳区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共济南市委员会",
        "location": "济南市济阳区",
    },
    {
        "id": 2,
        "name": "济阳区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "济南市人民政府",
        "location": "济南市济阳区",
    },
    {
        "id": 3,
        "name": "中共济南市济阳区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共济南市纪律检查委员会",
        "location": "济南市济阳区",
    },
    {
        "id": 4,
        "name": "济阳区监察委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "济南市监察委员会",
        "location": "济南市济阳区",
    },
    {
        "id": 5,
        "name": "济南市济阳区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "济南市人大常委会",
        "location": "济南市济阳区",
    },
    {
        "id": 6,
        "name": "济南市济阳区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "济南市政协",
        "location": "济南市济阳区",
    },
]

positions = [
    # 王友进 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共济南市济阳区委书记",
     "start": "2024?", "end": "present", "rank": "副厅级",
     "note": "上任时间待确认；2026年7月仍在任"},
    # 待查 — 区长
    {"person_id": 2, "org_id": 2, "title": "济阳区人民政府区长",
     "start": "", "end": "present", "rank": "副厅级",
     "note": "姓名和上任时间均待确认"},
    # 秦蕾 — 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "中共济南市济阳区委书记",
     "start": "2022?", "end": "2024?", "rank": "副厅级",
     "note": "任期起止待确认"},
    # 黄晓广 — 前任区长
    {"person_id": 4, "org_id": 2, "title": "济阳区人民政府区长",
     "start": "", "end": "", "rank": "副厅级",
     "note": "任期待确认"},
    # 待查 — 常务副区长
    {"person_id": 5, "org_id": 2, "title": "济阳区委常委、常务副区长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "姓名待确认"},
    # 待查 — 组织部部长
    {"person_id": 6, "org_id": 1, "title": "济阳区委常委、组织部部长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "姓名待确认"},
    # 待查 — 纪委书记
    {"person_id": 7, "org_id": 3, "title": "济阳区委常委、纪委书记、监委主任",
     "start": "", "end": "present", "rank": "正处级",
     "note": "姓名待确认"},
    # 待查 — 宣传部部长
    {"person_id": 8, "org_id": 1, "title": "济阳区委常委、宣传部部长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "姓名待确认"},
    # 待查 — 政法委书记
    {"person_id": 9, "org_id": 1, "title": "济阳区委常委、政法委书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "姓名待确认"},
    # 秦蕾 also sits on the committee
    {"person_id": 3, "org_id": 1, "title": "中共济南市济阳区委书记（曾任）",
     "start": "2022?", "end": "2024?", "rank": "副厅级",
     "note": ""},
    # 黄晓广 also sits in government
    {"person_id": 4, "org_id": 2, "title": "济阳区人民政府区长（曾任）",
     "start": "", "end": "", "rank": "副厅级",
     "note": ""},
]

relationships = [
    # 王友进 ← 前任 → 秦蕾
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "王友进接替秦蕾担任济阳区委书记",
        "overlap_org": "中共济南市济阳区委员会",
        "overlap_period": "",
    },
    # 待查区长 ← 前任 → 黄晓广
    {
        "person_a": 2,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "现任区长接替黄晓广担任济阳区长",
        "overlap_org": "济阳区人民政府",
        "overlap_period": "",
    },
    # 王友进 ↔ 区长（党政搭档）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长为党政正职搭档",
        "overlap_org": "济阳区",
        "overlap_period": "",
    },
    # 秦蕾 ↔ 黄晓广（曾任党政搭档）
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "秦蕾任区委书记期间与黄晓广为党政搭档",
        "overlap_org": "济阳区",
        "overlap_period": "",
    },
]

# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def person_color(p):
    """Return GEXF color triple for a person node by role."""
    role = p.get("current_post", "")
    if "区委书记" in role:
        return "255,50,50"  # Red
    if "区长" in role:
        return "50,100,255"  # Blue
    if "纪委书记" in role or "监委" in role:
        return "255,165,0"  # Orange
    return "100,100,100"  # Grey


def org_color(o):
    """Return GEXF color triple for an organization node by type."""
    t = o.get("type", "")
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(t, "200,200,200")


def is_top_leader(p):
    p_id = p.get("id", 0)
    return p_id in (1, 2)  # 区委书记 or 区长


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        );

        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]),
        )

    for o in organizations:
        cur.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]),
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) "
            "VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]),
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) "
            "VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]),
        )

    conn.commit()
    conn.close()


def build_gexf():
    """Generate GEXF graph using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append("    <creator>OpenCode Research Agent</creator>")
    lines.append("    <description>济阳区领导班子工作关系网络</description>")
    lines.append("  </meta>")
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append("    <nodes>")
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append("        <attvalues>")
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("source",""))}"/>')
        lines.append("        </attvalues>")
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append("      </node>")

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append("        <attvalues>")
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append("        </attvalues>")
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append("      </node>")

    lines.append("    </nodes>")

    # Edges
    lines.append("    <edges>")
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        person_id = pos["person_id"]
        org_id = pos["org_id"]
        title = esc(pos["title"])
        lines.append(
            f'      <edge id="e{eid}" source="p{person_id}" target="o{org_id}" '
            f'label="{title}" weight="1.0">'
        )
        lines.append("        <attvalues>")
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{title}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append("        </attvalues>")
        lines.append("      </edge>")

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        rtype = esc(r["type"])
        context = esc(r["context"])
        overlap_org = esc(r.get("overlap_org", ""))
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
            f'label="{rtype}" weight="2.0">'
        )
        lines.append("        <attvalues>")
        lines.append(f'          <attvalue for="0" value="{rtype}"/>')
        lines.append(f'          <attvalue for="1" value="{context}"/>')
        lines.append(f'          <attvalue for="2" value="{overlap_org}"/>')
        lines.append("        </attvalues>")
        lines.append("      </edge>")

    lines.append("    </edges>")
    lines.append("  </graph>")
    lines.append("</gexf>")

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def print_summary():
    print(f"✅ Database: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")
    print(f"✅ GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_db()
    build_gexf()
    print_summary()
    print("\n⚠️  NOTE: Extensive web search tools were unavailable during research.")
    print("   Several leadership positions are marked '待查' (to be looked up).")
    print("   This is a preliminary data build with open gaps. See open_gaps.md.")
