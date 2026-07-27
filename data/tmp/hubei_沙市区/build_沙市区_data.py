#!/usr/bin/env python3
"""沙市区领导班子工作关系网络 - 数据构建脚本"""

import os
import sys
import sqlite3
from datetime import datetime

SLUG = "沙市区"
REGION = "沙市区"
PARENT_CITY = "荆州市"
PROVINCE = "湖北省"
LEVEL = "市辖区"
TODAY = datetime.now().strftime("%Y-%m-%d")
AS_OF = "2026-07-25"

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "沙市区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "沙市区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════════════════════════

# Person ID convention: p{number} (used in GEXF), number used in DB
persons = [
    {
        "id": 1,
        "name": "卢永桢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "湖北",
        "education": "大学学历，公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "沙市区委书记",
        "current_org": "中共沙市区委员会",
        "source": "https://baike.baidu.com/item/%E5%8D%A2%E6%B0%B8%E6%A1%A2",
        "notes": "2024年8月由武汉市东西湖区副区长调任沙市区委书记。曾任武汉市东山街道党工委书记、慈惠街工委书记、东西湖区副区长等职。"
    },
    {
        "id": 2,
        "name": "郭熙胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沙市区委副书记、区长",
        "current_org": "沙湾区人民政府",
        "source": "http://www.shashi.gov.cn/ssqxw/ssyw/202606/t20260630_1119411.shtml",
        "notes": "作为区委副书记、区长主持区政府全面工作。履历详情待查。"
    },
    {
        "id": 3,
        "name": "刘艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沙市区委副书记、政法委书记",
        "current_org": "中共沙市区委员会",
        "source": "http://www.shashi.gov.cn/ssqxw/ssyw/202606/t20260630_1119411.shtml",
        "notes": "兼任区委政法委书记。履历详情待查。"
    },
    {
        "id": 4,
        "name": "李炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沙市区委常委、组织部部长",
        "current_org": "中共沙市区委员会组织部",
        "source": "http://www.shashi.gov.cn/ssqxw/ssyw/202606/t20260630_1119411.shtml",
        "notes": "履历详情待查。"
    },
    {
        "id": 5,
        "name": "余松柏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沙市区委领导",
        "current_org": "中共沙市区委员会",
        "source": "http://www.shashi.gov.cn/ssqxw/ssyw/202606/t20260630_1119411.shtml",
        "notes": "区领导。具体职务待查。"
    },
    {
        "id": 6,
        "name": "唐华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沙市区委领导",
        "current_org": "中共沙市区委员会",
        "source": "http://www.shashi.gov.cn/ssqxw/ssyw/202606/t20260630_1119411.shtml",
        "notes": "区领导。具体职务待查。"
    },
    {
        "id": 7,
        "name": "冯亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沙市区委领导",
        "current_org": "中共沙市区委员会",
        "source": "http://www.shashi.gov.cn/ssqxw/ssyw/202606/t20260630_1119411.shtml",
        "notes": "区领导。具体职务待查。"
    },
    {
        "id": 8,
        "name": "黄勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任",
        "current_org": "",
        "source": "https://www.sogou.com/web?query=%E6%B2%99%E5%B8%82%E5%8C%BA+%E5%8C%BA%E5%A7%94%E4%B9%A6%E8%AE%B0+%E7%8E%B0%E4%BB%BB",
        "notes": "前任沙市区委书记。2024年8月由卢永桢接替。去向待查。"
    },
]

organizations = [
    {"id": 1, "name": "中共沙市区委员会", "type": "党委", "level": "县处级", "parent": "中共荆州市委员会", "location": "荆州市沙市区"},
    {"id": 2, "name": "沙湾区人民政府", "type": "政府", "level": "县处级", "parent": "荆州市人民政府", "location": "荆州市沙市区"},
    {"id": 3, "name": "中共沙市区委组织部", "type": "党委", "level": "乡科级", "parent": "中共沙市区委员会", "location": "荆州市沙市区"},
    {"id": 4, "name": "中共沙市区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共沙市区委员会", "location": "荆州市沙市区"},
]

positions = [
    # 卢永桢
    {"person_id": "p1", "org_id": 1, "title": "沙市区委书记", "start": "2024-08", "end": "present", "rank": "县处级正职",
     "note": "2024年8月12日沙市区领导干部会议宣布省委决定"},
    {"person_id": "p1", "org_id": 0, "title": "武汉市东西湖区副区长", "start": "2021-12", "end": "2024-08", "rank": "县处级副职",
     "note": "兼开发区管委会副主任"},
    {"person_id": "p1", "org_id": 0, "title": "武汉市东西湖区慈惠街工委书记", "start": "", "end": "", "rank": "",
     "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "武汉市东山街道党工委书记", "start": "", "end": "", "rank": "",
     "note": "早期职务"},
    # 郭熙胜
    {"person_id": "p2", "org_id": 2, "title": "沙市区区长", "start": "", "end": "present", "rank": "县处级正职",
     "note": "兼区委副书记"},
    # 刘艳
    {"person_id": "p3", "org_id": 1, "title": "沙市区委副书记", "start": "", "end": "present", "rank": "县处级副职",
     "note": "兼政法委书记"},
    {"person_id": "p3", "org_id": 4, "title": "沙市区委政法委书记", "start": "", "end": "present", "rank": "乡科级正职",
     "note": "由区委副书记兼任"},
    # 李炜
    {"person_id": "p4", "org_id": 3, "title": "沙市区委组织部部长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "区委常委"},
    {"person_id": "p4", "org_id": 1, "title": "沙市区委常委", "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    # 余松柏 (区领导)
    {"person_id": "p5", "org_id": 1, "title": "沙市区领导", "start": "", "end": "present", "rank": "县处级副职",
     "note": "区委常委或副区长"},
    # 唐华 (区领导)
    {"person_id": "p6", "org_id": 1, "title": "沙市区领导", "start": "", "end": "present", "rank": "县处级副职",
     "note": "区委常委或副区长"},
    # 冯亮 (区领导)
    {"person_id": "p7", "org_id": 1, "title": "沙市区领导", "start": "", "end": "present", "rank": "县处级副职",
     "note": "区委常委或副区长"},
    # 黄勇 (前任区委书记)
    {"person_id": "p8", "org_id": 1, "title": "沙市区委书记", "start": "", "end": "2024-08", "rank": "县处级正职",
     "note": "前任，由卢永桢接替"},
]

relationships = [
    # 卢永桢 ↔ 郭熙胜 (党政主官搭档)
    {"person_a": "p1", "person_b": "p2", "type": "overlap", "context": "党政主官搭档",
     "overlap_org": "沙市区委/区政府", "overlap_period": "2024-08至今", "confidence": "confirmed"},
    # 卢永桢 ↔ 刘艳 (上下级)
    {"person_a": "p1", "person_b": "p3", "type": "superior_subordinate", "context": "区委书记与副书记",
     "overlap_org": "中共沙市区委", "overlap_period": "2024-08至今", "confidence": "confirmed"},
    # 卢永桢 ↔ 李炜 (上下级)
    {"person_a": "p1", "person_b": "p4", "type": "superior_subordinate", "context": "区委书记与组织部部长",
     "overlap_org": "中共沙市区委", "overlap_period": "2024-08至今", "confidence": "confirmed"},
    # 卢永桢 ↔ 黄勇 (前后任)
    {"person_a": "p1", "person_b": "p8", "type": "predecessor_successor", "context": "前后任区委书记",
     "overlap_org": "中共沙市区委", "overlap_period": "2024-08交接", "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color_and_size(post):
    if "区委书记" in post and "副" not in post:
        return ("255,50,50", 20.0)
    elif "区长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    elif "区委副书记" in post:
        return ("150,50,50", 15.0)
    elif "常委" in post and ("组织" in post or "政法" in post):
        return ("100,150,255", 12.0)
    elif "人大" in post or "政协" in post:
        return ("200,255,255", 12.0)
    elif "已离任" in post or "原" in post:
        return ("150,150,150", 10.0)
    else:
        return ("100,100,100", 12.0)


org_colors = {
    "党委": ("255,200,200", 8.0),
    "政府": ("200,200,255", 8.0),
    "人大": ("200,255,255", 8.0),
    "政协": ("255,240,200", 8.0),
}


def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # ── SQLite ────────────────────────────────────────────────────────────
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
            source TEXT,
            notes TEXT
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
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid("p" + str(p["id"])), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──────────────────────────────────────────────────────────────
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    print(f"\n{'='*60}")
    print(f"{SLUG} Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
