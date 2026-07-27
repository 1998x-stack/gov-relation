#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西沙区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 海南省
Parent city: 三沙市
Region: 西沙群岛
Target: 区委书记 & 区长
Task ID: hainan_西沙群岛

官方来源（截至2026-07-23）:
- https://www.sansha.gov.cn/ — 三沙市人民政府门户网站
- https://zh.wikipedia.org/wiki/西沙区 — 维基百科
- 上观新闻 2025-08-12 — 书记区长公开亮相报道

当前在任 (as of 2026-07-23):
- 区委书记: 黄晓华（来源：维基百科/上观新闻）
- 区长: 温一凡（来源：维基百科/上观新闻）

注：西沙区与三沙市实行市区合一管理体制。三沙市委市政府同时领导西沙区管理。
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "西沙群岛"
DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

AS_OF = "2026-07-23"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黄晓华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西沙区委书记",
        "current_org": "中共三沙市西沙区委员会",
        "source": "https://zh.wikipedia.org/wiki/西沙区"
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "温一凡",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西沙区区长",
        "current_org": "三沙市西沙区人民政府",
        "source": "https://zh.wikipedia.org/wiki/西沙区"
    },
    # ════════════════════════════════════════
    # 三沙市上级领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "葛国科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "广西浦北",
        "education": "浙江大学（博士）",
        "party_join": "中共党员（1998年加入）",
        "work_start": "2000年左右",
        "current_post": "中共三沙市委书记",
        "current_org": "中共三沙市委员会",
        "source": "https://zh.wikipedia.org/wiki/葛国科"
    },
    {
        "id": 4,
        "name": "陈儒茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三沙市代市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/202312/d6b3e6f4de034b2f8574517d324ac504.shtml"
    },
    # ════════════════════════════════════════
    # 三沙市副市长（西沙区分管领导参考）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "王长仁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年11月",
        "birthplace": "吉林农安",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三沙市人大常委会主任",
        "current_org": "三沙市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/王长仁"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共三沙市西沙区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共三沙市委员会",
        "location": "西沙区永兴岛"
    },
    {
        "id": 2,
        "name": "三沙市西沙区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "三沙市人民政府",
        "location": "西沙区永兴岛"
    },
    {
        "id": 3,
        "name": "中共三沙市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共海南省委",
        "location": "西沙区永兴岛"
    },
    {
        "id": 4,
        "name": "三沙市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "海南省人民政府",
        "location": "西沙区永兴岛"
    },
    {
        "id": 5,
        "name": "三沙市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "海南省人大常委会",
        "location": "西沙区永兴岛"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "西沙区委书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": "来源：维基百科/上观新闻"},
    # 区长
    {"person_id": 2, "org_id": 1, "title": "西沙区委副书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "西沙区区长",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": "来源：维基百科/上观新闻"},
    # 三沙市委书记
    {"person_id": 3, "org_id": 3, "title": "中共三沙市委书记",
     "start_date": "2024年12月", "end_date": "present", "rank": "正厅级", "note": "跨省调任（广西→海南）"},
    # 三沙市代市长
    {"person_id": 4, "org_id": 3, "title": "三沙市委副书记",
     "start_date": "2026年1月", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "三沙市代市长",
     "start_date": "2026年1月", "end_date": "present", "rank": "正厅级", "note": ""},
    # 人大主任
    {"person_id": 5, "org_id": 5, "title": "三沙市人大常委会主任",
     "start_date": "2022年1月", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 区委书记 ↔ 区长（核心搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "西沙区委书记与区长党政搭档",
     "overlap_org": "中共三沙市西沙区委员会/三沙市西沙区人民政府",
     "overlap_period": "当前"},
    # 区委书记 ↔ 三沙市委书记（上下级）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "西沙区委接受三沙市委领导",
     "overlap_org": "三沙市党委系统",
     "overlap_period": "当前"},
    # 区长 ↔ 三沙市市长（上下级）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "西沙区政府接受三沙市政府领导（市区合一体制）",
     "overlap_org": "三沙市政府系统",
     "overlap_period": "当前"},
    # 三沙市委书记 ↔ 代市长（搭档）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "葛国科任市委书记，陈儒茂任代市长，共同搭档",
     "overlap_org": "三沙市",
     "overlap_period": "2026年1月至今"},
]

# =========================================================================
# 5. GEXF BUILDER
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Return RGB string for a person based on their role."""
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — Party Secretary
    if "区长" in post or "市长" in post or "副区长" in post:
        return "50,100,255"   # Blue — Government
    if "人大" in post:
        return "200,255,255"  # Cyan
    return "100,100,100"      # Grey — Others


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf():
    lines = []
    now = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>三沙市西沙区领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes: nodes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="a0" title="type" type="string"/>')
    lines.append('      <attribute id="a1" title="current_post" type="string"/>')
    lines.append('      <attribute id="a2" title="current_org" type="string"/>')
    lines.append('    </attributes>')

    # Attributes: edges
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="e0" title="type" type="string"/>')
    lines.append('      <attribute id="e1" title="context" type="string"/>')
    lines.append('      <attribute id="e2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="e3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="a0" value="person"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="a2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="a0" value="organization"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="a2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="e0" value="worked_at"/>')
        lines.append(f'          <attvalue for="e1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="e0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="e1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="e2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="e3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    return "\n".join(lines)


# =========================================================================
# 6. BUILD
# =========================================================================
def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop existing tables for fresh build
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
    """)

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start_date TEXT, end_date TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start_date"], pos["end_date"], pos["rank"], pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

    # ── Summary ──
    print(f"✅ SQLite: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")

    # ── GEXF ──
    gexf_content = build_gexf()
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf_content)
    print(f"✅ GEXF:  {GEXF_PATH}")


# =========================================================================
# 7. Person JSON
# =========================================================================
def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "西沙区 - 维基百科",
         "url": "https://zh.wikipedia.org/wiki/西沙区",
         "publisher": "维基百科", "published_at": "2026-03-17",
         "accessed_at": AS_OF, "source_type": "encyclopedia",
         "reliability": "medium",
         "notes": "列明区委书记黄晓华、区长温一凡"},
        {"id": "S002", "title": "海南三沙市西沙区委书记、区长公开亮相",
         "url": "https://www.jfdaily.com/staticsg/res/html/web/newsDetail.html?id=827085",
         "publisher": "上观新闻", "published_at": "2025-08-12",
         "accessed_at": AS_OF, "source_type": "media",
         "reliability": "high",
         "notes": "文章已下线，标题确认黄晓华、温一凡同时公开亮相"},
        {"id": "S003", "title": "三沙市 - 维基百科",
         "url": "https://zh.wikipedia.org/wiki/三沙市",
         "publisher": "维基百科", "published_at": "",
         "accessed_at": AS_OF, "source_type": "encyclopedia",
         "reliability": "medium",
         "notes": "三沙市领导信息"},
        {"id": "S004", "title": "三沙市人民政府 - 领导之窗",
         "url": "https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml",
         "publisher": "三沙市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official",
         "reliability": "high",
         "notes": "市政府领导列表"},
    ]

    def make_person_json(p, timeline, relationships_list):
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "海南省",
                "city": "三沙市",
                "region": "西沙群岛",
                "job": p.get("current_post", ""),
                "task_id": "hainan_西沙群岛",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"xisha_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "partial",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 三沙"],
                 "last_attempted": AS_OF},
            ]
        }

    # ── 黄晓华 Person JSON ──
    hxh_timeline = [
        {"start": "", "end": "present", "org": "中共三沙市西沙区委员会",
         "title": "西沙区委书记",
         "notes": "现任；信息来源：维基百科/上观新闻",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到黄晓华的履历信息。其出生年份、籍贯、教育背景、此前职务均未知。",
         "confidence": "unverified", "source_ids": []},
    ]
    hxh_relationships = [
        {"person": "温一凡", "person_id": "xisha_温一凡",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄晓华（区委书记）与温一凡（区长）党政搭档",
         "overlap_org": "中共三沙市西沙区委员会/三沙市西沙区人民政府",
         "overlap_period": "当前",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "葛国科", "person_id": "xisha_葛国科",
         "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "西沙区委接受三沙市委领导",
         "overlap_org": "三沙市党委系统",
         "overlap_period": "当前",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
    ]

    hxh_json = make_person_json(persons[0], hxh_timeline, hxh_relationships)
    hxh_path = os.path.join(PERSONS_DIR, f"{TODAY}-海南省-三沙市-西沙区委书记-黄晓华.json")
    with open(hxh_path, "w", encoding="utf-8") as f:
        json.dump(hxh_json, f, ensure_ascii=False, indent=2)
    print(f"✅ Person JSON: {hxh_path}")

    # ── 温一凡 Person JSON ──
    wyf_timeline = [
        {"start": "", "end": "present", "org": "三沙市西沙区人民政府",
         "title": "西沙区区长",
         "notes": "现任；信息来源：维基百科/上观新闻",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到温一凡的履历信息。其出生年份、籍贯、教育背景、此前职务均未知。",
         "confidence": "unverified", "source_ids": []},
    ]
    wyf_relationships = [
        {"person": "黄晓华", "person_id": "xisha_黄晓华",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "温一凡（区长）与黄晓华（区委书记）党政搭档",
         "overlap_org": "中共三沙市西沙区委员会/三沙市西沙区人民政府",
         "overlap_period": "当前",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "陈儒茂", "person_id": "xisha_陈儒茂",
         "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "西沙区政府接受三沙市政府领导（市区合一体制）",
         "overlap_org": "三沙市政府系统",
         "overlap_period": "当前",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
    ]

    wyf_json = make_person_json(persons[1], wyf_timeline, wyf_relationships)
    wyf_path = os.path.join(PERSONS_DIR, f"{TODAY}-海南省-三沙市-西沙区长-温一凡.json")
    with open(wyf_path, "w", encoding="utf-8") as f:
        json.dump(wyf_json, f, ensure_ascii=False, indent=2)
    print(f"✅ Person JSON: {wyf_path}")


# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    build()
    build_person_jsons()
    print(f"\n{'='*60}")
    print(f"✅ Build complete!")
    print(f"   DB:    {DB_PATH}")
    print(f"   GEXF:  {GEXF_PATH}")
    print(f"{'='*60}")
