#!/usr/bin/env python3
"""
Build 于都县 (Yudu County, 赣州市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

于都县 is a county under 赣州市, Jiangxi Province.
Current as of: 2026-07-15

Targets: 县委书记 & 县长
Core figures: 黄法 (县委书记), 李松柏 (县委副书记、县长)

Note: Based on yudu.gov.cn official website news as of 2026-07.
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(STAGING_DIR))  # repo root
DB_PATH = os.path.join(STAGING_DIR, "于都县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "于都县_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "黄法",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-08",
        "birthplace": "江西赣州",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委书记",
        "current_org": "中共于都县委员会",
        "source": "https://www.yudu.gov.cn; https://baike.baidu.com",
    },
    {
        "id": 2,
        "name": "李松柏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "江西宁都",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委副书记、县长",
        "current_org": "于都县人民政府",
        "source": "https://www.yudu.gov.cn; https://baike.baidu.com",
    },
    # ── Leadership team (current as of 2025-2026) ──────────────────────
    {
        "id": 3,
        "name": "郭书珑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委副书记",
        "current_org": "中共于都县委员会",
        "source": "yudu.gov.cn public reports",
    },
    {
        "id": 4,
        "name": "罗沪京",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委常委、纪委书记、监委主任",
        "current_org": "中共于都县纪律检查委员会",
        "source": "yudu.gov.cn public reports",
    },
    {
        "id": 5,
        "name": "李兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委常委、常务副县长",
        "current_org": "于都县人民政府",
        "source": "yudu.gov.cn public reports",
    },
    {
        "id": 6,
        "name": "王峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委常委、组织部部长",
        "current_org": "中共于都县委组织部",
        "source": "yudu.gov.cn public reports",
    },
    {
        "id": 7,
        "name": "刘晓阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委常委、宣传部部长",
        "current_org": "中共于都县委宣传部",
        "source": "yudu.gov.cn public reports",
    },
    {
        "id": 8,
        "name": "钟财亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委常委、政法委书记",
        "current_org": "中共于都县委政法委",
        "source": "yudu.gov.cn public reports",
    },
    {
        "id": 9,
        "name": "廖剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委常委、副县长",
        "current_org": "于都县人民政府",
        "source": "yudu.gov.cn public reports",
    },
    {
        "id": 10,
        "name": "谢志锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "于都县委常委、统战部部长",
        "current_org": "中共于都县委统战部",
        "source": "yudu.gov.cn public reports (2026-07-13 visit)",
    },
    # ── Predecessors ──────────────────────────────────────────────────
    {
        "id": 11,
        "name": "陈阳山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原于都县委书记，前任）",
        "current_org": "",
        "source": "public reports",
    },
    {
        "id": 12,
        "name": "钟旭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原于都县委书记，前任）",
        "current_org": "",
        "source": "public reports",
    },
]

organizations = [
    {"id": 1, "name": "中共于都县委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州于都"},
    {"id": 2, "name": "于都县人民政府", "type": "政府", "level": "县处级",
     "parent": "赣州市人民政府", "location": "江西赣州于都"},
    {"id": 3, "name": "中共于都县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共于都县委员会", "location": "江西赣州于都"},
    {"id": 4, "name": "中共于都县委组织部", "type": "党委部门", "level": "正科级",
     "parent": "中共于都县委员会", "location": "江西赣州于都"},
    {"id": 5, "name": "中共于都县委宣传部", "type": "党委部门", "level": "正科级",
     "parent": "中共于都县委员会", "location": "江西赣州于都"},
    {"id": 6, "name": "中共于都县委统战部", "type": "党委部门", "level": "正科级",
     "parent": "中共于都县委员会", "location": "江西赣州于都"},
    {"id": 7, "name": "中共于都县委政法委", "type": "党委部门", "level": "正科级",
     "parent": "中共于都县委员会", "location": "江西赣州于都"},
    {"id": 8, "name": "于都县人民代表大会", "type": "人大", "level": "县处级",
     "parent": "", "location": "江西赣州于都"},
    {"id": 9, "name": "于都县政治协商会议", "type": "政协", "level": "县处级",
     "parent": "", "location": "江西赣州于都"},
]

positions = [
    # ── 黄法 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "于都县委书记",
     "start": "2021-08", "end": "", "rank": "县处级正职",
     "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "于都县委副书记、县长",
     "start": "2019-03", "end": "2021-08", "rank": "县处级正职",
     "note": "由信丰县调任"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "于都县委副书记",
     "start": "2019-03", "end": "2019-03", "rank": "县处级副职",
     "note": "同时任代理县长"},

    # ── 李松柏 ──
    {"id": 4, "person_id": 2, "org_id": 2, "title": "于都县委副书记、县长",
     "start": "2021-09", "end": "", "rank": "县处级正职",
     "note": "现任"},
    {"id": 5, "person_id": 2, "org_id": 1, "title": "于都县委副书记",
     "start": "2021-08", "end": "2021-09", "rank": "县处级副职",
     "note": "提名为县长候选人"},
    {"id": 6, "person_id": 2, "org_id": 1, "title": "于都县委常委",
     "start": "2021-08", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 郭书珑 ──
    {"id": 7, "person_id": 3, "org_id": 1, "title": "于都县委副书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 罗沪京 ──
    {"id": 8, "person_id": 4, "org_id": 3, "title": "于都县委常委、纪委书记、监委主任",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 李兴 ──
    {"id": 9, "person_id": 5, "org_id": 2, "title": "于都县委常委、常务副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 王峰 ──
    {"id": 10, "person_id": 6, "org_id": 4, "title": "于都县委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 刘晓阳 ──
    {"id": 11, "person_id": 7, "org_id": 5, "title": "于都县委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 钟财亮 ──
    {"id": 12, "person_id": 8, "org_id": 7, "title": "于都县委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 廖剑 ──
    {"id": 13, "person_id": 9, "org_id": 2, "title": "于都县委常委、副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # ── 谢志锋 ──
    {"id": 14, "person_id": 10, "org_id": 6, "title": "于都县委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "2026-07 current"},
]

relationships = [
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "黄法（书记）与李松柏（县长）在于都县党政班子搭档工作（2021-至今）",
     "overlap_org": "中共于都县委员会/于都县人民政府",
     "overlap_period": "2021-至今"},
    {"id": 2, "person_a_id": 1, "person_b_id": 11,
     "type": "predecessor_successor",
     "context": "黄法接替陈阳山任于都县委书记",
     "overlap_org": "中共于都县委员会",
     "overlap_period": "2021"},
    {"id": 3, "person_a_id": 1, "person_b_id": 12,
     "type": "predecessor_successor",
     "context": "黄法接替钟旭辉任于都县委书记（前任的前任）",
     "overlap_org": "中共于都县委员会",
     "overlap_period": ""},
    {"id": 4, "person_a_id": 2, "person_b_id": 1,
     "type": "predecessor_successor",
     "context": "李松柏接替黄法任于都县长",
     "overlap_org": "于都县人民政府",
     "overlap_period": "2021"},
    {"id": 5, "person_a_id": 5, "person_b_id": 2,
     "type": "superior_subordinate",
     "context": "李兴（常务副县长）在李松柏（县长）领导下工作",
     "overlap_org": "于都县人民政府",
     "overlap_period": ""},
    {"id": 6, "person_a_id": 4, "person_b_id": 1,
     "type": "superior_subordinate",
     "context": "罗沪京（纪委书记）在黄法（书记）领导下工作",
     "overlap_org": "中共于都县委员会",
     "overlap_period": ""},
    {"id": 7, "person_a_id": 6, "person_b_id": 1,
     "type": "superior_subordinate",
     "context": "王峰（组织部长）在黄法（书记）领导下工作",
     "overlap_org": "中共于都县委员会",
     "overlap_period": ""},
    {"id": 8, "person_a_id": 7, "person_b_id": 1,
     "type": "superior_subordinate",
     "context": "刘晓阳（宣传部长）在黄法（书记）领导下工作",
     "overlap_org": "中共于都县委员会",
     "overlap_period": ""},
    {"id": 9, "person_a_id": 8, "person_b_id": 1,
     "type": "superior_subordinate",
     "context": "钟财亮（政法委书记）在黄法（书记）领导下工作",
     "overlap_org": "中共于都县委员会",
     "overlap_period": ""},
    {"id": 10, "person_a_id": 9, "person_b_id": 2,
     "type": "superior_subordinate",
     "context": "廖剑（副县长）在李松柏（县长）领导下工作",
     "overlap_org": "于都县人民政府",
     "overlap_period": ""},
    {"id": 11, "person_a_id": 10, "person_b_id": 1,
     "type": "superior_subordinate",
     "context": "谢志锋（统战部长）在黄法（书记）领导下工作",
     "overlap_org": "中共于都县委员会",
     "overlap_period": "2026"},
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
    red_ids = {1}       # 黄法 (县委书记)
    blue_ids = {2, 5, 9}  # 县长, 副县长
    orange_ids = {4}    # 纪委书记

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
    lines.append('    <description>于都县（赣州市）领导班子工作关系网络</description>')
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
    print("  于都县 (Yudu County) 领导班子工作关系网络")
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
