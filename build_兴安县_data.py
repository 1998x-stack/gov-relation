#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兴安县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 兴安县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-22):
- 县委书记: 陈贤雄 (confirmed via xazf.gov.cn official news, July 2026)
- 县长: 蔡尧 (confirmed via xazf.gov.cn official news, July 2026)

数据来源:
- 兴安县人民政府门户网站 http://www.xazf.gov.cn/
- 公开新闻报道及政府会议报道
- 部分履历信息因网络访问限制标记为 unverified
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "兴安县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈贤雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委书记",
        "current_org": "中共兴安县委员会",
        "source": "confirmed — 兴安县人民政府门户网站 (xazf.gov.cn) 2026年7月多篇会议报道",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "蔡尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委副书记、县长",
        "current_org": "兴安县人民政府",
        "source": "confirmed — 兴安县人民政府门户网站 (xazf.gov.cn) 2026年7月多篇会议报道",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县人大常委会主任",
        "current_org": "兴安县人民代表大会常务委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县政协主席 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县政协主席",
        "current_org": "中国人民政治协商会议兴安县委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委常委、常务副县长",
        "current_org": "兴安县人民政府",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委常委、纪委书记、监委主任",
        "current_org": "中共兴安县纪律检查委员会/兴安县监察委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委常委、组织部部长",
        "current_org": "中共兴安县委员会组织部",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、宣传部部长 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委常委、宣传部部长",
        "current_org": "中共兴安县委员会宣传部",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、政法委书记 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委常委、政法委书记",
        "current_org": "中共兴安县委员会政法委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、统战部部长 (待确认姓名)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴安县委常委、统战部部长",
        "current_org": "中共兴安县委员会统战部",
        "source": "unverified — 需通过政府官网确认",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共兴安县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共桂林市委员会",
        "location": "兴安县",
    },
    {
        "id": 2,
        "name": "兴安县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "桂林市人民政府",
        "location": "兴安县",
    },
    {
        "id": 3,
        "name": "兴安县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "桂林市人民代表大会常务委员会",
        "location": "兴安县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议兴安县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议桂林市委员会",
        "location": "兴安县",
    },
    {
        "id": 5,
        "name": "中共兴安县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共桂林市纪律检查委员会",
        "location": "兴安县",
    },
    {
        "id": 6,
        "name": "中共兴安县委员会组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共兴安县委员会",
        "location": "兴安县",
    },
    {
        "id": 7,
        "name": "中共兴安县委员会宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共兴安县委员会",
        "location": "兴安县",
    },
    {
        "id": 8,
        "name": "中共兴安县委员会政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共兴安县委员会",
        "location": "兴安县",
    },
    {
        "id": 9,
        "name": "中共兴安县委员会统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共兴安县委员会",
        "location": "兴安县",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 陈贤雄
    {"person_id": 1, "org_id": 1, "title": "兴安县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "confirmed via official news"},
    # 蔡尧
    {"person_id": 2, "org_id": 2, "title": "兴安县委副书记、县长", "start": "待查", "end": "present", "rank": "正处级", "note": "confirmed via official news"},
    # 县人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "兴安县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    # 县政协主席
    {"person_id": 4, "org_id": 4, "title": "兴安县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    # 常务副县长
    {"person_id": 5, "org_id": 2, "title": "兴安县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 纪委书记
    {"person_id": 6, "org_id": 5, "title": "兴安县委常委、纪委书记、监委主任", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 组织部部长
    {"person_id": 7, "org_id": 6, "title": "兴安县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 宣传部部长
    {"person_id": 8, "org_id": 7, "title": "兴安县委常委、宣传部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 政法委书记
    {"person_id": 9, "org_id": 8, "title": "兴安县委常委、政法委书记", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 统战部部长
    {"person_id": 10, "org_id": 9, "title": "兴安县委常委、统战部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长为县委、县政府主要领导搭档关系",
        "overlap_org": "中共兴安县委员会/兴安县人民政府",
        "overlap_period": AS_OF,
    },
]

# =========================================================================
# 5. DB & GEXF
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS relationships")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS persons")
    c.execute("DROP TABLE IF EXISTS organizations")

    c.execute("""
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
            source TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
                   pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database: {DB_PATH}")


def person_color(p):
    """Return GEXF color for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post and "政法" not in post and "宣传" not in post and "组织" not in post and "统战" not in post:
        return "255,50,50"   # Red - Party Secretary
    if "县长" in post or "副县长" in post or "区长" in post:
        return "50,100,255"  # Blue - Government
    if "纪委" in post:
        return "255,165,0"   # Orange - Discipline
    return "100,100,100"     # Grey - Others


def org_color(o):
    """Return GEXF color for an organization node."""
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"


def build_gexf():
    priority_names = {"陈贤雄", "蔡尧"}
    is_priority = lambda n: n in priority_names

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>兴安县领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_priority(p["name"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # Person -> Organization (positions)
    for pos in positions:
        p = persons[pos["person_id"] - 1]
        oid = pos["org_id"]
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF: {GEXF_PATH}")


# =========================================================================
# 6. PERSON JSON
# =========================================================================
def write_person_json(person, extra_career=None, extra_relationships=None):
    """Write a per-person graph JSON file."""
    name = person["name"]
    if name == "待查":
        return  # skip unnamed persons

    source_register = [
        {
            "id": "S001",
            "title": "兴安县人民政府门户网站",
            "url": "http://www.xazf.gov.cn/",
            "publisher": "兴安县人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Confirmed current role via multiple news articles"
        }
    ]

    job_short = "县委书记" if "书记" in person["current_post"] and "县长" not in person["current_post"] else "县长"
    filename = f"{AS_OF}-广西壮族自治区-桂林市-{job_short}-{name}.json"

    career_timeline = extra_career if extra_career else [
        {
            "start": "待查",
            "end": "present",
            "org": person["current_org"],
            "title": person["current_post"],
            "level": "正处级",
            "location": "兴安县",
            "system": "party" if "县委" in person["current_org"] else "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "确认在任（截至2026年7月），具体上任时间待查",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        }
    ]

    rels = []
    if extra_relationships:
        rels = extra_relationships
    elif person["id"] == 1:  # 陈贤雄
        rels = [
            {
                "person": "蔡尧",
                "person_id": "guangxi_guilin_xingan_县长_蔡尧",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县委书记与县长在县委常委会和县政府工作中为搭档关系",
                "overlap_org": "中共兴安县委员会/兴安县人民政府",
                "overlap_period": AS_OF,
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ]
    elif person["id"] == 2:  # 蔡尧
        rels = [
            {
                "person": "陈贤雄",
                "person_id": "guangxi_guilin_xingan_县委书记_陈贤雄",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县长与县委书记在县委常委会和县政府工作中为搭档关系",
                "overlap_org": "中共兴安县委员会/兴安县人民政府",
                "overlap_period": AS_OF,
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ]

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "region": "兴安县",
            "job": job_short,
            "task_id": "guangxi_兴安县",
            "time_focus": "2026年7月（当前在任）",
        },
        "identity": {
            "person_id": f"guangxi_guilin_xingan_{job_short}_{name}",
            "name": name,
            "aliases": [],
            "gender": person["gender"] if person["gender"] != "待查" else "",
            "ethnicity": person["ethnicity"] if person["ethnicity"] != "待查" else "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_兴安县",
                "official_profile_url": "http://www.xazf.gov.cn/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [
            {
                "name": person["current_org"],
                "type": "党委" if "县委" in person["current_org"] else "政府",
                "role": person["current_post"],
                "period": f"至{AS_OF}在任",
            }
        ],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "待查",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，公开渠道未发现履职相关的负面信号",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"缺少{name}完整履历，包括出生年月、籍贯、学历、任职经历等",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历（出生年月、籍贯、学历、工作经历）",
                "why_it_matters": "核心领导人物的履历是构建关系网络和进行关联分析的基础",
                "suggested_queries": [
                    f"{name} 简历 兴安县",
                    f"{name} 任前公示 桂林",
                    f"{name} 出生 学历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的上任时间及前任",
                "why_it_matters": "了解领导过渡模式和交流路径",
                "suggested_queries": [
                    f"兴安县 {job_short} 任免 桂林市委",
                    f"兴安县前任{job_short}",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    filepath = os.path.join(PERSONS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Person JSON: {filepath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"=== 兴安县 Data Build ({AS_OF}) ===")
    build_db()
    build_gexf()

    # Person JSONs for core leaders
    chen_extra_career = [
        {
            "start": "待查",
            "end": "待查",
            "org": "兴安县人民政府",
            "title": "兴安县县长",
            "level": "正处级",
            "location": "兴安县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "推测陈贤雄在任县委书记前曾任兴安县县长，需进一步确认",
            "confidence": "unverified",
            "source_ids": [],
        },
        {
            "start": "待查（推测2024-2025年间）",
            "end": "present",
            "org": "中共兴安县委员会",
            "title": "兴安县委书记",
            "level": "正处级",
            "location": "兴安县",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "确认在任（截至2026年7月）",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ]

    cai_extra_career = [
        {
            "start": "待查",
            "end": "present",
            "org": "兴安县人民政府",
            "title": "兴安县委副书记、县长",
            "level": "正处级",
            "location": "兴安县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "确认在任（截至2026年7月）",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ]

    for p in persons:
        name = p["name"]
        if name == "陈贤雄":
            write_person_json(p, extra_career=chen_extra_career)
        elif name == "蔡尧":
            write_person_json(p, extra_career=cai_extra_career)
        elif name != "待查":
            write_person_json(p)

    print("✅ Done.")
