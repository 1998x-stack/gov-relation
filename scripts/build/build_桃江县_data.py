#!/usr/bin/env python3
"""
桃江县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for 桃江县 leadership network.
Investigation date: 2026-07-24

Current leadership (as of 2026-05):
   县委书记: 向荣 (born 1970-09, 湖南沅江人)
   县长: 周登高 (born 1982-09, 湖南宁乡人)
"""

import sqlite3
import os
import sys

# ── Paths (relative to repo root) ──
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "data", "database", "桃江县_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "桃江县_network.gexf")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

PERSONS = [
    # ── 1. 县委书记 ──
    {
        "id": 1,
        "name": "向荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "湖南省沅江市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共桃江县委书记",
        "current_org": "中共桃江县委员会",
        "source": "维基百科 https://zh.wikipedia.org/wiki/%E6%A1%83%E6%B1%9F%E5%8E%BF · 益阳市领导班子报告 2026-07-14",
    },
    # ── 2. 县长 ──
    {
        "id": 2,
        "name": "周登高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "湖南省宁乡市",
        "education": "湘潭大学行政管理专业硕士",
        "party_join": "中共党员",
        "work_start": "2000",
        "current_post": "桃江县人民政府县长",
        "current_org": "桃江县人民政府",
        "source": "维基百科 https://zh.wikipedia.org/wiki/%E5%91%A8%E7%99%BB%E9%AB%98 · 益阳市领导班子报告 2026-07-14",
    },
    # ── 3. 冷亮（前任副书记→现澧县县委书记）──
    {
        "id": 3,
        "name": "冷亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982",
        "birthplace": "湖南省益阳市赫山区",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共澧县县委书记",
        "current_org": "中共澧县委员会",
        "source": "益阳市领导班子报告 2026-07-14 · 常德市领导班子报告 2026-07-14",
    },
    # ── 4. 前县委书记（向荣前任）──
    # Note: Before 向荣, 桃江县委书记 was 汤跃武 (2016-2021). We don't have a confirmed current
    # replacement trajectory for him. Let's include as predecessor.
    {
        "id": 4,
        "name": "汤跃武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前桃江县委书记",
        "current_org": "中共桃江县委员会（前）",
        "source": "维基百科 https://zh.wikipedia.org/wiki/%E6%A1%83%E6%B1%9F%E5%8E%BF",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共桃江县委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市桃江县"},
    {"id": 2, "name": "桃江县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市桃江县"},
    {"id": 3, "name": "桃江县经济合作局", "type": "政府", "level": "乡科级", "parent": "桃江县人民政府", "location": "湖南省益阳市桃江县"},
    {"id": 4, "name": "中共安化县委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市安化县"},
    {"id": 5, "name": "安化县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市安化县"},
    {"id": 6, "name": "中共益阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省益阳市"},
    {"id": 7, "name": "益阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省益阳市"},
    {"id": 8, "name": "中共赫山区委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市赫山区"},
    {"id": 9, "name": "赫山区人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市赫山区"},
    {"id": 10, "name": "赫山区委办公室", "type": "党委", "level": "乡科级", "parent": "中共赫山区委员会", "location": "湖南省益阳市赫山区"},
    {"id": 11, "name": "益阳市龙岭工业园管委会", "type": "开发区", "level": "乡科级", "parent": "赫山区人民政府", "location": "湖南省益阳市赫山区"},
    {"id": 12, "name": "沧水铺镇循环经济工业园管委会", "type": "开发区", "level": "乡镇级", "parent": "赫山区人民政府", "location": "湖南省益阳市赫山区沧水铺镇"},
    {"id": 13, "name": "益阳市委办公室", "type": "党委", "level": "地市级", "parent": "中共益阳市委", "location": "湖南省益阳市"},
    {"id": 14, "name": "道林镇中心学校", "type": "事业单位", "level": "乡镇级", "parent": "宁乡市教育局", "location": "湖南省宁乡市道林镇"},
    {"id": 15, "name": "湘潭大学", "type": "事业单位", "level": "厅局级", "parent": "湖南省教育厅", "location": "湖南省湘潭市"},
    {"id": 16, "name": "中共澧县委员会", "type": "党委", "level": "县处级", "parent": "中共常德市委", "location": "湖南省常德市澧县"},
]

POSITIONS = [
    # ── 向荣 ──
    {"person_id": 1, "org_id": 1, "title": "中共桃江县委书记", "start": "2021-07", "end": "", "rank": "正处级", "note": "现任"},
    # 向荣早期履历未知

    # ── 周登高 ──
    {"person_id": 2, "org_id": 14, "title": "道林镇中心学校教师", "start": "2000", "end": "2005", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "湘潭大学行政管理专业硕士研究生", "start": "2005", "end": "2008", "rank": "", "note": "全日制学习"},
    {"person_id": 2, "org_id": 11, "title": "益阳市龙岭工业园管委会党政综合办公室主任", "start": "2008", "end": "2009", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "沧水铺镇循环经济工业园管委会办公室主任", "start": "2009", "end": "2010-03", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "赫山区委办公室调研室主任", "start": "2010-03", "end": "2010-10", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 3, "title": "桃江县经济合作局党组副书记、局长", "start": "2010-10", "end": "2012-09", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "安化县人民政府副县长", "start": "2012-11", "end": "2016-08", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "益阳市委办公室副主任", "start": "2016-08", "end": "2017-05", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "益阳市委副秘书长", "start": "2017-05", "end": "2020-04", "rank": "正处级", "note": "2017.05明确为正处级"},
    {"person_id": 2, "org_id": 4, "title": "中共安化县委副书记", "start": "2020-04", "end": "2021-07", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "桃江县人民政府县长", "start": "2021-07", "end": "", "rank": "正处级", "note": "现任"},

    # ── 冷亮 ──
    {"person_id": 3, "org_id": 8, "title": "赫山区委办公室干部/副主任", "start": "", "end": "", "rank": "", "note": "早期在赫山区委办工作"},
    {"person_id": 3, "org_id": 1, "title": "桃江县委副书记", "start": "", "end": "2024", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 16, "title": "澧县县长→县委书记", "start": "2024", "end": "", "rank": "正处级", "note": "现任，冷亮从桃江副书记直接调任澧县"},

    # ── 汤跃武（前县委书记）──
    {"person_id": 4, "org_id": 1, "title": "中共桃江县委书记", "start": "2016", "end": "2021-07", "rank": "正处级", "note": "向荣的前任"},
]

RELATIONSHIPS = [
    # 向荣 ↔ 周登高：党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "向荣(书记)+周登高(县长)为桃江县党政正职搭档，自2021年7月起共事", "overlap_org": "桃江县", "overlap_period": "2021-至今"},

    # 向荣 → 汤跃武：前后任县委书记
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "汤跃武2016-2021任桃江县委书记，向荣2021年7月接任", "overlap_org": "中共桃江县委员会", "overlap_period": "2021-07"},

    # 周登高 ↔ 安化县：曾在安化任职副县长+副书记
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "周登高2012-2016任安化副县长，2020-2021任安化县委副书记，在安化累计任职约5年", "overlap_org": "安化县", "overlap_period": "2012-2016, 2020-2021"},

    # 冷亮 ↔ 向荣：在桃江期间上下级
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "冷亮任桃江县委副书记期间，向荣为县委书记", "overlap_org": "中共桃江县委员会", "overlap_period": "2021-2024"},

    # 冷亮 ↔ 周登高：桃江县班子成员
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "冷亮(副书记)与周登高(县长)在桃江县党政班子共事", "overlap_org": "桃江县", "overlap_period": "2021-2024"},

    # 冷亮 → 赫山区：早期在赫山区委办工作
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "冷亮早期在赫山区委办公室工作，后调桃江、澧县", "overlap_org": "赫山区", "overlap_period": ""},

    # 周登高 ↔ 赫山区：曾在赫山区委办工作
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "周登高2010年曾任赫山区委办公室调研室主任", "overlap_org": "赫山区", "overlap_period": "2010-03—2010-10"},
]

# ═══════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    for t in ["relationships", "positions", "organizations", "persons"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")

    conn.execute("""
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
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    conn.execute("""
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
    conn.execute("""
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

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in PERSONS:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in ORGANIZATIONS:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in POSITIONS:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in RELATIONSHIPS:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════
# GEXF BUILD
# ═══════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(title):
    t = title
    if "书记" in t and "副" not in t:
        return "200,30,30"
    if "县长" in t and "副" not in t:
        return "30,100,200"
    if "副书记" in t:
        return "220,80,80"
    if "副" in t:
        return "100,150,220"
    if "前" in t:
        return "160,160,160"
    return "180,180,180"

def is_top_leader(name):
    return name in ["向荣", "周登高"]

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

def generate_gexf():
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>桃江县领导班子工作关系网络 — 含党政正职、副书记、前后任及关联组织</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p["current_post"])
        sz = "60.0" if is_top_leader(p["name"]) else "35.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        cr, cg, cb = c.split(",")
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        c = org_color(o["type"])
        cr, cg, cb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append('        <viz:size value="20.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    added_edges = set()
    for pos in POSITIONS:
        pid = pos["person_id"]
        oid = pos["org_id"]
        eid += 1
        edge_key = f"p{pid}-o{oid}-{pos['title']}"
        if edge_key in added_edges:
            continue
        added_edges.add(edge_key)
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  桃江县领导班子工作关系网络 — 数据构建")
    print("  调查日期: 2026-07-24")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("Done.")
