#!/usr/bin/env python3
"""Build 柳北区 (Liubei District, Liuzhou, Guangxi) leadership network.

Generated: 2026-07-22
Sources: lbq.gov.cn leadership page, build_城中区_data.py (predecessor info)
"""

import json
import os
import sqlite3
from datetime import datetime

# =========================================================================
# Constants
# =========================================================================
AS_OF = "2026-07-22"
STAGING = os.path.dirname(os.path.abspath(__file__))
PERSONS_DIR = os.path.join(STAGING, "persons")
DB_PATH = os.path.join(STAGING, "柳北区_network.db")
GEXF_PATH = os.path.join(STAGING, "柳北区_network.gexf")

NOW = AS_OF.replace("-", "")

# =========================================================================
# Source Register
# =========================================================================
source_register = [
    {
        "id": "S001",
        "title": "柳北区人民政府 - 区政府领导",
        "url": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml",
        "publisher": "柳州市柳北区人民政府",
        "published_at": "2026-07-22",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 洪进兴 as 区长, 杜冰/何杰/刘超/王廷华 as 副区长"
    },
    {
        "id": "S002",
        "title": "柳北区人民政府 - 领导之窗",
        "url": "http://www.lbq.gov.cn/xxgk/fdzdgknr/ldzc/lists.shtml",
        "publisher": "柳州市柳北区人民政府",
        "published_at": "2026-07-22",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 洪进兴 as 区长"
    },
    {
        "id": "S003",
        "title": "城中区领导网络构建脚本",
        "url": "build_城中区_data.py (local repository)",
        "publisher": "Gov-Relation Research",
        "published_at": "2026-07-22",
        "accessed_at": AS_OF,
        "source_type": "database",
        "reliability": "high",
        "notes": "Confirms 周水祥 as 柳北区委书记 (appointed 2026-06)"
    },
    {
        "id": "S004",
        "title": "周水祥百度百科",
        "url": "https://baike.baidu.com/item/%E5%91%A8%E6%B0%B4%E7%A5%A5/31661385",
        "publisher": "百度百科",
        "published_at": "2026",
        "accessed_at": AS_OF,
        "source_type": "encyclopedia",
        "reliability": "medium",
        "notes": "周水祥 biography: b.1984-06, Jiangxi Hukou, Tsinghua LLM"
    },
]

# =========================================================================
# Data: Persons
# =========================================================================
persons = [
    {
        "id": 1,
        "name": "周水祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-06",
        "birthplace": "",
        "education": "研究生/法律硕士（清华大学）",
        "party_join": "2005-11",
        "work_start": "2011-07",
        "current_post": "柳州市柳北区委书记",
        "current_org": "中共柳州市柳北区委员会",
        "source": "https://baike.baidu.com/item/%E5%91%A8%E6%B0%B4%E7%A5%A5/31661385"
    },
    {
        "id": 2,
        "name": "洪进兴",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳州市柳北区区长",
        "current_org": "柳州市柳北区人民政府",
        "source": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml"
    },
    {
        "id": 3,
        "name": "杜冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳北区副区长",
        "current_org": "柳州市柳北区人民政府",
        "source": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml"
    },
    {
        "id": 4,
        "name": "何杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳北区副区长",
        "current_org": "柳州市柳北区人民政府",
        "source": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml"
    },
    {
        "id": 5,
        "name": "刘超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳北区副区长",
        "current_org": "柳州市柳北区人民政府",
        "source": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml"
    },
    {
        "id": 6,
        "name": "王廷华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳北区副区长",
        "current_org": "柳州市柳北区人民政府",
        "source": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml"
    },
    {
        "id": 7,
        "name": "方正柱",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳北区政府党组成员",
        "current_org": "柳州市柳北区人民政府",
        "source": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml"
    },
    {
        "id": 8,
        "name": "许海亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳北区政府党组成员",
        "current_org": "柳州市柳北区人民政府",
        "source": "http://www.lbq.gov.cn/xxgk/qzfld/lists.shtml"
    },
    {
        "id": 9,
        "name": "宋军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "广西融安",
        "education": "在职大学学历",
        "party_join": "1998-12",
        "work_start": "1993-07",
        "current_post": "柳州市城中区委书记",
        "current_org": "中共柳州市城中区委员会",
        "source": "https://baike.baidu.com/item/%E5%AE%8B%E5%86%9B/57281422"
    },
    {
        "id": 10,
        "name": "莫慧明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-04",
        "birthplace": "广西柳城",
        "education": "在职大学学历",
        "party_join": "2008-04",
        "work_start": "2004-01",
        "current_post": "柳州市城中区政府党组书记、代理区长",
        "current_org": "柳州市城中区人民政府",
        "source": "https://baike.baidu.com/item/%E8%8E%AB%E6%85%A7%E6%98%8E/57616052"
    },
    {
        "id": 11,
        "name": "刘杰华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-05",
        "birthplace": "辽宁北票",
        "education": "在职研究生/工商管理学硕士",
        "party_join": "2002-12",
        "work_start": "2003-07",
        "current_post": "原城中区区长（~2024年离任）",
        "current_org": "",
        "source": "https://www.chengzhong.gov.cn"
    },
]

# =========================================================================
# Data: Organizations
# =========================================================================
organizations = [
    {"id": 1, "name": "中共柳州市柳北区委员会", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会",
     "location": "广西柳州市柳北区"},
    {"id": 2, "name": "柳州市柳北区人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市柳北区"},
    {"id": 3, "name": "中共柳州市城中区委员会", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会",
     "location": "广西柳州市城中区"},
    {"id": 4, "name": "柳州市城中区人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市城中区"},
    {"id": 5, "name": "北海市商务局", "type": "政府", "level": "县处级", "parent": "北海市人民政府",
     "location": "广西北海市"},
    {"id": 6, "name": "合浦县人民政府", "type": "政府", "level": "县处级", "parent": "北海市人民政府",
     "location": "广西北海市合浦县"},
    {"id": 7, "name": "中共北海市委组织部", "type": "党委", "level": "地厅级", "parent": "中共北海市委员会",
     "location": "广西北海市"},
    {"id": 8, "name": "柳州市发展和改革委员会", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市"},
    {"id": 9, "name": "鱼峰区人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市鱼峰区"},
    {"id": 10, "name": "融安县人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市融安县"},
]

# =========================================================================
# Data: Positions
# =========================================================================
positions = [
    # ── Zhou Shuixiang (周水祥) ──
    {"person_id": 1, "org_id": 7, "title": "北海市委组织部（选调生）", "start_date": "2011-07", "end_date": "", "rank": "", "note": "清华大学选调生"},
    {"person_id": 1, "org_id": 6, "title": "合浦县委常委、常务副县长、县委办主任", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "北海市商务局局长、党组书记", "start_date": "", "end_date": "2024-07", "rank": "正县级", "note": "兼市口岸办主任、贸促会会长"},
    {"person_id": 1, "org_id": 4, "title": "城中区委副书记、代区长", "start_date": "2024-07", "end_date": "2024-09", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 4, "title": "城中区委副书记、区长", "start_date": "2024-09-13", "end_date": "2026-06", "rank": "正县级", "note": "2024年9月13日城中区十三届人大五次会议当选"},
    {"person_id": 1, "org_id": 1, "title": "柳北区委书记", "start_date": "2026-06", "end_date": "present", "rank": "副厅级", "note": "2026年6月任前公示"},
]

# =========================================================================
# Data: Relationships
# =========================================================================
relationships = [
    # ── 书记 × 区长 ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "周水祥作为柳北区委书记，洪进兴作为区长，为党政一把手搭档",
     "overlap_org": "中共柳州市柳北区委员会/柳州市柳北区人民政府",
     "overlap_period": "2026-06至今", "confidence": "confirmed"},
    # ── 书记 × 前任城中区搭档 ──
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "周水祥与宋军在城中区党政班子共事，宋军为区委书记",
     "overlap_org": "中共柳州市城中区委员会/柳州市城中区人民政府",
     "overlap_period": "2024-2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "周水祥调任柳北区委书记后，莫慧明接任城中区代理区长",
     "overlap_org": "柳州市城中区人民政府",
     "overlap_period": "2026-07", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor",
     "context": "周水祥接替刘杰华任城中区区长",
     "overlap_org": "柳州市城中区人民政府",
     "overlap_period": "2024-07", "confidence": "confirmed"},
]

# =========================================================================
# Helper functions
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name):
    """Return R,G,B color string based on role."""
    for p in persons:
        if p["name"] == name:
            post = p.get("current_post", "")
            if "书记" in post and "副" not in post:
                return "255,50,50"
            elif "区长" in post:
                return "50,100,255"
            elif "副区长" in post:
                return "50,100,255"
            elif "党组成员" in post:
                return "100,100,100"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
    }
    return colors.get(org_type, "200,200,200")

# =========================================================================
# Build
# =========================================================================
def build():
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

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
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

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
        );

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
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    gexf_lines = []
    gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    gexf_lines.append('    <creator>Gov-Relation Research Agent</creator>')
    gexf_lines.append('    <description>柳北区领导班子关系网络</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')

    # Edge attributes
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('    </attributes>')

    # Nodes - persons
    gexf_lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        size = "20.0" if p["id"] in [1, 2] else "12.0"
        gexf_lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="person"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="4" value="{esc(p.get("source", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        gexf_lines.append(f'        <viz:size value="{size}"/>')
        gexf_lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        c = org_color(o["type"])
        gexf_lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="organization"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(o.get("level", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        gexf_lines.append('        <viz:size value="8.0"/>')
        gexf_lines.append('      </node>')
    gexf_lines.append('    </nodes>')

    # Edges
    gexf_lines.append('    <edges>')
    eid = 0

    # Person -> org (worked_at)
    for pos in positions:
        eid += 1
        gexf_lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    # Person <-> person (relationships)
    for r in relationships:
        eid += 1
        gexf_lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    gexf_lines.append('    </edges>')
    gexf_lines.append('  </graph>')
    gexf_lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(gexf_lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person JSON files ──
    def make_person_json(person, timeline, relationships_list, orgs):
        person_orgs = []
        for pos in timeline:
            for o in orgs:
                if o["id"] == pos["org_id"]:
                    person_orgs.append({"org_id": o["id"], "name": o["name"], "type": o["type"]})
                    break
            else:
                person_orgs.append({"org_id": pos["org_id"], "name": "", "type": ""})

        filtered_sources = [s for s in source_register if s["id"] in [r.get("source_ids", []) for r in relationships_list]]

        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "柳州市",
                "region": "柳北区",
                "job": person["current_post"],
                "task_id": "guangxi_柳北区",
                "time_focus": "2024-2026"
            },
            "identity": {
                "person_id": f"liubei_{person['name']}",
                "name": person["name"],
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": person.get("birth", ""),
                "birthplace": person.get("birthplace", ""),
                "native_place": "",
                "education": [],
                "party_join": person.get("party_join", ""),
                "work_start": person.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{person['name']}_{person.get('birth', '')}",
                    "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                    "official_profile_url": person.get("source", "")
                }
            },
            "current_status": {
                "current_post": person["current_post"],
                "current_org": person["current_org"],
                "administrative_rank": "副厅级（县区委书记）" if "书记" in person["current_post"] and "副" not in person["current_post"] else "正县级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003"]
            },
            "career_timeline": timeline,
            "organizations": person_orgs,
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "cross_city_rotation" if "周水祥" in person["name"] else "unknown",
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
                {"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "confirmed" if person.get("birth") else "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial" if person.get("birth") else "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "洪进兴缺少出生年月、籍贯、教育背景和完整履历信息" if "洪进兴" in person["name"] else "缺少出生年月、籍贯等细节"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{person['name']}的出生年月、籍贯、教育背景" if not person.get("birth") else f"{person['name']}的完整履历",
                    "why_it_matters": "核心身份信息，用于人员去重和履历分析",
                    "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示", f"{person['name']} 百度百科"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": f"{person['name']}的完整履历（此前任职经历）",
                    "why_it_matters": "了解晋升路径和工作交集",
                    "suggested_queries": [f"{person['name']} 曾任", f"{person['name']} 任职经历"],
                    "last_attempted": AS_OF
                }
            ]
        }

    # Build person JSON for 周水祥
    zhou_timeline = [pos for pos in positions if pos["person_id"] == 1]
    zhou_relationships = [r for r in relationships if r["person_a"] == 1 or r["person_b"] == 1]
    zhou_json = make_person_json(persons[0], zhou_timeline, zhou_relationships, organizations)
    zhou_path = os.path.join(PERSONS_DIR, f"{NOW}-广西壮族自治区-柳州市-区委书记-周水祥.json")
    with open(zhou_path, "w", encoding="utf-8") as f:
        json.dump(zhou_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON: {zhou_path}")

    # Build person JSON for 洪进兴
    hong_timeline = []
    hong_relationships = [r for r in relationships if r["person_a"] == 2 or r["person_b"] == 2]
    hong_json = make_person_json(persons[1], hong_timeline, hong_relationships, organizations)
    hong_path = os.path.join(PERSONS_DIR, f"{NOW}-广西壮族自治区-柳州市-区长-洪进兴.json")
    with open(hong_path, "w", encoding="utf-8") as f:
        json.dump(hong_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON: {hong_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
