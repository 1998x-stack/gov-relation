#!/usr/bin/env python3
"""鹤峰县领导班子工作关系网络数据生成脚本。

任务: hubei_鹤峰县
省份: 湖北省
上级市: 恩施土家族苗族自治州
级别: 县
核心目标: 县委书记 & 县长

当前领导班子 (截至 2025-2026 年):
- 县委书记: 向子明 (2024.11-)
- 县长: 王兵 (2021.11-)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "鹤峰县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "鹤峰县_network.gexf")
AS_OF = datetime.now().strftime("%Y-%m-%d")

# ── Data ───────────────────────────────────────────────────────────────────
persons = [
    {
        "id": "p1",
        "name": "向子明",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1973年7月",
        "birthplace": "湖北宣恩",
        "education": "省委党校大学",
        "party_join": "1995年3月",
        "work_start": "1993年8月",
        "current_post": "县委书记",
        "current_org": "中共鹤峰县委员会",
        "source": "https://baike.baidu.com/item/%E5%90%91%E5%AD%90%E6%98%8E/5037004",
        "notes": "2016.10 来凤县委常委、副县长; 2020.04 恩施州科协党组书记、主席; 2021.08 恩施市委副书记、代市长; 2021.11 恩施市委副书记、市长; 2024.11 鹤峰县委书记",
    },
    {
        "id": "p2",
        "name": "王兵",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1978年3月",
        "birthplace": "湖北恩施",
        "education": "大学本科",
        "party_join": "2001年6月",
        "work_start": "1999年12月",
        "current_post": "县长",
        "current_org": "鹤峰县人民政府",
        "source": "https://baike.baidu.com/item/%E7%8E%8B%E5%85%B5/59059980",
        "notes": "曾任恩施市芭蕉乡、六角亭办事处、白果乡; 咸丰副县长、政法委书记、常务副县长; 恩施州政府副秘书长; 2021.11 鹤峰县委副书记、县长",
    },
    {
        "id": "p3",
        "name": "彭元洪",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1975年6月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共恩施市委员会",
        "source": "https://baike.baidu.com/item/%E5%BD%AD%E5%85%83%E6%B4%AA/20372955",
        "notes": "2021.06-2024.10 鹤峰县委书记; 曾任鹤峰县长; 2024年调任恩施市委书记",
    },
    {
        "id": "p4",
        "name": "刘芳震",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1962年10月",
        "birthplace": "湖北鹤峰",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "前任恩施州长",
        "current_org": "恩施州人民政府",
        "source": "data/persons/20260724-湖北省-恩施土家族苗族自治州-前任州长-刘芳震.json",
        "notes": "恩施州前任州长，鹤峰县人。与鹤峰县有地理渊源",
    },
    {
        "id": "p5",
        "name": "任振鹤",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1964年2月",
        "birthplace": "湖北鹤峰",
        "education": "中央党校大学",
        "party_join": "1985年2月",
        "work_start": "1982年9月",
        "current_post": "甘肃省省长",
        "current_org": "甘肃省人民政府",
        "source": "data/persons/20260717-甘肃省-省本级-省长-任振鹤.json",
        "notes": "出生于鹤峰县，曾在鹤峰县任职多年（鹤峰县委副书记、副县长、民族贸易局等）",
    },
]

organizations = [
    {"id": 1, "name": "中共鹤峰县委员会", "type": "党委", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州鹤峰县"},
    {"id": 2, "name": "鹤峰县人民政府", "type": "政府", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州鹤峰县"},
    {"id": 3, "name": "中共恩施市委员会", "type": "党委", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州恩施市"},
    {"id": 4, "name": "恩施市人民政府", "type": "政府", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州恩施市"},
    {"id": 5, "name": "恩施州人民政府", "type": "政府", "level": "地市级", "parent": "湖北省", "location": "湖北省恩施州"},
    {"id": 6, "name": "恩施州科学技术协会", "type": "群团", "level": "地市级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州"},
    {"id": 7, "name": "中共咸丰县委员会", "type": "党委", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州咸丰县"},
    {"id": 8, "name": "咸丰县人民政府", "type": "政府", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州咸丰县"},
    {"id": 9, "name": "甘肃省人民政府", "type": "政府", "level": "省级", "parent": "甘肃省", "location": "甘肃省兰州市"},
    {"id": 10, "name": "中共来凤县委员会", "type": "党委", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州来凤县"},
    {"id": 11, "name": "中共宣恩县委员会", "type": "党委", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州宣恩县"},
    {"id": 12, "name": "宣恩县人民政府", "type": "政府", "level": "县级", "parent": "恩施土家族苗族自治州", "location": "湖北省恩施州宣恩县"},
    {"id": 13, "name": "鹤峰县人大常委会", "type": "人大", "level": "县级", "parent": "鹤峰县", "location": "湖北省恩施州鹤峰县"},
    {"id": 14, "name": "鹤峰县政协", "type": "政协", "level": "县级", "parent": "鹤峰县", "location": "湖北省恩施州鹤峰县"},
]

positions = [
    # 向子明
    {"person_id": "p1", "org_id": 1, "title": "县委书记、县人武部党委第一书记", "start": "2024年11月", "end": "present", "rank": "正县级", "note": "现任"},
    {"person_id": "p1", "org_id": 4, "title": "恩施市委副书记、市长", "start": "2021年8月", "end": "2024年10月", "rank": "正县级", "note": ""},
    {"person_id": "p1", "org_id": 6, "title": "恩施州科协党组书记、主席", "start": "2020年4月", "end": "2021年8月", "rank": "正县级", "note": ""},
    {"person_id": "p1", "org_id": 10, "title": "来凤县委常委、副县长", "start": "2016年10月", "end": "2020年4月", "rank": "副县级", "note": ""},
    {"person_id": "p1", "org_id": 12, "title": "宣恩县副县长", "start": "2010年12月", "end": "2016年10月", "rank": "副县级", "note": "2010.9-2010.12副县长兼珠山镇书记; 2012-2013福建涵江区挂职副区长"},
    {"person_id": "p1", "org_id": 11, "title": "珠山镇党委书记", "start": "2009年8月", "end": "2010年12月", "rank": "正科级", "note": ""},
    {"person_id": "p1", "org_id": 11, "title": "沙道沟镇党委书记、镇长", "start": "2006年11月", "end": "2009年8月", "rank": "正科级", "note": ""},
    {"person_id": "p1", "org_id": 11, "title": "沙道沟镇党委副书记、镇长", "start": "2004年2月", "end": "2006年11月", "rank": "正科级", "note": "其间在湖北省环保局挂职"},
    # 王兵
    {"person_id": "p2", "org_id": 2, "title": "县委副书记、县长", "start": "2021年11月", "end": "present", "rank": "正县级", "note": "现任"},
    {"person_id": "p2", "org_id": 5, "title": "恩施州政府副秘书长", "start": "", "end": "2021年11月", "rank": "正县级", "note": ""},
    {"person_id": "p2", "org_id": 7, "title": "咸丰县委常委、常务副县长", "start": "", "end": "", "rank": "副县级", "note": "曾任咸丰县委常委、政法委书记"},
    {"person_id": "p2", "org_id": 8, "title": "咸丰县副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 彭元洪
    {"person_id": "p3", "org_id": 1, "title": "县委书记", "start": "2021年6月", "end": "2024年10月", "rank": "正县级", "note": "前任县委书记"},
    {"person_id": "p3", "org_id": 2, "title": "县长", "start": "", "end": "2021年6月", "rank": "正县级", "note": "曾任鹤峰县长"},
    {"person_id": "p3", "org_id": 3, "title": "恩施市委书记", "start": "2024年", "end": "present", "rank": "正县级", "note": "现任恩施市委书记"},
    # 刘芳震
    {"person_id": "p4", "org_id": 5, "title": "恩施州长", "start": "", "end": "2024年", "rank": "正厅级", "note": "前任州长"},
    # 任振鹤
    {"person_id": "p5", "org_id": 9, "title": "甘肃省省长", "start": "2021年", "end": "present", "rank": "正省级", "note": "现任甘肃省省长"},
    {"person_id": "p5", "org_id": 1, "title": "鹤峰县委副书记", "start": "", "end": "", "rank": "", "note": "早年鹤峰任职"},
    {"person_id": "p5", "org_id": 2, "title": "鹤峰县委常委、副县长", "start": "", "end": "", "rank": "", "note": "早年鹤峰任职"},
]

relationships = [
    {
        "person_a": "p1", "person_b": "p2",
        "type": "superior_subordinate",
        "context": "党委书记与县长搭档",
        "overlap_org": "鹤峰县",
        "overlap_period": "2024.11-至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1", "person_b": "p3",
        "type": "predecessor_successor",
        "context": "向子明接替彭元洪任鹤峰县委书记",
        "overlap_org": "中共鹤峰县委员会",
        "overlap_period": "2024.11",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p3",
        "type": "overlap",
        "context": "彭元洪任县委书记时王兵任县长",
        "overlap_org": "鹤峰县",
        "overlap_period": "2021.11-2024.10",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1", "person_b": "p4",
        "type": "same_system",
        "context": "同在恩施州工作体系",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": "",
        "confidence": "plausible",
    },
    {
        "person_a": "p2", "person_b": "p4",
        "type": "superior_subordinate",
        "context": "王兵曾任恩施州政府副秘书长，刘芳震时任州长",
        "overlap_org": "恩施州人民政府",
        "overlap_period": "至2021.11",
        "confidence": "plausible",
    },
    {
        "person_a": "p5", "person_b": "p3",
        "type": "same_native_place",
        "context": "任振鹤出生于鹤峰，彭元洪曾任鹤峰县委书记",
        "overlap_org": "鹤峰县",
        "overlap_period": "",
        "confidence": "weak",
    },
]


# ── Build ──────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
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

    # Normalize person ids: strip "p" prefix for DB
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
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

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "委" not in post:
            return ("50,100,255", 20.0)
        elif "前任" in post and ("书记" in post or "县长" in post or "州长" in post):
            return ("100,100,100", 12.0)
        elif "省长" in post:
            return ("50,150,50", 15.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
        "群团": ("255,220,255", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>鹤峰县领导班子工作关系网络 - {AS_OF}</description>')
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
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
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

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"鹤峰县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
    print(f"AS_OF:       {AS_OF}")


if __name__ == "__main__":
    build()
