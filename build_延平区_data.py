#!/usr/bin/env python3
"""
Build 延平区 (Yanping District, 南平市, Fujian) government personnel
relationship network — SQLite database + GEXF graph.

延平区 is the central urban district (市中心城区) of Nanping city, Fujian Province.
Current as of: 2026-07-16

Targets: 区委书记 & 区长
Core figures: 何明星 (区委书记), 叶文平 (区长)
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "延平区_network.db")
GEXF_PATH = os.path.join(BASE, "延平区_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "何明星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区委书记、区人武部党委第一书记",
        "current_org": "中共延平区委员会",
        "source": "Wikipedia: https://en.wikipedia.org/wiki/Yanping_District; 延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 2,
        "name": "叶文平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区委副书记、区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn 首页领导信息 (2026年7月)",
    },
    # ── Predecessors ────────────────────────────────────────────────────
    # Note: 何明星前任区委书记和叶文平前任区长的信息在公开来源中未找到确切记录
    # 延平区在2023年8月政府搬迁，人事变动可能与此相关
    # ── 副区长 (from 延平区人民政府官网) ────────────────────────────────
    {
        "id": 3,
        "name": "邵良辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区委常委、副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 4,
        "name": "柯桦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 5,
        "name": "陈文献",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 6,
        "name": "范云松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 7,
        "name": "陈婧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 8,
        "name": "王希石",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 9,
        "name": "杜宏沪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    {
        "id": 10,
        "name": "詹泉照",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区副区长",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
    # ── 党组成员 ─────────────────────────────────────────────────────────
    {
        "id": 11,
        "name": "钟秋生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延平区政府党组成员",
        "current_org": "延平区人民政府",
        "source": "延平区人民政府官网 http://www.ypzf.gov.cn (2026年7月)",
    },
]

organizations = [
    {"id": 1, "name": "中共延平区委员会", "type": "党委", "level": "县处级",
     "parent": "中共南平市委员会", "location": "福建南平延平"},
    {"id": 2, "name": "延平区人民政府", "type": "政府", "level": "县处级",
     "parent": "南平市人民政府", "location": "福建南平延平"},
    {"id": 3, "name": "南平市人民政府", "type": "政府", "level": "地厅级",
     "parent": "福建省人民政府", "location": "福建南平"},
    {"id": 4, "name": "中共南平市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共福建省委员会", "location": "福建南平"},
]

positions = [
    # 何明星
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "延平区委书记、区人武部党委第一书记", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任（Wikipedia确认，具体到任时间待查）"},
    # 叶文平
    {"id": 2, "person_id": 2, "org_id": 1,
     "title": "延平区委副书记", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2,
     "title": "延平区长", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任"},
    # 邵良辉
    {"id": 4, "person_id": 3, "org_id": 1,
     "title": "延平区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 5, "person_id": 3, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 柯桦
    {"id": 6, "person_id": 4, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 陈文献
    {"id": 7, "person_id": 5, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 范云松
    {"id": 8, "person_id": 6, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 陈婧
    {"id": 9, "person_id": 7, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 王希石
    {"id": 10, "person_id": 8, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 杜宏沪
    {"id": 11, "person_id": 9, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 詹泉照
    {"id": 12, "person_id": 10, "org_id": 2,
     "title": "延平区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 钟秋生
    {"id": 13, "person_id": 11, "org_id": 2,
     "title": "延平区政府党组成员", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
]

relationships = [
    # 党政搭档：何明星 × 叶文平
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "何明星（区委书记）与叶文平（区长）为延平区党政正职搭档",
     "overlap_org": "延平区", "overlap_period": "至今"},
    # 何明星与各副区长的上下级关系
    {"id": 2, "person_a_id": 1, "person_b_id": 3,
     "type": "上下级",
     "context": "何明星（区委书记）与邵良辉（常委、副区长）",
     "overlap_org": "中共延平区委员会", "overlap_period": "至今"},
    {"id": 3, "person_a_id": 1, "person_b_id": 4,
     "type": "上下级",
     "context": "何明星（区委书记）与柯桦（副区长）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    {"id": 4, "person_a_id": 1, "person_b_id": 5,
     "type": "上下级",
     "context": "何明星（区委书记）与陈文献（副区长）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    {"id": 5, "person_a_id": 1, "person_b_id": 6,
     "type": "上下级",
     "context": "何明星（区委书记）与范云松（副区长）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 7,
     "type": "上下级",
     "context": "何明星（区委书记）与陈婧（副区长）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 8,
     "type": "上下级",
     "context": "何明星（区委书记）与王希石（副区长）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 9,
     "type": "上下级",
     "context": "何明星（区委书记）与杜宏沪（副区长）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 10,
     "type": "上下级",
     "context": "何明星（区委书记）与詹泉照（副区长）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    {"id": 10, "person_a_id": 1, "person_b_id": 11,
     "type": "上下级",
     "context": "何明星（区委书记）与钟秋生（党组成员）",
     "overlap_org": "延平区", "overlap_period": "至今"},
    # 叶文平与各副区长的工作关系
    {"id": 11, "person_a_id": 2, "person_b_id": 3,
     "type": "上下级",
     "context": "叶文平（区长）与邵良辉（常委、副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 12, "person_a_id": 2, "person_b_id": 4,
     "type": "上下级",
     "context": "叶文平（区长）与柯桦（副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 13, "person_a_id": 2, "person_b_id": 5,
     "type": "上下级",
     "context": "叶文平（区长）与陈文献（副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 14, "person_a_id": 2, "person_b_id": 6,
     "type": "上下级",
     "context": "叶文平（区长）与范云松（副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 15, "person_a_id": 2, "person_b_id": 7,
     "type": "上下级",
     "context": "叶文平（区长）与陈婧（副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 16, "person_a_id": 2, "person_b_id": 8,
     "type": "上下级",
     "context": "叶文平（区长）与王希石（副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 17, "person_a_id": 2, "person_b_id": 9,
     "type": "上下级",
     "context": "叶文平（区长）与杜宏沪（副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 18, "person_a_id": 2, "person_b_id": 10,
     "type": "上下级",
     "context": "叶文平（区长）与詹泉照（副区长）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
    {"id": 19, "person_a_id": 2, "person_b_id": 11,
     "type": "上下级",
     "context": "叶文平（区长）与钟秋生（党组成员）",
     "overlap_org": "延平区人民政府", "overlap_period": "至今"},
]


# ── BUILD SQLite ─────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    print(f"✓ SQLite DB created: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")
    return counts


# ── BUILD GEXF ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role:
        return "255,50,50"  # Red for party secretary
    if "区长" in role or "市长" in role or "县长" in role:
        return "50,100,255"  # Blue for government head
    if "纪委书记" in role or "纪检" in role:
        return "255,165,0"  # Orange for discipline
    if "常委" in role:
        return "150,100,255"  # Purple for standing committee
    return "100,100,100"  # Grey


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
    return p["id"] <= 2


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>延平区领导班子工作关系网络 - 区委书记何明星 &amp; 区长叶文平</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "role"), ("2", "birth"), ("3", "birthplace"), ("4", "education")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "context"), ("2", "start"), ("3", "end")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("education", ""))}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Worked-at edges (person -> organization)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person <-> person)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph created: {GEXF_PATH}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {len(positions) + len(relationships)}")


# ── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"延平区 (Yanping District) 领导班子工作关系网络")
    print(f"Date: {today}")
    print(f"{'─' * 50}")
    build_db()
    build_gexf()
    print(f"{'─' * 50}")
    print(f"Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
