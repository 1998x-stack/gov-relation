#!/usr/bin/env python3
"""
Build 南康区 (Nankang District, 赣州市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

南康区 is a district under 赣州市, Jiangxi Province.
Current as of: 2026-07-15

Targets: 区委书记 & 区长
Core figures: 何善锦 (区委书记), 梅旭军 (区委副书记、区长)
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "南康区_network.db")
GEXF_PATH = os.path.join(BASE, "南康区_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "何善锦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-09",
        "birthplace": "江西信丰",
        "education": "省委党校研究生",
        "party_join": "1991-10",
        "work_start": "1989-08",
        "current_post": "赣州市委常委、南康区委书记",
        "current_org": "中共南康区委员会",
        "source": "南康区人民政府官网 https://www.nkjx.gov.cn",
    },
    {
        "id": 2,
        "name": "梅旭军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南康区委副书记、区长",
        "current_org": "南康区人民政府",
        "source": "南康区人民政府官网新闻（2026年多次报道梅旭军主持区政府全面工作）",
    },
    {
        "id": 3,
        "name": "李赣兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "江西赣县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原南康区委副书记、区长→调离）",
        "current_org": "南康区人民政府",
        "source": "南康区人民政府官网 https://www.nkjx.gov.cn",
    },
    # ── Key deputies: 常务副区长 ───────────────────────────────────────
    {
        "id": 4,
        "name": "李成胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南康区委常委、常务副区长",
        "current_org": "南康区人民政府",
        "source": "公开报道/南康区政府官网",
    },
    # ── 纪委书记 ────────────────────────────────────────────────────────
    {
        "id": 5,
        "name": "陈培生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南康区委常委、纪委书记、监委主任",
        "current_org": "中共南康区纪律检查委员会",
        "source": "公开报道",
    },
    # ── 政法委书记 ──────────────────────────────────────────────────────
    {
        "id": 6,
        "name": "王俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南康区委常委、政法委书记",
        "current_org": "中共南康区委员会政法委员会",
        "source": "公开报道",
    },
    # ── 组织部部长 ──────────────────────────────────────────────────────
    {
        "id": 7,
        "name": "刘日辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南康区委常委、组织部部长",
        "current_org": "中共南康区委员会组织部",
        "source": "公开报道",
    },
    # ── 宣传部部长 ──────────────────────────────────────────────────────
    {
        "id": 8,
        "name": "刘婷婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南康区委常委、宣传部部长",
        "current_org": "中共南康区委员会宣传部",
        "source": "公开报道",
    },
    # ── Predecessors ────────────────────────────────────────────────────
    {
        "id": 9,
        "name": "徐兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-11",
        "birthplace": "江西赣州",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原南康区委书记→赣州市政协主席）",
        "current_org": "赣州市政协",
        "source": "公开报道/维基百科",
    },
]

organizations = [
    {"id": 1, "name": "中共南康区委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州南康"},
    {"id": 2, "name": "南康区人民政府", "type": "政府", "level": "县处级",
     "parent": "赣州市人民政府", "location": "江西赣州南康"},
    {"id": 3, "name": "中共南康区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市纪律检查委员会", "location": "江西赣州南康"},
    {"id": 4, "name": "中共南康区委员会政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共南康区委员会", "location": "江西赣州南康"},
    {"id": 5, "name": "中共南康区委员会组织部", "type": "党委", "level": "县处级",
     "parent": "中共南康区委员会", "location": "江西赣州南康"},
    {"id": 6, "name": "中共南康区委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共南康区委员会", "location": "江西赣州南康"},
    {"id": 7, "name": "赣州市政协", "type": "政协", "level": "地厅级",
     "parent": "江西省政协", "location": "江西赣州"},
    {"id": 8, "name": "赣州市人民政府", "type": "政府", "level": "地厅级",
     "parent": "江西省人民政府", "location": "江西赣州"},
]

positions = [
    # 何善锦
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "南康区委书记（赣州市委常委兼任）", "start": "2021", "end": "",
     "rank": "副厅级", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 8,
     "title": "赣州市委常委", "start": "2021", "end": "",
     "rank": "副厅级", "note": "现任，兼任南康区委书记"},
    # 梅旭军
    {"id": 3, "person_id": 2, "org_id": 2,
     "title": "南康区委副书记、区长", "start": "2025?", "end": "",
     "rank": "县处级正职", "note": "现任（接替李赣兴，具体到任时间待确认）"},
    # 李赣兴 (前任区长)
    {"id": 4, "person_id": 3, "org_id": 2,
     "title": "南康区委副书记、区长", "start": "2021", "end": "2025?",
     "rank": "县处级正职", "note": "前任，已调离"},
    # 李成胜
    {"id": 5, "person_id": 4, "org_id": 2,
     "title": "南康区委常委、常务副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 陈培生
    {"id": 6, "person_id": 5, "org_id": 3,
     "title": "南康区委常委、纪委书记、监委主任", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 王俊
    {"id": 7, "person_id": 6, "org_id": 4,
     "title": "南康区委常委、政法委书记", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 刘日辉
    {"id": 8, "person_id": 7, "org_id": 5,
     "title": "南康区委常委、组织部部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 刘婷婷
    {"id": 9, "person_id": 8, "org_id": 6,
     "title": "南康区委常委、宣传部部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 徐兵 (前任书记)
    {"id": 10, "person_id": 9, "org_id": 1,
     "title": "南康区委书记", "start": "2016", "end": "2021",
     "rank": "县处级正职", "note": "前任→升赣州市政协主席"},
    {"id": 11, "person_id": 9, "org_id": 7,
     "title": "赣州市政协主席", "start": "2021", "end": "",
     "rank": "正厅级", "note": "现任"},
]

relationships = [
    # 党政搭档：何善锦 × 梅旭军
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "何善锦（区委书记）与梅旭军（区长）为南康区党政正职搭档",
     "overlap_org": "南康区", "overlap_period": "2025?至今"},
    # 何善锦 × 李赣兴（前任搭档）
    {"id": 2, "person_a_id": 1, "person_b_id": 3,
     "type": "党政搭档",
     "context": "何善锦与李赣兴在南康区党政搭档（2021-2025?）",
     "overlap_org": "南康区", "overlap_period": "2021-2025?"},
    # 何善锦 ← 徐兵（继任关系）
    {"id": 3, "person_a_id": 9, "person_b_id": 1,
     "type": "前后任",
     "context": "徐兵（2016-2021南康区委书记）→ 何善锦（2021至今）",
     "overlap_org": "中共南康区委员会", "overlap_period": "2016-2021交接"},
    # 李赣兴 → 梅旭军（前后任）
    {"id": 4, "person_a_id": 3, "person_b_id": 2,
     "type": "前后任",
     "context": "李赣兴（前任区长）→ 梅旭军（现任区长）",
     "overlap_org": "南康区人民政府", "overlap_period": "2025?交接"},
    # 常委班子成员关系：何善锦与各常委
    {"id": 5, "person_a_id": 1, "person_b_id": 4,
     "type": "上下级",
     "context": "何善锦（区委书记）与李成胜（常委、常务副区长）",
     "overlap_org": "中共南康区委员会", "overlap_period": "至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 5,
     "type": "上下级",
     "context": "何善锦（区委书记）与陈培生（常委、纪委书记）",
     "overlap_org": "中共南康区委员会", "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 6,
     "type": "上下级",
     "context": "何善锦（区委书记）与王俊（常委、政法委书记）",
     "overlap_org": "中共南康区委员会", "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 7,
     "type": "上下级",
     "context": "何善锦（区委书记）与刘日辉（常委、组织部部长）",
     "overlap_org": "中共南康区委员会", "overlap_period": "至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 8,
     "type": "上下级",
     "context": "何善锦（区委书记）与刘婷婷（常委、宣传部部长）",
     "overlap_org": "中共南康区委员会", "overlap_period": "至今"},
    # 区长与副区长
    {"id": 10, "person_a_id": 2, "person_b_id": 4,
     "type": "上下级",
     "context": "梅旭军（区长）与李成胜（常务副区长）",
     "overlap_org": "南康区人民政府", "overlap_period": "至今"},
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
    return "100,100,100"  # Grey


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
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
    lines.append('    <description>南康区领导班子工作关系网络 - 区委书记何善锦 &amp; 区长梅旭军</description>')
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
    print(f"南康区 (Nankang District) 领导班子工作关系网络")
    print(f"Date: {today}")
    print(f"{'─' * 50}")
    build_db()
    build_gexf()
    print(f"{'─' * 50}")
    print(f"Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
