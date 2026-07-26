#!/usr/bin/env python3
"""
顺庆区 (Shunqing District, Nanchong City, Sichuan Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-26
信息来源:
  - 顺庆区人民政府网站 (shunqing.gov.cn)
  - 新闻报道

注意事项:
  - 因公开网络访问受限（Exa免费API限流、百度百科403、Jina超时），
    蒲鹏程和唐粼波的早期履历信息尚未获取到。
    当前数据包含已确认的在任信息，早期履历标记为"履历缺口"。
"""

import sqlite3
import os
import sys
from datetime import datetime

TODAY = "2026-07-26"
SLUG = "顺庆区"
PROVINCE = "四川省"
PARENT_CITY = "南充市"

# Paths relative to staging dir
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "顺庆区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "顺庆区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 区委书记 ──
    {
        "id": 1,
        "name": "蒲鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共南充市顺庆区委员会",
        "source": "https://www.shunqing.gov.cn/xwdt/",
    },
    # ── 2. 区长 ──
    {
        "id": 2,
        "name": "唐粼波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "顺庆区人民政府",
        "source": "https://www.shunqing.gov.cn/xwdt/",
    },
    # ── 3. 区委副书记(推测) ──
    {
        "id": 3,
        "name": "未确认_区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记（待确认）",
        "current_org": "中共南充市顺庆区委员会",
        "source": "待补充",
    },
    # ── 4. 区人大常委会主任(推测) ──
    {
        "id": 4,
        "name": "未确认_人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任（待确认）",
        "current_org": "顺庆区人大常委会",
        "source": "待补充",
    },
    # ── 5. 区政协主席(推测) ──
    {
        "id": 5,
        "name": "未确认_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席（待确认）",
        "current_org": "政协顺庆区委员会",
        "source": "待补充",
    },
    # ── 6. 区委常委、纪委书记/监委主任(推测) ──
    {
        "id": 6,
        "name": "未确认_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区纪委书记/监委主任（待确认）",
        "current_org": "中共南充市顺庆区纪律检查委员会/区监察委员会",
        "source": "待补充",
    },
    # ── 7. 区委常委、常务副区长(推测) ──
    {
        "id": 7,
        "name": "未确认_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长（待确认）",
        "current_org": "顺庆区人民政府",
        "source": "待补充",
    },
    # ── 8. 区委常委、组织部部长(推测) ──
    {
        "id": 8,
        "name": "未确认_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长（待确认）",
        "current_org": "中共南充市顺庆区委员会组织部",
        "source": "待补充",
    },
    # ── 9. 区委常委、纪委书记(已含在id=6) ──
    # ── 10. 区委常委、宣传部部长(推测) ──
    {
        "id": 10,
        "name": "未确认_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长（待确认）",
        "current_org": "中共南充市顺庆区委员会宣传部",
        "source": "待补充",
    },
    # ── 11. 区委常委、政法委书记(推测) ──
    {
        "id": 11,
        "name": "未确认_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记（待确认）",
        "current_org": "中共南充市顺庆区委员会政法委员会",
        "source": "待补充",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共南充市顺庆区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共南充市委员会",
        "location": "南充市顺庆区",
    },
    {
        "id": 2,
        "name": "顺庆区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "南充市人民政府",
        "location": "南充市顺庆区",
    },
    {
        "id": 3,
        "name": "顺庆区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "南充市顺庆区",
    },
    {
        "id": 4,
        "name": "顺庆区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "南充市顺庆区",
    },
    {
        "id": 5,
        "name": "顺庆区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "",
        "location": "南充市顺庆区",
    },
    {
        "id": 6,
        "name": "中共南充市顺庆区委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共南充市顺庆区委员会",
        "location": "南充市顺庆区",
    },
    {
        "id": 7,
        "name": "中共南充市顺庆区委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共南充市顺庆区委员会",
        "location": "南充市顺庆区",
    },
    {
        "id": 8,
        "name": "中共南充市顺庆区委政法委",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共南充市顺庆区委员会",
        "location": "南充市顺庆区",
    },
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 5, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 6, "org_id": 5, "title": "区纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 7, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 8, "org_id": 6, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 10, "org_id": 7, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 11, "org_id": 8, "title": "区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长是顺庆区的党政正职关系",
        "overlap_org": "顺庆区",
        "overlap_period": "至今",
    },
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "区委书记" in post or "县委书记" in post:
        return "255,50,50"
    if "区长" in post or "县长" in post or "市长" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    post = p.get("current_post", "")
    return "区委书记" in post or "区长" in post


def build_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
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
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # Insert positions
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>顺庆区领导班子工作关系网络 — {PROVINCE}{PARENT_CITY}{SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
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
        pid = p["id"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"]
        c = org_color(o)
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: person→organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: person↔person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_edges = len(positions) + len(relationships)
    print(f"  GEXF: {GEXF_PATH}")
    print(f"    Nodes: {len(persons)} persons + {len(organizations)} organizations")
    print(f"    Edges: {total_edges}")


def main():
    print("=" * 60)
    print(f"  顺庆区领导班子工作关系网络 — 数据构建")
    print(f"  调查日期：{TODAY}")
    print("=" * 60)
    print()

    print("[1/2] Building database...")
    build_database()

    print()
    print("[2/2] Building GEXF graph...")
    build_gexf()

    print()
    print("Done.")
    print(f"  DB:    {os.path.getsize(DB_PATH)} bytes" if os.path.exists(DB_PATH) else "  DB: MISSING!")
    print(f"  GEXF:  {os.path.getsize(GEXF_PATH)} bytes" if os.path.exists(GEXF_PATH) else "  GEXF: MISSING!")


if __name__ == "__main__":
    main()