#!/usr/bin/env python3
"""
南部县 (Nanbu County, Nanchong City, Sichuan Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-26
信息来源:
  - 综合公开新闻报道及训练数据知识（截至2025年初）
  - 南部县人民政府网站 (nanbu.gov.cn) 及南充市人民政府网站均无法直接访问
  - Exa 免费 API 限流、百度百科 403

注意事项:
  - 由于公开网络访问严重受限，本脚本使用训练数据中截至2025年初的知识
  - 现任县委书记 "尹成平"（推测）和县长 "待确认" 的 2025-2026 年确切职务
    需在可联网环境下通过 nanbu.gov.cn 或南充市委组织部任前公示二次核实
  - 早期履历大量缺失，标记为"履历缺口"
  - 请在可访问中国网络的机器上重启调查以补全数据
"""

import sqlite3
import os
import sys
from datetime import datetime

TODAY = "2026-07-26"
SLUG = "南部县"
PROVINCE = "四川省"
PARENT_CITY = "南充市"

# Paths relative to staging dir
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "南部县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "南部县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 县委书记（推测）──
    {
        "id": 1,
        "name": "尹成平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共南部县委员会",
        "source": "暂缺（外网受限，基于训练数据知识推测）",
    },
    # ── 2. 县长（待确认）──
    {
        "id": 2,
        "name": "县长_待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长（待确认）",
        "current_org": "南部县人民政府",
        "source": "待核实",
    },
    # ── 3. 县委副书记（推定但姓名待确认）──
    {
        "id": 3,
        "name": "未确认_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（待确认）",
        "current_org": "中共南部县委员会",
        "source": "待补充",
    },
    # ── 4. 县人大常委会主任 ──
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
        "current_post": "县人大常委会主任（待确认）",
        "current_org": "南部县人大常委会",
        "source": "待补充",
    },
    # ── 5. 县政协主席 ──
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
        "current_post": "县政协主席（待确认）",
        "current_org": "政协南部县委员会",
        "source": "待补充",
    },
    # ── 6. 纪委书记/监委主任 ──
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
        "current_post": "县委常委、纪委书记、监委主任（待确认）",
        "current_org": "中共南部县纪律检查委员会/南部县监察委员会",
        "source": "待补充",
    },
    # ── 7. 常务副县长 ──
    {
        "id": 7,
        "name": "未确认_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长（待确认）",
        "current_org": "南部县人民政府",
        "source": "待补充",
    },
    # ── 8. 组织部部长 ──
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
        "current_post": "县委常委、组织部部长（待确认）",
        "current_org": "中共南部县委组织部",
        "source": "待补充",
    },
    # ── 9. 宣传部部长 ──
    {
        "id": 9,
        "name": "未确认_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长（待确认）",
        "current_org": "中共南部县委宣传部",
        "source": "待补充",
    },
    # ── 10. 政法委书记 ──
    {
        "id": 10,
        "name": "未确认_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记（待确认）",
        "current_org": "中共南部县委政法委",
        "source": "待补充",
    },
    # ── 11. 统战部部长 ──
    {
        "id": 11,
        "name": "未确认_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长（待确认）",
        "current_org": "中共南部县委统战部",
        "source": "待补充",
    },
    # ── 12. 前县委书记黄波（训练数据参考）──
    {
        "id": 12,
        "name": "黄波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原县委书记（前任，已离任）",
        "current_org": "中共南部县委员会",
        "source": "推测（网络受限，需通过 nanbu.gov.cn 核实）",
    },
    # ── 13. 更早前任县委书记张根生 ──
    {
        "id": 13,
        "name": "张根生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "更早原县委书记（已离任）",
        "current_org": "中共南部县委员会",
        "source": "推测（网络训练，需核实）",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共南部县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共南充市委员会",
        "location": "南充市南部县",
    },
    {
        "id": 2,
        "name": "南部县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "南充市人民政府",
        "location": "南充市南部县",
    },
    {
        "id": 3,
        "name": "南部县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "南充市南部县",
    },
    {
        "id": 4,
        "name": "政协南部县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "南充市南部县",
    },
    {
        "id": 5,
        "name": "南部县纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "",
        "location": "南充市南部县",
    },
    {
        "id": 6,
        "name": "中共南部县委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共南部县委员会",
        "location": "南充市南部县",
    },
    {
        "id": 7,
        "name": "中共南部县委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共南部县委员会",
        "location": "南充市南部县",
    },
    {
        "id": 8,
        "name": "中共南部县委政法委",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共南部县委员会",
        "location": "南充市南部县",
    },
    {
        "id": 9,
        "name": "中共南部县委统战部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共南部县委员会",
        "location": "南充市南部县",
    },
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "推测为尹成平（2022-2023年左右由县长转任），需联网核实"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待确认姓名"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 6, "org_id": 5, "title": "县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 7, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 8, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 9, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 10, "org_id": 8, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 11, "org_id": 9, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "", "note": "待确认姓名"},
    {"person_id": 12, "org_id": 1, "title": "原县委书记", "start_date": "", "end_date": "2022-2023", "rank": "正处级", "note": "前任县委书记黄波，已离任"},
    {"person_id": 13, "org_id": 1, "title": "更早原县委书记", "start_date": "", "end_date": "2019前后", "rank": "正处级", "note": "前任县委书记张根生"},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长的党政正职关系",
        "overlap_org": "南部县",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "predecessor_successor",
        "context": "黄波为尹成平的前任县委书记",
        "overlap_org": "中共南部县委",
        "overlap_period": "2023年前后换届",
    },
    {
        "person_a": 12,
        "person_b": 13,
        "type": "predecessor_successor",
        "context": "张根生为黄波的前任县委书记",
        "overlap_org": "中共南部县委",
        "overlap_period": "2019年前后换届",
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
    post = p.get("current_post", "")
    if "县委书记" in post or "书记" in post:
        return "255,50,50"
    if "县长" in post:
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
    return "县委书记" in post or "县长" in post


def build_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

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

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

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
    lines.append(f'    <description>{SLUG}领导班子工作关系网络 — {PROVINCE}{PARENT_CITY}{SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

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
    print(f"  南部县领导班子工作关系网络 — 数据构建")
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