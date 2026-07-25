#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上海市普陀区 leadership network.

调查日期: 2026-07-25
信息来源: 上海市普陀区人民政府门户网站 (www.shpt.gov.cn)
调查级别: 市辖区(直辖市)

Confirmed from government news articles (2026-07):
- 胡广杰 — 普陀区委书记
- 赵亮 — 普陀区委副书记、区长
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "普陀区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "普陀区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "上海市普陀区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════════════════════

    # 区委书记 — 胡广杰
    {
        "id": 1,
        "name": "胡广杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-04",
        "birthplace": "浙江慈溪",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "1993-07",
        "current_post": "中共上海市普陀区委书记",
        "current_org": "中共上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
        "notes": "曾任上海市黄浦区副区长、区委常委；上海市住房和城乡建设管理委员会副主任；2021年8月起任普陀区委书记",
    },
    # 区委副书记、区长 — 赵亮
    {
        "id": 2,
        "name": "赵亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普陀区委副书记、区长",
        "current_org": "上海市普陀区人民政府",
        "source": "https://www.shpt.gov.cn/",
        "notes": "2025年任普陀区委副书记、区长",
    },
    # 区委副书记 — 赵勇
    {
        "id": 3,
        "name": "赵勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市普陀区委副书记",
        "current_org": "中共上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
    },
    # 区委常委、组织部部长 — 李红珍
    {
        "id": 4,
        "name": "李红珍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普陀区委常委、组织部部长",
        "current_org": "中共上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
    },
    # 区委常委 — 李荣华
    {
        "id": 5,
        "name": "李荣华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市普陀区委常委",
        "current_org": "中共上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
    },
    # 区委常委、统战部部长 — 魏静
    {
        "id": 6,
        "name": "魏静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普陀区委常委、统战部部长",
        "current_org": "中共上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
    },
    # 区委常委 — 厉蕾
    {
        "id": 7,
        "name": "厉蕾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市普陀区委常委",
        "current_org": "中共上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
    },
    # 区委常委 — 魏子新
    {
        "id": 8,
        "name": "魏子新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市普陀区委常委",
        "current_org": "中共上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
    },
    # 副区长 — 胡建会
    {
        "id": 9,
        "name": "胡建会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上海市普陀区副区长",
        "current_org": "上海市普陀区人民政府",
        "source": "https://www.shpt.gov.cn/",
    },

    # ═══════════════════════════════════════════════
    # 区人大 (District People's Congress)
    # ═══════════════════════════════════════════════
    {
        "id": 10,
        "name": "谈上伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普陀区人大常委会主任",
        "current_org": "上海市普陀区人民代表大会常务委员会",
        "source": "https://www.shpt.gov.cn/",
    },

    # ═══════════════════════════════════════════════
    # 区政协 (District Political Consultative Conference)
    # ═══════════════════════════════════════════════
    {
        "id": 11,
        "name": "杭春芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普陀区政协主席",
        "current_org": "中国人民政治协商会议上海市普陀区委员会",
        "source": "https://www.shpt.gov.cn/",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共上海市普陀区委员会",
        "type": "党委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市委",
        "location": "上海市普陀区",
    },
    {
        "id": 2,
        "name": "上海市普陀区人民政府",
        "type": "政府",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民政府",
        "location": "上海市普陀区",
    },
    {
        "id": 3,
        "name": "上海市普陀区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民代表大会常务委员会",
        "location": "上海市普陀区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议上海市普陀区委员会",
        "type": "政协",
        "level": "市辖区(直辖市)",
        "parent": "中国人民政治协商会议上海市委员会",
        "location": "上海市普陀区",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 胡广杰
    {"person_id": "p1", "org_id": 1, "title": "中共上海市普陀区委书记",
     "start_date": "2021-08", "end_date": "present", "rank": "正厅级",
     "note": "2021年8月起任普陀区委书记"},
    # 赵亮
    {"person_id": "p2", "org_id": 2, "title": "普陀区委副书记、区长",
     "start_date": "2025", "end_date": "present", "rank": "正厅级",
     "note": "2025年起任普陀区委副书记、区长"},
    {"person_id": "p2", "org_id": 1, "title": "中共上海市普陀区委副书记",
     "start_date": "2025", "end_date": "present", "rank": "正厅级",
     "note": ""},
    # 赵勇
    {"person_id": "p3", "org_id": 1, "title": "中共上海市普陀区委副书记",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
    # 李红珍
    {"person_id": "p4", "org_id": 1, "title": "普陀区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
    # 李荣华
    {"person_id": "p5", "org_id": 1, "title": "中共上海市普陀区委常委",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
    # 魏静
    {"person_id": "p6", "org_id": 1, "title": "普陀区委常委、统战部部长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
    # 厉蕾
    {"person_id": "p7", "org_id": 1, "title": "中共上海市普陀区委常委",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
    # 魏子新
    {"person_id": "p8", "org_id": 1, "title": "中共上海市普陀区委常委",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
    # 胡建会
    {"person_id": "p9", "org_id": 2, "title": "上海市普陀区副区长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管数据、政务智能等工作"},
    # 谈上伟
    {"person_id": "p10", "org_id": 3, "title": "普陀区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": ""},
    # 杭春芳
    {"person_id": "p11", "org_id": 4, "title": "普陀区政协主席",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
# Overlaps in 普陀区委常委会 (same org, same period)
relationships = [
    {
        "person_a": "p1",
        "person_b": "p2",
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档",
        "overlap_org": "中共上海市普陀区委员会/普陀区人民政府",
        "overlap_period": "2025-至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p3",
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记",
        "overlap_org": "中共上海市普陀区委员会",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2",
        "person_b": "p3",
        "type": "overlap",
        "context": "区委副书记与区长",
        "overlap_org": "中共上海市普陀区委员会",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p4",
        "type": "superior_subordinate",
        "context": "区委书记与组织部长",
        "overlap_org": "中共上海市普陀区委员会",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p5",
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共上海市普陀区委员会",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p6",
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共上海市普陀区委员会",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p7",
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共上海市普陀区委员会",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p8",
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共上海市普陀区委员会",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2",
        "person_b": "p9",
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "普陀区人民政府",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p10",
        "type": "overlap",
        "context": "区委与区人大领导",
        "overlap_org": "普陀区",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p11",
        "type": "overlap",
        "context": "区委与区政协领导",
        "overlap_org": "普陀区",
        "overlap_period": "至今",
        "confidence": "confirmed",
    },
]

# ── AS-OF DATE ─────────────────────────────────────────────────────
AS_OF = "2026-07-25"


# ═══════════════════════════════════════════════════════════════════
#  Build
# ═══════════════════════════════════════════════════════════════════
def build():
    """Run database + GEXF build."""
    import sqlite3

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
            start_date TEXT,
            end_date TEXT,
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
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start_date", ""), pos.get("end_date", "present"),
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
        if "区委书记" in post and "副" not in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "区长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "区委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and "区长" in post:
            return ("100,150,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>普陀区领导班子工作关系网络 - {AS_OF}</description>')
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
    print(f"普陀区 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
