#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 连江县 (Lianjiang County) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_连江县")
DB_PATH = os.path.join(STAGING, "连江县_network.db")
GEXF_PATH = os.path.join(STAGING, "连江县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (from July 2026) ──
    {"id": 1, "name": "郭勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "福建福清", "education": "省委党校研究生, 公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共连江县委书记", "current_org": "中共连江县委员会",
     "source": "https://baike.baidu.com/item/%E9%83%AD%E5%8B%87/ 及连江县融媒体中心报道"},
    # ── Current Acting County Mayor (from July 2026) ──
    {"id": 2, "name": "薛博", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-08", "birthplace": "陕西子长", "education": "研究生学历, 理学博士",
     "party_join": "中共党员", "work_start": "2008-09",
     "current_post": "连江县委副书记、代县长", "current_org": "连江县人民政府",
     "source": "https://baike.baidu.com/item/%E8%96%9B%E5%8D%9A/ 及连江县融媒体中心报道"},
    # ── Previous Party Secretary (Dec 2024 - Jul 2026) ──
    {"id": 3, "name": "高双成", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "福建福清", "education": "省委党校在职研究生",
     "party_join": "中共党员", "work_start": "1993-09",
     "current_post": "（原连江县委书记）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E9%AB%98%E5%8F%8C%E6%88%90/"},
    # ── Previous Original Party Secretary (before Dec 2024) ──
    {"id": 4, "name": "陈劲松", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原连江县委书记，2024年12月离任）", "current_org": "",
     "source": "https://www.sohu.com/ 福建多位县级党政主官履新报道 2024-12-30"},
    # ── Former Deputy Party Secretary (transferred Jul 2026) ──
    {"id": 5, "name": "林吓清", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-07", "birthplace": "福建平潭", "education": "在职研究生, 公共管理硕士",
     "party_join": "中共党员", "work_start": "2005-07",
     "current_post": "永泰县委副书记、代县长", "current_org": "永泰县人民政府",
     "source": "https://baike.baidu.com/item/%E6%9E%97%E5%90%93%E6%B8%85/"},
    # ── Standing Committee Members (as of Nov 2025) ──
    {"id": 6, "name": "郑东平", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "连江县委常委、宣传部部长", "current_org": "中共连江县委员会",
     "source": "https://www.baidu.com/link? 连江县委领导班子页面"},
    {"id": 7, "name": "余良发", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-12", "birthplace": "福建福清", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992-09",
     "current_post": "连江县委常委、县纪委书记、县监委主任", "current_org": "中共连江县纪律检查委员会",
     "source": "https://baike.baidu.com/item/%E4%BD%99%E8%89%AF%E5%8F%91/"},
    {"id": 8, "name": "雷发勇", "gender": "男", "ethnicity": "畲族",
     "birth": "1968-10", "birthplace": "福建连江筱埕", "education": "在职大学",
     "party_join": "中共党员", "work_start": "1989-08",
     "current_post": "连江县委常委、政法委书记", "current_org": "中共连江县委员会",
     "source": "https://baike.baidu.com/item/%E9%9B%B7%E5%8F%91%E5%8B%87/"},
    {"id": 9, "name": "颜学淦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "连江县委常委、统战部部长", "current_org": "中共连江县委员会",
     "source": "https://www.baidu.com/link? 连江县委领导班子页面"},
    {"id": 10, "name": "张记欢", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "连江县委常委、副县长", "current_org": "连江县人民政府",
     "source": "https://www.baidu.com/link? 连江县委领导班子页面"},
    {"id": 11, "name": "陈钧", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "连江县委常委、组织部部长", "current_org": "中共连江县委员会",
     "source": "https://www.baidu.com/link? 连江县委领导班子页面"},
    {"id": 12, "name": "刘麟翔", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-12", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "连江县委常委、副县长", "current_org": "连江县人民政府",
     "source": "https://www.lianjiang.gov.cn/ 领导信息"},
    {"id": 13, "name": "王泽荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "连江县委常委（挂职）", "current_org": "中共连江县委员会",
     "source": "https://www.baidu.com/link? 连江县委领导班子页面"},
    # ── County Government Leaders (newly appointed) ──
    {"id": 14, "name": "冯慧钦", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "连江县人大常委会主任", "current_org": "连江县人大常委会",
     "source": "连江县人大会议报道"},
]

organizations = [
    {"id": 1, "name": "中共连江县委员会", "type": "党委", "level": "县处级", "parent": "中共福州市委员会", "location": "福建福州连江"},
    {"id": 2, "name": "连江县人民政府", "type": "政府", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州连江"},
    {"id": 3, "name": "中共连江县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共福州市纪律检查委员会", "location": "福建福州连江"},
    {"id": 4, "name": "连江县人大常委会", "type": "人大", "level": "县处级", "parent": "福州市人大常委会", "location": "福建福州连江"},
    {"id": 5, "name": "连江县人民武装部", "type": "事业单位", "level": "县处级", "parent": "福州警备区", "location": "福建福州连江"},
    {"id": 6, "name": "福州市数据管理局", "type": "政府", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州"},
    {"id": 7, "name": "永泰县人民政府", "type": "政府", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州永泰"},
    {"id": 8, "name": "福州市晋安区委员会", "type": "党委", "level": "县处级", "parent": "中共福州市委员会", "location": "福建福州晋安"},
    {"id": 9, "name": "福清市人民政府", "type": "政府", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州福清"},
    {"id": 10, "name": "福州市江阴工业集中区管委会", "type": "事业单位", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州福清"},
]

positions = [
    # ── 郭勇 ──
    {"person_id": 1, "org_id": 1, "title": "中共连江县委书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": "接替高双成"},
    {"person_id": 1, "org_id": 2, "title": "连江县人民政府县长", "start": "2025-04", "end": "2026-07", "rank": "正处级", "note": "当选县长，接替高双成"},
    {"person_id": 1, "org_id": 2, "title": "连江县人民政府代县长", "start": "2025-04", "end": "2025-04", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "晋安区委副书记", "start": "unknown", "end": "2021-07", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "晋安区委常委、副区长", "start": "unknown", "end": "unknown", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "晋安区委常委、宣传部部长", "start": "unknown", "end": "unknown", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "晋安区委常委、统战部部长", "start": "unknown", "end": "unknown", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "福州市江阴工业集中区管委会副主任", "start": "unknown", "end": "unknown", "rank": "副处级", "note": "早期任职"},
    {"person_id": 1, "org_id": 9, "title": "福州市人才发展集团党委书记、董事长", "start": "unknown", "end": "2021-07", "rank": "正处级", "note": "调任连江前职务"},
    # ── 薛博 ──
    {"person_id": 2, "org_id": 2, "title": "连江县代县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "空降任职"},
    {"person_id": 2, "org_id": 6, "title": "福州市数据管理局局长", "start": "unknown", "end": "2026-07", "rank": "正处级", "note": "兼市数字福州建设领导小组办公室主任"},
    {"person_id": 2, "org_id": 6, "title": "福州市大数据发展管理委员会主任", "start": "unknown", "end": "unknown", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "永泰县副县长", "start": "unknown", "end": "unknown", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "闽侯县白沙镇党委书记", "start": "unknown", "end": "unknown", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "福州市科技局副局长", "start": "unknown", "end": "unknown", "rank": "副处级", "note": ""},
    # ── 高双成 ──
    {"person_id": 3, "org_id": 1, "title": "中共连江县委书记", "start": "2024-12", "end": "2026-07", "rank": "正处级", "note": "免去县长职务，任书记"},
    {"person_id": 3, "org_id": 2, "title": "连江县人民政府县长", "start": "2021-12", "end": "2024-12", "rank": "正处级", "note": "2021年6月任代县长"},
    {"person_id": 3, "org_id": 9, "title": "福清市副市长", "start": "unknown", "end": "2021-06", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "福州市江阴工业集中区管委会纪工委书记", "start": "unknown", "end": "unknown", "rank": "副处级", "note": ""},
    # ── 陈劲松 ──
    {"person_id": 4, "org_id": 1, "title": "中共连江县委书记", "start": "unknown", "end": "2024-12", "rank": "正处级", "note": ""},
    # ── 林吓清 ──
    {"person_id": 5, "org_id": 7, "title": "永泰县人民政府代县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "平级调任"},
    {"person_id": 5, "org_id": 1, "title": "连江县委副书记", "start": "unknown", "end": "2026-07", "rank": "副处级", "note": ""},
]

relationships = [
    # ── 书记-县长 工作关系 ──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "郭勇（县委书记）与薛博（代县长）搭档", "overlap_org": "连江县", "overlap_period": "2026-07至今"},
    # ── 前任-继任 书记关系 ──
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "高双成2026年7月卸任县委书记，郭勇接任", "overlap_org": "中共连江县委员会", "overlap_period": "2025-04至2026-07"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "陈劲松2024年12月卸任县委书记，高双成接任", "overlap_org": "中共连江县委员会", "overlap_period": "2024-12"},
    # ── 县长-前任县长 接替 ──
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "郭勇2025年4月当选县长，接替高双成（升书记）", "overlap_org": "连江县人民政府", "overlap_period": "2025-04"},
    # ── 同乡关系 ──
    {"person_a": 1, "person_b": 3, "type": "same_native_place", "context": "郭勇与高双成均为福建福清人", "overlap_org": "", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "same_native_place", "context": "高双成与余良发均为福建福清人", "overlap_org": "", "overlap_period": ""},
    # ── 常委班子成员 ──
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate", "context": "郑东平（宣传部长）在郭勇（书记）领导下工作", "overlap_org": "中共连江县委员会", "overlap_period": "2025年起"},
    {"person_a": 7, "person_b": 1, "type": "superior_subordinate", "context": "余良发（纪委书记）在郭勇领导下工作", "overlap_org": "中共连江县委员会", "overlap_period": "2025年起"},
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate", "context": "雷发勇（政法委书记）在郭勇领导下工作", "overlap_org": "中共连江县委员会", "overlap_period": "2025年起"},
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "颜学淦（统战部长）在郭勇领导下工作", "overlap_org": "中共连江县委员会", "overlap_period": "2025年起"},
    {"person_a": 10, "person_b": 1, "type": "superior_subordinate", "context": "张记欢（副县长）在郭勇领导下工作", "overlap_org": "连江县人民政府", "overlap_period": "2025年起"},
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate", "context": "陈钧（组织部长）在郭勇领导下工作", "overlap_org": "中共连江县委员会", "overlap_period": "2025年起"},
    {"person_a": 12, "person_b": 1, "type": "superior_subordinate", "context": "刘麟翔（副县长）在郭勇领导下工作", "overlap_org": "连江县人民政府", "overlap_period": "2025年起"},
]

# ── BUILD FUNCTIONS ─────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for po in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                  (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def person_color(pid):
        """Red=party secretary, Blue=government head, Orange=discipline, Grey=other."""
        name = next(p["name"] for p in persons if p["id"] == pid)
        current_post = next(p["current_post"] for p in persons if p["id"] == pid)
        if "县委书记" in current_post or "书记" in name == "郭勇" and "县委书记" in current_post:
            return "255,50,50"
        if "县长" in current_post or "代县长" in current_post:
            return "50,100,255"
        if "纪委书记" in current_post:
            return "255,165,0"
        return "100,100,100"

    def is_top_leader(pid):
        p = next(x for x in persons if x["id"] == pid)
        return "县委书记" in p["current_post"] or "县长" in p["current_post"] or "代县长" in p["current_post"]

    def org_color(otype):
        colors = {
            "党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
            "政协": "255,240,200", "事业单位": "220,220,220", "开发区": "200,255,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>连江县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["id"])
        sz = "20.0" if is_top_leader(p["id"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Org nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> org (worked_at)
    for po in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{po["person_id"]}" target="o{po["org_id"]}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po["title"])}（{po["start"]}-{po["end"]}）"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person -> person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")

# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")

    # Statistics
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
