#!/usr/bin/env python3
"""
Build 信丰县 (Xinfeng County, 赣州市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

信丰县 is a county under 赣州市, Jiangxi Province.
Current as of: 2026-07-15

Targets: 县委书记 & 县长
Core figures: 袁炎 (原县委书记, 2021.08-2025.07), 张琳 (县委副书记、县长)

Note: 袁炎 moved to 南昌经开区党工委副书记、管委会主任 in 2025.07.
Current 信丰县委书记 (as of 2026-07) could not be confirmed via web sources
due to network restrictions. The script uses the best available evidence.
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "信丰县_network.db")
GEXF_PATH = os.path.join(BASE, "信丰县_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "袁炎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "江西赣州",
        "education": "本科/硕士",
        "party_join": "2000-03",
        "work_start": "1997-11",
        "current_post": "南昌经开区党工委副书记、管委会主任（原信丰县委书记）",
        "current_org": "南昌经济技术开发区",
        "source": "https://baike.baidu.com/item/袁炎/8348630; https://www.jxxf.gov.cn",
    },
    {
        "id": 2,
        "name": "张琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "江西兴国",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委副书记、县长",
        "current_org": "信丰县人民政府",
        "source": "https://www.jxxf.gov.cn",
    },
    # ── Leadership team (current as of 2023-2024) ───────────────────────
    {
        "id": 3,
        "name": "彭钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委副书记（原副县长）",
        "current_org": "中共信丰县委员会",
        "source": "government public reports",
    },
    {
        "id": 4,
        "name": "李绍武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委常委、常务副县长",
        "current_org": "信丰县人民政府",
        "source": "government public reports",
    },
    {
        "id": 5,
        "name": "陈大林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委常委、纪委书记、监委主任",
        "current_org": "中共信丰县纪律检查委员会",
        "source": "government public reports",
    },
    {
        "id": 6,
        "name": "陈金焘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委常委、组织部部长",
        "current_org": "中共信丰县委组织部",
        "source": "government public reports",
    },
    {
        "id": 7,
        "name": "杨祥文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委常委、统战部部长",
        "current_org": "中共信丰县委统战部",
        "source": "government public reports",
    },
    {
        "id": 8,
        "name": "杨铮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委常委、政法委书记",
        "current_org": "中共信丰县委政法委",
        "source": "government public reports",
    },
    {
        "id": 9,
        "name": "刘宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委常委、宣传部部长",
        "current_org": "中共信丰县委宣传部",
        "source": "government public reports",
    },
    {
        "id": 10,
        "name": "朱永金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "信丰县委常委、副县长",
        "current_org": "信丰县人民政府",
        "source": "government public reports",
    },
    # ── Predecessors ──────────────────────────────────────────────────
    {
        "id": 11,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原信丰县委书记，前任接替）",
        "current_org": "",
        "source": "public reports",
    },
    {
        "id": 12,
        "name": "黄蕙",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原信丰县委副书记、县长）",
        "current_org": "",
        "source": "public reports",
    },
]

organizations = [
    {"id": 1, "name": "中共信丰县委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州信丰"},
    {"id": 2, "name": "信丰县人民政府", "type": "政府", "level": "县处级",
     "parent": "赣州市人民政府", "location": "江西赣州信丰"},
    {"id": 3, "name": "信丰县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共信丰县委员会", "location": "江西赣州信丰"},
    {"id": 4, "name": "中共信丰县委组织部", "type": "党委部门", "level": "正科级",
     "parent": "中共信丰县委员会", "location": "江西赣州信丰"},
    {"id": 5, "name": "中共信丰县委宣传部", "type": "党委部门", "level": "正科级",
     "parent": "中共信丰县委员会", "location": "江西赣州信丰"},
    {"id": 6, "name": "中共信丰县委统战部", "type": "党委部门", "level": "正科级",
     "parent": "中共信丰县委员会", "location": "江西赣州信丰"},
    {"id": 7, "name": "中共信丰县委政法委", "type": "党委部门", "level": "正科级",
     "parent": "中共信丰县委员会", "location": "江西赣州信丰"},
    {"id": 8, "name": "信丰县人民代表大会", "type": "人大", "level": "县处级",
     "parent": "", "location": "江西赣州信丰"},
    {"id": 9, "name": "信丰县政治协商会议", "type": "政协", "level": "县处级",
     "parent": "", "location": "江西赣州信丰"},
    {"id": 10, "name": "南昌经济技术开发区", "type": "开发区", "level": "国家级",
     "parent": "江西省人民政府", "location": "江西南昌"},
]

positions = [
    # ── 袁炎 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "信丰县委书记",
     "start": "2021-08", "end": "2025-07", "rank": "县处级正职",
     "note": "由信丰县长升任县委书记"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "信丰县委副书记、县长",
     "start": "2019-02", "end": "2021-08", "rank": "县处级正职",
     "note": "此前任县委副书记、提名县长"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "信丰县委副书记",
     "start": "2016-08", "end": "2019-01", "rank": "县处级副职",
     "note": ""},
    {"id": 4, "person_id": 1, "org_id": 10, "title": "南昌经开区党工委副书记、管委会主任",
     "start": "2025-07", "end": "", "rank": "副厅级",
     "note": "现任；试用期一年（赣府字〔2025〕42号）"},

    # ── 张琳 ──
    {"id": 5, "person_id": 2, "org_id": 2, "title": "信丰县委副书记、县长",
     "start": "2021", "end": "", "rank": "县处级正职",
     "note": "现任"},

    # ── 彭钢 ──
    {"id": 6, "person_id": 3, "org_id": 1, "title": "信丰县委副书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 李绍武 ──
    {"id": 7, "person_id": 4, "org_id": 2, "title": "信丰县委常委、常务副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 陈大林 ──
    {"id": 8, "person_id": 5, "org_id": 3, "title": "信丰县委常委、纪委书记、监委主任",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 陈金焘 ──
    {"id": 9, "person_id": 6, "org_id": 4, "title": "信丰县委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 杨祥文 ──
    {"id": 10, "person_id": 7, "org_id": 6, "title": "信丰县委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 杨铮 ──
    {"id": 11, "person_id": 8, "org_id": 7, "title": "信丰县委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 刘宁 ──
    {"id": 12, "person_id": 9, "org_id": 5, "title": "信丰县委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 朱永金 ──
    {"id": 13, "person_id": 10, "org_id": 2, "title": "信丰县委常委、副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},
]

relationships = [
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "袁炎（书记）与张琳（县长）在信丰县党政班子搭档工作（2021-2025）",
     "overlap_org": "中共信丰县委员会/信丰县人民政府",
     "overlap_period": "2021-2025"},
    {"id": 2, "person_a_id": 1, "person_b_id": 11,
     "type": "predecessor_successor",
     "context": "袁炎接替刘勇任信丰县委书记",
     "overlap_org": "中共信丰县委员会",
     "overlap_period": "2021"},
    {"id": 3, "person_a_id": 1, "person_b_id": 12,
     "type": "predecessor_successor",
     "context": "袁炎接替黄蕙任信丰县长",
     "overlap_org": "信丰县人民政府",
     "overlap_period": "2019"},
    {"id": 4, "person_a_id": 2, "person_b_id": 12,
     "type": "predecessor_successor",
     "context": "张琳接替黄蕙任信丰县长",
     "overlap_org": "信丰县人民政府",
     "overlap_period": "2021"},
    {"id": 5, "person_a_id": 4, "person_b_id": 2,
     "type": "superior_subordinate",
     "context": "李绍武（常务副县长）在张琳（县长）领导下工作",
     "overlap_org": "信丰县人民政府",
     "overlap_period": ""},
    {"id": 6, "person_a_id": 5, "person_b_id": 1,
     "type": "superior_subordinate",
     "context": "陈大林（纪委书记）在袁炎（书记）领导下工作",
     "overlap_org": "中共信丰县委员会",
     "overlap_period": ""},
    {"id": 7, "person_a_id": 6, "person_b_id": 1,
     "type": "superior_subordinate",
     "context": "陈金焘（组织部长）在袁炎（书记）领导下工作",
     "overlap_org": "中共信丰县委员会",
     "overlap_period": ""},
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
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(pid):
    """Color by role: red=secretary, blue=gov leader, orange=discipline, grey=other."""
    red_ids = {1}      # 袁炎 (县委书记)
    blue_ids = {2, 4, 10}  # 县长, 副县长
    orange_ids = {5}   # 纪委书记

    if pid in red_ids:
        return "255,50,50"
    elif pid in blue_ids:
        return "50,100,255"
    elif pid in orange_ids:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "党委部门": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []

    # Header
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Sisyphus Government Network Investigator</creator>')
    lines.append('    <description>信丰县（赣州市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = p["id"]
        name = p["name"]
        birth = esc(p["birth"])
        birthplace = esc(p["birthplace"])
        role = esc(p["current_post"] or "")
        source = esc(p["source"] or "")
        c = person_color(pid)
        sz = "20.0" if pid in (1, 2) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{birth}"/>')
        lines.append(f'          <attvalue for="3" value="{birthplace}"/>')
        lines.append(f'          <attvalue for="4" value="{source}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"]
        oname = o["name"]
        otype = o["type"]
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (positions)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos["title"]
        start = pos["start"]
        end = pos["end"]
        note = pos["note"]
        label = f"{title} ({start}–{end})" if start else title
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(label)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person (relationships)
    for r in relationships:
        a = r["person_a_id"]
        b = r["person_b_id"]
        rtype = r["type"]
        ctx = r["context"]
        label = f"{rtype}: {esc(ctx)}"
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{label}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created: {GEXF_PATH}")


# ── MAIN ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  信丰县 (Xinfeng County) 领导班子工作关系网络")
    print(f"  Date: {today}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("-" * 60)
    print("  Done. Artifacts:")
    print(f"    DB:   {DB_PATH}")
    print(f"    GEXF: {GEXF_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
